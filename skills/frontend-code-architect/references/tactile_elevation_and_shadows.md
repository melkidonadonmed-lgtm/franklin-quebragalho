# Technical Reference: Layered Shadows (`OKLCH`), `@container`, 4 Card Variants & 3 Complexity Tier Blueprints (`v7.0.0`)

> **When to consult this reference (`franklin_skills_get(skill_name="frontend-code-architect", section="references")`):**
> Use this module when implementing or refactoring projects across the **3 Complexity Tiers** (Axis 9), tactile surfaces (`.sculpted-card` / `<Card />`), structural navigation (`<Breadcrumbs />`), and reactive themes (`OKLCH` + `light-dark()` + anti-FOUC).

---

## 1. Tier 1 Blueprint (Low Complexity): Landing Page & Institutional Hub ("Aura Studio")

- **When to use:** Marketing sites, product hotsites, interactive portfolios, or static documentation (1–2 devs).
- **Philosophy:** Zero-Runtime CSS with flat cascade-layered organization (`@layer tokens, reset, layouts, components, utilities;`).

```text
aura-studio-landing/
├── index.html                   # Semantic HTML5 + <meta name="color-scheme" content="light dark">
├── pricing.html
├── manifest.json
├── assets/
│   ├── css/
│   │   ├── main.css             # @layer tokens, reset, layouts, components, utilities;
│   │   ├── 01-tokens.css        # OKLCH primitives & semantics, shadows, fluid typography
│   │   ├── 02-reset.css         # box-sizing: border-box, logical properties, display: flow-root
│   │   ├── 03-layouts.css       # Macrolayouts (Grid RAM, header, footer)
│   │   ├── 04-components.css    # Microlayouts (Cards with @container, buttons, breadcrumbs)
│   │   └── 05-utilities.css     # Spacing helpers, isolation: isolate, blend modes
│   ├── js/
│   │   ├── theme-switcher.js    # Light/dark toggle persisted to localStorage
│   │   └── main.js
│   └── media/
│       ├── icons/favicon.svg    # Adaptive favicon using @media (prefers-color-scheme: dark)
│       └── images/
└── README.md
```

---

## 2. Tier 2 Blueprint (Medium Complexity): Feature-Driven Modular SPA ("FinPulse Analytics")

- **When to use:** Financial dashboards, CRMs, internal tools (React/Vue/Angular + TS) with multi-state flows (3–8 devs).
- **Philosophy:** *Feature-Driven Architecture*: pure atomic primitives in `src/components/ui`, macrolayouts in `src/components/layout`, and isolated domain modules in `src/features/<domain>/`.

```text
finpulse-spa/
├── index.html
├── package.json
├── tsconfig.json
└── src/
    ├── app/
    │   ├── App.tsx
    │   ├── providers/ThemeProvider.tsx
    │   └── router/AppRouter.tsx
    ├── styles/
    │   ├── tokens.css           # Primitive & semantic OKLCH tokens + Elevation
    │   └── globals.css          # Logical reset, fluid typography, global layers
    ├── components/
    │   ├── ui/
    │   │   ├── Button/
    │   │   ├── Card/            # Polymorphic (as='article'|'section'|'div', variant='elevated'|'outlined'|'subtle')
    │   │   └── Breadcrumbs/     # <nav aria-label="Breadcrumb"><ol role="list">
    │   └── layout/
    │       ├── AppShell.tsx
    │       ├── SidebarGlobalNav.tsx
    │       └── Topbar.tsx
    ├── features/
    │   ├── portfolio-metrics/   # api/, components/, hooks/, types/, index.ts
    │   └── transactions/        # api/, components/, index.ts
    ├── hooks/
    ├── utils/
    └── main.tsx
```

---

## 3. Tier 3 Blueprint (High Complexity): Fullstack SaaS & PWA Platform ("NexusCloud Enterprise")

- **When to use:** Multi-tenant SaaS platforms, e-commerce, and hybrid PWAs with SSR, RSC, dynamic SEO, and multiple shells (8+ devs).
- **Philosophy:** App Router using **Route Groups `(marketing)` and `(workspace)`** to isolate Macrolayouts without mutating URLs, plus **Private `_components` folders** colocated next to routes.

