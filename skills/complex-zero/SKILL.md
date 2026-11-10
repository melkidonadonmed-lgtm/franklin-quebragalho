---
name: complex-zero
description: "Audita via ciclo ReAct (CDP DevTools e AST) aplicações frontend complexas com canvas infinito @xyflow/react, WebSocket Chokidar, nós fantasmas funções falsas e Next.js 15 async params. Use para grafos; não use para páginas simples."
version: "3.0.0"
updated_at: "2026-04-19"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "3.0.0"
  updated_at: "2026-04-19"
  author: "Franklin Quebra-Galho"
  category: "general"
  tags: ["frontend", "architecture", "nav-x-func-fusion", "react-flow", "xyflow", "nextjs-15", "oklch", "container-queries", "ast-analysis", "devtools-cdp"]
---
# Complex-Zero + Nav-X-Func (`v3.0.0`) — Fusão de Auditoria ReAct Visual/CDP, Organização Macro/Micro, Hierarquia Visual, Anti-Proliferação de Abas e AST Anti-Fake

## 1. Visão Geral, Propósito, Fusão com `nav-x-func` e Gatilhos de Ativação (Quando Usar)

A skill **`complex-zero` (`v3.0.0`)** opera agora em **Fusão Simbiótica Obrigatória com a skill [`nav-x-func` (`v6.0.0`)](../nav-x-func/SKILL.md)**, atuando como auditor visual empírico (Chrome DevTools Print + DOM/CSS Computado) e arquiteto determinístico (0 a 100 pontos + Score `SGA`/`TIF`) para **interfaces web de alta densidade** — dashboards analíticos, bancadas de agentes, editores em canvas infinito (`@xyflow/react` / mapas 2D), observabilidade em tempo real (`WebSocket` + `chokidar`) e **Next.js 15+ App Router**.

### Por que `complex-zero` e `nav-x-func` operam fundidas (`v3.0.0`)?

Auditorias puramente estáticas baseadas em regex superficial geram o anti-padrão de **"Pseudo-Auditoria com Pseudo-ReAct"**: o código passa porque contém a palavra `oklch(` ou `clamp(`, mas na tela real os menus estão espremidos (`font-size: 11px/12px`, `gap: 4px`), a hierarquia visual está achatada, o dashboard divide espaço espremido com o canvas infinito e o agente cria novas abas (`role="tab"` / sub-abas) em vez de reutilizar os elementos existentes da página.

A fusão elimina **5 falhas estruturais e visuais críticas**:

1. **Fim do Pseudo-ReAct (Inspeção Visual & Metadados Reais no Chrome DevTools):** É **proibido** aprovar qualquer interface sem executar o protocolo empírico no navegador (`take_screenshot` + `take_snapshot` + `evaluate_script` medindo `getComputedStyle` e `getBoundingClientRect` no DOM real).
2. **Proibição de Criar Novas Abas & Reuso In-Place (`Anti-Tab-Sprawl` — Eixo `nav-x-func`):** Proibido criar novas abas (`role="tab"`), sub-abas aninhadas (`switchSubview` dentro de `switchTab`), mais de $3$ blocos `<nav>` (Global, Local, Breadcrumbs) ou múltiplos campos de chat/busca concorrentes. Toda refatoração deve **consolidar e reutilizar os slots/cards/containers já existentes na página**.
3. **Hierarquia Visual Monotônica & Fim das Micro-Fontes Inline (`Anti-Flat-Hierarchy`):** Proibido achatar a interface com dezenas de `style="font-size: 11px|12px|13px"` inline. Exige progressão monotônica real ($H_1 > H_2 > H_3 > \text{Body} \ge 14\text{px} > \text{Caption} \ge 12\text{px}$).
4. **Descompactação de Menus e Tipografia de Navegação (`Anti-Cramped-Menu`):** Proibido conectar ou aprovar menus/abas/pílulas espremidos (`font-size < 13px`, `gap < 6px`, `padding: 4px 8px`, `min-block-size < 40px` ou `scrollWidth > clientWidth`).
5. **Ilusão Visual / Placebo no Grafo e Rotas (`AST Anti-Fake & Next.js 15+`):** Reprova *Ghost Nodes* sem arquivo físico no disco, handlers vazios (`() => {}`), `Math.random()` em telemetria, strings `'[PASS]'` chumbadas estaticamente nos nós, superlotação de `.metric-badge` dentro de nós pequenos e acesso síncrono a `params.slug` no Next.js 15+.

