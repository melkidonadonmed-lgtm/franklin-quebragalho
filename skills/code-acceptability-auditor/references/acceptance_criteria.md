# Python Code Acceptance Criteria (`code-acceptability-auditor` v1.1.0)

This specification defines the mandatory technical standards for approving Python scripts and modules prior to `git commit`, Pull Request merge, or production deployment.

---

## 1. Deterministic 13-Rule & Penalty Table

| Rule ID | Category | Severity | Penalty | Trigger Condition | Required Remediation |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **`SYN001`** | Syntax | `CRITICAL` | `-25.0` | `ast.parse()` fails with `SyntaxError`. | Fix syntax errors before submitting file. |
| **`SEC001`** | Security | `CRITICAL` | `-25.0` | `eval()` or `exec()` call in AST. | Use `ast.literal_eval()` or typed Pydantic parsing. |
| **`SEC002`** | Security | `CRITICAL` | `-25.0` | `subprocess.*(..., shell=True)` or `os.system()`. | Pass argument list with `shell=False`. |
| **`SEC003`** | Security | `CRITICAL` | `-25.0` | Hardcoded secret, password, API key, or JWT token. | Load from environment (`os.getenv` / `.env`). |
| **`ERR001`** | Errors | `HIGH` | `-10.0` | Bare `except:` clause without exception class. | Catch specific exceptions (e.g., `except ValueError:`). |
| **`ERR002`** | Errors | `MEDIUM` | `-5.0` | Overly broad catch (`except Exception:`). | Narrow to expected exception or log and re-raise. |
| **`ERR003`** | Errors | `CRITICAL` | `-25.0` | Silenced `except` block with `pass`, `...`, or `continue`. | Log error or explicitly re-raise exception. |
| **`TYP001`** | Typing | `MEDIUM` | `-5.0` | Function parameter missing Type Hint (`self`/`cls` exempt). | Annotate all signature parameters. |
| **`TYP002`** | Typing | `MEDIUM` | `-5.0` | Function/method missing return hint (`__init__` exempt). | Declare explicit `-> Type` return annotation. |
| **`ARCH001`** | Architecture | `LOW` | `-2.0` | Function/method exceeds `60` lines (`end_lineno - lineno + 1 > 60`). | Extract cohesive helper functions (SRP). |
| **`ARCH002`** | Cognitive Complexity | `MEDIUM` | `-5.0` | Control nesting depth (`if/for/while`) `> 3` levels (`elif` counts at parent level). | Apply Early Returns (Guard Clauses) or split helpers. |
| **`ARCH003`** | Cyclomatic Complexity | `MEDIUM` | `-5.0` | McCabe complexity $M = E - N + 2P > 10$. | Reduce branching ($M \le 10$) via dispatch tables or helpers. |
| **`STUB001`** | Implementation | `CRITICAL` | `-25.0` | Non-abstract function body is bare `pass`, `...`, or `raise NotImplementedError`. | Implement real business logic before committing. |

---

## 2. Quality Score Formula & Approval Gate

$$\text{Quality Score} = \max\left(0.0, 100.0 - \sum_{i=1}^{n} \text{Penalty}_i\right)$$

A Python artifact receives **`APPROVED`** if and only if:

1. `passed_syntax is True`
2. `critical_violations == 0`
3. `quality_score >= 75.0`
