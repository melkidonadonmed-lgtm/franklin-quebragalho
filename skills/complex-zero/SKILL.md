---
name: complex-zero
description: "Audita via ciclo ReAct (CDP DevTools e AST) aplicações frontend complexas com canvas infinito @xyflow/react, WebSocket Chokidar, nós fantasmas funções falsas e Next.js 15 async params. Use para grafos; não use para páginas simples."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
metadata:
  version: "3.1.0"
  updated_at: "2026-11-13"
  author: "UI-Architect & Melki"
  category: "Frontend de Alta Densidade, Grafos Reativos e Auditoria ReAct/CDP"
  tags: ["frontend", "xyflow", "nextjs-15", "oklch", "container-queries", "ast-analysis", "devtools-cdp"]
---

# `complex-zero` — Auditoria ReAct/CDP, Grafos `@xyflow/react` e AST Anti-Fake

## 1. Propósito e Gatilhos (Quando Usar)

Auditor empírico (Chrome DevTools Print + Sonda DOM + AST, integrado ao `SGA`/`TIF` de [`../auditoria-projetos-sistema/SKILL.md`](../auditoria-projetos-sistema/SKILL.md)) para **interfaces web de alta densidade**: canvas infinito (`@xyflow/react`), cockpits multi-painel, telemetria `WebSocket` + `chokidar` e Next.js 15+:

- Validar abas por domínio (sem duplicatas, plumbing de backend ou sub-abas aninhadas), hierarquia visual monotônica e menus descompactados.
- Detectar *Ghost Nodes*, handlers vazios `() => {}`, `Math.random()` em telemetria e `params.slug` síncrono no Next.js 15+.

## 2. Entradas e Pre-Flight Condicional

- **`target_path` (obrigatório):** Diretório ou arquivo `.tsx`, `.ts`, `.css`, `.html`, `mcp_apps_ui_*.go`.
- **`live_url` (recomendado):** URL ativa (`http://localhost:3000`) para captura e sonda CDP.
- **`mode` (opcional):** `unified-audit` | `consolidate-ui` | `react-cdp`.
- **Pre-Flight Condicional:** Só consulte `google-developer-knowledge` (`search_documents`), `gemini_get_doc` (`chunk_id`), `aistudio.google.com/llms.txt` (evite `gemini_search_docs`, desabilitada) e [`../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../agent-server-auditor/references/audit-websocket-jsonrpc.md) se `target_path` usar `WebSocket`, `@google/genai` ou JSON-RPC 2.0 (jitter, `BATCH_UPDATE` `150ms`).

## 3. Processamento: Ciclo ReAct em 4 Estágios (4 Eixos × 25 pts)

Consulte as regras e penalidades completas em [`references/eixos_e_ciclo_cdp.md`](references/eixos_e_ciclo_cdp.md) e [`references/react_devtools_and_xyflow_patterns.md`](references/react_devtools_and_xyflow_patterns.md):

1. **`[1. THOUGHT]`**: Mapear abas e slots sem esconder desorganização da aba principal.
2. **`[2. ACTION]`**: Rodar `scripts/complex_zero_ast_auditor.py` (invoca `deterministic_scorer.py`) + no Chrome DevTools MCP: `navigate_page` $\to$ `take_screenshot` $\to$ `take_snapshot` $\to$ `evaluate_script` (`--dump-cdp-script`).
3. **`[3. OBSERVATION]`**: Cruzar screenshot com JSON da sonda (`hierarchyMonotonic`, `crampedMenus`, `duplicateTabs`, `backendExposedTabs`, `graphNodes <= 2` métricas).
4. **`[4. SELF-CORRECTION]`**: Saneamento de menus (`>= 13px`, `gap >= 8px`, `min-block-size >= 44px`), Canvas (`>= 520px`) e Next.js 15 `Promise` até `Score >= 90/100`.

```powershell
uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py --target <path> [--live-url <url>]
```

## 4. Saídas e Entregáveis

Relatório (`Alvo | URL | Score Complex-Zero [XX/100] | SGA [XX.XX/100]`) nos 4 Eixos (`[PASS]`/`[FAIL]`/`[UNVERIFIED]`) conforme [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md), com correções `arquivo:linha`.

## 5. Exceções, Limites e Guardrails (Quando NÃO Usar)

- **Fora de Escopo:** Páginas simples (`frontend-code-architect`), criação de `DESIGN.md` (`design-md`), Física 3D (`code-quality-audit-3d-physics`) ou servidores backend sem UI (`agent-server-auditor`).
- **Aprovação Estrita:** Zero `[PASS]` com menus `< 13px`, `Math.random()` em telemetria, stubs `{}` ou ausência de `take_screenshot` + `evaluate_script` quando houver servidor ativo.
