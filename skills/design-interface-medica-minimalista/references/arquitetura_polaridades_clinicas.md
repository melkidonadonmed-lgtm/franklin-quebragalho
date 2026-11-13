# Arquitetura de Polaridades Clínicas e Impressão A4 — Design Médico Minimalista

Referência detalhada dos tokens e regras ergonômicas consumida por [`../SKILL.md`](../SKILL.md), complementando [`guia_tokens_clinicos_a4.md`](guia_tokens_clinicos_a4.md) e [`../../design-md/SKILL.md`](../../design-md/SKILL.md).

## 1. Polaridades Clínicas `OKLCH`, Luz Zenital & 4 Variantes de Cards (Eixos 3–5 & 7)

- **Consultório Diurno & Impressão (`[data-theme="clinical-day"]`):** `--surface-canvas: oklch(0.97 0.005 245)`; `--surface-sunken: oklch(0.95 0.006 245)`; `--surface-card: oklch(1 0 0)`; `--ink-primary: oklch(0.18 0.02 255)` (contraste WCAG AAA $\ge 14:1$).
- **Plantão Noturno / UTI / Laudos (`[data-theme="clinical-night"]`):** Elevação progressiva de $L$ (zero preto puro anti-*OLED smearing*): `--surface-canvas: oklch(0.16 0.015 255)`; `--surface-card: oklch(0.21 0.018 255)`; `--surface-elevated: oklch(0.26 0.02 255)`; `--ink-primary: oklch(0.96 0.005 245)`.
- **Iluminação Zenital & Recesso:** Catch-Light (`inset 0 1px 0 0`) + `--shadow-elevation-1..3` / `--shadow-layer-sm/md/lg`; inputs de sinais vitais/prescrição em `--surface-sunken` + `--shadow-inset-sunken`.
- **Destaque Acromático, 4 Variantes & Semântica Contida:** Ação primária acromática (`oklch(0.18 0.02 255)` / `oklch(0.97 0.005 245)`); cards *Elevated*, *Outlined*, *Filled/Subtle*, *Interactive*; alertas via micro-dot `6px`, `border-inline-start: 2px solid` ou badge translúcido `color-mix(in oklab, ...)` mantendo texto `--ink-primary`.

## 2. Box Lógico, Nitidez GPU, `tabular-nums` & Blindagem Anti-Squish (Eixos 1–2)

- Propriedades lógicas (`inline-size`, `padding-inline`, `margin-block`), `display: flow-root`, `gap`; `-webkit-font-smoothing: antialiased`, `text-rendering: optimizeLegibility`, `font-synthesis: none`, `max-inline-size: 65ch`; zero `scale()` fracionário (use `translateY(-1px)` hover / `translateY(0)` active).
- **Zero Emojis:** Apenas ícones **Lucide** (`stroke-width: 1.75`) ou marcadores monoespaçados.
- **`tabular-nums` & Unidades Inquebráveis:** `JetBrains Mono` / `IBM Plex Mono` com `tabular-nums` em sinais vitais, `SOFA`/`CHA2DS2-VASc`/`CKD-EPI`, SIGTAP/CID-10 e doses; unidades (`mg/dL`, `mL/min/1.73m²`, `mcg/kg/min`, `mEq/L`) com `white-space: nowrap; flex-shrink: 0` e alvos $\ge 44 \times 44\text{px}$.

## 3. Arquétipos Clínicos, `@container` & Folha Vetorial A4 (Eixos 6 & 8)

- *Workbench Split-View* ou *Command Center* com `container-type: inline-size` + `@container`.
- Navegação Global (`<nav aria-label="Menu clínico principal">`), Local (`Seções do prontuário`) e Breadcrumbs (`>= 3` níveis).
- **Folha Vetorial A4 (`210mm × 297mm` `.sus-grid`):** 100% CSS Grid vetorial e SVG; em tela `--surface-canvas` + `--shadow-elevation-2`; em `@media print` ocultar `.no-print`/`nav`/`aside` e zerar sombras.
