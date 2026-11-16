# Deterministic Audit and Rejection Criteria (`test-quality-auditor` v1.3.0)

Every audit performed by this skill MUST emit deterministic verdicts backed by real AST, multi-domain structural analyzers (Python, TypeScript/JS, Go, MCP Protocol, and Harness), and test runner evidence:

- `[PASS]`: Structural, semantic, or determinism requirement proven with zero violations.
- `[FAIL]`: Violation confirmed by analyzer or runner citing exact `file:line` and anomaly code.
- `[UNVERIFIED]`: Cannot be verified due to missing target file or blocking syntax error (`SYNTAX_ERROR`).

---

### Rule 1: Test Body Integrity & Assertion Density (Ban Placebo Tests)

- **Criterion**: Every test function (`test_*` in Python, `test(...)`/`it(...)` in JS/TS, or `func Test*(t *testing.T)` in Go) MUST include at least one verifiable assertion on the output or side effect of the SUT.
- **Deterministic Check**:
  - Test containing only `pass`, `return`, `t.Log`, or empty body -> `[FAIL: EMPTY_TEST_BODY]` (Critical | `-85 pts` | Demotes to Level 1)
  - Test calling code (`Act`) with `assertion_count == 0` -> `[FAIL: MISSING_ASSERTIONS]` (Critical | `-80 pts` | Demotes to Level 1)
  - Explicit assertions verifying return value or typed contract -> `[PASS]`

### Rule 2: Assertion Rigor & Ban on Tautologies (`TAUTOLOGICAL_ASSERT` / `WEAK_ASSERT`)

- **Criterion**: Assertions MUST be falsifiable by business-logic mutations. Constant or purely superficial assertions are rejected.
- **Deterministic Check**:
  - `assert True`, `self.assertTrue(True)`, `assert.ok(true)`, or `if false { t.Fatal(...) }` -> `[FAIL: TAUTOLOGICAL_ASSERT]` (Critical | `-80 pts` | Demotes to Level 1)
  - Primary assertion limited to `assert x is not None` without checking domain attributes or values -> `[FAIL: WEAK_IS_NOT_NONE_ASSERT]` (Medium | `-55 pts`)
  - Superficial length/type check (`assert.ok(str.length > 5)`) -> `[FAIL: WEAK_SURFACE_ASSERT]` (Medium | `-22 pts`)
  - Strict value comparison (`==`, `assert.strictEqual`, `t.Errorf`), structure, or typed contract -> `[PASS]`

### Rule 3: Explicit Exception & Error Handling (`SILENCED_EXCEPTION_IN_TEST`)

- **Criterion**: Tests MUST NEVER swallow exceptions or errors via `try...except: pass`, empty `catch {}`, or discarded `_`. Expected failures MUST be validated via `pytest.raises(...)`, `await assert.rejects(...)`, or `errors.Is(err, ErrExpected)`.
- **Deterministic Check**:
  - `ExceptHandler` or `catch` block containing only `pass` or empty body -> `[FAIL: SILENCED_EXCEPTION_IN_TEST]` (Critical | `-75 pts` | Demotes to Level 1)
  - Explicit `pytest.raises` / `assert.rejects` / `errors.Is` validating error type and message -> `[PASS]`

### Rule 4: Temporal Determinism & Concurrency Immunity (`NON_DETERMINISTIC_TIME`)

- **Criterion**: Tests MUST be independent of CPU speed, OS load, or wall-clock time.
- **Deterministic Check**:
  - Direct `time.sleep()`, `datetime.now()`, `Date.now()`, or `time.Sleep()` without sync primitive or clock injection -> `[FAIL: NON_DETERMINISTIC_TIME]` (High | `-25 pts`)
  - Injected/frozen clock or atomic/channel synchronization -> `[PASS]`

### Rule 5: Global State Isolation & Teardown Cleanup (`GLOBAL_STATE_LEAKAGE`)

- **Criterion**: Any test mutating global state (`globalThis.window`, `globalThis.fetch`, `os.environ`, `os.Setenv`, singletons, or session files) MUST guarantee restoration via `try...finally`, `t.Setenv`, `t.TempDir()`, or `t.Cleanup`.
- **Deterministic Check**:
  - Direct global/environment mutation without guaranteed restoration -> `[FAIL: GLOBAL_STATE_LEAKAGE]` (High | `-25 pts`)
  - Guaranteed isolation and teardown via `try...finally`, `t.TempDir()`, or `t.Cleanup` -> `[PASS]`

### Rule 6: Decoupling from Volatile Catalog Constants (`BRITTLE_CATALOG_COUNT`)

- **Criterion**: Tests over live catalogs MUST NOT hardcode fragile counts (`assert len(data) == 24`); they MUST derive expectations from the canonical source on disk (`len(data) == len(expected_dirs)`).
- **Deterministic Check**:
  - Hardcoded literal equality `len(data) == N` over mutable catalogs without filesystem derivation -> `[FAIL: BRITTLE_CATALOG_COUNT]` (Medium | `-22 pts`)
  - Dynamic derivation from source of truth and item contracts -> `[PASS]`

### Rule 7: Go Test Module Compliance (`go_test_auditor.py` $\leftrightarrow$ `evals/modules/go_evals.json`)

