---
name: design-md
description: >-
  Gera ou atualiza o arquivo de contrato DESIGN.md na raiz do projeto ou via Google Stitch, selecionando o tema, atmosfera, tipografia, espaçamento, contraste e camadas de acordo com o propósito do projeto (Conversão/SaaS, Editorial, FinTech, IA Nativa/AETHER, MedTech ou Terminal IBM Ex Umbris), sem impor paletas de cores fixas. Não use para auditar repositório completo (use auditoria-projetos-sistema).
version: "5.0.0"
license: MIT
metadata:
  author: "FrontCraftMaster & Melki"
  version: "5.0.0"
  category: "Design System Adaptativo por Propósito, Arquitetura Visual e Documentação Canônica"
  updated_at: "2026-10-19"
  tags:
    - "design-md"
    - "estilo-por-proposito"
    - "ex-umbris-ad-lucem"
    - "aether-2027"
    - "arquitetura-visual"
updated_at: 2026-10-19
author: FrontCraftMaster & Melki
category: Design System Adaptativo por Propósito, Arquitetura Visual e Documentação Canônica
authorized_sub_skills:
  - name: minimal-impact-ui
    role: "Atlas Ex Umbris Ad Lucem + WinUI 3 Gallery (6 arquétipos de página, 28 efeitos, 3 temas e boilerplate HTML/CSS/JS)"
  - name: frontend-code-architect
    role: "Estruturação modular src/ em 5 camadas de Design Atômico e componentes guiados por propósito"
  - name: frontend-testing-auditor
    role: "Auditoria determinística de contraste, tipografia, espaçamento, camadas e FSM via scripts/audit_tactile_ui.py"
---

# Gerador e Sintetizador Canônico de `DESIGN.md` (`design-md` v5.0.0 — Arquitetura Visual Guiada por Propósito) 📐

Utilitário especializado em inspecionar um projeto frontend (local em disco ou remoto no **Google Stitch MCP**), compreender o **propósito e domínio do produto** e sintetizar o arquivo **`DESIGN.md`** na pasta raiz como fonte única da verdade (*Single Source of Truth*). Em vez de aplicar uma paleta fixa repetitiva em todos os projetos, adapta a atmosfera (*Ad Lucem*, *Cinza Monolítico `#57545d` + Menus `#8e8999`*, *Preto Terminal IBM `Ex Umbris`*, *AETHER 2027* ou paleta própria do domínio) respeitando **espaçamento, contraste, tipografia, estilo, camadas e hierarquia**.

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Quando um projeto novo ou existente precisar criar ou atualizar seu contrato `DESIGN.md` alinhado ao objetivo do produto.
- Quando o usuário solicitar explicitamente a definição de estilo, atmosfera, tipografia e tokens visuais de um projeto local ou do **Google Stitch** (`stitch*:*`).

### 🚫 Quando NÃO Usar (Limites e Exceções)
- Para scripts puramente backend/CLI sem interface gráfica.
- Nunca imponha uma única paleta de cores fixa sem antes analisar o propósito do projeto e seu público-alvo.

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `project_root_path` (obrigatório para projetos locais): Caminho absoluto da raiz onde o `DESIGN.md` será gravado.
- `project_purpose` (opcional, inferido automaticamente se omitido): `conversao_saas`, `editorial_leitura`, `fintech_confianca`, `ia_nativa_aether`, `medtech_clinico` ou `devtools_terminal_ibm`.
- `atmosphere_preference` (opcional): Preferência de família tonal (`ad-lucem`, `monolith-gray`, `ibm-terminal-dark`, `aether-oklch` ou `studio-v45` opcional).
- `stitch_project_id` (opcional): ID do projeto no Google Stitch MCP (`list_projects` / `get_screen` / `get_project`).

---

## ⚙️ Fluxo de Síntese por Propósito (`v5.0`)

