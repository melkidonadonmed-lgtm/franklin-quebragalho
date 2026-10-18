---
name: design-md
description: >-
  Sintetiza e gera o contrato canônico DESIGN.md (v4.5-soft — Minimalist Impact, Nexus Bento & Soft Tactile Architecture) na raiz de projetos frontend, documentando economia tonal 60-30-10, 4+1 camadas de elevação 135°, 8 kits Soft UI, Design Atômico em 5 camadas e paleta anti-cobalto.
version: "4.5.0"
license: MIT
metadata:
  author: "FrontCraftMaster & Melki"
  version: "4.5.0"
  category: "Design System Tátil, Minimalist Impact e Documentação Canônica"
  updated_at: "2026-10-18"
  tags:
    - "design-md"
    - "minimalist-impact"
    - "soft-ui"
    - "nexus-bento"
    - "anti-cobalto"
updated_at: 2026-10-18
author: FrontCraftMaster & Melki
category: Design System Tátil, Minimalist Impact e Documentação Canônica
authorized_sub_skills:
  - name: frontend-code-architect
    role: "Estruturação modular src/ em 5 camadas de Design Atômico e componentes Soft UI"
  - name: frontend-testing-auditor
    role: "Auditoria determinística FSM + Axe-Core (AUDIT-A11Y-01, AUDIT-VIS-01, AUDIT-STATE-01, AUDIT-SEC-01)"
---

# Gerador e Sintetizador Canônico de `DESIGN.md` (`design-md` v4.5.0 — Minimalist Impact & Soft Tactile) 📐

Utilitário especializado em inspecionar um projeto frontend (local em disco ou remoto no **Google Stitch MCP**) e sintetizar o arquivo **`DESIGN.md` (`v4.5-soft`)** na pasta raiz como fonte única da verdade (*Single Source of Truth*) sob o paradigma **Minimalist Impact, Nexus Bento & Soft Tactile Architecture**.

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Automaticamente quando **`analise-design-tatil-frontend`** (Fase 1), **`consultor-design-tatil-frontend`** (Fase 2) ou **`frontend-code-architect`** verificarem a raiz do projeto e notarem que o arquivo `DESIGN.md` ainda não existe ou precisa ser atualizado para `v4.5-soft`.
- Quando o usuário solicitar explicitamente a criação ou atualização do `DESIGN.md` de um projeto local ou do **Google Stitch** (`stitch*:*`).

### 🚫 Quando NÃO Usar (Limites e Exceções)
- Para scripts puramente backend/CLI sem interface gráfica.
- Nunca gere tokens com azul cobalto elétrico (`#0044FF`, `#0057FF`, `#1D4ED8`, `#233DFF`), glassmorphism (`backdrop-filter: blur`) ou bordas neon.

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `project_root_path` (obrigatório para projetos locais): Caminho absoluto da raiz onde o `DESIGN.md` será gravado.
- `stitch_project_id` (opcional): ID do projeto no Google Stitch MCP (`list_projects` / `get_screen` / `get_project`).
- `theme_preset` (opcional, padrão `slate`): Um dos 4 presets Soft UI (`slate` Cerulean `#0284C7`, `moss` Forest `#174930`, `sapphire` Ocean Sapphire `#1E6091` ou `obsidian` Dark `#38BDF8`) ou dos 22 temas minerais homologados.

---

## ⚙️ Fluxo de Síntese e Arquitetura (`v4.5-soft`)

### Passo 1: Varredura de Ativos e Economia Tonal 60-30-10
1. Inspecione `package.json`, `globals.css`, `tailwind.config.*`, `index.html` e as pastas da raiz (`src/components/ui/`, `src/components/bento/`, `src/components/layout/`, `src/config/`, `src/styles/`, `src/types/`).
2. Aplique a **Regra 60-30-10 Tonal Restrita**:
   - **60% `surface-canvas` (Layer 0)**: Fundo neutro contínuo (`#F1F4F8` no Light; `#12151B` / `#090B10` no Dark).
   - **30% Camadas de Elevação (Layers 1 a 3 + Layer 4 Contrast)**:
     - `Layer 1 (surface-inset)`: `#E5E9F0` com sombra interna dupla (`inset 4px 4px 10px rgba(166,180,200,0.45), inset -4px -4px 10px rgba(255,255,255,0.85)`) para campos de busca, inputs, trilhos e o berço deslizante do ícone ativo na sidebar (`#sidebar-active-tracker`).
     - `Layer 2 (surface-flat)`: `#E9EEF5` para agrupamento intermediário sem bordas duras de `1px`.
     - `Layer 3 (surface-raised / .ui-card-soft / .bento-card-soft)`: `#F1F4F8` / `#F8FAFC` esculpido com iluminação direcional dupla a **135°** (`8px 8px 20px rgba(166,180,200,0.42), -8px -8px 20px rgba(255,255,255,0.95)`).
     - `Layer 4 (surface-contrast / .terrixa-notched)`: `#1E293B` para âncoras de alto contraste por inversão tonal monocromática (sem neon).
   - **10% `--accent-point` (Acento Focal Único — Zero Cobalto)**: **Cerulean Sapphire** (`#0284C7`), **Ocean Sapphire** (`#1E6091`), **Moss Forest** (`#174930`) ou **Mineral Ice** (`#38BDF8` no dark mode).

