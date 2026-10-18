---
name: consultor-design-tatil-frontend
description: >-
  Fase 2 (Interactive Design Consultant, Folder Scaffolder & Mockup Architect) da esteira de Frontend Tátil & Minimalist Impact Melki (DESIGN.md v4.5-soft). Apresenta opções interativas via ask_question (4 presets Soft UI 135° sem cobalto: Nexus Slate Cerulean, Moss, Soft Sapphire, Obsidian Dark + 22 temas minerais, pares tipográficos Public Sans / Plus Jakarta / Instrument Serif e geometrias), estrutura as pastas em Design Atômico via frontend-code-architect (v4.0) e gera DESIGN.md v4.5-soft + mockup HTML.
license: MIT
metadata:
  version: "2.1.0"
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
version: 2.1.0
updated_at: 2026-10-18
author: FrontCraftMaster & Melki
category: Consultoria de Design Tátil, Minimalist Impact e UX
authorized_sub_skills:
  - name: design-md
    role: "Geração e atualização do contrato canônico DESIGN.md v4.5-soft na raiz do projeto"
  - name: frontend-code-architect
    role: "Scaffolding modular src/ em 5 camadas de Design Atômico (v4.0.0)"
  - name: refatoracao-design-tatil-frontend
    role: "Fase 3 — Aplicação das escolhas aprovadas em todos os componentes do projeto"
---

# Fase 2: Consultoria Interativa, Scaffolding de Pastas e Mockup Tátil (`consultor-design-tatil-frontend` v2.1.0 — Minimalist Impact & Soft UI) 🎨

Motor consultivo e organizador estrutural (**Fase 2**) da esteira Frontend Melki. Recebe o diagnóstico da `analise-design-tatil-frontend`, **consulta as preferências do usuário via `ask_question`**, **organiza as pastas em 5 camadas de Design Atômico** (`DESIGN.md v4.5-soft`, `styles/`, `components/ui/`, `components/bento/`, `components/layout/`, `config/`, `types/`) e entrega o **`DESIGN.md`** + **Mockup HTML de Referência**.

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Quando o usuário pedir sugestões visuais, escolha de paleta/tipografia Minimalist Impact, criação de `DESIGN.md v4.5-soft` ou organização das pastas base do frontend.
- Automaticamente após a `analise-design-tatil-frontend` detectar que o projeto não possui `DESIGN.md`, tokens de superfície tátil ou pastas de componentes organizadas.
- Para gerar um protótipo/mockup comparativo baseado no estúdio `DESIGN.md v4.5` antes de refatorar todo o código.

