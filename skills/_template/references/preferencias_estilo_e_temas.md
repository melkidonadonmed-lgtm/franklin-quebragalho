# Preferências de Estilo, Arquitetura Visual & Temas por Objetivo

> **Princípio Diretor (Fim da "Paleta Fixa")**: Nenhum projeto deve receber uma paleta de cores engessada ou componentes táteis repetitivos que deixem todos os sistemas com a mesma aparência. A escolha de **tema, superfície, acento cromático, tipografia, espaçamento, contraste e camadas** deve derivar diretamente do **propósito e objetivo do projeto**, guiada pelas preferências estéticas e invariantes arquiteturais abaixo (*Ex Umbris Ad Lucem* & *AETHER 2027*).

---

## 1. Diagnóstico de Propósito do Projeto (Intent-Driven Theme Selection)

Antes de definir cores, fontes ou componentes, toda skill de arquitetura, frontend ou auditoria deve responder: **Qual é o objetivo central deste produto e sob qual condição cognitiva o usuário o opera?**

| Objetivo / Domínio do Projeto | Condição de Uso & Prioridade Cognitiva | Atmosfera / Tema Recomendado | Acento Pontual Sugerido (98/2 ou 60-30-10) |
| :--- | :--- | :--- | :--- |
| **1. Conversão & SaaS de Alta Densidade** | Decisão rápida, clareza de fluxo, destaque inequívoco para a ação principal (CTA) e leitura dinâmica de status. | **Ad Lucem (Claro Técnico)** ou **AETHER Dual-Adaptive** com cards de contraste alternados (`#18181C`) para áreas de destaque. | **Cerúleo Técnico** (`#35acd8`), **Índigo** (`#4F46E5` / `oklch(0.58 0.22 260)`) ou **Carmim Selo** (`#e13535`). |
| **2. Editorial, Documentação & Conhecimento** | Leitura longa sem fadiga visual, ritmo tipográfico cadenciado, largura de linha controlada (`60ch–70ch`) e foco no conteúdo. | **Ad Lucem (Papel Quente `#F6F6F4` / `#F3F3F5`)** com tensão tipográfica Serif + Sans. | **Carmim Editorial** (`#e13535` / `#FF3B1D`) ou **Âmbar Imperial** (`#B45309`). |
| **3. Confiança, FinTech & Governança Executiva** | Precisão numérica absoluta (`tabular-nums`), sobriedade institucional, rastreabilidade de dados e zero distração visual. | **Cinza sobre Cinza Monolítico (`#57545d`)** ou **Ad Lucem Alabastro** com blocos de sumário em alto contraste. | **Âmbar Imperial** (`#D97706`), **Esmeralda Sóbrio** (`#059669`) ou **Azul Petróleo**. |
| **4. Imersão, IA Nativa & Exploração Criativa** | Percepção de profundidade espacial, resposta fluida em tempo real, visualização de grafos/agentes e estética de vanguarda. | **AETHER 2027 (Obsidiana ou Alabastro Perceptual `oklch()`)** ou **Cinza Monolítico (`#57545d` + Menus `#8e8999`)**. | **Cerúleo Luminoso** (`#38BDF8`), **Violeta Espectral** (`oklch(0.62 0.20 285)`) ou **Carmim**. |
| **5. MedTech & Saúde Clínica (PEP / A4)** | Plantões longos, leitura crítica de sinais vitais/doses sem erro humano, conformidade de impressão A4 e contraste máximo. | **Ad Lucem Clínico (`#F4F6F8` / `#FFFFFF`)** ou modo noturno de laudo com zero brilho especular excessivo. | **Esmeralda Clínico** (`#059669` / `#10B981`) e **Azul Hospitalar Sóbrio** (`#0284C7`), com vermelho restrito a alertas vitais. |
| **6. DevTools, Telemetria & Terminal IBM** | Inspeção de logs, métricas de baixa latência, operação intensiva via atalhos (`Ctrl+K`) e contraste de terminal. | **Preto Terminal IBM (`Ex Umbris` `#070709` / `#09090B`)** acoplado à tipografia **IBM Plex**. | **Cerúleo Terminal** (`#38BDF8`), **Verde Matriz** (`#10B981`) ou **Carmim de Falha** (`#F43F5E`). |

