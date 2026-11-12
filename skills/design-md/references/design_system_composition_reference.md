# Referência Mestre de Arquitetura, Design System em 3 Camadas (`OKLCH`), Física Óptica e Modelos por Complexidade (`v7.0.0`)

Esta referência consolida os **9 Eixos + Matriz de Decisão** da Fonte Única de Verdade (SSOT) em [`../../rules/diretrizes-frontend-9-eixos.md`](../../rules/diretrizes-frontend-9-eixos.md) para consulta direta das skills `design-md`, `frontend-code-architect`, `frontend-ui-ux-auditor`, `frontend-testing-auditor` e `auditoria-projetos-sistema`.

---

## 1. Eixo 1 e 2: Box Model Lógico, Anti-Colapso de Margem e Tipografia Fluida

```css
/* Reset Base com Box Model Previsível e Propriedades Lógicas */
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
  /* Escala Tipográfica Fluida com clamp(mínimo, ideal, máximo) */
  --step--1: clamp(0.8125rem, 0.78rem + 0.16vw, 0.9rem);
  --step-0:  clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --step-1:  clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --step-2:  clamp(1.5625rem, 1.4rem + 0.8vw, 2rem);
  --step-3:  clamp(1.953rem, 1.7rem + 1.25vw, 2.665rem);
}

/* Prevenção de Colapso de Margem: BFC limpo e Coruja Lobotomizada */
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

/* Alinhamento numérico obrigatório */
.tabular-data, .tabular-metric, table td, input[type="number"], .metric-value {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}
```

---

## 2. Eixos 3, 4 e 5: Tokens em 3 Camadas (`OKLCH`), `light-dark()`, `color-mix()`, RCS e Sombras Multi-Camadas (`tokens.css`)

```css
:root {
  color-scheme: light dark;

  /* 1. TOKENS PRIMITIVOS (Catálogo Bruto) */
  --primitive-blue-500: oklch(0.62 0.21 258);
  --primitive-emerald-500: oklch(0.70 0.17 160);
  --primitive-neutral-50: oklch(0.985 0.004 255);
  --primitive-neutral-100: oklch(0.955 0.008 255);
  --primitive-neutral-800: oklch(0.22 0.025 260);
  --primitive-neutral-900: oklch(0.16 0.02 260);

  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;

  /* 2. TOKENS SEMÂNTICOS (Reativos via light-dark, color-mix e RCS from) */
  --brand-primary: var(--primitive-blue-500);
  --brand-accent: var(--primitive-emerald-500);

  --bg-canvas: light-dark(var(--primitive-neutral-50), var(--primitive-neutral-900));
  --bg-surface-1: light-dark(oklch(1 0 0), var(--primitive-neutral-800));
  --bg-surface-2: light-dark(
    var(--primitive-neutral-100),
    oklch(from var(--primitive-neutral-800) calc(l + 0.05) c h)
  );

  /* Aliases de compatibilidade SSOT (--surface-* e --ink-*) */
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

  /*Derivação por Relative Color Syntax (RCS) */
  --btn-hover: oklch(from var(--brand-primary) calc(l - 0.08) c h);
  --badge-bg: oklch(from var(--brand-primary) l c h / 0.12);

  /* SOMBRAS EM CAMADAS: Umbra de contato + Penumbra difusa com spread negativo */
  --shadow-elevation-1:
    0px 1px 2px 0px oklch(0.2 0.03 255 / 0.05),
    0px 2px 4px -1px oklch(0.2 0.03 255 / 0.04),
    var(--catch-light);
  --shadow-elevation-2:
    0px 2px 4px -1px oklch(0.2 0.03 255 / 0.06),
    0px 6px 12px -2px oklch(0.2 0.03 255 / 0.08),
    0px 14px 24px -4px oklch(0.2 0.03 255 / 0.05);
  --shadow-elevation-3:
    0px 4px 8px -2px oklch(0.2 0.03 255 / 0.06),
    0px 16px 24px -4px oklch(0.2 0.03 255 / 0.10),
    0px 32px 48px -8px oklch(0.2 0.03 255 / 0.14);
  --shadow-inset:
    inset 0px 2px 4px 0px oklch(0.15 0.02 255 / 0.08),
    inset 0px 0px 0px 1px oklch(0.15 0.02 255 / 0.05);

  --elevation-1: var(--shadow-elevation-1);
  --elevation-2: var(--shadow-elevation-2);
  --elevation-3: var(--shadow-elevation-3);
  --sunken-recess: var(--shadow-inset);

  --font-sans: 'Inter', 'Plus Jakarta Sans', 'Geist', 'IBM Plex Sans', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'IBM Plex Mono', 'Geist Mono', ui-monospace, monospace;
  --ease-out-natural: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-state-fast: cubic-bezier(0.4, 0, 0.2, 1);
}

@media (prefers-color-scheme: dark) {
  :root {
    --shadow-elevation-1:
      0px 2px 4px oklch(0 0 0 / 0.45),
      inset 0px 1px 0px 0px oklch(1 0 0 / 0.08);
    --shadow-elevation-2:
      0px 8px 20px -2px oklch(0 0 0 / 0.6),
      0px 0px 12px 0px oklch(from var(--brand-primary) l c h / 0.14),
      inset 0px 1px 0px 0px oklch(1 0 0 / 0.12);
    --shadow-elevation-3:
      0px 20px 40px -6px oklch(0 0 0 / 0.75),
      0px 0px 24px 0px oklch(from var(--brand-primary) l c h / 0.24),
      inset 0px 1px 0px 0px oklch(1 0 0 / 0.16);
  }
}

[data-theme="light"] { color-scheme: light; }
[data-theme="dark"]  { color-scheme: dark; }
```

