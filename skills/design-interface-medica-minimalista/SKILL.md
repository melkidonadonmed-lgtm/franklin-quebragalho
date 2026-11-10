---
name: design-interface-medica-minimalista
description: "Arquitetura para interfaces clínicas, prontuários eletrônicos PEP, receituários e laudos A4 .sus-grid e calculadoras médicas. Use para sistemas de saúde; não use para SaaS genérico."
version: "5.0.0"
updated_at: "2026-10-27"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "5.0.0"
  updated_at: "2026-10-27"
  author: "Melki"
  category: "Design System Clínico, MedTech & Impressão Vetorial A4"
  tags: ["medtech-ui", "clinical-design", "prontuario-eletronico", "a4-print", "tabular-nums"]
---
# Design de Interface Médica Minimalista & Precisão Clínica (`design-interface-medica-minimalista` v5.0.0)

Diretrizes visuais, ergonômicas e de segurança assistencial para sistemas médicos, Prontuários Eletrônicos do Paciente (PEP), calculadoras clínicas e receituários/laudos vetoriais A4. Adapta a polaridade e a composição ao **propósito assistencial** (consultório diurno, UTI/plantão noturno, laudos diagnósticos ou prescrição impressa) sob os **9 Eixos do SSOT canônico** (Box Lógico e Anti-Colapso, Tipografia Fluida e Anti-Borrão GPU, Cores `OKLCH` + `light-dark()`, Tokens em 3 Camadas, Sombras Multi-Camadas em 3 Níveis, Macrolayouts vs. Microlayouts `@container`, 4 Variantes de Cards, Navegação Semântica em 3 Camadas e Engenharia Real-State).

---

## 🎯 Gatilhos de Ativação (Quando Usar)

- Criar ou refatorar telas de prontuário eletrônico (PEP), prescrição médica, evolução clínica, triagem ou calculadoras nefrológicas, cardiológicas e intensivas.
- Projetar folhas vetoriais de impressão (`@media print` / A4 `210mm × 297mm`) para receituários, APAC/LME, atestados, solicitações de exames e sumários de alta usando **100% CSS Grid vetorial e SVG**.

### Quando NÃO Usar (Fronteira Estrita)

- Para aplicações SaaS gerais, e-commerce, jogos ou dashboards corporativos fora da área da saúde (use **`design-md`**, **`frontend-code-architect`** ou **`auditoria-projetos-sistema`**).
- Nunca delegue o cálculo matemático de doses, infusões ou escores clínicos a inferência livre do LLM — todo cálculo deve residir em função determinística tipada e testada (ou `agy_deterministic_calc_suite`).

---

## 📥 Entradas Esperadas

- `clinical_context` (obrigatório): Contexto assistencial (`ambulatorio_pep`, `uti_plantao_noturno`, `calculadora_doses`, `receituario_a4`).
- `target_stack` (opcional): React + TypeScript + Tailwind v4/CSS Variables ou HTML5/CSS3 standalone.

---

## ⚙️ Fluxo de Execução — Arquitetura Visual Guiada pelo Propósito Clínico (9 Eixos)

Consulte os tokens e templates detalhados em [`references/guia_tokens_clinicos_a4.md`](references/guia_tokens_clinicos_a4.md) e o contrato [`../design-md/SKILL.md`](../design-md/SKILL.md):

### 1. Polaridades Clínicas por Ambiente, Tokens em 3 Camadas `OKLCH`, Luz Zenital e Sombras Multi-Camadas (Eixos 3, 4 & 5)

- **Papéis Semânticos de Superfície (`--bg-*` / `--surface-*` e `light-dark()`)**:
  - **Consultório Diurno & Impressão (`[data-theme="clinical-day"]`)**: `--bg-canvas` / `--surface-canvas: oklch(0.97 0.005 245)` (`#F4F6F8`); `--surface-sunken: oklch(0.95 0.006 245)` (`#ECEFF3`); `--bg-surface-1` / `--surface-card: oklch(1 0 0)` (`#FFFFFF`); `--text-primary` / `--ink-primary: oklch(0.18 0.02 255)` (`#0F172A`, contraste WCAG AAA $\ge 14:1$).
  - **Plantão Noturno / UTI / Laudos (`[data-theme="clinical-night"]`)**: Elevação progressiva de luminosidade (zero `#000000` puro para prevenir *OLED smearing*): `--bg-canvas` / `--surface-canvas: oklch(0.16 0.015 255)` (`#0B0E14`); `--bg-surface-1` / `--surface-card: oklch(0.21 0.018 255)` (`#121721`); `--bg-surface-2` / `--surface-elevated: oklch(0.26 0.02 255)` (`#181F2C`); `--text-primary` / `--ink-primary: oklch(0.96 0.005 245)` (`#F1F5F9`).
