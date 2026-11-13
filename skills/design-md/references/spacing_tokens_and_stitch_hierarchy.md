# Engenharia de Espaçamento UX/UI, Tokens Semânticos (Google Stitch & Tailwind v4), Hierarquia Visual e Matriz de Cores OKLCH

> **Referência Canônica Tier-3 (`design-md`)** — Sintetiza `html-spacing-skill.md`, `color-quality-matrix-skill.md`, `TOKENS OKLHC`, `Design Tokens na Prática`, `frontend-best-pratics.md`, `modern-web-guidance` (`fluid-scaling`, `design-token-reactivity`), **Google Stitch (`DESIGN.md`)** e **Tailwind CSS v4 (`@theme`)**.

---

## 1. Fundamentos do Box Model e Propriedades Lógicas Internacionais

### 1.1. Dimensionamento Previsível (`box-sizing: border-box`)
Por padrão, os navegadores utilizam `box-sizing: content-box`, somando `padding` e `border` à largura/altura declaradas e provocando quebras involuntárias de layout. Todo contrato `DESIGN.md` exige o reset universal no `@layer base`:

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

### 1.2. Propriedades Lógicas de Espaçamento (LTR / RTL Ready)
Proíbe-se o uso de propriedades físicas direcionais (`left`, `right`, `top`, `bottom`, `width`, `height`) em componentes reutilizáveis. Utilize exclusivamente propriedades lógicas baseadas nos eixos *inline* (fluxo de leitura) e *block* (fluxo de empilhamento):

| Propriedade Física Legada (Proibida) | Propriedade Lógica Canônica (`DESIGN.md`) | Função Espacial |
| :--- | :--- | :--- |
| `padding-left` + `padding-right` | `padding-inline` (`start` / `end`) | Isolamento interno horizontal do componente |
| `padding-top` + `padding-bottom` | `padding-block` (`start` / `end`) | Isolamento interno vertical do componente |
| `margin-left` + `margin-right` | `margin-inline` (`auto` para centralizar) | Amortecimento externo horizontal |
| `margin-top` + `margin-bottom` | `margin-block` (`start` / `end`) | Amortecimento externo vertical |
| `width` / `height` | `inline-size` / `block-size` | Dimensões intrínsecas nos eixos de fluxo |
| `min-width` / `max-width` | `min-inline-size` / `max-inline-size` | Limites de leitura (ex.: `60ch`) e toque (`48px`) |
| `border-left` / `border-bottom` | `border-inline-start` / `border-block-end` | Indicadores ativos em sidebars e abas |

---

## 2. Arquitetura de Tokens de Espaçamento: Primitivos (`4px/8px`) + Semânticos (Google Stitch)

Para evitar que agentes geradores de UI (como **Google Stitch** e LLMs) inventem pixels arbitrários (`13px`, `27px`), o contrato `DESIGN.md` deve declarar **duas camadas de tokens de espaçamento**:
1. **Escala Primitiva (`4px/8px` Grid):** Ritmo matemático base.
2. **Tokens Semânticos de Intenção (`--space-*`):** Traduzem a **Lei da Proximidade de Gestalt** ($\text{Gap Interno de Item} < \text{Padding do Card} \le \text{Gap da Grade} < \text{Inset de Seção}$).

### 2.1. Declaração Canônica CSS + Reatividade de Densidade (`design-token-reactivity`)

