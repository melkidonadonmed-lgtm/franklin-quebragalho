# Mathematical Specification of the 6 Dimensions — Frontend UI/UX Auditor

Detailed criteria for the 9 Axes audited by [`../SKILL.md`](../SKILL.md) and [`../scripts/ui_ux_frontend_auditor.py`](../scripts/ui_ux_frontend_auditor.py), integrating `rules/frontend-9-axes-guidelines.md` and [`tactile_elevation_and_shadows.md`](tactile_elevation_and_shadows.md).

## Dimension 1: 3-Layer Design Tokens (`OKLCH`) & Spacing (`W = 0.20`)

- **Token Layers:** Primitives (`--primitive-*`, `--space-*`) $\to$ Semantics (`--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--text-primary`/`--ink-primary`, `--border-subtle`) $\to$ Component tokens using `oklch()`, `light-dark()`, `color-mix(in oklab, ...)`, and RCS (`from`). Dark Mode elevates $L = 0.16 \to 0.22 \to 0.27$ (zero pure `#000000`).
- **Stitch Scale & Concentric Radii:** Progression `4, 8, 12, 16, 24, 32, 48, 64px` (`--space-*`, `--space-card-gap`, `--space-card-padding`, `--space-grid-gap`, `--space-section-inset`), satisfying $\text{Inner Gap} < \text{Card Padding} \le \text{Grid Gap} < \text{Section Inset}$ and $R_{\text{inner}} = \max(4\text{px}, R_{\text{outer}} - \text{Padding})$, rejecting magic numbers (`p-[13px]`, `margin: 11px`).

## Dimension 2: Fluid Typography, GPU Sharpness & WCAG 2.1 AA (`W = 0.20`)

- `-webkit-font-smoothing: antialiased`, `text-rendering: optimizeLegibility`, `font-optical-sizing: auto`, `font-synthesis: none` on `html, body`; fluid `clamp()`, `max-inline-size: 65ch` (`text-wrap: pretty`), `text-wrap: balance` on `h1`–`h4`, and `tabular-nums` on numeric metrics.
- Forbid fractional `scale()` on text containers and fonts `< 12px`; enforce luminance contrast $CR = \frac{L_{\text{lighter}} + 0.05}{L_{\text{darker}} + 0.05} \ge 4.5:1$ (normal text) and $\ge 3.0:1$ (large text/UI).

## Dimension 3: Logical Box Model, DOM & 3-Layer Navigation (`W = 0.15`)

- `box-sizing: border-box`, logical properties (`inline-size`, `block-size`, `padding-inline`, `margin-block`, `border-inline-start`), `display: flow-root`, `gap`, and `.prose > * + *`.
- Max DOM depth $\le 12$ levels and `divsoup_ratio <= 0.45` with HTML5 semantic landmarks (`<main>`, `<header>`, `<nav>`, `<aside>`, `<section>`, `<article>`).
- Contextual Navigation: (1) Global (`<nav aria-label>`), (2) Local/In-Page, (3) Breadcrumbs (`<nav aria-label="Breadcrumb"><ol role="list">` + `aria-current="page"`, mandatory **only in deep hierarchies $\ge 3$ levels**), `:focus-visible`, and DOM Order = Visual Order (no `row-reverse` or arbitrary `order`).

## Dimension 4: 1:1 Vector Iconography & Zero Emojis (`W = 0.15`)

- Standardized 1:1 square bounding box (`16x16px`, `20x20px`, `24x24px`), single vector icon family (Lucide or Phosphor, `stroke-width: 1.75`), `filter: drop-shadow()` on alpha masks, and zero UI emojis.

## Dimension 5: Zenithal Light (`90°–120°`), 3 Shadows & Blend Isolation (`W = 0.15`)

- Primitives `--shadow-layer-sm/md/lg` and Semantic elevation tokens combining **Contact Umbra** + **Negative-Spread Penumbra (`-1px`..`-8px`)** + **Top Catch-Light (`inset 0 1px 0 0`)** in `--shadow-elevation-1..3` / `--elevation-1..3` / `--shadow-elevation-low/medium/high` (+ *Ambient Brand Glow* in Dark Mode) and recessed cavities (`--shadow-inset` / `--elevation-pressed-inset`).
- `isolation: isolate` on `mix-blend-mode` surfaces and `linear-gradient(in oklch longer hue ...)`.

## Dimension 6: `@container`, Cards, PWA & Physical Motion (`W = 0.15`)

- CSS Grid RAM (`minmax(min(100%, 280px), 1fr)`), Flexbox (`flex-wrap: balance`, `align-items: safe center`, `min-inline-size: 0`), `container-type: inline-size` separated from `subgrid` (4 regions + `.card:has(> img)`), 4 card variants (*Elevated*, *Outlined*, *Filled/Subtle*, *Interactive*), Bottom Bar (`env(safe-area-inset-bottom)`) $\leftrightarrow$ `240px` `100dvh` Sidebar Rail, and `@media (display-mode: standalone)`.
- Animate strictly `transform` and `opacity` (`cubic-bezier(0.22, 1, 0.36, 1)`), declare `transition-behavior: allow-discrete` separately after `transition`, `content-visibility: auto`, `@media (prefers-reduced-motion: ...)`, and `@media (any-pointer: coarse)` ($\ge 48 \times 48\text{ px}$ with `gap >= 8px`, `touch-action: manipulation`).
