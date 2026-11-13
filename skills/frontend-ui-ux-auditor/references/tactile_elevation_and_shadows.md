# Referência Técnica: Elevação Óptica Zenital (90°–120°), Sombras em 3 Camadas (`OKLCH`) e Tailwind CSS v4 (`@theme`)

Esta referência substitui declarações legadas em `#HEX`/`rgba()` e configs `tailwind.config.js` (v3) pelo padrão vigente **CSS OKLCH + `light-dark()` + Tailwind v4 CSS-First (`@theme`)**.

---

## 1. Modelo Óptico de Luz Zenital (90°–120°) e 3 Camadas Reais

1. **Umbra de Contato:** Deslocamento curto (`1px`–`4px`) e baixo desfoque (`2px`–`8px`), ancorando o componente à superfície subjacente.
2. **Penumbra Difusa com `spread` Negativo (`-1px` a `-8px`):** Contrai o perímetro antes da difusão, concentrando a massa gravitacional na base sem sujar as laterais.
3. **Borda Especular Zenital (`--catch-light`):** Realce interno superior (`inset 0 1px 0 0`) simulando luz incidente de cima (`90°–120°`).
4. **Dinâmica Tátil sem Borrão GPU:** Repouso (`--shadow-elevation-1`) $\to$ Hover (`translateY(-2px)` + `--shadow-elevation-2`) $\to$ Active (`translateY(0px)` + `--shadow-inset` ou retorno ao Nível 1; **proibido `scale()` fracionário em textos**).

---

## 2. Tokens Semânticos `OKLCH` + `light-dark()` + Tailwind CSS v4 (`@theme`)

```css
@import "tailwindcss";

:root {
  color-scheme: light dark;

  --brand-primary: oklch(0.62 0.21 258);
  --surface-canvas: light-dark(oklch(0.985 0.004 255), oklch(0.16 0.02 260));
  --surface-sunken: light-dark(oklch(0.955 0.008 255), oklch(0.13 0.02 260));
  --surface-card: light-dark(oklch(1 0 0), oklch(0.22 0.025 260));
  --surface-elevated: light-dark(oklch(1 0 0), oklch(0.27 0.025 260));

  --text-primary: light-dark(oklch(0.18 0.02 255), oklch(0.96 0.01 255));
  --text-secondary: light-dark(oklch(0.45 0.03 255), oklch(0.74 0.02 255));
  --border-subtle: light-dark(oklch(0.20 0.02 255 / 0.08), oklch(1 0 0 / 0.12));
  --catch-light: inset 0 1px 0 0 light-dark(oklch(1 0 0 / 0.85), oklch(1 0 0 / 0.12));

  /* Primitivas e Semânticas em 3 Camadas Ópticas (Umbra + Penumbra Spread Negativo + Catch-Light) */
  --shadow-layer-sm:
    0 1px 2px 0 light-dark(oklch(0.20 0.03 255 / 0.06), oklch(0 0 0 / 0.45)),
    0 2px 4px -1px light-dark(oklch(0.20 0.03 255 / 0.04), oklch(0 0 0 / 0.35)),
    var(--catch-light);
  --shadow-layer-md:
    0 2px 4px -1px light-dark(oklch(0.20 0.03 255 / 0.06), oklch(0 0 0 / 0.50)),
    0 8px 20px -2px light-dark(oklch(0.20 0.03 255 / 0.09), oklch(0 0 0 / 0.60)),
    0 0 12px 0 light-dark(transparent, oklch(from var(--brand-primary) l c h / 0.14)),
    var(--catch-light);
  --shadow-layer-lg:
    0 4px 8px -2px light-dark(oklch(0.20 0.03 255 / 0.07), oklch(0 0 0 / 0.55)),
    0 20px 40px -6px light-dark(oklch(0.20 0.03 255 / 0.14), oklch(0 0 0 / 0.75)),
    0 0 24px 0 light-dark(transparent, oklch(from var(--brand-primary) l c h / 0.24)),
    var(--catch-light);

  --shadow-elevation-1: var(--shadow-layer-sm);
  --shadow-elevation-2: var(--shadow-layer-md);
  --shadow-elevation-3: var(--shadow-layer-lg);
  --shadow-inset:
    inset 0 2px 4px 0 light-dark(oklch(0.15 0.02 255 / 0.08), oklch(0 0 0 / 0.65)),
    inset 0 0 0 1px light-dark(oklch(0.15 0.02 255 / 0.05), oklch(1 0 0 / 0.06));
  --elevation-pressed-inset:
    inset 0 3px 6px -1px light-dark(oklch(0.15 0.02 255 / 0.16), oklch(0 0 0 / 0.55)),
    inset 0 1px 2px 0 light-dark(oklch(0.15 0.02 255 / 0.22), oklch(0 0 0 / 0.70));

  --elevation-flat: none;
  --elevation-1: var(--shadow-elevation-1);
  --elevation-2: var(--shadow-elevation-2);
  --elevation-3: var(--shadow-elevation-3);
  --elevation-low: var(--shadow-elevation-1);
  --elevation-medium: var(--shadow-elevation-2);
  --elevation-high: var(--shadow-elevation-3);
  --shadow-inset-sunken: var(--shadow-inset);
  --shadow-clean-card: var(--shadow-elevation-2);
}

@variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));

@theme inline {
  --color-canvas: var(--surface-canvas);
  --color-sunken: var(--surface-sunken);
  --color-card: var(--surface-card);
  --color-elevated: var(--surface-elevated);
  --color-primary: var(--brand-primary);
  --shadow-elevation-1: var(--shadow-layer-sm);
  --shadow-elevation-2: var(--shadow-layer-md);
  --shadow-elevation-3: var(--shadow-layer-lg);
  --shadow-elevation-low: var(--shadow-elevation-1);
  --shadow-elevation-medium: var(--shadow-elevation-2);
  --shadow-elevation-high: var(--shadow-elevation-3);
  --shadow-inset-sunken: var(--shadow-inset);
  --shadow-tactile-sm: var(--shadow-elevation-1);
  --shadow-tactile-md: var(--shadow-elevation-2);
  --shadow-tactile-lg: var(--shadow-elevation-3);
  --shadow-tactile-inset: var(--shadow-inset);
  --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);
}
```

