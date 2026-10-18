---
name: analise-design-tatil-frontend
description: >-
  Fase 1 (Inspector & Structural Scanner) da esteira de Frontend Tátil & Minimalist Impact Melki (DESIGN.md v4.5-soft). Varre a raiz do projeto frontend (detectando stack Next.js/React/Vite/HTML e mapeando pastas/arquivos faltantes como DESIGN.md, components/ui/, components/bento/, components/layout/, config/tokens.ts, styles/globals.css e types/), inspeciona a UI com os 4 subagentes de UI (Topologia 3+1) + frontend-testing-auditor (v2.5.0) e audita conformidade com Minimalist Impact (60-30-10 tonal, Soft UI 135°, zero cobalto/glassmorphism/neon).
license: MIT
metadata:
  version: "2.1.0"
  author: "FrontCraftMaster & Melki"
  category: "Design System Tátil, Minimalist Impact e Frontend"
  updated_at: "2026-10-18"
  tags:
    - "design-tatil"
    - "minimalist-impact"
    - "auditoria-ui"
    - "design-md"
    - "anti-cobalto"
    - "subagentes-ui-3+1"
version: 2.1.0
updated_at: 2026-10-18
author: FrontCraftMaster & Melki
category: Design System Tátil, Minimalist Impact e Frontend
authorized_sub_skills:
  - name: design-md
    role: "Síntese e criação automática do DESIGN.md v4.5-soft na raiz quando ausente"
  - name: frontend-code-architect
    role: "Padronização modular src/ em 5 camadas de Design Atômico (v4.0.0)"
  - name: frontend-testing-auditor
    role: "Auditoria determinística FSM + Axe-Core (AUDIT-A11Y-01, AUDIT-VIS-01, AUDIT-STATE-01, AUDIT-SEC-01)"
  - name: consultor-design-tatil-frontend
    role: "Fase 2 — Seleção interativa de tema (4 presets Soft UI + 22 paletas), mockup e scaffolding"
  - name: refatoracao-design-tatil-frontend
    role: "Fase 3 — Implementação prática nos componentes em 3 ondas (Topologia 3+1)"
---

# Fase 1: Inspeção Visual, Varredura da Raiz e Auditoria Frontend (`analise-design-tatil-frontend` v2.1.0 — Minimalist Impact & Soft Tactile) 🔍

Ponto de entrada (**Fase 1**) da esteira de UI/UX Tátil & Minimalist Impact Melki (`DESIGN.md v4.5-soft`). Une **varredura estrutural da pasta raiz do projeto** (detectando se faltam `DESIGN.md`, `components/ui/`, `components/bento/`, `components/layout/`, `config/tokens.ts`, `styles/globals.css`, `types/`) com **auditoria determinística de UI** (`frontend-testing-auditor` v2.5.0 + Google HTML/CSS Style Guide + 4 Módulos Táteis).

---

## 🔗 Esteira Encadeada de Frontend (Zero Sobreposição)

