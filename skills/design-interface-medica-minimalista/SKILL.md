---
name: design-interface-medica-minimalista
description: >-
  Preset clínico especializado (Nexus Slate Cerulean / Moss / Soft Sapphire / Polar Sand) para prontuários eletrônicos, receituários A4, calculadoras médicas e SaaS de saúde, integrado ao Minimalist Impact & Soft Tactile Architecture (DESIGN.md v4.5-soft). Use quando o usuário pedir o desenvolvimento, análise ou refatoração de interfaces médicas, clínicas ou laboratoriais sem azul cobalto.
license: MIT
metadata:
  version: "2.1.0"
  author: "Franklin-Main & Melki"
  category: "Design de Interface Médica Minimalista & Soft UI"
  updated_at: "2026-10-18"
  tags:
    - "saude"
    - "clinico"
    - "prontuario"
    - "minimalist-impact"
    - "soft-ui"
    - "anti-cobalto"
version: 2.1.0
updated_at: 2026-10-18
author: Franklin-Main & Melki
category: Design de Interface Médica Minimalista & Soft UI
authorized_sub_skills:
  - name: design-md
    role: "Criação automática do DESIGN.md v4.5-soft clínico na raiz do projeto quando ausente"
  - name: frontend-code-architect
    role: "Estruturação modular src/ em 5 camadas de Design Atômico (v4.0.0)"
  - name: frontend-testing-auditor
    role: "Auditoria determinística FSM + Axe-Core (v2.5.0) para segurança clínica"
---

# Design System Médico Executivo & Minimalist Impact (`design-interface-medica-minimalista` v2.1.0 — Soft Tactile `v4.5-soft`) 🩺

Preset de domínio clínico do **Minimalist Impact & Soft Tactile Architecture (`DESIGN.md v4.5-soft`)**, calibrado para alta legibilidade em plantões, zero fadiga visual, elevação por camadas tonais a 135°, precisão numérica (`tabular-nums`) e impressão limpa em papel A4.

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Criar, auditar ou refatorar telas de prontuários eletrônicos (PEP), calculadoras médicas (ex.: clearance renal, déficit de água livre, infusão), receituários ou laudos.
- Configurar a árvore de pastas de um app médico (`DESIGN.md v4.5-soft`, `components/ui/SoftCard.tsx`, `styles/globals.css`, `modules/calculadoras/`, `lib/utils/`).

### Quando NÃO Usar
- Para cockpits de infraestrutura fora da área da saúde (use a esteira `analise-design-tatil-frontend` $\rightarrow$ `consultor-design-tatil-frontend` $\rightarrow$ `refatoracao-design-tatil-frontend`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
1. **Domínio ou Caso de Uso Clínico**: Prontuário, calculadora médica, prescrição ou painel hospitalar.
2. **Caminho Raiz do Projeto (`project_root_path`)**: Para verificar/criar `DESIGN.md v4.5-soft` e organizar as pastas em Design Atômico.
3. **Preset Tonal Clínico**: `slate` (Nexus Slate Cerulean `#F1F4F8` / `#0284C7`), `sapphire` (Soft Sapphire `#F5F4EE` / `#1E6091`), `moss` (Calm Moss `#F4F3EC` / `#174930`) ou `obsidian` (Plantão Noturno `#12151B` / `#181D26` / `#38BDF8`).

---

## 🔄 Processamento, Fluxo e Arquitetura Clínica + Minimalist Impact (`v4.5-soft`)

### 1. Paleta Clínica Tonal 60-30-10 (`[DISC-PALETA]`)
- **Zero Azul Cobalto ou Neon**: Proibido `#0044FF`, `#0057FF`, `#233DFF`, `#1D4ED8`, `#0000FF` ou `#00FF00`.
- **Camadas Tonais 135° (Diurno Clínico)**:
  - `60%` `surface-canvas`: `#F1F4F8` (Slate) ou `#F5F4EE` (Warm Ivory).
  - `30%` `surface-raised` (`.ui-card-soft` com sombra dupla 135°) e `surface-inset` (`#E5E9F0` para inputs de dose/peso/idade e busca).
  - `10%` `--accent-point`: **Cerulean Sapphire** (`#0284C7`), **Ocean Sapphire** (`#1E6091`) ou **Clinical Emerald/Moss** (`#059669` / `#174930`).
- **Tema Escuro Plantão (`obsidian` / `tactile-matte`)**: Canvas `#12151B` / `#090B10`, Cards `#181D26` / `#141824` ($L_{\text{card}} > L_{\text{canvas}}$) e acento **Mineral Ice** (`#38BDF8`).

### 2. Ergonomia Tátil, Tipografia e Anti-Squish (`[DISC-TATIL]` & `AUDIT-VIS-01`)
- **Zero Emojis na UI Clínica**: Utilize exclusivamente ícones vetoriais **Lucide Icons** (`stroke-width="1.5"`).
- **Alvos Ergonômicos e Anti-Squish**: Botões e selects com altura mínima de **`44px`**, `flex-shrink: 0; white-space: nowrap;` (nunca quebrar rótulos de ação ou unidades como `mg/dL`, `mL/min` ou `mEq/L`).
- **Tipografia de Precisão**: `Public Sans` / `Plus Jakarta Sans` para leitura rápida (`line-height: 1.6`) e `JetBrains Mono` (`tabular-nums`) para doses, resultados laboratoriais e fórmulas.
- **Anti-Glassmorphism**: Zero `backdrop-filter: blur` e zero bordas duras de `1px`.

### 3. Design Atômico, Cálculos Determinísticos e Auditoria FSM (`[DISC-OPCOES]` & `[DISC-SUPPLY]`)
- Ao inspecionar o projeto médico, se não houver `DESIGN.md` na raiz, acione **`design-md`** (`v4.5-soft`) e **`frontend-code-architect`** (`v4.0.0`).
- Para cálculos médicos, delegue a aritmética para funções determinísticas testadas (ou `agy_deterministic_calc_suite`), nunca deixando o LLM calcular doses de cabeça.
- Audite os estados `Idle`, `Loading` (`role="status"`), `Error` (`role="alert"`) e sanitização XSS com **`frontend-testing-auditor`** (`v2.5.0`).

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
1. **Estrutura Raiz e `DESIGN.md v4.5-soft`**: Confirmação da criação de `DESIGN.md`, `components/ui/SoftCard.tsx`, `styles/globals.css` e `modules/`.
2. **Componentes Clínicos Tipados**: Código sem emojis e sem cobalto, com alvos de `44px` anti-squish, números `tabular-nums` e CSS `@media print` calibrado para folha A4.
3. **Matriz de Conformidade (`[DISC-PALETA]`, `[DISC-TATIL]`, `[DISC-OPCOES]`, `[DISC-SUPPLY]`)** + Score `frontend-testing-auditor`.
