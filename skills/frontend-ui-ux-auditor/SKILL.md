---
name: frontend-ui-ux-auditor
description: "Audita com precisão matemática densidade de nós DOM, contraste WCAG 2.1 AA, luz zenital 90-120, elevação por sombras, espaçamento e camadas. Use para diagnóstico visual de frontend; não use para backend."
version: "3.1.0"
updated_at: "2026-11-12"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "3.1.0"
  updated_at: "2026-11-12"
  author: "UI-Architect & Melki"
  category: "Frontend UI/UX Mathematical Auditing, OKLCH Design Tokens, Logical Box Model & Optical Physics"
  tags: ["ui-ux-audit", "oklch", "wcag-contrast", "zenithal-light", "dom-density", "container-queries"]
---
# Skill: Auditor de UI/UX, Box Model Lógico, Cores Perceptuais `OKLCH`, Navegação Contextual e Luz Zenital (`v3.1.0`)

## 1. Objetivo, Propósito e Quando Usar (Gatilhos)

Esta Skill estabelece a esteira de auditoria matemática para inspecionar componentes e layouts frontend, garantindo acabamento alinhado aos **9 Eixos da SSOT** ([`../../rules/diretrizes-frontend-9-eixos.md`](../../rules/diretrizes-frontend-9-eixos.md)). O motor determinístico (`scripts/ui_ux_frontend_auditor.py`) avalia Design Tokens em 3 camadas (`OKLCH` / escala `4px/8px`), propriedades lógicas e prevenção de colapso de margem, contraste WCAG 2.1 AA, nitidez tipográfica fluida anti-borrão GPU, árvore DOM, navegação contextual, sombras multi-camadas com luz zenital (90°–120°) e Container Queries (`@container`).

### Gatilhos Positivos (Quando Usar)

- Solicitação de auditoria ou inspeção visual/estrutural de telas, interfaces, menus, cards e layouts.
- Verificação de Design Tokens em 3 camadas (`--bg-canvas`/`--surface-canvas`, `--text-primary`/`--ink-primary`, `oklch()`, `light-dark()`, `color-mix()`, RCS `from`) e conformidade com `DESIGN.md` (escala Base-4 / Base-8).
- Avaliação de Box Model lógico (`inline-size`, `padding-inline`, `margin-block`), contenção de colapso de margem (`display: flow-root`, `gap`, `.prose > * + *`), nitidez tipográfica (`clamp()`, `65ch`, `text-wrap: balance/pretty`, `antialiased`, `font-synthesis: none`) e `@container`.
- Auditoria de acessibilidade e navegação em 3 camadas (contraste WCAG 2.1 AA, `<nav aria-label>`, Breadcrumbs `<ol role="list">` + `aria-current="page"`, Ordem DOM = Ordem Visual e touch targets $\ge 44 \times 44\text{ px}$).

### Gatilhos Negativos (Quando NÃO Usar)

- Revisão de regras de negócio puramente backend (queries SQL, rotas gRPC isoladas).
- Testes unitários de algoritmos computacionais sem relação com a camada visual.

---

## 2. Entradas e Pré-requisitos

1. **Alvo da Auditoria:** Arquivo `.html`, `.css`, `.jsx`, `.tsx`, `.vue` ou diretório raiz do frontend.
2. **Motor Determinístico:** `scripts/ui_ux_frontend_auditor.py`, executável via CLI (`python scripts/ui_ux_frontend_auditor.py --target <caminho>`) ou MCP (`franklin_run_skill_script`).
3. **Contrato de Design (Opcional):** `DESIGN.md` na raiz do projeto.

---

## 3. Processamento e Fluxo: As 6 Dimensões da Auditoria Frontend UI/UX (Cobrindo os 9 Eixos)

### 3.1. Dimensão 1: Design Tokens em 3 Camadas (`OKLCH`) e Escala Modular Base-4 / Base-8 (`W = 0.20`)

