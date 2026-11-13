# Os 5 Pilares de Princípios de Design & Física Óptica (`design-md`)

Complemento técnico de [`SKILL.md`](../SKILL.md). Consulte também [`design_system_composition_reference.md`](design_system_composition_reference.md) e [`spacing_tokens_and_stitch_hierarchy.md`](spacing_tokens_and_stitch_hierarchy.md).

## Pilar 1 — Filosofia e Identidade Visual Contextual
- Justificar matiz ($H$), croma ($C$), tipografia e densidade pelo universo real do produto (rejeitando paletas genéricas).
- **Hero Funcional:** Abrir imediatamente com o elemento central de valor (painel interativo, busca, indicador vivo), evitando banners decorativos vazios.
- Bordas (`1px solid var(--border-subtle)`), espaçamento e `tabular-nums` codificam hierarquia informacional.

## Pilar 2 — Arquitetura Espacial Desacoplada
- **Macrolayouts (`@media`):** CSS Grid (`repeat(auto-fit, minmax(min(100%, 280px), 1fr))`), `100dvh`; escolher **apenas o Arquétipo Espacial do produto** (*Split-View*, *Bento Grid 12 col*, *Command Center*, *Editorial 65ch*, *HUD Espacial* ou *Folha Vetorial A4 `@media print`*).
- **Microlayouts (`@container`, Flexbox & `subgrid`):** Flexbox (`flex-wrap: balance`, `align-items: safe center`, `min-inline-size: 0` sem misturar `width` e `flex-basis`), `container-type: inline-size` separado do nó `subgrid` (4 regiões em `<article>`, `.card:has(> img)`), tokens primitivos `--space-*` + semânticos (`--space-inline-icon`, `--space-card-gap`, `--space-card-padding: clamp(1rem, 3cqi, 1.75rem)`, `--space-grid-gap`, `--space-section-inset`), Gestalt ($\text{Gap Interno} < \text{Padding} \le \text{Gap Grade} < \text{Inset Seção}$), `display: flow-root`, `.prose > * + *` e Raios Concêntricos ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$).
- **Tipografia & Nitidez GPU:** `clamp()` ($\max \le 2.5\times \min$, somando `rem` + `vw`/`cqi` para WCAG 1.4.4 até 200%), `60ch–65ch`, `text-wrap: balance` (títulos `1.15–1.25`), `text-wrap: pretty` (parágrafos `1.5–1.65`), `tabular-nums`, `-webkit-font-smoothing: antialiased`, `font-synthesis: none`.

## Pilar 3 — Cores `OKLCH` (60-30-10) & Elevação $L$
- **60% Dominante (`--bg-app`/`--surface-canvas`)**, **30% Secundária (`--bg-surface`/`--bg-card`)**, **10% Destaque (`--brand-primary`)**.
- **Dark Mode:** Clarear $L$ progressivamente (`0.14` Canvas -> `0.18` Surface -> `0.22` Card -> `0.26` Modal) + borda especular `oklch(1 0 0 / 0.12)`.
- **Derivações:** `light-dark()`, `color-mix(in oklab, ...)` e RCS `oklch(from var(--brand-primary) calc(l - 0.08) c h)`.

## Pilar 4 — Física Óptica das Sombras em Camadas
$$\texttt{box-shadow: } \underbrace{\Delta x \ \Delta y \ R_{\text{blur}} \ R_{\text{spread}} \ \text{cor}}_{\text{1. Umbra}}, \ \underbrace{\Delta x \ \Delta y \ R_{\text{blur}} \ R_{\text{spread}} \ \text{cor}}_{\text{2. Penumbra (Spread } -1\text{px a }-8\text{px)}}, \ \underbrace{\texttt{inset } 0\text{px } 1\text{px } 0\text{px } 0\text{px } \text{cor}}_{\text{3. Catch-Light Zenital}}$$
- Em Tailwind v4 `@theme`, expor `--shadow-elevation-*` com `@variant dark`.
- **`box-shadow`** (caixas DOM) vs. **`text-shadow`** (serifas/glifos sobre mídia) vs. **`filter: drop-shadow()`** (SVGs/PNGs/alpha).
- **4 Modos (usar apenas os aplicáveis):** *Glassmorphism* (`isolation: isolate`, `backdrop-filter: blur(16..20px) saturate(180%)`), *Neumorphism Tátil* (outset + `--shadow-inset` / `--elevation-pressed-inset`), *Dark Glow* (`0 0 12..24px oklch(... / 0.14..0.24)`), *Flutuação `<dialog>` + `@starting-style`* (`allow-discrete`).

## Pilar 5 — Interatividade, AOM e `@layer`
- Ordem DOM = Visual; `:focus-visible`; `:user-invalid`/`:user-valid`; `<dialog>`, `popover="auto"`, `<details>`; Lei de Fitts `@media (any-pointer: coarse)` (`>= 48x48px`, `gap >= 8px`); `@media (prefers-reduced-motion: reduce)`; `@layer reset, tokens, base, layouts, components, utilities;` (zero `!important`).
