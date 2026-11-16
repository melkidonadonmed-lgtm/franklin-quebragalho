# The 5 Pillars of Design Principles & Optical Physics (`design-md`)

Technical reference supporting [`../SKILL.md`](../SKILL.md). See also [`design_system_composition_reference.md`](design_system_composition_reference.md) and [`spacing_tokens_and_stitch_hierarchy.md`](spacing_tokens_and_stitch_hierarchy.md).

## Pillar 1 — Visual Philosophy & Contextual Identity

- Justify hue ($H$), chroma ($C$), typography, and density directly from the product domain (rejecting generic off-the-shelf palettes).
- **Functional Hero:** Open immediately with the core value element (live dashboard, search control, or key indicator), avoiding empty decorative banners.
- Borders (`1px solid var(--border-subtle)`), spacing rhythm, and `tabular-nums` encode informational hierarchy without visual clutter.

## Pillar 2 — Decoupled Spatial Architecture

- **Macrolayouts (`@media`):** CSS Grid (`repeat(auto-fit, minmax(min(100%, 280px), 1fr))`), `100dvh`; select **strictly the matching Spatial Archetype** (*Split-View*, *12-Col Bento Grid*, *Command Center*, *Editorial 65ch*, *Spatial HUD*, or *Vector A4 Print Sheet `@media print`*).
- **Microlayouts (`@container`, Flexbox & `subgrid`):** Flexbox (`flex-wrap: balance`, `align-items: safe center`, `min-inline-size: 0` without mixing `width` and `flex-basis`), `container-type: inline-size` separated from the `subgrid` node (4 regions inside `<article>`, `.card:has(> img)`), primitive `--space-*` + semantic tokens (`--space-inline-icon`, `--space-card-gap`, `--space-card-padding: clamp(1rem, 3cqi, 1.75rem)`, `--space-grid-gap`, `--space-section-inset`), Gestalt Proximity ($\text{Inner Gap} < \text{Card Padding} \le \text{Grid Gap} < \text{Section Inset}$), `display: flow-root`, `.prose > * + *`, and Concentric Radii ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$).
- **Typography & GPU Sharpness:** `clamp()` ($\max \le 2.5\times \min$, combining `rem` + `vw`/`cqi` for WCAG 1.4.4 zoom up to 200%), `60ch–65ch`, `text-wrap: balance` (headings `1.15–1.25`), `text-wrap: pretty` (paragraphs `1.5–1.65`), `tabular-nums`, `-webkit-font-smoothing: antialiased`, and `font-synthesis: none`.

## Pillar 3 — `OKLCH` Colors (`60-30-10`) & $L$ Elevation

- **60% Dominant (`--bg-app`/`--surface-canvas`)**, **30% Secondary (`--bg-surface`/`--bg-card`)**, **10% Accent (`--brand-primary`)**.
- **Dark Mode:** Elevate lightness $L$ progressively (`0.14` Canvas -> `0.18` Surface -> `0.22` Card -> `0.26` Modal; or `0.16 -> 0.22 -> 0.27` SSOT baseline) + specular hairline `oklch(1 0 0 / 0.12)`.
- **Derivations:** `light-dark()`, `color-mix(in oklab, ...)`, and RCS `oklch(from var(--brand-primary) calc(l - 0.08) c h)`.

## Pillar 4 — Optical Physics of Multi-Layer Shadows (`[LOCK-02]`)

$$\texttt{box-shadow: } \underbrace{\Delta x \ \Delta y \ R_{\text{blur}} \ R_{\text{spread}} \ \text{color}}_{\text{1. Contact Umbra}}, \ \underbrace{\Delta x \ \Delta y \ R_{\text{blur}} \ R_{\text{spread}} \ \text{color}}_{\text{2. Penumbra (Negative Spread } -1\text{px to }-8\text{px)}}, \ \underbrace{\texttt{inset } 0\text{px } 1\text{px } 0\text{px } 0\text{px } \text{color}}_{\text{3. Zenithal Catch-Light}}$$

- In Tailwind CSS v4 `@theme`, expose `--shadow-elevation-*` alongside `@variant dark`.
- **`box-shadow`** (DOM boxes) vs. **`text-shadow`** (glyphs/serifs over media) vs. **`filter: drop-shadow()`** (SVGs/PNGs/alpha cutouts).
- **4 Contextual Modes (apply only when pertinent):** *Glassmorphism* (`isolation: isolate`, `backdrop-filter: blur(16..20px) saturate(180%)`), *Tactile Inset* (outset + `--shadow-inset` / `--elevation-pressed-inset`), *Dark Glow* (`0 0 12..24px oklch(... / 0.14..0.24)`), and *Native `<dialog>` + `@starting-style`* (`allow-discrete`).

## Pillar 5 — Interactivity, AOM & `@layer`

- DOM Order = Visual Order; `:focus-visible`; `:user-invalid`/`:user-valid`; native `<dialog>`, `popover="auto"`, `<details>`; Fitts' Law `@media (any-pointer: coarse)` (`>= 48x48px`, `gap >= 8px`); `@media (prefers-reduced-motion: reduce)`; `@layer reset, tokens, base, layouts, components, utilities;` (zero `!important`).
