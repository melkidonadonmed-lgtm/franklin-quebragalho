---
name: frontend-code-architect
description: "Use this skill when implementing or refactoring React, Next.js, and Tailwind web UI components from DESIGN.md with OKLCH 3-layer tokens, @container, 4 card variants, and Real-State FSM. Do NOT use for authoring DESIGN.md contracts alone or backend-only services."
metadata:
  author: "Franklin"
  version: "7.0.0"
  updated_at: "2026-11-16"
  tags: ["frontend-code-architect", "react", "nextjs", "tailwind", "oklch", "container-queries", "cards", "sombras-elevacao", "fsm", "estados-finitos", "implementar-refatorar-interfaces", "real-state"]
---

# `frontend-code-architect` — Frontend Implementation & Real-State Engineering

## 1. Overview & Scope

Implements and refactors web UI code aligned with `rules/frontend-9-axes-guidelines.md` and `DESIGN.md` (`design-md`), delivering logical CSS, 3-layer `OKLCH` tokens, `@container`, 4 card variants, single-DOM nav, and Real-State FSMs.

- **When NOT to Use:** Exclude `DESIGN.md`-only authoring (`design-md`), read-only audits (`frontend-ui-ux-auditor`, `frontend-testing-auditor`), `@xyflow/react` CDP graphs (`complex-zero`), and clinical EHR/A4 systems (`clinical-minimalist-ui`).

## 2. Inputs & Prerequisites

- **`target_path` (required):** Standalone `.html` or frontend root directory.
- **`complexity_tier` & `design_contract` (optional):** Auto-detected `tier_1_static` (`@layer` `<= 150 KB`), `tier_2_spa_feature`, or `tier_3_fullstack_pwa` (App Router + PWA); `<project_root>/DESIGN.md`.

## 3. Step-by-Step Procedure

See [references/architecture_4_modules_and_axes.md](references/architecture_4_modules_and_axes.md), [references/canonical_templates.md](references/canonical_templates.md), [references/layout_grid_cards_and_navigation.md](references/layout_grid_cards_and_navigation.md), and [references/tactile_elevation_and_shadows.md](references/tactile_elevation_and_shadows.md):

1. **Tier Structure (`tier_1..3`):** Organize `@layer`, Feature-Driven SPA (`src/{app,styles,components/{ui,layout},features/<domain>}`), or App Router PWA (`(marketing)/`, `(workspace)/`, `_components/`, anti-FOUC, `Viewport`), keeping files `<= 300 lines`.
2. **Logical Box & `[LOCK-02]` `OKLCH`:** Apply `border-box`, logical CSS, `flow-root`/`gap`, `clamp()`, `65ch`, `antialiased`, `font-synthesis: none`, `tabular-nums`, 3-layer `OKLCH` (`light-dark()`/`color-mix()`/`from`), Dark $L = 0.16 \to 0.27$, and 3-layer shadows (`--shadow-elevation-1..3`, `--shadow-inset`, `drop-shadow()`, `isolation: isolate`).
3. **Macro/Micro (`@container`) & Cards:** Build Grid RAM, `@container` off `subgrid`, 4 card variants (`elevated`, `outlined`, `subtle`, `interactive`), `cubic-bezier(0.22, 1, 0.36, 1)`, `any-pointer: coarse` (`>= 48px`), `content-visibility: auto`, and `display-mode: standalone`.
4. **Single-DOM Nav & FSM:** Transition Bottom Bar (`env(safe-area-inset-bottom)`) $\leftrightarrow$ `240px` Rail, add Breadcrumbs (`>= 3` levels), preserve DOM = Tab order, and wire real `idle | loading | empty | error | pressed` states.

## 4. Gotchas & Edge Cases

- **Defaults Over Menus:** Infer `complexity_tier` and folder layout from `package.json`/`next.config.*`.
- **Hard Bans:** Zero `#000000`, flat shadows, fractional `scale()` on text, uncontained margin collapse, `setTimeout` placebos, `alert('Coming soon')`, `row-reverse` breaking `Tab`, UI emojis, Base64 `> 50 KB`, or orphan `ui/` components.
- **Stop Criteria:** Stop with `[UNVERIFIED]` if `target_path` is missing; preserve existing user references.

## 5. Output Schema & Validation Criteria

Deliver modular files (`<= 300 lines`, zero `any`, zero orphans) verified against [rules/audit_criteria.md](rules/audit_criteria.md) and post-edit `frontend-ui-ux-auditor` + `frontend-testing-auditor` runs.

## 6. User Communication Rule

Always formulate all direct user-facing conversation, explanations, clarifying questions, status reports, and deliverables in Portuguese (Brazil / pt-BR), unless the user explicitly requests otherwise.