### Passo 1: Diagnóstico do Propósito do Projeto e Escolha da Atmosfera
Consulte [`../_template/references/preferencias_estilo_e_temas.md`](../_template/references/preferencias_estilo_e_temas.md), a skill [`../minimal-impact-ui/SKILL.md`](../minimal-impact-ui/SKILL.md) e as referências interativas:
- [`../minimal-impact-ui/references/atlas_ex_umbris_winui.html`](../minimal-impact-ui/references/atlas_ex_umbris_winui.html) (*Atlas Ex Umbris + WinUI 3 Gallery* — 3 temas ao vivo, 4 cores pontuais de 2%, 6 arquétipos de composição de página além de formulários/gráficos, 28 efeitos de superfície/layout/motion/controles e nitidez tipográfica zero vermelho embaçado).
- [`references/ex_umbris_ad_lucem_studio.html`](references/ex_umbris_ad_lucem_studio.html) (*Ex Umbris Ad Lucem Studio* — 3 famílias tonais, 4 níveis de tinta, sombra esculpida em 3 camadas + 1px Rim Light, proporção 98/2).
- [`references/aether_2027_design_system.html`](references/aether_2027_design_system.html) (*AETHER 2027* — matriz de decisão por objetivo, `oklch()`, Bento Grid assimétrico e contraste perceptual APCA).
- [`references/design_md_v4_5_studio.html`](references/design_md_v4_5_studio.html) (Referência opcional de controles de estúdio v4.5 quando o projeto exigir estética de hardware dedicado).

1. **Enquadre o Objetivo**:
   - *Editorial / SaaS Diurno / MedTech*: Priorize **Ad Lucem** (`--bg-canvas: #F3F3F5` / `#F6F6F4`, `--bg-surface: #FFFFFF`, `--bg-elevated: #E6E6EA`, card de contraste alternado `--bg-contrast-card: #18181C`).
   - *Estúdio Analítico / Produtividade Anti-TDAH / Governança*: Priorize **Cinza sobre Cinza Monolítico** (`--bg-canvas: #57545d`, `--bg-surface: #49464f`, `--bg-elevated: #635f6a`, card de contraste `#232127`, menus em `#8e8999` com tinta escura `--nav-ink: #16151A`).
   - *DevTools / Observabilidade / Engenharia / Terminal*: Priorize **Preto Terminal IBM (`Ex Umbris`)** (`--bg-canvas: #070709` / `#09090B`, `--bg-surface: #101014`, `--bg-elevated: #18181E`) acoplado obrigatoriamente a **`IBM Plex Sans` + `IBM Plex Mono`**.
2. **Defina o Acento Pontual por Intenção (Proporção 98/2) e o Arquétipo de Página**:
   - Escolha a cor de acento (`--punctual-accent`: Carmim `#e13535`, Cerúleo `#35acd8` com texto escuro `#091318`, Esmeralda `#10B981` com texto escuro `#062016`, ou Âmbar `#D97706`) e selecione um dos **6 Arquétipos de Página** (*Split-Screen Workbench*, *Timeline Cronológica*, *Kanban Operacional*, *Canvas de Nós*, *Wizard Modo Foco Anti-TDAH* ou *Catálogo WinUI Gallery*).

### Passo 2: Especificação de Nitidez Tipográfica, Espaçamento, Contraste e Camadas
- **Nitidez Tipográfica (Zero Letras Vermelhas Embaçadas sobre Cinza/Escuro)**: Proibido `color: #e13535` puro ou serifa fina embaçada em fundos cinza/pretos; use `.highlight-surgical` (Semibold + sublinhado `2px` em `--punctual-accent`) em títulos e `.accent-text` (`#FFFFFF` no cinza/escuro ou `#991B1B` no claro + fundo `--punctual-soft` + `border-left: 2.5px solid var(--punctual-accent)`) em badges/tags, além de `font-variant-numeric: tabular-nums`.
- **Camadas, Motion & Elevação**: Sombra esculpida em 3 estágios (`--shadow-sculpted`: Umbra + Penumbra + Difusão) + luz de borda zenital de `1px` (`inset 0 1px 0 0 var(--rim-light)`) + curvas físicas `cubic-bezier(0.16, 1, 0.3, 1)` (`Quint Out`) e `cubic-bezier(0.34, 1.56, 0.64, 1)` (`Spring`).
- **Espaçamento & Geometria**: Respiro mínimo de 25%–35% de canvas aberto, Bento Grid assimétrico (`col-span-2` no item prioritário) e raios concêntricos ($R_{\text{interno}} = R_{\text{externo}} - \text{Padding}$).

