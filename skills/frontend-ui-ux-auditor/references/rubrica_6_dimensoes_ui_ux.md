# Especificação Matemática das 6 Dimensões — Frontend UI/UX Auditor

Critérios detalhados dos 9 Eixos auditados por [`../SKILL.md`](../SKILL.md) e pelo script [`../scripts/ui_ux_frontend_auditor.py`](../scripts/ui_ux_frontend_auditor.py), integrando [`../../../rules/diretrizes-frontend-9-eixos.md`](../../../rules/diretrizes-frontend-9-eixos.md) e [`tactile_elevation_and_shadows.md`](tactile_elevation_and_shadows.md).

## Dimensão 1: Design Tokens em 3 Camadas (`OKLCH`) & Espaçamento (`W = 0.20`)

- **Camadas:** Primitivos (`--primitive-*`, `--space-*`) $\to$ Semânticos (`--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--text-primary`/`--ink-primary`, `--border-subtle`) $\to$ Componente, com `oklch()`, `light-dark()`, `color-mix(in oklab, ...)` e RCS (`from`). Modo escuro elevando $L = 0.16 \to 0.22 \to 0.27$ (zero `#000000` puro).
- **Escala Stitch & Raios Concêntricos:** Progressão `4, 8, 12, 16, 24, 32, 48, 64px` (`--space-*` e `--space-card-gap`, `--space-card-padding`, `--space-grid-gap`, `--space-section-inset`), obedecendo $\text{Gap Interno} < \text{Padding do Card} \le \text{Gap da Grade} < \text{Inset de Seção}$ e $R_{\text{interno}} = \max(4\text{px}, R_{\text{externo}} - \text{Padding})$, rejeitando valores arbitrários (`p-[13px]`, `margin: 11px`). Ver [`../../design-md/references/spacing_tokens_and_stitch_hierarchy.md`](../../design-md/references/spacing_tokens_and_stitch_hierarchy.md).

## Dimensão 2: Tipografia Fluida, Nitidez GPU & WCAG 2.1 AA (`W = 0.20`)

- `-webkit-font-smoothing: antialiased`, `text-rendering: optimizeLegibility`, `font-optical-sizing: auto`, `font-synthesis: none` em `html, body`; escala `clamp()`, `max-inline-size: 65ch` (`text-wrap: pretty`), `text-wrap: balance` em `h1`–`h4` e `tabular-nums` em métricas.
- Proibido `scale()` fracionário em texto, fontes $< 12\text{px}$; validar luminância $CR = \frac{L_{\text{claro}} + 0.05}{L_{\text{escuro}} + 0.05} \ge 4.5:1$ (normal) e $\ge 3.0:1$ (grande/UI).

## Dimensão 3: Box Model Lógico, DOM & Navegação 3 Camadas (`W = 0.15`)

- `box-sizing: border-box`, propriedades lógicas (`inline-size`, `block-size`, `padding-inline`, `margin-block`, `border-inline-start`), `display: flow-root`, `gap` e `.prose > * + *`.
- Profundidade DOM $\le 12$ níveis e `divsoup_ratio` $\le 0.45$ com HTML5 semântico (`<main>`, `<header>`, `<nav>`, `<aside>`, `<section>`, `<article>`).
- Navegação Contextual: (1) Global (`<nav aria-label>`), (2) Local/In-Page, (3) Breadcrumbs (`<nav aria-label="Caminho de navegação"><ol role="list">` + `aria-current="page"`, obrigatório **apenas em hierarquia profunda $\ge 3$ níveis**), `:focus-visible` e Ordem DOM = Ordem Visual (sem `row-reverse`/`order` arbitrário).

## Dimensão 4: Iconografia Vetorial 1:1 & Zero Emojis (`W = 0.15`)

- Bounding Box 1:1 padronizado (`16x16px`, `20x20px`, `24x24px`), família vetorial única (Lucide ou Phosphor, `stroke-width: 1.75`), `filter: drop-shadow()` em máscaras alfa e zero emojis na UI.

## Dimensão 5: Luz Zenital (90°–120°), 3 Sombras & Blend Isolation (`W = 0.15`)

- Primitivas `--shadow-layer-sm/md/lg` e Semânticos combinando **Umbra** + **Penumbra com `spread` negativo (`-1px`..`-8px`)** + **Catch-Light (`inset 0 1px 0 0`)** em `--shadow-elevation-1..3` / `--elevation-1..3` / `--shadow-elevation-low/medium/high` (+ *Ambient Brand Glow* no Dark Mode) e cavidades (`--shadow-inset` / `--elevation-pressed-inset`).
- `isolation: isolate` em `mix-blend-mode` e `linear-gradient(in oklch longer hue ...)`.

## Dimensão 6: `@container`, Cards, PWA & Movimento Físico (`W = 0.15`)

- CSS Grid RAM (`minmax(min(100%, 280px), 1fr)`), Flexbox (`flex-wrap: balance`, `align-items: safe center`, `min-inline-size: 0`), `container-type: inline-size` + `subgrid` (4 regiões + `.card:has(> img)`), 4 variantes (*Elevated*, *Outlined*, *Filled/Subtle*, *Interactive*), Bottom Bar (`env(safe-area-inset-bottom)`) $\leftrightarrow$ Sidebar Rail `240px` `100dvh` e `@media (display-mode: standalone)`. Ver [`../../frontend-code-architect/references/layout_grid_cards_and_navigation.md`](../../frontend-code-architect/references/layout_grid_cards_and_navigation.md).
- Animar apenas `transform` e `opacity` (`cubic-bezier(0.22, 1, 0.36, 1)`), `transition-behavior: allow-discrete` em propriedade separada após `transition`, `content-visibility: auto`, `@media (prefers-reduced-motion: ...)` e `@media (any-pointer: coarse)` ($\ge 48 \times 48\text{ px}$ com `gap >= 8px`, `touch-action: manipulation`).
