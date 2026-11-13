# Arquitetura de Layout (Flexbox vs. Grid vs. Subgrid), Cards Dinâmicos, Navegação Adaptável e Fluidez (React 19 / Next.js 15 / Tailwind v4)

> **Referência Canônica Tier-3 (`frontend-code-architect`)** — Sintetiza `Card UI Analytics`, `Cartões CSS Dinâmicos`, `BARRA DE NAVEGAÇÃO ADAPTAVEL`, `usabilidade e fluidez`, `adaptabilidade`, `Design Responsivo Moderno`, `melhores práticas de acessibilidade` e os 7 guias do `modern-web-guidance` (`css-layout`, `card`, `navbar`, `motion`, `interactions-in-complex-layouts`, `fluid-scaling`, `design-token-reactivity`).

---

## 1. Árvore de Decisão Espacial: Macrolayout (Grid) vs. Microlayout (`@container` + Flex/Subgrid)

### 1.1. Macrolayouts (Estrutura Global da Página / App Shell)
- **Mecanismo:** **CSS Grid** aliado a **Media Queries (`@media`)** e unidades de viewport dinâmicas (`100dvh`).
- **Responsabilidade:** Coordenar a casca global (`header`, `aside` / barra de navegação de `240px`, `<main>` e painel inspetor).
- **Padrão RAM (Repeat, Auto, Minmax) sem Overflow Horizontal:**
  ```css
  .macro-card-grid {
    display: grid;
    /* min(100%, 280px) evita barra de rolagem horizontal em telas menores que 280px */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
    gap: var(--space-grid-gap, clamp(1rem, 2.5vw, 1.5rem));
  }
  ```

### 1.2. Microlayouts (Componentes Autônomos Independentes do Viewport)
- **Mecanismo:** **Container Queries (`container-type: inline-size`)** + unidades `cqi`/`cqw`.
- **Regra de Ouro:** Um componente reutilizável (Card, Widget, Toolbar) **nunca consulta `@media`** para reorganizar suas colunas internas; ele responde à largura real do seu próprio contêiner (`@container card (min-width: 340px)`).

### 1.3. Regras Críticas de Flexbox (1D) vs. CSS Grid (2D) (`modern-web-guidance: css-layout`)

| Cenário | Mecanismo Correto | Regras Técnicas Obrigatórias |
| :--- | :--- | :--- |
| **Linha de tags, pílulas, filtros ou botões** | **Flexbox (1D)** | Usar `display: flex; flex-wrap: wrap; flex-wrap: balance; gap: var(--space-2);` (evita linha órfã com 1 item isolado). |
| **Centralização de barra ou modal** | **Flexbox / Grid** | Usar `align-items: safe center; justify-content: safe center;` (impede que o topo/início de elementos focáveis seja cortado fora da tela em viewports estreitos). |
| **Filhos Flex/Grid com texto longo ou truncado** | **Flexbox / Grid** | Declarar `min-inline-size: 0` no filho (o padrão `min-inline-size: auto` impede `text-overflow: ellipsis` e estoura o contêiner). |
| **Dimensionamento intrínseco Flex** | **Flexbox (1D)** | Usar shorthand `flex: 1 1 250px`. **Proibido** declarar `width` ou `inline-size` junto com `flex-basis`. |
| **Alinhamento vertical entre Cards irmãos** | **CSS Grid + `subgrid`** | Usar `grid-row: span 4; grid-template-rows: auto auto 1fr auto; grid-template-rows: subgrid;` para alinhar `Media`, `Header`, `Content` e `Footer` entre colunas. |

---

## 2. Anatomia Canônica de Cards Dinâmicos (`<article>`, `subgrid`, `:has()` e React 19)

### 2.1. As 4 Regiões Semânticas e Alinhamento por `subgrid`
Todo cartão de conteúdo ou analytics deve usar `<article>` como raiz semântica, dividido em até 4 regiões (`Media`, `Header`, `Content`, `Footer`).
- **Isolamento `@container` vs. `subgrid`:** Nunca aplique `container-type: inline-size` no exato mesmo elemento DOM que declara `grid-template-rows: subgrid` (pois a contenção de tamanho desativa a herança das tracks do Grid pai). Aplique `container-type: inline-size` em um wrapper ou no `.card-body`.
- **Escopo Condicional de Mídia via `:has()`:** Em layouts horizontais (`@container card (min-width: 380px)`), crie a coluna de imagem **apenas quando a mídia existir**, evitando colunas vazias fantasmas:

