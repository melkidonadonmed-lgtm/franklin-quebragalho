---
name: frontend-ui-ux-auditor
description: "Audita com precisão matemática densidade de nós DOM, contraste WCAG 2.1 AA, luz zenital 90-120, elevação por sombras, espaçamento e camadas. Use para diagnóstico visual de frontend; não use para backend."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "3.1.0"
  updated_at: "2026-11-13"
  author: "UI-Architect & Melki"
  category: "Frontend UI/UX Mathematical Auditing, OKLCH Design Tokens, Logical Box Model & Optical Physics"
  tags: ["ui-ux-audit", "oklch", "wcag-contrast", "zenithal-light", "dom-density", "container-queries"]
---

# Frontend UI/UX Auditor (`frontend-ui-ux-auditor`)

## 1. Propósito e Gatilhos (Quando Usar)

Executa auditoria matemática e visual de componentes/layouts frontend alinhada aos **9 Eixos da SSOT** ([`../../rules/diretrizes-frontend-9-eixos.md`](../../rules/diretrizes-frontend-9-eixos.md)) via motor determinístico `scripts/ui_ux_frontend_auditor.py`:

- Inspecionar telas, menus, cards e layouts quanto a Tokens OKLCH em 3 camadas e escala `4px/8px` (`DESIGN.md`).
- Validar Box Model lógico, anti-colapso (`display: flow-root`), contraste WCAG 2.1 AA, nitidez GPU, `@container`, sombras com luz zenital (90°–120°), DOM e navegação em 3 camadas.

## 2. Entradas e Pré-requisitos

- **`target_path` (obrigatório):** Arquivo `.html`, `.css`, `.jsx`, `.tsx`, `.vue` ou diretório frontend.
- **Motor Determinístico:** `scripts/ui_ux_frontend_auditor.py` (CLI ou `franklin_run_skill_script`).
- **`DESIGN.md` (opcional):** Contrato de tokens na raiz do projeto.

## 3. Processamento: As 6 Dimensões da Auditoria Frontend

Consulte [`references/rubrica_6_dimensoes_ui_ux.md`](references/rubrica_6_dimensoes_ui_ux.md), [`references/tactile_elevation_and_shadows.md`](references/tactile_elevation_and_shadows.md), [`../design-md/references/spacing_tokens_and_stitch_hierarchy.md`](../design-md/references/spacing_tokens_and_stitch_hierarchy.md) e [`../frontend-code-architect/references/layout_grid_cards_and_navigation.md`](../frontend-code-architect/references/layout_grid_cards_and_navigation.md):

| Dimensão Auditada | Peso ($W_j$) | Critério Central de Avaliação |
| :--- | :---: | :--- |
| **1. Design Tokens 3 Camadas & OKLCH** | `0.20` | Escala `4px/8px`, `--bg-canvas`/`--text-primary`, `oklch`/`light-dark`, Dark $L = 0.16 \to 0.27$, zero arbitrários. |
| **2. Tipografia Fluida & WCAG AA** | `0.20` | `clamp()`, `65ch`, `balance/pretty`, `antialiased`, `font-synthesis: none`, zero `scale()` fracionário, $CR \ge 4.5:1$. |
| **3. Box Lógico, DOM & Nav 3 Camadas** | `0.15` | `border-box`, `flow-root`, DOM $\le 12$, `divsoup <= 0.45`, Breadcrumbs (`>= 3` níveis) e Ordem DOM = `Tab`. |
| **4. Iconografia 1:1 & Zero Emojis** | `0.15` | Ícones 1:1 (`16/20/24px`), família vetorial única (`stroke-width: 1.75`) e zero emojis. |
| **5. Luz Zenital, 3 Sombras & Isolation** | `0.15` | Umbra + Penumbra negativa + Catch-Light (`inset 0 1px 0 0`), Ambient Glow e `isolation: isolate`. |
| **6. `@container`, Cards & Motion** | `0.15` | Grid RAM, `@container`/`subgrid`, 4 variantes, `cubic-bezier(0.22, 1, 0.36, 1)`, `any-pointer: coarse` $\ge 48\text{px}$. |

```powershell
uv run python skills/frontend-ui-ux-auditor/scripts/ui_ux_frontend_auditor.py --target "<arquivo_ou_diretorio>"
```

## 4. Saídas e Entregáveis

- **Score Ponderado ($\text{Score}_{\text{UI/UX}} = \sum_{j=1}^{6} W_j \cdot S_j$):** Laudo estruturado por dimensão (`0..100`) e achados conforme [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).

## 5. Exceções, Limites e Quando NÃO Usar

- **Somente Backend ou Algoritmos:** Não use para queries SQL, gRPC ou testes unitários sem camada visual.
- **Estático vs. DOM Renderizado / Browser:** `ui_ux_frontend_auditor.py` é estático; para `take_snapshot`, `a11y` ou `chrome-devtools` / `agent-browser` `@eX` em runtime, combine com `auditoria-projetos-sistema` ou `complex-zero`.
- **Somente Leitura:** Apenas diagnostica e pontua; refatorações pertencem a `frontend-code-architect`.
