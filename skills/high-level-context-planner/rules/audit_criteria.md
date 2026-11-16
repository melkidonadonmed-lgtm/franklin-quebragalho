# Deterministic Audit & Rejection Criteria (`high-level-context-planner` v3.0.0)

This specification defines falsifiable compliance gates for plans emitted by `high-level-context-planner`. Every verification MUST output one deterministic marker:

- `[PASS]`: Requirement verified against schema rules and actual disk/input artifacts.
- `[FAIL]`: Requirement violated with an explicit defect reason.
- `[UNVERIFIED]`: Cannot be verified due to missing briefing inputs.

---

### Rule 1: 4-Quadrant Intent Triage & Framework Selection

- **Criterion**: Does the plan classify the request into one of the 4 quadrants (`direta`, `estruturada`, `ambigua`, `mutacao_critica_hitl`) and pair a structural framework (`CLAREZA`, `CREATE`, `RTF`, `TAG`, `TASS`) with non-linear cognitive patterns (`CoT`, `ReAct`, `ToT`, `Self-Refine`)?
- **Test**: Both `intencao` and `frameworks_selecionados` blocks are present and consistent with task complexity.
- **Result**:
  - Intent classified and frameworks explicitly declared -> `[PASS]`
  - Missing intent diagnosis or blind linear plan under uncertainty -> `[FAIL: Missing intent diagnosis or framework selection]`

---

### Rule 2: Complexity Wall Shielding (`<= 5` Active Rules per Node)

- **Criterion**: Does every node in `grafo_execucao` obey `regras_ativas_count <= 5`?
- **Test**: `scripts/cognitive_plan_builder.py` validates `max_regras_por_no <= 5` with status `SHIELDED` or `SUBDIVIDED`.
- **Result**:
  - All execution nodes remain at `<= 5` active rules -> `[PASS]`
  - Any node holds `> 5` simultaneous constraints without splitting -> `[FAIL: Prompt Complexity Wall violation (> 5 rules/node)]`

---

### Rule 3: Mandatory Phase 0 & Non-Linear Fallback Branches

- **Criterion**: Does the execution graph start at Phase 0 (precondition, schema, and L1/L2 hygiene verification) and declare `ramo_fallback` recovery routes on failure-prone nodes?
- **Test**: First node is `step_00_fase_zero` and critical nodes specify `ramo_fallback` and falsifiable acceptance criteria.
- **Result**:
  - Begins with Phase 0 and defines fallback branches -> `[PASS]`
  - Skips Phase 0 or omits contingency routing -> `[FAIL: Missing mandatory Phase 0 or fallback branch]`

---

### Rule 4: Falsifiable Decomposition, `[ID] [P?] [US#]` Notation & Zero File Collisions

- **Criterion**: Do all phases define tasks using `[ID] [P?] [US#] exact/path.ext` and objective Go/No-Go criteria?
- **Test**: Parallel `[P]` tasks touch strictly disjoint `target_files` without write contention.
- **Result**:
  - Exact file paths, objective gates, and disjoint parallel files -> `[PASS]`
  - Vague criteria or two parallel `[P]` tasks editing the same file -> `[FAIL: Missing exact task paths or parallel file collision]`

---

### Rule 5: Full Hand-Off Consumption & Append-Only Convergence

- **Criterion**: When fed a YAML hand-off payload from `gap-analyzer-auditor`, did the revised plan incorporate every adjustment in **Append-Only** mode?
- **Test**: The v2.0+ plan appends `APPEND_CONVERGENCE_TASKS` without erasing or renumbering already completed tasks.
- **Result**:
  - All mitigations appended while preserving completed history -> `[PASS]`
  - Ignored hand-off instructions or destructively rewrote completed tasks -> `[FAIL: Hand-off violation or destructive history rewrite]`

---

### Rule 6: HITL Gate on Critical Mutations & `Complexity Tracking` (YAGNI)

- **Criterion**: Do `mutacao_critica_hitl` intents enforce `requer_hitl: true` with a `hitl_gate` node, and does the Markdown plan justify any extra abstractions in a `Complexity Tracking` table?
- **Test**: No direct disk mutations executed during planning; irreversible operations gated by HITL; YAGNI justification documented.
- **Result**:
  - HITL gate enforced and `Complexity Tracking` included -> `[PASS]`
  - Omitted HITL gate on destructive actions or unjustified over-engineering -> `[FAIL: HITL security breach or YAGNI violation]`
