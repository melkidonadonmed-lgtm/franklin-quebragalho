# Deterministic Audit Criteria — `design-md` (`v8.2.0`)

Objective and falsifiable criteria (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for auditing the creation and update of the `DESIGN.md` architectural contract aligned with the **9-Axis SSOT** (`rules/frontend-9-axes-guidelines.md`).

---

## 1. Logical Box Model, Anti-Margin-Collapse & Purpose-Driven Identity (`[AUDIT-DESIGN-01]`)

- **`[PASS]`**: `DESIGN.md` explicitly states `project_purpose`, `complexity_tier` (*Tier 1: Static `@layer`*, *Tier 2: Feature-Driven SPA*, or *Tier 3: Fullstack App Router & PWA*), selects one of the **6 Canonical Spatial Archetypes**, and mandates `box-sizing: border-box`, logical properties (`inline-size`, `block-size`, `padding-inline`, `margin-block`), and margin-collapse prevention (`display: flow-root`, parent `gap`, and `.prose > * + *`).
- **`[FAIL]`** (`TEMPLATED_THEME_OR_PHYSICAL_BOX`): Mechanical reuse of an unrelated project's layout/palette without matching the domain purpose, or omission of logical properties and BFC containment.
- **`[UNVERIFIED]`**: Target project root path is inaccessible on disk.

## 2. Perceptual `OKLCH` Colors, Light/Dark Themes & 3-Layer Tokens (`[AUDIT-DESIGN-02]`)

- **`[PASS]`**: Organizes tokens into **3 Hierarchical Layers** (*1. Primitives*, *2. Semantic/Alias* reactive tokens using `oklch()`, `light-dark()`, `color-mix(in oklab, ...)`, and Relative Color Syntax RCS `from`, *3. Component*), synchronizes `<meta name="color-scheme" content="light dark">` and `color-scheme: light dark`, enforces the `60-30-10` ratio, and defines progressive lightness $L$ elevation in Dark Mode (`0.16 -> 0.22 -> 0.27`, avoiding pure `#000000`).
- **`[FAIL]`** (`CHROMATIC_POLLUTION_OR_MISSING_3_LAYERS`): Neon/oversaturated accents for artificial contrast, pure `#000000` causing OLED smearing in Dark Mode, or missing separation between primitive and semantic tokens (`--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--text-primary`/`--ink-primary`).

## 3. `[LOCK-02]` Multi-Layer Shadows (3 Types), Zenith Lighting & Fluid Typographic Sharpness (`[AUDIT-DESIGN-03]`)

- **`[PASS]`**: Specifies all 3 shadow properties (`box-shadow` with `inset` and negative `spread`, `text-shadow`, `filter: drop-shadow()`), realistic 3-level shadows (Contact Umbra + negative-spread Penumbra `-1px..-8px` + Top Catch-Light `inset 0 1px 0 0` and `--shadow-inset`), `isolation: isolate` for blend modes, fluid `clamp()` scale ($\max \le 2.5\times \min$), `max-inline-size: 65ch`, `text-wrap: balance/pretty`, `antialiased` + `font-synthesis: none`, zero fractional `scale()` on text, and `font-variant-numeric: tabular-nums`.
- **`[FAIL]`** (`WASHED_SHADOW_OR_GPU_BLUR_RISK`): Single-pass flat shadow (`0 4px 12px rgba(0,0,0,0.4)`), missing `font-synthesis: none`, or missing `tabular-nums` on metrics/tables.

## 4. Macro/Microlayout (`@container`), 4 Card Variants, 3-Layer Navigation & Real-State (`[AUDIT-DESIGN-04]`)

- **`[PASS]`**: Separates Macrolayout (`@media`, CSS Grid RAM) from Microlayout (`@container` isolated from `subgrid`), defines contextual usage of the **4 Card Variants** (*Elevated*, *Outlined*, *Filled/Subtle*, *Interactive*), specifies **Contextual Navigation** (*Global*, *Local/In-Page* when applicable, and *Breadcrumbs* `<ol role="list">` + `aria-current="page"` strictly in hierarchies $\ge 3$ levels, DOM Order = Visual Order), `cubic-bezier(0.22, 1, 0.36, 1)` easing, `@media (prefers-reduced-motion: reduce)`, `@media (any-pointer: coarse)` ($\ge 48\text{px}$ / $\ge 44\text{px}$ touch target), zero UI emojis, and 100% Real-State Engineering.
- **`[FAIL]`** (`PLACEBO_EMOJI_OR_BROKEN_NAV`): Permitting emojis in the UI, `flex-direction: row-reverse` breaking `Tab` focus order, or omitting real functional states (`idle`, `loading`, `empty`, `error`, `pressed`).
