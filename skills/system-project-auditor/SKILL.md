---
name: system-project-auditor
description: "Audit real repository code (AST), physical structure, MVP readiness, 3-layer navigation (X activates Y / SGA), 60-30-10 OKLCH UI physics, and live DOM via agent-browser @eX (0-100 score). Use for repository, MVP, and navigation audits. Do NOT use for refactoring code, greenfield scaffolding, or README syncing."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "6.0.0"
  updated_at: "2026-11-16"
  author: "Franklin"
  category: "Unified Project, Real-Code AST, MVP, SGA & 60-30-10 OKLCH Auditing"
  tags: ["system-project-auditor", "auditoria-projetos-sistema", "antigravity-project-auditor", "nav-x-func", "auditoria", "projeto", "projetos", "sistemas", "mvp", "ilhas", "ilhas-funcionais", "navegacao", "navegabilidade", "sga", "tif", "ast", "orfao", "agent-browser", "estrutural", "repositorios", "camadas", "dead-ends", "evolucao", "60-30-10-oklch", "3-layer-navigation", "deterministic-scorer"]
---

# `system-project-auditor` (`v6.0.0`) — Real Code, MVP, `SGA` & OKLCH

> Canonical 3-in-1 fusion. Never audit from `.md` docs alone—run `scripts/` first on AST code and disk layout.

## 1. Overview & Scope

- **Mode 1 (`mvp_and_plan`):** MVP blocker diagnosis emitting the **5 Pillars** table and **3-Phase Plan**.
- **Mode 2 (`deep_code_and_nav_audit` — default):** AST health, orphans, Docs-vs-Disk parity, 3-Layer Navigation (`X activates Y`), `OKLCH 60-30-10`, 3-Level Shadows, `0–100` score, `SGA`, and `TIF`.
- **Mode 3 (`live_dom_inspection` — HITL):** Live DOM audit (`@eX`, menus `>=13px`/`gap>=8px`, FSM, Dark/Light) via `agent-browser` or `chrome-devtools-mcp`.
- **When NOT to Use:** Do NOT use to refactor code (`frontend-code-architect`), bootstrap/sync `README.md` (`project-idea-organizer`), or audit Android/APKs (`android-agy-projects`, `re-a-ndroid`).

## 2. Inputs & Prerequisites

- **`project_root_path`** (required), **`execution_mode`**, **`user_focus_query`**, **`app_url`** (Mode 3 requires HITL).

```powershell
uv run python skills/system-project-auditor/scripts/project_structure_and_code_auditor.py --target <path>
uv run python skills/system-project-auditor/scripts/frontiercode_maintainability_guardrail.py <file.py>
uv run python skills/system-project-auditor/scripts/deterministic_scorer.py --scan <path>
uv run python skills/system-project-auditor/scripts/ai_ready_data_pipeline.py
```

## 3. Step-by-Step Procedure

1. **Governance & Parity (`40 pts`):** Audit `README.md`, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `CURRENT_STATE.md`, `DESIGN.md`, `rules/`, `.env.example`, `.gitignore`; classify (`[IMPLEMENTED_FUNCTIONAL | SUPERFICIAL_MOCK | DOCUMENTED_MISSING | GHOST_CODE]`).
2. **AST, Orphans & MCP (`40 pts`):** Flag orphans, stubs, `>60`-line functions, strict schemas (`extra="forbid"` / `Zod .strict()`), STDIO hygiene; for Gemini/WS/JSON-RPC, query `google-developer-knowledge`/`gemini_get_doc` and apply `agent-server-auditor`.
3. **`60-30-10 OKLCH`, Shadows & `SGA` (`20 pts`):** Verify via [report axes](references/audit_report_and_oklch_axes.md), [5 pillars](references/pillars_5_matrix_and_handoff_2026.md), [rubric](references/audit_rubric_and_agent_browser.md), and [UI taxonomy](references/ui_subagent_taxonomy_6_layers.md).

## 4. Gotchas & Edge Cases

- Run `project_structure_and_code_auditor.py` and `deterministic_scorer.py` before emitting findings.
- Never mutate code without HITL approval, never pass placebos (`onClick={() => {}}`, `pass`), and never open URLs in `agent-browser` without HITL.

## 5. Output Schema & Validation Criteria

Emit `[PASS]`, `[FAIL]`, or `[UNVERIFIED]` per [`rules/audit_criteria.md`](rules/audit_criteria.md): Score `XX/100`, `SGA`, `TIF`, causal MVP diagnosis, AST parity table, 5 Pillars Matrix, and 3-Phase Plan.

## 6. User Communication Rule

All direct responses, audit reports, clarifying questions, and summaries to the end user MUST be in **Portuguese (Brazil / `pt-BR`)**, unless explicitly requested otherwise.