```css
:root {
  /* 1. ESCALA PRIMITIVA DE ESPAÇAMENTO (Grade 8px com submúltiplos de 4px) */
  --space-0-5: 0.125rem; /* 2px  - Micro-ajuste óptico / borda fina */
  --space-1:   0.25rem;  /* 4px  - Gap entre badge e ícone */
  --space-2:   0.5rem;   /* 8px  - Gap padrão ícone-texto / controles densos */
  --space-3:   0.75rem;  /* 12px - Gap interno entre regiões de um Card */
  --space-4:   1rem;     /* 16px - Padding padrão de Card compacto / gap de lista */
  --space-6:   1.5rem;   /* 24px - Padding padrão de Card amplo / gap de Grid */
  --space-8:   2rem;     /* 32px - Separação entre subseções */
  --space-12:  3rem;     /* 48px - Separação entre grandes blocos de página */
  --space-16:  4rem;     /* 64px - Inset vertical de seções Hero/Macro */

  /* 2. TOKENS SEMÂNTICOS DE INTENÇÃO (Google Stitch & Componentes Autônomos) */
  --space-inline-icon:       var(--space-2);                      /* 8px */
  --space-component-padding: var(--space-3) var(--space-4);       /* 12px 16px */
  --space-card-gap:          var(--space-3);                      /* 12px (interno ao card) */
  --space-card-padding:      clamp(1rem, 3cqi, 1.75rem);          /* 16px -> 28px via @container */
  --space-grid-gap:          clamp(1rem, 2.5vw, 1.5rem);          /* 16px -> 24px entre cards */
  --space-section-inset:     clamp(1.5rem, 4vw, 3rem);            /* 24px -> 48px entre seções */
  --space-flow:              1.25em;                              /* Ritmo de prosa (.prose > * + *) */

  /* 3. RAIOS DE BORDA E CONCÊNTRICOS */
  --radius-sm:   0.375rem; /* 6px */
  --radius-md:   0.5rem;   /* 8px */
  --radius-lg:   0.75rem;  /* 12px */
  --radius-card: 1rem;     /* 16px */
}

/* Reatividade de Densidade sem JavaScript (zero especificidade via :where) */
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

### 2.2. A Tríade do Espaçamento (`Padding` vs. `Margin` vs. `Gap`) e Margin Collapse
- **`padding` (Isolamento Interno):** Aplica respiro dentro da borda do elemento e **expande a área clicável/tátil** de botões e links.
- **`gap` (Espaçamento Inter-Elementos):** Mecanismo primário em contêineres **Flexbox** e **CSS Grid** (`row-gap` / `column-gap`), definindo o espaço exato entre irmãos sem vazar margens nas bordas externas.
- **`margin` (Amortecimento Externo) e Colapso de Margem ($M_{\text{res}} = \max(M_1, M_2)$):**
  - No fluxo normal de bloco, margens verticais adjacentes colapsam para o maior valor.
  - **Onde o colapso NÃO ocorre:** (1) Eixo horizontal (`inline`), (2) Filhos de **Flexbox** ou **CSS Grid**, (3) Contêineres com `padding` ou `border`, e (4) Contêineres com **Contexto de Formatação de Bloco (BFC)** via `display: flow-root`.
  - **Padrões Obrigatórios Anti-Vazamento:**
    ```css
    /* Isola margens internas sem usar overflow: hidden (que cortaria box-shadow) */
    .section-container {
      display: flow-root;
    }

    /* Coruja Lobotomizada: ritmo vertical uniforme em blocos de texto/artigos */
    .prose > * + * {
      margin-block-start: var(--space-flow, 1.25em);
    }
    ```

### 2.3. Geometria Óptica de Raios Concêntricos em Cards
Quando um elemento interno (imagem de capa, bloco de métrica `.metric-item` ou botão de largura total) está aninhado dentro de um card arredondado com `padding` $P$, usar o mesmo `border-radius` em ambos gera uma dissonância visual nos cantos. Calcule o raio interno pela fórmula:
$$R_{\text{interno}} = \max(4\text{px}, R_{\text{externo}} - P_{\text{padding}})$$
- **Exemplo Canônico:** Se o `.card` tem `--radius-card: 16px` e `padding: 6px` no wrapper de mídia, o `.card-media` usa `border-radius: calc(var(--radius-card) - 6px)` (`10px`).

---

## 3. Integração Tailwind CSS v4 (`@theme`) vs. Style Dictionary

### 3.1. Configuração CSS-First no Tailwind CSS v4 (`app.css`)
O Tailwind CSS v4 elimina `tailwind.config.js` e adota `@import "tailwindcss";` combinado com a diretiva `@theme`:

```css
@import "tailwindcss";

