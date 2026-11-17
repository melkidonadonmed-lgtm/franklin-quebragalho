# Canonical Dossier on Test Quality Auditing & Eval Engineering (`test-quality-auditor` v1.3.0)

This document consolidates the technical foundation, diagnostic matrices, and Eval-Driven Harness architecture used by `test-quality-auditor`.

---

## 1. Test Problem Statement Diagnosis

| Dimension | Critical Analysis & Engineering Approach |
| :--- | :--- |
| **The Problem** | **False Sense of Security (*Green Build Illusion*):** AI agents and developers frequently produce test suites that pass 100% of runs (*green builds*) yet miss production regressions. Tests call the target unit but rely on weak assertions, tautological mocks, leaked global state, or swallowed exceptions. |
| **The Approach** | **Assertion Integrity & Determinism Auditing:** Instead of measuring line coverage alone, the auditor inspects assertion falsifiability via AST, state isolation (`try/finally` and fixtures), mock scope, and immunity to temporal/concurrency flakiness. |
| **Target Outcome** | **High Mutation Score (*Deterministic Guardrails*):** Convert superficial checks into strict guardrails where any business-rule regression immediately breaks the test suite. |

---

## 2. Arrange-Act-Assert (AAA) Anatomy Inspection

High-integrity automated tests obey strict **Arrange-Act-Assert (AAA)** separation:

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                      TEST ANATOMY (AAA PATTERN)                           │
├───────────────────┬───────────────────────────────────────────────────────┤
│ 1. ARRANGE        │ • Deterministic fixture/data setup                    │
│ (Preparation)     │ • Mock ONLY external I/O (DB/network), never the SUT  │
│                   │ • Preserve global state for guaranteed teardown       │
├───────────────────┼───────────────────────────────────────────────────────┤
│ 2. ACT            │ • Single targeted invocation of unit or contract      │
│ (Execution)       │ • Capture return values and errors without masking    │
├───────────────────┼───────────────────────────────────────────────────────┤
│ 3. ASSERT         │ • Strict return-value and invariant assertions        │
│ (Verification)    │ • Validate side effects and typed contracts           │
└───────────────────┴───────────────────────────────────────────────────────┘
```

### Critical Assembly Defects Inspected:
1. **Arrange Contamination:** Mocking internal unit logic turns the test into a mock echo chamber; mutating `globalThis.window`, `globalThis.fetch`, or `os.environ` outside `try/finally` leaks across tests.
2. **Act Scope Creep:** Mixing unrelated mutable calls inside one test hides root causes when assertions fail.
3. **Assert Weakness:** Missing `assert`, tautologies (`assert True`), or superficial checks (`assert res is not None`, `assert len(str) > 5`) let semantic regressions pass silently.

---

## 3. Tautological Failure Analysis — Why It Passed Yet Failed the Spec

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                     TAUTOLOGICAL FAILURE ANALYSIS                         │
├───────────────────────────────────────────────────────────────────────────┤
│ WHY DID IT PASS?                                                          │
│ • The test runner (Pytest / Node Test Runner) exited 0 because syntax     │
│   was valid and no uncaught exception escaped.                            │
│ • The test asserted 'assert True', 'assert res is not None', or           │
│   'assert.ok(formatted.length > 5)'.                                      │
├───────────────────────────────────────────────────────────────────────────┤
│ WHY DID IT FAIL THE REAL REQUIREMENT?                                     │
│ • It never validated CONTENT, FORMAT, or BUSINESS INVARIANTS.             │
│ • If a bug alters the output from $100.00 to $0.00 (or formatDate returns │
│   "Invalid Date", length 12 > 5), the assertion STILL PASSES!             │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Why Defects Persist (5 Hidden Contamination Factors)

1. **Implementation Coupling & Volatile Constants:** Hardcoded catalog counts (e.g., `assert len(skills) == 21`) break whenever legitimate items are added instead of checking filesystem parity.
2. **Temporal Non-Determinism (*Flaky Tests*):** Raw `time.sleep()`, `datetime.now()`, or wall-clock delta assertions (`Date.now() - start`) fail intermittently under CI CPU contention.
3. **Tautological Mocks:** Stubbing services to echo the exact asserted literal bypasses type and schema invariants.
4. **Missing State Teardown (*State Leakage*):** Mutating globals or writing checkpoints to disk without `try/finally` or `tmp_path` leaves dirty state if an assertion aborts early.
5. **Assertion Extremes:** Swinging between vague existence checks (`is not None`) and brittle cosmetic string matching.

---

## 5. Test Quality Spectrum (Levels 1 to 4)

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                       TEST QUALITY SPECTRUM                               │
├───────────────────────────────────────────────────────────────────────────┤
│ LEVEL 1: ILLUSORY / PLACEBO (Score: 0 - 25)                               │
│ • No assertions, 'assert True', 'try...except: pass' silencing failures.  │
│                                                                           │
│ LEVEL 2: SUPERFICIAL / FRAGILE (Score: 26 - 50)                           │
│ • Weak checks ('is not None', 'length > 5'), SUT mocks, or state leaks.   │
│                                                                           │
│ LEVEL 3: RIGID FUNCTIONAL (Score: 51 - 80)                                │
│ • Checks happy-path values strictly, yet omits boundaries/teardown, uses  │
│   brittle static counts, or relies on wall-clock timing.                  │
│                                                                           │
│ LEVEL 4: DETERMINISTIC & RESILIENT (Score: 81 - 100)                      │
│ • Strict AAA, frozen/injected clock, guaranteed teardown via try/finally, │
│   explicit exception assertions, and adversarial edge coverage.           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Eval-Driven Harness Architecture

### 6.1. `evals/evals.json` and Workspace Layout
```text
test-quality-auditor/
├── SKILL.md
├── rules/audit_criteria.md
├── scripts/test_quality_auditor.py
└── evals/
    ├── evals.json
    └── workspace/
        └── iteration-1/
            ├── grading.json     # Individual case grading with Concrete Evidence
            └── benchmark.json   # Baseline vs. Treatment aggregate statistics