---

## 2. Entradas, Pré-requisitos, Parâmetros e Fronteiras com o Ecossistema Frontend

| Parâmetro | Tipo | Obrigatório | Descrição |
| :--- | :--- | :---: | :--- |
| `target_path` | `string` | Sim | Diretório raiz ou arquivo alvo (`.tsx`, `.ts`, `.css`, `.html`, `mcp_apps_ui_*.go`) a ser auditado. |
| `live_url` | `string` | Recomendado | URL em execução (ex.: `http://localhost:8080/mcp/ui` ou `http://localhost:3000`) para Print + Sonda DOM/CSS no Chrome DevTools. |
| `mode` | `"unified-audit" \| "consolidate-ui" \| "react-cdp"` | Não | Auditoria unificada AST + `nav-x-func` + CDP (`unified-audit`, padrão), refatoração consolidando slots sem criar abas (`consolidate-ui`) ou sonda live (`react-cdp`). |

### Orquestração com o Ecossistema `UI-Architect` e Protocolos de API (`Pre-Flight`)

- **`complex-zero` $\leftrightarrow$ `nav-x-func` (Fusão Direta):** `complex_zero_ast_auditor.py` executa automaticamente `visual_hierarchy_and_cdp_probe.py` e aciona `deterministic_scorer.py` da `nav-x-func` (calculando `SGA` + `TIF` + `INE` + `ICI` + `ICTE` com penalidades reais para menus compactados, proliferação de abas e quebra de hierarquia).
- **`chrome-devtools-mcp` / `a11y-debugging`:** Usados obrigatoriamente na etapa `[2. ACTION]` do ciclo ReAct para tirar print (`take_screenshot`), inspecionar metadados/landmarks (`take_snapshot`) e extrair estilos computados (`evaluate_script`).
- **Ancoragem Pre-Flight de APIs Gemini, WebSockets (`wss://`) e JSON-RPC 2.0 (Proibido Chegar às Cegas):** Ao auditar dashboards com streaming em tempo real, chamadas Gemini API / Live API / Antigravity Agent ou pontes MCP/JSON-RPC, consulte primeiro [`https://aistudio.google.com/docs`](https://aistudio.google.com/docs), [`https://aistudio.google.com/docs/antigravity-agent`](https://aistudio.google.com/docs/antigravity-agent), [`https://aistudio.google.com/llms.txt`](https://aistudio.google.com/llms.txt), [`https://aistudio.google.com/llms-full.txt`](https://aistudio.google.com/llms-full.txt) e [`https://github.com/google-gemini/cookbook`](https://github.com/google-gemini/cookbook) (ou `gemini_search_docs`), e valide o transporte WebSocket / contratos JSON-RPC 2.0 segundo a sub-skill [`../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../agent-server-auditor/references/audit-websocket-jsonrpc.md).

---

## 3. Fluxo de Processamento: Ciclo ReAct Empírico de 4 Estágios (Zero Pseudo-ReAct)

```
[1. THOUGHT & SLOT INVENTORY (Inventário de Elementos Existentes)]
  Mapear os containers/cards/inputs atuais da página.
  REGRA DE OURO: Proibido criar novas abas (`role="tab"`), sub-abas ou novos `<nav>`.
  Planejar onde conectar ou fundir as funções usando APENAS os elementos já existentes.
        |
        v
[2. ACTION (Dupla Sondagem Obrigatória: Script Unificado + Chrome DevTools Live)]
  A) Rodar `complex_zero_ast_auditor.py --target <path> [--live-url <url>]` (que já aciona `nav-x-func`).
  B) No Chrome DevTools MCP (`chrome-devtools-mcp`), executar na página real:
     1. `navigate_page` / `list_pages`
     2. `take_screenshot` (Print visual obrigatório para enxergar menus compactados, colisão e poluição)
     3. `take_snapshot` (Árvore A11y, metadados `<title>`/`<meta>` e contagem de inputs/landmarks)
     4. `evaluate_script` (colando o script de `complex_zero_ast_auditor.py --dump-cdp-script`)
        |
        v
[3. OBSERVATION (Cruzamento Print Visual + Metadados DOM/CSS + AST)]
  Verificar no Print e no JSON do `evaluate_script`:
  - `hierarchyMonotonic`: `fontSize(h1) > fontSize(h2) > fontSize(h3) >= fontSize(body)`?
  - `crampedMenus`: algum menu/botão tem `fontSize < 13px`, `gap < 6px`, `height < 40px` ou `scrollWidth > clientWidth`?
  - `organizationSprawl`: `visibleNavs <= 3`, `allTabs <= 4`, zero sub-abas aninhadas e `visibleInputs <= 2`?
  - `graphNodes`: nós limpos (máx. 2 métricas essenciais), zero `'[PASS]'` hardcoded e zero sobreposição?
        |
        v
[4. SELF-CORRECTION (Consolidação In-Place + Re-Print de Homologação)]
  1. Fundir abas/sub-abas redundantes e remover entradas de chat duplicadas.
  2. Descompactar menus (`font-size: 13px..14px`, `gap: 8px..12px`, `padding: 8px 14px`, `min-block-size: 44px`).
  3. Isolar o Canvas Infinito em viewport amplo (`min-block-size: 520px`) separado de grades densas.
  4. Reexecutar `complex_zero_ast_auditor.py` + `take_screenshot` até `Score >= 90/100` e `SGA >= 85/100`.
```

### Matriz de Pontuação Determinística Adaptativa à Stack (0 a 100 Pontos)

| Eixo | Peso | Critério de Avaliação Contextual (`complex-zero` + `nav-x-func`) | Penalidade Determinística |
| :--- | :---: | :--- | :--- |
| **1. Interatividade, Foco, Lei de Fitts & Menus Descompactados** | **25 pts** | Semântica nativa (`<button>`, `<nav>`), `:focus-visible`, `@media (any-pointer: coarse)` $\ge 48\text{px}$, `prefers-reduced-motion` e **menus/botões legíveis (`font-size >= 13px`, `gap >= 6px`, `min-block-size >= 44px`, zero texto truncado)**. | **`-15 pts` (Crítico)** por menu compactado (`font-size < 13px`, `gap < 6px`, `min-block-size < 40px` ou `padding: 4px 8px`); `-10 pts` por falta de `:focus-visible`. |
| **2. Organização `nav-x-func`, Orçamento de Abas, Hierarquia Visual & `OKLCH`** | **25 pts** | Máximo de **3 `<nav>`** e **até 4 abas primárias** (permitidas quando separam visões distintas), **zero sub-abas aninhadas**, **1 único Composer de chat**, escala monotônica ($H_1 > H_2 > H_3 > \text{Body}$), zero poluição de `style="font-size:11px/12px"` inline, `@container` e `oklch()`. | **`-15 pts` (Crítico)** por excesso de abas (`> 4`), sub-abas aninhadas, `<nav> > 3` ou inputs duplicados; **`-15 pts` (Crítico)** por achatamento de hierarquia / micro-fontes inline (`11px/12px`). |
| **3. Integridade Real-State & AST Anti-Fake (e Grafo `@xyflow` *se presente*)** | **25 pts** | Zero handlers vazios `{}`, zero `Math.random()` fingindo telemetria e zero `'[PASS]'` hardcoded. *Se o projeto usar grafo/canvas 2D*, verifica paridade `1:1` nó $\leftrightarrow$ dados reais, batch `150ms` e nós limpos (máx. 2 métricas no nó; detalhes no inspetor lateral). | **`-15 pts` (Crítico)** por stub vazio `{}`, `Math.random()` placebo, `'[PASS]'` chumbado ou *Ghost Node* (nunca penalize a ausência de `@xyflow` se o projeto não for de grafo). |
| **4. Inspeção Chrome DevTools (Print/Metadados) & Rotas da Stack (Next.js 15+ *se aplicável*)** | **25 pts** | Metadados completos (`<title>`, `<meta name="viewport">`), sonda `evaluate_script` aprovada no navegador real e rotas íntegras (*se for Next.js 15+*, exige `Promise<{ slug: string }>` com `await params` / `use(params)`). | **`-15 pts` (Crítico)** por reprovação na sonda de DOM/metadados ao vivo ou acesso síncrono `params.slug` em projetos Next.js 15+. |

---

## 4. Módulo 1: Protocolo Obrigatório Chrome DevTools MCP (Print Visual + Metadados + DOM/CSS)

Para impedir qualquer "pseudo-auditoria", execute os comandos abaixo para auditar o código e extrair a sonda JS do Chrome DevTools:

```powershell
# 1. Executar auditoria unificada (complex-zero v3.0 + ponte automática nav-x-func v6.0)
uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py --target <caminho_do_projeto>

# 2. Sondar também uma URL local/remota ao vivo
uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py --target <caminho_do_projeto> --live-url http://localhost:8080/mcp/ui

# 3. Exportar o script JS exato para rodar na tool `evaluate_script` do Chrome DevTools MCP
uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py --dump-cdp-script

# 4. Rodar autoteste determinístico
uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py --self-test
```

Quando o servidor MCP **`chrome-devtools-mcp`** estiver disponível, o agente **DEVE** executar a sequência:

1. `navigate_page(url="<live_url>")`
2. `take_screenshot()` — inspecionar visualmente o print procurando:
   - Menus/abas com texto espremido, quebrado em 2 linhas ou pequeno demais,
   - Excesso de barras horizontais empilhadas no topo da página,
   - Dashboard espremido junto com o canvas 2D/grafo,
   - Caixas de entrada de chat/busca repetidas em vários lugares.
3. `take_snapshot()` — verificar a árvore semântica de acessibilidade e os landmarks.
4. `evaluate_script(function="<conteúdo de --dump-cdp-script>")` — validar matematicamente `visualHierarchy.hierarchyMonotonic`, `crampedMenus.length === 0` e `organizationSprawl`.

---

## 5. Módulo 2: Regras de Ouro de Organização, Hierarquia Visual e Reuso In-Place (Fusão `nav-x-func`)

1. **Regra Anti-Novas-Abas (`In-Place Slot Reuse`):**
   - Antes de adicionar qualquer visualização ou controle, faça o inventário dos containers existentes (`<section>`, `<aside>`, cards existentes).
   - **PROIBIDO** criar uma nova aba (`role="tab"`) quando já existem 3–4 abas primárias, e **ESTRITAMENTE PROIBIDO** criar sub-abas dentro de abas (`switchNodesSubview` ou fileiras de botões de modo dentro de uma aba).
   - Se a tela tiver múltiplos inputs de chat/comando, **funda-os em 1 único Composer / Command Bar (`Ctrl+K`)**.
2. **Regra de Descompactação de Menus e Escala Tipográfica Clara:**
   - **Menus, Abas e Botões (`.mode-btn`, `.chip-btn`, `[role="tab"]`):** `font-size >= 0.875rem` (`14px`, mínimo absoluto `13px`), `padding: 8px 14px`, `min-block-size: 44px` (`48px` em `pointer: coarse`), `gap >= 8px` entre itens da barra e `white-space: nowrap`.
   - **Escala de Hierarquia Visual Sem Inline Hardcode:**
     - `H1 / Título Principal`: `clamp(1.35rem, 1.15rem + 0.8vw, 1.85rem)`, `font-weight: 700..800`.
     - `H2 / Título de Ilha`: `clamp(1.1rem, 1rem + 0.4vw, 1.35rem)`, `font-weight: 700`.
     - `Body / Controles Primários`: `clamp(0.925rem, 0.9rem + 0.2vw, 1rem)` (`14.8px..16px`).
     - `Captions / Badges Tabulares`: `0.75rem..0.8125rem` (`12px..13px` — **proibido `< 12px`** e proibido espalhar `style="font-size:11px"` inline).
3. **Regra de Nós Limpos no Grafo (`@xyflow/react` / Canvas 2D):**
   - Cada nó do grafo deve exibir apenas **Identificador Claro (`>= 13px`, `font-weight: 600`) + Tipo (`[DIR]`/`[FILE]`) + no máximo 1 ou 2 métricas compactas essenciais**; os detalhes completos (latência detalhada, heap, preview Base64, diff) devem abrir no **Painel Inspetor Lateral já existente** ao clicar no nó (`Clicar em X ativa Y`), evitando poluir e espremer a caixa do nó!

> Consulte as implementações completas de referência em [`references/react_devtools_and_xyflow_patterns.md`](references/react_devtools_and_xyflow_patterns.md).

---

## 6. Saídas, Entregáveis e Modelo de Relatório de Auditoria Unificado

```markdown
### [RELATÓRIO UNIFICADO DE AUDITORIA VISUAL, ESTRUTURAL & REACT-CDP — COMPLEX-ZERO v3.0 + NAV-X-FUNC v6.0]
- **Alvo Inspecionado:** `<target_path>` | **URL Live / Print:** `<live_url ou N/A>`
- **Score Complex-Zero:** `[XX/100]` (`[PASS >= 90 | WARN 75..89 | FAIL < 75]`)
- **Score Arquitetural `nav-x-func` (`SGA`):** `[XX.XX/100]` (`INE: XX | ICI: XX | IPC: XX | IRM: XX | ICTE: XX | TIF: PASS/FAIL`)

#### 1. Diagnóstico Empírico por Eixo (25 pts cada)
- **[PASS/FAIL] Eixo 1 (Interatividade, Foco, Fitts & Descompactação de Menus):** `[XX/25]` — <Menus `font >= 13px`, `gap >= 8px`, zero truncamento>
- **[PASS/FAIL] Eixo 2 (Organização `nav-x-func`, Reuso Sem Novas Abas, Hierarquia Visual & OKLCH):** `[XX/25]` — <Navs `<= 3`, Tabs `<= 4`, zero sub-abas, escala monotônica>
- **[PASS/FAIL] Eixo 3 (Grafo Real-Time, Nós Limpos & AST Anti-Fake):** `[XX/25]` — <Nós Fantasmas: N | Stubs AST: N | Poluição de Nós: N>
- **[PASS/FAIL] Eixo 4 (Print/Metadados Chrome DevTools & Next.js 15+ Async):** `[XX/25]` — <Evidência do Print + `evaluate_script` + Rotas>

#### 2. Consolidações In-Place e Correções Cirúrgicas Aplicadas
1. `<arquivo:linha>` — <Descrição da consolidação de abas/menus/hierarquia/Real-State aplicada>
```

---

## 7. Exceções, Limites, Guardrails e Quando NÃO Usar

### Quando NÃO Usar (`Should-Not-Trigger`)

- **Não use para** páginas institucionais estáticas simples (Nível 1 sem estado complexo) — prefira `frontend-code-architect`.
- **Não use para** gerar exclusivamente o arquivo `DESIGN.md` do zero — use `design-md`.
- **Não use para** auditoria de motores de Física 3D/WebGL puros — use `code-quality-audit-3d-physics`.
- **Não use para** scripts de backend puro sem interface — use `code-acceptability-auditor` ou `agent-server-auditor`.

### Guardrails Inegociáveis (Zero Pseudo-Auditoria / Zero Pseudo-ReAct)

1. **Proibido Aprovar Sem Inspeção de Organização, Hierarquia e Menus:** Nenhum projeto recebe `[PASS]` se tiver menus com `font-size < 13px`, `gap < 6px`, `min-block-size < 40px` ou dezenas de `style="font-size:11px/12px"` inline.
2. **Proibido Criar Novas Abas na Refatoração:** Sempre reutilize e limpe os elementos/containers já existentes na página; reduza abas e sub-abas em vez de multiplicá-las.
3. **Proibido Omitir Print + `evaluate_script` Quando Houver Servidor/UI Ativa:** Sempre capture o print (`take_screenshot`) e rode a sonda DOM (`--dump-cdp-script`) no Chrome DevTools MCP para validar o resultado real renderizado.
