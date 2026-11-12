---
name: complex-zero
description: "Audita via ciclo ReAct (CDP DevTools e AST) aplicações frontend complexas com canvas infinito @xyflow/react, WebSocket Chokidar, nós fantasmas funções falsas e Next.js 15 async params. Use para grafos; não use para páginas simples."
version: "3.1.0"
updated_at: "2026-11-12"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
allowed-tools: ["read_file", "write_file", "edit_file", "run_command", "call_mcp_tool"]
metadata:
  version: "3.1.0"
  updated_at: "2026-11-12"
  author: "UI-Architect & Melki"
  category: "Frontend de Alta Densidade, Grafos Reativos e Auditoria ReAct/CDP"
  tags: ["frontend", "xyflow", "nextjs-15", "oklch", "container-queries", "ast-analysis", "devtools-cdp"]
---
# Skill: `complex-zero` (`v3.1.0`) — Auditoria ReAct Visual/CDP, Coesão de Abas por Domínio, Hierarquia Visual e AST Anti-Fake

## 1. Visão Geral, Propósito e Gatilhos de Ativação (Quando Usar)

Atua como auditor empírico (Chrome DevTools Print + DOM/CSS Computado) e arquiteto determinístico (`0 a 100` pontos integrado ao `SGA`/`TIF` de [`auditoria-projetos-sistema` `v6.0.0`](../auditoria-projetos-sistema/SKILL.md)) para **interfaces web de alta densidade**: editores em canvas infinito (`@xyflow/react` / mapas 2D), cockpits multi-painel, telemetria reativa (`WebSocket` + `chokidar`) e rotas **Next.js 15+ App Router**.

Elimina **5 falhas estruturais e visuais críticas**:

1. **Fim do Pseudo-ReAct (Inspeção Real via Chrome DevTools):** Quando houver UI ativa, exige evidência empírica (`take_screenshot` + `take_snapshot` + `evaluate_script` com `getComputedStyle` e `getBoundingClientRect`).
2. **Governança Semântica de Abas (`Domain-Tab Separation` vs. `Anti-Duplicate-Tab`):** Criar abas primárias (`role="tab"`) para **separar domínios/visões genuinamente distintos É PERMITIDO**. É **estritamente proibido**: **(a)** criar novas abas com a **mesma função** de uma existente, **(b)** abrir abas extras **enquanto a aba principal ainda estiver bagunçada/não saneada**, **(c)** expor **componentes internos de backend** (filas cruas, tabelas internas, configs de infraestrutura) como abas de UI e **(d)** criar sub-abas aninhadas dentro de abas (`switchSubview` dentro de `switchTab`) ou `> 3` blocos `<nav>`.
3. **Hierarquia Visual Monotônica (`Anti-Flat-Hierarchy`):** Bloqueia poluição de `style="font-size: 11px|12px"` inline e exige progressão real ($H_1 > H_2 > H_3 > \text{Body} \ge 14\text{px} > \text{Caption} \ge 12\text{px}$).
4. **Descompactação de Menus (`Anti-Cramped-Menu`):** Reprova menus/abas espremidos (`font-size < 13px`, `gap < 6px`, `min-block-size < 40px` ou `scrollWidth > clientWidth`).
5. **Integridade AST Anti-Fake & Next.js 15+:** Reprova *Ghost Nodes* sem arquivo físico, handlers vazios (`() => {}`), `Math.random()` em telemetria, strings `'[PASS]'` hardcoded nos nós, superlotação de badges no card do nó (`> 2` métricas) e acesso síncrono a `params.slug` no Next.js 15+.

---

## 2. Entradas, Parâmetros e Protocolo Condicional de Pre-Flight

| Parâmetro | Tipo | Obrigatório | Descrição |
| :--- | :--- | :---: | :--- |
| `target_path` | `string` | Sim | Diretório ou arquivo alvo (`.tsx`, `.ts`, `.css`, `.html`, `mcp_apps_ui_*.go`). |
| `live_url` | `string` | Recomendado | URL ativa (ex.: `http://localhost:3000`) para Print + Sonda DOM no Chrome DevTools. |
| `mode` | `"unified-audit" \| "consolidate-ui" \| "react-cdp"` | Não | Auditoria completa (`unified-audit`), saneamento estrutural (`consolidate-ui`) ou sonda live (`react-cdp`). |

### Protocolo Condicional de Pre-Flight (WebSockets, Gemini Live & JSON-RPC)

