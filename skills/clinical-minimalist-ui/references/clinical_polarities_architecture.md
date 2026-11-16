# Clinical Polarities & Vector A4 Print Architecture — Clinical Minimalist UI

Detailed ergonomic and token specification consumed by [`../SKILL.md`](../SKILL.md), complementing [`clinical_a4_tokens_guide.md`](clinical_a4_tokens_guide.md) and `design-md`.

## 1. Clinical `OKLCH` Polarities, Zenithal Light & 4 Card Variants (Axes 3–5 & 7)

- **Outpatient Daytime & Print (`[data-theme="clinical-day"]`):** `--surface-canvas: oklch(0.97 0.005 245)`; `--surface-sunken: oklch(0.95 0.006 245)`; `--surface-card: oklch(1 0 0)`; `--ink-primary: oklch(0.18 0.02 255)` (WCAG AAA contrast $\ge 14:1$).
- **Night Shift / ICU / Diagnostics (`[data-theme="clinical-night"]`):** Progressive lightness $L$ elevation (zero pure black anti-OLED smearing): `--surface-canvas: oklch(0.16 0.015 255)`; `--surface-card: oklch(0.21 0.018 255)`; `--surface-elevated: oklch(0.26 0.02 255)`; `--ink-primary: oklch(0.96 0.005 245)`.
- **Zenithal Lighting & Sunken Recess (`[LOCK-02]`):** Top Catch-Light (`inset 0 1px 0 0`) + `--shadow-elevation-1..3` / `--shadow-layer-sm/md/lg`; vital-sign and prescription inputs styled with `--surface-sunken` + `--shadow-inset-sunken`.
- **Achromatic Accent, 4 Variants & Contained Semantics:** Achromatic primary CTA (`oklch(0.18 0.02 255)` / `oklch(0.97 0.005 245)`); *Elevated*, *Outlined*, *Filled/Subtle*, and *Interactive* cards; clinical alerts via `6px` micro-dot, `border-inline-start: 2px solid`, or translucent `color-mix(in oklab, ...)` badge keeping `--ink-primary` text.

## 2. Logical Box Model, GPU Sharpness, `tabular-nums` & Anti-Squish Shielding (Axes 1–2)

- Logical properties (`inline-size`, `padding-inline`, `margin-block`), `display: flow-root`, `gap`; `-webkit-font-smoothing: antialiased`, `text-rendering: optimizeLegibility`, `font-synthesis: none`, `max-inline-size: 65ch`; zero fractional `scale()` (use `translateY(-1px)` hover / `translateY(0)` active).
- **Zero Emojis:** Exclusively **Lucide** vector icons (`stroke-width: 1.75`) or monospace markers.
- **`tabular-nums` & Unbreakable Units:** `JetBrains Mono` / `IBM Plex Mono` with `tabular-nums` for vital signs, `SOFA`/`CHA2DS2-VASc`/`CKD-EPI`, SIGTAP/ICD-10 codes, and dosages; clinical units (`mg/dL`, `mL/min/1.73m²`, `mcg/kg/min`, `mEq/L`) guarded with `white-space: nowrap; flex-shrink: 0` and touch targets $\ge 44 \times 44\text{px}$.

## 3. Clinical Archetypes, `@container` & Vector A4 Sheet (Axes 6 & 8)

- *Workbench Split-View* or *Command Center* using `container-type: inline-size` + `@container`.
- 3-Layer Navigation: Global (`<nav aria-label="Primary clinical menu">`), Local (`Chart sections`), and Breadcrumbs (`>= 3` levels).
- **Vector A4 Print Sheet (`210mm × 297mm` `.sus-grid`):** 100% vector CSS Grid and SVG; on screen `--surface-canvas` + `--shadow-elevation-2`; inside `@media print` hide `.no-print`/`nav`/`aside` and strip all shadows.
