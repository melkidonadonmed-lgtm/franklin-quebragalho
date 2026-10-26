#!/usr/bin/env python3
"""
cognitive_plan_builder.py
Motor determinístico de Diagnóstico de Intenção, Seleção de Frameworks (CLAREZA, CREATE,
RTF, TAG, TASS + CoT, ReAct, ToT, Self-Refine), Blindagem contra a Parede de Complexidade
(<= 5 regras ativas por nó) e Exportação para DAGExecutionPlan (Epic-Volta).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field, model_validator

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

MAX_RULES_PER_NODE: int = 5

IntentCategory = Literal["direta", "estruturada", "ambigua", "mutacao_critica_hitl"]
StructuralFramework = Literal["CLAREZA", "CREATE", "RTF", "TAG", "TASS"]
CognitivePattern = Literal["CoT", "ReAct", "ToT", "Self-Refine"]
ExecutionType = Literal["model_reasoning", "tool_io", "decision_gate", "deterministic_code", "hitl_gate"]

HITL_KEYWORDS: Tuple[str, ...] = (
    "deletar", "apagar", "excluir", "remove-item", "rm -rf", "drop table",
    "truncate", "deploy", "produção", "producao", "pagar", "transferir", "formatar",
)
AMBIGUOUS_KEYWORDS: Tuple[str, ...] = (
    "tenho uma ideia", "me ajude a pensar", "como posso criar", "explorar",
    "brainstorm", "do zero", "sugira", "o que acha",
)
STRUCTURED_KEYWORDS: Tuple[str, ...] = (
    "refatorar", "migrar", "implementar", "arquitetura", "pipeline", "fases",
    "múltiplos", "multiplos", "sistema", "auditar", "suíte", "suite", "integrar",
)


class IntentDiagnosis(BaseModel):
    """Diagnóstico estruturado da intenção em 4 quadrantes operacionais."""

    model_config = ConfigDict(extra="forbid")

    categoria: IntentCategory
    diagnostico: str = Field(..., min_length=5)
    requer_hitl: bool = False


class SelectedFrameworks(BaseModel):
    """Combinação de framework estrutural de entrega e padrões cognitivos não-lineares."""

    model_config = ConfigDict(extra="forbid")

    estrutural: StructuralFramework
    cognitivo: List[CognitivePattern] = Field(..., min_length=1)


class ComplexityShieldReport(BaseModel):
    """Relatório de blindagem contra a Parede de Complexidade de Prompts."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["SHIELDED", "SUBDIVIDED", "VIOLATION"] = "SHIELDED"
    max_regras_por_no: int = Field(..., ge=1, le=MAX_RULES_PER_NODE)
    disclosure_tier: Literal[1, 2, 3] = 2
    estrategia: str


class ExecutionNode(BaseModel):
    """Nó atômico do grafo de execução não-linear com teto estrito de <= 5 regras."""

    model_config = ConfigDict(extra="forbid")

    etapa_id: str = Field(..., min_length=2)
    nome: str = Field(..., min_length=3)
    responsible_skill: str = "high-level-context-planner"
    tipo_execucao: ExecutionType = "model_reasoning"
    padrao_cognitivo: CognitivePattern = "CoT"
    regras_ativas_count: int = Field(..., ge=1, le=MAX_RULES_PER_NODE)
    regras_ativas: List[str] = Field(default_factory=list)
    precondicoes: List[str] = Field(default_factory=list)
    target_files: List[str] = Field(default_factory=list)
    criterio_aceite: str = Field(..., min_length=3)
    ramo_fallback: Optional[str] = None

    @model_validator(mode="after")
    def _check_rules_consistency(self) -> "ExecutionNode":
        if self.regras_ativas and len(self.regras_ativas) > MAX_RULES_PER_NODE:
            raise ValueError(
                f"Nó '{self.etapa_id}' viola a Parede de Complexidade: "
                f"{len(self.regras_ativas)} regras ativas (máximo permitido: {MAX_RULES_PER_NODE})."
            )
        if self.regras_ativas and self.regras_ativas_count != len(self.regras_ativas):
            self.regras_ativas_count = len(self.regras_ativas)
        return self


