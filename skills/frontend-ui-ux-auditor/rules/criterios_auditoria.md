# Critérios Determinísticos de Auditoria — `frontend-ui-ux-auditor` (`v3.0.0`)

Estes critérios regem o motor estático `scripts/ui_ux_frontend_auditor.py` alinhado aos **9 Eixos da SSOT** (`Preferências de Trabalho com Agentes.md`).

---

## 1. Regras de Aprovação e Reprovação (`[PASS]` / `[FAIL]`)

### `UIUX-TOKENS-01` — Design Tokens em 3 Camadas (`OKLCH`) e Escala Modular Base-4 / Base-8 (`W = 0.20`)

- **[PASS]:** Espaçamentos (`padding`, `margin`, `gap`) aderentes à progressão de 4px/8px (`4, 8, 12, 16, 24, 32, 48, 64px`), uso de variáveis CSS semânticas (`var(--*)`, `oklch()`, `light-dark()`, `color-mix()`) e ausência de valores arbitrários fora de escala (`p-[13px]`, `margin: 11px`).
- **[FAIL]:** Declarações arbitrárias fora da grade de 8px ou ausência de variáveis semânticas de Design Tokens.

### `UIUX-TYPO-WCAG-02` — Tipografia Fluida Anti-Borrão GPU e Contraste WCAG 2.1 AA (`W = 0.20`)

- **[PASS]:** Presença de `<meta name="viewport">`, suavização `-webkit-font-smoothing: antialiased` / `optimizeLegibility` / `font-synthesis: none`, escala fluida `clamp()`, `max-inline-size: 65ch`, `text-wrap: balance/pretty`, fontes de corpo $\ge 12\text{px}$, zero `scale()` fracionário em contêineres de texto e razão de contraste WCAG 2.1 AA $CR \ge 4.5:1$ para texto normal ($CR \ge 3.0:1$ para texto grande/UI).
- **[FAIL]:** Contraste inferior a $4.5:1$, ausência de meta viewport, fontes de texto corrido $< 12\text{px}$ ou falta de suavização subpixel.

### `UIUX-DOM-03` — Box Model Lógico, Estrutura Semântica, Divsoup Ratio e Navegação em 3 Camadas (`W = 0.15`)

- **[PASS]:** `box-sizing: border-box`, propriedades lógicas (`inline-size`, `padding-inline`, `margin-block`) e contenção BFC (`display: flow-root` / `gap`); profundidade máxima da árvore DOM $\le 12$ níveis, `divsoup_ratio` $\le 0.45$, tags semânticas HTML5 (`main`, `header`, `nav`, `section`, `aside`, `article`), `:focus-visible`, `aria-current="page"` (Breadcrumbs `<ol role="list">`) e Ordem DOM = Ordem Visual (sem `row-reverse` quebrando o `Tab`).
- **[FAIL]:** Árvore DOM com profundidade $> 12$, `divsoup_ratio > 0.45`, uso de `row-reverse` em navegação ou ausência de marcos semânticos e foco de teclado.

### `UIUX-ICON-04` — Iconografia Vetorial 1:1 e Zero Emojis (`W = 0.15`)

- **[PASS]:** Ícones SVG ou classes vetoriais com proporção quadrada 1:1, bounding box padronizado (`16px`, `20px` ou `24px` / `w-4 h-4`, `w-5 h-5`, `w-6 h-6`), `stroke-width` uniforme e ausência de emojis na interface.
- **[FAIL]:** Ícones assimétricos (`width != height`) ou tamanhos fora do padrão geométrico.

### `UIUX-LIGHT-05` — Luz Zenital (90°–120°), Sombras em 3 Níveis e Blend Isolation (`W = 0.15`)

- **[PASS]:** Presença de borda especular superior (`inset 0 1px 0 0` / `--catch-light` / `--specular-rim`), combinada com sombras de elevação em múltiplas camadas (Umbra + Penumbra com `spread` negativo nos Níveis 1, 2 e 3 via `--shadow-elevation-1/2/3`, `--elevation-1/2/3`, `--elevation-low/medium/high` ou `tactile-*`), `isolation: isolate` quando houver blend modes e resposta física no `:hover` e `:active`.
- **[FAIL]:** Uso de sombra única pesada/lavada (`0 4px 12px rgba(0,0,0,0.4)`) ou ausência de indicadores de elevação multifásica e luz zenital.

### `UIUX-MOTION-06` — Macro/Microlayout (`@container`), Transições GPU Zero-Reflow e Acessibilidade Motora (`W = 0.15`)

- **[PASS]:** Animações restritas a `transform`, `box-shadow`, `background-color`, `border-color` e `opacity` com curvas de desaceleração natural (`cubic-bezier(0.22, 1, 0.36, 1)`), suporte a `@container` / Grid RAM, `@media (pointer: coarse)` ($\ge 44\text{px}$) e suporte explícito a `@media (prefers-reduced-motion: reduce)` ou `motion-reduce:transition-none`.
- **[FAIL]:** Transições em propriedades que causam *layout thrashing* (`width`, `height`, `margin`, `padding`, `top`, `left`) ou ausência de suporte a movimento reduzido.
