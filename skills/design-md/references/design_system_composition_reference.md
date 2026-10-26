# Referência de Composição de Frontend e Padrão `DESIGN.md`

Esta referência consolida os fundamentos de composição espacial, tipografia fluida, hierarquia visual e tokens semânticos extraídos de sistemas de design de alto nível (**Google Stitch `DESIGN.md`**, **Linear**, **Vercel Geist**, **Stripe**, **Radix UI** e **Every Layout**).

---

## 1. Princípio Central: Semântica Acima de Paletas Fixas

Um bom `DESIGN.md` **não engessa todos os projetos na mesma paleta de cores**. Ele define **papéis semânticos** (superfície, tinta, borda, acento e feedback) e escolhe os valores cromáticos que melhor servem ao domínio do projeto:

| Domínio / Propósito do Produto | Polaridade e Atmosfera Recomendada | Prioridade de Composição |
| :--- | :--- | :--- |
| **Editorial, Documentação & Clínico (Impressão A4)** | **Alta Luminosidade (Light Mode):** Papel claro ou branco puro em `@media print`, tinta de altíssimo contraste (`>= 10:1`). | Leitura confortável (`60ch–75ch`), grades vetoriais precisas e zero ruído decorativo. |
| **SaaS Operacional, Produtividade & Anti-TDAH** | **Contraste Equilibrado (Neutro / Low-Glare ou Dual Theme):** Superfícies suaves que reduzem ofuscamento em longas jornadas. | Agrupamento claro por função, no máximo 1 CTA sólido por vista e foco imediato na tarefa. |
| **DevTools, Observabilidade & Terminais** | **Alta Densidade Técnica (Dark ou Carbon):** Fundo escuro com separação nítida por bordas de `1px` e tipografia monoespaçada tabular. | Tabelas de alta densidade, logs alinhados, atalhos de teclado (`Ctrl+K`) e latência visual zero. |
| **Produtos Criativos, Showcase & 3D WebGL** | **Atmosfera Imersiva Contextual:** Paleta guiada pela direção de arte do projeto, preservando contraste legível no HUD. | Canvas amplo, controles flutuantes discretos e transições elásticas suaves. |

---

## 2. Escala Tipográfica Modular e Fluida (`clamp()`)

Use uma razão modular entre **1.200 (Minor Third)** para interfaces densas e **1.250 (Major Third)** para páginas editoriais:

```css
:root {
  /* Famílias escolhidas conforme a personalidade do projeto */
  --font-sans: "Inter", "Plus Jakarta Sans", system-ui, -apple-system, sans-serif;
  --font-mono: "JetBrains Mono", "IBM Plex Mono", ui-monospace, monospace;

  /* Escala Tipográfica Fluida */
  --text-xs: clamp(0.6875rem, 0.65rem + 0.15vw, 0.75rem);   /* 11px - 12px: Micro-rótulos e badges */
  --text-sm: clamp(0.8125rem, 0.78rem + 0.2vw, 0.875rem);   /* 13px - 14px: Controles, tabelas e metadados */
  --text-base: clamp(0.9375rem, 0.9rem + 0.25vw, 1rem);     /* 15px - 16px: Leitura principal */
  --text-lg: clamp(1.125rem, 1.05rem + 0.35vw, 1.25rem);    /* 18px - 20px: Títulos de card/seção */
  --text-xl: clamp(1.375rem, 1.25rem + 0.6vw, 1.625rem);    /* 22px - 26px: Títulos de vista */
  --text-2xl: clamp(1.75rem, 1.5rem + 1.2vw, 2.25rem);      /* 28px - 36px: Âncoras e KPIs principais */
}

/* Regra obrigatória para números, preços, dosagens, contadores e tabelas */
.tabular-data,
table td,
input[type="number"],
.metric-value {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}
```

---

## 3. Primitivas de Composição Espacial (Every Layout + CSS Moderno)

Em vez de criar classes ad-hoc para cada tela, combine 4 primitivas fundamentais com escala **Base-4 / Base-8** (`4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px`):

1. **Stack (Fluxo Vertical):** Controla o ritmo vertical entre elementos filhos (`display: flex; flex-direction: column; gap: var(--space-4)`).
2. **Cluster (Agrupamento Horizontal Flexível):** Ideal para barras de filtros, tags e grupos de botões (`display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-2)`).
3. **Bento / Auto-Grid:** Grade responsiva sem media queries frágeis (`display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr)); gap: var(--space-4)`).
4. **Split-View (Sidebar + Main Canvas):** Estrutura ergonômica para aplicações (`display: grid; grid-template-columns: minmax(15rem, 20rem) minmax(0, 1fr)`).

---

## 4. Checklist Rápido de Qualidade de Composição

- [ ] **Squint Test (3 Níveis):** Ao desfocar a visão, o título/KPI primário, os blocos secundários e os rótulos terciários continuam distinguíveis?
- [ ] **Isolamento de Acento (90/8/2):** Há apenas **1 botão sólido primário** na região principal da tela?
- [ ] **Contraste Real:** Textos primários e secundários atingem `>= 4.5:1` (WCAG AA) sobre a superfície em que estão aplicados?
- [ ] **Completude de Estados:** Componentes assíncronos preveem estados `idle`, `loading`, `success`, `empty` e `error`?
- [ ] **Zero Poluição:** Nenhum emoji usado como ícone de interface e nenhum ativo Base64 pesado (`> 50 KB`) chumbado no HTML/CSS?