class CognitiveAdaptivePlan(BaseModel):
    """Contrato completo do Plano Adaptativo Executável (v3.0.0)."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str
    version: str = "3.0.0"
    target_orchestrator: str = "skill-orquestrador-planos-encadeados"
    strategic_goal: str
    intencao: IntentDiagnosis
    frameworks_selecionados: SelectedFrameworks
    blindagem_complexidade: ComplexityShieldReport
    grafo_execucao: List[ExecutionNode] = Field(..., min_length=1)


def classify_intent_and_frameworks(
    query: str, override_framework: Optional[str] = None
) -> Tuple[IntentDiagnosis, SelectedFrameworks]:
    """Classifica a intenção nos 4 quadrantes e seleciona os frameworks ideais."""
    q_low = query.strip().lower()
    is_hitl = any(k in q_low for k in HITL_KEYWORDS)
    is_ambiguous = any(k in q_low for k in AMBIGUOUS_KEYWORDS)
    is_structured = any(k in q_low for k in STRUCTURED_KEYWORDS) or len(query.split()) > 14

    if is_hitl:
        intent = IntentDiagnosis(
            categoria="mutacao_critica_hitl",
            diagnostico="Operação com risco de mutação crítica/irreversível detectada; requer Gate HITL.",
            requer_hitl=True,
        )
        fw_struct: StructuralFramework = "CLAREZA"
        fw_cog: List[CognitivePattern] = ["CoT", "ReAct", "Self-Refine"]
    elif is_ambiguous:
        intent = IntentDiagnosis(
            categoria="ambigua",
            diagnostico="Demanda exploratória ou aberta; requer geração e poda de hipóteses arquiteturais.",
            requer_hitl=False,
        )
        fw_struct = "CREATE"
        fw_cog = ["ToT", "CoT", "Self-Refine"]
    elif is_structured:
        intent = IntentDiagnosis(
            categoria="estruturada",
            diagnostico="Demanda técnica multifacetada com dependências entre etapas, ferramentas e validação.",
            requer_hitl=False,
        )
        fw_struct = "CLAREZA"
        fw_cog = ["CoT", "ReAct", "ToT", "Self-Refine"]
    else:
        intent = IntentDiagnosis(
            categoria="direta",
            diagnostico="Comando pontual de baixa entropia; execução direta sem burocracia multifásica.",
            requer_hitl=False,
        )
        fw_struct = "TAG"
        fw_cog = ["CoT"]

    if override_framework in ("CLAREZA", "CREATE", "RTF", "TAG", "TASS"):
        fw_struct = override_framework  # type: ignore[assignment]

    return intent, SelectedFrameworks(estrutural=fw_struct, cognitivo=fw_cog)


def subdivide_overloaded_nodes(raw_nodes: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], bool]:
    """Subdivide automaticamente nós que acumulam > 5 regras ativas (Prompt Complexity Wall Shield)."""
    shielded: List[Dict[str, Any]] = []
    was_subdivided = False

    for node in raw_nodes:
        rules = list(node.get("regras_ativas", []))
        count = int(node.get("regras_ativas_count", len(rules) or 2))
        if len(rules) <= MAX_RULES_PER_NODE and count <= MAX_RULES_PER_NODE:
            node_copy = dict(node)
            node_copy["regras_ativas_count"] = len(rules) if rules else count
            shielded.append(node_copy)
            continue

        was_subdivided = True
        if not rules:
            rules = [f"Regra operacional #{i + 1}" for i in range(count)]

        chunks = [rules[i : i + MAX_RULES_PER_NODE] for i in range(0, len(rules), MAX_RULES_PER_NODE)]
        prev_deps = list(node.get("precondicoes", []))
        base_id = str(node.get("etapa_id", "step"))
        base_name = str(node.get("nome", "Etapa"))

        for idx, chunk in enumerate(chunks, start=1):
            sub_id = f"{base_id}_p{idx}"
            sub_node = dict(node)
            sub_node["etapa_id"] = sub_id
            sub_node["nome"] = f"{base_name} (Sub-nó Atômico {idx}/{len(chunks)})"
            sub_node["regras_ativas"] = chunk
            sub_node["regras_ativas_count"] = len(chunk)
            sub_node["precondicoes"] = prev_deps
            shielded.append(sub_node)
            prev_deps = [sub_id]

    return shielded, was_subdivided


def _build_core_discovery_nodes() -> List[ExecutionNode]:
    """Constrói os nós iniciais de Fase 0, exploração ReAct e decisão ToT."""
    return [
        ExecutionNode(
            etapa_id="step_00_fase_zero",
            nome="Fase 0: Diagnóstico de Pré-condições, Schemas e Higiene L1/L2",
            responsible_skill="high-level-context-planner",
            tipo_execucao="model_reasoning",
            padrao_cognitivo="CoT",
            regras_ativas_count=3,
            regras_ativas=[
                "Validar insumos e caminhos reais no disco",
                "Garantir <= 5 regras ativas por nó (Complexity Wall Shield)",
                "Confirmar ausência de ciclos de dependência",
            ],
            precondicoes=[],
            criterio_aceite="[PASS] Pré-requisitos e contratos Pydantic v2 validados",
            ramo_fallback="step_00_clarify_inputs",
        ),
        ExecutionNode(
            etapa_id="step_01_exploracao_react",
            nome="Fase 1: Coleta de Evidências e Interação com Ferramentas",
            responsible_skill="auditoria-projetos-sistema",
            tipo_execucao="tool_io",
            padrao_cognitivo="ReAct",
            regras_ativas_count=3,
            regras_ativas=[
                "Intercalar Thought -> Tool Call -> Observation",
                "Isolar estado em Context Fork sem histórico bruto",
                "Capturar evidências verificáveis ([FATO] vs [LACUNA])",
            ],
            precondicoes=["step_00_fase_zero"],
            criterio_aceite="[PASS] Evidências coletadas sem overflow de contexto",
            ramo_fallback="step_01_alternative_source",
        ),
        ExecutionNode(
            etapa_id="step_02_decisao_tot",
            nome="Fase 2: Bifurcação Arquitetural e Seleção de Abordagem",
            responsible_skill="high-level-context-planner",
            tipo_execucao="decision_gate",
            padrao_cognitivo="ToT",
            regras_ativas_count=3,
            regras_ativas=[
                "Comparar Opção 1 (Cirúrgica) vs Opção 2 (Estrutural)",
                "Podar ramos que violem YAGNI ou parem no No-Go",
                "Garantir tasks [P] em arquivos disjuntos",
            ],
            precondicoes=["step_01_exploracao_react"],
            criterio_aceite="[PASS] Ramo vencedor selecionado com Complexity Tracking validado",
            ramo_fallback="step_02_recalibrate_branches",
        ),
    ]


def build_default_nodes(intent: IntentDiagnosis) -> List[ExecutionNode]:
    """Constrói os nós canônicos do grafo não-linear conforme a categoria da intenção."""
    nodes = _build_core_discovery_nodes()
    prev_id = "step_02_decisao_tot"
    if intent.requer_hitl:
        nodes.append(
            ExecutionNode(
                etapa_id="step_02_hitl_gate",
                nome="Fase 2.5: Portão de Aprovação Humana Obrigatória (HITL)",
                responsible_skill="skill-orquestrador-planos-encadeados",
                tipo_execucao="hitl_gate",
                padrao_cognitivo="ReAct",
                regras_ativas_count=2,
                regras_ativas=[
                    "Pausar mutação crítica e serializar checkpoint",
                    "Exigir approval_token e idempotency_key antes de prosseguir",
                ],
                precondicoes=[prev_id],
                criterio_aceite="[PASS] Aprovação humana explícita registrada no Harness",
                ramo_fallback="step_abort_safe_rollback",
            )
        )
        prev_id = "step_02_hitl_gate"

    nodes.append(
        ExecutionNode(
            etapa_id="step_03_validacao_self_refine",
            nome="Fase 3: Verificação Determinística e Ciclo Self-Refine",
            responsible_skill="code-acceptability-auditor",
            tipo_execucao="deterministic_code",
            padrao_cognitivo="Self-Refine",
            regras_ativas_count=3,
            regras_ativas=[
                "Executar Gerador -> Crítico AST/Testes -> Refinador",
                "Confirmar Quality Score >= 75 e suíte pytest 100% PASS",
                "Se falhar após retry, emitir Hand-off para gap-analyzer-auditor",
            ],
            precondicoes=[prev_id],
            criterio_aceite="[PASS] 100% dos testes e critérios Go/No-Go aprovados",
            ramo_fallback="step_04_gap_analyzer_handoff",
        )
    )
    return nodes


def build_cognitive_plan(
    query: str, override_framework: Optional[str] = None, plan_id: str = "plan-cognitive-001"
) -> CognitiveAdaptivePlan:
    """Gera um Plano Adaptativo Executável completo a partir de uma meta."""
    intent, frameworks = classify_intent_and_frameworks(query, override_framework)
    nodes = build_default_nodes(intent)
    max_rules = max(n.regras_ativas_count for n in nodes)
    tier: Literal[1, 2, 3] = 1 if intent.categoria == "direta" else (3 if intent.requer_hitl else 2)
    shield = ComplexityShieldReport(
        status="SHIELDED",
        max_regras_por_no=max_rules,
        disclosure_tier=tier,
        estrategia=f"Decomposição atômica em {len(nodes)} nós independentes (<= {MAX_RULES_PER_NODE} regras/nó) com divulgação L1->L2->L3",
    )
    return CognitiveAdaptivePlan(
        plan_id=plan_id,
        strategic_goal=query.strip(),
        intencao=intent,
        frameworks_selecionados=frameworks,
        blindagem_complexidade=shield,
        grafo_execucao=nodes,
    )


def convert_to_epic_volta_dag(plan: CognitiveAdaptivePlan) -> Dict[str, Any]:
    """Converte o CognitiveAdaptivePlan para o contrato DAGExecutionPlan do motor Epic-Volta."""
    tasks: List[Dict[str, Any]] = []
    for node in plan.grafo_execucao:
        tasks.append({
            "id": node.etapa_id,
            "group_id": node.padrao_cognitivo.lower().replace("-", "_"),
            "description": f"{node.nome} [{node.padrao_cognitivo} | {node.regras_ativas_count} regras]",
            "dependencies": node.precondicoes,
            "criticality": "HIGH" if plan.intencao.requer_hitl or "fase_zero" in node.etapa_id else "MEDIUM",
            "payload": {
                "skill": node.responsible_skill,
                "execution_type": node.tipo_execucao,
                "cognitive_pattern": node.padrao_cognitivo,
                "active_rules": node.regras_ativas,
                "target_files": node.target_files,
                "fallback_branch": node.ramo_fallback,
            },
        })
    return {
        "objective": plan.strategic_goal,
        "acceptance_criteria": [n.criterio_aceite for n in plan.grafo_execucao],
        "tasks": tasks,
    }


def run_self_test() -> int:
    """Executa bateria de auto-testes determinísticos do motor cognitivo."""
    plan = build_cognitive_plan("Refatorar módulo de autenticação OAuth2 e auditar testes em múltiplas fases")
    assert plan.intencao.categoria == "estruturada"
    assert plan.frameworks_selecionados.estrutural == "CLAREZA"
    assert plan.blindagem_complexidade.max_regras_por_no <= MAX_RULES_PER_NODE

    hitl_plan = build_cognitive_plan("Deletar tabelas antigas do banco de produção e executar deploy")
    assert hitl_plan.intencao.categoria == "mutacao_critica_hitl"
    assert hitl_plan.intencao.requer_hitl is True
    assert any(n.tipo_execucao == "hitl_gate" for n in hitl_plan.grafo_execucao)

    overloaded = [{
        "etapa_id": "step_overload",
        "nome": "Nó Sobrecarregado",
        "regras_ativas": [f"Regra {i}" for i in range(8)],
        "regras_ativas_count": 8,
        "precondicoes": [],
        "criterio_aceite": "[PASS] Subdividido",
    }]
    sub_nodes, was_sub = subdivide_overloaded_nodes(overloaded)
    assert was_sub is True and len(sub_nodes) == 2
    assert all(n["regras_ativas_count"] <= MAX_RULES_PER_NODE for n in sub_nodes)

    dag = convert_to_epic_volta_dag(plan)
    assert "tasks" in dag and len(dag["tasks"]) == len(plan.grafo_execucao)

    print(json.dumps({
        "status": "[PASS]",
        "engine": "cognitive_plan_builder v3.0.0",
        "max_rules_per_node_enforced": MAX_RULES_PER_NODE,
        "tests_passed": 4,
    }, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    """Ponto de entrada CLI do construtor e validador de planos cognitivos."""
    parser = argparse.ArgumentParser(description="Motor Cognitivo de Intenção e Planejamento Não-Linear v3.0.")
    parser.add_argument("--intent", type=str, default="", help="Intenção ou meta para gerar plano adaptativo.")
    parser.add_argument("--framework", type=str, default="", help="Override opcional de framework (CLAREZA, CREATE, RTF, TAG, TASS).")
    parser.add_argument("--validate-file", type=str, default="", help="Arquivo JSON de plano cognitivo a validar.")
    parser.add_argument("--export-dag", type=str, default="", help="Caminho opcional para exportar DAGExecutionPlan.")
    parser.add_argument("--self-test", action="store_true", help="Executa auto-teste determinístico.")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if args.validate_file:
        fpath = Path(args.validate_file).resolve()
        if not fpath.is_file():
            print(json.dumps({"status": "[FAIL]", "error": f"Arquivo não encontrado: {fpath}"}, ensure_ascii=False))
            return 1
        raw_data = json.loads(fpath.read_text(encoding="utf-8"))
        if isinstance(raw_data.get("grafo_execucao"), list):
            sub_nodes, was_sub = subdivide_overloaded_nodes(raw_data["grafo_execucao"])
            raw_data["grafo_execucao"] = sub_nodes
            if was_sub and isinstance(raw_data.get("blindagem_complexidade"), dict):
                raw_data["blindagem_complexidade"]["status"] = "SUBDIVIDED"
        validated = CognitiveAdaptivePlan.model_validate(raw_data)
        if args.export_dag:
            dag_out = convert_to_epic_volta_dag(validated)
            Path(args.export_dag).write_text(json.dumps(dag_out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(validated.model_dump_json(indent=2))
        return 0

    query = args.intent.strip() or "Estruturar plano técnico multifásico com validação AST e testes"
    plan = build_cognitive_plan(query, override_framework=args.framework.strip() or None)
    if args.export_dag:
        dag_out = convert_to_epic_volta_dag(plan)
        Path(args.export_dag).write_text(json.dumps(dag_out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(plan.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
