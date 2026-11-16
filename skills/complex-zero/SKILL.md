---
name: complex-zero
description: "Use this skill when auditing dense frontend apps via ReAct CDP DevTools and AST for @xyflow/react infinite canvas, 150ms WebSocket/Chokidar telemetry, ghost nodes, fake stubs, and Next.js 15+ async params. Do NOT use for simple pages or backend-only APIs."
metadata:
  author: "Franklin"
  version: "3.1.0"
  updated_at: "2026-11-16"
  tags: ["complex-zero", "xyflow", "react-flow", "nextjs-15", "async-params", "websocket", "chokidar", "cdp-devtools", "ast-analysis", "canvas-infinito", "nos-fantasmas", "funcoes-falsas", "oklch", "container-queries"]
---

# `complex-zero` — ReAct/CDP, `@xyflow/react` & Anti-Fake AST Auditor

## 1. Overview & Scope

Empirical auditor pairing Chrome DevTools MCP (`take_screenshot`, `take_snapshot`, `evaluate_script`) with static AST checks ([scripts/complex_zero_ast_auditor.py](scripts/complex_zero_ast_auditor.py), [scripts/visual_hierarchy_and_cdp_probe.py](scripts/visual_hierarchy_and_cdp_probe.py), bridged to `SGA`/`TIF` in `system-project-auditor`) for dense UIs: `@xyflow/react`, `WebSocket` + `chokidar`, and Next.js 15+.

- **When NOT to Use:** Exclude simple static pages (`frontend-code-architect`), standalone `DESIGN.md` authoring (`design-md`), 3D physics (`code-quality-audit-3d-physics`), or UI-less backend servers (`agent-server-auditor`).

## 2. Inputs & Prerequisites

- **`target_path` (required) & `live_url` (recommended):** Target path (`.tsx`, `.ts`, `.css`, `.html`, `mcp_apps_ui_*.go`) and live server URL (`http://localhost:3000`).
- **Conditional Pre-Flight:** Consult `google-developer-knowledge`, `gemini_get_doc`, `aistudio.google.com/llms.txt`, and `skills/agent-server-auditor/references/audit-websocket-jsonrpc.md` only when `target_path` uses `WebSocket`, `@google/genai`, or JSON-RPC 2.0.

## 3. Step-by-Step Procedure

See [references/axes_and_cdp_cycle.md](references/axes_and_cdp_cycle.md) and [references/react_devtools_and_xyflow_patterns.md](references/react_devtools_and_xyflow_patterns.md):

1. **`[1. THOUGHT]`:** Map domain tabs, nav slots, and graph nodes without hiding clutter from the primary tab.
2. **`[2. ACTION]`:** Run `uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py --target "<target_path>" [--live-url "<url>"]` (`--dump-cdp-script`); in Chrome DevTools MCP run `navigate_page` $\to$ `take_screenshot` $\to$ `take_snapshot` $\to$ `evaluate_script`.
3. **`[3. OBSERVATION]`:** Cross-check screenshot against probe JSON (`hierarchyMonotonic`, `crampedMenus`, duplicate/backend tabs, `<= 2` node badges) and AST checks (Ghost Nodes, `{}` handlers, `Math.random()`, legacy `reactflow`, sync `params.slug`).
4. **`[4. SELF-CORRECTION]`:** Fix cramped menus (`>= 13px`, `gap >= 6px`, `min-block-size >= 44px`), apply `OKLCH` + `[LOCK-02]` 3-layer shadows + `@container`, batch `WebSocket` at `150ms` (`BATCH_UPDATE`), and migrate Next.js 15+ routes to `Promise<...>` until `total_score >= 90/100`.

## 4. Gotchas & Edge Cases

- **Defaults Over Menus:** Run `--dump-cdp-script` when `live_url` is set; consolidate duplicate/backend tabs in-place.
- **Strict Invariants:** Never pass `< 13px` menus, `Math.random()` metrics, `{}` stubs, hardcoded `'[PASS]'` node tags, or skipped `take_screenshot`/`evaluate_script` on live servers.
- **Stop Criteria:** Stop with `[UNVERIFIED]` if `target_path` is missing or `live_url` is unreachable.

## 5. Output Schema & Validation Criteria

Emit `Target | URL | Complex-Zero Score [XX/100] | SGA [XX.XX/100]` across 4 Axes (`25 pts` each, `[PASS] >= 90`, `[WARN] >= 75`, `[FAIL] < 75`) per [rules/audit_criteria.md](rules/audit_criteria.md) with `file:line` fixes.

## 6. User Communication Rule

Always formulate all direct user-facing conversation, explanations, clarifying questions, status reports, and deliverables in Portuguese (Brazil / pt-BR), unless the user explicitly requests otherwise.
