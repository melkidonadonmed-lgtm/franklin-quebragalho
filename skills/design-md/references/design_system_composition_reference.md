# Master Architecture Reference: 3-Layer Design System (`OKLCH`), Optical Physics & Complexity Tiers (`v8.2.0`)

This reference consolidates the **9 Axes + Decision Matrix** from the Single Source of Truth (`rules/frontend-9-axes-guidelines.md`) for direct consultation by `design-md`, `frontend-code-architect`, `frontend-ui-ux-auditor`, `frontend-testing-auditor`, and `system-project-auditor`.

---

## 1. Axes 1 & 2: Logical Box Model, Margin Collapse Prevention & Fluid Typography

```css
/* Base Reset with Predictable Box Model and Logical Properties */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  font-optical-sizing: auto;
  font-synthesis: none;
}

:root {
  /* Fluid Typographic Scale using clamp(min, preferred, max) */
  --step--1: clamp(0.8125rem, 0.78rem + 0.16vw, 0.9rem);
  --step-0:  clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --step-1:  clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --step-2:  clamp(1.5625rem, 1.4rem + 0.8vw, 2rem);
  --step-3:  clamp(1.953rem, 1.7rem + 1.25vw, 2.665rem);
}

/* Margin Collapse Prevention: Clean BFC and Lobotomized Owl */
.section-wrapper {
  display: flow-root;
}

.prose > * + * {
  margin-block-start: var(--flow-space, 1.25em);
}

h1, h2, h3, h4 {
  text-wrap: balance;
  line-height: 1.18;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

p, li {
  font-size: var(--step-0);
  line-height: 1.6;
  max-inline-size: 65ch;
  text-wrap: pretty;
  color: var(--text-secondary);
}

/* Mandatory Tabular Numeric Alignment */
.tabular-data, .tabular-metric, table td, input[type="number"], .metric-value {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}
```

---

## 2. Axes 3, 4 & 5: 3-Layer Tokens (`OKLCH`), `light-dark()`, `color-mix()`, RCS & Multi-Layer Shadows (`tokens.css`)

