---
name: design-md
description: "Cria ou atualiza o contrato DESIGN.md na raiz do projeto definindo tokens semânticos OKLCH, escala tipográfica modular, espaçamento e camadas. Use para criar o DESIGN.md; não use para projetos sem UI."
version: "8.2.0"
updated_at: "2026-10-31"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "8.2.0"
  updated_at: "2026-10-31"
  author: "UI-Architect & Melki"
  category: "Guia de Princípios de Design System Frontend (OKLCH), Física Óptica de Sombras e Arquitetura Espacial"
  tags: ["design-md", "frontend-design-md", "principios-de-design", "oklch", "sombras-multi-camadas", "container-queries", "starting-style", "aom-acessibilidade"]
---
# Guia de Princípios e Arquitetura de `DESIGN.md` (`design-md` v8.2.0 — Engenharia Visual Contextual, Zero Copia-e-Cola)

Esta skill atua como um **guia de princípios de engenharia visual, psicologia perceptual e arquitetura espacial** para sintetizar o contrato **`DESIGN.md`** (ou `design.md`) sob medida para a realidade de cada projeto, consultando como base:

- Referência de Composição e Física Óptica: [`references/design_system_composition_reference.md`](references/design_system_composition_reference.md)
- Fonte Única de Verdade (SSOT): [`Preferências de Trabalho com Agentes.md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md).

> **Regra de Ouro (Proibição de Copia-e-Cola de Componentes):** O `DESIGN.md` **NÃO é um despejo de componentes prontos** nem uma colagem cega de árvores Next.js, grafos React Flow ou carrosséis em projetos que não usam esses recursos. Ele é um **guia de princípios e decisões arquiteturais** derivado do propósito real do produto, do seu público-alvo e da sua stack (HTML/CSS puro, Go Server-Driven UI, SPA ou Fullstack).

---

## 1. Quando Usar, Entradas / Pré-requisitos e Limites de Escopo

### Entradas / Pré-requisitos e Quando Usar

- Contexto do produto, público-alvo, stack de frontend e arquivos existentes do repositório (`README.md`, CSS/tokens) para definir ou evoluir os princípios visuais, tokens semânticos `OKLCH`, regras espaciais e contratos de interação no arquivo `DESIGN.md` da raiz de um projeto com interface gráfica.
- Guiar a escolha contextual de paleta, tipografia, modo de elevação/sombra e arquétipo de layout antes de codificar telas ou componentes.

### Quando NÃO Usar (Limites e Exceções)

- Para projetos puramente backend/CLI sem interface gráfica.
- Para documentar arquitetura de nuvem/backend (`SPEC.md` / [`backend-architecture-skill`](file:///c:/Users/melki/dev/repos/adk-tests/.agents/skills/backend-architecture-skill/SKILL.md)), mapa de contexto do ecossistema (`CONTEXT.md`) ou regras operacionais (`AGENTS.md`).
- **Nunca copie componentes ou adendos fora do escopo do projeto** (ex.: não inclua regras de Canvas Infinito se o projeto for um sistema clínico editorial ou uma landing page).

---

## 2. Processamento / Fluxo — Os 5 Pilares de Princípios para Construir o `DESIGN.md`

Ao redigir o `DESIGN.md` de um projeto, traduza os **5 Pilares** abaixo para o domínio específico do produto (em vez de copiar blocos estáticos):

### Pilar 1: Filosofia de Design e Identidade Visual Contextual

1. **Decisões Opinativas e Contextuais:** Rejeite fórmulas genéricas e paletas arbitrárias. Justifique a escolha do matiz principal ($H$), saturação/croma ($C$), tipografia e densidade a partir do universo do produto e do seu público-alvo (ex.: sobriedade de baixa fadiga ocular para ferramentas clínicas/IDE vs. energia editorial para vitrines).
2. **Impacto do Elemento Principal (*Hero Funcional*):** A abertura da interface deve apresentar imediatamente a característica mais marcante do produto (seja um indicador numérico ao vivo, um painel interativo, uma busca semântica ou uma demonstração em tempo real), evitando banners decorativos vazios.
3. **Estrutura Visual como Informação:** Bordas (`1px solid var(--border-subtle)`), separadores, espaçamentos e marcadores numéricos (`font-variant-numeric: tabular-nums`) existem para codificar informação, agrupar dados relacionados e criar hierarquia — nunca como decoração gratuita.

### Pilar 2: Arquitetura Espacial Desacoplada (Macrolayouts vs. Microlayouts)

1. **Macrolayouts (Casca da Página):** Regidos por CSS Grid, Media Queries e `100dvh`, gerenciam a estrutura global (cabeçalho, navegação, área principal e painéis de inspeção) conforme a viewport. Selecione **apenas o Arquétipo Espacial que resolve o problema do projeto** (*Split-View Workbench*, *Bento Grid 12 col*, *Command Center / Data Grid*, *Canvas Editorial 65ch*, *HUD Espacial* ou *Folha Vetorial A4 `@media print`*).
2. **Microlayouts (Componentes Autônomos):** Regidos por Flexbox/Grid e **Container Queries (`@container`)**. Todo componente reutilizável declara `container-type: inline-size` no pai e usa unidades relativas ao container (`cqw`), reorganizando seu layout interno pela sua própria largura útil — sem quebrar ao ser movido de uma coluna estreita para o palco principal.
3. **Tipografia Fluida e Nitidez Óptica:** Escala fluida com `clamp(min, ideal, max)`, leitura confortável (`max-inline-size: 60ch..65ch`, `text-wrap: balance` em títulos e `text-wrap: pretty` em parágrafos) e travas anti-borrão GPU (`-webkit-font-smoothing: antialiased`, `font-synthesis: none`).

### Pilar 3: Cores e Elevação no Espaço Perceptual `OKLCH`

1. **Regra de Composição 60-30-10:**
   - **60% — Superfície Dominante / Neutra (`--bg-app` / `--surface-canvas`):** Fundo principal em tons suaves de baixíssimo croma.
   - **30% — Superfícies Secundárias (`--bg-surface` / `--bg-card`):** Barras laterais, cabeçalhos, cartões e painéis de suporte.
   - **10% — Destaque e Ação (`--brand-primary`):** Reservado estritamente para pontos focais interativos, botões primários (CTAs), indicadores de foco e estados ativos.
2. **Elevação por Luminosidade ($L$) no Dark Mode:** No modo escuro, sombras pretas puras perdem contraste. A profundidade no eixo Z é comunicada clareando progressivamente a luminosidade ($L$) das superfícies (`0.14` Canvas $\to$ `0.18` Surface $\to$ `0.22` Card $\to$ `0.26` Modal), combinada com bordas especulares sutis (`oklch(1 0 0 / 0.12)`).
3. **Derivações Dinâmicas (Zero Hex Hardcoded):** Use `light-dark()`, `color-mix(in oklab, ...)` para fundos translúcidos/badges e **Sintaxe de Cores Relativas (RCS)** (`oklch(from var(--brand-primary) calc(l - 0.08) c h)`) para calcular matematicamente estados `:hover` e `:active`.

### Pilar 4: Física e Matemática das Sombras em Camadas (*Multi-Layered Shadows*)

Uma única declaração de `box-shadow` gera sombras pesadas e artificiais. O `DESIGN.md` deve especificar a física da luz natural (incidência zenital 90°–120°) empilhando de **2 a 4 camadas**:
$$\texttt{box-shadow: } \underbrace{\Delta x \ \Delta y \ R_{\text{blur}} \ R_{\text{spread}} \ \text{cor}}_{\text{1. Umbra (Contato curto e nítido)}}, \ \underbrace{\Delta x \ \Delta y \ R_{\text{blur}} \ R_{\text{spread}} \ \text{cor}}_{\text{2. Penumbra Média}}, \ \underbrace{\Delta x \ \Delta y \ R_{\text{blur}} \ R_{\text{spread}} \ \text{cor}}_{\text{3. Penumbra Ambiente (Spread Negativo)}}$$

1. **Importância do Spread Radius Negativo (`-2px` a `-8px`):** Na camada ampla da penumbra, o spread negativo contrai a forma base antes do desfoque, impedindo que a sombra vaze pelas laterais e concentrando a gravidade visual na base do elemento.
2. **Escolha da Propriedade Correta:**
   - `box-shadow`: Caixas retangulares do DOM (acompanha `border-radius`, suporta `inset` e `spread`; atenção a `overflow: hidden` no pai).
   - `text-shadow`: Glifos tipográficos (garante legibilidade sobre gradientes/imagens sem criar caixa).
   - `filter: drop-shadow()`: Segue a máscara alfa exata de SVGs vazados, PNGs transparentes ou `clip-path`.
3. **Seleção Contextual dos 4 Modos de Sombra (escolha apenas os modos pertinentes ao projeto):**
   - **Modo 1 — Glassmorphism com Elevação Especular:** Para docks/modais translúcidos (`isolation: isolate`, `backdrop-filter: blur(16px..20px) saturate(180%)`, oclusão profunda + bisel superior `inset 0px 1px 0px oklch(1 0 0 / 0.20)`).
   - **Modo 2 — Neumorphism Tátil Moderno (Outset + Inset):** Extrusão suave (`--elevation-low/medium`) para cartões/botões combinada com cavidades *Sunken Wells* (`--shadow-inset` duplo) para inputs e botões `:active`.
   - **Modo 3 — High-Contrast Dark Glow:** Para editores visuais, grafos e dashboards densos em tema escuro (sombra preta densa de oclusão + halo difuso `0px 0px 16px oklch(from var(--brand-primary) l c h / 0.20..0.35)`).
   - **Modo 4 — Flutuação Gravitacional em Modais Nativos (`<dialog>` + `@starting-style`):** 3 camadas com spread negativo (`-8px`) aliadas a `transition: opacity 0.3s, transform 0.3s, overlay 0.3s allow-discrete, display 0.3s allow-discrete` e `@starting-style` para entrada/saída suave sem bibliotecas JS.

### Pilar 5: Engenharia de Interatividade, Acessibilidade Nativa (AOM) e Cascata CSS

1. **Ordem DOM = Ordem Visual:** A navegação por `Tab` e leitores de tela (AOM) seguem a sequência do HTML; nunca use `order` ou posicionamentos que desconectem a ordem visual da ordem do DOM.
2. **Anel de Foco & Primitivas Nativas:** Ative o anel de foco exclusivamente na navegação por teclado via `:focus-visible` (`outline: 2px solid var(--brand-primary); outline-offset: 2px`), use `:user-invalid`/`:user-valid` para validação tardia e prefira `<dialog>`, `popover="auto"` e `<details>` nativos.
3. **Lei de Fitts e Conforto Vestibular:** Em telas de toque (`@media (any-pointer: coarse)`), expanda alvos interativos para no mínimo **48 × 48 px** (~9 mm) com espaçamento mínimo de **8 px** entre botões; respeite `@media (prefers-reduced-motion: reduce)`.
4. **Cascata `@layer` e Proporcionalidade de Arquivos:** Organize o CSS em camadas explícitas (`@layer reset, tokens, base, layouts, components, utilities;`) eliminando `!important`, e estruture as pastas de forma proporcional à stack real do projeto (**Nível 1:** CSS em camadas/HTML enxuto; **Nível 2:** SPA Feature-Driven com colocalização; **Nível 3:** Fullstack App Router/PWA).

---

## 3. Saídas / Entregáveis — Como Estruturar o `DESIGN.md` do Projeto (Roteiro Adaptativo)

Ao gerar o `<project_root>/DESIGN.md`, sintetize um guia enxuto, opinativo e focado no projeto contendo:

1. **Propósito Visual, Público-Alvo e Hero Funcional** (decisões contextuais do produto).
2. **Arquitetura de Tokens em 3 Camadas (`OKLCH` 60-30-10, Elevação $L$ no Dark Mode e Derivações RCS/`color-mix`)**.
3. **Sistema de Sombras em Camadas e Modos de Profundidade Selecionados** (Umbra + Penumbra + Spread Negativo + `inset` especular).
4. **Arquitetura Espacial (Macrolayout escolhido + Regras de Microlayout `@container` + Escala Tipográfica)**.
5. **Regras de Interatividade, Acessibilidade AOM (`:focus-visible`, Lei de Fitts $48\times 48\text{px}$, `@starting-style`) e Organização `@layer` / Colocalização** (incluindo *apenas* os adendos técnicos de [`references/design_system_composition_reference.md`](references/design_system_composition_reference.md) que o projeto realmente utilizar).

---

## 4. Orquestração (`Topologia 3+1`)

- **Persona Coordenadora:** `UI-Architect`
- **Subagentes Vinculados:** `ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction` e `ui-deterministic-observer`.