```css
/* Wrapper de Contêiner + Card com 4 Regiões e Subgrid */
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

/* Elevação Tridimensional no Hover e Retorno Tátil no Active */
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

/* Subgrid para alinhar Media, Header, Body e Footer entre cartões lado a lado */
.card-grid-aligned > .ui-card {
  grid-row: span 4;
  display: grid;
  grid-template-rows: auto auto 1fr auto; /* Fallback obrigatório na mesma cascata */
  grid-template-rows: subgrid;
}

/* Microlayout: Grade interna de métricas vira 2 colunas quando o PRÓPRIO card >= 340px */
.metrics-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3, 0.75rem);
}
@container card (min-width: 340px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  /* Só divide em coluna lateral de mídia se o card realmente tiver imagem/mídia */
  .ui-card:has(> .card-media, > img, > picture) {
    display: grid;
    grid-template-columns: minmax(140px, 35%) 1fr;
    align-items: start;
  }
}

/* Raio Concêntrico nos itens internos: R_inner = max(4px, R_outer - Padding) */
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

### 2.2. Clickable Cards (`::after` Stretch) e Choice Cards (`:has(> :checked)`)
1. **Clickable Card Acessível:** Jamais envolva todo o `<article>` em uma tag `<a>` (faz leitores de tela anunciarem todo o parágrafo como um único nome de link gigante). Coloque o `<a class="card-link">` dentro do `<h3>` e expanda sua área de clique via `::after`, mantendo botões secundários clicáveis acima com `z-index: 1`:
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
2. **Choice Card (Radio/Checkbox sem Layout Shift):** Em cartões de escolha (`<label class="ui-card">`), estilize o estado selecionado com `:has(> input:checked)` alterando apenas `border-color`, `outline` ou `box-shadow` (**nunca altere `border-width` ou `padding`**, o que causaria salto de layout / CLS).

### 2.3. Componente Canônico React 19 + TypeScript (`ElevatedCard.tsx` — Sem `forwardRef` Legado)
No **React 19**, `ref` é passado diretamente como prop padrão sem `React.forwardRef`:

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

## 3. Navegação Adaptável (Bottom Bar $\leftrightarrow$ Sidebar Rail `240px` + Popover Intrínseco)

### 3.1. Arquitetura de Único DOM (Transição Mobile Bottom Nav $\to$ Desktop Sidebar Rail)
Em vez de duplicar marcação HTML entre mobile e desktop (ou usar `order` para inverter a sequência de `Tab`), um único `<nav class="adaptive-nav" aria-label="Navegação Principal">` transiciona perfeitamente da base da tela (zona do polegar no mobile) para uma barra lateral esquerda de `240px` no desktop (`>= 48em` / `768px`):

```html
<div class="app-shell">
  <nav class="adaptive-nav" aria-label="Navegação Principal">
    <div class="nav-brand">
      <span class="brand-logo" aria-hidden="true">◆</span>
      <span class="brand-name">Analytics Workspace</span>
    </div>
    <ul class="nav-list" role="list">
      <li class="nav-item">
        <a href="/visao-geral" class="nav-link" aria-current="page">
          <svg class="nav-icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>
          <span class="nav-label">Visão Geral</span>
        </a>
      </li>
      <li class="nav-item">
        <a href="/relatorios" class="nav-link">
          <svg class="nav-icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/></svg>
          <span class="nav-label">Relatórios</span>
        </a>
      </li>
    </ul>
  </nav>
  <main class="main-content" id="main-content">...</main>
</div>
```

```css
/* Mobile-First: Bottom Navigation Bar na Zona do Polegar (< 48em) */
.app-shell {
  display: grid;
  grid-template-columns: 1fr;
  min-block-size: 100dvh;
}

