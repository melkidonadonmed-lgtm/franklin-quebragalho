# Critérios Determinísticos de Auditoria — `complex-zero` (`v3.0.0`) + `nav-x-func` (`v6.0.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditoria ReAct empírica (Print Visual + Metadados/DOM no Chrome DevTools MCP/CDP), organização macro/micro (`nav-x-func`), hierarquia visual monotônica, descompactação de menus, reuso in-place sem criar novas abas e engenharia de interfaces complexas (`@xyflow/react`, `WebSocket` em lote de `150ms`, `OKLCH`, `@container` e Next.js 15+ App Router).

---

## 1. Eixo 1: Interatividade Semântica, Fluxo de Foco, Lei de Fitts e Descompactação de Menus (`25 pts` — `[AUDIT-CZ-01]`)

- **`[PASS]`**: Controles interativos utilizam elementos nativos (`<button>`, `<a>`, `<input>`, `<nav>`), preservam a paridade Ordem DOM = Ordem Visual, aplicam a regra LVHA, declaram `:focus-visible`, respeitam `@media (prefers-reduced-motion: reduce)`, garantem alvos visíveis `>= 44x44px` (`>= 48x48px` sob `@media (any-pointer: coarse)`) e **mantêm menus/abas/botões descompactados (`font-size >= 13px`, `gap >= 6px`, `padding >= 8px 12px`, `scrollWidth <= clientWidth`)**.
- **`[FAIL: CRAMPED_MENU_OR_FITTS_VIOLATION]`**: Presença de menus/botões compactados com `font-size < 13px`, barras `<nav>`/`.mode-switcher` com `gap < 6px`, alvos interativos com `min-block-size < 40px` ou `padding: 4px 8px` (`-15 pts`), `<div onClick>` sem `role`/`tabIndex` (`-5 pts`) ou supressão global de foco (`outline: none` sem `:focus-visible`, `-10 pts`).
- **`[UNVERIFIED]`**: Nenhum controle interativo presente no escopo avaliado.

## 2. Eixo 2: Organização `nav-x-func`, Reuso In-Place (Anti-Abas), Hierarquia Visual, `@container` e `OKLCH` (`25 pts` — `[AUDIT-CZ-02]`)

- **`[PASS]`**: Respeita o limite das **3 Camadas de Navegação (`<= 3` tags `<nav>`)**, máximo de **4 abas primárias (`role="tab"`)**, **zero sub-abas aninhadas dentro de abas**, **1 único Composer/Command Bar de chat** (reutilizando os slots existentes da página sem criar novas abas), hierarquia tipográfica monotônica ($H_1 > H_2 > H_3 > \text{Body} \ge 14\text{px} > \text{Caption} \ge 12\text{px}$), zero poluição de `style="font-size: 11px/12px"` inline, `@container` (`container-type: inline-size`), tokens em `oklch()` ($L = 0.16 \to 0.22 \to 0.27$) e `tabular-nums`.
- **`[FAIL: SPRAWL_HIERARCHY_OR_CONTAINER_VIOLATION]`**: Proliferação de abas/sub-abas aninhadas ou mais de 3 `<nav>` na página (`-15 pts`), múltiplos campos de entrada/chat concorrentes sem unificação (`-15 pts`), achatamento de hierarquia visual por abuso de micro-fontes inline `11px/12px` (`-15 pts`), ausência de `@container`/`oklch()` (`-10 pts`) ou validação de contraste hardcoded (`oklchContrastValid: true`, `-15 pts`).

## 3. Eixo 3: Grafo Reativo Real-Time (`@xyflow/react`), Nós Limpos & AST Anti-Fake (`25 pts` — `[AUDIT-CZ-03]`)

- **`[PASS]`**: Uso do pacote moderno `@xyflow/react` (ou canvas 2D isolado em viewport `>= 520px`), `WebSocket` + `chokidar` com debounce/lote de `150ms` (`BATCH_UPDATE`), paridade `1:1` entre nós do grafo e arquivos físicos no disco (`fs.existsSync` com confinamento contra Path Traversal), zero funções vazias (`{}`), zero stubs (`console.log`/`alert`), zero emojis, **zero strings `'[PASS]'` chumbadas estaticamente nos nós** e **máximo de 2 badges compactos por nó** (delegando detalhes ao painel inspetor lateral já existente).
- **`[FAIL: GHOST_NODE_PLACEBO_OR_OVERSTUFFING]`**: Presença de nós fantasmas apontando para arquivos inexistentes (`-15 pts`), handlers vazios/stubs (`-15 pts`), telemetria falsificada com `Math.random()` (`-15 pts`), badge `'[PASS]'` hardcoded no template do nó (`-15 pts`) ou superlotação de `.metric-badge` espremidos dentro do card do nó (`-8 a -15 pts`).

## 4. Eixo 4: Inspeção Visual Chrome DevTools (Print + Metadados DOM) & Next.js 15+ Async (`25 pts` — `[AUDIT-CZ-04]`)

- **`[PASS]`**: Execução do protocolo Chrome DevTools MCP (`take_screenshot` + `take_snapshot` + `evaluate_script` via `--dump-cdp-script`) comprovando hierarquia visual monotônica e zero menus espremidos no DOM renderizado, metadados completos (`<title>`, `<meta name="viewport">`, `<meta name="description">`) e, em rotas Next.js 15+ App Router, tipagem `params: Promise<{ slug: string }>` consumida com `await params` ou `use(params)`.
- **`[FAIL: LIVE_DOM_OR_SYNC_PARAMS_VIOLATION]`**: Reprovação na sonda de DOM/metadados em runtime (`-10 a -15 pts`) ou acesso síncrono direto a `params.slug` / `searchParams` sem `await` ou `use()` no Next.js 15+ (`-15 pts`).
