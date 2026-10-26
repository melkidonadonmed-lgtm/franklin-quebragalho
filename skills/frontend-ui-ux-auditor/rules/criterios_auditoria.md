# Critérios Determinísticos de Auditoria — `frontend-ui-ux-auditor`

Estes critérios regem o motor estático `scripts/ui_ux_frontend_auditor.py` (`v1.0.0`).

---

## 1. Regras de Aprovação e Reprovação (`[PASS]` / `[FAIL]`)

### `UIUX-TOKENS-01` — Design Tokens e Escala Modular de 8px (`W = 0.20`)
- **[PASS]:** Espaçamentos (`padding`, `margin`, `gap`) aderentes à progressão de 8px (`4, 8, 12, 16, 24, 32, 48, 64px`), uso de variáveis CSS (`var(--*)`) e ausência de valores arbitrários fora de escala (`p-[13px]`, `margin: 11px`).
- **[FAIL]:** Declarações arbitrárias fora da grade de 8px ou ausência de variáveis semânticas de Design Tokens.

### `UIUX-TYPO-WCAG-02` — Tipografia, Nitidez Mobile e Contraste WCAG 2.1 AA (`W = 0.20`)
- **[PASS]:** Presença de `<meta name="viewport">`, suavização `-webkit-font-smoothing: antialiased` / `optimizeLegibility`, fontes de corpo $\ge 12\text{px}$ e razão de contraste WCAG 2.1 AA $CR \ge 4.5:1$ para texto normal ($CR \ge 3.0:1$ para texto grande/UI).
- **[FAIL]:** Contraste inferior a $4.5:1$, ausência de meta viewport, fontes de texto corrido $< 12\text{px}$ ou falta de suavização subpixel.

### `UIUX-DOM-03` — Estrutura Semântica, Divsoup Ratio e Profundidade DOM (`W = 0.15`)
- **[PASS]:** Profundidade máxima da árvore DOM $\le 12$ níveis, `divsoup_ratio` ($\text{tags } \langle\text{div}\rangle / \text{total de tags}$) $\le 0.45$, presença de tags semânticas HTML5 (`main`, `header`, `nav`, `section`, `aside`, `article`) e `:focus-visible` / `aria-current`.
- **[FAIL]:** Árvore DOM com profundidade $> 12$, `divsoup_ratio > 0.45` ou ausência de marcos semânticos e foco de teclado.

### `UIUX-ICON-04` — Iconografia e Consistência Geométrica 1:1 (`W = 0.15`)
- **[PASS]:** Ícones SVG ou classes vetoriais com proporção quadrada 1:1, bounding box padronizado (`16px`, `20px` ou `24px` / `w-4 h-4`, `w-5 h-5`, `w-6 h-6`) e `stroke-width` uniforme.
- **[FAIL]:** Ícones assimétricos (`width != height`) ou tamanhos fora do padrão geométrico.

### `UIUX-LIGHT-05` — Física da Luz (135° / Chanfro Especular), Elevação em Camadas e Efeito Tátil (`W = 0.15`)
- **[PASS]:** Presença de chanfro especular interno (`inset 0 1px 0 0 rgba(255, 255, 255, ...)` / `--specular-rim`) ou borda superior reflexiva (`border-top` 135°), combinado com sombras de elevação em múltiplas camadas (Oclusão de Contato + Key Light via `--elevation-*` / `tactile-*`) e resposta física no estado `:active` (`--elevation-pressed` / `scale(0.99)`).
- **[FAIL]:** Uso de sombra única pesada/opaca (`0 4px 20px rgba(0,0,0,0.3)`) ou ausência total de indicadores de elevação multifásica e refração superior em componentes de superfície.

### `UIUX-MOTION-06` — Transições GPU Zero-Reflow, Dinâmica Tátil e Acessibilidade Motora (`W = 0.15`)
- **[PASS]:** Animações restritas a `transform`, `box-shadow` e `opacity` com curvas mecânicas (`cubic-bezier(0.2, 0.8, 0.2, 1)` para press em `100ms` e `cubic-bezier(0.2, 0, 0, 1)` para release em `160ms`) e suporte explícito a `@media (prefers-reduced-motion: reduce)` ou `motion-reduce:transition-none`.
- **[FAIL]:** Transições em propriedades que causam *layout thrashing* (`width`, `height`, `margin`, `padding`, `top`, `left`) ou ausência de suporte a movimento reduzido.
