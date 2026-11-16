# 5-Module AAA & Quality Spectrum Breakdown (`test-quality-auditor` v1.3.0)

Companion reference to [`SKILL.md`](../SKILL.md). See also [`test_quality_and_evals_dossier.md`](test_quality_and_evals_dossier.md), [`go_test_quality_module.md`](go_test_quality_module.md), [`mcp_test_quality_module.md`](mcp_test_quality_module.md), and [`harness_test_quality_module.md`](harness_test_quality_module.md).

## 1. 7-Step Diagnostic Workflow Structure

1. **Test Problem Statement:** Explain **The Problem** (*Green Build / Green Go / Green MCP / Green Harness Illusion*), **The Approach** (Assertion Rigor, Error Checks, JSON-RPC Lifecycle, HITL Guards, Isolation), and **The Goal** (*High Mutation Score*).
2. **Domain-Specific AAA Anatomy:**
   - **Go (`*_test.go`):** `ARRANGE` (`t.TempDir()`, `t.Setenv()`, `t.Cleanup()`), `ACT` (`res, err := sut()` without `_`), `ASSERT` (`if err != nil { t.Fatalf(...) }`, `errors.Is`).
   - **MCP (`JSON-RPC 2.0`):** `ARRANGE` (isolated temp state), `ACT` (`initialize` $\rightarrow$ `notifications/initialized` without `id` $\rightarrow$ `tools/list` $\rightarrow$ `tools/call`), `ASSERT` (JSON parse, `-32601`, Zero-Trust block).
   - **Harness (`SemanticGuard` / `CheckpointStore` / `Eval Harness`):** `ARRANGE` (`tmp_path`, adversarial payloads), `ACT` (`sanitize_input`, `evaluate_action_risk`, full `create -> get -> update_status -> clear`, `run_eval_harness`), `ASSERT` (`pytest.raises(SecurityViolationError)`, `RiskLevel.CRITICAL`, `pass_rate_gain > 0`).
3. **Tautological Failure Root Cause:** Explain technically why `Exit Code 0` succeeded without guarding business logic.
4. **Persistence Factors:** `SILENCED_ERROR_IN_TEST`, `UNSAFE_GOROUTINE_FATAL`, `MCP_INCOMPLETE_STDIO_HANDSHAKE`, `MCP_TAUTOLOGICAL_RAW_RESPONSE`, `HARNESS_WEAK_INJECTION_GUARD_TEST`, `HARNESS_UNVERIFIED_RISK_TRANSITION`, `HARNESS_MISSING_TEARDOWN_CLEANUP`, `HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE`.
5. **Quality Spectrum (Levels 1 to 4):**
   - **Level 1 (`0–25 pts` — Placebo):** Missing assertions, `assert True`, discarded `_`, unparsed JSON, or Harness without exception/critical-risk check.
   - **Level 2 (`26–50 pts` — Superficial):** `is not None`, `t.Fatal` in goroutine, `stdio` without handshake, uncleaned global state.
   - **Level 3 (`51–80 pts` — Rigid):** Exact happy-path, yet `os.Setenv` missing `t.Cleanup` or `tools/list` checked only by `len > 0`.
   - **Level 4 (`81–100 pts` — Deterministic):** Strict AAA, isolated teardown, adversarial error assertions, and closed contracts.
6. **Surgical Refactoring:** Before vs. After raising to Level 4 + real runner re-execution (`pytest`, `go test ./...`, `node --test`).
7. **Mirrored Evals:** [`scripts/eval_harness.py`](../scripts/eval_harness.py) producing `grading.json` and `benchmark.json`.
