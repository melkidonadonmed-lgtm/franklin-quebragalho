---
name: design-md
description: "Use this skill when creating or updating a project's DESIGN.md contract with 3-layer OKLCH semantic tokens, modular type scale, spacing, and zenith shadows. Do NOT use for implementing React/Tailwind UI components or backend-only projects."
metadata:
  author: "Franklin"
  version: "8.2.0"
  updated_at: "2026-11-16"
  tags: ["design-md", "design-system", "oklch", "light-dark", "tokens-semanticos", "escala-tipografica", "contrato-design", "sombras-elevacao", "luz-zenital", "container-queries", "starting-style", "acessibilidade"]
---

# `design-md` — Contextual `DESIGN.md` Contract Authoring

## 1. Overview & Scope

Synthesizes `<project_root>/DESIGN.md` from product purpose, audience, and stack via [references/design_md_5_pillars_detailed.md](references/design_md_5_pillars_detailed.md), [references/design_system_composition_reference.md](references/design_system_composition_reference.md), and [references/spacing_tokens_and_stitch_hierarchy.md](references/spacing_tokens_and_stitch_hierarchy.md).

- **When NOT to Use:** Exclude backend/CLI services without UI, architecture specs (`solution-content-architect`), `CONTEXT.md`, `AGENTS.md`, and direct React/Tailwind coding (`frontend-code-architect`).

## 2. Inputs & Prerequisites

- **Product Context:** Domain purpose, complexity tier (`Tier 1..3`), and one canonical Spatial Archetype (of 6).
- **Optional Assets & Baseline:** `README.md`, `SPEC.md`, existing CSS tokens, `rules/frontend-9-axes-guidelines.md`, and [rules/audit_criteria.md](rules/audit_criteria.md).

## 3. Step-by-Step Procedure

1. **Purpose & Archetype:** Justify hue ($H$), chroma ($C$), and density by domain; require a *Functional Hero* and pick one archetype (`Split-View`, `12-Col Bento`, `Command Center`, `Editorial 65ch`, `Spatial HUD`, or `Vector A4`).
2. **Logical Box & Type:** Mandate `border-box`, logical CSS (`inline-size`, `padding-inline`, `margin-block`), `flow-root`, `gap`, `.prose > * + *`, `4px/8px` `--space-*`, concentric radii, `clamp()` ($\max \le 2.5\times \min$), `65ch`, `balance/pretty`, `tabular-nums`, `antialiased`, and `font-synthesis: none`.
3. **3-Layer `OKLCH` (`60-30-10`):** Define Primitives, Semantics (`--bg-canvas`/`--surface-canvas` 60%, `--bg-surface-1`/`--surface-card` 30%, `--brand-primary` 10%), and Component tokens via `oklch()`, `light-dark()`, `color-mix()`, and RCS `from`; raise Dark Mode $L$ (`0.16 -> 0.22 -> 0.27`, zero `#000000`).
4. **`[LOCK-02]` Zenith Shadows:** Specify Umbra + negative-spread Penumbra (`-1px..-8px`) + Catch-Light (`inset 0 1px 0 0`) across `--shadow-elevation-1..3`, `--shadow-inset`, `text-shadow`, and `drop-shadow()`, adding only pertinent modes (Glass, Tactile, Dark Glow, `<dialog>` + `@starting-style`).
5. **AOM & `@layer`:** Enforce DOM = Tab order, `:focus-visible`, `any-pointer: coarse` (`>= 48px`), `prefers-reduced-motion`, 3-layer nav with Breadcrumbs (`>= 3` levels), Real-State FSM, and `@layer` without `!important`.

## 4. Gotchas & Edge Cases

- **Defaults Over Menus:** Infer hue, tier, and archetype from the product brief without stalling on preference menus.
- **Hard Bans:** Reject flat single-pass shadows, `#000000`, neon colors, fractional `scale()` on text, UI emojis, and unrelated addenda.
- **Stop Criteria:** Stop with `[UNVERIFIED]` if no UI scope exists or `<project_root>` is inaccessible.

## 5. Output Schema & Validation Criteria

Deliver `<project_root>/DESIGN.md` covering Purpose/Hero, 3-Layer `OKLCH` Tokens, 3-Layer Shadows, Spatial/Type Rules, and AOM/`@layer`, passing `[AUDIT-DESIGN-01]`..`[AUDIT-DESIGN-04]` in [rules/audit_criteria.md](rules/audit_criteria.md).

## 6. User Communication Rule

Always formulate all direct user-facing conversation, explanations, clarifying questions, status reports, and deliverables in Portuguese (Brazil / pt-BR), unless the user explicitly requests otherwise.
