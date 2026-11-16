# Harness Test Quality Engineering Dossier (`shared/harness.py` & `Eval-Driven Harness`)

Specifies **Module 5 (`harness_test_auditor.py` $\leftrightarrow$ `evals/modules/harness_evals.json`)** of `test-quality-auditor` (`v1.3.0`), auditing suites that verify **Operational Governance Harnesses (Zero-Trust / HITL)** and **Data-Driven Eval Harnesses**.

---

## 1. Module 1: Green Build Illusion in Harness Tests

In agentic systems, the **Harness** is the critical containment boundary preventing destructive execution (`Remove-Item -Recurse -Force`, `DROP TABLE`), Prompt Injection, or unverified skill approvals. A *Green Build Illusion* inside a Harness test compromises the entire safety plane:

1. **Semantic Guard Tested Only on Happy-Path (`HARNESS_WEAK_INJECTION_GUARD_TEST` — `-50 pts`)**:
   - Passes injection payload (`"Ignore all previous instructions"`) to `SemanticGuard.sanitize_input(...)` without requiring `pytest.raises(SecurityViolationError)` or status `"BLOCKED"`.
2. **HITL Policy Gate Missing Critical Risk Check (`HARNESS_UNVERIFIED_RISK_TRANSITION` — `-45 pts`)**:
   - Passes destructive command (`Remove-Item -Recurse -Force` or `rm -rf`) to `evaluate_action_risk()` / `franklin_harness_guard()` but checks only `len(reason) > 0` without asserting `risk == RiskLevel.CRITICAL` or `status == "APPROVAL_REQUIRED"`.
3. **Production Checkpoint Store Pollution (`HARNESS_MISSING_TEARDOWN_CLEANUP` — `-35 pts`)**:
   - Instantiates `CheckpointStore` on the default production file without `tmp_path` (`t.TempDir()`) or `try...finally` `clear()`, polluting `.context/checkpoints.json`.
4. **Incomplete HITL Lifecycle (`HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE` — `-25 pts`)**:
   - Calls only `store.create(...)` without verifying disk persistence (`.get()` / `.list()`) or status transition (`PENDING` $\rightarrow$ `APPROVED` / `REJECTED`) via `.update_status()`.
5. **Eval Harness Test Missing Evidence or Delta (`HARNESS_EVAL_MISSING_EVIDENCE_OR_DELTA` — `-35 pts`)**:
   - Invokes `run_eval_harness()` yet asserts only `"grading_path" in res`, ignoring `pass_rate == 1.0`, non-empty `evidence`, and `delta["pass_rate_gain"] > 0`.

---

## 2. Module 2: AAA Anatomy for Harness Tests

| AAA Stage | Deterministic Requirement in Harness Test Suites |
| :--- | :--- |
| **1. ARRANGE (Isolation & Adversarial Vectors)** | Instantiate `CheckpointStore(tmp_path / "checkpoints.json")` in an isolated temp dir. Prepare deterministic test matrix covering `LOW`, `MEDIUM`, `CRITICAL` risks and adversarial Prompt Injection / control bytes (`\x00-\x1f`). |
| **2. ACT (Trigger Guard / Eval Runner)** | Execute `SemanticGuard.sanitize_input()`, `evaluate_action_risk()`, `create()` $\rightarrow$ `get()` $\rightarrow$ `update_status()` $\rightarrow$ `clear()`, or `run_eval_harness(skill_root, eval_module=...)`. |
| **3. ASSERT (Zero-Trust Invariants & Delta)** | Require `with pytest.raises(SecurityViolationError):`, exact `RiskLevel` assertions, JSON disk persistence parity, and `pass_rate == 1.0` + `pass_rate_gain > 0` across mirrored modules. |

---

## 3. Module 3: `harness_test_auditor.py` Anomaly Taxonomy

| Rule ID | Severity | Penalty | Deterministic Trigger |
| :--- | :---: | :---: | :--- |
| `HARNESS_WEAK_INJECTION_GUARD_TEST` | Critical | `-50 pts` | `SemanticGuard` / `sanitize_input` with injection payload lacking `pytest.raises(SecurityViolationError)` or `"BLOCKED"`. |
| `HARNESS_UNVERIFIED_RISK_TRANSITION` | Critical | `-45 pts` | `evaluate_action_risk` / `franklin_harness_guard` with destructive command lacking `RiskLevel.CRITICAL` or `"APPROVAL_REQUIRED"`. |
| `HARNESS_MISSING_TEARDOWN_CLEANUP` | High | `-35 pts` | Checkpoint creation without `tmp_path`, `TempDir(`, `tempfile`, or `try...finally`. |
| `HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE` | Medium | `-25 pts` | `CheckpointStore.create()` without verifying `.get()` / `.list()` or `.update_status()`. |
| `HARNESS_EVAL_MISSING_EVIDENCE_OR_DELTA` | High | `-35 pts` | `run_eval_harness()` call without checking `pass_rate`, `pass_rate_gain`, `evidence`, or `failed`. |

