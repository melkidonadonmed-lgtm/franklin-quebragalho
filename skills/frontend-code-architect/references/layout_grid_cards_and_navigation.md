# Layout Architecture (Flexbox vs. Grid vs. Subgrid), Dynamic Cards, Adaptive Navigation & Fluidity (React 19 / Next.js 15 / Tailwind v4)

> **Tier-3 Canonical Reference (`frontend-code-architect`)** — Synthesizes `css-layout`, `card`, `navbar`, `motion`, `interactions-in-complex-layouts`, `fluid-scaling`, and `design-token-reactivity`.

---

## 1. Spatial Decision Tree: Macrolayout (Grid) vs. Microlayout (`@container` + Flex/Subgrid)

### 1.1. Macrolayouts (Global Page Shell)

- **Mechanism:** **CSS Grid** paired with **Media Queries (`@media`)** and dynamic viewport units (`100dvh`).
- **Responsibility:** Coordinate the global shell (`header`, `aside` / `240px` navigation rail, `<main>`, and inspector pane).
- **RAM Pattern (Repeat, Auto, Minmax) without Horizontal Overflow:**
  ```css
  .macro-card-grid {
    display: grid;
    /* min(100%, 280px) prevents horizontal scrollbars on viewports narrower than 280px */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
    gap: var(--space-grid-gap, clamp(1rem, 2.5vw, 1.5rem));
  }
  ```

### 1.2. Microlayouts (Viewport-Independent Autonomous Components)

- **Mechanism:** **Container Queries (`container-type: inline-size`)** + `cqi`/`cqw` units.
- **Golden Rule:** A reusable component (Card, Widget, Toolbar) **never queries `@media`** to reorganize its internal columns; it adapts to the actual width of its own container (`@container card (min-width: 340px)`).

### 1.3. Critical Flexbox (1D) vs. CSS Grid (2D) Rules

| Scenario | Correct Mechanism | Mandatory Technical Rules |
| :--- | :--- | :--- |
| **Row of tags, pills, filters, or buttons** | **Flexbox (1D)** | Use `display: flex; flex-wrap: wrap; flex-wrap: balance; gap: var(--space-2);` (prevents single-item orphan lines). |
| **Toolbar or modal centering** | **Flexbox / Grid** | Use `align-items: safe center; justify-content: safe center;` (prevents top/start clipping of focusable controls on narrow viewports). |
| **Flex/Grid children with long or truncated text** | **Flexbox / Grid** | Declare `min-inline-size: 0` on the child (default `min-inline-size: auto` blocks `text-overflow: ellipsis` and overflows the container). |
| **Intrinsic Flex sizing** | **Flexbox (1D)** | Use shorthand `flex: 1 1 250px`. **Forbidden** to declare `width` or `inline-size` alongside `flex-basis`. |
| **Vertical alignment across sibling Cards** | **CSS Grid + `subgrid`** | Use `grid-row: span 4; grid-template-rows: auto auto 1fr auto; grid-template-rows: subgrid;` to align `Media`, `Header`, `Content`, and `Footer` across columns. |

---

## 2. Canonical Dynamic Card Anatomy (`<article>`, `subgrid`, `:has()`, and React 19)

### 2.1. The 4 Semantic Regions & `subgrid` Alignment

Every content or analytics card should use `<article>` as its semantic root, divided into up to 4 regions (`Media`, `Header`, `Content`, `Footer`).
- **Isolating `@container` vs. `subgrid`:** Never apply `container-type: inline-size` on the exact DOM element that declares `grid-template-rows: subgrid` (size containment disables parent Grid track inheritance). Place `container-type: inline-size` on an outer wrapper or `.card-body`.
- **Conditional Media Column via `:has()`:** In horizontal layouts (`@container card (min-width: 340px)`), create the media column **only when media exists**, avoiding empty ghost tracks:

