---
name: system-project-auditor
description: "Audit existing repositories (0-100 score + SGA) across real AST code health, Docs-vs-Disk parity, causal MVP blockers, and, for UI targets, 3-layer navigation (X activates Y), 60-30-10 OKLCH physics, and live agent-browser @eX DOM. Use for repository, MVP, and navigation audits. Do NOT use for coding (solution-content-architect), scaffolding (project-idea-organizer), or APKs (re-a-ndroid)."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: read_file run_command
metadata:
  version: "6.1.0"
  updated_at: "2026-11-17"
  author: "Franklin"
  category: "Unified Project, Real-Code AST, MVP, SGA & 60-30-10 OKLCH Auditing"
  tags: "system-project-auditor, auditoria-projetos-sistema, antigravity-project-auditor, nav-x-func, auditoria, projeto, projetos, sistemas, mvp, ilhas, ilhas-funcionais, navegacao, navegabilidade, sga, tif, ast, orfao, agent-browser, estrutural, repositorios, camadas, dead-ends, evolucao, 60-30-10-oklch, 3-layer-navigation, deterministic-scorer"
---

# `system-project-auditor` (`v6.1.0`) — Stack-Adaptive Code, MVP & `SGA`

> Canonical 3-in-1 read-only fusion. Never audit from `.md` docs alone—run `scripts/` on real AST code and disk layout first.

## 1. Overview & Scope

- **Mode 1 (`mvp_and_plan`):** Causal MVP blocker diagnosis emitting the **5 Pillars** matrix and a defect-driven remediation list.
- **Mode 2 (`deep_code_and_nav_audit` — default):** Polyglot AST health (Python, TS/JS, Go), orphans, Docs-vs-Disk parity, `0–100` score, `SGA`/`TIF`, plus 3-Layer Navigation (`X activates Y`) and `OKLCH 60-30-10` *only when UI exists*.
- **Mode 3 (`live_dom_inspection` — HITL, UI only):** Live DOM audit (`@eX`, menus `>=13px`/`gap>=8px`, FSM, Dark/Light) via `agent-browser` or `chrome-devtools-mcp`.
- **When NOT to Use:** Do NOT refactor or write app code (`solution-content-architect` / `ui-clean-worker`), scaffold/sync `README.md` (`project-idea-organizer`), or audit Android/APKs (`android-agy-projects`, `re-a-ndroid`).

## 2. Inputs & Prerequisites

- **`project_root_path`** (required), **`execution_mode`**, **`user_focus_query`**, **`app_url`** (Mode 3 requires HITL and UI).

```powershell
uv run python skills/system-project-auditor/scripts/project_structure_and_code_auditor.py --target <path>
uv run python skills/system-project-auditor/scripts/deterministic_scorer.py --scan <path>
# Run ONLY when Python files exist in <path>:
uv run python skills/system-project-auditor/scripts/frontiercode_maintainability_guardrail.py <file.py>
```

## 3. Step-by-Step Procedure

1. **Step 0 — Composable Stack Capability Gating:** Detect `has_ui_layer`, `has_agent_or_mcp_layer`, and `has_python_files` from scanner output. If `has_ui_layer == False`, mark UI/OKLCH/Mode 3 `@eX` as `[PASS: N/A_BACKEND_ONLY]`, reallocate those `20` UI points to AST/Contract/Parity health, and forbid any UI action items.
2. **Governance, Parity & AST (`75 pts` headless / `65 pts` UI; ReAct + CoT):** Audit `README.md`, `AGENTS.md`, `.context/spec.md`, `.context/context.md` (optional on `1–4` file standalone micro-repos), `.env.example`, `.gitignore`; classify real modules (`[IMPLEMENTED_FUNCTIONAL | SUPERFICIAL_MOCK | DOCUMENTED_MISSING | GHOST_CODE]`); if `has_agent_or_mcp_layer == True`, apply `agent-server-auditor` and query `google-developer-knowledge`/`gemini_get_doc`.
3. **Conditional UI `60-30-10 OKLCH` & `SGA` (`20 pts` when UI exists + `15 pts` Contracts/HITL):** Verify via [report axes](references/audit_report_and_oklch_axes.md), [5 pillars](references/pillars_5_matrix_and_handoff_2026.md), [rubric](references/audit_rubric_and_agent_browser.md), [UI taxonomy](references/ui_subagent_taxonomy_6_layers.md), and [V1 vs V2 diff template](templates/resolution_diff_v1_v2.html).

## 4. Gotchas & Edge Cases

- Run `project_structure_and_code_auditor.py` and `deterministic_scorer.py` before emitting findings; never run `frontiercode_maintainability_guardrail.py` without a `.py` file argument.
- Never mutate code without HITL approval, never pass placebos (`onClick={() => {}}`, `pass`), and never open URLs in `agent-browser` without HITL.

## 5. Output Schema & Validation Criteria

Emit `Read-After-Write`-verified verdicts (`[PASS]`, `[FAIL]`, `[PASS: N/A_BACKEND_ONLY]`, `[UNVERIFIED]`) per [`rules/audit_criteria.md`](rules/audit_criteria.md): Score `XX/100`, `SGA`, `TIF`, causal MVP diagnosis, AST parity table, 5 Pillars Matrix, and a **Defect-Driven Action Plan** (1:1 traced to real findings; output `No structural remediation required` when clean).

## 6. User Communication Rule

All direct responses, audit reports, clarifying questions, and summaries to the end user MUST be in **Portuguese (Brazil / `pt-BR`)**, unless explicitly requested otherwise.
