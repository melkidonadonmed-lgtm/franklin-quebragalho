# Go Test Quality Module (`go_test_auditor.py` — `v1.1.0`)

Defines the **7 Sequential Modules** and **Quality Spectrum (Levels 1–4)** for **Go (`*_test.go`, `testing`, Table-Driven Tests, Concurrency, and Google ADK Go v2)** test suites.

---

## 1. Go Testing Problem Statement

| Dimension | Critical Analysis & Engineering Approach |
| :--- | :--- |
| **The Problem** | **False Sense of Security in `go test ./...` (*Green Go Test Illusion*):** Any `func TestX(t *testing.T)` exiting without calling `t.Fail()`, `t.Error()`, `t.Fatal()`, or panicking reports `PASS (ok)`. Tests frequently discard errors (`res, _ := sut()`), log errors without failing (`t.Log(err)`), or check only `if res == nil`, letting critical bugs slip through. |
| **The Approach** | **Structural Inspection of `testing.T`, Error Handling & Concurrency:** [`scripts/go_test_auditor.py`](../scripts/go_test_auditor.py) parses each `func Test*(t *testing.T)`, counts real guards (`t.Fatalf`, `t.Errorf`, `errors.Is`, `assert.*`), flags `_` error discards, blocks `t.Fatal` inside goroutines, and enforces `t.TempDir()`, `t.Setenv()`, and `t.Cleanup()`. |
| **Target Outcome** | **Deterministic Guardrails & Race Immunity (*High Mutation Score*):** Any business contract violation, unexpected error, or resource leak deterministically fails `go test -race ./...`. |

---

## 2. Go Test AAA Anatomy

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                    GO TEST ANATOMY (AAA PATTERN)                              │
├───────────────────┬───────────────────────────────────────────────────────────┤
│ 1. ARRANGE        │ • Directory isolation via t.TempDir()                     │
│ (Preparation)     │ • Scoped environment via t.Setenv(k, v)                   │
│                   │ • Teardown registered with t.Cleanup(func() { ... })      │
├───────────────────┼───────────────────────────────────────────────────────────┤
│ 2. ACT            │ • Explicit call capturing (res, err) without '_'          │
│ (Execution)       │ • Deterministic goroutine sync (atomic/chan/WaitGroup)    │
├───────────────────┼───────────────────────────────────────────────────────────┤
│ 3. ASSERT         │ • Fatal error guard: if err != nil { t.Fatalf(...) }      │
│ (Verification)    │ • Typed error check: errors.Is(err, ErrExpected)          │
│                   │ • Strict domain field checks with t.Errorf(...)           │
└───────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 3. Tautological Failure Analysis in Go

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                    GO TAUTOLOGICAL FAILURE ANALYSIS                           │
├───────────────────────────────────────────────────────────────────────────────┤
│ WHY DID IT PASS? ('go test' Exit Code 0)                                      │
│ • The code compiled and ran:                                                  │
│     res, _ := store.AnalyzeIssue("ISS-101")                                   │
│     if res == nil { t.Fatal("nil result") }                                   │
│ • Because AnalyzeIssue returned a zero-initialized struct (&Triage{}),        │
│   the pointer was non-nil and the runner printed '--- PASS: TestAnalyzeIssue'.│
├───────────────────────────────────────────────────────────────────────────────┤
│ WHY DID IT FAIL THE REAL REQUIREMENT?                                         │
│ 1. The returned error was swallowed via blank identifier '_'.                 │
│ 2. If SLA scoring breaks and returns SLABreached=false and ImpactScore=0 for  │
│    a P0 incident, this test still PASSES 100%!                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Why Defects Persist in Go (5 Interference Factors)

1. **Silenced Error Return (`SILENCED_ERROR_IN_TEST`):** Discarding errors via `res, _ := fn()` or logging `if err != nil { t.Log(err) }` without failing the test.
2. **Unsafe Goroutine Fatal (`UNSAFE_GOROUTINE_FATAL`):** Calling `t.Fatalf` or `t.FailNow` inside `go func() { ... }()`. Because `t.FailNow()` calls `runtime.Goexit()`, invoking it from a child goroutine exits only that goroutine rather than aborting the test safely (flagged by `go vet` / `-race`).
3. **Process Environment Leakage (`GLOBAL_STATE_LEAKAGE`):** Calling `os.Setenv` or `os.Chdir` directly instead of `t.Setenv` / `t.TempDir()`, corrupting sibling tests and `t.Parallel()`.
4. **Blind Wall-Clock Sleep (`NON_DETERMINISTIC_TIME`):** Unsynchronized `time.Sleep(...)` instead of `sync/atomic`, channels, `WaitGroup`, or explicit flush barriers.
5. **Pointer-Only Check (`WEAK_NIL_ONLY_ASSERT`):** Asserting only `if got == nil { t.Fatal(...) }` without checking struct invariants.