---

## 📤 Saídas e Entregáveis — Template Canônico (`<project_root>/DESIGN.md`)

```markdown
# DESIGN.md — Arquitetura Visual, Atmosfera & Sistema de Estilo por Propósito
---
version: "5.0-adaptive"
project_purpose: "<conversao_saas | editorial_leitura | fintech_confianca | ia_nativa_aether | medtech_clinico | devtools_terminal_ibm>"
atmosphere_family: "<ad-lucem | monolith-gray | ibm-terminal-dark | aether-oklch | custom-domain>"
tokens:
  bg-canvas:        "#F3F3F5"   # Superfície base (respiro >= 25% da viewport)
  bg-surface:       "#FFFFFF"   # Card primário
  bg-elevated:      "#E6E6EA"   # Superfície secundária / agrupador
  bg-contrast-card: "#18181C"   # Bloco de inversão rítmica para destaque estrutural
  ink-primary:      "#111113"   # Títulos e métricas âncora (WCAG AAA / APCA Lc >= 75)
  ink-secondary:    "#4A4A52"   # Corpo de leitura (max 65ch, WCAG AA >= 4.5:1)
  ink-muted:        "#71717A"   # Rótulos e legendas
  ink-subtle:       "#A1A1AA"   # Placeholders e metadados terciários
  nav-bg:           "rgba(228, 228, 233, 0.88)"
  nav-ink:          "#18181B"   # Tinta escura nítida sobre menus claros ou #8e8999
  punctual-accent:  "#35acd8"   # Acento cirúrgico guiado pelo propósito (2% a 10% da tela)
  border-hairline:  "rgba(24, 24, 27, 0.08)"
  rim-light:        "rgba(255, 255, 255, 0.85)"
lighting:
  shadow-sculpted:  "0 1px 2px rgba(9,9,11,0.05), 0 8px 24px -4px rgba(9,9,11,0.06), 0 20px 40px -12px rgba(9,9,11,0.04), inset 0 1px 0 0 var(--rim-light)"
typography:
  font-sans:    "'Plus Jakarta Sans', 'Inter', sans-serif" # Ou 'IBM Plex Sans' no tema Terminal IBM
  font-display: "'Instrument Serif', serif"                # Opcional para tensão editorial
  font-mono:    "'IBM Plex Mono', 'JetBrains Mono', monospace" # Obrigatório tabular-nums em dados
---

## 1. Propósito do Projeto e Direção de Atmosfera
- **Objetivo Cognitivo**: [Descrever como o tema escolhido serve ao propósito do projeto].
- **Isolamento de Acento (Von Restorff 98/2 ou 60-30-10)**: Apenas 1 CTA primário sólido por vista; ações secundárias em `.btn-ghost`.

## 2. Tipografia, Hierarquia (Squint Test) e Alinhamento Tabular
- Escala fluida com `clamp()`, largura de leitura de `60ch–70ch` e `font-variant-numeric: tabular-nums` em KPIs, preços e tabelas.

## 3. Espaçamento, Camadas Esculpidas e Arquitetura `src/` (5 Camadas Atômicas)
- Bento Grid de 12 colunas (`gap: 16px..24px`), raios concêntricos ($R_{\text{int}} = R_{\text{ext}} - \text{Padding}$), sombra em 3 camadas + `1px` Rim Light e estados finitos FSM (`idle | loading | error | pressed`) com alvos $\ge 44 \times 44\text{px}$.
```

---

## 🤖 Ativação de Subagentes e Orquestração (`Topologia 3+1`)
- **Persona Responsável:** `FrontCraftMaster`
- **Subagentes Vinculados:** `ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction` e `ui-deterministic-observer`.