---

## 2. Preferências de Atmosfera e Superfícies (3 Famílias Base + Estúdio v4.5)

As famílias abaixo são **pontos de partida calibrados** (preferências do desenvolvedor), podendo ter seus matizes ajustados ao domínio do projeto desde que preservem a **física de camadas, legibilidade e contraste**.

### Família A — *Ad Lucem* (Claro Editorial & Alto Contraste Escultural)
* **Filosofia**: A luz é a matéria-prima. O espaço negativo respira e a elevação nasce de sombras esculpidas em 3 camadas e blocos de contraste alternados.
* **Tokens de Referência**:
  * `--bg-canvas`: `#F3F3F5` (ou `#F6F6F4` / `#F7F4EF` em projetos editoriais/clínicos)
  * `--bg-surface`: `#FFFFFF` (cards primários)
  * `--bg-elevated`: `#E6E6EA` (superfícies secundárias, wells e agrupadores)
  * `--bg-contrast-card`: `#18181C` com texto `#FAFAFA` (usado pontualmente em 1 card de destaque/sumário para criar ritmo visual e quebrar a monotonia de telas 100% brancas)
  * `--ink-primary`: `#111113` | `--ink-secondary`: `#4A4A52` | `--ink-muted`: `#71717A` | `--ink-subtle`: `#A1A1AA`
  * `--nav-bg`: `rgba(228, 228, 233, 0.88)` com `--nav-ink: #18181B` (tinta escura nítida; **proibido texto branco lavado sobre menu claro**).

### Família B — *Cinza sobre Cinza Monolítico* (`#57545d` Fundo + `#8e8999` Menus)
* **Filosofia**: Brutalismo sereno de estúdio. Reduz o cansaço de telas brancas sem mergulhar no breu total, criando uma atmosfera arquitetural sofisticada.
* **Tokens de Referência**:
  * `--bg-canvas`: `#57545d` (Ardósia Monolítico)
  * `--bg-surface`: `#49464f` (Card em degrau tonal abaixo do canvas)
  * `--bg-elevated`: `#635f6a` (Superfície elevada iluminada)
  * `--bg-contrast-card`: `#232127` (Bloco de ancoragem profunda)
  * `--ink-primary`: `#F4F3F6` | `--ink-secondary`: `#DFDCE5` | `--ink-muted`: `#BCB7C6`
  * **Arquitetura de Menus `#8e8999`**: Barras de navegação e seletores usam `--nav-bg: #8e8999` em formato pílula (`border-radius: 9999px`), obrigatoriamente com **tinta escura de alto contraste** (`--nav-ink: #16151A`) para leitura imediata, e item ativo encapsulado em pílula escura (`--nav-active-bg: #18181C`, `--nav-active-ink: #FFFFFF`).

### Família C — *Ex Umbris / Preto Terminal IBM* (Obsidiana + Tipografia IBM Plex)
* **Filosofia**: Escuridão profunda de instrumento de precisão. A profundidade não vem de sombras pretas invisíveis no escuro, mas de **degraus de luminância** (`+4%` a `+7%` de luz por camada) e **Rim Light superior de 1px**.
* **Tokens de Referência**:
  * `--bg-canvas`: `#070709` ou `#09090B` (Preto Obsidiana / Terminal)
  * `--bg-surface`: `#101014` ou `#121215` (Card primário)
  * `--bg-elevated`: `#18181E` ou `#18181C` (Superfície elevada / hover)
  * `--bg-contrast-card`: `#F3F3F5` com `--contrast-card-ink: #09090B` (Inversão cirúrgica para callouts de alto impacto)
  * `--ink-primary`: `#F4F4F6` | `--ink-secondary`: `#A1A1AA` | `--ink-muted`: `#71717A`
  * `--rim-light`: `rgba(255, 255, 255, 0.08)` (`inset 0 1px 0 0 var(--rim-light)`)