| Fase / Skill | Papel Exato |
| :--- | :--- |
| **Fase 1: `analise-design-tatil-frontend`** *(esta)* | Varre a raiz do projeto (pastas/arquivos faltantes), audita UI/HTML/CSS (`[PASS]/[FAIL]` + `AUDIT-VIS-01`) e aciona `design-md` (`v4.5-soft`) se faltar `DESIGN.md`. |
| **Fase 2: `consultor-design-tatil-frontend`** | Oferece opções via `ask_question` (4 presets Soft UI: *Nexus Slate Cerulean*, *Moss*, *Soft Sapphire*, *Obsidian Dark* + 22 temas), cria as pastas faltantes via `frontend-code-architect` e gera `DESIGN.md` + mockup. |
| **Fase 3: `refatoracao-design-tatil-frontend`** | Executa a refatoração de código em 3 ondas com os 4 subagentes (`ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer`) + `frontend-code-architect` (`v4.0.0`). |
| **Gatekeeper: `frontend-testing-auditor`** | Executa a suíte determinística `Jest/Vitest + RTL + Axe-Core` (`AUDIT-A11Y-01/02`, `AUDIT-VIS-01`, `AUDIT-STATE-01/02`, `AUDIT-SEC-01`) e calcula o Score ponderado (0–100). |

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Analisar ou auditar o frontend de um projeto, verificando tanto a **organização da pasta raiz (Design Atômico)** quanto a **qualidade visual/tátil (`Minimalist Impact v4.5-soft`)**.
- Diagnosticar o que falta na estrutura do projeto (`DESIGN.md`, `components/ui/`, `components/bento/`, `components/layout/`, `config/`, `styles/`, `types/`) antes de iniciar uma refatoração.
- Validar conformidade com o **Google HTML/CSS Style Guide**, **Minimalist Impact (`v4.5-soft`)** e **Banimento Estrito de Azul Cobalto**.

