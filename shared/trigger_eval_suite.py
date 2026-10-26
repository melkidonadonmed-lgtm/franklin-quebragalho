"""
trigger_eval_suite.py
Suíte Determinística de Avaliação de Disparo Nível 1 (Should-Trigger vs. Near-Misses)
para as 25 Agent Skills Canônicas do Franklin Quebra-Galho.

Objetivo:
Validar matematicamente que as descrições do Nível 1 (<available_skills>) e o motor
de ranqueamento (rank_skills_for_query) atingem 100% de Top-1 Accuracy nos casos
should-trigger e 100% de rejeição nos casos near-miss (incluindo cláusulas negativas
'não use para ...').
"""

from __future__ import annotations

from typing import Dict, List, Literal
from pydantic import BaseModel, ConfigDict, Field

from shared.catalog_service import rank_skills_for_query


class TriggerEvalCase(BaseModel):
    """Caso individual de avaliação Should-Trigger e Near-Miss."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    case_id: str
    cluster: str
    query: str
    expected_skill: str
    near_miss_skills: List[str] = Field(default_factory=list)
    case_type: Literal["should_trigger", "negative_clause_near_miss"] = "should_trigger"
    rationale: str


class TriggerCaseOutcome(BaseModel):
    """Resultado determinístico da execução de um TriggerEvalCase."""

    model_config = ConfigDict(extra="forbid")

    case_id: str
    query: str
    expected_skill: str
    top1_skill: str
    top1_score: int
    expected_skill_score: int
    top3_skills: List[str]
    near_miss_scores: Dict[str, int]
    passed_top1: bool
    passed_near_miss: bool


class TriggerEvalReport(BaseModel):
    """Relatório consolidado de precisão, recall, F1 e rejeição de near-misses."""

    model_config = ConfigDict(extra="forbid")

    total_cases: int
    covered_skills_count: int
    top1_hits: int
    top3_hits: int
    near_miss_rejections: int
    top1_accuracy: float = Field(ge=0.0, le=1.0)
    top3_recall: float = Field(ge=0.0, le=1.0)
    near_miss_rejection_rate: float = Field(ge=0.0, le=1.0)
    f1_score: float = Field(ge=0.0, le=1.0)
    status: Literal["[PASS]", "[FAIL]"]
    outcomes: List[TriggerCaseOutcome]
    failures: List[str]


CANONICAL_TRIGGER_EVAL_CASES: List[TriggerEvalCase] = [
    # Cluster 1: Prompts, Entropia, Soluções & Sentinela de Contexto
    TriggerEvalCase(
        case_id="TRG-01",
        cluster="Prompts & Contexto",
        query="auditar factibilidade FATO INFERÊNCIA LACUNA, modular entropia e refinar prompt sob Zero-Trust XML OWASP LLM 2026",
        expected_skill="refine-prompt",
        near_miss_skills=["arquiteto-conteudo-solucoes", "context-sentinel"],
        rationale="Disparo direto por auditoria epistêmica, modulação de entropia e Zero-Trust XML.",
    ),
    TriggerEvalCase(
        case_id="TRG-02",
        cluster="Prompts & Contexto",
        query="desenhar soluções técnicas, biblioteca de prompts enterprise, código tipado e roadmaps em 4 modos com 7 Módulos de Guardrails",
        expected_skill="arquiteto-conteudo-solucoes",
        near_miss_skills=["refine-prompt", "high-level-context-planner"],
        rationale="Disparo de arquitetura autônoma de soluções e roadmaps em 4 modos.",
    ),
    TriggerEvalCase(
        case_id="TRG-03",
        cluster="Prompts & Contexto",
        query="auditoria epistêmica isolada de prompt e modulação de entropia socrática",
        expected_skill="refine-prompt",
        near_miss_skills=["arquiteto-conteudo-solucoes"],
        case_type="negative_clause_near_miss",
        rationale="Cláusula negativa em arquiteto-conteudo-solucoes ('não use para auditoria epistêmica isolada') deve penalizá-la em favor de refine-prompt.",
    ),
    TriggerEvalCase(
        case_id="TRG-04",
        cluster="Prompts & Contexto",
        query="auditar integridade da janela de contexto em conversas multi-turn e extrair estado estruturado da sessão em SQLite ou JSON",
        expected_skill="context-sentinel",
        near_miss_skills=["refine-prompt", "curadoria-obsidian-vault"],
        rationale="Sentinela de janela de contexto multi-turn vs. refinador de prompt isolado.",
    ),
    # Cluster 2: Engenharia Frontend, UI/UX, DESIGN.md & Interface Médica
    TriggerEvalCase(
        case_id="TRG-05",
        cluster="Frontend & UI",
        query="criar ou atualizar o contrato DESIGN.md na raiz do projeto definindo tokens semânticos e escala tipográfica modular",
        expected_skill="design-md",
        near_miss_skills=["frontend-code-architect", "frontend-ui-ux-auditor"],
        rationale="Autoria do contrato DESIGN.md vs. implementação de componentes.",
    ),
    TriggerEvalCase(
        case_id="TRG-06",
        cluster="Frontend & UI",
        query="implementar e refatorar interfaces web React Next.js Tailwind consumindo o contrato DESIGN.md com estados finitos FSM",
        expected_skill="frontend-code-architect",
        near_miss_skills=["design-md", "frontend-testing-auditor", "auditoria-projetos-sistema"],
        rationale="Implementação/refatoração de código frontend (auditoria-projetos-sistema tem cláusula 'não use para refatorar código').",
    ),
    TriggerEvalCase(
        case_id="TRG-07",
        cluster="Frontend & UI",
        query="auditar qualidade de interfaces web via audit_tactile_ui.py verificando WAI-ARIA, zero emojis, zero bloat Base64 e anti-XSS",
        expected_skill="frontend-testing-auditor",
        near_miss_skills=["frontend-ui-ux-auditor", "frontend-code-architect"],
        rationale="Auditoria determinística via audit_tactile_ui.py (Base64, XSS, WAI-ARIA).",
    ),
    TriggerEvalCase(
        case_id="TRG-08",
        cluster="Frontend & UI",
        query="auditar com precisão matemática densidade de nós DOM, contraste WCAG 2.1 AA, física da luz 135 e elevação por sombras",
        expected_skill="frontend-ui-ux-auditor",
        near_miss_skills=["frontend-testing-auditor", "design-md"],
        rationale="Auditoria óptica/matemática de densidade DOM, física da luz 135° e sombras.",
    ),
    TriggerEvalCase(
        case_id="TRG-09",
        cluster="Frontend & UI",
        query="arquitetura para interfaces clínicas, prontuários eletrônicos PEP, receituários laudos A4 .sus-grid e calculadoras médicas",
        expected_skill="design-interface-medica-minimalista",
        near_miss_skills=["design-md", "frontend-code-architect"],
        rationale="Especialista em interface clínica, PEP, .sus-grid e proteção de unidades de dose.",
    ),
    # Cluster 3: Google Drive, Disco Local Windows & Obsidian Vault
    TriggerEvalCase(
        case_id="TRG-10",
        cluster="Drive, Disco & Vault",
        query="auditar e higienizar Google Drive detectando arquivos pesados >100MB, duplicatas por hash e pastas vazias órfãs com Dry-run",
        expected_skill="gdrive-auditoria-limpeza",
        near_miss_skills=["gdrive-taxonomia-organizacao", "manutencao-disco-windows"],
        rationale="Limpeza de pesados/duplicatas no Drive vs. taxonomia de pastas ou disco Windows local.",
    ),
    TriggerEvalCase(
        case_id="TRG-11",
        cluster="Drive, Disco & Vault",
        query="estruturar e categorizar pastas no Google Drive aplicando taxonomia canônica numerada e padronização de datas ISO YYYY-MM-DD",
        expected_skill="gdrive-taxonomia-organizacao",
        near_miss_skills=["gdrive-auditoria-limpeza", "organizador-fluxo-arvore-arquivos"],
        rationale="Taxonomia canônica numerada e datas ISO no Google Drive.",
    ),
    TriggerEvalCase(
        case_id="TRG-12",
        cluster="Drive, Disco & Vault",
        query="manutenção de arquivos locais no Windows 11 Downloads e Desktop isolando instaladores antigos e resíduos temporários",
        expected_skill="manutencao-disco-windows",
        near_miss_skills=["gdrive-auditoria-limpeza", "refine-prompt"],
        case_type="negative_clause_near_miss",
        rationale="Manutenção de pastas locais no Windows (refine-prompt possui cláusula 'Não use para manutenção de arquivos locais').",
    ),
    TriggerEvalCase(
        case_id="TRG-13",
        cluster="Drive, Disco & Vault",
        query="auditar e higienizar o cofre do Obsidian validando frontmatter YAML, links bidirecionais Wikilinks e MemPalace wing notes",
        expected_skill="curadoria-obsidian-vault",
        near_miss_skills=["redator-tecnico-markdown", "manutencao-disco-windows"],
        rationale="Curadoria estrutural do Obsidian Vault e sincronização MemPalace.",
    ),
    # Cluster 4: Qualidade de Código AST, Suítes de Testes & Física 3D
    TriggerEvalCase(
        case_id="TRG-14",
        cluster="Código, Testes & 3D",
        query="auditar estaticamente arquivos Python via AST contra eval/exec, shell=True, ausência de type hints e funções longas >60 linhas",
        expected_skill="code-acceptability-auditor",
        near_miss_skills=["test-quality-auditor", "auditoria-projetos-sistema"],
        rationale="Auditor AST de aceitabilidade de código Python (Quality Score 0-100).",
    ),
    TriggerEvalCase(
        case_id="TRG-15",
        cluster="Código, Testes & 3D",
        query="auditoria de suítes de testes em 5 módulos Python TS Go MCP e Harness detectando Green Build Illusion e falhas AAA",
        expected_skill="test-quality-auditor",
        near_miss_skills=["code-acceptability-auditor", "code-quality-audit-3d-physics"],
        rationale="Auditor de qualidade de testes (Green Build Illusion, AAA, grading.json).",
    ),
    TriggerEvalCase(
        case_id="TRG-16",
        cluster="Código, Testes & 3D",
        query="auditar e sanitizar código de Física 3D, Computação Gráfica WebGL Three.js Babylon.js, shaders, colisões e nota Snorm Pass@10",
        expected_skill="code-quality-audit-3d-physics",
        near_miss_skills=["code-acceptability-auditor", "test-quality-auditor"],
        rationale="Auditoria especializada em motores 3D, shaders, colisões e simulação numérica.",
    ),
    # Cluster 5: Planejamento Fase 0, Gap Analysis (RCA) & Orquestração DAG
    TriggerEvalCase(
        case_id="TRG-17",
        cluster="Planejamento & Loop Fechado",
        query="planejador de contexto de alto nível decompondo metas em fases numeradas com Fase 0, tasks paralelizáveis e Complexity Tracking",
        expected_skill="high-level-context-planner",
        near_miss_skills=["skill-orquestrador-planos-encadeados", "gap-analyzer-auditor"],
        rationale="Decomposição estratégica em Fase 0 e Complexity Tracking (Plano v2.0).",
    ),
    TriggerEvalCase(
        case_id="TRG-18",
        cluster="Planejamento & Loop Fechado",
        query="analista de brechas RCA e convergência Spec-to-Code inspecionando logs e traces para emitir Hand-off Payload YAML",
        expected_skill="gap-analyzer-auditor",
        near_miss_skills=["high-level-context-planner", "auditoria-projetos-sistema"],
        rationale="Análise de causa-raiz (RCA) sobre logs/traces e Hand-off Payload YAML.",
    ),
    TriggerEvalCase(
        case_id="TRG-19",
        cluster="Planejamento & Loop Fechado",
        query="orquestrador executivo de planos encadeados DAG mapeando dependências entre skills especialistas e executando ondas sequenciais",
        expected_skill="skill-orquestrador-planos-encadeados",
        near_miss_skills=["high-level-context-planner", "gap-analyzer-auditor"],
        rationale="Execução de ondas DAG encadeadas com isolamento de estado compartilhado.",
    ),
    # Cluster 6: Organização de Projetos, Diagnóstico de MVP & Arquitetura de Ilhas
    TriggerEvalCase(
        case_id="TRG-20",
        cluster="Projetos, MVP & Arquitetura",
        query="auditoria arquitetural e diagnóstico de MVP para Antigravity varrendo CONTEXT.md, AGENTS.md, SPEC.md e README.md isoladamente",
        expected_skill="antigravity-project-auditor",
        near_miss_skills=["auditoria-projetos-sistema", "organizador-projetos-ideias"],
        rationale="Diagnóstico read-only de MVP e arquivos base para Antigravity.",
    ),
    TriggerEvalCase(
        case_id="TRG-21",
        cluster="Projetos, MVP & Arquitetura",
        query="auditar integridade estrutural de repositórios, código órfão e esteira dinâmica via agent-browser @eX com nota de 0 a 100",
        expected_skill="auditoria-projetos-sistema",
        near_miss_skills=["antigravity-project-auditor", "frontend-testing-auditor"],
        rationale="Auditoria estrutural 0-100 combinada com esteira dinâmica agent-browser (@eX).",
    ),
    TriggerEvalCase(
        case_id="TRG-22",
        cluster="Projetos, MVP & Arquitetura",
        query="organizar ideias do zero com perguntas guiadas e sugestão de MVP ou reestruturar README.md fiel ao disco e contratos MCP tools.json",
        expected_skill="organizador-projetos-ideias",
        near_miss_skills=["antigravity-project-auditor", "organizador-fluxo-arvore-arquivos"],
        rationale="Ideação guiada do zero ou reestruturação de README.md e contratos MCP/FastAPI.",
    ),
    TriggerEvalCase(
        case_id="TRG-23",
        cluster="Projetos, MVP & Arquitetura",
        query="arquitetura em Ilhas Funcionais Island UI/UX, auditoria de navegação real Clicar em X ativa Y, Dead Ends, suficiência funcional e score determinístico SGA V1 vs V2 em HTML",
        expected_skill="nav-x-func",
        near_miss_skills=["design-md", "auditoria-projetos-sistema"],
        rationale="Aglomeração funcional por ilhas (Island UI/UX), navegação real (X ativa Y), suficiência funcional (TIF) e score comparativo V1 vs V2.",
    ),
    # Cluster 7: Documentos Markdown, Conversão PDF & Fluxos Mermaid
    TriggerEvalCase(
        case_id="TRG-24",
        cluster="Documentos & Diagramas",
        query="redigir relatórios executivos, notas técnicas e atas de decisão em Markdown com caixas de alerta GitHub e Google Style Guides",
        expected_skill="redator-tecnico-markdown",
        near_miss_skills=["conversor-html-pdf", "curadoria-obsidian-vault"],
        rationale="Redação técnica em Markdown com alertas GitHub e Google Style Guides.",
    ),
    TriggerEvalCase(
        case_id="TRG-25",
        cluster="Documentos & Diagramas",
        query="converter documentos Markdown e HTML para arquivos PDF profissionais via Microsoft Edge ou Chrome headless com CSS de impressão",
        expected_skill="conversor-html-pdf",
        near_miss_skills=["redator-tecnico-markdown", "organizador-fluxo-arvore-arquivos"],
        rationale="Conversão de Markdown/HTML para PDF via Edge/Chrome headless.",
    ),
    TriggerEvalCase(
        case_id="TRG-26",
        cluster="Documentos & Diagramas",
        query="transformar ideias brutas e requisitos de apps em fluxos visuais Mermaid e árvores de diretórios comentadas",
        expected_skill="organizador-fluxo-arvore-arquivos",
        near_miss_skills=["organizador-projetos-ideias", "redator-tecnico-markdown"],
        rationale="Geração de fluxos Mermaid e árvores de diretórios comentadas.",
    ),
    TriggerEvalCase(
        case_id="TRG-27",
        cluster="Código, Testes & 3D",
        query="auditar sistemas agênticos, servidores MCP 2026-07-28 STDIO stdout, nós A2A agent-card JWS, higiene de binários, travas max_steps e persistir memories/audit_report.json",
        expected_skill="agent-server-auditor",
        near_miss_skills=["antigravity-project-auditor", "test-quality-auditor", "code-acceptability-auditor"],
        rationale="Auditoria arquitetural de agentes, servidores MCP STDIO, A2A agent-card JWS e snapshot memories/audit_report.json.",
    ),
]


def _evaluate_single_case(case: TriggerEvalCase) -> TriggerCaseOutcome:
    """Executa o ranqueamento Nível 1 para um caso e verifica Top-1 e rejeição de near-misses."""
    ranked = rank_skills_for_query(case.query, limit=30)
    score_by_name: Dict[str, int] = {item[1]["name"]: item[0] for item in ranked}
    top3_names = [item[1]["name"] for item in ranked[:3]]
    top1_name = top3_names[0] if top3_names else ""
    top1_score = ranked[0][0] if ranked else 0
    expected_score = score_by_name.get(case.expected_skill, 0)

    near_miss_scores = {nm: score_by_name.get(nm, 0) for nm in case.near_miss_skills}
    passed_top1 = top1_name == case.expected_skill and expected_score > 0
    passed_near_miss = all(expected_score > nm_score for nm_score in near_miss_scores.values())

    return TriggerCaseOutcome(
        case_id=case.case_id,
        query=case.query,
        expected_skill=case.expected_skill,
        top1_skill=top1_name,
        top1_score=top1_score,
        expected_skill_score=expected_score,
        top3_skills=top3_names,
        near_miss_scores=near_miss_scores,
        passed_top1=passed_top1,
        passed_near_miss=passed_near_miss,
    )


def run_trigger_eval_suite(cases: List[TriggerEvalCase] | None = None) -> TriggerEvalReport:
    """Executa toda a bateria Should-Trigger vs. Near-Miss e calcula métricas determinísticas."""
    active_cases = cases if cases is not None else CANONICAL_TRIGGER_EVAL_CASES
    outcomes: List[TriggerCaseOutcome] = []
    failures: List[str] = []
    top1_hits = 0
    top3_hits = 0
    nm_rejections = 0

    for c in active_cases:
        out = _evaluate_single_case(c)
        outcomes.append(out)
        if out.passed_top1:
            top1_hits += 1
        else:
            failures.append(
                f"[{c.case_id}] Top-1 incorreto para '{c.expected_skill}': obteve '{out.top1_skill}' ({out.top1_score} pts vs {out.expected_skill_score} pts)"
            )
        if c.expected_skill in out.top3_skills:
            top3_hits += 1
        if out.passed_near_miss:
            nm_rejections += 1
        else:
            failures.append(
                f"[{c.case_id}] Falha de separação Near-Miss para '{c.expected_skill}' ({out.expected_skill_score} pts): {out.near_miss_scores}"
            )

    total = max(1, len(active_cases))
    precision = round(top1_hits / total, 4)
    recall = round(top3_hits / total, 4)
    nm_rate = round(nm_rejections / total, 4)
    f1 = round((2 * precision * nm_rate) / (precision + nm_rate), 4) if (precision + nm_rate) > 0 else 0.0
    covered_skills = len({c.expected_skill for c in active_cases})
    status: Literal["[PASS]", "[FAIL]"] = "[PASS]" if not failures else "[FAIL]"

    return TriggerEvalReport(
        total_cases=len(active_cases),
        covered_skills_count=covered_skills,
        top1_hits=top1_hits,
        top3_hits=top3_hits,
        near_miss_rejections=nm_rejections,
        top1_accuracy=precision,
        top3_recall=recall,
        near_miss_rejection_rate=nm_rate,
        f1_score=f1,
        status=status,
        outcomes=outcomes,
        failures=failures,
    )