* **Regra de Acoplamento Tipográfico IBM**: Sempre que o projeto adotar o tema **Preto Terminal (`Ex Umbris`)**, a tipografia deve priorizar **`IBM Plex Sans`** (corpo/UI) e **`IBM Plex Mono`** (títulos técnicos, métricas, comandos e tabelas) com `letter-spacing: -0.03em`.

### Referências Interativas Canônicas (`minimal-impact-ui` & `design-md`)
* **[`atlas_ex_umbris_winui.html`](../../minimal-impact-ui/references/atlas_ex_umbris_winui.html)** e **[`compendio_completo_ex_umbris_winui.md`](../../minimal-impact-ui/references/compendio_completo_ex_umbris_winui.md)** (na skill **[`minimal-impact-ui`](../../minimal-impact-ui/SKILL.md)**): Modelo canônico de referência **Ex Umbris Ad Lucem + WinUI 3 Gallery** (Guia Anti-TDAH) com os 3 temas (`gray` `#57545d` + menus `#8e8999`, `light` `#F3F3F5`, `dark` `#070709`), 4 cores pontuais (2%), 6 arquétipos de composição de página, catálogo interativo de 28 efeitos, 3 playgrounds ao vivo e montador de pedidos.
* **[`ex_umbris_ad_lucem_studio.html`](../../design-md/references/ex_umbris_ad_lucem_studio.html)**, **[`aether_2027_design_system.html`](../../design-md/references/aether_2027_design_system.html)** e **[`design_md_v4_5_studio.html`](../../design-md/references/design_md_v4_5_studio.html)** (em `skills/design-md/references/`): Showcases complementares para direção editorial, espaço `oklch()` e controles de estúdio v4.5.

---

## 3. Os 6 Pilares da Arquitetura Visual e Regras de Nitidez (`AUDIT-VIS-01`)

Independentemente do tema escolhido para o projeto, toda interface construída ou auditada deve respeitar estes 6 pilares:

### 3.1. Proporção Cromática 98% / 2% & 4 Cores Pontuais Calibradas (Von Restorff)
* **90% a 98% da tela** deve ser composta pela escala estrutural neutra do tema (canvas `#57545d` / `#F3F3F5` / `#070709`, superfícies `#49464f` / `#FFFFFF` / `#101014`, bordas sutis e hierarquia de tintas).
* **2% da tela** recebe uma única **Cor Pontual Calibrada por Objetivo** (`--punctual-accent`):
  1. **Design, Editorial, Produtividade & Foco (Padrão):** Carmim Selo (`#e13535`) — texto no botão `--punctual-btn-ink: #FFFFFF`.
  2. **IA, Engenharia de Dados, SaaS & Telemetria:** Azul Cerúleo (`#35acd8`) — texto no botão obrigatoriamente escuro (`--punctual-btn-ink: #091318`).
  3. **MedTech, Clínica, Calculadoras & SUS:** Esmeralda Clínico (`#10B981`) — texto no botão obrigatoriamente escuro (`--punctual-btn-ink: #062016`).
  4. **FinTech, Jurídico, Patrimônio & Alertas:** Âmbar Imperial (`#D97706`) — texto no botão `--punctual-btn-ink: #FFFFFF`.
* **Efeito Von Restorff**: Deve existir **apenas 1 ou 2 CTAs Primários sólidos** (ou `.directional-pill-cta` com seta `↘`) com cor de acento na dobra principal; botões secundários usam estilo `.btn-ghost` ou grafite elevado.