### Quando NÃO Usar
- Para aplicar diretamente mutações em lote nos componentes sem levantar o diagnóstico inicial (use `refatoracao-design-tatil-frontend` após esta análise).
- Para auditoria exclusiva de backend sem interface (use `auditoria-projetos-sistema`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `project_root_path` (obrigatório): Caminho da pasta raiz do projeto frontend a ser inspecionado.
- `target_url` (opcional): URL ativa (`http://localhost:3000`, `:5173`, `:8080`) para inspeção ao vivo via `agent-browser`.
- `auto_scaffold_missing` (opcional, padrão `true`): Quando `true`, ao detectar ausência de `DESIGN.md` ou pastas base, aciona `design-md` e `frontend-code-architect` para estruturá-los.

---

## ⚙️ Fluxo de Execução em 3 Passos

### Passo 1: Varredura da Pasta Raiz e Auditoria de Design Atômico (`frontend-code-architect` v4.0)
Inspecione a raiz do projeto (`package.json`, `tsconfig.json`, `index.html`, `app/` ou `src/`) e verifique a árvore canônica:

| Camada Estrutural | Next.js / React / Vite (`src/` ou `app/`) | HTML5 / CSS / Vanilla JS | Ação se Ausente (`[MISSING]`) |
| :--- | :--- | :--- | :--- |
| **1. Manifesto de Design** | `DESIGN.md` (`v4.5-soft` na raiz/config) | `DESIGN.md` (na raiz) | **Acionar `design-md`** para sintetizar e criar o `DESIGN.md v4.5-soft` imediatamente. |
| **2. Átomos & Moléculas** | `components/ui/` (`SoftCard.tsx`, botões, inputs) | `components/ui/` | Criar diretório e mapear componentes monolíticos da raiz para extração. |
| **3. Organismos & Layout** | `components/bento/` + `components/layout/` | `components/layout/` | Isolar Bento Grid (12 colunas) e Tactile Companion Sidebar (`#sidebar-active-tracker`). |
| **4. Tokens & Estilos** | `config/tokens.ts` + `styles/globals.css` + `styles/theme.css` | `css/themes.css` + `css/style.css` | Injetar tokens `v4.5-soft` (`--surface-canvas`, `--surface-raised`, `--surface-inset`, `--accent-point: #0284C7`). |
| **5. Contratos & Domínio** | `types/index.ts` + `modules/` + `lib/utils.ts` | `js/modules/` + `js/utils/` | Centralizar tipos (`TonalLayer`, `ComponentFSMState`) e helpers (`<= 300` linhas/arquivo). |

### Passo 2: Auditoria Minimalist Impact (`v4.5-soft`), 4 Módulos Táteis e `AUDIT-VIS-01`
Avalie o código e/ou a página renderizada emitindo `[PASS]` ou `[FAIL]`:
1. **`[DISC-PALETA]` (Regra 60-30-10 & Anti-Cobalto)**:
   - **Banimento Estrito de Azul Cobalto**: Proibido `#0044FF`, `#0057FF`, `#233DFF`, `#1D4ED8` e neon saturado.
   - **Acentos Autorizados**: **Cerulean Sapphire** (`#0284C7`), **Ocean Sapphire** (`#1E6091`), **Moss Forest** (`#174930`), **Mineral Ice** (`#38BDF8`) e os 22 temas minerais homologados.
2. **`[DISC-TATIL]` & `AUDIT-VIS-01` (4+1 Camadas Tonais, Iluminação 135° e Ergonomia)**:
   - **Zero Glassmorphism / Zero Bordas Duras 1px**: Zero `backdrop-filter: blur`; exigir elevação por sombras duplas a 135° (`.ui-card-soft` / `.bento-card-soft`), cavidades `surface-inset` (para busca, inputs e berço do ícone ativo na sidebar `#sidebar-active-tracker`), inversão tonal `.terrixa-notched` (`surface-contrast`) e $L_{\text{card}} > L_{\text{canvas}}$ no dark mode.
   - **Ergonomia de Clique e Anti-Squish**: Botões $\ge 40\text{px}$ (`44px` ideal) com `flex-shrink: 0; white-space: nowrap;`, sidebar $\ge 240\text{px}..272\text{px}$ (colapsável para `92px`), respiro amplo (`gap >= 24px`) e atalho `Ctrl+K`.
3. **`[DISC-OPCOES]` & `[DISC-SUPPLY]`**:
   - Uso de `shadcn/ui`, `Radix UI`, `Lucide Icons` (`stroke-width: 1.5px..2px`), `Tailwind CSS` e tipografia `Public Sans` / `Plus Jakarta Sans` + `Instrument Serif` + `JetBrains Mono`.
4. **Rubrica `frontend-testing-auditor` (`v2.5.0`) + Google HTML/CSS Style Guide**:
   - Checagem de `AUDIT-A11Y-01/02` (Axe-Core + foco teclado), `AUDIT-VIS-01` (zero blur), `AUDIT-STATE-01/02` (FSM `Idle/Loading/Error/Pressed`) e `AUDIT-SEC-01` (anti-XSS).

### Passo 3: Despacho de Subagentes (`Topologia 3+1`) e Hand-off Automático
- Acione via `invoke_subagent` (ou `franklin_execute_dag`):
  - **Onda 1**: `ui-shell-navigator` (4+1 Tonal Layers, Nexus Bento 12 cols, Tactile Companion Sidebar `#sidebar-active-tracker`, CLS $< 0.1$).
  - **Onda 2**: `ui-controls-data` (5 Camadas Atômicas, 8 Kits Soft UI, 44px anti-squish, WAI-ARIA) + `ui-motion-interaction` (Spring physics `--ease-spring`, `:active -> surface-inset`, `prefers-reduced-motion`).
  - **Onda 3**: `ui-deterministic-observer` (Checklist `[AUDIT-01..09]` + rubrica `frontend-testing-auditor` $0.35\cdot\text{A11y} + 0.30\cdot\text{FSM} + 0.20\cdot\text{Tokens} + 0.15\cdot\text{Sec}$).

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
1. **Mapa Estrutural da Raiz (`[OK]` vs `[MISSING]`)**: Diagnóstico de `DESIGN.md v4.5-soft` e das 5 camadas de Design Atômico.
2. **Matriz Determinística de Discrepâncias (`[DISC-PALETA]`, `[DISC-TATIL]`, `[DISC-OPCOES]`, `[DISC-SUPPLY]`)** + Score `frontend-testing-auditor` (`0–100`).
3. **Hand-off Executável**: Criação do `DESIGN.md` (`v4.5-soft`) e plano pronto para a Fase 2 (`consultor-design-tatil-frontend`) ou Fase 3 (`refatoracao-design-tatil-frontend`).