```css
:root {
  color-scheme: light dark;

  /* 1. PRIMITIVE TOKENS (Raw Palette & Rhythm Catalog) */
  --primitive-blue-500: oklch(0.62 0.21 258);
  --primitive-emerald-500: oklch(0.70 0.17 160);
  --primitive-neutral-50: oklch(0.985 0.004 255);
  --primitive-neutral-100: oklch(0.955 0.008 255);
  --primitive-neutral-800: oklch(0.22 0.025 260);
  --primitive-neutral-900: oklch(0.16 0.02 260);

  --space-0-5: 0.125rem; /* 2px */
  --space-1: 0.25rem;    /* 4px */
  --space-2: 0.5rem;     /* 8px */
  --space-3: 0.75rem;    /* 12px */
  --space-4: 1rem;       /* 16px */
  --space-6: 1.5rem;     /* 24px */
  --space-8: 2rem;       /* 32px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
  --space-inline-icon: var(--space-2);
  --space-card-gap: var(--space-3);
  --space-card-padding: clamp(1rem, 3cqi, 1.75rem);
  --space-grid-gap: clamp(1rem, 2.5vw, 1.5rem);
  --space-section-inset: clamp(1.5rem, 4vw, 3rem);
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-card: 1rem;
  --radius-full: 9999px;

  /* 2. SEMANTIC TOKENS (Reactive via light-dark, color-mix, and RCS from) */
  --brand-primary: var(--primitive-blue-500);
  --brand-accent: var(--primitive-emerald-500);

  --bg-canvas: light-dark(var(--primitive-neutral-50), var(--primitive-neutral-900));
  --bg-surface-1: light-dark(oklch(1 0 0), var(--primitive-neutral-800));
  --bg-surface-2: light-dark(
    var(--primitive-neutral-100),
    oklch(from var(--primitive-neutral-800) calc(l + 0.05) c h)
  );

  /* SSOT Compatibility Aliases (--surface-* and --ink-*) */
  --surface-canvas: var(--bg-canvas);
  --surface-sunken: var(--bg-surface-2);
  --surface-card: var(--bg-surface-1);
  --surface-elevated: var(--bg-surface-2);
  --surface-glass: oklch(from var(--bg-surface-1) l c h / 0.72);

  --text-primary: light-dark(
    color-mix(in oklab, var(--brand-primary) 15%, oklch(0.15 0.02 255)),
    oklch(0.96 0.01 255)
  );
  --text-secondary: light-dark(oklch(0.45 0.03 255), oklch(0.74 0.02 255));
  --text-muted: light-dark(oklch(0.52 0.02 255), oklch(0.66 0.02 255));
  --ink-primary: var(--text-primary);
  --ink-secondary: var(--text-secondary);
  --ink-muted: var(--text-muted);

  --border-subtle: light-dark(oklch(0.2 0.02 255 / 0.08), oklch(1 0 0 / 0.12));
  --catch-light: inset 0px 1px 0px 0px light-dark(oklch(1 0 0 / 0.85), oklch(1 0 0 / 0.12));

  /* Relative Color Syntax (RCS) State Derivation */
  --btn-hover: oklch(from var(--brand-primary) calc(l - 0.08) c h);
  --badge-bg: oklch(from var(--brand-primary) l c h / 0.12);

  /* LAYERED SHADOWS: Primitives (--shadow-layer-*) + Semantics (Umbra + Negative-Spread Penumbra + Catch-Light) */
  --shadow-layer-sm:
    0px 1px 2px 0px oklch(0.2 0.03 255 / 0.05),
    0px 2px 4px -1px oklch(0.2 0.03 255 / 0.04),
    var(--catch-light);
  --shadow-layer-md:
    0px 2px 4px -1px oklch(0.2 0.03 255 / 0.06),
    0px 6px 12px -2px oklch(0.2 0.03 255 / 0.08),
    0px 14px 24px -4px oklch(0.2 0.03 255 / 0.05),
    var(--catch-light);
  --shadow-layer-lg:
    0px 4px 8px -2px oklch(0.2 0.03 255 / 0.06),
    0px 16px 24px -4px oklch(0.2 0.03 255 / 0.10),
    0px 32px 48px -8px oklch(0.2 0.03 255 / 0.14),
    var(--catch-light);

  --shadow-elevation-1: var(--shadow-layer-sm);
  --shadow-elevation-2: var(--shadow-layer-md);
  --shadow-elevation-3: var(--shadow-layer-lg);
  --shadow-inset:
    inset 0px 2px 4px 0px light-dark(oklch(0.15 0.02 255 / 0.08), oklch(0 0 0 / 0.65)),
    inset 0px 0px 0px 1px light-dark(oklch(0.15 0.02 255 / 0.05), oklch(1 0 0 / 0.05));
  --elevation-pressed-inset:
    inset 0px 3px 6px -1px light-dark(oklch(0.15 0.02 255 / 0.16), oklch(0 0 0 / 0.55)),
    inset 0px 1px 2px 0px light-dark(oklch(0.15 0.02 255 / 0.22), oklch(0 0 0 / 0.70));

  /* Semantic Aliases & Tailwind CSS v4 (@theme) Compatibility */
  --elevation-flat: none;
  --elevation-1: var(--shadow-elevation-1);
  --elevation-2: var(--shadow-elevation-2);
  --elevation-3: var(--shadow-elevation-3);
  --elevation-low: var(--shadow-elevation-1);
  --elevation-medium: var(--shadow-elevation-2);
  --elevation-high: var(--shadow-elevation-3);
  --shadow-elevation-low: var(--shadow-elevation-1);
  --shadow-elevation-medium: var(--shadow-elevation-2);
  --shadow-elevation-high: var(--shadow-elevation-3);
  --shadow-inset-sunken: var(--shadow-inset);
  --sunken-recess: var(--shadow-inset);
  --shadow-clean-card: var(--shadow-elevation-2);

  --font-sans: 'Inter', 'Plus Jakarta Sans', 'Geist', 'IBM Plex Sans', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'IBM Plex Mono', 'Geist Mono', ui-monospace, monospace;
  --ease-out-natural: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-state-fast: cubic-bezier(0.4, 0, 0.2, 1);
}

@media (prefers-color-scheme: dark) {
  :root {
    --shadow-layer-sm:
      0px 1px 2px 0px oklch(0 0 0 / 0.45),
      0px 2px 4px -1px oklch(0 0 0 / 0.35),
      inset 0px 1px 0px 0px oklch(1 0 0 / 0.08);
    --shadow-layer-md:
      0px 2px 4px -1px oklch(0 0 0 / 0.50),
      0px 8px 20px -2px oklch(0 0 0 / 0.60),
      0px 0px 12px 0px oklch(from var(--brand-primary) l c h / 0.14),
      inset 0px 1px 0px 0px oklch(1 0 0 / 0.12);
    --shadow-layer-lg:
      0px 4px 8px -2px oklch(0 0 0 / 0.55),
      0px 20px 40px -6px oklch(0 0 0 / 0.75),
      0px 0px 24px 0px oklch(from var(--brand-primary) l c h / 0.24),
      inset 0px 1px 0px 0px oklch(1 0 0 / 0.16);
  }
}

[data-theme="light"] { color-scheme: light; }
[data-theme="dark"] {
  color-scheme: dark;
  --shadow-layer-sm:
    0px 1px 2px 0px oklch(0 0 0 / 0.45),
    0px 2px 4px -1px oklch(0 0 0 / 0.35),
    inset 0px 1px 0px 0px oklch(1 0 0 / 0.08);
  --shadow-layer-md:
    0px 2px 4px -1px oklch(0 0 0 / 0.50),
    0px 8px 20px -2px oklch(0 0 0 / 0.60),
    0px 0px 12px 0px oklch(from var(--brand-primary) l c h / 0.14),
    inset 0px 1px 0px 0px oklch(1 0 0 / 0.12);
  --shadow-layer-lg:
    0px 4px 8px -2px oklch(0 0 0 / 0.55),
    0px 20px 40px -6px oklch(0 0 0 / 0.75),
    0px 0px 24px 0px oklch(from var(--brand-primary) l c h / 0.24),
    inset 0px 1px 0px 0px oklch(1 0 0 / 0.16);
}
```