```css
/* Container Wrapper + 4-Region Subgrid Card */
.card-shell {
  container-type: inline-size;
  container-name: card;
}

.ui-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-card-gap, 0.75rem);
  padding: var(--space-card-padding, clamp(1rem, 3cqi, 1.75rem));
  background-color: var(--bg-card);
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-card, 16px);
  box-shadow: var(--elevation-low);
  transition:
    transform 0.25s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.25s cubic-bezier(0.22, 1, 0.36, 1),
    background-color 0.2s ease,
    border-color 0.2s ease;
}

/* Tactile Hover Lift & Active Return */
.ui-card.is-interactive:hover {
  transform: translateY(-4px);
  box-shadow: var(--elevation-medium);
}
.ui-card.is-interactive:active {
  transform: translateY(-1px);
  box-shadow: var(--elevation-low);
}
.ui-card:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 2px;
}

/* Subgrid aligning Media, Header, Body, and Footer across sibling cards */
.card-grid-aligned > .ui-card {
  grid-row: span 4;
  display: grid;
  grid-template-rows: auto auto 1fr auto; /* Mandatory fallback in same cascade */
  grid-template-rows: subgrid;
}

/* Microlayout: Inner metrics grid switches to 2 columns when the card itself >= 340px */
.metrics-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3, 0.75rem);
}
@container card (min-width: 340px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  /* Split into side media column only when card actually contains media */
  .ui-card:has(> .card-media, > img, > picture) {
    display: grid;
    grid-template-columns: minmax(140px, 35%) 1fr;
    align-items: start;
  }
}

/* Concentric Radius on nested items: R_inner = max(4px, R_outer - Padding) */
.metric-item {
  background-color: var(--bg-surface);
  padding: var(--space-3) var(--space-4);
  border-radius: calc(var(--radius-card, 16px) - 6px); /* 10px */
  display: flex;
  flex-direction: column;
}
.metric-value {
  font-size: clamp(1.25rem, 2.5cqi, 1.75rem);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
```

### 2.2. Clickable Cards (`::after` Stretch) & Choice Cards (`:has(> :checked)`)

1. **Accessible Clickable Card:** Never wrap an entire `<article>` in an `<a>` tag (screen readers announce the entire card body as a single giant link name). Place `<a class="card-link">` inside `<h3>` and stretch its hit target via `::after`, lifting secondary actions via `z-index: 1`:
   ```css
   .ui-card:has(a.card-link) { position: relative; }
   .ui-card a.card-link::after {
     content: "";
     position: absolute;
     inset: 0;
     z-index: 0;
     border-radius: inherit;
   }
   .ui-card :is(a:not(.card-link), button, input, select) {
     position: relative;
     z-index: 1;
   }
   ```
2. **Choice Card (Radio/Checkbox without Layout Shift):** On `<label class="ui-card">` choice cards, style checked state via `:has(> input:checked)` mutating only `border-color`, `outline`, or `box-shadow` (**never alter `border-width` or `padding`**, avoiding CLS).

### 2.3. Canonical React 19 + TypeScript Component (`ElevatedCard.tsx` — No Legacy `forwardRef`)

In **React 19**, `ref` is passed directly as a standard prop without `React.forwardRef`:

```tsx
import React from 'react';

export type ElevationLevel = 'low' | 'medium' | 'high' | 'inset';

export interface ElevatedCardProps extends React.HTMLAttributes<HTMLElement> {
  as?: 'article' | 'section' | 'div';
  elevation?: ElevationLevel;
  interactive?: boolean;
  ref?: React.Ref<HTMLElement>;
}

const ELEVATION_TOKEN: Record<ElevationLevel, string> = {
  low: 'var(--elevation-low)',
  medium: 'var(--elevation-medium)',
  high: 'var(--elevation-high)',
  inset: 'var(--shadow-inset-sunken)',
};

export function ElevatedCard({
  as: Component = 'article',
  elevation = 'low',
  interactive = false,
  className = '',
  style,
  children,
  ref,
  ...props
}: ElevatedCardProps) {
  return (
    <div className="card-shell">
      <Component
        ref={ref as React.Ref<never>}
        tabIndex={interactive ? 0 : undefined}
        className={`ui-card ${interactive ? 'is-interactive' : ''} ${className}`.trim()}
        style={{ boxShadow: ELEVATION_TOKEN[elevation], ...style }}
        {...props}
      >
        {children}
      </Component>
    </div>
  );
}
```

---

## 3. Adaptive Navigation (Bottom Bar $\leftrightarrow$ `240px` Sidebar Rail + Intrinsic Popover)

### 3.1. Single-DOM Architecture (Mobile Bottom Nav $\to$ Desktop Sidebar Rail)

Instead of duplicating HTML markup between mobile and desktop (or using `order` to invert `Tab` sequence), a single `<nav class="adaptive-nav" aria-label="Primary navigation">` transitions from the bottom thumb zone on mobile to a `240px` left rail on desktop (`>= 48em` / `768px`):

