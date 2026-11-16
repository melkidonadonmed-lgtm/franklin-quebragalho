---
name: frontend-ui-ux-auditor
description: "Use this skill when mathematically auditing DOM node density, WCAG 2.1 AA contrast, 90-120 zenithal light, 3-layer elevation shadows, spacing, and @layer rules via ui_ux_frontend_auditor.py. Do NOT use for refactoring code, backend audits, or runtime CDP."
metadata:
  author: "Franklin"
  version: "3.1.0"
  updated_at: "2026-11-16"
  tags: ["frontend-ui-ux-auditor", "ui-ux", "oklch", "wcag", "contraste", "luz-zenital", "densidade-dom", "sombras-elevacao", "container-queries", "divsoup", "precisao-matematica"]
---

# `frontend-ui-ux-auditor` — Mathematical UI/UX & Optical Physics Auditor

## 1. Overview & Scope

Performs deterministic mathematical and visual audits on `.html`, `.css`, `.jsx`, `.tsx`, and `.vue` files via [scripts/ui_ux_frontend_auditor.py](scripts/ui_ux_frontend_auditor.py), scoring the **9-Axis SSOT** (`rules/frontend-9-axes-guidelines.md`) across 6 weighted dimensions.

- **When NOT to Use:** Read-only diagnostic skill; do not use for editing/refactoring UI code (`frontend-code-architect`), authoring `DESIGN.md` (`design-md`), backend/SQL audits (`agent-server-auditor`), or live browser CDP testing (`complex-zero` / `system-project-auditor`).

## 2. Inputs & Prerequisites

- **`target_path` (required):** Frontend file (`.html`, `.css`, `.jsx`, `.tsx`, `.vue`) or directory.
- **Engine & Contract:** [scripts/ui_ux_frontend_auditor.py](scripts/ui_ux_frontend_auditor.py) (`--target`, `--json`, `--self-test`) and optional `<project_root>/DESIGN.md`.

## 3. Step-by-Step Procedure

Consult [references/ui_ux_6_dimensions_rubric.md](references/ui_ux_6_dimensions_rubric.md) and [references/tactile_elevation_and_shadows.md](references/tactile_elevation_and_shadows.md):

1. **Run Static Auditor:** Execute `uv run python skills/frontend-ui-ux-auditor/scripts/ui_ux_frontend_auditor.py --target "<target_path>" --json`.
2. **Dim 1 — Tokens & `4px/8px` Scale (`0.20`):** Check `--bg-canvas`/`--surface-canvas`, `oklch()`, `light-dark()`, Dark Mode $L = 0.16 \to 0.27$, concentric radii, and zero off-scale values (`p-[13px]`).
3. **Dim 2 — Fluid Type & WCAG AA (`0.20`):** Check viewport meta, `clamp()`, `65ch`, `balance/pretty`, `antialiased`, `font-synthesis: none`, zero fractional `scale()` on text, and $CR \ge 4.5:1$.
4. **Dim 3 — Box, DOM & Nav (`0.15`):** Verify `border-box`, `flow-root`, DOM depth `<= 12`, `divsoup_ratio <= 0.45`, HTML5 landmarks, `:focus-visible`, Breadcrumbs (`>= 3` levels), and DOM = Tab order.
5. **Dims 4–6 — Icons (`0.15`), `[LOCK-02]` Shadows (`0.15`) & Motion (`0.15`):** Check 1:1 SVGs (`16/20/24px`), zero emojis, Umbra + negative Penumbra + `--catch-light`, `isolation: isolate`, `@container`, `cubic-bezier(0.22, 1, 0.36, 1)`, zero reflow animations, `any-pointer: coarse` (`>= 48px`), and `prefers-reduced-motion`.

## 4. Gotchas & Edge Cases

- **Defaults Over Menus:** Pass `--json` by default; reserve `--self-test` for engine checks.
- **Optical & CSS Traps:** Flag single-pass `rgba(0,0,0)` shadows, `#000000`, `transition: ... allow-discrete` inside shorthands, and `width`/`height`/`margin` animations.
- **Stop Criteria:** Stop and report `[UNVERIFIED]` if `target_path` is missing or contains no eligible frontend files.

## 5. Output Schema & Validation Criteria

Emit $\text{Score}_{\text{UI/UX}} = \sum_{j=1}^{6} W_j \cdot S_j$ (`0..100`), grade, dimension scores, and violations per [rules/audit_criteria.md](rules/audit_criteria.md) (`PASS` requires `final_score >= 85.0`, zero contrast errors, and `zero_reflow_motion == true`).

## 6. User Communication Rule

Always formulate all direct user-facing conversation, explanations, clarifying questions, status reports, and deliverables in Portuguese (Brazil / pt-BR), unless the user explicitly requests otherwise.