```

### 6.2. Comparative Assertion Engineering Matrix
| Check Type | Weak / Brittle Assertion | Robust Assertion (Level 4) | Validation Mechanism |
| :--- | :--- | :--- | :--- |
| **Output Format** | "Return valid JSON." | "Output is valid JSON with keys `aprovado`, `score_medio`, `nivel_espectro`, `issues`." | Python (`json.loads` + Schema) |
| **Date Formatting** | `assert.ok(formatted.length > 5)` | `assert.match(formatted, /^\d{2}\/\d{2}\/\d{4}/)` | Deterministic Regex |
| **Global Isolation** | Loose `globalThis.window = mockWindow` | `try { ... } finally { globalThis.window = originalWindow; }` | AST Check (`GLOBAL_STATE_LEAKAGE`) |
| **Live Catalog** | Fixed `assert len(data) == 21` | `assert len(data) == len(expected_skill_dirs) and len(data) >= 21` | Dynamic Filesystem Parity |
| **Go Test (`*_test.go`)** | `res, _ := sut(); if res == nil { t.Fatal() }` | `res, err := sut(); if err != nil { t.Fatalf(...) }` + `errors.Is` + `t.TempDir()` | Go Module (`go_test_auditor.py`) |
| **MCP Server/Tool** | `res = call_mcp(); assert len(res) > 0` | `initialize` $\rightarrow$ `tools/list` $\rightarrow$ `json.loads`/`Unmarshal` + `-32601` + `BLOCKED` | MCP Module (`mcp_test_auditor.py`) |
| **Harness (HITL & Evals)** | `SemanticGuard.sanitize_input(inj)` without `raises` | `pytest.raises(SecurityViolationError)` + `RiskLevel.CRITICAL` + `tmp_path` + `update_status` + `pass_rate_gain` | Harness Module (`harness_test_auditor.py`) |

---

## 7. Specialist Domain Modules & Mirrored Evals (`v1.3.0`)

- **[Go Test Quality Module (`go_test_quality_module.md`)](go_test_quality_module.md):** 7-Module breakdown for `*_test.go` suites (`testing.T`, Table-Driven Tests, ADK Go v2, `SILENCED_ERROR_IN_TEST`, `WEAK_NIL_ONLY_ASSERT`, `UNSAFE_GOROUTINE_FATAL`, `GLOBAL_STATE_LEAKAGE`) $\leftrightarrow$ [`evals/modules/go_evals.json`](evals/modules/go_evals.json).
- **[MCP Test Quality Module (`mcp_test_quality_module.md`)](mcp_test_quality_module.md):** 7-Module breakdown for **Model Context Protocol** servers and tools (JSON-RPC 2.0 `stdio`, FastMCP Python, Go `StdioServer`) $\leftrightarrow$ [`evals/modules/mcp_evals.json`](evals/modules/mcp_evals.json).
- **[Harness Test Quality Module (`harness_test_quality_module.md`)](harness_test_quality_module.md):** 7-Module breakdown for **Governance Harnesses (Zero-Trust / HITL)** and **Eval-Driven Harnesses** $\leftrightarrow$ [`evals/modules/harness_evals.json`](evals/modules/harness_evals.json).
- **Base Mirrors:** [`evals/modules/python_evals.json`](evals/modules/python_evals.json) ($\leftrightarrow$ `python_ast_auditor.py`) and [`evals/modules/ts_js_evals.json`](evals/modules/ts_js_evals.json) ($\leftrightarrow$ `ts_js_auditor.py`).