### Passo 2: Integração com `frontend-code-architect` (v4.0) e `frontend-testing-auditor` (v2.5)
- Documente no `DESIGN.md` a hierarquia em **5 Camadas de Design Atômico** (Átomos, Moléculas, Organismos, Templates Bento 12 colunas e Pages/Views) e os invariantes de auditoria (`AUDIT-A11Y-01`, `AUDIT-VIS-01`, `AUDIT-STATE-01`, `AUDIT-SEC-01`).
- Referencie o estúdio interativo canônico em [`references/design_md_v4_5_studio.html`](references/design_md_v4_5_studio.html).

---

## 📤 Saídas e Entregáveis — Template Canônico (`<project_root>/DESIGN.md`)

```markdown
# DESIGN.md v4.5 — Minimalist Impact, Nexus Bento & Soft Tactile Architecture
---
version: "4.5-soft"
name: "Minimalist Tactile Prestige + Nexus Operations"
colors:
  surface-canvas: "#F1F4F8"     # Layer 0: Fundo neutro contínuo (60%)
  surface-flat:   "#E9EEF5"     # Layer 2: Placa intermediária sem borda dura
  surface-raised: "#F1F4F8"     # Layer 3: Placa esculpida neumórfica 135° (30%)
  surface-inset:  "#E5E9F0"     # Layer 1: Cavidade física (inputs/trilhos/berço de ícone ativo)
  surface-contrast: "#1E293B"   # Layer 4: Âncora de inversão tonal Terrixa
  text-primary:   "#1E293B"     # Grafite profundo legível (WCAG AA/AAA)
  text-secondary: "#64748B"     # Slate suave para metadados
  accent-point:   "#0284C7"     # Destaque focal Cerulean Sapphire (10% max — Zero Cobalto)
  accent-secondary: "#7DD3FC"   # Acento suave complementar
  accent-emerald: "#059669"     # Indicador semântico de estabilidade
lighting:
  soft-shadow:    "8px 8px 20px rgba(166, 180, 200, 0.42)"
  soft-highlight: "-8px -8px 20px rgba(255, 255, 255, 0.95)"
  inset-shadow:   "inset 4px 4px 10px rgba(166, 180, 200, 0.45), inset -4px -4px 10px rgba(255, 255, 255, 0.85)"
presets:
  slate:    { canvas: "#F1F4F8", raised: "#F1F4F8", inset: "#E5E9F0", accent: "#0284C7" }
  moss:     { canvas: "#F4F3EC", raised: "#F8F7F2", inset: "#E8E5DC", accent: "#174930" }
  sapphire: { canvas: "#F5F4EE", raised: "#FAF9F5", inset: "#E6E5DD", accent: "#1E6091" }
  obsidian: { canvas: "#12151B", raised: "#181D26", inset: "#0D1016", accent: "#38BDF8" }
skills_integrated:
  - frontend-code-architect (v4.0.0): Design Atômico em 5 camadas + src/ modular
  - frontend-testing-auditor (v2.5.0): Auditoria Axe-Core + FSM + Anti-Glassmorphism (AUDIT-VIS-01)
---

## 1. Pilha de Elevação Tonal (4+1 Camadas) e Iluminação 135°
- **Zero Glassmorphism / Zero Neon / Zero Bordas Duras 1px (`AUDIT-VIS-01`)**: Proibido `backdrop-filter: blur()`, brilhos neon ou azul cobalto (`#0044FF`, `#0057FF`, `#1D4ED8`).
- **Sidebar Tátil com Tracker de Ícone (`#sidebar-active-tracker`)**: Trilho colapsável (`272px` <-> `92px`) onde um berço escavado (`surface-inset`) com barra vertical de `4px` acompanha suavemente o ícone ativo via Scroll-Spy.
- **Inversão Tonal Terrixa (`.terrixa-notched`)**: Destaque de containers críticos por contraste monocromático (`surface-contrast: #1E293B`) e recorte chanfrado `28px`.

## 2. Tipografia e Escala Respirável (Grid 8pt / Gap >= 24px)
- **Display & Sans**: `Public Sans` / `Plus Jakarta Sans` (ou `Instrument Serif` no modo Editorial) com `line-height: 1.6`.
- **Monospace / Telemetria**: `JetBrains Mono` (`tabular-nums`).

## 3. Arquitetura Modular `src/` (Design Atômico em 5 Camadas)
- `src/components/ui/` — Átomos e Moléculas (`.ui-btn-tactile`, `.badge-soft`, `.activity-row`, `<SoftCard />`).
- `src/components/bento/` — Organismos Bento Grid (12 colunas, `gap: 1.75rem`).
- `src/components/layout/` — Tactile Companion Sidebar, Header Dock e Bottom Nav.
- `src/config/` — `tokens.ts` e `DESIGN.md`.
- `src/styles/` — `globals.css` e `theme.css`.
- `src/types/` — Contratos TypeScript estritos (`TonalLayer`, `ComponentFSMState`, `AuditTelemetryResult`).
```