---

## 3. Axes 6, 7, 8 & 9: 6 Spatial Archetypes, `@container`, 4 Cards, 3-Layer Navigation & 3 Complexity Tiers

| Spatial Archetype | Domain / Problem Nature | Macro (`@media`) & Micro (`@container`) Composition |
| :--- | :--- | :--- |
| **1. Workbench Split-View** | Creation tools, editors, generators, simulators. | Parameter sidebar (`overflow-y: auto`) + live primary canvas. |
| **2. Asymmetric Bento Grid (12 col)** | Overviews, technical portfolios, executive summaries. | 12-column CSS Grid (`col-span-4`, `col-span-8`, `gap: var(--space-6)`); cards with `@container`. |
| **3. Command Center / Data Grid** | Analytics, FinTech, monitoring, incident triage. | `sticky` headers, `nowrap` rows with `tabular-nums`, `Cluster` toolbar, and Slide-over Drawer. |
| **4. Editorial & Reading Canvas** | Technical docs, interactive essays, reports. | Center column `max-inline-size: 65ch`, `.prose > * + *`, local Table of Contents, and Breadcrumbs. |
| **5. Spatial HUD with Floating Dock** | 3D viewers, maps, infinite whiteboards. | `100vw / 100vh` viewport, floating `--surface-glass` docks (`backdrop-filter: blur(16px)`) + `--shadow-elevation-3`. |
| **6. Vector A4 Print Sheet** | Formal document preview/export (`@media print`). | `210mm × 297mm` sheet in **100% vector CSS Grid & SVG** (zero heavy Base64 bitmaps). |

### Quick Quality Checklist (`Self-Refine`)

- [ ] **Logical Box Model & BFC:** Uses `inline-size`, `padding-inline`, `margin-block`, `display: flow-root`, and parent `gap`?
- [ ] **3-Layer OKLCH Tokens:** Primitives, Semantics (`light-dark()`, `color-mix()`, RCS `from`), and Component tokens defined with progressive Dark Mode $L$ elevation ($L = 0.16 \to 0.22 \to 0.27$)?
- [ ] **Shadows & GPU Sharpness:** Umbra + Penumbra + Catch-Light active, `antialiased` + `font-synthesis: none`, `text-wrap: balance/pretty`, `tabular-nums`, and zero fractional `scale()` on text?
- [ ] **Contextual Navigation & Real-State:** Global + Local (when applicable) + Breadcrumbs (`<ol role="list">` + `aria-current="page"` strictly in hierarchies $\ge 3$ levels), DOM Order = Visual Order, and 100% real functional controls?

---

## 4. Cross-References for Complex UIs, Real-Time Graphs & Next.js 15+ App Router

- **Macro-Micro, OKLCH & AOM Accessibility:** `rules/frontend-9-axes-guidelines.md`.
- **Interactive Graphs (`@xyflow/react`), Chokidar/WS & Next.js 15+ Async Params:** `skills/complex-zero/SKILL.md`.

---

## 5. Specialized Scope Addenda (`v8.2.0`)

### 5.1. Feature-Driven Folder Convention & Colocation (Next.js App Router & React)

- Group routes under `src/app/(dashboard)/` with private `_components/` folders for route-exclusive components without exposing them as public routes.
- Encapsulate business domains under `src/features/<domain>/{api,components,hooks,types}/` and atomic primitives under `src/components/{ui,feedback}/`.
- Enforce strict colocation (`Component.tsx`, `Component.module.css`, `Component.test.tsx`, `Component.types.ts`).

### 5.2. Addendum A — Infinite Canvas, Geometry & Visual Editors (`React Flow` / 1,000+ Nodes)

