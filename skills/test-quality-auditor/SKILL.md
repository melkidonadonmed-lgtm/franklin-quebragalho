---
name: test-quality-auditor
description: "Audit test suites across 5 modules (Python, TS/JS, Go, MCP, and Harness) to detect Green Build Illusion, AAA pattern defects, and weak assertions, emitting grading.json and benchmark.json. Use for auditing test suites and evals. Do NOT use for production Python AST checks (code-acceptability-auditor) or 3D physics (code-quality-audit-3d-physics)."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: read_file run_command
metadata:
  version: "1.3.1"
  updated_at: "2026-11-18"
  author: "Franklin"
  category: "Test Suite Quality Auditing & Eval Harness Engineering"
  tags: "test-quality-auditor, test-quality, auditoria, suites, testes, modulos, python, ts, go, mcp, harness, green, build, illusion, falhas, aaa, aaa-pattern, qualidade, ast-auditor, go-testing, mcp-testing, harness-testing, mirrored-evals, mutation-score, evals, grading-json, benchmark-json"
---

# `test-quality-auditor` (`v1.3.1`) — Deterministic Test & Eval Auditor

Modular engine (`< 300` lines/module, typed domain models in [`scripts/models.py`](scripts/models.py)) with 1:1 mirrored evals (`evals/modules/*_evals.json`) for **5 domains**: Python (`python_ast_auditor.py`), TS/JS (`ts_js_auditor.py`), Go (`go_test_auditor.py`), MCP (`mcp_test_auditor.py`), and Harness (`harness_test_auditor.py` + `perfkit_stats.py`).

## 1. Overview & Scope

- Audits test efficacy, AAA rigor, and Levels 1–4 across `test_*.py`, `*.test.ts`, `*_test.go`, `test_server.py`, and `test_harness_quality.py`.
- Detects *Green Build Illusion* (`assert True`, `_` Go error discards, goroutine `t.Fatal`, incomplete MCP handshakes, missing `pytest.raises(SecurityViolationError)`), emitting `grading.json` and `benchmark.json`.
- **When NOT to Use:** Do NOT use for production AST gates (`code-acceptability-auditor`), 3D physics (`code-quality-audit-3d-physics`), RCA (`gap-analyzer-auditor`), or disk/Drive cleanup (`windows-disk-maintenance`, `gdrive-cleanup-auditor`).

## 2. Inputs & Prerequisites

- **`target_path`** (required): Test file/dir or `evals/evals.json`. **`domain`** & **`eval_module`** (`auto`/`all` | `python` | `ts_js` | `go` | `mcp` | `harness`).

## 3. Step-by-Step Procedure

Consult [spectrum](references/test_quality_5_modules_spectrum.md), [dossier](references/test_quality_and_evals_dossier.md), [Go module](references/go_test_quality_module.md), [MCP module](references/mcp_test_quality_module.md), and [Harness module](references/harness_test_quality_module.md):

```powershell
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py <target_path> --markdown
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py <target_path> --domain go --markdown
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py --run-evals --eval-module harness
```

1. **Modular Scan (`CoT`):** Run `test_quality_auditor.py` (5 domain auditors + `perfkit_stats.py` for $P_{50}..P_{99.9}$, `stddev` `ddof=1`, `geomean`).
2. **7-Module Audit & Fix (`ReAct + RAW`):** Analyze Problem, AAA, Tautology, Persistence Factors, Levels 1–4 (`0–100`), refactor to Level 4 + re-run (`pytest`/`go test`/`node --test`), and run [`scripts/eval_harness.py`](scripts/eval_harness.py) (`Read-After-Write`).

## 4. Gotchas & Edge Cases

- **Zero-Trust & Guardrail Gate:** Never pass suites by line coverage or `Exit Code 0` alone without checking assertion falsifiability and adversarial boundaries (`pytest.raises`, negative tests).
- **3-Gate Pipeline:** Gate 1 (`code-acceptability-auditor`), **Gate 2 (`test-quality-auditor` — requires Level 4 `81–100 pts`)**, Gate 3 (`gap-analyzer-auditor`).

## 5. Output Schema & Validation Criteria

Emit a 7-Module Dossier per [`rules/audit_criteria.md`](rules/audit_criteria.md) with Level 1–4 table, Before/After diffs, `grading.json` / `benchmark.json`, `[PASS]` / `[FAIL]` / `[UNVERIFIED]`, and `file:///` links.

## 6. User Communication Rule

All direct responses, test audit dossiers, clarifying questions, and summaries addressed to the end user MUST be in **Portuguese (Brazil / `pt-BR`)**, unless explicitly requested otherwise.
