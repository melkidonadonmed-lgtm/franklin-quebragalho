# ESTADO ATUAL, TRAVAS ARQUITETURAIS & CHANGELOG (`CURRENT_STATE.md`)

> **Propósito:** Fonte de verdade histórica e trava anti-regressão (*Architectural Lock*) sincronizada entre o repositório `franklin-quebragalho` (`CURRENT_STATE.md`) e a memória global (`C:\Users\melki\.gemini\`). Qualquer agente deve ler este arquivo e `.context/context.md` (`CONTEXT.md`) antes de alterar skills, regras, contratos MCP ou documentos-base.

---

## 1. Snapshot do Estado Atual (`2026-11-13`)

| Dimensão | Estado Canônico Verificado no Disco | Fonte de Verdade / Validador |
| :--- | :--- | :--- |
| **Tríade de Governança v2.0** | `AGENTS.md` (SSOT raiz; `.agents/AGENTS.md` espelhado apenas nos repositórios externos), `CONTEXT.md` $\leftrightarrow$ `.context/context.md`, `SPEC.md` $\leftrightarrow$ `.context/spec.md` | Sincronizados automaticamente por `scripts/sync_gemini_ecosystem.py` |
| **Skills Canônicas** | **`29 Skills`** em `skills/` (após fusão 3-em-1 em `auditoria-projetos-sistema` `v6.0.0`) | `uv run python scripts/validate_skills.py` (`29/29 PASS`) |
| **Subagentes Declarativos** | **`10 Subagentes`** em `agents/*.md` (Topologia `3+1` de UI + `review-squad` + `adk-go-operator` + `dev-workspace-publisher` + `intent-hitl-mediator` + `read-after-write-verifier` + `vault-memory-retriever`) | `scripts/sync_gemini_ecosystem.py` $\to$ `~/.gemini/config/agents/` e `.agents/agents/` |
| **Regras do Ecossistema (`rules/`)** | **`2 Regras Globais`** (`diretrizes-qualidade-eficiencia.md`, `diretrizes-frontend-9-eixos.md`) + **`5 Regras Condicionais`** (`authoring-*.md`) | Sincronizadas 1:1 com `C:\Users\melki\.gemini\config\rules\` e `plugins\franklin-skills\rules\` |
| **Servidor MCP (`server.py`)** | **`13 Tools`**, **`8 Resources`** e **`2 Prompts`** (`franklin-skills`) | `mcp_config.json` $\leftrightarrow$ `C:\Users\melki\.gemini\config\mcp_config.json` |
| **Identidade A2A (`v1.0` JWS)** | `.well-known/agent-card.json` e `agent_card.json` com **29 skill IDs** e `tags` completas | `shared/a2a_bridge.py` (`HMAC-SHA256` + RFC 8785 JCS) |
| **Snapshot de Auditoria** | `memories/audit_report.json` (`100.0/100 APPROVED`, `29` skills) | Regenerado automaticamente por `sync_gemini_ecosystem.py` |
| **Suíte de Testes** | **`104/104 PASS`** em 11 suítes (`tests/test_*.py`), precisão de disparo Top-1 `F1 = 1.0` | `uv run pytest -q` |

---

## 2. Travas Arquiteturais Imutáveis (*Architectural Locks* — Proibido Regredir)

1. **`[LOCK-01]` Fusão 3-em-1 em `auditoria-projetos-sistema` (`v6.0.0`):**
   - As antigas skills `antigravity-project-auditor` e `nav-x-func` foram **permanentemente fundidas** em [`skills/auditoria-projetos-sistema/SKILL.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/auditoria-projetos-sistema/SKILL.md).
   - **Proibido** recriar as pastas `skills/antigravity-project-auditor/` ou `skills/nav-x-func/`, ou fazer auditoria que leia apenas `.md` sem rodar `project_structure_and_code_auditor.py`, `deterministic_scorer.py` e `frontiercode_maintainability_guardrail.py`.
   - Os nomes legados (`antigravity-project-auditor`, `project-auditor`, `mvp`, `nav-x-func`, `nav`, `arquitetura`, `ilhas`) permanecem exclusivamente como **aliases de redirecionamento** em `shared/catalog_service.py` apontando para `auditoria-projetos-sistema`.
2. **`[LOCK-02]` Regra `60-30-10` com Cores `OKLCH` e Sombras em 3 Camadas Reais:**
   - Toda auditoria e implementação visual (incluindo `templates/universal-app/src/canvas/elevationRenderer.ts`, `globals.css` e `google-drive-index-app/src/index.css`) deve aplicar a proporção **`60-30-10`** em **`oklch(L C H / alpha)`** + `light-dark()`, separar primitivas (`--shadow-layer-sm/md/lg`) de tokens semânticos (`--shadow-elevation-1..3` / `--shadow-elevation-low/medium/high` / `--elevation-1..3` + `--shadow-inset` / `--shadow-inset-sunken` / `--elevation-pressed-inset`) e garantir **3 camadas ópticas reais** em todos os níveis: **Umbra de Contato + Penumbra Difusa (`spread` negativo `-1px` a `-8px`) + Borda Especular Zenital (`inset 0 1px 0 0` / `--catch-light`)** (somando *Ambient Brand Glow* no Dark Mode).
3. **`[LOCK-03]` Sincronia Obrigatória Projeto $\leftrightarrow$ Memória Global (`~/.gemini` & `.agents/` / `.context/`):**
   - Toda alteração em `skills/`, `agents/`, `rules/`, `AGENTS.md`, `SPEC.md`, `CONTEXT.md` ou `CURRENT_STATE.md` deve ser seguida da execução de `uv run python scripts/sync_gemini_ecosystem.py`, que sincroniza `AGENTS.md` (podando `.agents/AGENTS.md` neste repositório-raiz e espelhando `.agents/AGENTS.md` nos externos), `.context/context.md`, `.context/spec.md` (em `franklin-quebragalho` e nos repositórios com Tríade espelhada como `adk-go-mcp`, `adk-py-agents`, `adk-ts-agent`, `GoSTylo`, `PCM`), `C:\Users\melki\.gemini\config\rules\`, `C:\Users\melki\.gemini\config\plugins\franklin-skills\`, `.well-known/agent-card.json` e `memories/audit_report.json`.

---

## 3. Histórico de Evolução (Changelog Consolidado)

### `[2026-11-13]` — Fase 33: Baseline Gemini 4, Decisions API, Antigravity `Orchestrator`, SDKs `googleapis` (`v1` vs `v1beta`) & Watchdog `official_sources.json` (24 Fontes)

- **Gemini 4, Managed Agents & `googleapis` SDK Baselines:** Atualizadas regras (`authoring-rules-and-google-apis.md`, `authoring-subagents.md`, `diretrizes-qualidade-eficiencia.md`), `AGENTS.md`, `MY_AGENTS.md`, `MY_SKILLS.md`, `CONTEXT.md`, skills/referências (`agent-server-auditor` `v1.2.0`, `auditoria-projetos-sistema`, `complex-zero`, `organizador-projetos-ideias`, `re-a-ndroid`, `arquiteto-conteudo-solucoes`, `test-quality-auditor`) e `tests/test_ecosystem_contracts.py` (`104/104 PASS`) com Gemini 4 (`gemini-4-hydrogen` c/ `xhigh`, `gemini-4-argon`, `gemini-4-carbon`), `gemini-decision-1`, `antigravity-preview-09-2026` (`Orchestrator` + BYOS), `gemini-3.8-live*`/`tts`/`gemini-omni-1.2-flash`, baselines `googleapis` (`python/js-genai>=3.3.0`, `java-genai>=2.3.0`, `kotlin-genai>=2.1.0`, `Google.GenAI>=2.1.0`, `go-genai>=1.77.0`, ADK `v2.14.1`/`v2.7.1`/`v2.5.0`) e nota da mudança `v1` vs `v1beta` (`HttpOptions(api_version='v1beta')` / `GOOGLE_GENAI_API_VERSION=v1beta`).
- **Specs Lock & Higiene:** Expandido [`references/official_sources.json`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/references/official_sources.json) para **24 fontes vivas** (`aistudio.google.com/docs/{deprecations,latest-model,antigravity-agent}.md` + 6 `CHANGELOG.md` oficiais de `googleapis/*-genai`) e removido uso legado de `enable_write_tools`, `gemini_search_docs` e `call_mcp_tool` em `tools:` de subagentes.

### `[2026-11-13]` — Fase 32: Arquitetura de Referências Canônicas Tier-3 de Frontend (`Exemplos App` + `modern-web-guidance` + Google Stitch + Tailwind v4 `@theme` + Next.js 15 / React 19)

- **Novas Referências Tier-3 e Upgrade de Skills/Subagentes/Auditores:** Criados [`skills/design-md/references/spacing_tokens_and_stitch_hierarchy.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/design-md/references/spacing_tokens_and_stitch_hierarchy.md) e [`skills/frontend-code-architect/references/layout_grid_cards_and_navigation.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-code-architect/references/layout_grid_cards_and_navigation.md), além da atualização das referências de `design-md`, `frontend-code-architect`, `frontend-ui-ux-auditor`, `frontend-testing-auditor`, `auditoria-projetos-sistema` e `plan-uiux`, das 7 `SKILL.md` de frontend, dos 4 subagentes `agents/ui-*.md`, do SSOT [`rules/diretrizes-frontend-9-eixos.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/rules/diretrizes-frontend-9-eixos.md) e dos 3 auditores determinísticos (`ui_ux_frontend_auditor.py`, `audit_tactile_ui.py`, `deterministic_scorer.py`) cobrindo:
  1. **Espaçamento UX/UI & Tokens (Google Stitch & Tailwind v4 `@theme`):** Dupla camada de tokens (`--space-0-5..16` + semânticos `--space-inline-icon`, `--space-card-gap`, `--space-card-padding`, `--space-grid-gap`, `--space-section-inset`), Proximidade de Gestalt, Raios Concêntricos ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$), `display: flow-root` e `:where([data-density])`.
  2. **Flexbox (1D) vs. CSS Grid (2D) vs. Subgrid & Cards:** Padrão RAM `minmax(min(100%, 280px), 1fr)`, `flex-wrap: balance`, `align-items: safe center`, `min-inline-size: 0`, `<article>` de 4 regiões com `subgrid` (separado do nó `container-type`), mídia condicional `.card:has(> img)`, clickable `a.card-link::after` stretch e React 19 sem `forwardRef`.
  3. **Hierarquia Visual, Navegação Adaptável & Fluidez (INP/LCP):** `clamp()` ($\max \le 2.5\times \min$), `max-inline-size: 60ch–65ch`, `tabular-nums`, `feColorMatrix`, Navegação de Único DOM (Bottom Bar com `env(safe-area-inset-bottom)` $\leftrightarrow$ Sidebar Rail `240px` `100dvh` + Popover intrínseco via `ResizeObserver`), `any-pointer: coarse` (`48x48px`), `transition-behavior: allow-discrete` declarado em propriedade separada, View Transitions, Predictive Back e `content-visibility: auto`.

### `[2026-11-09]` — Fase 31: Padronização da Tríade de Governança v2.0 (`AGENTS.md`, `CONTEXT.md`, `SPEC.md` + `.agents/` e `.context/`), Higienização de Pastas & Organização `adk-tests`

- **Padronização Canônica v2.0:** Alinhamento estrutural de [`AGENTS.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/AGENTS.md) (Kernel Operacional v2.0 + 7 Regras de Ouro + 8 Personas + 10 Subagentes + Memória Evolutiva + Fechamento Self-Refine, sem cópia redundante em `.agents/AGENTS.md`), [`CONTEXT.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CONTEXT.md) / [`.context/context.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/context.md) (Visão Geral, Decisões Críticas, Changelog e Backlog) e [`SPEC.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/SPEC.md) / [`.context/spec.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/spec.md) (Scope Lock, Contratos I/O e Critério de Aceite).
- **Higienização e Sincronia Multi-Repo (`franklin-quebragalho`, `adk-tests` e `~/.agents/skills`):** Removidos arquivos redundantes/poluentes (`shared/{AGENTS,CLAUDE,CONTEXT,SPEC}.md`, `.context/{CURRENT_STATE,SESSION_LOG}.md`, `Indice_Google_Drive.html`, `workspace_index.json`, `skills/arquiteto-conteudo-solucoes/README.md`, `adk-tests/bin/adk_sessions.db*`, `adk-tests/go_agent/benchmark.json` e `.rea.backup`), restauradas as skills externas de `~/.agents/skills` sem arquivos sintéticos e espelhada a Tríade de Governança v2.0 também em `adk-tests` via `scripts/sync_gemini_ecosystem.py`.

### `[2026-11-03]` — Fase 30: Fusão Canônica de Auditoria (`v6.0.0`), Governança `rules/` + `CURRENT_STATE.md` e Sincronia Global

- **Fusão 3-em-1 (`auditoria-projetos-sistema` `v6.0.0`):** Incorporou `antigravity-project-auditor` (diagnóstico causal de MVP e 5 pilares) e `nav-x-func` (Navegação em 3 Camadas, `X ativa Y`, `SGA` + `TIF` e template `V1 vs V2`), adicionando o novo scanner real `scripts/project_structure_and_code_auditor.py` e reduzindo o catálogo de `31` para **`29 Skills Canônicas`** sem sobreposição.
- **Governança e Prevenção de Drift:** Criada a pasta `rules/` na raiz do projeto sincronizada com `~/.gemini/config/rules/`, criado `CURRENT_STATE.md` com travas anti-regressão e reescritos `AGENTS.md`, `SPEC.md` e `CONTEXT.md` de forma enxuta e interligada.
- **Correção de Sombras em Camadas (`elevationRenderer.ts`):** Refatorado o pipeline Canvas 2D e `globals.css` do `universal-app` para 3 níveis de elevação + recesso `sunken` com 3 camadas ópticas (Penumbra Difusa + Umbra de Contato + Rim Light Zenital + Anel 1px) em `OKLCH`.
- **Alinhamento de `server.py`, `mcp_config.json`, `agent-card.json` e `memories/audit_report.json`:** Enxugados `@mcp.resource` e `@mcp.prompt` em `server.py`, unificado `mcp_config.json`, garantidas `tags` completas nos 29 cards A2A e automatizada a atualização de `memories/audit_report.json` no `sync_gemini_ecosystem.py`.

### `[2026-10-27 a 2026-11-02]` — Fases 28 e 29: SSOT em 9 Eixos, A2A v1.0 JWS e Módulos Especialistas (`re-a-ndroid`, `android-agy-projects`, `plan-uiux`, `audit-skills-antigravity`, `complex-zero`)

- Consolidação do Guia Mestre SSOT em 9 Eixos (`Preferências de Trabalho com Agentes.md`), Topologia `3+1` de Subagentes de UI (`ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer`), assinatura criptográfica JCS/JWS no `AgentCard` e auditores poliglotas (`agent-server-auditor`, `test-quality-auditor` v1.3, `code-acceptability-auditor` v1.1).
