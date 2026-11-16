# Technical Reference: Zenithal Optical Elevation (`90°–120°`), 3-Layer Shadows (`OKLCH`) & Tailwind CSS v4 (`@theme`)

This reference replaces legacy `#HEX`/`rgba()` declarations and `tailwind.config.js` (v3) configurations with the modern **CSS `OKLCH` + `light-dark()` + Tailwind v4 CSS-First (`@theme`)** standard.

---

## 1. Zenithal Light Optical Model (`90°–120°`) & 3 Real Shadow Layers (`[LOCK-02]`)

1. **Contact Umbra:** Short vertical offset (`1px`–`4px`) and tight blur (`2px`–`8px`), anchoring the surface to the underlying plane.
2. **Diffuse Penumbra with Negative `spread` (`-1px` to `-8px`):** Contracts the perimeter prior to diffusion, concentrating gravitational weight beneath the base without muddying lateral edges.
3. **Zenithal Specular Rim (`--catch-light`):** Top internal highlight (`inset 0 1px 0 0`) simulating overhead light incident at `90°–120°`.
4. **Tactile Feedback without GPU Blur:** Rest (`--shadow-elevation-1`) $\to$ Hover (`translateY(-2px)` + `--shadow-elevation-2`) $\to$ Active (`translateY(0px)` + `--shadow-inset` or Level 1 return; **fractional `scale()` on text forbidden**).

---

## 2. Semantic Tokens `OKLCH` + `light-dark()` + Tailwind CSS v4 (`@theme`)

```css
@import "tailwindcss";

:root {
  color-scheme: light dark;

  --brand-primary: oklch(0.62 0.21 258);
  --surface-canvas: light-dark(oklch(0.985 0.004 255), oklch(0.16 0.02 260));
  --surface-sunken: light-dark(oklch(0.955 0.008 255), oklch(0.13 0.02 260));
  --surface-card: light-dark(oklch(1 0 0), oklch(0.22 0.025 260));
  --surface-elevated: light-dark(oklch(1 0 0), oklch(0.27 0.025 260));

  --text-primary: light-dark(oklch(0.18 0.02 255), oklch(0.96 0.01 255));
  --text-secondary: light-dark(oklch(0.45 0.03 255), oklch(0.74 0.02 255));
  --border-subtle: light-dark(oklch(0.20 0.02 255 / 0.08), oklch(1 0 0 / 0.12));
  --catch-light: inset 0 1px 0 0 light-dark(oklch(1 0 0 / 0.85), oklch(1 0 0 / 0.12));

  /* 3-Layer Optical Shadow Primitives & Semantics (Umbra + Negative-Spread Penumbra + Catch-Light) */
  --shadow-layer-sm:
    0 1px 2px 0 light-dark(oklch(0.20 0.03 255 / 0.06), oklch(0 0 0 / 0.45)),
    0 2px 4px -1px light-dark(oklch(0.20 0.03 255 / 0.04), oklch(0 0 0 / 0.35)),
    var(--catch-light);
  --shadow-layer-md:
    0 2px 4px -1px light-dark(oklch(0.20 0.03 255 / 0.06), oklch(0 0 0 / 0.50)),
    0 8px 20px -2px light-dark(oklch(0.20 0.03 255 / 0.09), oklch(0 0 0 / 0.60)),
    0 0 12px 0 light-dark(transparent, oklch(from var(--brand-primary) l c h / 0.14)),
    var(--catch-light);
  --shadow-layer-lg:
    0 4px 8px -2px light-dark(oklch(0.20 0.03 255 / 0.07), oklch(0 0 0 / 0.55)),
    0 20px 40px -6px light-dark(oklch(0.20 0.03 255 / 0.14), oklch(0 0 0 / 0.75)),
    0 0 24px 0 light-dark(transparent, oklch(from var(--brand-primary) l c h / 0.24)),
    var(--catch-light);

  --shadow-elevation-1: var(--shadow-layer-sm);
  --shadow-elevation-2: var(--shadow-layer-md);
  --shadow-elevation-3: var(--shadow-layer-lg);
  --shadow-inset:
    inset 0 2px 4px 0 light-dark(oklch(0.15 0.02 255 / 0.08), oklch(0 0 0 / 0.65)),
    inset 0 0 0 1px light-dark(oklch(0.15 0.02 255 / 0.05), oklch(1 0 0 / 0.06));
  --elevation-pressed-inset:
    inset 0 3px 6px -1px light-dark(oklch(0.15 0.02 255 / 0.16), oklch(0 0 0 / 0.55)),
    inset 0 1px 2px 0 light-dark(oklch(0.15 0.02 255 / 0.22), oklch(0 0 0 / 0.70));

  --elevation-flat: none;
  --elevation-1: var(--shadow-elevation-1);
  --elevation-2: var(--shadow-elevation-2);
  --elevation-3: var(--shadow-elevation-3);
  --elevation-low: var(--shadow-elevation-1);
  --elevation-medium: var(--shadow-elevation-2);
  --elevation-high: var(--shadow-elevation-3);
  --shadow-inset-sunken: var(--shadow-inset);
  --shadow-clean-card: var(--shadow-elevation-2);
}

@variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));

@theme inline {
  --color-canvas: var(--surface-canvas);
  --color-sunken: var(--surface-sunken);
  --color-card: var(--surface-card);
  --color-elevated: var(--surface-elevated);
  --color-primary: var(--brand-primary);
  --shadow-elevation-1: var(--shadow-layer-sm);
  --shadow-elevation-2: var(--shadow-layer-md);
  --shadow-elevation-3: var(--shadow-layer-lg);
  --shadow-elevation-low: var(--shadow-elevation-1);
  --shadow-elevation-medium: var(--shadow-elevation-2);
  --shadow-elevation-high: var(--shadow-elevation-3);
  --shadow-inset-sunken: var(--shadow-inset);
  --shadow-tactile-sm: var(--shadow-elevation-1);
  --shadow-tactile-md: var(--shadow-elevation-2);
  --shadow-tactile-lg: var(--shadow-elevation-3);
  --shadow-tactile-inset: var(--shadow-inset);
  --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);
}
```

