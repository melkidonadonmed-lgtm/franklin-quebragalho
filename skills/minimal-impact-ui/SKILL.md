---
name: minimal-impact-ui
description: >-
  Sistema de design e arquitetura front-end HTML, CSS, Tailwind e JavaScript baseado no padrão Ex Umbris Ad Lucem (Minimalismo de Impacto) e WinUI 3 Gallery. Use para criar ou estilizar páginas HTML, apps web, calculadoras médicas, formulários SUS, dashboards, prontuários ou ferramentas Anti-TDAH com os 3 temas (Cinza #57545d + menus #8e8999, Claro Editorial #F3F3F5 e Preto Terminal IBM #070709), 6 arquétipos de página, 28 efeitos WinUI, tipografia nítida sem letras vermelhas embaçadas sobre cinza e regra 98% neutro / 2% acento (#e13535, #35acd8, #10B981, #D97706). Não use para auditoria de repositório sem UI (use auditoria-projetos-sistema).
version: "1.0.0"
license: MIT
metadata:
  author: "FrontCraftMaster & Melki"
  version: "1.0.0"
  category: "Design System Ex Umbris Ad Lucem, WinUI 3 Gallery & Arquitetura Front-End Anti-TDAH"
  updated_at: "2026-10-19"
  tags:
    - "minimal-impact-ui"
    - "ex-umbris-ad-lucem"
    - "winui-3-gallery"
    - "anti-tdah"
    - "arquitetura-visual"
updated_at: 2026-10-19
author: FrontCraftMaster & Melki
category: Design System Ex Umbris Ad Lucem, WinUI 3 Gallery & Arquitetura Front-End Anti-TDAH
agent_persona: "FrontCraftMaster"
dag_id: "ui"
gate_script: "skills/frontend-testing-auditor/scripts/audit_tactile_ui.py"
min_score: 90.0
authorized_sub_skills:
  - name: design-md
    role: "Síntese e atualização do contrato DESIGN.md guiado pelo propósito do projeto"
  - name: frontend-code-architect
    role: "Particionamento em 5 camadas de Design Atômico para projetos multi-arquivo React/TS"
  - name: frontend-testing-auditor
    role: "Auditoria determinística de contraste, tipografia, camadas, FSM e Axe-Core via audit_tactile_ui.py"
---

# Sistema de Design & Arquitetura Front-End: `minimal-impact-ui` (Ex Umbris Ad Lucem + WinUI 3 Gallery)

Esta skill aplica a arquitetura visual **Ex Umbris Ad Lucem** (*Das Sombras para a Luz* — Minimalismo de Impacto) combinada ao vocabulário espacial, cinemático e de controles do **WinUI 3 Gallery**. Consulte o modelo interativo completo em [`references/atlas_ex_umbris_winui.html`](references/atlas_ex_umbris_winui.html) e o compêndio integral em [`references/compendio_completo_ex_umbris_winui.md`](references/compendio_completo_ex_umbris_winui.md).

---

## 1. Visão Geral, Filosofia Central e Quando Usar (Gatilhos de Ativação)

- **Proporção Cromática 98% / 2% (Efeito de Isolamento de Von Restorff):** 98% da interface é construída em tons neutros arquitetônicos (`#57545d`, `#49464f`, `#F3F3F5`, `#070709`). Apenas **2% da tela** recebe uma única cor pontual calibrada por objetivo (`--punctual-accent`).
- **Nitidez Tipográfica Absoluta (Zero Letras Vermelhas Embaçadas e Zero Serifa Fina em Cinza/Escuro):** Proíbe `color: #e13535` puro ou fontes serifadas finas (`Instrument Serif`) sobre fundos cinza/escuros (baixo contraste `2.1:1` e aberração cromática ocular). Todo destaque sobre fundo cinza ou preto usa **texto branco puro (`#FFFFFF`) em Semibold (`font-weight: 600`)** ancorado por **sublinhado cirúrgico de `2px`** (`.highlight-surgical` / `.font-serif-editorial` em títulos) ou **borda lateral esquerda de `2.5px solid var(--punctual-accent)`** (`.accent-text` em badges e tags).
- **Menus Nítidos de Alto Contraste (`#8e8999`):** Proíbe letras brancas lavadas sobre barras claras ou `#8e8999`. Os links do menu usam tinta grafite escura (`#16151A`) dentro de contêineres em pílula (`rounded-full`), invertendo para fundo escuro sólido (`#1E1C22`) e texto claro (`#F5F4F8`) no item ativo ou hover.

### Quando Ativar Esta Skill
- Criação ou estilização de páginas HTML, aplicações web single-file ou modulares, calculadoras médicas, geradores de documentos do SUS (APAC, LME, SISREG, SISCAN), prontuários/evoluções, dashboards ou ferramentas Anti-TDAH.
- Sempre que o pedido mencionar `@minimal-impact-ui`, "meu estilo de HTML", "tema cinza `#57545d`", "Ex Umbris", "WinUI Gallery" ou "minimalismo de impacto".

### Quando NÃO Usar (Limites e Exceções)
- Não use para scripts puramente backend/CLI sem interface gráfica.
- Não use para auditoria estrutural read-only de repositórios inteiros sem geração/refatoração de UI (use `auditoria-projetos-sistema`).

---

## 2. Entradas e Pré-requisitos

- `app_goal` (obrigatório): Objetivo funcional e domínio do aplicativo ou página (`medtech`, `tdah`, `saas`, `editorial`, `fintech`).
- `initial_theme` (opcional, padrão `"gray"`): `"gray"` (Cinza `#57545d` + Menus `#8e8999`), `"light"` (Claro Editorial `#F3F3F5`) ou `"dark"` (Preto Terminal IBM `#070709`).
- `accent_preset` (opcional, inferido pelo domínio): `"red"` (`#e13535`), `"blue"` (`#35acd8`), `"green"` (`#10B981`) ou `"amber"` (`#D97706`).
- `page_archetype` (opcional): Escolha entre os **6 Arquétipos de Composição de Página** além de formulários e gráficos comuns.

---

## 3. Processamento e Arquitetura: 3 Temas, 4 Cores Pontuais, 6 Arquétipos e 28 Efeitos

### 3.1. Matriz dos 3 Temas Oficiais (Alternância Ao Vivo + `localStorage`)

| Token CSS / Atributo | 1. Cinza Monolítico (`data-theme="gray"` — Padrão) | 2. Claro Editorial (`data-theme="light"` — Ad Lucem) | 3. Preto Terminal IBM (`data-theme="dark"`) |
| :--- | :--- | :--- | :--- |
| **Fundo Principal (`--bg-canvas`)** | `#57545d` | `#F3F3F5` | `#070709` |
| **Superfície de Card (`--bg-surface`)** | `#49464f` | `#FFFFFF` | `#101014` |
| **Superfície Elevada (`--bg-elevated`)** | `#635f6a` | `#E6E6EA` | `#18181E` |
| **Card de Contraste (`--bg-contrast-card`)** | `#232127` (texto `#F4F3F7`) | `#18181C` (texto `#F4F4F6`) | `#1D1D24` (texto `#FAFAFA`) |
| **Barra de Menu (`--nav-shell-bg`)** | `#8e8999` (tinta `#16151A`) | `rgba(255, 255, 255, 0.92)` (tinta `#18181B`) | `rgba(16, 16, 20, 0.92)` (tinta `#E4E4E7`) |
| **Texto Primário (`--ink-primary`)** | `#F7F6F9` | `#111115` | `#F4F4F6` |
| **Texto Secundário (`--ink-secondary`)** | `#DFDDE4` | `#3F3F46` | `#B4B4BE` |
| **Texto Silenciado (`--ink-muted`)** | `#BDB9C6` | `#686873` | `#7D7D8A` |
| **Texto de Acento (`--punctual-text`)** | `#FFFFFF` (com filete/borda 2.5px) | `#991B1B` (escuro nítido) | `#FFFFFF` (com filete/borda 2.5px) |
| **Tipografia Base (`--font-sans`)** | `Inter`, `Plus Jakarta Sans` | `Inter`, `Plus Jakarta Sans` | `IBM Plex Sans` + títulos `IBM Plex Mono` |

### 3.2. As 4 Cores Pontuais Calibradas por Objetivo (Regra dos 2%)

| Domínio / Objetivo do Projeto | Cor Pontual (`--punctual-accent`) | Fundo Suave (`--punctual-soft`) | Brilho (`--punctual-glow`) | Texto no Botão (`--punctual-btn-ink`) |
| :--- | :--- | :--- | :--- | :--- |
| **Design, Editorial, Produtividade & Foco (Padrão)** | `#e13535` (Carmim Selo) | `rgba(225, 53, 53, 0.12)` | `rgba(225, 53, 53, 0.35)` | `#FFFFFF` |
| **IA, Engenharia de Dados, SaaS & Telemetria** | `#35acd8` (Azul Cerúleo) | `rgba(53, 172, 216, 0.14)` | `rgba(53, 172, 216, 0.38)` | `#091318` (Grafite Escuro) |
| **MedTech, Clínica, Calculadoras & SUS** | `#10B981` (Esmeralda Clínico) | `rgba(16, 185, 129, 0.13)` | `rgba(16, 185, 129, 0.35)` | `#062016` (Verde-Preto Escuro) |
| **FinTech, Jurídico, Patrimônio & Alertas** | `#D97706` (Âmbar Imperial) | `rgba(217, 119, 6, 0.13)` | `rgba(217, 119, 6, 0.35)` | `#FFFFFF` |

### 3.3. Os 6 Arquétipos de Composição de Página (Além de Formulários e Gráficos)

| # | Arquétipo de Página | Estrutura Espacial | Quando Usar (Exemplos Reais) | Quando Evitar |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **Split-Screen Live Workbench** | Painel esquerdo (`col-span-5`) com pílulas de inserção rápida e campos compactos + Painel direito (`col-span-7`) com folha A4 / preview ao vivo. | Geradores de Evolução Médica, APAC/LME/SISREG, editores de prompts/skills e laudos estruturados. | Telas exclusivamente mobile sem converter o painel direito em aba ou modal rápido. |
| **02** | **Linha do Tempo Cronológica (Timeline)** | Eixo vertical contínuo (`border-l-2 border-strong`) com nós numerados (`D1`, `D2`, `D3`), cards expansíveis e ponto de 2% no marco atual. | Evolução hospitalar dia a dia, histórico comparativo de exames, linha de cuidado ou roadmaps. | Catálogos de itens sem relação temporal ou cronológica. |
| **03** | **Quadro Kanban Operacional** | 3 a 4 colunas de estágio (`Pendente`, `Em Análise`, `Concluído`) com contadores no topo e cartões compactos com filete lateral. | Gestão de pacientes do turno, acompanhamento de processos SUS ou quadro de tarefas (Anti-TDAH). | Mais de 5 colunas simultâneas ou centenas de registros sem filtro. |
| **04** | **Canvas Espacial de Nós (Árvore de Decisão)** | Nós clicáveis sobre malha arquitetônica (`64x64px`) que iluminam o caminho escolhido (`Sim / Não`) com borda `--punctual-accent`. | Diretrizes clínicas (sepse, dor torácica, regulação SUS), algoritmos diagnósticos e fluxos de IA. | Cadastros tabulares simples de preenchimento linear. |
| **05** | **Wizard Modo Foco Anti-TDAH** | Monólito centralizado exibindo apenas 1 decisão/etapa por tela com barra de progresso superior em `JetBrains Mono` e botões grandes. | Processos complexos onde exibir 30 ou 40 campos de uma vez causa paralisia ou fadiga cognitiva. | Edição rápida de apenas 1 campo isolado em uma ficha já concluída. |
| **06** | **Catálogo Interativo (WinUI Gallery)** | `SelectorBar` em pílulas no topo + busca instantânea por palavra-chave + grade de cartões com `Expander` de código/copiar em cada item. | Bulário pessoal, biblioteca de protocolos clínicos, cofre de prompts e documentação interativa. | Entrada sequencial de dados de um único atendimento. |

### 3.4. Resumo dos 28 Efeitos, Layouts, Motion & Controles (WinUI 3 + Ex Umbris)

Consulte a tabela detalhada e snippets em [`references/compendio_completo_ex_umbris_winui.md`](references/compendio_completo_ex_umbris_winui.md):
1. **Materiais & Luz (01–06):** `(01) AcrylicBrush` (`backdrop-filter: blur(16px)` + opacidade `85%–92%` apenas em navbars/popovers), `(02) SystemBackdrop / Mica` (degrau tonal de `6%–10%` entre `#57545d`, `#49464f` e `#635f6a`), `(03) ThemeShadow + Rim Light 1px` (`--shadow-sculpted` + `inset 0 1px 0 0 var(--rim-light)`), `(04) ContentIsland & Contraste Alternado` (alternar `#49464f` com `#232127` em raio `14px`), `(05) Compact Sizing` (`py-1.5 px-2.5` + `tabular-nums`), `(06) Grade Arquitetônica Blueprint` (`64x64px` em `--border-hairline`).
2. **Layout & Espaço (07–14):** `(07) Bento Grid (VariableSizedWrapGrid)` (`col-span-2` no card focal de 2%), `(08) SplitView` (Master-Detail `320px 1fr`), `(09) Expander` (revelação progressiva escondendo os 80% técnicos), `(10) Canvas (Top, Left, Z-Index)` (camadas espaciais), `(11) SelectorBar & TabView em Pílula`, `(12) Viewbox & Folha A4 Proporcional` (`210x297mm` branco sobre palco `#57545d`), `(13) StackPanel & WrapPanel (Chips clicáveis)`, `(14) Border & Molduras Hairline` (`1px`).
3. **Motion & Cinemática (15–20):** `(15) Implicit Transitions`, `(16) Connected Animation` (expansão no lugar mantendo âncora retiniana Anti-TDAH), `(17) Easing Functions Físicas` (`Quint Out cubic-bezier(0.16, 1, 0.3, 1)` de `250ms–450ms` para painéis e `Spring cubic-bezier(0.34, 1.56, 0.64, 1)` para badges; proibido `linear` em UI), `(18) Theme Transitions` (`450ms`), `(19) Page Transitions Stagger` (`40ms`), `(20) ParallaxView Sutil`.
4. **Controles & Fluxo Anti-TDAH (21–28):** `(21) Command Palette (Ctrl+K)`, `(22) App Notifications (Toasts) & Badges` (zero `alert()` nativo), `(23) Popup & Popover Contextual`, `(24) Botão Pílula Direcional (↘)` (texto escuro `#091318`/`#062016` em Azul/Verde; branco em Carmim/Âmbar), `(25) RichEditBox com Templates Clínicos` (macros de 1 clique + `localStorage`), `(26) Storage Dropzone Tátil`, `(27) InkCanvas`, `(28) Squint Test & Modo Foco`.

---

## 4. Armadilhas e Guardrails (*Gotchas*)

- **Nunca use `color: #e13535` puro sobre fundo cinza (`#57545d` / `#49464f`) ou preto (`#070709`):** O contraste cai para `2.1:1` e causa embaçamento visual. Use sempre `.accent-text` (`color: var(--punctual-text)` `#FFFFFF` Semibold + fundo `--punctual-soft` + `border-left: 2.5px solid var(--punctual-accent)`) ou `.highlight-surgical` (sublinhado `2px`).
- **Nunca use texto branco sobre menu `#8e8999` ou sobre botão Azul (`#35acd8`) / Verde (`#10B981`):** No menu `#8e8999`, a tinta obrigatória é `#16151A`; nos botões preenchidos Azul/Verde, use `--punctual-btn-ink` escuro (`#091318` / `#062016`).

---

## 5. Saídas, Entregáveis e Checklist de Validação

1. **Zero letras vermelhas soltas sobre cinza/preto:** Todo destaque usa `.accent-text` ou `.highlight-surgical`.
2. **Contraste de menus em `#8e8999`:** Links da barra superior em `#16151A`, invertendo para fundo `#1E1C22` e texto `#F5F4F8` na pílula ativa.
3. **Sombra física + Rim Light:** Cards principais aplicam `--shadow-sculpted` com `inset 0 1px 0 0 var(--rim-light)`.
4. **Funcionalidade 100% operante e `@media print` A4:** Todos os seletores de tema, filtros, sliders, cópia e impressão A4 funcionam sem erros e passam em `audit_tactile_ui.py` ($\ge 90.0/100$).
