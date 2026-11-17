# Technical Specification of AST & Regex Rules (`security_rules_spec.md` — `v1.1.0`)

Engineering specification for deterministic detection of all 13 rules (`SEC001`..`SEC003`, `SYN001`, `ERR001`..`ERR003`, `TYP001`..`TYP002`, `ARCH001`..`ARCH003`, and `STUB001`).

---

## 1. Security Inspection (`SEC001` – `SEC003`)

### `SEC001` — Dynamic Code Execution (`eval` / `exec`)

- **AST Node**: `ast.Call`
- **Condition**: `isinstance(node.func, ast.Name)` with `node.func.id in {"eval", "exec"}` or `isinstance(node.func, ast.Attribute)` with `node.func.attr in {"eval", "exec"}` when base object is `builtins`.
- **Safe Exclusion**: `ast.literal_eval` is permitted and does not trigger an alert.

### `SEC002` — Command Injection (`shell=True` / `os.system`)

- **AST Node**: `ast.Call`
- **Condition A**: Call to `subprocess.{run, Popen, call, check_call, check_output}` containing `ast.keyword(arg="shell", value=ast.Constant(value=True))`.
- **Condition B**: Direct call to `os.system(...)` or `os.popen(...)`.

### `SEC003` — Hardcoded Credentials & Secret Leaks

- **Hybrid Inspection (AST + Regex)**:
  1. **AST (`ast.Assign`, `ast.AnnAssign`, `ast.Dict`)**: Identifiers matching `(api[_-]?key|secret|password|passwd|pwd|access[_-]?token|auth[_-]?token|private[_-]?key|client[_-]?secret|jwt[_-]?secret)` assigned non-empty `str` constants (`len >= 6`) that are not placeholders (`YOUR_...`, `<...>`, `changeme`, `dummy`, `example`, `none`, `null`, `todo`).
  2. **Token Signature Regex**: Matches known prefixes inside string literals:
     - `sk-[A-Za-z0-9_-]{16,}` (OpenAI / API Secret Key)
     - `gh[pousr]_[A-Za-z0-9]{20,}` (GitHub Personal/Server Token)
     - `AIza[0-9A-Za-z_-]{20,}` (Google Cloud / Gemini API Key)
     - `AKIA[0-9A-Z]{16}` (AWS Access Key ID)
     - `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}` (Literal JWT)

---

## 2. Exception Handling Inspection (`ERR001` – `ERR003`)

- **`ERR001` (Bare `except:`)**: `isinstance(node, ast.ExceptHandler)` with `node.type is None`.
- **`ERR002` (`except Exception:`)**: `node.type` is `ast.Name(id="Exception" | "BaseException")` or a tuple containing `Exception`/`BaseException`.
- **`ERR003` (Silenced Exception)**: Handler `node.body` (excluding an initial docstring literal) consists solely of `ast.Pass`, `ast.Continue`, or `ast.Expr(value=ast.Constant(value=Ellipsis))`.

---

## 3. Typing, Modularity, Complexity & Stub Inspection (`TYP001`, `TYP002`, `ARCH001`..`ARCH003`, `STUB001`)

- **`TYP001`**: Inspects `args.posonlyargs`, `args.args`, `args.kwonlyargs`, `args.vararg`, and `args.kwarg`. Exempts `self` and `cls`.
- **`TYP002`**: Checks `node.returns is None` in `FunctionDef` and `AsyncFunctionDef`. Exempts `__init__` when arguments are typed or enforces `-> None` in strict mode.
- **`ARCH001`**: Computes `span = (node.end_lineno or node.lineno) - node.lineno + 1`. Fires when `span > 60`.
- **`ARCH002` (Cognitive Complexity)**: Recursively traverses function body counting nesting depth for `ast.If`, `ast.For`, `ast.AsyncFor`, `ast.While`, `ast.With`, `ast.AsyncWith`, and `ast.Try` (`elif` chains stay at the parent `if` depth). Fires when `max_depth > 3`.
- **`ARCH003` (McCabe Cyclomatic Complexity)**: Computes $M = 1 + \text{decision points}$ (`If`, `For`, `AsyncFor`, `While`, `ExceptHandler`, `IfExp`, `comprehension.ifs`, and boolean `BoolOp`). Fires when $M > 10$.
- **`STUB001` (Zero Tolerance for Fake Functions)**: Fires (`CRITICAL`, `-25.0`) when a non-abstract function/method body (outside `ABC`, `Protocol`, `@abstractmethod`, `@overload`, dunders, `.pyi`, or `tests/`) contains only `pass`, `...`, or `raise NotImplementedError`.
