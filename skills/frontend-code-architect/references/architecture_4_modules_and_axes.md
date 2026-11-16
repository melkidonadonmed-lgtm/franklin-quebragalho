# 4-Module & 9-Axis Architecture — Frontend Code Architect

Detailed operational specification consumed by [`../SKILL.md`](../SKILL.md) and aligned with the SSOT (`rules/frontend-9-axes-guidelines.md`).

## Module 1: Complexity Tiers (Axis 9)

1. **Tier 1 — Landing Page / Static Hub / Standalone:** Single file (`.html` `<= 150 KB`) or embedded template without artificial folder bloat; multi-file static setups use Zero-Runtime CSS via `@layer reset, tokens, base, layouts, components, utilities;`.
2. **Tier 2 — Feature-Driven Modular SPA:** Strict colocation (`Component.tsx`, `.module.css`, `.test.tsx`, `.types.ts` in the same folder):

   ```text
   src/
   ├── app/                     # Global providers and application routing
   ├── styles/                  # tokens.css (3-layer OKLCH + shadows) and globals.css (@layer)
   ├── components/
   │   ├── ui/                  # Domain-agnostic primitives (Button, Card, Dialog, Input)
   │   └── layout/              # Macrolayouts (AppShell, Header, Sidebar)
   ├── features/                # Isolated business modules (<domain>/{api,components,hooks,types})
   └── types/ & utils/          # Strict TypeScript contracts (zero any) and pure utilities
   ```

3. **Tier 3 — Fullstack Platform, App Router & PWA:** Route groups (`(marketing)/`, `(workspace)/`), route-colocated private `_components/`, `manifest.ts`, `Viewport` API (`colorScheme: 'light dark'`), and synchronous anti-FOUC script inside `<head>`.

## Module 2: Logical Box Model, Fluid Typography & `OKLCH` (Axes 1–5)

- **Box Model (Axis 1):** `box-sizing: border-box`, logical properties (`inline-size`, `block-size`, `padding-inline`, `padding-block`, `margin-inline`, `margin-block`, `border-inline-start`), `display: flow-root` on wrappers, `gap` on Flex/Grid, and `.prose > * + * { margin-block-start: var(--flow-space, 1.25em); }`.
- **Typography & GPU Sharpness (Axis 2):** `antialiased`, `grayscale`, `optimizeLegibility`, `font-optical-sizing: auto`, `font-synthesis: none` on `html, body`; `clamp()` (`--step--1`..`--step-3`), `max-inline-size: 65ch` (`text-wrap: pretty`, `line-height: 1.6`), `text-wrap: balance` on `h1`–`h4` (`line-height: 1.18`, `letter-spacing: -0.02em`), and `font-variant-numeric: tabular-nums` on metrics.
- **OKLCH Tokens, Dark Mode & Shadows (Axes 3–5):** Primitives (`--primitive-*`, `--space-*`, `--radius-*`, `--shadow-layer-sm/md/lg`), Semantics (`--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--bg-surface-2`/`--surface-elevated`/`--surface-sunken`, `--surface-glass`, `--text-primary`/`--ink-primary`, `--text-secondary`/`--ink-secondary`, `--border-subtle`, `--shadow-elevation-1..3`, `--shadow-inset`/`--elevation-pressed-inset`), and Component tokens. In Dark Mode, elevate lightness $L$ progressively (`0.16` Canvas -> `0.22` Card -> `0.27` Modal) + *Ambient Brand Glow* (`0px 0px 12px..24px 0px oklch(from var(--brand-primary) l c h / 0.14..0.24)`). Build 3-layer optical shadows (Umbra + Penumbra with `-1px` to `-8px` spread + Catch-Light `inset 0 1px 0 0`), `text-shadow` on `.heroTitleOverGradient`, `filter: drop-shadow()` on `.menuDropdownShadow`, `isolation: isolate`, and `linear-gradient(in oklch longer hue ...)`. Tailwind CSS v4: expose `--shadow-elevation-*` inside `@theme` with `@variant dark`.

## Module 3: Macrolayouts, Microlayouts, PWAs & Cards (Axes 6 & 7)

- **Grids & Cards:** CSS Grid RAM (`repeat(auto-fit, minmax(min(100%, 280px), 1fr))`), 1D Flexbox (`flex-wrap: balance`, `align-items: safe center`, `min-inline-size: 0` without mixing `width` and `flex-basis`), and 6 Spatial Archetypes (*Split-View*, *12-Col Bento*, *Command Center*, *Editorial*, *Spatial HUD*, *Vector A4 Print Sheet `@media print`*).
- **`@container` & `subgrid`:** Isolate `container-type: inline-size; container-name: card;` from the node declaring `grid-template-rows: subgrid` (4 regions: `Media`, `Header`, `Content`, `Footer`), `.ui-card:has(> .card-media, > img)`, and concentric radii $R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$.
- **PWAs & GPU Fluidity:** `@media (display-mode: standalone), (display-mode: minimal-ui)` hiding `.install-pwa-banner` and setting `user-select: none` on `nav, button, .app-header`; card variants `elevated`, `outlined`, `subtle`, `interactive` (`a.card-link::after { inset: 0 }` + secondary actions at `z-index: 1`); `cubic-bezier(0.22, 1, 0.36, 1)`, `transition-behavior: allow-discrete` as a separate property after `transition`, `@media (prefers-reduced-motion: ...)`, `@media (any-pointer: coarse)` (`48x48px`, `touch-action: manipulation`), and `content-visibility: auto; contain-intrinsic-size: auto 320px auto 640px;`.

## Module 4: Single-DOM Adaptive Navigation & Real-State (Axis 8)

- **Single DOM (`<nav class="adaptive-nav" aria-label="Primary navigation">`):** Fixed Bottom Bar on compact screens (`padding-block-end: env(safe-area-inset-bottom, 0px)`, 3–5 destinations, `min-inline-size: 48px; min-block-size: 56px`) transitioning to Sidebar Rail (`inline-size: 240px; block-size: 100dvh; position: sticky`) at `@media (min-width: 48em)` or intrinsic navbar with `ResizeObserver` + `popover="auto"`, non-color active indicator $\ge 3:1$ on `aria-current="page"`, local/in-page navigation, and Breadcrumbs (`<ol role="list">` + `::before`) strictly when hierarchy depth $\ge 3$ levels. DOM Order = Visual Order; Real-State FSM (`idle`, `loading`, `empty`, `error`, `pressed`).