- **Arquitetura em 3 Camadas (Eixos 3 & 4):** Verifica a separação entre *Primitivos* (`--primitive-*`, `--space-*`), *Semânticos* (`--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--text-primary`/`--ink-primary`, `--border-subtle`) e *Componente*, com suporte a `oklch()`, `light-dark()`, `color-mix(in oklab, ...)` e RCS (`from`), além de elevação progressiva no Modo Escuro ($L = 0.16 \to 0.22 \to 0.27$, zero `#000000` puro).
- **Grade de Espaçamento e Detecção de Valores Arbitrários:** Todo `padding`, `margin` e `gap` deve derivar da progressão canônica (`4, 8, 12, 16, 24, 32, 48, 64px`) e raios concêntricos ($R_{\text{interno}} = \max(4\text{px}, R_{\text{externo}} - \text{Padding})$), rejeitando valores arbitrários (`p-[13px]`, `w-[37px]`, `margin: 11px`).

### 3.2. Dimensão 2: Tipografia Fluida, Nitidez Anti-Borrão GPU e Contraste WCAG 2.1 AA (`W = 0.20`)

- **Travas de Renderização e Escala Fluida (Eixo 2):** Exige `-webkit-font-smoothing: antialiased`, `text-rendering: optimizeLegibility`, `font-optical-sizing: auto` e `font-synthesis: none` em `html, body`; escala `clamp()`, `max-inline-size: 65ch` (`text-wrap: pretty` em `p, li`), `text-wrap: balance` em títulos (`h1`–`h4`) e `font-variant-numeric: tabular-nums` em métricas.
- **Prevenção de Borrão GPU e Contraste WCAG 2.1 AA:** Proíbe `scale()` fracionário em textos, texto colorido de baixo contraste sobre fundo médio, fontes $< 12\text{px}$ e valida a luminância relativa W3C ($CR = \frac{L_{\text{claro}} + 0.05}{L_{\text{escuro}} + 0.05} \ge 4.5:1$ para texto normal; $\ge 3.0:1$ para texto grande/UI).

### 3.3. Dimensão 3: Box Model Lógico, Anti-Colapso de Margem, Árvore DOM e Navegação em 3 Camadas (`W = 0.15`)

- **Box Model e Colapso de Margem (Eixo 1):** Verifica `box-sizing: border-box`, propriedades lógicas (`inline-size`, `block-size`, `padding-inline`, `margin-block`, `border-inline-start`), contenção BFC com `display: flow-root`, espaçamento delegado ao pai via `gap` e `.prose > * + *`.
- **Densidade DOM:** Profundidade máxima **$\le 12$ níveis** e `divsoup_ratio` ($\frac{\text{tags } \langle\text{div}\rangle}{\text{total de tags}}$) **$\le 0.45$**, exigindo HTML5 semântico (`<main>`, `<header>`, `<nav>`, `<aside>`, `<section>`, `<article>`).
- **Navegação Contextual (Eixo 8):** (1) *Global* (`<nav aria-label>`), (2) *Local/In-Page* (quando a vista possuir múltiplas seções/filtros), (3) *Estrutural/Breadcrumbs* (`<nav aria-label="Caminho de navegação"><ol role="list">` + `aria-current="page"`, exigido **apenas em fluxos com hierarquia profunda $\ge 3$ níveis**, dispensado em landing pages, modais ou cockpits de tela única), `:focus-visible` e **Ordem DOM = Ordem Visual** (proibido `flex-direction: row-reverse` ou `order` arbitrário que quebre a tecla `Tab`).

### 3.4. Dimensão 4: Iconografia Vetorial 1:1 e Zero Emojis (`W = 0.15`)

- **Bounding Box Padronizado (1:1):** $16 \times 16\text{ px}$ (`w-4 h-4`), $20 \times 20\text{ px}$ (`w-5 h-5`) ou $24 \times 24\text{ px}$ (`w-6 h-6`), família vetorial única (**Lucide** ou **Phosphor**, `stroke-width: 1.75`), `filter: drop-shadow()` quando houver sombra em máscara alfa e **zero emojis na interface**.

