# UX/UI Spacing Engineering, Semantic Tokens (Google Stitch & Tailwind v4), Visual Hierarchy & OKLCH Color Matrix

> **Tier-3 Canonical Reference (`design-md`)** — Synthesizes `html-spacing`, `color-quality-matrix`, `OKLCH` tokens, `fluid-scaling`, `design-token-reactivity`, **Google Stitch (`DESIGN.md`)**, and **Tailwind CSS v4 (`@theme`)**.

---

## 1. Box Model Foundations & International Logical Properties

### 1.1. Predictable Sizing (`box-sizing: border-box`)

By default, browsers use `box-sizing: content-box`, adding `padding` and `border` onto declared dimensions and causing unexpected layout overflow. Every `DESIGN.md` contract mandates the universal reset inside `@layer base`:

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

### 1.2. Logical Spacing Properties (LTR / RTL Ready)

Physical directional properties (`left`, `right`, `top`, `bottom`, `width`, `height`) are forbidden in reusable components. Use logical properties anchored to the *inline* (reading flow) and *block* (stacking flow) axes:

| Legacy Physical Property (Forbidden) | Canonical Logical Property (`DESIGN.md`) | Spatial Role |
| :--- | :--- | :--- |
| `padding-left` + `padding-right` | `padding-inline` (`start` / `end`) | Internal horizontal isolation |
| `padding-top` + `padding-bottom` | `padding-block` (`start` / `end`) | Internal vertical isolation |
| `margin-left` + `margin-right` | `margin-inline` (`auto` to center) | External horizontal buffering |
| `margin-top` + `margin-bottom` | `margin-block` (`start` / `end`) | External vertical buffering |
| `width` / `height` | `inline-size` / `block-size` | Intrinsic flow-axis dimensions |
| `min-width` / `max-width` | `min-inline-size` / `max-inline-size` | Reading (`60ch`) and touch (`48px`) bounds |
| `border-left` / `border-bottom` | `border-inline-start` / `border-block-end` | Active indicators on sidebars and tabs |

---

## 2. Spacing Token Architecture: `4px/8px` Primitives + Semantic Intent (Google Stitch)

To prevent UI agents and LLMs from inventing arbitrary pixel numbers (`13px`, `27px`), `DESIGN.md` must declare **two spacing token layers**:
1. **Primitive Scale (`4px/8px` Grid):** Mathematical baseline rhythm.
2. **Semantic Intent Tokens (`--space-*`):** Express the **Gestalt Law of Proximity** ($\text{Inner Item Gap} < \text{Card Padding} \le \text{Grid Gap} < \text{Section Inset}$).

### 2.1. Canonical CSS Declaration & Zero-JS Density Reactivity (`design-token-reactivity`)

```css
:root {
  /* 1. PRIMITIVE SPACING SCALE (8px Grid with 4px Sub-multiples) */
  --space-0-5: 0.125rem; /* 2px  - Optical micro-adjustment / hairline */
  --space-1:   0.25rem;  /* 4px  - Gap between badge and icon */
  --space-2:   0.5rem;   /* 8px  - Standard icon-text / dense control gap */
  --space-3:   0.75rem;  /* 12px - Internal gap between card regions */
  --space-4:   1rem;     /* 16px - Compact card padding / list item gap */
  --space-6:   1.5rem;   /* 24px - Standard spacious card padding / Grid gap */
  --space-8:   2rem;     /* 32px - Subsection separation */
  --space-12:  3rem;     /* 48px - Major page-block separation */
  --space-16:  4rem;     /* 64px - Hero / Macro section vertical inset */

  /* 2. SEMANTIC INTENT TOKENS (Google Stitch & Autonomous Components) */
  --space-inline-icon:       var(--space-2);                      /* 8px */
  --space-component-padding: var(--space-3) var(--space-4);       /* 12px 16px */
  --space-card-gap:          var(--space-3);                      /* 12px (inside card) */
  --space-card-padding:      clamp(1rem, 3cqi, 1.75rem);          /* 16px -> 28px via @container */
  --space-grid-gap:          clamp(1rem, 2.5vw, 1.5rem);          /* 16px -> 24px between cards */
  --space-section-inset:     clamp(1.5rem, 4vw, 3rem);            /* 24px -> 48px between sections */
  --space-flow:              1.25em;                              /* Prose rhythm (.prose > * + *) */

  /* 3. BORDER & CONCENTRIC RADII */
  --radius-sm:   0.375rem; /* 6px */
  --radius-md:   0.5rem;   /* 8px */
  --radius-lg:   0.75rem;  /* 12px */
  --radius-card: 1rem;     /* 16px */
}

/* Zero-JS Density Reactivity (zero specificity via :where) */
:where([data-density="compact"]) {
  --space-card-gap:     var(--space-2);
  --space-card-padding: clamp(0.75rem, 2cqi, 1.125rem);
  --space-grid-gap:     var(--space-3);
}

:where([data-density="spacious"]) {
  --space-card-gap:     var(--space-4);
  --space-card-padding: clamp(1.25rem, 4cqi, 2.25rem);
  --space-grid-gap:     var(--space-6);
}
```