---

## 5. Go Test Quality Spectrum (Levels 1 to 4)

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                GO TEST QUALITY SPECTRUM (*_test.go)                           │
├───────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 1: ILLUSORY / PLACEBO (Score: 0 - 25)                                   │
│ • Empty body, t.Log() only, missing t.Error/t.Fatal (`MISSING_ASSERTIONS`),   │
│   `if false { t.Fatal() }`, or discarded `_` error + nil-only check.          │
│                                                                               │
│ LEVEL 2: SUPERFICIAL / FRAGILE (Score: 26 - 50)                               │
│ • Exclusive `if res == nil` (`WEAK_NIL_ONLY_ASSERT`) or illegal `t.Fatalf`    │
│   inside `go func()` (`UNSAFE_GOROUTINE_FATAL`).                              │
│                                                                               │
│ LEVEL 3: RIGID FUNCTIONAL (Score: 51 - 80)                                    │
│ • Checks domain fields, yet leaks `os.Setenv` without `t.Cleanup`             │
│   (`GLOBAL_STATE_LEAKAGE`) or uses arbitrary `time.Sleep`.                    │
│                                                                               │
│ LEVEL 4: DETERMINISTIC & RESILIENT (Score: 81 - 100)                          │
│ • Strict AAA with `t.TempDir()` / `t.Setenv()` / `t.Cleanup()`, explicit      │
│   `if err != nil { t.Fatalf(...) }`, `errors.Is`, and invariant checks.       │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Surgical Refactoring Before vs. After (Go)

### BEFORE (Level 1 — Score 0/100: `SILENCED_ERROR_IN_TEST` + `WEAK_NIL_ONLY_ASSERT`)

```go
func TestAnalyzeIssueSilenced(t *testing.T) {
	store := domain.NewDefaultStore()
	triage, _ := store.AnalyzeIssue("ISS-101")
	if triage == nil {
		t.Fatal("expected non-nil triage")
	}
}
```

### AFTER (Level 4 — Score 100/100: Deterministic & Resilient)

```go
func TestStoreAnalyzeIssueAndSLABreach(t *testing.T) {
	store := domain.NewDefaultStore()

	triage, err := store.AnalyzeIssue("ISS-101")
	if err != nil {
		t.Fatalf("unexpected error analyzing ISS-101: %v", err)
	}
	if !triage.SLABreached || !triage.EscalationRequired || triage.ImpactScore < 90 {
		t.Errorf("expected P0 SLA breach with score >= 90, got %+v", triage)
	}

	_, err = store.AnalyzeIssue("ISS-999")
	if !errors.Is(err, domain.ErrIssueNotFound) {
		t.Fatalf("expected ErrIssueNotFound for unknown ID, got %v", err)
	}
}
```

---

## 7. Go Assertion Engineering Comparison Matrix (`testing.T`)

| Check Type | Weak / Fragile Assertion | Robust Assertion (Level 4) | Auditor Rule |
| :--- | :--- | :--- | :--- |
| **Error Return** | `res, _ := svc.Run(ctx)` | `res, err := svc.Run(ctx); if err != nil { t.Fatalf("...: %v", err) }` | `SILENCED_ERROR_IN_TEST` |
| **Expected Error** | `if err == nil { t.Error("error") }` | `if !errors.Is(err, domain.ErrIssueNotFound) { t.Fatalf(...) }` | `WEAK_NIL_ONLY_ASSERT` |
| **Goroutines** | `go func() { t.Fatalf("fail") }()` | `errCh <- err` in child goroutine + `if err := <-errCh; err != nil { t.Fatal(err) }` | `UNSAFE_GOROUTINE_FATAL` |
| **Env / Filesystem** | `os.Setenv("K", "V")` / `/tmp/test` | `t.Setenv("K", "V")` / `t.TempDir()` + `t.Cleanup(...)` | `GLOBAL_STATE_LEAKAGE` |
| **Debounce / Timing** | Unsynchronized `time.Sleep(1 * time.Second)` | `atomic.AddInt32(&count, 1)` + `debouncer.FlushAndClose()` | `NON_DETERMINISTIC_TIME` |