### 3.5. Dimensão 5: Os 3 Tipos de Sombra, Luz Zenital (90°–120°) e Blend Isolation (`W = 0.15`)

Conforme [`references/tactile_elevation_and_shadows.md`](references/tactile_elevation_and_shadows.md):

- **Sombras Realistas em Camadas (Eixo 5):** Combina **Umbra de contato** + **Penumbra difusa com `spread` negativo** + **Borda Especular Superior (`inset 0 1px 0 0` / `--catch-light`)** nos 3 níveis (`--shadow-elevation-1..3` / `--elevation-1..3`) e cavidade tátil (`--shadow-inset` / `--sunken-recess`), proibindo sombra única lavada.
- **Blend Modes e Gradientes OKLCH:** Exige `isolation: isolate` em contêineres com `mix-blend-mode` e recomenda `linear-gradient(in oklch longer hue ...)`.

### 3.6. Dimensão 6: Macro/Microlayout (`@container`), 4 Variantes de Cards, PWA e Movimento Físico (`W = 0.15`)

- **Macrolayout (`@media`) vs. Microlayout (`@container`) & 4 Cards (Eixos 6 & 7):** CSS Grid RAM para página, `container-type: inline-size` + `@container` para cards (*Elevated*, *Outlined*, *Filled/Subtle*, *Interactive*) e `@media (display-mode: standalone)` para PWAs.
- **Movimento Físico e Acessibilidade Motora:** Animar apenas `transform`, `box-shadow`, `background-color`, `border-color` e `opacity` (`cubic-bezier(0.22, 1, 0.36, 1)`), respeitando `@media (prefers-reduced-motion: reduce)` e `@media (pointer: coarse)` ($\ge 44 \times 44\text{ px}$).

---

## 4. Saídas e Entregáveis: Rubrica Matemática

$$\text{Score}_{\text{UI/UX}} = \sum_{j=1}^{6} W_j \cdot S_j$$

| Dimensão Auditada | Peso ($W_j$) | Critério Central de Avaliação |
| :--- | :---: | :--- |
| **Design Tokens 3 Camadas & OKLCH** | **0.20 (20%)** | Escala Base-4/Base-8, tokens semânticos (`oklch`/`light-dark`) e zero valores arbitrários. |
| **Tipografia Fluida & Nitidez GPU** | **0.20 (20%)** | `clamp()`, `65ch`, `balance/pretty`, `antialiased`, `font-synthesis: none` e contraste WCAG AA. |
| **Box Lógico, DOM & Nav 3 Camadas** | **0.15 (15%)** | `border-box`, propriedades lógicas/`flow-root`, DOM $\le 12$, `divsoup` $\le 0.45$, Breadcrumbs e Ordem Tab. |
| **Iconografia 1:1 & Zero Emojis** | **0.15 (15%)** | Proporção 1:1 (16/20/24px), `stroke-width` uniforme e zero emojis. |
| **Luz Zenital, 3 Sombras & Isolation** | **0.15 (15%)** | Catch-light (`inset 0 1px 0 0`), sombras multi-camadas em 3 níveis e `isolation: isolate`. |
| **Macro/Micro `@container`, Cards & Motion** | **0.15 (15%)** | Zero reflow GPU, `@container`, curvas Bézier, `pointer: coarse` $\ge 44\text{px}$ e `prefers-reduced-motion`. |

### Execução do Motor Determinístico (`scripts/ui_ux_frontend_auditor.py`)

```powershell
uv run python skills/frontend-ui-ux-auditor/scripts/ui_ux_frontend_auditor.py --target "<arquivo_ou_diretorio>"
```

---

## 5. Exceções, Limites e Guardrails

- **Escopo Estático vs. Runtime:** `ui_ux_frontend_auditor.py` inspeciona estaticamente HTML/CSS/JSX/TSX conforme [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md); para inspeção interativa do DOM renderizado (`@eX` / CDP), combine com `auditoria-projetos-sistema` ou `complex-zero`.
- **Somente Leitura:** Esta skill diagnostica e pontua a interface; mutações de refatoração cabem a `frontend-code-architect`.
