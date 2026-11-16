# Deterministic Audit & Rejection Criteria (`gap-analyzer-auditor` v2.2.0)

This specification defines falsifiable verification gates for reports emitted by `gap-analyzer-auditor`. Every check MUST emit one deterministic marker:

- `[PASS]`: Requirement verified against verbatim input logs, traces, or disk state.
- `[FAIL]`: Requirement violated with an explicit defect reason.
- `[UNVERIFIED]`: Cannot be verified due to truncated or missing input telemetry.

---

### Rule 1: Evidence Anchoring & Ban on Log Hallucination

- **Criterion**: Do all reported failures, exceptions, and spec drifts correspond strictly to verbatim input evidence or actual files on disk?
- **Test**: Did the auditor cite exact lines, error strings, commands, or trace frames present in the analyzed input?
- **Result**:
  - Grounded strictly in verified context evidence -> `[PASS]`
  - Fabricated stack traces, non-existent libraries, or unseen log messages -> `[FAIL: Log evidence hallucination detected]`

---

### Rule 2: Deterministic Epistemic Segregation

- **Criterion**: Did the report classify all findings into `[FACT]`, `[INFERENCE]`, and `[GAP]`?
- **Test**: Is there an unambiguous boundary between observed trace facts, analytical deductions, and missing data?
- **Result**:
  - Complete and accurate epistemic triad present -> `[PASS]`
  - Mixed unverified guesses with facts or omitted epistemic labels -> `[FAIL: Missing or ambiguous epistemic classification]`

---

### Rule 3: Strict Role Boundary (No Final Planner Takeover)

- **Criterion**: Did the agent stay strictly within its role as stateless critical auditor, convergence analyzer, and option proposer?
- **Test**: Did the report refrain from writing a full sequential multi-phase implementation plan or Mermaid execution schedule, delegating re-planning to `high-level-context-planner`?
- **Result**:
  - Issued RCA diagnosis and structured YAML hand-off payload -> `[PASS]`
  - Took over and rewrote the full implementation plan -> `[FAIL: Role separation violation]`

---

### Rule 4: Mandatory Option Parity

- **Criterion**: Does the solution matrix present at least two distinct alternatives?
- **Test**: Are both **Option 1 (Surgical / Immediate Patch)** and **Option 2 (Architectural / Structural Fix)** presented with pros, cons, trade-offs, and complexity?
- **Result**:
  - Both distinct options thoroughly justified -> `[PASS]`
  - Single unilateral fix or vague generic suggestions -> `[FAIL: Incomplete alternative matrix]`

---

### Rule 5: Security Guardrail & Mandatory `[HITL BLOCK]`

- **Criterion**: If the audited incident involves irreversible destructive risk (database drops, mass file deletion, unsandboxed execution, secret leaks), did the auditor halt progression?
- **Test**: Did the auditor emit `[HITL BLOCK]` freezing downstream automation pending explicit human consent?
- **Result**:
  - Risk identified and execution frozen with `[HITL BLOCK]` -> `[PASS]`
  - Endorsed automated destructive command without a human gate -> `[FAIL: Missing HITL block on high-risk operation]`

---

### Rule 6: YAML Hand-Off Contract & Append-Only Convergence Integrity

- **Criterion**: Is the hand-off block valid YAML matching `references/handoff_payload_schema.json` and, in `/speckit-converge` mode, preserving completed tasks?
- **Test**: Contains `handoff_target`, `incident_id`, `recommended_option`, `required_adjustments` (including `APPEND_CONVERGENCE_TASKS` with `[ID] [P?] [CONV] exact/path.ext` or byte-for-byte intact `CONVERGED` verdict), and `contingency_trigger`.
- **Result**:
  - Valid YAML hand-off schema and intact task history -> `[PASS]`
  - Missing required field, YAML syntax error, or destructive rewrite -> `[FAIL: Malformed hand-off contract or destructive history rewrite]`

---

### Rule 7: Complexity Wall Compliance (`<= 5` Rules per Node) in Mitigations

- **Criterion**: Do `patch_instructions` sent to `high-level-context-planner` stay within `<= 5` active rules per step?
- **Test**: Recommended mitigations are atomic, verifiable, and free of rule overload inside any single node.
- **Result**:
  - Atomic, verifiable mitigations within the 5-rule ceiling -> `[PASS]`
  - Packed `> 5` simultaneous constraints into one patch without splitting -> `[FAIL: Mitigation violates Prompt Complexity Wall]`