```text
nexuscloud-enterprise/
├── public/icons/                # PWA icons (192x192, 512x512, maskable)
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root Layout (Variable fonts, Viewport API, anti-FOUC script)
│   │   ├── manifest.ts          # Dynamic Web App Manifest (PWA)
│   │   ├── global-error.tsx
│   │   ├── not-found.tsx
│   │   ├── (marketing)/         # Group 1: Public pages (Transparent Navbar + Footer)
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── pricing/page.tsx
│   │   │   └── _components/     # HeroGradientOklch.tsx, PricingComparisonGrid.tsx
│   │   ├── (workspace)/         # Group 2: Authenticated Workspace & PWA (Sidebar + Breadcrumbs + Topbar)
│   │   │   ├── layout.tsx
│   │   │   ├── loading.tsx
│   │   │   ├── error.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx
│   │   │   │   └── _components/ # RealtimeTelemetryCard.tsx, ServerLoadGrid.tsx
│   │   │   └── projects/[projectId]/
│   │   │       ├── page.tsx
│   │   │       └── opengraph-image.tsx
│   │   └── api/v1/telemetry/route.ts
│   ├── components/
│   │   ├── ui/                  # Button, Card, Dialog, Badge, Input
│   │   └── navigation/          # GlobalNav, LocalTableOfContents, StructuralBreadcrumbs
│   ├── lib/
│   ├── config/
│   └── styles/design-system.css
└── next.config.ts
```

### Root Layout with Anti-FOUC & `Viewport` API (`src/app/layout.tsx`)

```tsx
import type { Metadata, Viewport } from 'next';
import '@/styles/design-system.css';

export const viewport: Viewport = {
  colorScheme: 'light dark',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: 'oklch(0.985 0.004 255)' },
    { media: '(prefers-color-scheme: dark)', color: 'oklch(0.16 0.02 260)' },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  var saved = localStorage.getItem('nexus-theme');
                  if (saved === 'dark' || saved === 'light') {
                    document.documentElement.setAttribute('data-theme', saved);
                  }
                } catch (e) {}
              })();
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

---

## 4. Interactivity, Coarse Pointers (`pointer: coarse`) & Macro/Microlayout (`@container`)

Consult full contracts in `skills/design-md/references/design_system_composition_reference.md`:

```css
/* 1. Base Tactile Button + LVHA Order (:link -> :visited -> :hover -> :active) + Pointer Rules */
.btn-action {
  padding: 0.5em 1em; border-radius: 6px;
  background-color: var(--brand-primary, oklch(0.62 0.21 259));
  color: oklch(1 0 0); font-weight: 600;
  user-select: none; touch-action: manipulation;
  box-shadow: var(--shadow-elevation-1), inset 0 1px 1px oklch(1 0 0 / 0.18), inset 0 -1px 2px oklch(0 0 0 / 0.40);
  transition: background-color 0.2s ease, transform 0.15s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.15s cubic-bezier(0.22, 1, 0.36, 1);
}
@media (any-pointer: coarse) {
  .btn-action { padding: 0.85em 1.5em; min-height: 48px; min-width: 48px; }
}
.btn-action:hover {
  background-color: oklch(from var(--brand-primary) calc(l - 0.08) c h);
  transform: translateY(-1px);
  box-shadow: var(--shadow-elevation-2), inset 0 1px 1px oklch(1 0 0 / 0.25);
}
.btn-action:active {
  transform: translateY(1px);
  box-shadow: var(--elevation-pressed-inset, var(--shadow-inset));
  transition-duration: 80ms;
}
.btn-action:focus { outline: none; }
.btn-action:focus-visible { outline: 2px solid oklch(0.68 0.17 237); outline-offset: 2px; }

/* 2. Contextual Shadow Helpers (Title over Media & SVG/Alpha Dropdown) */
.heroTitleOverGradient {
  text-shadow: 0 2px 4px oklch(0 0 0 / 0.35), 0 4px 12px oklch(0 0 0 / 0.20);
}
.menuDropdownShadow {
  filter: drop-shadow(0 4px 6px oklch(0 0 0 / 0.08)) drop-shadow(0 10px 15px oklch(0 0 0 / 0.12));
}

/* 3. 3-Column Macrolayout (Header + Sidebar + Canvas + Chat) & @container Microlayout */
.app-layout {
  display: grid; height: 100vh; width: 100vw;
  grid-template-rows: 60px 1fr;
  grid-template-columns: 240px 1fr 340px;
  grid-template-areas: "header header header" "sidebar canvas chat";
}
.floating-analytics-card {
  width: clamp(260px, 30vw, 440px); resize: horizontal; overflow: auto;
  container-type: inline-size; container-name: analyticsCard;
}
@container analyticsCard (min-width: 320px) {
  .card-metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); }
}
.chat-messages-scroll { overflow-y: auto; overscroll-behavior-y: contain; }
```

---

## 5. Interactive Graphs (`@xyflow/react`) & Next.js 15+ Async Params

For real-time graph dashboards (`onlyRenderVisibleElements`, module-scoped `nodeTypes`, `150ms` WebSocket/Chokidar batching) and Next.js 15+ `params: Promise<...>` routing, consult `skills/complex-zero/SKILL.md`.
