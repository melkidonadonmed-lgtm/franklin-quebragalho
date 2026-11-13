# Os 4 Eixos, Pré-Flight e Ciclo ReAct/CDP — `complex-zero`

Referência estendida consumida por [`../SKILL.md`](../SKILL.md) e integrada a [`react_devtools_and_xyflow_patterns.md`](react_devtools_and_xyflow_patterns.md) e [`../../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../../agent-server-auditor/references/audit-websocket-jsonrpc.md).

## 5 Falhas Estruturais Bloqueadas

1. **Fim do Pseudo-ReAct (Chrome DevTools Real):** Exige `take_screenshot` + `take_snapshot` + `evaluate_script` (`getComputedStyle` e `getBoundingClientRect`) quando houver URL ativa.
2. **Governança Semântica de Abas (`Domain-Tab Separation` vs. `Anti-Duplicate-Tab`):** Abas primárias (`role="tab"`) podem separar domínios distintos, mas proíbem: (a) abas com função duplicada, (b) novas abas com aba principal bagunçada, (c) exposição de plumbing interno de backend como aba e (d) sub-abas aninhadas (`switchSubview` em `switchTab`) ou `> 3` blocos `<nav>`.
3. **Hierarquia Monotônica (`Anti-Flat-Hierarchy`):** Bloqueia `style="font-size: 11px|12px"` inline; exige $H_1 > H_2 > H_3 > \text{Body} \ge 14\text{px} > \text{Caption} \ge 12\text{px}$.
4. **Menus Legíveis (`Anti-Cramped-Menu`):** Bloqueia `font-size < 13px`, `gap < 6px`, `min-block-size < 40px` ou `scrollWidth > clientWidth`.
5. **AST Anti-Fake & Next.js 15+:** Bloqueia *Ghost Nodes*, handlers `() => {}`, `Math.random()` em telemetria, `'[PASS]'` hardcoded, `> 2` métricas por card de nó e acesso síncrono a `params.slug`.

## Matriz de Pontuação (25 pts por Eixo)

| Eixo | Critério Determinístico | Penalidade Principal |
| :--- | :--- | :--- |
| **1. Interatividade, Fitts, INP & Menus (`25 pts`)** | Elementos nativos, `:focus-visible`, `@media (any-pointer: coarse)` $\ge 48\text{px}$, `prefers-reduced-motion`, `transition-behavior: allow-discrete` separado, `content-visibility: auto`, menus `>= 13px`/`gap >= 6px`/`min-block-size >= 44px`. | `-15 pts` menu compactado; `-10 pts` sem `:focus-visible`. |
| **2. Coesão de Abas, Hierarquia & `OKLCH` (`25 pts`)** | `<= 3 <nav>`, zero abas duplicadas/backend/sub-abas, 1 Composer, escala monotônica, `@container` e `oklch()`. | `-15 pts` abas inválidas ou `<nav> > 3`; `-15 pts` micro-fontes inline. |
| **3. Grafo Real-State & AST Anti-Fake (`25 pts`)** | Zero `{}` vazios/`Math.random()`/`'[PASS]'`; grafo `@xyflow/react` 1:1 com disco, lote `150ms` e `<= 2` métricas/nó. | `-15 pts` por placebo, superlotação ou *Ghost Node*. |
| **4. Sonda DevTools & Rotas Next.js 15+ (`25 pts`)** | `<title>`, `<meta name="viewport">`, sonda `evaluate_script` e `params: Promise<{ slug: string }>` com `await`/`use()`. | `-15 pts` falha DOM ou acesso síncrono a `params.slug`. |