### 3.2. Nitidez Tipográfica Absoluta (Zero Letras Vermelhas Embaçadas & Zero Serifa Fina sobre Cinza/Escuro)
* **Proibição de Letras Vermelhas Soltas no Cinza/Escuro**: Em fundos cinza (`#57545d`, `#49464f`) ou pretos (`#070709`), letras vermelhas puras (`color: #e13535`) sofrem de baixo contraste (`2.1:1`) e aberração cromática ocular, e fontes serifadas finas (`Instrument Serif`) ficam embaçadas.
* **Solução Obrigatória de Alta Nitidez**:
  1. **Em Títulos (`.highlight-surgical` / `.font-serif-editorial`)**: Usar `var(--font-sans)` em Semibold (`font-weight: 600`, `font-style: normal`) com **sublinhado cirúrgico de `2px`** (`text-decoration: underline; text-decoration-color: var(--punctual-accent); text-decoration-thickness: 2px; text-underline-offset: 6px;`).
  2. **Em Badges e Tags (`.accent-text`)**: Usar `--punctual-text: #FFFFFF` (no cinza/escuro) ou `#991B1B` (no claro) em `font-weight: 600`, fundo `--punctual-soft` e **filete lateral esquerdo de `2.5px solid var(--punctual-accent)`**.
* **4 Níveis Semânticos de Tinta (`Squint Test` `< 500ms`)**: `--ink-primary`, `--ink-secondary` (`max-width: 65ch`), `--ink-muted` e `--ink-subtle`.
* **Pares de Fontes de Alta Nitidez & Alinhamento Tabular**:
  * `Inter` + `JetBrains Mono`, `Plus Jakarta Sans` + `JetBrains Mono` ou `IBM Plex Sans` + `IBM Plex Mono` (obrigatório em `data-theme="dark"`).
  * `font-variant-numeric: tabular-nums` obrigatório em qualquer número dinâmico, dose, escore, preço, latência ou tabela, com piso `font-size >= 12px` (`0.75rem`, exceto cabeçalhos `th` técnicos uppercase em `mono`).

### 3.3. Espaçamento, Respiro (Whitespace) & Geometria Concêntrica
* **Taxa de Respiro**: Pelo menos **25% a 35% da viewport** deve permanecer como espaço aberto (`--bg-canvas`), com opção de `Compact Sizing` (`py-1.5 px-2.5`) em tabelas operacionais de alta densidade.
* **Bento Grid Assimétrico**: Card focal expandido em `col-span-2` (em grades de 3 colunas) ou `col-span-8` / `col-span-7` (em grades de 12 colunas), com raios concêntricos ($R_{\text{interno}} = \max(4\text{px}, R_{\text{externo}} - \text{Padding})$).

### 3.4. Camadas, Sombra Esculpida em 3 Estágios, Rim Light & Contraste Alternado
* **Sombra Esculpida Tripla (`--shadow-sculpted`) + Rim Light (`1px`)**: Umbra de contato curta + Penumbra direcional + Difusão ambiental longa + `inset 0 1px 0 0 var(--rim-light)` no topo do card.
* **ContentIsland & Contraste Alternado (`Terrixa`)**: Alternar superfície padrão (`#49464f` / `#FFFFFF`) com blocos de alto contraste escuro (`#232127` / `#18181C`, `.surface-contrast`) para criar ritmo visual sem adicionar novas cores.
* **AcrylicBrush Calibrado**: Restrito a barras fixas (`nav-shell`), popovers e `Command Palette (Ctrl+K)` com `backdrop-filter: blur(16px)` e opacidade alta (`85%` a `92%`), nunca em tabelas ou textos longos.

### 3.5. Motion Físico (WinUI 3 Cinemática) & Acessibilidade Determinística (FSM)
* **Curvas de Velocidade Físicas**:
  * **Quint Out (`cubic-bezier(0.16, 1, 0.3, 1)` ou `cubic-bezier(0.22, 1, 0.36, 1)`, `250ms–450ms`)**: Padrão para `SplitView`, `Expander`, `Connected Animation` (expansão no lugar preservando a âncora espacial Anti-TDAH) e troca de temas (`450ms`).
  * **Spring Overshoot (`cubic-bezier(0.34, 1.56, 0.64, 1)`, `350ms`)**: Micro-feedbacks em badges e notificações toast. (Proibido `linear` em transições de UI).
* **Estados Finitos (FSM) & Impressão A4**: Estados explícitos (`idle`, `loading`, `error`, `pressed`), `@media (prefers-reduced-motion: reduce)` e `@media print` A4 limpo (`#FFFFFF` / `#111115`).

