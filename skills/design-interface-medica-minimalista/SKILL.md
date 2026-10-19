---
name: design-interface-medica-minimalista
description: >-
  Preset e arquitetura exclusivamente clínica/hospitalar (PEP, receituários A4, triagem e calculadoras médicas com tabular-nums, alto contraste e zero emojis) guiada pelo propósito assistencial. Não use para apps gerais fora da área da saúde (use design-md, frontend-code-architect ou auditoria-projetos-sistema).
license: MIT
metadata:
  author: "FrontCraftMaster & Melki"
  version: "3.0.0"
  category: "Design System Clínico, MedTech & Impressão Hospitalar A4"
  updated_at: "2026-10-19"
  tags:
    - "medtech-ui"
    - "clinical-design"
    - "prontuario-eletronico"
    - "a4-print"
    - "tabular-nums"
version: 3.0.0
updated_at: 2026-10-19
author: FrontCraftMaster & Melki
category: Design System Clínico, MedTech & Impressão Hospitalar A4
---

# Design de Interface Médica Minimalista & Precisão Clínica (`design-interface-medica-minimalista` v3.0.0)

Diretrizes visuais, ergonômicas e de segurança assistencial para sistemas médicos, Prontuários Eletrônicos do Paciente (PEP), calculadoras clínicas e receituários A4. Adapta o estilo ao **propósito clínico** (consultório diurno, UTI/plantão noturno, laudos radiológicos ou prescrição impressa) priorizando **contraste impecável, espaçamento de leitura rápida, tipografia tabular e zero ruído cognitivo**.

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Criar ou refatorar telas de prontuário eletrônico (PEP), prescrição médica, evolução clínica, triagem ou calculadoras nefrológicas/cardiológicas/intensivas.
- Configurar folhas de estilo `@media print` para receituários, atestados, solicitações de exames e sumários de alta em formato **A4**.

### Quando NÃO Usar (Fronteira Estrita)
- Para aplicações SaaS gerais, e-commerce, jogos ou dashboards corporativos fora da área da saúde (use **`design-md`**, **`frontend-code-architect`** ou **`auditoria-projetos-sistema`**).
- Nunca delegue o cálculo matemático de doses ou escores clínicos a inferência livre do LLM — todo cálculo deve residir em função determinística tipada e testada (ou `agy_deterministic_calc_suite`).

---

## 📥 Entradas Esperadas
- `clinical_context` (obrigatório): Contexto assistencial (`ambulatorio_pep`, `uti_plantao_noturno`, `calculadora_doses`, `receituario_a4`).
- `target_stack` (opcional): React + TypeScript + Tailwind/CSS Variables ou HTML5/CSS3.

---

## ⚙️ Fluxo de Execução — Arquitetura Visual Guiada pelo Propósito Clínico

Consulte os tokens e templates detalhados em [`references/guia_tokens_clinicos_a4.md`](references/guia_tokens_clinicos_a4.md), o padrão [`../minimal-impact-ui/SKILL.md`](../minimal-impact-ui/SKILL.md) ([`atlas_ex_umbris_winui.html`](../minimal-impact-ui/references/atlas_ex_umbris_winui.html)) e [`../_template/references/preferencias_estilo_e_temas.md`](../_template/references/preferencias_estilo_e_temas.md):

### 1. Atmosferas Clínicas por Turno e Ambiente (3 Temas + Preset Esmeralda `#10B981`)
- **Enfermaria, Prontuário & Uso Prolongado (*Cinza sobre Cinza `#57545d` + Menus `#8e8999`*)**:
  - `--bg-canvas: #57545d`; `--bg-surface: #49464f`; `--bg-elevated: #635f6a`; `--bg-contrast-card: #232127`; menus `#8e8999` com tinta escura `#16151A`.
- **Ambulatório, Consultório Diurno & Impressão (*Ad Lucem Clínico*)**:
  - `--bg-canvas: #F3F3F5` / `#F4F6F8`; `--bg-surface: #FFFFFF`; `--bg-elevated: #E6E6EA`; `--ink-primary: #111115` (contraste AAA $\ge 14:1$).
- **Plantão Noturno / UTI / Laudos (*Preto Terminal IBM `Ex Umbris`*)**:
  - `--bg-canvas: #070709`; `--bg-surface: #101014`; `--bg-elevated: #18181E` acoplado a `IBM Plex Sans` + `IBM Plex Mono`.
- **Semântica Cromática Estrita & Nitidez Tipográfica (Zero Letras Vermelhas Embaçadas)**:
  - **Ação Clínica / Estabilidade (2%)**: Esmeralda Clínico (`#10B981` com texto escuro obrigatório `#062016` em botões preenchidos `.accent-bg`).
  - **Zero Letras Vermelhas Soltas no Cinza/Escuro**: Alertas e destaques usam `.accent-text` (texto `#FFFFFF` Semibold + fundo `--punctual-soft` + `border-left: 2.5px solid #e13535`) ou `.highlight-surgical` (sublinhado `2px`).

### 2. Tipografia Tabular, Unidades Inquebráveis & Zero Emojis
- **Proibição Absoluta de Emojis**: Interfaces clínicas usam exclusivamente ícones vetoriais **Lucide** (`stroke-width: 1.75`) ou marcadores técnicos monoespaçados.
- **Dados Numéricos & Doses (`tabular-nums` + `Compact Sizing`)**: Sinais vitais, escores (`SOFA`, `CHA2DS2-VASc`, `CKD-EPI`), tabelas SIGTAP/CID-10 e posologias usam `JetBrains Mono` / `IBM Plex Mono` com `font-variant-numeric: tabular-nums` e modo `Compact Sizing` (`py-1.5 px-2.5`).
- **Blindagem Anti-Squish de Unidades**: Unidades críticas (`mg/dL`, `mL/min/1.73m²`, `mcg/kg/min`, `mEq/L`) exigem `white-space: nowrap; flex-shrink: 0` e alvos interativos $\ge 44 \times 44\text{px}$.

### 3. Arquétipos Clínicos (`minimal-impact-ui`) e Folha A4 Proporcional (`Viewbox` & `@media print`)
- **Arquétipos Recomendados**: **01. Split-Screen Live Workbench** (`SplitView`: pílulas de exame físico/sinais vitais à esquerda + folha A4 APAC/LME/Evolução ao vivo à direita), **02. Linha do Tempo Cronológica** (`D1, D2, D3` de internação/antibiótico), **04. Árvore de Decisão Clínica** e **25. RichEditBox com Templates Clínicos** + `Popover Contextual` de doses.
- **Folha A4 Fiel (`Viewbox` 210x297mm)**: Renderizada em `#FFFFFF` com `--shadow-sculpted` sobre o palco `#57545d`, e regras `@media print` que ocultam `.no-print`/`header.nav-shell` e forçam fundo branco e tinta `#111115`.

---

## 📤 Saídas e Entregáveis
Componentes clínicos tipados (`.tsx` / `.html`), variáveis CSS com suporte a `@media print` A4 e verificação determinística via [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md) e `frontend-testing-auditor`.