---

## 3. Eixos 6, 7, 8 e 9: 6 Arquétipos Espaciais, `@container`, 4 Cards, Navegação em 3 Camadas e 3 Níveis de Complexidade

| Arquétipo Espacial | Domínio / Natureza do Problema | Composição Macro (`@media`) e Micro (`@container`) |
| :--- | :--- | :--- |
| **1. Workbench Split-View** | Ferramentas de criação, editores, geradores e simuladores. | Painel lateral de parâmetros (`overflow-y: auto`) + canvas principal ao vivo. |
| **2. Bento Grid Assimétrico (12 col)** | Visões gerais, portfólios técnicos, resumos executivos. | CSS Grid 12 colunas (`col-span-4`, `col-span-8`, `gap: var(--space-6)`); cards com `@container`. |
| **3. Command Center / Data Grid** | Sistemas analíticos, FinTech, monitoramento e triagem. | Cabeçalhos `sticky`, linhas `nowrap` com `tabular-nums`, barra `Cluster` e *Slide-over Drawer*. |
| **4. Canvas Editorial & Leitura** | Documentação técnica, artigos interativos, relatórios. | Coluna central `max-inline-size: 65ch`, `.prose > * + *`, *Table of Contents* local e Breadcrumbs. |
| **5. HUD Espacial com Dock Flutuante** | Visualizadores 3D, mapas, lousas infinitas. | Viewport `100vw / 100vh`, docks flutuantes `--surface-glass` (`backdrop-filter: blur(16px)`) + `--shadow-elevation-3`. |
| **6. Folha Vetorial de Impressão A4** | Exportação/visualização de documentos formais (`@media print`). | Folha `210mm × 297mm` em **100% CSS Grid vetorial e SVG** (zero bitmaps Base64 pesados). |

### Checklist Rápido de Qualidade (`Self-Refine`)

- [ ] **Box Model Lógico e BFC:** Usa `inline-size`, `padding-inline`, `margin-block`, `display: flow-root` e `gap` no pai?
- [ ] **Tokens em 3 Camadas OKLCH:** Primitivos, Semânticos (`light-dark()`, `color-mix()`, RCS `from`) e Componente definidos com Dark Mode em elevação progressiva ($L = 0.16 \to 0.22 \to 0.27$)?
- [ ] **Sombras e Nitidez GPU:** Umbra + Penumbra + Catch-Light ativos, `antialiased` + `font-synthesis: none`, `text-wrap: balance/pretty`, `tabular-nums` e zero `scale()` fracionário em textos?
- [ ] **Navegação Contextual e Real-State:** Global + Local (quando aplicável) + Breadcrumbs (`<ol role="list">` + `aria-current="page"` apenas em hierarquias $\ge 3$ níveis), Ordem DOM = Ordem Visual e 100% dos controles com lógica funcional real?

---

## 4. Referências Internas para Interfaces Complexas, Grafos em Tempo Real e App Router 15+

- **Macro-Micro, OKLCH e Acessibilidade AOM:** [`../../../rules/diretrizes-frontend-9-eixos.md`](../../../rules/diretrizes-frontend-9-eixos.md).
- **Grafos Interativos (`@xyflow/react`), Chokidar/WS e Next.js 15+ Async Params:** [`../../complex-zero/SKILL.md`](../../complex-zero/SKILL.md).

---

## 5. Adendos Especializados por Escopo de Projeto (`v8.0.0` — `design.md` & Acervo Google Drive)

### 5.1. Convenção de Pastas Feature-Driven & Colocalização (Next.js App Router & React)

- Agrupe rotas em `src/app/(dashboard)/` com pastas privadas `_components/` para componentes exclusivos da rota sem expô-los como rotas públicas.
- Encapsule domínios de negócio em `src/features/<dominio>/{api,components,hooks,types}/` e componentes atômicos em `src/components/{ui,feedback}/`.
- Mantenha colocalização estrita (`Componente.tsx`, `Componente.module.css`, `Componente.test.tsx`, `Componente.types.ts`).

### 5.2. Adendo A — Canvas Infinito, Geometria e Editores Visuais (`React Flow` / +1.000 Nós)

