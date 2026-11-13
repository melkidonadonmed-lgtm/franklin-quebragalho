# Arquitetura dos 4 Módulos e 9 Eixos — Frontend Code Architect

Referência operacional detalhada consumida pela skill [`../SKILL.md`](../SKILL.md) e pela SSOT [`../../../rules/diretrizes-frontend-9-eixos.md`](../../../rules/diretrizes-frontend-9-eixos.md).

## Módulo 1: Níveis de Complexidade (Eixo 9)

1. **Nível 1 — Landing Page / Hub Estático / Standalone:** arquivo único (`.html` `<= 150 KB`) ou template embarcado sem pastas artificiais; multi-arquivo estático com Zero-Runtime CSS via `@layer reset, tokens, base, layouts, components, utilities;`.
2. **Nível 2 — SPA Modular Orientada a Domínio (*Feature-Driven*):** colocalização (`Componente.tsx`, `.module.css`, `.test.tsx`, `.types.ts` na mesma pasta):

   ```text
   src/
   ├── app/                     # Providers globais e roteamento da aplicação
   ├── styles/                  # tokens.css (3 camadas OKLCH + sombras) e globals.css (@layer)
   ├── components/
   │   ├── ui/                  # Primitivos agnósticos de negócio (Button, Card, Dialog, Input)
   │   └── layout/              # Macrolayouts (AppShell, Header, Sidebar)
   ├── features/                # Módulos de negócio isolados (<dominio>/{api,components,hooks,types})
   └── types/ & utils/          # Contratos TypeScript estritos (zero any) e utilitários puros
   ```

3. **Nível 3 — Plataforma Fullstack, App Router & PWA:** grupos de rotas (`(marketing)/`, `(workspace)/`), `_components/` privados ao lado das rotas, `manifest.ts`, `Viewport` API (`colorScheme: 'light dark'`) e script síncrono anti-FOUC no `<head>`.

## Módulo 2: Box Model Lógico, Tipografia Fluida e OKLCH (Eixos 1 a 5)

- **Box Model (Eixo 1):** `box-sizing: border-box`, propriedades lógicas (`inline-size`, `block-size`, `padding-inline`, `padding-block`, `margin-inline`, `margin-block`, `border-inline-start`), `display: flow-root` nos wrappers, `gap` em Flex/Grid e `.prose > * + * { margin-block-start: var(--flow-space, 1.25em); }`.
- **Tipografia & GPU (Eixo 2):** `antialiased`, `grayscale`, `optimizeLegibility`, `font-optical-sizing: auto`, `font-synthesis: none` em `html, body`; `clamp()` (`--step--1`..`--step-3`), `max-inline-size: 65ch` (`text-wrap: pretty`, `line-height: 1.6`), `text-wrap: balance` em `h1`–`h4` (`line-height: 1.18`, `letter-spacing: -0.02em`) e `font-variant-numeric: tabular-nums` em métricas.
- **Tokens OKLCH, Dark Mode & Sombras (Eixos 3–5):** Primitivos (`--primitive-*`, `--space-*`, `--radius-*`, `--shadow-layer-sm/md/lg`), Semânticos (`--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--bg-surface-2`/`--surface-elevated`/`--surface-sunken`, `--surface-glass`, `--text-primary`/`--ink-primary`, `--text-secondary`/`--ink-secondary`, `--border-subtle`, `--shadow-elevation-1..3`, `--shadow-inset`/`--elevation-pressed-inset`) e Componente. No Dark Mode, elevar $L$ progressivamente (`0.16` Fundo -> `0.22` Card -> `0.27` Modal) + *Ambient Brand Glow* (`0px 0px 12px..24px 0px oklch(from var(--brand-primary) l c h / 0.14..0.24)`). Sombras em 3 camadas ópticas (Umbra + Penumbra com `spread` `-1px` a `-8px` + Catch-Light `inset 0 1px 0 0`), `text-shadow` em `.heroTitleOverGradient`, `filter: drop-shadow()` em `.menuDropdownShadow`, `isolation: isolate` e `linear-gradient(in oklch longer hue ...)`. Tailwind CSS v4: `--shadow-elevation-*` em `@theme` com `@variant dark`.

## Módulo 3: Macrolayouts, Microlayouts, PWAs & Cards (Eixos 6 e 7)

- **Grids & Cards:** CSS Grid RAM (`repeat(auto-fit, minmax(min(100%, 280px), 1fr))`), Flexbox 1D (`flex-wrap: balance`, `align-items: safe center`, `min-inline-size: 0` sem misturar `width` e `flex-basis`), 6 Arquétipos Espaciais (*Split-View*, *Bento 12 col*, *Command Center*, *Editorial*, *HUD Espacial*, *Folha Vetorial A4 `@media print`*).
- **`@container` & `subgrid`:** separar `container-type: inline-size; container-name: card;` do nó com `grid-template-rows: subgrid` (4 regiões: `Media`, `Header`, `Content`, `Footer`), `.ui-card:has(> .card-media, > img)` e raios concêntricos $R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$.
- **PWAs & Fluidez GPU:** `@media (display-mode: standalone), (display-mode: minimal-ui)` ocultando `.install-pwa-banner` e `user-select: none` em `nav, button, .app-header`; variantes `elevated`, `outlined`, `subtle`, `interactive` (`a.card-link::after { inset: 0 }` + ações com `z-index: 1`); `cubic-bezier(0.22, 1, 0.36, 1)`, `transition-behavior: allow-discrete` após `transition`, `@media (prefers-reduced-motion: ...)`, `@media (any-pointer: coarse)` (`48x48px`, `touch-action: manipulation`) e `content-visibility: auto; contain-intrinsic-size: auto 320px auto 640px;`.

## Módulo 4: Navegação Adaptável & Real-State (Eixo 8)

- **Único DOM (`<nav class="adaptive-nav" aria-label="Navegação Principal">`):** Bottom Bar fixa em compactos (`padding-block-end: env(safe-area-inset-bottom, 0px)`, 3–5 destinos, `min-inline-size: 48px; min-block-size: 56px`) $\leftrightarrow$ Sidebar Rail (`inline-size: 240px; block-size: 100dvh; position: sticky`) em `@media (min-width: 48em)` ou navbar com `ResizeObserver` + `popover="auto"`, marcador não-cor $\ge 3:1$ em `aria-current="page"`, navegação local/in-page e Breadcrumbs (`<ol role="list">` + `::before`) somente quando houver $\ge 3$ níveis. Ordem DOM = Ordem Visual; estados reais (`idle`, `loading`, `empty`, `error`, `pressed`).