---

## 3. Tabela Diagnóstica de Camadas (Checklist do Auditor)

| Camada / Regra | Assinatura Esperada | Falha Comum (`[FAIL]`) |
| :--- | :--- | :--- |
| **Umbra + Penumbra** | 2+ declarações em `box-shadow` com `spread` negativo (`-1px`..`-8px`) | Sombra única borrada (`0 4px 12px rgba(0,0,0,0.4)`) |
| **Luz Zenital (`90°–120°`)** | `inset 0 1px 0 0` (`--catch-light` / `--specular-rim`) | Superfície chapada sem separação no Dark Mode |
| **Elevação Dark Mode** | Luminosidade progressiva `OKLCH` ($L = 0.16 \to 0.22 \to 0.27$) | Fundo `#000000` puro ou sombra preta invisível |
| **Resposta Motora** | `transform: translateY(-1px/-2px)` + `:focus-visible` + `prefers-reduced-motion` | Animação em `width`/`height`/`margin` (reflow) ou `scale(0.97)` em texto |
| **Espaçamento & Proximidade** | Escala `4px/8px` (`--space-*`) + Semânticos (`--space-card-padding`, `--space-grid-gap`) + Raios Concêntricos ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$) | Valores mágicos (`13px`), `padding` maior que `gap` externo ou vazamento de margem sem `display: flow-root` |
| **Flexbox, Grid & Cards** | Macrolayout Grid `RAM` (`minmax(min(100%, 280px), 1fr)`) + Microlayout `@container` + `subgrid` 4 regiões + `flex-wrap: balance` + `safe center` | Card consultando `@media`, coluna de mídia vazia sem `:has(> img)` ou `container-type` no mesmo nó do `subgrid` |
| **Hierarquia & Tipografia** | `clamp()` com $\max \le 2.5\times \min$ + `max-inline-size: 60ch` + `tabular-nums` + `text-wrap: balance/pretty` | `font-size` em `vw` puro (quebra zoom 200%), linhas $> 80\text{ch}$ ou números dançando sem `tabular-nums` |
| **Navegação & Fluidez** | Único DOM Bottom Nav (`env(safe-area-inset-bottom)`) $\leftrightarrow$ Sidebar Rail (`240px`, `100dvh`) + `aria-current="page"` ($\ge 3:1$) + `any-pointer: coarse` (`48x48px`) + `content-visibility: auto` | HTML duplicado mobile/desktop, `transition: ... allow-discrete` no shorthand ou alvos $< 48\text{px}$ no touch |