```html
<div class="app-shell">
  <nav class="adaptive-nav" aria-label="Primary navigation">
    <div class="nav-brand">
      <span class="brand-logo" aria-hidden="true">◆</span>
      <span class="brand-name">Analytics Workspace</span>
    </div>
    <ul class="nav-list" role="list">
      <li class="nav-item">
        <a href="/overview" class="nav-link" aria-current="page">
          <svg class="nav-icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>
          <span class="nav-label">Overview</span>
        </a>
      </li>
      <li class="nav-item">
        <a href="/reports" class="nav-link">
          <svg class="nav-icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/></svg>
          <span class="nav-label">Reports</span>
        </a>
      </li>
    </ul>
  </nav>
  <main class="main-content" id="main-content">...</main>
</div>
```

```css
/* Mobile-First: Thumb-Zone Bottom Navigation Bar (< 48em) */
.app-shell {
  display: grid;
  grid-template-columns: 1fr;
  min-block-size: 100dvh;
}

.main-content {
  padding: clamp(1rem, 3vw, 2.5rem);
  /* Compensate for fixed bottom bar + iOS/Android Safe Area */
  padding-block-end: calc(72px + env(safe-area-inset-bottom, 0px));
}

.adaptive-nav {
  position: fixed;
  inset-block-end: 0;
  inset-inline: 0;
  z-index: 1000;
  background-color: var(--bg-surface);
  border-block-start: 1px solid var(--border-subtle);
  box-shadow: var(--elevation-nav);
  padding-block-end: env(safe-area-inset-bottom, 0px);
}

.nav-brand { display: none; }

.nav-list {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: safe center;
  list-style: none;
  padding-block: var(--space-1, 0.25rem);
  padding-inline: var(--space-2, 0.5rem);
}

.nav-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  min-inline-size: 48px;
  min-block-size: 56px;
  padding-inline: var(--space-2, 0.5rem);
  border-radius: 10px;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  user-select: none;
  touch-action: manipulation;
  transition: background-color 0.2s ease, color 0.2s ease, transform 0.15s cubic-bezier(0.22, 1, 0.36, 1);
}

/* Non-Color Active Indicator (>= 3:1): Tinted pill + font-weight 600 */
.nav-link[aria-current="page"] {
  color: var(--brand-primary);
  font-weight: 600;
  background-color: color-mix(in oklab, var(--brand-primary) 14%, transparent);
}

/* Desktop (>= 48em / 768px): Transition to Left Sidebar Rail (240px) */
@media (min-width: 48em) {
  .app-shell {
    grid-template-columns: 240px 1fr;
  }
  .main-content {
    padding-block-end: 2.5rem;
  }
  .adaptive-nav {
    position: sticky;
    inset-block-start: 0;
    inset-block-end: auto;
    block-size: 100dvh;
    inline-size: 240px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: var(--space-4, 1.5rem) var(--space-3, 1rem);
    border-block-start: none;
    border-inline-end: 1px solid var(--border-subtle);
  }
  .nav-brand {
    display: flex;
    align-items: center;
    gap: var(--space-2, 0.5rem);
    padding-inline: var(--space-2, 0.5rem);
    margin-block-end: var(--space-6, 1.5rem);
  }
  .nav-list {
    flex-direction: column;
    justify-content: flex-start;
    gap: var(--space-2, 0.5rem);
    flex: 1;
  }
  .nav-item, .nav-link {
    inline-size: 100%;
  }
  .nav-link {
    flex-direction: row;
    justify-content: flex-start;
    gap: var(--space-3, 0.75rem);
    min-block-size: 48px;
    padding-inline: var(--space-3, 0.75rem);
  }
}
```

### 3.2. Intrinsic Top Navbar (`ResizeObserver` + Native HTML Popover API)

When a horizontal top bar must collapse overflowing links into a compact menu without guessing fixed breakpoints (e.g., when i18n translations alter label widths):
1. Use `ResizeObserver` comparing `navLinks.scrollWidth <= nav.clientWidth` (temporarily applying `.is-measuring` to measure intrinsic width).
2. Trigger the compact drawer via the **native Popover API** (`<button popovertarget="mobile-nav">`, `<div id="mobile-nav" popover="auto">`), styling `[popover]:is(:popover-open, .\:popover-open)` alongside `@starting-style`.

### 3.3. Accessible Breadcrumbs with Silent Separators (`::before`)