- **Grelha de Fundo (`.canvasPattern`):** `background-image: radial-gradient(var(--border-subtle) 1px, transparent 1px); background-size: 24px 24px;`
- **Redimensionamento Nativo (`.nodeResizable`):** `resize: both; overflow: auto; min-width: 200px; min-height: 120px; max-width: 600px; max-height: 500px;`
- **Sinalização Reativa (`.nodeFlashing`):** `@keyframes flashYellow` de `oklch(0.85 0.18 85)` + `scale(1.12)` para `var(--bg-card)` + `scale(1)` em `1.5s cubic-bezier(0.4, 0, 0.2, 1) forwards`.
- **Alta Escala (+1.000 nós):** `onlyRenderVisibleElements={true}`, Web Workers fora da *main thread* (Dagre/ELK), `React.memo`, **Batching de eventos em janela de `150ms`** e **LOD Semântico por Zoom** ($< 0.4$ Macro vs. $\ge 0.4$ Micro).

### 5.3. Adendo B & C — Matriz de Propriedades de Sombra, 4 Modos Contextuais e `<dialog>` Nativo com `@starting-style`

| Propriedade | Alvo no DOM | `inset` / `spread`? | Uso Canônico |
| :--- | :--- | :--- | :--- |
| **`box-shadow`** | Caixa retangular (`border-box`) | Sim / Sim | Cards, modais, inputs *sunken* (cuidado com `overflow: hidden` no pai). |
| **`text-shadow`** | Glifos tipográficos | Não / Não | Legibilidade de títulos sobre gradientes ou imagens sem caixa. |
| **`filter: drop-shadow()`** | Máscara Alfa (transparência real) | Não / Não | Contorno exato de ícones SVG vazados, PNGs transparentes ou `clip-path`. |

```css
/* Modo 1 & 4: Modal Nativo <dialog> Glassmorphic + Multi-Layered Shadows + @starting-style (Zero JS Animation) */
dialog::backdrop {
  background-color: oklch(0 0 0 / 0.55);
  backdrop-filter: blur(8px);
  opacity: 0;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), overlay 0.3s allow-discrete, display 0.3s allow-discrete;
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
    0px 16px 32px -4px oklch(0 0 0 / 0.60),                        /* 1. Umbra escura */
    0px 4px 12px 0px oklch(0 0 0 / 0.35),                          /* 2. Penumbra média */
    0px 0px 24px 0px oklch(from var(--brand-primary) l c h / 0.20),/* 3. Ambient Glow */
    inset 0px 1px 0px 0px oklch(1 0 0 / 0.25);                     /* 4. Bisel especular */
  opacity: 0;
  transform: scale(0.92) translateY(16px);
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), overlay 0.3s allow-discrete, display 0.3s allow-discrete;
}
.glassModal[open] { opacity: 1; transform: scale(1) translateY(0); }
@starting-style { .glassModal[open] { opacity: 0; transform: scale(0.92) translateY(16px); } }
```

### 5.5. Adendo D — Grid Sliders com CSS Scroll Snap e `TabControl` Acessível

- **Carrossel Sem JS (`.sliderGrid`):** `display: grid; grid-auto-flow: column; grid-auto-columns: clamp(260px, 40vw, 360px); overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: thin;` com filhos `.sliderCard { scroll-snap-align: start; }`.
- **Abas com Overflow Horizontal (`.tabsOverflowContainer`):** `role="tablist"` com `display: flex; overflow-x: auto; white-space: nowrap;` e botões `role="tab"` com `aria-selected="true|false"` e `aria-controls`.

### 5.6. Adendos E, F, G, H e I — Seletores Modernos, Subgrid, Trigonometria, Formulários e Sistemas Agênticos

- **Seletores Modernos:** `:has()` (estilização relacional do pai), `:is()` / `:not()` (agrupamento e exclusão lógica), `:focus-visible` (foco por teclado), `::before` / `::after` (separadores silenciosos), `::selection`.
- **CSS Subgrid (`.bentoCardSubgrid`):** `grid-row: span 3; display: grid; grid-template-rows: subgrid;` para alinhar cabeçalhos, corpos e rodapés entre colunas vizinhas.
- **Trigonometria Nativa (`sin()`, `cos()`):** Posicionamento circular/radial sem JS via `translate(calc(cos(var(--angle)) * var(--orbit-radius)), calc(sin(var(--angle)) * var(--orbit-radius)))`.
- **Formulários Modernos (`:user-invalid` / `:user-valid`):** Validação visual tardia (dispara somente após interação do usuário, nunca no carregamento inicial), combinada com `<dialog>`, `popover="auto"`, `<details name="...">` e `inert`.
- **Sistemas Agênticos (AI/LLM UI):** Acordeões `<details class="reasoningAccordion">` para *Chain-of-Thought*, *Scroll Lock Override* durante streaming, Cartões de Tool Calls com `tabular-nums` e Portões HITL (`approval_token` + `idempotency_key`).