- **Quando NÃO acionar:** Em dashboards puramente locais, REST/SSR padrão ou grafos estáticos sem streaming — **não desperdice contexto** auditando WebSockets ou SDKs de IA.
- **Quando acionar:** **Exclusivamente** quando `target_path` importar ou instanciar `WebSocket` (`ws://`/`wss://`), `@google/genai` / Live API ou pontes MCP/JSON-RPC 2.0.
- **Como executar:** Consulte assinaturas atuais via `gemini_search_docs` (quando houver SDK Gemini) e valide reconexão com jitter, lote `150ms` (`BATCH_UPDATE`) e envelope JSON-RPC 2.0 contra [`../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../agent-server-auditor/references/audit-websocket-jsonrpc.md).

---

## 3. Fluxo de Processamento: Ciclo ReAct Empírico em 4 Estágios

1. **`[1. THOUGHT & DOMAIN INVENTORY]`**: Mapeie a aba principal e os slots existentes (`<section>`, `<aside>`). Saneie **primeiro** a aba principal; separe em abas distintas apenas domínios funcionais independentes, sem duplicar função nem vazar componentes de backend.
2. **`[2. ACTION (Script AST + Chrome DevTools)]`**:
   - Execute `uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py --target <path> [--live-url <url>]` (aciona automaticamente `deterministic_scorer.py` de `auditoria-projetos-sistema`).
   - Com servidor ativo e `chrome-devtools-mcp`, execute: `navigate_page` $\rightarrow$ `take_screenshot` $\rightarrow$ `take_snapshot` $\rightarrow$ `evaluate_script` (com a sonda de `--dump-cdp-script`).
3. **`[3. OBSERVATION]`**: Cruze o print visual com o JSON da sonda (`hierarchyMonotonic`, `crampedMenus`, `duplicateTabs`, `backendExposedTabs` e `graphNodes` com `<= 2` métricas e detalhes no inspetor lateral).
4. **`[4. SELF-CORRECTION]`**: Saneie a aba principal, funda apenas abas de função duplicada, remova abas de plumbing interno, descompacte menus (`font-size: 13px..14px`, `gap >= 8px`, `min-block-size >= 44px`), isole o Canvas Infinito (`min-block-size: 520px`) e revalide até `Score >= 90/100`.

### Matriz de Pontuação Determinística (0 a 100 Pontos — 25 pts por Eixo)

| Eixo | Critério Determinístico | Penalidade Principal |
| :--- | :--- | :--- |
| **1. Interatividade, Foco, Fitts & Menus (`25 pts`)** | Elementos nativos (`<button>`, `<nav>`), `:focus-visible`, `@media (any-pointer: coarse)` $\ge 48\text{px}$, `prefers-reduced-motion` e menus legíveis (`font-size >= 13px`, `gap >= 6px`, `min-block-size >= 44px`). | **`-15 pts`** por menu compactado; **`-10 pts`** sem `:focus-visible`. |
| **2. Coesão de Abas, Hierarquia & `OKLCH` (`25 pts`)** | `<= 3 <nav>`, abas primárias distintas por domínio (zero abas duplicadas, zero abas de backend interno, zero sub-abas aninhadas), 1 único Composer de chat, escala monotônica, `@container` e `oklch()`. | **`-15 pts`** por abas duplicadas/backend/sub-abas ou `<nav> > 3`; **`-15 pts`** por micro-fontes inline (`11px/12px`). |
| **3. Grafo Real-State & AST Anti-Fake (`25 pts`)** | Zero handlers vazios `{}`, zero `Math.random()` em métricas, zero `'[PASS]'` hardcoded. Se houver grafo `@xyflow/react`: paridade `1:1` com disco, lote `150ms` e `<= 2` métricas por nó (detalhes no inspetor lateral). | **`-15 pts`** por stub vazio, `Math.random()`, `'[PASS]'` hardcoded, superlotação de nó ou *Ghost Node*. |
| **4. Sonda DevTools & Rotas Next.js 15+ (`25 pts`)** | `<title>`, `<meta name="viewport">`, sonda `evaluate_script` aprovada e, em Next.js 15+, `params: Promise<{ slug: string }>` consumido com `await` / `use()`. | **`-15 pts`** por falha na sonda DOM ou acesso síncrono a `params.slug`. |

> Implementações de referência completas (`devtools_auditor.ts`, `ast_integrity_checker.ts`, `CustomMetricNode.tsx` com `<= 2` métricas e `metrics_watcher.ts`) em [`references/react_devtools_and_xyflow_patterns.md`](references/react_devtools_and_xyflow_patterns.md).

---

## 4. Saídas, Entregáveis e Modelo de Relatório

Emita relatório executivo contendo:
- **Cabeçalho**: `Alvo | URL Live | Score Complex-Zero [XX/100] | SGA (auditoria-projetos-sistema) [XX.XX/100]`.
- **Diagnóstico nos 4 Eixos (`[PASS]` / `[FAIL]` / `[UNVERIFIED]`)** conforme [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).
- **Correções Cirúrgicas (`arquivo:linha`)**: Saneamento da aba principal, fusão de abas de função repetida, remoção de abas de backend, descompactação de menus e eliminação de placebos AST.

---

## 5. Exceções, Limites e Guardrails (Quando NÃO Usar)

- **Não use para** páginas estáticas simples sem estado denso (`frontend-code-architect`), criação isolada do `DESIGN.md` (`design-md`), motores de Física 3D/WebGL (`code-quality-audit-3d-physics`) ou servidores backend sem UI (`agent-server-auditor`).
- **Guardrails Inegociáveis:**
  1. **Saneie a Aba Principal Primeiro:** Nunca crie abas adicionais para esconder desorganização da aba principal, nunca crie abas com função duplicada e nunca exponha componentes internos de backend como abas de usuário.
  2. **Zero Aprovação com Menus Espremidos ou Placebos:** Reprove imediatamente `font-size < 13px` em navegação, `gap < 6px`, `Math.random()` fingindo telemetria ou handlers vazios `{}`.
  3. **Evidência Real Quando Houver Servidor Ativo:** Capture `take_screenshot` + `evaluate_script` (`--dump-cdp-script`) no Chrome DevTools MCP antes de homologar `[PASS]`.