### Quando NÃO Usar
- Para inspeção estática/auditoria pura sem proposição de design (use `analise-design-tatil-frontend`).
- Quando o `DESIGN.md` e as escolhas já estão definidas e o usuário quer apenas refatorar o código das telas (use `refatoracao-design-tatil-frontend`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `project_root_path` (obrigatório): Caminho raiz do projeto frontend.
- `missing_structure_report` (opcional): Lista de pastas/arquivos faltantes detectados na Fase 1.
- `archetype_preference` (opcional, padrão `slate`): Um dos **4 Presets Soft UI (`v4.5-soft`)** ou dos **22 temas homologados (`v2.6.0-2026`)**.

---

## ⚙️ Diretrizes Minimalist Impact (`v4.5-soft`) + 4 Módulos Táteis Melki

### 1. Módulo de Paleta Tonal 60-30-10 & Banimento de Cobalto (`[DISC-PALETA]`)
- **4 Presets Soft UI (`DESIGN.md v4.5-soft`)**:
  1. `slate` (**Nexus v4.5 Slate Prestige**): Canvas `#F1F4F8`, Raised `#F1F4F8`, Inset `#E5E9F0`, Contrast `#1E293B`, Accent **Cerulean Sapphire** `#0284C7` + Emerald `#059669`.
  2. `moss` (**Moss & Calm System**): Canvas `#F4F3EC`, Raised `#F8F7F2`, Inset `#E8E5DC`, Contrast `#1A2E22`, Accent **Forest Moss** `#174930`.
  3. `sapphire` (**Soft Sapphire System**): Canvas `#F5F4EE`, Raised `#FAF9F5`, Inset `#E6E5DD`, Contrast `#1E293B`, Accent **Ocean Sapphire** `#1E6091` + Glacier Sky `#69ADC6`.
  4. `obsidian` (**Obsidian Dark Tactile**): Canvas `#12151B`, Raised `#181D26`, Inset `#0D1016`, Contrast `#F1F4F8`, Accent **Mineral Ice** `#38BDF8`.
- **Catálogo de 22 Temas Minerais**: Inclui `tactile-matte` (`#090B10`/`#141824`), `phantom-4k`, `quiet-luxury-titanium`, `steadfast-stainless`, `warm-editorial-paper` e `polar-sand`.
- **Regra Anti-Cobalto**: Proibido azul cobalto puro/elétrico (`#0044FF`, `#0057FF`, `#233DFF`, `#1D4ED8`) e cores neon.

### 2. Módulo de Elevação Tonal (4+1 Camadas), Tipografia e Geometria (`[DISC-TATIL]`)
- **Superfícies e Luz 135°**: Zero `backdrop-filter: blur` e zero bordas duras de `1px`. Iluminação direcional dupla a 135° (`8px 8px 20px rgba(166,180,200,0.42), -8px -8px 20px rgba(255,255,255,0.95)`), cavidades escavadas `surface-inset` (`inset 4px 4px 10px ...`), inversão tonal `.terrixa-notched` (`surface-contrast`) e $L_{\text{card}} > L_{\text{canvas}}$ no dark mode.
- **Sidebar Tátil com Tracker de Ícone (`#sidebar-active-tracker`)**: Trilho colapsável (`272px` $\leftrightarrow$ `92px`) com berço `surface-inset` e barra vertical de `4px` que acompanha o ícone ativo via Scroll-Spy.
- **Pares Tipográficos (`TYPOGRAPHY_PRESETS`)**:
  1. `nexus-sans` / `humanist-tech`: `Public Sans` / `Plus Jakarta Sans` + `JetBrains Mono` (`line-height: 1.6`)
  2. `editorial-serif`: `Instrument Serif` + `Public Sans` / `Plus Jakarta Sans` + `JetBrains Mono`
  3. `swiss-grotesk`: `Space Grotesk` + `Inter` + `JetBrains Mono`
  4. `classic-garamond`: `Cormorant Garamond` + `Plus Jakarta Sans` + `JetBrains Mono`
- **Geometrias (`GEOMETRY_PRESETS`)**: Squircle contínuo (`--rounded-sm: 10px`, `--rounded-md: 16px`, `--rounded-lg: 24px`, `--rounded-pill: 9999px`).

### 3. Módulo de Opções Interativas e Supply Chain (`[DISC-OPCOES]` & `[DISC-SUPPLY]`)
- **Consulta via `ask_question`**: Apresente opções diretas de preset (`Nexus Slate Cerulean`, `Moss`, `Soft Sapphire`, `Obsidian Dark`), par tipográfico e estrutura de pastas.
- **Supply Chain Copy-Paste**: `shadcn/ui`, `Radix UI`, `Lucide Icons` e `Tailwind CSS`.

---

## 🔄 Fluxo de Execução em 3 Passos

### Passo 1: Alinhamento Rápido via `ask_question`
Caso o usuário não tenha fixado o tema/tipografia no prompt, apresente via `ask_question` as recomendações calibradas para o domínio do projeto.

### Passo 2: Scaffolding Automático em Design Atômico (`frontend-code-architect` v4.0 + `design-md` v4.5)
Com base na árvore raiz do projeto, crie imediatamente o que estiver ausente:
1. **`DESIGN.md` (`v4.5-soft` via `design-md`)**: Documentando a regra 60-30-10, as 4+1 camadas tonais, iluminação 135° e paleta sem cobalto.
2. **Estrutura de Pastas (`src/`)**:
   - `styles/globals.css` e `styles/theme.css`.
   - `components/ui/` (`SoftCard.tsx`, botões `.ui-btn-tactile`, badges `.badge-soft`, inputs `surface-inset`), `components/bento/` e `components/layout/`.
   - `config/tokens.ts` e `types/index.ts`.

### Passo 3: Mockup de Referência e Hand-off para a Fase 3
- Gere `.context/mockup_tatil_referencia.html` baseado em `skills/design-md/references/design_md_v4_5_studio.html` quando solicitado.
- Entregue o contrato pronto para execução pela **`refatoracao-design-tatil-frontend`** (Fase 3).

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
1. **Documento Canônico [`DESIGN.md`](file:///DESIGN.md) (`v4.5-soft`)** criado/atualizado na raiz do projeto.
2. **Árvore de Pastas em Design Atômico Provisionada**: Links clicáveis `file:///` para `components/ui/`, `components/bento/`, `components/layout/`, `config/`, `styles/` e `types/`.
3. **Matriz de Conformidade (`[DISC-PALETA]`, `[DISC-TATIL]`, `[DISC-OPCOES]`, `[DISC-SUPPLY]`)**.
