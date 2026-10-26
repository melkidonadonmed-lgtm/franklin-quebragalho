#!/usr/bin/env python3
"""
dag_chain_validator.py
Compilador topológico de ondas (Algoritmo de Kahn), detector de colisões de arquivos
em tarefas paralelas ([P]), validador de higiene de contexto (Context Fork <= 5 regras)
e gerador de envelopes ContextTransitionPayload para skill-orquestrador-planos-encadeados v3.0.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Set, Tuple

from pydantic import BaseModel, ConfigDict, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

MAX_ACTIVE_RULES: int = 5
FORBIDDEN_CONTEXT_KEYS: Tuple[str, ...] = (
    "full_chat_history", "raw_transcript", "entire_conversation", "unfiltered_history",
)


class ContextTransitionEnvelope(BaseModel):
    """Envelope isolado de transição de contexto entre ondas/nós (Zero Context Rot)."""

    model_config = ConfigDict(extra="forbid")

    phase_id: str
    wave_index: int = Field(..., ge=0)
    sequence_index: int = Field(..., ge=0)
    target_skill: str
    cognitive_pattern: str = "CoT"
    isolated_state_key: str
    input_payload: Dict[str, Any] = Field(default_factory=dict)
    active_rules: List[str] = Field(default_factory=list, max_length=MAX_ACTIVE_RULES)
    target_files: List[str] = Field(default_factory=list)
    expected_outputs: List[str] = Field(default_factory=list)
    acceptance_criteria: List[str] = Field(default_factory=list)
    fallback_branch: Optional[str] = None
    status: Literal[
        "PENDING", "IN_PROGRESS", "COMPLETED", "RETRYING", "FALLBACK_ROUTED", "BLOCKED_HITL", "FAILED"
    ] = "PENDING"


class DAGValidationReport(BaseModel):
    """Relatório determinístico da compilação topológica de Kahn e auditoria de colisões."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["[PASS]", "[FAIL]"]
    total_nodes: int
    total_waves: int
    waves: List[List[str]]
    has_cycle: bool
    file_collisions: List[str]
    context_violations: List[str]
    envelopes: List[ContextTransitionEnvelope]


