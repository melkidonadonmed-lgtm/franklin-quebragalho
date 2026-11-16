---
name: chained-plan-orchestrator
description: "Compile execution plans into topological DAG waves using Kahn's algorithm, prevent parallel file-write collisions, isolate worker state via Context Fork (<= 5 rules), and dispatch sequential waves with HITL checkpoints. Use when orchestrating multi-skill DAG pipelines. Do NOT use for single-turn tasks or initial Phase 0 planning from scratch."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  author: "Franklin"
  version: "3.0.0"
  updated_at: "2026-11-16"
  category: "DAG Orchestration & Context Fork Dispatch"
  tags: ["chained-plan-orchestrator", "orquestracao", "orquestrador", "ondas", "dag", "kahn", "context-fork", "planos-encadeados", "multiagente", "fan-out", "hitl"]
---

# `chained-plan-orchestrator` (`v3.0.0`) — Kahn DAG & Context Fork

## 1. Overview & Scope

Executive engine for **Kahn Topological Wave Compilation**, strict **Context Fork** isolation (`<= 5` rules/node), and sequential wave fan-out/fan-in via `invoke_subagent` or `franklin_execute_dag`.

### When NOT to Use
- **Single-Turn Tasks:** Execute atomic single-skill requests directly.
- **Initial Phase 0 Planning:** Delegate intent triage and plan drafting to `high-level-context-planner`.
- **Root-Cause Failure Diagnostics:** Escalate unrecovered trace failures to `gap-analyzer-auditor`.

## 2. Inputs & Prerequisites

- **`structured_plan` (required):** `CognitiveAdaptivePlan` (`grafo_execucao`), `DAGExecutionPlan` (`tasks`), or `phases` JSON.
- **`execution_mode` (optional):** `native_subagents`, `franklin_dag`, or `step_by_step`.
- **`max_retries` (optional):** Retries before `fallback_branch` or `gap-analyzer-auditor` escalation (default: `1`).

## 3. Step-by-Step Procedure

Consult [`dag_stages_and_context_fork.md`](references/dag_stages_and_context_fork.md) and [`context_transition_schema.json`](references/context_transition_schema.json):

1. **Stage 1 — Kahn & Guards:** Block unresolved `[GAP]`s, reject cycles (`CYCLE_DETECTED`), block same-wave `target_files` collisions (`PARALLEL_FILE_COLLISION`), and verify skill slugs.
2. **Stage 2 — Context Fork (`<= 5` rules):** Build lean `ContextTransitionEnvelope` payloads with unique `isolated_state_key` (never pass raw history).
3. **Stage 3 — Pre-Flight CLI Validation:** Run before dispatching waves:

```powershell
uv run python skills/chained-plan-orchestrator/scripts/dag_chain_validator.py --self-test
uv run python skills/chained-plan-orchestrator/scripts/dag_chain_validator.py --plan plans/distributed_agent_mediation_dag.json
```

4. **Stages 4–5 — Dispatch, HITL & Read-After-Write:** Execute `Wave 0..N`, hold `hitl_gate` nodes in `BLOCKED_HITL` via `franklin_harness_guard` / `franklin_harness_checkpoint`, route faults to `fallback_branch`, and verify post-conditions.

## 4. Gotchas & Edge Cases

- **Zero Context Rot:** Reject `full_chat_history`, `raw_transcript`, `entire_conversation`, or `unfiltered_history`.
- **No Write Contention or HITL Bypass:** Serialize colliding `[P]` nodes before dispatch; never advance `BLOCKED_HITL` without an `approval_token`.

## 5. Output Schema & Validation Criteria

1. **Kahn Wave Topology (`Wave 0..N`):** `DAGValidationReport` (`status: "[PASS]"`, `has_cycle: false`, `file_collisions: []`) + envelopes matching [`context_transition_schema.json`](references/context_transition_schema.json).
2. **Traceability Matrix:** `Wave | Node | Skill | Cognitive Pattern | Rules (<=5) | Status` per [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

All internal DAG payloads and Context Fork envelopes MUST stay in Technical English; however, **all user-facing wave progress updates, HITL pause prompts, fallback notices, and Self-Refine summaries MUST be communicated in Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.