- **Background Dot Grid (`.canvasPattern`):** `background-image: radial-gradient(var(--border-subtle) 1px, transparent 1px); background-size: 24px 24px;`
- **Native Resizing (`.nodeResizable`):** `resize: both; overflow: auto; min-width: 200px; min-height: 120px; max-width: 600px; max-height: 500px;`
- **Reactive Signaling (`.nodeFlashing`):** `@keyframes flashYellow` from `oklch(0.85 0.18 85)` + `scale(1.12)` to `var(--bg-card)` + `scale(1)` over `1.5s cubic-bezier(0.4, 0, 0.2, 1) forwards`.
- **High Scale (1,000+ nodes):** `onlyRenderVisibleElements={true}`, off-main-thread Web Workers (Dagre/ELK), `React.memo`, **`150ms` event batching**, and **Zoom-Based Semantic LOD** ($< 0.4$ Macro vs. $\ge 0.4$ Micro).

### 5.3. Addenda B & C — Shadow Property Matrix, 4 Contextual Modes & Native `<dialog>` with `@starting-style`

| Property | DOM Target | `inset` / `spread`? | Canonical Usage |
| :--- | :--- | :--- | :--- |
| **`box-shadow`** | Rectangular box (`border-box`) | Yes / Yes | Cards, modals, sunken inputs (watch parent `overflow: hidden`). |
| **`text-shadow`** | Typographic glyphs | No / No | Heading legibility over gradients or photos without box wrappers. |
| **`filter: drop-shadow()`** | Alpha mask (true transparency) | No / No | Crisp contours on open SVGs, transparent PNGs, or `clip-path`. |

```css
/* Mode 1 & 4: Native <dialog> Glassmorphic Modal + Multi-Layered Shadows + @starting-style (Zero JS Animation) */
dialog::backdrop {
  background-color: oklch(0 0 0 / 0.55);
  backdrop-filter: blur(8px);
  opacity: 0;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), overlay 0.3s, display 0.3s;
  transition-behavior: allow-discrete;
}
dialog[open]::backdrop { opacity: 1; }
@starting-style { dialog[open]::backdrop { opacity: 0; } }

.glassModal {
  isolation: isolate;
  background: oklch(0.20 0.03 260 / 0.72);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid oklch(1 0 0 / 0.15);
  border-radius: 20px;
  box-shadow:
    0px 16px 32px -4px oklch(0 0 0 / 0.60),                        /* 1. Dark Umbra */
    0px 4px 12px 0px oklch(0 0 0 / 0.35),                          /* 2. Mid Penumbra */
    0px 0px 24px 0px oklch(from var(--brand-primary) l c h / 0.20),/* 3. Ambient Glow */
    inset 0px 1px 0px 0px oklch(1 0 0 / 0.25);                     /* 4. Specular Rim */
  opacity: 0;
  transform: scale(0.92) translateY(16px);
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), overlay 0.3s, display 0.3s;
  transition-behavior: allow-discrete;
}
.glassModal[open] { opacity: 1; transform: scale(1) translateY(0); }
@starting-style { .glassModal[open] { opacity: 0; transform: scale(0.92) translateY(16px); } }
```

### 5.4. Addendum D — CSS Scroll Snap Sliders & Accessible `TabControl`

- **Zero-JS Carousel (`.sliderGrid`):** `display: grid; grid-auto-flow: column; grid-auto-columns: clamp(260px, 40vw, 360px); overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: thin;` with `.sliderCard { scroll-snap-align: start; }`.
- **Horizontally Overflowing Tabs (`.tabsOverflowContainer`):** `role="tablist"` with `display: flex; overflow-x: auto; white-space: nowrap;` and `role="tab"` buttons carrying `aria-selected="true|false"` and `aria-controls`.

### 5.5. Addenda E, F, G, H & I — Modern Selectors, Subgrid, Trigonometry, Forms & Agentic UI

- **Modern Selectors:** `:has()` (relational parent styling), `:is()` / `:not()` (grouping and exclusion), `:focus-visible` (keyboard focus ring), `::before` / `::after` (silent separators), `::selection`.
- **CSS Subgrid (`.bentoCardSubgrid`):** `grid-row: span 3; display: grid; grid-template-rows: subgrid;` to align headers, bodies, and footers across adjacent columns.
- **Native Trigonometry (`sin()`, `cos()`):** Radial/circular positioning without JS via `translate(calc(cos(var(--angle)) * var(--orbit-radius)), calc(sin(var(--angle)) * var(--orbit-radius)))`.
- **Modern Forms (`:user-invalid` / `:user-valid`):** Deferred validation (fires only after user interaction, never on initial load), paired with `<dialog>`, `popover="auto"`, `<details name="...">`, and `inert`.
- **Agentic Systems (AI/LLM UI):** `<details class="reasoningAccordion">` for Chain-of-Thought, *Scroll Lock Override* during streaming, Tool-Call cards with `tabular-nums`, and HITL gates (`approval_token` + `idempotency_key`).
