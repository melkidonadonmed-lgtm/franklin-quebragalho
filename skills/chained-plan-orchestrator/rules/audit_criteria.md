# Deterministic DAG Orchestration & Compilation Criteria (`chained-plan-orchestrator` v3.0.0)

To guarantee cycle-free wave compilation, parallel write safety, and zero context rot, every orchestration run is evaluated against these deterministic rules:

- `[PASS]`: Requirement verified by `scripts/dag_chain_validator.py` and disk/runtime checks.
- `[FAIL]`: Requirement violated, blocking wave dispatch immediately.
- `[UNVERIFIED]`: Cannot be verified due to missing input plan artifacts.

---

### Rule 1: Kahn Topological Ordering & Acyclicity (DAG)

- **Criterion**: Does the input plan form a valid Directed Acyclic Graph compilable into sequential parallel waves (`Wave 0..Wave N`)?
- **Test**: `scripts/dag_chain_validator.py` confirms `has_cycle == False` and groups all nodes into valid topological waves.
- **Result**:
  - Strict topological ordering verified -> `[PASS]`
  - Circular dependency detected -> `[FAIL: Circular dependency loop detected (CYCLE_DETECTED)]`

---

### Rule 2: Parallel Write Collision Guard (`[P]`)

- **Criterion**: Do all nodes scheduled in the same parallel wave (`Wave K`) operate on strictly disjoint `target_files`?
- **Test**: No two parallel subagents or tasks in the same wave write to the same file path.
- **Result**:
  - `file_collisions` list is empty -> `[PASS]`
  - Overlapping `target_files` inside the same wave -> `[FAIL: Parallel file-write collision detected (PARALLEL_FILE_COLLISION)]`

---

### Rule 3: Strict Context Fork Isolation & `<= 5` Active Rules Cap

- **Criterion**: Does each `ContextTransitionEnvelope` carry only task-specific `input_payload`, a unique `isolated_state_key`, and at most 5 active rules (`active_rules <= 5`)?
- **Test**: Forbidden raw history keys (`full_chat_history`, `raw_transcript`, `entire_conversation`, `unfiltered_history`) are absent and no node exceeds 5 rules.
- **Result**:
  - Isolated, typed payload respecting `<= 5` active rules -> `[PASS]`
  - Raw conversation history injected or `> 5` rules on a node -> `[FAIL: Context hygiene or Prompt Complexity Wall violation]`

---

### Rule 4: Non-Linear Fallback Routing & Read-After-Write Verification

- **Criterion**: Is every wave deliverable physically verified (Read-After-Write) before advancing, routing recoverable errors to `fallback_branch`?
- **Test**: Node outputs satisfy `acceptance_criteria` or deterministically trigger `RETRYING` / `FALLBACK_ROUTED`.
- **Result**:
  - Post-condition verified with measurable evidence -> `[PASS]`
  - Failed after retry without an active recovery branch -> `[FAIL: Acceptance criteria unmet]`

---

### Rule 5: Human-in-the-Loop Safeguards (`BLOCKED_HITL`)

- **Criterion**: Are `hitl_gate` nodes and destructive mutations paused in `BLOCKED_HITL` pending explicit human confirmation?
- **Test**: Critical mutations require an active harness checkpoint (`franklin_harness_checkpoint`) and valid `approval_token` before execution.
- **Result**:
  - All HITL stop gates respected -> `[PASS]`
  - Destructive action executed without human approval -> `[FAIL: HITL safeguard violation]`