.main-content {
  padding: clamp(1rem, 3vw, 2.5rem);
  /* Compensa a barra fixa inferior + Safe Area do iOS/Android */
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

/* Indicador Ativo Não-Cor (>= 3:1): Pílula de fundo + barra/peso 600 */
.nav-link[aria-current="page"] {
  color: var(--brand-primary);
  font-weight: 600;
  background-color: color-mix(in oklab, var(--brand-primary) 14%, transparent);
}

/* Desktop (>= 48em / 768px): Transição para Sidebar Rail Esquerda (240px) */
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

### 3.2. Navbar Superior Intrínseca (`ResizeObserver` + HTML Popover API Nativa)
Quando uma barra horizontal superior precisa colapsar links em um menu compacto sem chutar um breakpoint fixo (pois traduções i18n alteram o comprimento dos textos):
1. Use `ResizeObserver` comparando `navLinks.scrollWidth <= nav.clientWidth` (aplicando temporariamente `.is-measuring` para medir a largura intrínseca).
2. Acione o menu compacto via **Popover API nativa** (`<button popovertarget="mobile-nav">`, `<div id="mobile-nav" popover="auto">`), estilizando `[popover]:is(:popover-open, .\:popover-open)` e `@starting-style`.

### 3.3. Breadcrumbs Acessíveis com Separadores Silenciosos (`::before`)
```html
<nav aria-label="Caminho de navegação">
  <ol role="list" class="breadcrumb-list">
    <li><a href="/">Início</a></li>
    <li><a href="/painel">Painel</a></li>
    <li><a href="/painel/relatorios" aria-current="page">Relatórios</a></li>
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

## 4. Usabilidade, Fluidez Perceptual (60–120fps), Core Web Vitals e Next.js 15

### 4.1. Lei de Fitts, Apontadores (`any-pointer: coarse`) e Máquina de 4 Estados (FSM)
- **Lei de Fitts:** Todo controle interativo em `@media (any-pointer: coarse)` exige área mínima de **`48 × 48 px`**, espaçamento mínimo de **`8 px`** entre alvos adjacentes, `touch-action: manipulation` (elimina atraso de `300ms`) e `user-select: none`.
- **4 Estados Finitos Obrigatórios (Zero Mocks/Placebos):**
  1. `loading`: Skeleton `shimmer` com **exatamente a mesma geometria** do card real (`aspect-ratio` e `min-block-size`) para garantir **CLS $= 0$**.
  2. `empty`: Mensagem explicativa clara + botão CTA primário para criar o primeiro registro.
  3. `error`: Alerta semântico (`role="alert"` / `aria-live="assertive"`) traduzindo o erro técnico + botão de retentativa (`onRetry`).
  4. `populated`: Dados reais renderizados com `tabular-nums`.

### 4.2. Animações no Compositor GPU, `allow-discrete`, View Transitions e Predictive Back
- **Propriedades Permitidas:** Anime exclusivamente `transform` e `opacity`. Jamais anime `top`, `left`, `width`, `height` ou `margin`.
- **Animação de Elementos Discretos (`<dialog>`, `[popover]`):** Declare `transition-behavior: allow-discrete` **como propriedade separada após `transition`** (incluí-lo no shorthand `transition` quebra o parsing em navegadores mais antigos):
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
- **Movimento Reduzido Caso-a-Caso (`prefers-reduced-motion`):** Envolva animações contínuas/decorativas em `@media (prefers-reduced-motion: no-preference)` e, em `@media (prefers-reduced-motion: reduce)`, substitua deslocamentos espaciais (`translateY`, `scale`) por transições rápidas de `opacity`/`background-color`.
- **View Transitions API & Predictive Back:** Envolva mudanças de estado/rota que reordenam o DOM em `if (document.startViewTransition) document.startViewTransition(() => updateState())` e suporte preview de retorno preditivo (`transform: scale(0.90)`).

### 4.3. Fluidez sob Carga (INP $\le 200\text{ms}$, LCP $\le 2.5\text{s}$) e Next.js 15 Async Params
1. **Isolamento de Renderização (`content-visibility: auto`):** Em listas extensas, feeds ou colunas Kanban, aplique:
   ```css
   .heavy-feed-section, .kanban-column {
     content-visibility: auto;
     contain-intrinsic-size: auto 320px auto 640px;
   }
   ```
2. **Batching de Eventos (`150ms`):** Atualizações de WebSocket/streaming ou sliders em tempo real devem ser agrupadas em janelas de `150ms` (`requestAnimationFrame` / throttle) para não bloquear a Main Thread.
3. **Next.js 15 App Router (Async `params` & `searchParams`):** Em páginas e layouts do Next.js 15, `params` e `searchParams` são `Promise` e exigem `await`:
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