---

## 4. Os 6 Arquétipos de Composição de Página (Além de Formulários e Gráficos)

Para evitar que toda aplicação gerada caia no clichê de "formulário simples ou dashboard de gráficos", selecione um dos **6 Arquétipos Espaciais** documentados em [`minimal-impact-ui`](../../minimal-impact-ui/SKILL.md):

1. **01. Split-Screen Live Workbench (`SplitView`):** Entrada rápida com pílulas/macros na esquerda (`col-span-5`) + Preview ao vivo / Folha A4 oficial na direita (`col-span-7`). Ideal para Evolução Médica, APAC/LME/SISREG, laudos e geradores de prompts.
2. **02. Linha do Tempo Cronológica (`Timeline`):** Eixo vertical contínuo (`border-l-2 border-strong`) com marcos numerados (`D1, D2, D3`), cards expansíveis e ponto de 2% no evento atual. Ideal para evolução hospitalar, histórico de exames e roadmaps.
3. **03. Quadro Kanban Operacional:** 3 a 4 colunas de estágio (`Pendente → Em Análise → Concluído`) com contadores no topo e filete lateral de prioridade. Ideal para gestão de leitos/plantão, processos SUS e fluxo de tarefas Anti-TDAH.
4. **04. Canvas Espacial de Nós / Árvore de Decisão Interativa:** Nós clicáveis sobre malha arquitetônica (`64x64px`) iluminando o caminho ativo (`Sim / Não`) com borda `--punctual-accent`. Ideal para diretrizes médicas (sepse, dor torácica) e fluxos de agentes.
5. **05. Wizard Modo Foco (1 Decisão por Tela — Anti-Sobrecarga TDAH):** Monólito centralizado com 1 etapa lógica por vez, barra de progresso em `Mono` e botões grandes de escolha rápida.
6. **06. Catálogo Interativo & Cofre de Conhecimento (`WinUI 3 Gallery`):** `SelectorBar` em pílulas no topo + busca instantânea + grade de cards com `Expander` de código/copiar em cada item.

---

## 5. Vocabulário Canônico dos 28 Efeitos, Layouts, Motion & Controles (WinUI 3 + Ex Umbris)

| Categoria | Itens do Catálogo (`minimal-impact-ui` / `atlas_ex_umbris_winui.html`) |
| :--- | :--- |
| **1. Materiais & Luz (6)** | `(01) AcrylicBrush (Vidro Acromático)`, `(02) SystemBackdrop / Superfície Mica`, `(03) ThemeShadow + Rim Light 1px`, `(04) ContentIsland & Contraste Alternado`, `(05) Compact Sizing (Alta Densidade)`, `(06) Grade Arquitetônica (Blueprint 64x64px)` |
| **2. Layout & Espaço (8)** | `(07) Grid & VariableSizedWrapGrid (Bento)`, `(08) SplitView (Master-Detail)`, `(09) Expander (Revelação Progressiva)`, `(10) Canvas (Top, Left, Z-Index)`, `(11) SelectorBar & TabView em Pílula`, `(12) Viewbox & Folha A4 Proporcional`, `(13) StackPanel & WrapPanel (Chips)`, `(14) Border & Molduras Hairline` |
| **3. Motion & Animação (6)** | `(15) Implicit Transitions`, `(16) Connected Animation (Continuidade Anti-TDAH)`, `(17) Easing Functions Físicas (Quint Out & Spring)`, `(18) Theme Transitions (450ms)`, `(19) Page Transitions (Stagger)`, `(20) ParallaxView Sutil` |
| **4. Controles & Fluxo (8)** | `(21) Command Palette (Ctrl+K)`, `(22) App Notifications (Toasts) & Badges`, `(23) Popup & Popover Contextual`, `(24) Botão Pílula Direcional (↘)`, `(25) RichEditBox com Templates Clínicos`, `(26) Storage Dropzone Tátil`, `(27) InkCanvas (Desenho & Marcação)`, `(28) Squint Test & Modo Foco` |

