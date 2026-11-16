# Go/No-Go Decision Matrix Guidelines (`high-level-context-planner`)

This reference defines deterministic quality gates and phase transition rules applied by `high-level-context-planner`.

---

## 1. Falsifiability Principle for Quality Gates

Acceptance criteria MUST never rely on subjective checks ("verify it looks good", "test general behavior"). Express every gate as a falsifiable assertion:

- Process exit codes (`$LASTEXITCODE -eq 0` / exit status `0`).
- Physical filesystem existence (`Test-Path` / `Path.is_file()`).
- Required fields and strict schema validation (`Pydantic v2`, `JSON Schema 2020-12`).
- Deterministic pass/fail output from automated test or lint runners.

---

## 2. Canonical Gate Structure

Every planned phase MUST specify:

1. **Go Condition (Approval):** Exact verifiable state authorizing progression to the next phase.
2. **No-Go Condition (Block):** Concrete terminal failure, timeout, or schema violation halting progression.
3. **Contingency Route:** Immediate recovery action preventing blind retry loops:
   - Escalate traceback and diff to `gap-analyzer-auditor` for root-cause analysis.
   - Roll back to the last verified checkpoint.
   - Pause for interactive developer resolution (`ask_question`) on critical `[GAP]`s.

---

## 3. Standard Transition Matrix

| Phase | Go Condition (Pass) | No-Go Condition (Block) | Contingency Route |
| :--- | :--- | :--- | :--- |
| **Phase 0: Prerequisites** | Environment variables verified, target paths validated, and schemas compile cleanly. | Missing dependency, undefined path, or invalid input schema. | Halt and request missing parameters via `ask_question`. |
| **Intermediate Phases** | Command exits `0` and post-mutation Read-After-Write assertion passes. | Compilation error, runtime exception, or data contract breach. | Invoke `gap-analyzer-auditor` with execution trace and logs. |
| **Final Phase: Release** | Full validation suite passes (`validate_skills.py` / `pytest`) with zero regressions. | Schema mismatch, test failure, or unapproved destructive side effect. | Block release and emit convergence gap report. |
