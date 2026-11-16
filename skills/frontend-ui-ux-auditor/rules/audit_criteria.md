# Deterministic Audit Criteria — `frontend-ui-ux-auditor` (`v3.1.0`)

Objective rules governing the static engine `scripts/ui_ux_frontend_auditor.py` aligned with the **9-Axis SSOT** (`rules/frontend-9-axes-guidelines.md`).

---

## 1. Approval and Failure Rules (`[PASS]` / `[FAIL]`)

### `UIUX-TOKENS-01` — 3-Layer Design Tokens (`OKLCH`) & Base-4 / Base-8 Scale (`W = 0.20`)

- **`[PASS]`**: Spacing (`padding`, `margin`, `gap`) adheres to the `4px/8px` progression (`4, 8, 12, 16, 24, 32, 48, 64px`), uses semantic CSS custom properties (`var(--*)`, `oklch()`, `light-dark()`, `color-mix()`), and eliminates off-scale arbitrary values (`p-[13px]`, `margin: 11px`).
- **`[FAIL]`**: Arbitrary values outside the 8px scale or absence of semantic Design Token variables.

### `UIUX-TYPO-WCAG-02` — Anti-GPU-Blur Fluid Typography & WCAG 2.1 AA Contrast (`W = 0.20`)

- **`[PASS]`**: Includes `<meta name="viewport">`, subpixel smoothing (`-webkit-font-smoothing: antialiased` / `optimizeLegibility` / `font-synthesis: none`), fluid `clamp()`, `max-inline-size: 65ch`, `text-wrap: balance/pretty`, body copy $\ge 12\text{px}$, zero fractional `scale()` on text containers, and WCAG 2.1 AA contrast ratio $CR \ge 4.5:1$ for normal text ($CR \ge 3.0:1$ for large text/UI).
- **`[FAIL]`**: Contrast below $4.5:1$, missing viewport meta tag, body font `< 12px`, or missing subpixel smoothing.

### `UIUX-DOM-03` — Logical Box Model, Semantic Structure, Divsoup Ratio & 3-Layer Navigation (`W = 0.15`)

- **`[PASS]`**: Uses `box-sizing: border-box`, logical properties (`inline-size`, `padding-inline`, `margin-block`), BFC containment (`display: flow-root` / `gap`); max DOM depth $\le 12$ levels, `divsoup_ratio <= 0.45`, HTML5 semantic landmarks (`main`, `header`, `nav`, `section`, `aside`, `article`), `:focus-visible`, `aria-current="page"` (Breadcrumbs `<ol role="list">`), and DOM Order = Visual Order (zero `row-reverse` breaking `Tab`).
- **`[FAIL]`**: DOM depth `> 12`, `divsoup_ratio > 0.45`, `row-reverse` in navigation, or missing semantic landmarks and keyboard focus ring.

### `UIUX-ICON-04` — 1:1 Vector Iconography & Zero Emojis (`W = 0.15`)

- **`[PASS]`**: SVG icons or vector utility classes maintain a 1:1 square aspect ratio (`16px`, `20px`, or `24px` / `w-4 h-4`, `w-5 h-5`, `w-6 h-6`), uniform `stroke-width`, and zero UI emojis.
- **`[FAIL]`**: Asymmetric icons (`width != height`) or non-standard geometric bounding boxes.

### `UIUX-LIGHT-05` — `[LOCK-02]` Zenithal Light (`90°–120°`), 3-Level Shadows & Blend Isolation (`W = 0.15`)

- **`[PASS]`**: Declares top specular rim (`inset 0 1px 0 0` / `--catch-light` / `--specular-rim`) paired with multi-layer elevation shadows (Contact Umbra + negative-spread Penumbra across Levels 1–3 via `--shadow-elevation-1/2/3`, `--elevation-1/2/3`, `--elevation-low/medium/high`, or `tactile-*`), `isolation: isolate` for blend modes, and physical `:hover`/`:active` feedback.
- **`[FAIL]`**: Flat single-pass shadow (`0 4px 12px rgba(0,0,0,0.4)`) or absence of multi-layer elevation and zenith lighting cues.

### `UIUX-MOTION-06` — Macro/Microlayout (`@container`), Zero-Reflow GPU Motion & Motor Accessibility (`W = 0.15`)

- **`[PASS]`**: Animates strictly `transform`, `box-shadow`, `background-color`, `border-color`, and `opacity` with natural deceleration (`cubic-bezier(0.22, 1, 0.36, 1)`), supports `@container` / Grid RAM, `@media (pointer: coarse)` ($\ge 44\text{px}$ / $\ge 48\text{px}$), and explicit `@media (prefers-reduced-motion: reduce)` or `motion-reduce:transition-none`.
- **`[FAIL]`**: Transitions on layout-thrashing properties (`width`, `height`, `margin`, `padding`, `top`, `left`) or missing reduced-motion support.