---

## 3. Diagnostic Layer Table (Auditor Checklist)

| Layer / Rule | Expected Signature | Common Failure (`[FAIL]`) |
| :--- | :--- | :--- |
| **Umbra + Penumbra** | 2+ `box-shadow` layers with negative `spread` (`-1px`..`-8px`) | Flat single blurred shadow (`0 4px 12px rgba(0,0,0,0.4)`) |
| **Zenithal Light (`90°–120°`)** | `inset 0 1px 0 0` (`--catch-light` / `--specular-rim`) | Flat surface lacking separation in Dark Mode |
| **Dark Mode Elevation** | Progressive `OKLCH` lightness ($L = 0.16 \to 0.22 \to 0.27$) | Pure `#000000` background or invisible black shadow |
| **Motor Response** | `transform: translateY(-1px/-2px)` + `:focus-visible` + `prefers-reduced-motion` | Animating `width`/`height`/`margin` (reflow) or `scale(0.97)` on text |
| **Spacing & Proximity** | `4px/8px` scale (`--space-*`) + Semantics (`--space-card-padding`, `--space-grid-gap`) + Concentric Radii ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$) | Magic values (`13px`), inner padding larger than outer gap, or margin collapse without `display: flow-root` |
| **Flexbox, Grid & Cards** | Macrolayout Grid `RAM` (`minmax(min(100%, 280px), 1fr)`) + Microlayout `@container` + 4-region `subgrid` + `flex-wrap: balance` + `safe center` | Card querying `@media`, ghost media column without `:has(> img)`, or `container-type` on the `subgrid` node |
| **Hierarchy & Typography** | `clamp()` with $\max \le 2.5\times \min$ + `max-inline-size: 60ch` + `tabular-nums` + `text-wrap: balance/pretty` | Pure `vw` `font-size` (breaks 200% zoom), lines `> 80ch`, or jittering numbers without `tabular-nums` |
| **Navigation & Fluidity** | Single DOM Bottom Nav (`env(safe-area-inset-bottom)`) $\leftrightarrow$ Sidebar Rail (`240px`, `100dvh`) + `aria-current="page"` ($\ge 3:1$) + `any-pointer: coarse` (`48x48px`) + `content-visibility: auto` | Duplicated mobile/desktop HTML, `transition: ... allow-discrete` in shorthand, or touch targets `< 48px` |
