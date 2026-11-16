# Deterministic Audit Criteria — `frontend-code-architect` (`v7.0.0`)

Objective and falsifiable criteria (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for auditing frontend code implementation against the **9-Axis SSOT** (`rules/frontend-9-axes-guidelines.md`).

---

## 1. Modularity (`<= 300 lines`), Reference Preservation & 3 Complexity Tiers (`[AUDIT-ARCH-01]`)

- **`[PASS]`**: Respects the `<= 300 lines` (`~15 KB`) threshold per file/call and preserves user design references. Structures the project proportionally to scope: **Tier 1** (standalone `.html` `<= 150 KB` or native CSS with `@layer tokens, reset, layouts, components, utilities;`), **Tier 2** (Feature-Driven SPA with `src/components/{ui,layout}` and `src/features/<domain>/` or Atomic Design), or **Tier 3** (Fullstack App Router with `(marketing)` / `(workspace)`, private `_components/`, `Viewport` API, and synchronous anti-FOUC script).
- **`[FAIL]`** (`MONOLITH_OR_DISCARDED_REFERENCE`): Files `> 300 lines` (hard ceiling `600`), replacing functional user references with generic templates, or embedding Base64 bitmaps `> 50 KB`.
- **`[UNVERIFIED]`**: Target path is not yet initialized on disk.

## 2. Logical Box Model, Anti-Margin-Collapse, 3-Layer `OKLCH` Tokens & `[LOCK-02]` Shadows (`[AUDIT-ARCH-02]`)

- **`[PASS]`**: Enforces `box-sizing: border-box`, logical properties (`inline-size`, `padding-inline`, `margin-block`), BFC containment (`display: flow-root`, parent `gap`, `.prose > * + *`), **3-layer tokens** (*Primitives*, *Semantics* `--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--text-primary`/`--ink-primary` via `oklch()`, `light-dark()`, `color-mix()`, and RCS `from`, and *Component*), progressive Dark Mode $L$ elevation (`0.16 -> 0.22 -> 0.27`), multi-layer shadows (`--shadow-elevation-1..3` / `--elevation-1..3`, `--shadow-inset`, `drop-shadow()`), and `isolation: isolate` on blend modes.
- **`[FAIL]`** (`CHROMATIC_POLLUTION_OR_WASHED_SHADOW`): Neon/oversaturated highlights, pure `#000000` causing OLED smearing, single-pass flat shadows, or vertical margin collapse leaking due to missing `flow-root`/`gap`.

## 3. Anti-GPU-Blur Fluid Typography, `@container`, 4 Cards & 3-Layer Navigation (`[AUDIT-ARCH-03]`)

- **`[PASS]`**: Applies `antialiased`, `grayscale`, `optimizeLegibility`, `font-optical-sizing: auto`, and `font-synthesis: none` on `html, body`; fluid `clamp()` scale, `max-inline-size: 65ch`, `text-wrap: balance/pretty`, and `font-variant-numeric: tabular-nums`; separates Macrolayout (`@media`, Grid RAM) from Microlayout (`@container`); contextually implements the **4 Card Variants** (`elevated`, `outlined`, `subtle`, `interactive`), **Contextual Navigation** (*Global*, *Local/In-Page* when applicable, *Breadcrumbs* `<ol role="list">` + `aria-current="page"` strictly for hierarchies $\ge 3$ levels, DOM Order = Visual Order), zero UI emojis, `@media (prefers-reduced-motion: reduce)`, and `@media (any-pointer: coarse)` ($\ge 48\text{px}$ / $\ge 44\text{px}$).
- **`[FAIL]`** (`GPU_BLUR_EMOJI_OR_BROKEN_TAB_ORDER`): Fractional `scale()` on text containers, `flex-direction: row-reverse` breaking navigation `Tab` sequence, missing `font-synthesis: none`, or presence of UI emojis.

## 4. Real-State Engineering (Zero Placebos), Zero Orphans & Strict Typing (`[AUDIT-ARCH-04]`)

- **`[PASS]`**: Enforces strict TypeScript/ES6+ contracts (zero `any`), real view/feature consumption of every created component (zero orphans), and 100% real functional logic across all controls (search, filter, calculation, persistence, and states `idle`, `active`/`loading`, `empty`, `error`, `pressed` — zero `setTimeout` placebos or `alert('Coming soon')`).
- **`[FAIL]`** (`PLACEBO_OR_ORPHAN_COMPONENT`): Fake/stub functions, controls without effect on real state, or unused orphan components inside `src/components/ui/`.