```html
<nav aria-label="Breadcrumb">
  <ol role="list" class="breadcrumb-list">
    <li><a href="/">Home</a></li>
    <li><a href="/dashboard">Dashboard</a></li>
    <li><a href="/dashboard/reports" aria-current="page">Reports</a></li>
  </ol>
</nav>
```
```css
.breadcrumb-list { display: flex; flex-wrap: wrap; gap: 0.5rem; list-style: none; }
.breadcrumb-list li + li::before {
  content: "/";
  margin-inline-end: 0.5rem;
  color: var(--text-secondary);
}
```

---

## 4. Usability, Perceptual Fluidity (60–120fps), Core Web Vitals & Next.js 15

### 4.1. Fitts' Law, Coarse Pointers (`any-pointer: coarse`) & 4-State FSM

- **Fitts' Law:** Every interactive control under `@media (any-pointer: coarse)` requires a minimum **`48 × 48 px`** target, at least **`8 px`** gap between adjacent targets, `touch-action: manipulation` (eliminates `300ms` tap delay), and `user-select: none`.
- **4 Mandatory Finite States (Zero Mocks/Placebos):**
  1. `loading`: Shimmer skeleton with the **exact same geometry** as the real card (`aspect-ratio` and `min-block-size`) to guarantee **CLS $= 0$**.
  2. `empty`: Clear explanatory message + primary CTA button to create or restore data.
  3. `error`: Semantic alert (`role="alert"` / `aria-live="assertive"`) translating the technical error + retry button (`onRetry`).
  4. `populated`: Real data rendered with `tabular-nums`.

### 4.2. GPU-Composited Animations, `allow-discrete`, View Transitions & Predictive Back

- **Allowed Properties:** Animate strictly `transform` and `opacity`. Never animate `top`, `left`, `width`, `height`, or `margin`.
- **Animating Discrete Elements (`<dialog>`, `[popover]`):** Declare `transition-behavior: allow-discrete` **as a separate property after `transition`** (placing it inside the `transition` shorthand breaks parsing in older engines):
  ```css
  .popover-panel {
    opacity: 0;
    transform: translateY(-8px);
    transition: opacity 0.2s ease, transform 0.2s cubic-bezier(0.22, 1, 0.36, 1), overlay 0.2s, display 0.2s;
    transition-behavior: allow-discrete;
  }
  .popover-panel:is(:popover-open, .\:popover-open) {
    opacity: 1;
    transform: translateY(0);
  }
  @starting-style {
    .popover-panel:is(:popover-open, .\:popover-open) {
      opacity: 0;
      transform: translateY(-8px);
    }
  }
  ```
- **Case-by-Case Reduced Motion (`prefers-reduced-motion`):** Wrap continuous/decorative motion in `@media (prefers-reduced-motion: no-preference)`, and under `@media (prefers-reduced-motion: reduce)` replace spatial shifts (`translateY`, `scale`) with subtle `opacity`/`background-color` transitions.
- **View Transitions API & Predictive Back:** Wrap DOM-reordering state updates in `if (document.startViewTransition) document.startViewTransition(() => updateState())` and support predictive-back previews (`transform: scale(0.90)`).

### 4.3. Fluidity Under Load (INP $\le 200\text{ms}$, LCP $\le 2.5\text{s}$) & Next.js 15 Async Params

1. **Rendering Isolation (`content-visibility: auto`):** On long feeds, lists, or Kanban columns, apply:
   ```css
   .heavy-feed-section, .kanban-column {
     content-visibility: auto;
     contain-intrinsic-size: auto 320px auto 640px;
   }
   ```
2. **Event Batching (`150ms`):** Throttle or coalesce WebSocket/streaming updates and live sliders in `150ms` windows (`requestAnimationFrame` / timer batch) so the Main Thread stays unblocked.
3. **Next.js 15 App Router (Async `params` & `searchParams`):** In Next.js 15 pages and layouts, `params` and `searchParams` are `Promise` objects requiring `await`:
   ```tsx
   export default async function ReportDetailPage({
     params,
     searchParams,
   }: {
     params: Promise<{ reportId: string }>;
     searchParams: Promise<{ density?: 'compact' | 'spacious' }>;
   }) {
     const { reportId } = await params;
     const { density = 'spacious' } = await searchParams;
     return <main data-density={density} data-report-id={reportId}>...</main>;
   }
   ```