- **Iluminação Zenital (90°–120°) e Elevação em 3 Níveis**:
  - Cards clínicos e painéis ativos recebem `Top Catch-Light` (`inset 0 1px 0 0`) e sombras multi-camadas (`--shadow-elevation-1..3` / `--elevation-1..3`). Campos de entrada de sinais vitais e prescrição usam recesso físico (`--surface-sunken` + `--shadow-inset: inset 0 2px 4px 0 oklch(0 0 0 / 0.08)`).
- **Destaque Acromático, 4 Variantes de Cards e Semântica Clínica Contida**:
  - Ações primárias usam contraste acromático de alto impacto (`#0F172A` no claro / `#F8FAFC` no escuro).
  - Use as **4 Variantes Funcionais de Cards (Eixo 7)**: *Elevated* (resumo do paciente/alerta ativo), *Outlined* (tabelas laboratoriais/evolução), *Filled/Subtle* (histórico/sinais vitais secundários) e *Interactive* (seleção de protocolo/calculadoras).
  - Indicadores de status (estabilidade, atenção farmacêutica, alerta crítico/alergia) usam micro-dots de `6px`, borda lateral lógica `border-inline-start: 2px solid` ou badges translúcidos (`color-mix(in oklab, ...)`) com texto neutro de alto contraste (`--ink-primary`).

### 2. Box Lógico, Nitidez Tipográfica Anti-Borrão, Unidades Inquebráveis & Zero Emojis (Eixos 1 & 2)

- **Box Lógico e Anti-Colapso**: Use propriedades lógicas (`inline-size`, `padding-inline`, `margin-block`), `display: flow-root` e `gap` no elemento pai.
- **Travas de Renderização e Anti-Borrão GPU**: Aplique `-webkit-font-smoothing: antialiased`, `text-rendering: optimizeLegibility`, `font-synthesis: none`, largura de leitura `max-inline-size: 65ch` em notas de evolução e proíba `scale()` fracionário em contêineres de texto (use `translateY(-1px)` no hover e `translateY(0px)` no active).
- **Proibição Absoluta de Emojis**: Interfaces clínicas usam exclusivamente ícones vetoriais **Lucide** (`stroke-width: 1.75`) ou marcadores técnicos monoespaçados.
- **Dados Numéricos & Doses (`tabular-nums`)**: Sinais vitais, escores (`SOFA`, `CHA2DS2-VASc`, `CKD-EPI`), tabelas SIGTAP/CID-10 e posologias usam `JetBrains Mono` / `IBM Plex Mono` com `font-variant-numeric: tabular-nums`.
- **Blindagem Anti-Squish de Unidades**: Unidades críticas (`mg/dL`, `mL/min/1.73m²`, `mcg/kg/min`, `mEq/L`) exigem `white-space: nowrap; flex-shrink: 0` e alvos interativos $\ge 44 \times 44\text{px}$.

### 3. Arquétipos Espaciais Clínicos, `@container`, Navegação em 3 Camadas e Folha Vetorial A4 (Eixos 6 & 8)

- **Macrolayouts (`@media`) & Microlayouts (`@container`)**: Combine **1. Workbench Split-View** (parâmetros clínicos à esquerda + folha A4/laudo ao vivo à direita) ou **3. Command Center / Data Grid de Alta Densidade** com `container-type: inline-size` + `@container` nos cards de sinais vitais e prescrição.
- **Navegação Semântica em 3 Camadas**: Global (`<nav aria-label="Menu clínico principal">`), Local (`<nav aria-label="Seções do prontuário">`) e Breadcrumbs (`<nav aria-label="Caminho de navegação"><ol role="list">` + `aria-current="page"`).
- **Folha Vetorial A4 (`210mm × 297mm`)**: Construída com **100% CSS Grid vetorial e SVG**, exibida em tela sobre `--surface-canvas` com `--shadow-elevation-2`, e em `@media print` ocultando `.no-print`/`nav`/`aside`, removendo sombras e garantindo fidelidade milimétrica para exportação PDF.

---

## 📤 Saídas e Entregáveis

Componentes clínicos tipados (`.tsx` / `.html`) com estado real e validação fisiológica determinística, variáveis CSS com `@media print` A4 vetorial e verificação via [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md) e `frontend-testing-auditor`.
