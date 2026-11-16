# Intent Quadrants, Frameworks & Complexity Shielding (`high-level-context-planner`)

Detailed reference complementing [`SKILL.md`](../SKILL.md), [`go_no_go_decision_matrix.md`](go_no_go_decision_matrix.md), [`handoff_consumption_protocol.md`](handoff_consumption_protocol.md), and [`context_plan_schema.json`](context_plan_schema.json).

## 1. Four-Quadrant Intent Matrix

| Category | Definition | Dispatch Strategy | Cognitive Pattern |
| :--- | :--- | :--- | :--- |
| **`1. direta`** | Single unambiguous query or isolated quick edit | Direct execution without multi-phase overhead | `Zero-Shot` / lightweight `CoT` |
| **`2. estruturada`** | Multi-module technical task with dependencies | DAG graph with Phase 0, `[ID] [P?] [US#]`, and `ramo_fallback` | `ReAct` or `CoT` + `ToT` |
| **`3. ambigua`** | Exploratory demand or critical missing specs | Competing hypotheses, scope pruning, and MVP framing | `CREATE` + `ToT` |
| **`4. mutacao_critica_hitl`** | Destructive action, DB drop/alter, deploy, or secrets | Immediate pause + checkpoint (`requer_hitl: true`) | `ReAct` + Approval Gate |

## 2. Structural Frameworks & Cognitive Patterns

- **Structural Frameworks:** `CLAREZA` (code & zero-hallucination audits), `CREATE` (ideation/SPEC/MVP), `RTF` (tables/extractions), `TAG` (direct automations), `TASS` (executive docs).
- **Cognitive Patterns:** `CoT` (causal step chains), `ReAct` (Thought -> Tool -> Observation), `ToT` (competing Option 1 vs. Option 2 branches + Go/No-Go pruning), `Self-Refine` (criteria verification).

## 3. Four Safeguards Against Prompt Complexity Wall & Destructive Rewrites

1. **Cap `regras_ativas_count <= 5` per node:** Automatically subdivide overloaded steps into `step_02_p1` / `step_02_p2` when rules exceed 5.
2. **Progressive Disclosure (`L1 -> L2 -> L3`):** Keep L1 discovery compact, load L2 active phase rules only, and fetch L3 schemas/scripts on demand.
3. **Hard Constraints in Code:** Enforce invariants deterministically via `Pydantic v2 extra="forbid"` inside `scripts/cognitive_plan_builder.py`.
4. **Context Fork `[P]` + Append-Only (`/speckit-converge`):** Restrict parallel `[P]` tasks to disjoint files; never rewrite completed `[x] T001` items—append `## Phase N: Convergence & Mitigation` with `- [ ] T0XX [P] [CONV] exact/path.ext`.
