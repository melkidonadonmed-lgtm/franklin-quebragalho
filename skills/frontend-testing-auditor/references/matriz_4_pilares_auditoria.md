# Matriz dos 4 Pilares Determinísticos — Frontend Testing Auditor

Detalhamento técnico das verificações aplicadas por [`../SKILL.md`](../SKILL.md) e pelo script [`../scripts/audit_tactile_ui.py`](../scripts/audit_tactile_ui.py), em consonância com [`../../../rules/diretrizes-frontend-9-eixos.md`](../../../rules/diretrizes-frontend-9-eixos.md) e [`a11y_fsm_rubric.md`](a11y_fsm_rubric.md).

## Pilar 1: Acessibilidade, Navegação, Nitidez GPU & `tabular-nums` (`AUDIT-A11Y` — 35%)

- **`[AUDIT-A11Y-01]` Axe-Core, Tipografia & Contraste:** Zero violações WCAG 2.1 AA ($\ge 4.5:1$); exige `antialiased`, `optimizeLegibility` e `font-synthesis: none` em `html, body`, escala `clamp()`, `max-inline-size: 65ch`, `text-wrap: balance/pretty`, proibindo `scale()` fracionário em texto e texto de baixo contraste sobre fundo cinza médio.
- **`[AUDIT-A11Y-02]` Navegação Único DOM, Teclado & Motion:** Alcançável via `Tab` (`:focus-visible`), **Ordem DOM = Ordem Visual** (zero `row-reverse` em `<nav>`), Bottom Bar (`env(safe-area-inset-bottom)`) $\leftrightarrow$ Sidebar Rail (`240px` `100dvh`), `<nav aria-label>` único, `aria-current="page"` ($\ge 3:1$), Breadcrumbs `<ol role="list">` + `::before` ($\ge 3$ níveis), `tabular-nums`, alvos `@media (any-pointer: coarse)` $\ge 48\text{px}$ (`touch-action: manipulation`), `transition-behavior: allow-discrete` após `transition`, `content-visibility: auto` e `prefers-reduced-motion`.

## Pilar 2: Engenharia Real-State & FSM (`AUDIT-STATE` — 30%)

- **`[AUDIT-STATE-01]` Estados Finitos Reais (`idle | loading/active | empty | error | pressed`):** Expor `data-state`, `data-theme`, `aria-busy="true"`, `role="status"`/`role="alert"` e controles reais (proibido `setTimeout` placebo ou `alert('Em breve')`). Nomes de componentes/classes são livres por domínio.
- **`[AUDIT-STATE-02]` Anti-Comment-Gaming:** Comentários simulando estados (`// idle | loading | error`) são removidos e penalizados em `-25 pts`.

## Pilar 3: Tokens OKLCH 3 Camadas, Sombras & Anti-Orfandade (`AUDIT-VIS-01` — 20%)

1. Tokens semânticos (`--bg-canvas`/`--bg-surface-1`/`--text-primary` ou `--surface-canvas`/`--surface-card`/`--ink-primary` em `oklch()`/`light-dark()`) e arquitetura em Níveis 1–3 (`@layer`, `src/features/`, App Router `(grupos)`/`_components`).
2. Luz zenital (`inset 0 1px 0 0` / `--catch-light`), sombras multi-camadas em 3 níveis (`--shadow-elevation-1/2/3` ou `--elevation-1/2/3`) e cavidade (`--shadow-inset` / `--sunken-recess`).
3. **Anti-Orfandade (`-25 pts`), Zero Emojis (`AUDIT-VIS-EMOJI`) e Zero Bloat Base64 (`AUDIT-VIS-BLOAT` > 50 KB):** Reprova `Card.tsx`/`SurfaceCard.tsx`/`SoftCard.tsx` não importados, emojis e Base64 excessivo.

## Pilar 4: Segurança Frontend (`AUDIT-SEC` — 15%)

- **`[AUDIT-SEC-01]` Anti-XSS:** Proibido `dangerouslySetInnerHTML` sem `DOMPurify.sanitize()` (exceção única: script síncrono anti-FOUC no `<head>` lendo `localStorage` para `data-theme`) ou `eval()`.