### 2.2. The Spacing Triad (`Padding` vs. `Margin` vs. `Gap`) & Margin Collapse

- **`padding` (Internal Isolation):** Applies breathing room inside the border and **expands the hit/touch area** of buttons and links.
- **`gap` (Inter-Element Spacing):** Primary spacing mechanism in **Flexbox** and **CSS Grid** (`row-gap` / `column-gap`), setting exact sibling spacing without leaking margins onto outer edges.
- **`margin` (External Buffering) & Margin Collapse ($M_{\text{res}} = \max(M_1, M_2)$):**
  - In normal block flow, adjacent vertical margins collapse to the larger value.
  - **Where collapse does NOT occur:** (1) Horizontal (`inline`) axis, (2) **Flexbox** or **CSS Grid** children, (3) Containers with `padding` or `border`, and (4) Containers establishing a **Block Formatting Context (BFC)** via `display: flow-root`.
  - **Mandatory Anti-Leak Patterns:**
    ```css
    /* Isolates internal margins without overflow: hidden (which would clip box-shadow) */
    .section-container {
      display: flow-root;
    }

    /* Lobotomized Owl: uniform vertical rhythm in prose/articles */
    .prose > * + * {
      margin-block-start: var(--space-flow, 1.25em);
    }
    ```

### 2.3. Optical Geometry of Concentric Radii in Cards

When an inner element (cover image, `.metric-item`, or full-width button) is nested inside a rounded card with padding $P$, reusing the identical `border-radius` causes optical corner dissonance. Compute the inner radius via:
$$R_{\text{inner}} = \max(4\text{px}, R_{\text{outer}} - P_{\text{padding}})$$
- **Canonical Example:** If `.card` has `--radius-card: 16px` and `padding: 6px` on its media wrapper, `.card-media` uses `border-radius: calc(var(--radius-card) - 6px)` (`10px`).

---

## 3. Tailwind CSS v4 (`@theme`) vs. Style Dictionary

### 3.1. CSS-First Configuration in Tailwind CSS v4 (`app.css`)

Tailwind CSS v4 replaces `tailwind.config.js` with `@import "tailwindcss";` paired with `@theme`:

```css
@import "tailwindcss";

@theme {
  /* Semantic OKLCH colors mapped to bg-app, bg-surface, bg-card, text-primary utilities */
  --color-app:           var(--bg-app);
  --color-surface:       var(--bg-surface);
  --color-card:          var(--bg-card);
  --color-text-primary:  var(--text-primary);
  --color-text-muted:    var(--text-secondary);
  --color-brand:         var(--brand-primary);

  /* Layered shadows mapped to shadow-elevation-low / medium / high */
  --shadow-elevation-low:    var(--elevation-low);
  --shadow-elevation-medium: var(--elevation-medium);
  --shadow-elevation-high:   var(--elevation-high);

  /* Semantic radii and spacing */
  --radius-card: 1rem;
  --radius-inner: calc(var(--radius-card) - 0.375rem);
}
```

### 3.2. Decision Matrix: Tailwind v4 (`@theme`) vs. Style Dictionary (`tokens.json`)

