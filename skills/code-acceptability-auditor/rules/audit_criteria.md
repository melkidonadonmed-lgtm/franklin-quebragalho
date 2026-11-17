# Deterministic Audit and Rejection Criteria (`code-acceptability-auditor` v1.1.0)

Every audit performed by this skill MUST emit deterministic verdicts grounded in real Python AST evidence and lexical security patterns:

- `[PASS]`: Syntax, security, error handling, typing, and modularity verified without blocking violations.
- `[FAIL]`: Violation confirmed by the AST/Regex scanner citing exact `file:line`, `rule_id`, and penalty.
- `[UNVERIFIED]`: Cannot be verified due to missing target file or invalid path.

---

### Rule 1: AST Syntactic Integrity (`SYN001`)

- **Criterion**: Target Python file MUST parse cleanly via `ast.parse()` without raising `SyntaxError`.
- **Deterministic Check**:
  - `ast.parse()` raises `SyntaxError` -> `[FAIL: SYN001]` (`CRITICAL` | `-25.0` | `passed_syntax = False` | immediate `REJECTED`).
  - AST built cleanly -> `[PASS]`.

### Rule 2: Ban Arbitrary Dynamic Execution (`SEC001`)

- **Criterion**: No module may invoke `eval()` or `exec()` on dynamic strings or expressions.
- **Deterministic Check**:
  - `ast.Call` invoking `eval`/`exec` (`Name` or `builtins.eval`/`builtins.exec`) -> `[FAIL: SEC001]` (`CRITICAL` | `-25.0` | `REJECTED`).
  - Zero `eval`/`exec` calls (safe `ast.literal_eval` allowed) -> `[PASS]`.

### Rule 3: Ban Subprocesses with `shell=True` (`SEC002`)

- **Criterion**: Calls to `subprocess.run`, `Popen`, `call`, `check_call`, `check_output`, `os.system`, or `os.popen` MUST NOT enable `shell=True`.
- **Deterministic Check**:
  - `subprocess.*` with `shell=True` or direct `os.system(...)`/`os.popen(...)` -> `[FAIL: SEC002]` (`CRITICAL` | `-25.0` | `REJECTED`).
  - Argument list invocation with `shell=False` (or omitted) -> `[PASS]`.

### Rule 4: Hardcoded Credentials & Secret Protection (`SEC003`)

- **Criterion**: No secret identifier (`api_key`, `secret`, `password`, `passwd`, `token`, `private_key`, `access_key`, `jwt`) or token pattern (`sk-...`, `ghp_...`, `AIza...`, `AKIA...`, `Bearer eyJ...`) may contain a hardcoded literal.
- **Deterministic Check**:
  - Literal secret assignment or API token match in active code -> `[FAIL: SEC003]` (`CRITICAL` | `-25.0` | `REJECTED`).
  - Loaded via `os.getenv(...)`, `os.environ[...]`, `pydantic_settings`, or documentation placeholders -> `[PASS]`.

### Rule 5: Ban Silenced or Overly Broad Exceptions (`ERR001`, `ERR002`, `ERR003`)

- **Criterion**: `except` handlers MUST target specific exception classes and never silently swallow failures via `pass`, `...`, or `continue`.
- **Deterministic Check**:
  - `ast.ExceptHandler` body (excluding docstrings) contains only `pass`, `continue`, or `...` -> `[FAIL: ERR003]` (`CRITICAL` | `-25.0` | `REJECTED`).
  - Bare `except:` (`type is None`) -> `[FAIL: ERR001]` (`HIGH` | `-10.0`).
  - Broad `except Exception:` or `except BaseException:` -> `[FAIL: ERR002]` (`MEDIUM` | `-5.0`).
  - Specific typed exceptions with logging, recovery, or `raise` -> `[PASS]`.

### Rule 6: Explicit Type Hints in Signatures (`TYP001`, `TYP002`)

- **Criterion**: All functions and methods (`FunctionDef` / `AsyncFunctionDef`) MUST annotate parameters (except `self`/`cls`) and return types (`-> Type`, except `__init__`).
- **Deterministic Check**:
  - Parameter (except `self`/`cls`) missing annotation (`arg.annotation is None`) -> `[FAIL: TYP001]` (`MEDIUM` | `-5.0`).
  - Function/method (except `__init__`) missing return annotation (`node.returns is None`) -> `[FAIL: TYP002]` (`MEDIUM` | `-5.0`).
  - Fully annotated signature -> `[PASS]`.

### Rule 7: Modularity, Cognitive & Cyclomatic Complexity (`ARCH001`, `ARCH002`, `ARCH003`)

- **Criterion**: Functions MUST obey SRP: length `<= 60` lines (`ARCH001`), control nesting `<= 3` levels (`ARCH002`, counting `elif` at parent depth), and McCabe complexity $M = E - N + 2P \le 10$ (`ARCH003`).
- **Deterministic Check**:
  - Function span `> 60` lines -> `[FAIL: ARCH001]` (`LOW` | `-2.0`).
  - Control nesting depth `> 3` -> `[FAIL: ARCH002]` (`MEDIUM` | `-5.0`).
  - McCabe complexity $M > 10$ -> `[FAIL: ARCH003]` (`MEDIUM` | `-5.0`).
  - All functions within limits (`<= 60` lines, `<= 3` levels, $M \le 10$) -> `[PASS]`.

### Rule 8: Ban Empty / Unimplemented Stub Functions (`STUB001`)

- **Criterion**: Production Python functions and methods MUST NOT consist solely of `pass`, `...`, or `raise NotImplementedError(...)` outside `Protocol`/`ABC` interfaces, `@abstractmethod`/`@overload` signatures, `.pyi` stubs, or test suites (`tests/`, `test_*.py`).
- **Deterministic Check**:
  - Non-exempt function body (after docstring) is a bare `pass`, `...`, or `raise NotImplementedError` -> `[FAIL: STUB001]` (`CRITICAL` | `-25.0` | `REJECTED`).
  - Concrete implementation or valid `@abstractmethod`/`Protocol` contract -> `[PASS]`.

### Rule 9: Final Quality Gate (`Quality Gate`)

- **Criterion**: A Python file is `APPROVED` if and only if `passed_syntax == True`, `critical_violations == 0`, and `quality_score >= 75.0`.
- **Deterministic Check**:
  - `not passed_syntax` or `critical_violations > 0` or `quality_score < 75.0` -> `[FAIL: QUALITY_GATE_REJECTED]`.
  - All 3 conditions satisfied -> `[PASS]`.