- **Criterion**: Go test suites (`testing.T`, Table-Driven Tests, ADK Go v2) MUST check every returned error, assert domain fields beyond `nil`, and NEVER call `t.Fatal`/`t.FailNow` inside secondary goroutines.
- **Deterministic Check**:
  - Discarding error with blank identifier (`res, _ := sut(...)`) or `if err != nil` without `t.Fatal`/`t.Error` -> `[FAIL: SILENCED_ERROR_IN_TEST]` (Critical | `-65 pts`)
  - Single check limited to `if res == nil { t.Fatal(...) }` or `assert.NotNil(t, res)` without checking domain fields -> `[FAIL: WEAK_NIL_ONLY_ASSERT]` (Medium | `-55 pts`)
  - Calling `t.Fatal`, `t.Fatalf`, or `t.FailNow` inside `go func() { ... }()` -> `[FAIL: UNSAFE_GOROUTINE_FATAL]` (High | `-40 pts`)
  - Full `(res, err)` check, `errors.Is`, domain invariants, and safe concurrency -> `[PASS]`

### Rule 8: MCP Test Module Compliance (`mcp_test_auditor.py` $\leftrightarrow$ `evals/modules/mcp_evals.json`)

- **Criterion**: MCP test suites MUST verify the JSON-RPC 2.0 lifecycle (`initialize` $\rightarrow$ `notifications/initialized` without `id` $\rightarrow$ `tools/list` $\rightarrow$ `tools/call`), decode JSON payloads, assert error codes (`-32601`), and test Zero-Trust boundaries.
- **Deterministic Check**:
  - Calling `tools/call` via `stdio` without prior `initialize` handshake or sending `notifications/initialized` with an `id` field -> `[FAIL: MCP_INCOMPLETE_STDIO_HANDSHAKE]` (High | `-30 pts`)
  - Validating JSON MCP tool output only as a raw string (`len(res) > 0` / `is not None`) without `json.loads` / `json.Unmarshal` -> `[FAIL: MCP_TAUTOLOGICAL_RAW_RESPONSE]` (Critical | `-55 pts`)
  - Checking `tools/list` by count `> 0` only without verifying canonical tool names -> `[FAIL: MCP_WEAK_TOOLS_LIST_DISCOVERY]` (Medium | `-25 pts`)
  - Invoking `nonexistent_tool` without checking JSON-RPC error code `-32601` -> `[FAIL: MCP_UNVERIFIED_ERROR_CODE_CONTRACT]` (High | `-30 pts`)
  - Sending adversarial payload (`../` or Prompt Injection) without explicit rejection assertion (`BLOCKED` / Security Error) -> `[FAIL: MCP_WEAK_SECURITY_GUARD_ASSERT]` (High | `-35 pts`)
  - Full JSON-RPC 2.0 lifecycle, JSON decoding, and Zero-Trust boundary verification -> `[PASS]`

### Rule 9: Harness Test Module Compliance (`harness_test_auditor.py` $\leftrightarrow$ `evals/modules/harness_evals.json`)

- **Criterion**: Tests covering Governance Harnesses (`SemanticGuard`, `evaluate_action_risk`, `CheckpointStore`) and Eval Harnesses (`run_eval_harness`) MUST verify injection blocking, `RiskLevel.CRITICAL` transitions, `tmp_path` isolation, full checkpoint lifecycle, and `pass_rate_gain`.
- **Deterministic Check**:
  - Calling `SemanticGuard.sanitize_input` with injection payload without `pytest.raises(SecurityViolationError)` / `"BLOCKED"` -> `[FAIL: HARNESS_WEAK_INJECTION_GUARD_TEST]` (Critical | `-50 pts`)
  - Calling `evaluate_action_risk` / `franklin_harness_guard` with destructive command without asserting `RiskLevel.CRITICAL` / `"APPROVAL_REQUIRED"` -> `[FAIL: HARNESS_UNVERIFIED_RISK_TRANSITION]` (Critical | `-45 pts`)
  - Mutating `CheckpointStore` or `franklin_harness_guard` without `tmp_path`/`TempDir`/`try...finally` -> `[FAIL: HARNESS_MISSING_TEARDOWN_CLEANUP]` (High | `-35 pts`)
  - Calling `CheckpointStore.create()` without verifying retrieval (`.get()` / `.list()`) or transition (`.update_status()`) -> `[FAIL: HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE]` (Medium | `-25 pts`)
  - Calling `run_eval_harness()` without inspecting `pass_rate`, `pass_rate_gain`, or `evidence` -> `[FAIL: HARNESS_EVAL_MISSING_EVIDENCE_OR_DELTA]` (High | `-35 pts`)
  - Complete Level 4 Governance & Eval Harness verification -> `[PASS]`

### Rule 10: Mirrored Eval Suite Compliance (`evals/modules/*_evals.json` & `evals/evals.json`)

- **Criterion**: Each of the 5 analyzer modules (`python`, `ts_js`, `go`, `mcp`, `harness`) MUST have a mirrored file at `evals/modules/<mod>_evals.json` producing `<mod>_grading.json` and `<mod>_benchmark.json` in `evals/workspace/iteration-1/modules/`, alongside consolidated `evals/evals.json` (20 cases).
- **Deterministic Check**:
  - Any mirrored module missing, lacking concrete `evidence`, or scoring `pass_rate < 1.0` -> `[FAIL: INVALID_EVAL_HARNESS]`
  - All 5 mirrored modules (17 modular cases) + 3 Near-Misses (20 total cases) passing at `100% PASS` -> `[PASS]`