| Criterion | Tailwind CSS v4 (`@theme`) | Style Dictionary (Cross-Platform JSON) |
| :--- | :--- | :--- |
| **Project Scope** | React 19 / Next.js 15 web apps prioritizing velocity and native CSS. | Multi-platform Design Systems shared across **Web, Android (Kotlin/Compose), and iOS**. |
| **Source of Truth** | Directly in global CSS (`tokens.css` / `app.css`) with OKLCH variables. | Platform-neutral `tokens.json` synced with Figma (Tokens Studio). |
| **Build Pipeline** | Zero extra token compilation step. | Compiles `variables.css`, `tokens.ts`, and XML/Kotlin via `npx style-dictionary build`. |

---

## 4. The 4 Pillars of Visual Hierarchy & Fluid Typography (`clamp()`)

1. **Pillar 1 — Fluid Scaling (`clamp()`) with WCAG 1.4.4 Compliance (200% Zoom):**
   - Never use raw `vw` or `cqi` alone in `font-size` (breaks browser text zoom). Always sum a `rem` base (`1rem + 2cqi`) and ensure the maximum is **$\le 2.5\times$ the minimum**:
     ```css
     h1 {
       font-size: clamp(1.75rem, 1.2rem + 2.5vw, 3rem); /* 28px -> 48px (ratio 1.71x <= 2.5x) */
       line-height: 1.15;
       letter-spacing: -0.02em;
       text-wrap: balance;
     }
     h2, .card-title {
       font-size: clamp(1.125rem, 0.95rem + 1.5cqi, 1.5rem);
       line-height: 1.22;
       letter-spacing: -0.015em;
       text-wrap: balance;
     }
     p, .card-text {
       font-size: clamp(0.9375rem, 0.88rem + 0.5cqi, 1.0625rem);
       line-height: 1.55;
       max-inline-size: 60ch; /* Ergonomic 45-75 character line measure */
       text-wrap: pretty;
     }
     .metric-value, td[data-numeric="true"] {
       font-variant-numeric: tabular-nums; /* Exact vertical digit alignment */
     }
     ```
2. **Pillar 2 — `60-30-10` Chromatic Ratio in Perceptual `OKLCH`:**
   - **60% Dominant Surface (`--bg-app`):** Desaturated neutral canvas (`oklch(0.98 0.005 250)` in Light; `oklch(0.14 0.02 260)` or `0.16` in Dark — **pure `#000000` forbidden**).
   - **30% Structural Surface (`--bg-surface` / `--bg-card`):** Panels, sidebars, and cards (`oklch(0.18 0.02 260)` to `oklch(0.22 0.03 260)` in Dark Mode, signaling $Z$-elevation via lightness $L$).
   - **10% Focal Accent (`--brand-primary`):** Reserved strictly for primary CTAs, active navigation markers (`aria-current="page"`), and `:focus-visible` rings.
3. **Pillar 3 — Dynamic Color Derivation (RCS + `color-mix(in oklab)` + `light-dark()`):**
   - Derive `:hover`, `:active`, and translucent surface states mathematically from `--brand-primary`:
     ```css
     :root {
       color-scheme: light dark;
       --brand-primary: oklch(0.62 0.22 255);
       --btn-primary-hover:  oklch(from var(--brand-primary) calc(l - 0.08) c h);
       --btn-primary-active: oklch(from var(--brand-primary) calc(l - 0.14) c h);
       --badge-bg:           color-mix(in oklab, var(--brand-primary) 15%, transparent);
       --border-subtle:      light-dark(oklch(0.20 0.02 255 / 0.08), oklch(1.0 0 0 / 0.12));
       --text-primary:       light-dark(oklch(0.18 0.02 255), oklch(0.96 0.01 250)); /* Avoids pure #FFF */
     }
     ```
4. **Pillar 4 — SVG Color Matrices (`feColorMatrix` $5\times 4$) & `oklch` Gradients:**
   - Always interpolate gradients with `linear-gradient(in oklch, var(--brand-primary), var(--brand-accent))` to eliminate sRGB muddy gray midpoints.
   - Use isolated hidden SVG `<feColorMatrix type="matrix">` filters for duotone visual effects and Protanopia/Deuteranopia color-vision verification without duplicating raster assets.
