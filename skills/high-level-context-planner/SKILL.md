---
name: high-level-context-planner
description: "Decompose complex goals into cognitive Phase 0 plans with 4-quadrant intent triage, parallelizable [ID] [P?] [US#] tasks, Go/No-Go matrices, and Complexity Tracking (<= 5 rules per node). Use when planning multi-phase epics or consuming RCA hand-offs. Do NOT use for single-turn tasks, raw log RCA (gap-analyzer-auditor), or executing Kahn DAG waves (chained-plan-orchestrator)."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  author: "Franklin"
  version: "3.0.0"
  updated_at: "2026-11-16"
  category: "Intent Triage & Cognitive Planning"
  tags: ["high-level-context-planner", "planejamento", "planejador", "fase", "fase-0", "complexidade", "complexity-tracking", "intent-triage", "cot-tot", "react", "append-only", "convergencia", "go-no-go", "dag"]
---

# `high-level-context-planner` (`v3.0.0`) — Phase 0 & Complexity Shield

## 1. Overview & Scope

Cognitive planner for 4-quadrant intent triage, **Complexity Wall Shielding** (`<= 5` rules/node), Phase 0 `[ID] [P?] [US#]` plans, Go/No-Go matrices, and append-only `/speckit-converge` re-planning from `gap-analyzer-auditor` hand-offs.

### When NOT to Use
- **Single-Turn Commands (`direta`):** Deliver directly without multi-phase planning.
- **Forensic Log RCA:** Route trace diagnostics first to `gap-analyzer-auditor`.
- **DAG Wave Dispatch:** Route Kahn compilation and fan-out to `chained-plan-orchestrator`.

## 2. Inputs & Prerequisites

- **`strategic_goal` / `user_query` (required):** Epic, feature goal, or raw spec.
- **`handoff_payload` (conditional):** YAML adjustments per [`handoff_consumption_protocol.md`](references/handoff_consumption_protocol.md).
- **`operational_constraints` (optional):** Paths, runtime limits, `MAX_RULES_PER_NODE = 5`.

## 3. Step-by-Step Procedure

Consult [`planner_frameworks_and_quadrants.md`](references/planner_frameworks_and_quadrants.md) and [`go_no_go_decision_matrix.md`](references/go_no_go_decision_matrix.md):

1. **Intent Triage:** Classify as `direta`, `estruturada`, `ambigua` (resolve `[GAP]`s first), or `mutacao_critica_hitl` (`requer_hitl: true`).
2. **Framework Synthesis:** Pair structural (`CLAREZA`, `CREATE`, `RTF`, `TAG`, `TASS`) + cognitive (`CoT`, `ReAct`, `ToT`, `Self-Refine`).
3. **Complexity Wall & Phase 0:** Cap `regras_ativas_count <= 5` (split overloaded nodes), anchor on `step_00_fase_zero` + `ramo_fallback`, keep `[P]` files disjoint, and apply `/speckit-converge` append-only.
4. **CLI Verification:** Validate deterministically against [`rules/audit_criteria.md`](rules/audit_criteria.md):

```powershell
uv run python skills/high-level-context-planner/scripts/cognitive_plan_builder.py --self-test
uv run python skills/high-level-context-planner/scripts/cognitive_plan_builder.py --intent "<goal>" --framework CLAREZA
uv run python skills/high-level-context-planner/scripts/cognitive_plan_builder.py --validate-file plan.json --export-dag dag_plan.json
```

## 4. Gotchas & Edge Cases

- **No Blind Linear Plans:** Empirical uncertainty requires `ReAct`/`ToT` + `ramo_fallback`.
- **No Write Collisions or Rewrites:** Keep `[P]` `target_files` disjoint; never erase completed tasks; retain `hitl_gate` when `requer_hitl: true`.

## 5. Output Schema & Validation Criteria

1. **JSON Plan:** Matches [`context_plan_schema.json`](references/context_plan_schema.json) (`max_regras_por_no <= 5`, `target_orchestrator: "chained-plan-orchestrator"`).
2. **Markdown Plan:** Mermaid `flowchart TD`, `[ID] [P?] [US#]` checklist, Go/No-Go Matrix, `Complexity Tracking`, and `[PASS]`/`[FAIL]` status per [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

Internal schemas and JSON contracts stay in Technical English; **all user-facing plan walkthroughs, Phase 0 clarifications, Go/No-Go rationales, and Self-Refine summaries MUST be delivered in Portuguese (Brazil / `pt-BR`)**, unless requested otherwise.
