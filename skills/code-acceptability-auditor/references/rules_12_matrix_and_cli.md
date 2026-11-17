# 13 AST Rules Matrix & CLI Execution Modes — `code-acceptability-auditor`

Complete penalty and CLI command reference consumed by `SKILL.md`, complementing [`acceptance_criteria.md`](acceptance_criteria.md) and [`security_rules_spec.md`](security_rules_spec.md).

## 13 AST Rules Matrix

| Rule ID | Category | Severity | Penalty | Problem Description | Action / Recommendation |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **`SEC001`** | Security | **CRITICAL** | `-25.0` | Call to `eval()` or `exec()`. | Use `ast.literal_eval` or structured parsing. |
| **`SEC002`** | Security | **CRITICAL** | `-25.0` | Subprocess with `shell=True`. | Set `shell=False` and pass argument list. |
| **`SEC003`** | Security | **CRITICAL** | `-25.0` | Suspected hardcoded key/JWT/password. | Move credentials to `.env` / environment. |
| **`SYN001`** | Syntax | **CRITICAL** | `-25.0` | Python `SyntaxError`. | Fix syntax before execution. |
| **`ERR001`** | Error Handling | **HIGH** | `-10.0` | Bare `except:` clause. | Specify exact exception (`except ValueError:`). |
| **`ERR002`** | Error Handling | **MEDIUM** | `-5.0` | Broad catch (`except Exception:`/`BaseException`). | Narrow to domain-specific exception class. |
| **`ERR003`** | Error Handling | **CRITICAL** | `-25.0` | Silenced exception via `pass`, `...`, or `continue`. | Log, handle explicitly, or `raise`. |
| **`TYP001`** | Typing | **MEDIUM** | `-5.0` | Parameter missing Type Hint (`self`/`cls` exempt). | Add type annotations to all arguments. |
| **`TYP002`** | Typing | **MEDIUM** | `-5.0` | Function missing return annotation (`__init__` exempt). | Declare explicit `-> Type`. |
| **`ARCH001`** | Architecture | **LOW** | `-2.0` | Oversized function (`> 60` lines). | Split responsibilities (SRP). |
| **`ARCH002`** | Cognitive Complexity | **MEDIUM** | `-5.0` | Nesting depth `> 3` levels. | Use Early Return / helper functions. |
| **`ARCH003`** | Cyclomatic Complexity | **MEDIUM** | `-5.0` | McCabe $M = E - N + 2P > 10$. | Reduce branching ($M \le 10$) via dispatch/helpers. |
| **`STUB001`** | Implementation | **CRITICAL** | `-25.0` | Empty stub (`pass`, `...`, `NotImplementedError`) outside ABC/Protocol/tests. | Implement concrete function logic. |

## CLI Execution Modes (`pwsh`)

```powershell
# 1. Audit single Python file
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --file path/to/file.py

# 2. Audit directory with JSON output
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --dir shared --json

# 3. Deterministic self-test
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --self-test

# 4. Trigger Evals (F1 = 1.0)
uv run python skills/code-acceptability-auditor/scripts/trigger_eval_runner.py

# 5. Benchmark A vs B / Failure Auditor
uv run python skills/code-acceptability-auditor/scripts/skill_failure_auditor.py

# 6. Install .git/hooks/pre-commit gate
uv run python skills/code-acceptability-auditor/scripts/install_pre_commit_hook.py --repo-root .

# 7. Combined Gate (AST + Pytest)
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --dir shared; uv run pytest -q
```
