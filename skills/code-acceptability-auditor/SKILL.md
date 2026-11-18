---
name: code-acceptability-auditor
description: "Audit Python modules statically via AST against eval/exec, shell=True, hardcoded secrets, missing type hints, silenced exceptions, stubs, and functions >60 lines. Use to compute the Quality Score (>=75) before commits. Do NOT use for theoretical Q&A, test suites (test-quality-auditor), or 3D physics (code-quality-audit-3d-physics)."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: read_file run_command
metadata:
  version: "1.1.1"
  updated_at: "2026-11-18"
  author: "Franklin"
  category: "Python AST Code Quality & Security Gatekeeping"
  tags: "code-acceptability-auditor, ast, python, python-audit, auditar, estaticamente, arquivos, eval, exec, shell, type, hints, type-hints, funcoes, longas, linhas, qualidade, acceptability, security, pre-commit, quality-gate, cyclomatic-complexity"
---

# `code-acceptability-auditor` (`v1.1.1`) — Python AST Quality Gate

## 1. Overview & Scope

Performs static Python **AST** auditing as **Gate 1** of the quality pipeline without executing untrusted code:
- Validates Python files/directories prior to `git commit` against `eval`/`exec`, `shell=True`, hardcoded secrets, missing type hints, functions `> 60` lines, nesting `> 3`, and McCabe $M > 10$, computing the **Quality Score** (`0.0–100.0`, requiring `score >= 75.0`, `critical_count == 0`, and `passed_syntax == True`).
- **When NOT to Use:** Do NOT use for theoretical Python Q&A, greenfield scaffolding, test-suite AAA grading (`test-quality-auditor`), runtime RCA (`gap-analyzer-auditor`), or 3D/WebGL physics (`code-quality-audit-3d-physics`).

## 2. Inputs & Prerequisites

- **`--file` / `--dir` (required):** Target Python file or directory root under audit.
- **`min_quality_score` (`75.0` default) & `max_critical_violations` (`0`)** on Python `3.12+` with `pydantic>=2.0`.

## 3. Step-by-Step Procedure

Consult the 13-rule matrix (`SEC001..003`, `SYN001`, `ERR001..003`, `TYP001..002`, `ARCH001..003`, `STUB001`) and 7 CLI modes in [`references/rules_12_matrix_and_cli.md`](references/rules_12_matrix_and_cli.md) and [`references/security_rules_spec.md`](references/security_rules_spec.md):

1. **Wave 1 (`CoT + ReAct`):** Run static AST scanning against the target file or directory:
```powershell
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --dir shared --json
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --self-test
```
2. **Wave 2 (`Score`):** Compute the deterministic score:
$$\text{Quality Score} = \max\left(0.0, 100.0 - \sum \text{Penalties}\right)$$
3. **Wave 3 (`RAW Gate`):** Enforce pre-commit checks: reject any artifact where `not passed_syntax`, `critical_count > 0`, or `quality_score < 75.0`, re-run the scanner (`Read-After-Write`) after refactoring, and run [`scripts/test_code_acceptability_auditor.py`](scripts/test_code_acceptability_auditor.py) when modifying rules.

## 4. Gotchas & Edge Cases

- Bare `except:` (`ERR001`, `-10`) differs from `except Exception:` (`ERR002`, `-5`); both escalate to `ERR003` (`-25`) when the handler contains only `pass`, `...`, or `continue`.
- `SEC003` exempts `os.getenv`/`os.environ.get` and doc placeholders (`YOUR_API_KEY`); `TYP001` exempts `self`/`cls`, `TYP002` exempts `__init__`. Enforce Google Python Style Guide (`pyguide.md`, `[tool.ruff.lint.pydocstyle] convention = "google"`).
- Keep [`references/trigger_matrix_queries.json`](references/trigger_matrix_queries.json), [`references/trigger_eval_report_baseline.json`](references/trigger_eval_report_baseline.json), and [`assets/.github/workflows/ci.yml`](assets/.github/workflows/ci.yml) intact for `trigger_eval_runner.py` and CI gates.

## 5. Output Schema & Validation Criteria

Emit a Pydantic-validated report (`FileAuditReport` / `DirectoryAuditSummary`) matching [`references/acceptance_criteria.md`](references/acceptance_criteria.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md), including `status` (`APPROVED`/`REJECTED`), `quality_score`, `passed_syntax`, `violations`, and `[PASS]` / `[FAIL: <RULE_ID>]` verdicts.

## 6. User Communication Rule

All direct responses, violation breakdowns, clarifying questions, and delivery summaries addressed to the end user MUST be written in **Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.