def _normalize_grafo_nodes(grafo: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normaliza nós vindos de CognitiveAdaptivePlan (grafo_execucao)."""
    return [
        {
            "id": str(n.get("etapa_id", f"node_{i}")),
            "skill": str(n.get("responsible_skill", "franklin-main")),
            "cognitive_pattern": str(n.get("padrao_cognitivo", "CoT")),
            "dependencies": list(n.get("precondicoes", [])),
            "active_rules": list(n.get("regras_ativas", [])),
            "rules_count": int(n.get("regras_ativas_count", len(n.get("regras_ativas", [])) or 1)),
            "target_files": list(n.get("target_files", [])),
            "input_payload": dict(n.get("input_payload", {})),
            "expected_outputs": [f"{n.get('etapa_id', f'node_{i}')}_artifact"],
            "acceptance_criteria": [str(n.get("criterio_aceite", "[PASS] Concluído"))],
            "fallback_branch": n.get("ramo_fallback"),
            "is_hitl": n.get("tipo_execucao") == "hitl_gate",
        }
        for i, n in enumerate(grafo)
    ]


def _normalize_task_or_phase_nodes(raw_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normaliza nós vindos de DAGExecutionPlan (tasks) ou lista de fases (phases)."""
    if isinstance(raw_plan.get("tasks"), list):
        out: List[Dict[str, Any]] = []
        for i, t in enumerate(raw_plan["tasks"]):
            payload = t.get("payload", {}) if isinstance(t.get("payload"), dict) else {}
            rules = list(payload.get("active_rules", []))
            out.append({
                "id": str(t.get("id", f"task_{i}")),
                "skill": str(payload.get("skill", t.get("group_id", "franklin-main"))),
                "cognitive_pattern": str(payload.get("cognitive_pattern", "ReAct")),
                "dependencies": list(t.get("dependencies", [])),
                "active_rules": rules,
                "rules_count": len(rules) if rules else 2,
                "target_files": list(payload.get("target_files", [])),
                "input_payload": payload,
                "expected_outputs": list(payload.get("isolated_state_keys", [f"{t.get('id', f'task_{i}')}_out"])),
                "acceptance_criteria": [str(t.get("description", "[PASS] Task concluída"))],
                "fallback_branch": payload.get("fallback_branch"),
                "is_hitl": payload.get("execution_type") == "hitl_gate",
            })
        return out

    phases = raw_plan.get("phases", [])
    if not isinstance(phases, list):
        return []
    result: List[Dict[str, Any]] = []
    for i, p in enumerate(phases):
        pid = str(p.get("phase_id", f"fase_{i}"))
        deps = p.get("depends_on", [])
        dep_list = [deps] if isinstance(deps, str) else list(deps)
        if not dep_list and i > 0 and "depends_on" not in p:
            dep_list = [str(phases[i - 1].get("phase_id", f"fase_{i - 1}"))]
        result.append({
            "id": pid,
            "skill": str(p.get("target_skill", p.get("responsible_skill", "franklin-main"))),
            "cognitive_pattern": str(p.get("cognitive_pattern", "CoT")),
            "dependencies": dep_list,
            "active_rules": list(p.get("context_constraints", []))[:MAX_ACTIVE_RULES],
            "rules_count": len(p.get("context_constraints", [])) or 1,
            "target_files": list(p.get("target_files", [])),
            "input_payload": dict(p.get("input_payload", {})),
            "expected_outputs": list(p.get("expected_outputs", p.get("outputs", [f"{pid}_out"]))),
            "acceptance_criteria": list(p.get("acceptance_criteria", ["[PASS] Fase concluída"])),
            "fallback_branch": p.get("fallback_branch"),
            "is_hitl": False,
        })
    return result


def _normalize_plan_nodes(raw_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normaliza nós de qualquer formato de plano suportado."""
    if isinstance(raw_plan.get("grafo_execucao"), list):
        return _normalize_grafo_nodes(raw_plan["grafo_execucao"])
    return _normalize_task_or_phase_nodes(raw_plan)


def _advance_wave_degrees(
    current_wave: List[str], adj: Dict[str, List[str]], in_degree: Dict[str, int], queue: deque[str]
) -> None:
    """Decrementa o grau de entrada dos vizinhos da onda atual e enfileira nós prontos."""
    for u in current_wave:
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)


def compile_kahn_waves(nodes: List[Dict[str, Any]]) -> Tuple[List[List[str]], bool]:
    """Executa ordenação topológica em ondas paralelas via Algoritmo de Kahn."""
    node_ids = [n["id"] for n in nodes]
    id_set: Set[str] = set(node_ids)
    in_degree: Dict[str, int] = {nid: 0 for nid in node_ids}
    adj: Dict[str, List[str]] = {nid: [] for nid in node_ids}

    for n in nodes:
        nid = n["id"]
        valid_deps = [d for d in n.get("dependencies", []) if d in id_set]
        for dep in valid_deps:
            adj[dep].append(nid)
            in_degree[nid] += 1

    queue: deque[str] = deque([nid for nid in node_ids if in_degree[nid] == 0])
    waves: List[List[str]] = []
    visited = 0

    while queue:
        current_wave = list(queue)
        queue.clear()
        waves.append(current_wave)
        visited += len(current_wave)
        _advance_wave_degrees(current_wave, adj, in_degree, queue)

    return waves, visited != len(node_ids)


def _check_single_wave_collisions(
    w_idx: int, wave: List[str], by_id: Dict[str, Dict[str, Any]]
) -> List[str]:
    """Verifica colisões de arquivos dentro de uma única onda paralela."""
    seen_files: Dict[str, str] = {}
    collisions: List[str] = []
    for nid in wave:
        for fpath in by_id[nid].get("target_files", []):
            norm_f = fpath.strip().lower().replace("\\", "/")
            if norm_f in seen_files:
                collisions.append(
                    f"[FAIL: PARALLEL_FILE_COLLISION] Onda {w_idx}: nós '{seen_files[norm_f]}' e '{nid}' "
                    f"disputam escrita simultânea em '{fpath}'."
                )
            else:
                seen_files[norm_f] = nid
    return collisions


def audit_wave_collisions_and_context(
    nodes: List[Dict[str, Any]], waves: List[List[str]]
) -> Tuple[List[str], List[str]]:
    """Detecta colisões de escrita em arquivos na mesma onda e violações de higiene de contexto."""
    by_id: Dict[str, Dict[str, Any]] = {n["id"]: n for n in nodes}
    collisions: List[str] = []
    context_violations: List[str] = []

    for w_idx, wave in enumerate(waves):
        collisions.extend(_check_single_wave_collisions(w_idx, wave, by_id))

    for n in nodes:
        nid = n["id"]
        rcount = int(n.get("rules_count", len(n.get("active_rules", []))))
        if rcount > MAX_ACTIVE_RULES or len(n.get("active_rules", [])) > MAX_ACTIVE_RULES:
            context_violations.append(
                f"[FAIL: COMPLEXITY_WALL_VIOLATION] Nó '{nid}' possui {rcount} regras ativas (máx: {MAX_ACTIVE_RULES})."
            )
        payload = n.get("input_payload", {})
        bad_keys = [k for k in FORBIDDEN_CONTEXT_KEYS if isinstance(payload, dict) and k in payload]
        for bk in bad_keys:
            context_violations.append(
                f"[FAIL: CONTEXT_ROT_VIOLATION] Nó '{nid}' injeta chave proibida de histórico bruto '{bk}'."
            )

    return collisions, context_violations


def validate_and_compile_plan(raw_plan: Dict[str, Any]) -> DAGValidationReport:
    """Valida um plano completo, compila ondas de Kahn e gera envelopes ContextTransitionEnvelope."""
    nodes = _normalize_plan_nodes(raw_plan)
    if not nodes:
        return DAGValidationReport(
            status="[FAIL]",
            total_nodes=0,
            total_waves=0,
            waves=[],
            has_cycle=False,
            file_collisions=[],
            context_violations=["[FAIL: EMPTY_PLAN] Nenhum nó válido encontrado em grafo_execucao, tasks ou phases."],
            envelopes=[],
        )

    waves, has_cycle = compile_kahn_waves(nodes)
    collisions, ctx_violations = audit_wave_collisions_and_context(nodes, waves)
    by_id: Dict[str, Dict[str, Any]] = {n["id"]: n for n in nodes}

    envelopes: List[ContextTransitionEnvelope] = []
    seq = 0
    for w_idx, wave in enumerate(waves):
        for nid in wave:
            n = by_id[nid]
            rules = list(n.get("active_rules", []))[:MAX_ACTIVE_RULES]
            envelopes.append(
                ContextTransitionEnvelope(
                    phase_id=nid,
                    wave_index=w_idx,
                    sequence_index=seq,
                    target_skill=n["skill"],
                    cognitive_pattern=n.get("cognitive_pattern", "CoT"),
                    isolated_state_key=f"wave{w_idx}_{nid}_state",
                    input_payload=n.get("input_payload", {}),
                    active_rules=rules,
                    target_files=n.get("target_files", []),
                    expected_outputs=n.get("expected_outputs", [f"{nid}_out"]),
                    acceptance_criteria=n.get("acceptance_criteria", ["[PASS] Concluído"]),
                    fallback_branch=n.get("fallback_branch"),
                    status="BLOCKED_HITL" if n.get("is_hitl") else "PENDING",
                )
            )
            seq += 1

    passed = (not has_cycle) and (not collisions) and (not ctx_violations)
    return DAGValidationReport(
        status="[PASS]" if passed else "[FAIL]",
        total_nodes=len(nodes),
        total_waves=len(waves),
        waves=waves,
        has_cycle=has_cycle,
        file_collisions=collisions,
        context_violations=ctx_violations,
        envelopes=envelopes,
    )


def _build_self_test_fixtures() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Retorna os 3 planos de teste (válido em ondas, cíclico e com colisão de escrita)."""
    valid_plan = {
        "grafo_execucao": [
            {"etapa_id": "step_00", "nome": "Fase 0", "regras_ativas_count": 2, "precondicoes": [], "target_files": ["cfg.json"], "criterio_aceite": "[PASS]"},
            {"etapa_id": "step_01a", "nome": "Worker A", "regras_ativas_count": 2, "precondicoes": ["step_00"], "target_files": ["src/a.py"], "criterio_aceite": "[PASS]"},
            {"etapa_id": "step_01b", "nome": "Worker B", "regras_ativas_count": 2, "precondicoes": ["step_00"], "target_files": ["tests/t_a.py"], "criterio_aceite": "[PASS]"},
        ]
    }
    cyclic_plan = {"phases": [{"phase_id": "A", "depends_on": "B"}, {"phase_id": "B", "depends_on": "A"}]}
    collision_plan = {
        "grafo_execucao": [
            {"etapa_id": "p1", "nome": "P1", "precondicoes": [], "target_files": ["shared/same.py"], "regras_ativas_count": 1, "criterio_aceite": "[PASS]"},
            {"etapa_id": "p2", "nome": "P2", "precondicoes": [], "target_files": ["shared/same.py"], "regras_ativas_count": 1, "criterio_aceite": "[PASS]"},
        ]
    }
    return valid_plan, cyclic_plan, collision_plan


def run_self_test() -> int:
    """Executa bateria de auto-testes determinísticos do compilador de ondas DAG."""
    valid_plan, cyclic_plan, collision_plan = _build_self_test_fixtures()
    rep = validate_and_compile_plan(valid_plan)
    assert rep.status == "[PASS]" and rep.total_waves == 2 and rep.waves[1] == ["step_01a", "step_01b"]

    cyc_rep = validate_and_compile_plan(cyclic_plan)
    assert cyc_rep.status == "[FAIL]" and cyc_rep.has_cycle is True

    col_rep = validate_and_compile_plan(collision_plan)
    assert col_rep.status == "[FAIL]" and len(col_rep.file_collisions) == 1

    print(json.dumps({
        "status": "[PASS]",
        "engine": "dag_chain_validator v3.0.0",
        "kahn_waves_verified": True,
        "collision_detection_verified": True,
        "cycle_detection_verified": True,
        "tests_passed": 3,
    }, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    """Ponto de entrada CLI do validador e compilador de ondas DAG."""
    parser = argparse.ArgumentParser(description="Compilador de Ondas DAG (Kahn) e Validador de Context Fork v3.0.")
    parser.add_argument("--plan", type=str, default="", help="Caminho para arquivo JSON do plano ou JSON inline.")
    parser.add_argument("--self-test", action="store_true", help="Executa auto-teste determinístico.")
    args = parser.parse_args()

    if args.self_test or not args.plan.strip():
        return run_self_test()

    plan_arg = args.plan.strip()
    fpath = Path(plan_arg)
    raw_plan = json.loads(fpath.read_text(encoding="utf-8")) if fpath.is_file() else json.loads(plan_arg)
    report = validate_and_compile_plan(raw_plan)
    print(report.model_dump_json(indent=2))
    return 0 if report.status == "[PASS]" else 1


if __name__ == "__main__":
    sys.exit(main())
