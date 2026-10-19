---
name: consultor-design-tatil-frontend
description: >-
  Fase 2 (Consultoria Interativa & Mockup): apresenta via ask_question os 4 presets Soft UI 135° (slate, moss, sapphire, obsidian), tipografia e geometria, gerando DESIGN.md v4.5-soft e mockup HTML. Não use para diagnóstico (Fase 1) nem refatoração (Fase 3).
license: MIT
metadata:
  version: "2.2.0"
  author: "FrontCraftMaster & Melki"
  category: "Consultoria de Design Tátil, Minimalist Impact e UX"
  updated_at: "2026-10-18"
  tags:
    - "consultoria-ux"
    - "minimalist-impact"
    - "soft-ui"
    - "scaffolding-frontend"
    - "design-md"
    - "anti-cobalto"
version: 2.2.0
updated_at: 2026-10-18
author: FrontCraftMaster & Melki
category: Consultoria de Design Tátil, Minimalist Impact e UX
authorized_sub_skills:
  - name: design-md
    role: "Geração e atualização do contrato canônico DESIGN.md v4.5-soft na raiz do projeto"
  - name: frontend-code-architect
    role: "Scaffolding modular src/ em 5 camadas de Design Atômico (v4.1.0)"
  - name: refatoracao-design-tatil-frontend
    role: "Fase 3 — Aplicação das escolhas aprovadas em todos os componentes do projeto"
---

# Fase 2: Consultoria Interativa, Scaffolding de Pastas e Mockup Tátil (`consultor-design-tatil-frontend` v2.2.0) 🎨

Motor consultivo e organizador estrutural (**Fase 2**) da esteira Frontend Melki. Recebe o diagnóstico da `analise-design-tatil-frontend`, **consulta as preferências do usuário via `ask_question`**, estrutura as pastas em 5 camadas de Design Atômico (`frontend-code-architect` v4.1.0) e entrega o **`DESIGN.md` (`v4.5-soft`)** + **Mockup HTML de Referência**.

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Quando o usuário pedir sugestões visuais, escolha interativa de paleta/tipografia Minimalist Impact (`ask_question`) ou geração de mockup HTML comparativo antes de refatorar.
- Automaticamente após a Fase 1 (`analise-design-tatil-frontend`) quando as escolhas estéticas ainda não estiverem fechadas.

### 🚫 Quando NÃO Usar
- Para inspeção estática/auditoria pura (use `analise-design-tatil-frontend`).
- Quando o preset já está definido e o usuário quer apenas refatorar o código das telas (use `refatoracao-design-tatil-frontend`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `project_root_path` (obrigatório): Caminho raiz do projeto frontend.
- `missing_structure_report` (opcional): Lista de pastas/arquivos faltantes detectados na Fase 1.
- `archetype_preference` (opcional, padrão `slate`): Um dos **4 Presets Soft UI (`slate`, `moss`, `sapphire`, `obsidian`)** documentados em [`references/paleta_estilo_melki.md`](references/paleta_estilo_melki.md).

---

## 🔄 Fluxo de Execução em 3 Passos

### Passo 1: Alinhamento Rápido via `ask_question` (`[DISC-OPCOES]`)
Caso o usuário não tenha fixado o tema/tipografia/arquétipo no prompt, apresente via `ask_question`:
1. **Preset Tonal Soft UI 135° (`[DISC-PALETA]`)**: `slate` (*Nexus Slate Cerulean* `#0284C7` — Recomendado), `moss` (*Biophilic Moss* `#2E6F40`), `sapphire` (*Ocean Sapphire* `#0369A1`) ou `obsidian` (*Phantom Obsidian 4K* `#38BDF8`).
2. **Arquétipo de Layout por Domínio (`[DISC-LAYOUT]`)**:
   - **`tactile-bento`** (*Tactile Raised Card* — Dashboards, SaaS e KPIs com `<SoftCard />` em relevo 135° sobre `--surface-raised: #F8FAFC`);
   - **`surface-well`** (*Surface Well* — Leitura longa, documentação e prontuários clínicos em cavidade `--surface-inset` sem fadiga visual);
   - **`split-pane-studio`** (*Split-Pane Studio* — IDEs, terminais e cockpits agênticos multi-painel com trilho `#sidebar-active-tracker`).
3. **Par Tipográfico (`[DISC-TATIL]`)**: `editorial-precision` (`Public Sans` + `Plus Jakarta Sans` + `JetBrains Mono`, escala `1.25` — Recomendado), `editorial-serif` (`Instrument Serif` + `Public Sans`) ou `swiss-grotesk` (`Space Grotesk` + `Public Sans`).
4. **Geometria**: `organic` (`24px` — Recomendado), `tactile` (`20px`) ou `technical` (`16px`).

### Passo 2: Scaffolding Automático em Design Atômico (`frontend-code-architect` v4.1 + `design-md` v4.5)
Com base na árvore raiz do projeto, crie imediatamente o que estiver ausente:
1. **`DESIGN.md` (`v4.5-soft` via `design-md`)**: Documentando a regra 60-30-10 e as 4+1 camadas tonais (`--surface-canvas`, `--surface-inset`, `--surface-flat`, `--surface-raised`, `--surface-contrast`).
2. **Estrutura de Pastas (`src/`)**: `components/ui/`, `components/bento/`, `components/layout/`, `config/tokens.ts`, `styles/globals.css` e `types/index.ts`.

### Passo 3: Mockup de Referência e Hand-off para a Fase 3 (`Topologia 3+1`)
- Gere `.context/mockup_tatil_referencia.html` baseado em [`../design-md/references/design_md_v4_5_studio.html`](../design-md/references/design_md_v4_5_studio.html) quando solicitado.
- Encaminhe o contrato aprovado para a **`refatoracao-design-tatil-frontend`** (Fase 3) e acione os 4 subagentes de UI (`ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer`) via `invoke_subagent` ou `franklin_execute_dag(plan_path_or_json="ui", target_dir="<project_root_path>")`.

---

## 🤖 Ativação de Agentes e Subagentes (`Topologia 3+1`)
- **Persona Coordenadora:** `FrontCraftMaster`
- **Subagentes Vinculados:** `ui-shell-navigator` (Onda 1), `ui-controls-data` (Onda 2A), `ui-motion-interaction` (Onda 2B) e `ui-deterministic-observer` (Onda 3 Gatekeeper).
- **Comandos de Disparo:** `invoke_subagent` ou `franklin_execute_dag(plan_path_or_json="ui", target_dir="<project_root_path>")`.

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
1. **Documento Canônico `DESIGN.md` (`v4.5-soft`)** criado/atualizado na raiz do projeto.
2. **Árvore de Pastas em Design Atômico Provisionada** com links clicáveis `file:///`.
3. **Matriz de Conformidade (`[DISC-PALETA]`, `[DISC-TATIL]`, `[DISC-OPCOES]`, `[DISC-SUPPLY]`)**.