---

## 4. Module 4: Harness Test Quality Spectrum (Levels 1 to 4)

- **Level 1: Illusory / Placebo (`0–25 pts`)**: Supplies injection payload without expecting an exception and passes destructive commands without asserting `RiskLevel.CRITICAL`.
- **Level 2: Superficial / Fragile (`26–55 pts`)**: Leaks checkpoints into production storage without `tmp_path` and checks only `store.create()`.
- **Level 3: Rigid Functional (`56–80 pts`)**: Calls `run_eval_harness()` without validating `pass_rate_gain` or per-case `evidence`.
- **Level 4: Deterministic & Resilient (`81–100 pts`)**: Isolates persistence in `tmp_path`, validates control-char stripping, enforces `SecurityViolationError` on injections, proves `LOW`/`MEDIUM`/`CRITICAL`, exercises full `PENDING` $\rightarrow$ `APPROVED` $\rightarrow$ `clear()`, and validates all 5 mirrors in `evals/modules/*_evals.json`.

---

## 5. Module 5: Surgical Refactoring (Before vs. After)

### BEFORE (Level 1/2 — Rejected at `-85 pts`)

```python
def test_harness_insecure():
    # Missing pytest.raises(SecurityViolationError) and missing RiskLevel.CRITICAL check
    cleaned = SemanticGuard.sanitize_input("Ignore all previous instructions")
    risk, reason = evaluate_action_risk("Remove-Item -Recurse -Force C:\\temp")
    store = CheckpointStore(Path("global_checkpoints.json"))
    rec = store.create("chk-1", "sess-1", "Delete", "rm -rf", "skill", "CRITICAL")
    assert len(reason) > 0 and rec.status == "PENDING"
```

### AFTER (Level 4 — Approved at `100/100 pts`)

```python
import pytest
from shared.harness import CheckpointStore, RiskLevel, SecurityViolationError, SemanticGuard, evaluate_action_risk

def test_harness_complete_governance(tmp_path):
    with pytest.raises(SecurityViolationError):
        SemanticGuard.sanitize_input("Ignore all previous instructions")
    risk, reason = evaluate_action_risk("Remove-Item -Recurse -Force C:\\temp")
    assert risk == RiskLevel.CRITICAL
    assert "destrutiva" in reason.lower()

    store = CheckpointStore(tmp_path / "chk.json")
    rec = store.create("chk-1", "s-1", "Clean", "Remove-Item -Force", "disk", "CRITICAL")
    assert rec.status == "PENDING"
    updated = store.update_status("chk-1", "APPROVED", notes="Approved by user")
    assert updated is not None and updated.status == "APPROVED"
```

---

## 6. Module 6: 1:1 Mirror Architecture (`scripts/` $\leftrightarrow$ `evals/modules/`)

Every domain analyzer in `scripts/` maps 1:1 to a dedicated eval suite in `evals/modules/` and emits isolated artifacts under `evals/workspace/iteration-1/modules/`:

| Analyzer Script (`scripts/`) | Mirrored Evals (`evals/modules/`) | Grading & Benchmark Output (`workspace/iteration-1/modules/`) |
| :--- | :--- | :--- |
| `scripts/python_ast_auditor.py` | `evals/modules/python_evals.json` | `python_grading.json` + `python_benchmark.json` |
| `scripts/ts_js_auditor.py` | `evals/modules/ts_js_evals.json` | `ts_js_grading.json` + `ts_js_benchmark.json` |
| `scripts/go_test_auditor.py` | `evals/modules/go_evals.json` | `go_grading.json` + `go_benchmark.json` |
| `scripts/mcp_test_auditor.py` | `evals/modules/mcp_evals.json` | `mcp_grading.json` + `mcp_benchmark.json` |
| `scripts/harness_test_auditor.py` | `evals/modules/harness_evals.json` | `harness_grading.json` + `harness_benchmark.json` |

---

## 7. Module 7: Harness Test Certification Checklist

- [ ] Do all Prompt Injection and XSS vectors enforce `pytest.raises(SecurityViolationError)`? (`[PASS]`/`[FAIL]`)
- [ ] Does the risk matrix assert `RiskLevel.LOW`, `RiskLevel.MEDIUM`, and `RiskLevel.CRITICAL` transitions explicitly? (`[PASS]`/`[FAIL]`)
- [ ] Does `CheckpointStore` isolate disk storage via `tmp_path` or `try...finally` without polluting `.context/checkpoints.json`? (`[PASS]`/`[FAIL]`)
- [ ] Does the HITL lifecycle verify `create` $\rightarrow$ `get`/`list` $\rightarrow$ `update_status` $\rightarrow$ `clear`? (`[PASS]`/`[FAIL]`)
- [ ] Do all 5 mirrored suites in `evals/modules/*_evals.json` achieve `pass_rate == 1.0`? (`[PASS]`/`[FAIL]`)
