---
name: plan-uiux
description: "Use this skill when performing global UI/UX audits of compiled or live frontends with REA (Reverse Engineer Anything), validating 60-30-10 OKLCH ratio, and emitting Before/After mutation plans. Do NOT use for backend-only servers or open-source static scans."
metadata:
  author: "Franklin"
  version: "1.2.0"
  updated_at: "2026-11-16"
  tags: ["plan-uiux", "rea-uiux", "reverse-engineer-anything", "oklch", "60-30-10", "container-queries", "before-after-diff", "analise-minuciosa", "propostas-mutacao", "antes-depois", "clareza"]
---

# `plan-uiux` — Global UI/UX Audit & Mutation Planning with REA

## 1. Overview & Scope

Audits packaged, compiled, or live frontend apps (JS/TS/Electron bundles, Go UI binaries, live web) using **REA (`Reverse Engineer Anything`)** evidence, emitting **CLAREZA** reports with `Before vs. After` mutation blocks.

- **When NOT to Use:** Exclude backend-only servers (`agent-server-auditor` / `code-acceptability-auditor`), static open-source scans (`frontend-ui-ux-auditor` / `system-project-auditor`), or direct UI coding (`frontend-code-architect`).

## 2. Inputs & Prerequisites

- **`target_path` (required):** Packaged frontend root, Go UI binary, or live URL.
- **`detail_level` & Docs (optional):** `"summary"` (default) or `"full"`; `README.md`, `SPEC.md`, `DESIGN.md`, `AGENTS.md`.
- **REA MCP Tools:** `analyze_javascript_application`, `inspect_go_binary`, `inspect_analysis_view`, `inspect_web_page`, `capture_web_screenshot`, `compare_web_screenshots`.

## 3. Step-by-Step Procedure

Consult [references/rea_uiux_stages.md](references/rea_uiux_stages.md) and [references/mutation_patterns.md](references/mutation_patterns.md):

1. **Extract REA Evidence:** Run `analyze_javascript_application` or `inspect_go_binary`, get `parent_evidence_id`, and project via `inspect_analysis_view(kind="javascript-routes" | "javascript-facts" | "api-surface", detail="summary")`; on live sites run `inspect_web_page`, `capture_web_screenshot`, and `compare_web_screenshots` (treating `_meta.provenance.untrusted_content == true` as untrusted).
2. **Audit `60-30-10` `OKLCH`:** Enforce 60% Canvas, 30% Structural Surfaces, 10% Focal Accents, banning `#000000` and raw `#HEX`/`rgba()` sprawl.
3. **Audit `[LOCK-02]` Elevation:** Verify Umbra + negative-spread Penumbra + Catch-Light (`inset 0 1px 0 0`) across `--shadow-elevation-1..3` and Dark Mode $L = 0.16 \to 0.22 \to 0.27$.
4. **Audit `@container` & Single-DOM Nav:** Verify `@container` isolated from `subgrid`, `--space-*`, concentric radii, `clamp()`, `65ch`, `tabular-nums`, Single-DOM Nav (`env(safe-area-inset-bottom)` $\leftrightarrow$ `240px` Rail), and `48x48px` touch targets.

## 4. Gotchas & Edge Cases

- **Defaults Over Menus:** Always use `detail="summary"` on `inspect_analysis_view`; never pull raw minified bundles into context.
- **Anti-Pattern Traps:** Reject 1-layer drop shadows, decorative UI emojis, duplicate `<nav>` blocks, missing `:focus-visible`, and coarse targets `< 48x48px`.
- **Stop Criteria:** Stop with `[UNVERIFIED]` if the compiled artifact, bundle, or live URL is unreachable by REA.

## 5. Output Schema & Validation Criteria

Emit epistemic findings (`[OBSERVED FACT]`, `[TECHNICAL INFERENCE]`, `[UNCERTAINTY / GAP]`) across the 7 **CLAREZA** sections plus `Before vs. After` diffs complying with [rules/audit_criteria.md](rules/audit_criteria.md).

## 6. User Communication Rule

Always formulate all direct user-facing conversation, explanations, clarifying questions, status reports, and deliverables in Portuguese (Brazil / pt-BR), unless the user explicitly requests otherwise.