@theme {
  /* Cores Semânticas OKLCH mapeadas para utilitários bg-app, bg-surface, bg-card, text-primary */
  --color-app:           var(--bg-app);
  --color-surface:       var(--bg-surface);
  --color-card:          var(--bg-card);
  --color-text-primary:  var(--text-primary);
  --color-text-muted:    var(--text-secondary);
  --color-brand:         var(--brand-primary);

  /* Sombras em Camadas mapeadas para shadow-elevation-low / medium / high */
  --shadow-elevation-low:    var(--elevation-low);
  --shadow-elevation-medium: var(--elevation-medium);
  --shadow-elevation-high:   var(--elevation-high);

  /* Raios e Espaçamentos Semânticos */
  --radius-card: 1rem;
  --radius-inner: calc(var(--radius-card) - 0.375rem);
}
```

### 3.2. Matriz de Decisão: Tailwind v4 (`@theme`) vs. Style Dictionary (`tokens.json`)

| Critério | Tailwind CSS v4 (`@theme`) | Style Dictionary (JSON Multi-Plataforma) |
| :--- | :--- | :--- |
| **Escopo do Projeto** | Aplicações Web React 19 / Next.js 15 focadas em velocidade e CSS nativo. | Design Systems multiplataforma compartilhados entre **Web, Android (Kotlin/Compose) e iOS**. |
| **Fonte da Verdade** | Diretamente no CSS global (`tokens.css` / `app.css`) com variáveis OKLCH. | Arquivos neutros `tokens.json` sincronizados com Figma (Tokens Studio). |
| **Build Pipeline** | Zero etapa extra de compilação de tokens. | Compila `variables.css`, `tokens.ts` e XML/Kotlin via `npx style-dictionary build`. |

---

## 4. Os 4 Pilares da Hierarquia Visual e Tipografia Fluida (`clamp()`)

1. **Pilar 1 — Escalonamento Fluido (`clamp()`) com Conformidade WCAG 1.4.4 (Zoom 200%):**
   - Nunca use `vw` ou `cqi` puros em `font-size` (bloqueia o zoom de navegador). Some sempre uma base em `rem` (`1rem + 2cqi`) e garanta que o valor máximo seja **$\le 2.5\times$ o valor mínimo**:
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
       max-inline-size: 60ch; /* Limite ergonômico de 45 a 75 caracteres por linha */
       text-wrap: pretty;
     }
     .metric-value, td[data-numeric="true"] {
       font-variant-numeric: tabular-nums; /* Alinhamento vertical perfeito de dígitos */
     }
     ```
2. **Pilar 2 — Proporção Cromática `60-30-10` em Espaço Perceptual `OKLCH`:**
   - **60% Superfície Dominante (`--bg-app`):** Fundo neutro dessaturado (`oklch(0.98 0.005 250)` no Light; `oklch(0.14 0.02 260)` no Dark — **proibido `#000000` puro**).
   - **30% Superfície Estrutural (`--bg-surface` / `--bg-card`):** Painéis, sidebars e cartões (`oklch(0.18 0.02 260)` a `oklch(0.22 0.03 260)` no Dark Mode, comunicando altura $Z$ pelo clareamento de $L$).
   - **10% Ponto Focal (`--brand-primary`):** Reservado estritamente para CTAs primários, indicadores ativos (`aria-current="page"`) e anéis `:focus-visible`.
3. **Pilar 3 — Derivação Dinâmica de Cores (RCS + `color-mix(in oklab)` + `light-dark()`):**
   - Gere estados `:hover`, `:active` e superfícies translúcidas matematicamente a partir de `--brand-primary`:
     ```css
     :root {
       color-scheme: light dark;
       --brand-primary: oklch(0.62 0.22 255);
       --btn-primary-hover:  oklch(from var(--brand-primary) calc(l - 0.08) c h);
       --btn-primary-active: oklch(from var(--brand-primary) calc(l - 0.14) c h);
       --badge-bg:           color-mix(in oklab, var(--brand-primary) 15%, transparent);
       --border-subtle:      light-dark(oklch(0.20 0.02 255 / 0.08), oklch(1.0 0 0 / 0.12));
       --text-primary:       light-dark(oklch(0.18 0.02 255), oklch(0.96 0.01 250)); /* Evita #FFF puro */
     }
     ```
4. **Pilar 4 — Matriz de Cores SVG (`feColorMatrix` $5\times 4$) e Gradientes em `oklch`:**
   - Sempre interpole gradientes com `linear-gradient(in oklch, var(--brand-primary), var(--brand-accent))` para eliminar a "zona cinza morta" do sRGB.
   - Use `<feColorMatrix type="matrix">` isolado em SVG oculto para filtros *duotone* de identidade visual e simulação/correção de daltonismo (Protanopia/Deuteranopia) sem recriar assets rasterizados.
