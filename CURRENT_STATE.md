# ESTADO ATUAL, TRAVAS ARQUITETURAIS & CHANGELOG (`CURRENT_STATE.md`)

> **Propósito:** Fonte de verdade histórica e trava anti-regressão (*Architectural Lock*) sincronizada entre o repositório `franklin-quebragalho` (`CURRENT_STATE.md`) e a memória global (`C:\Users\melki\.gemini\`). Qualquer agente deve ler este arquivo e `.context/context.md` (`CONTEXT.md`) antes de alterar skills, regras, contratos MCP ou documentos-base.

---

## 1. Snapshot do Estado Atual (`2026-11-09`)

| Dimensão | Estado Canônico Verificado no Disco | Fonte de Verdade / Validador |
| :--- | :--- | :--- |
| **Tríade de Governança v2.0** | `AGENTS.md` $\leftrightarrow$ `.agents/AGENTS.md`, `CONTEXT.md` $\leftrightarrow$ `.context/context.md`, `SPEC.md` $\leftrightarrow$ `.context/spec.md` | Sincronizados automaticamente por `scripts/sync_gemini_ecosystem.py` |
| **Skills Canônicas** | **`29 Skills`** em `skills/` (após fusão 3-em-1 em `auditoria-projetos-sistema` `v6.0.0`) | `uv run python scripts/validate_skills.py` (`29/29 PASS`) |
| **Subagentes Declarativos** | **`10 Subagentes`** em `agents/*.md` (Topologia `3+1` de UI + `review-squad` + `adk-go-operator` + `dev-workspace-publisher` + `intent-hitl-mediator` + `read-after-write-verifier` + `vault-memory-retriever`) | `scripts/sync_gemini_ecosystem.py` $\to$ `~/.gemini/config/agents/` e `.agents/agents/` |
| **Regras do Ecossistema (`rules/`)** | **`2 Regras Globais`** em `rules/` (`diretrizes-qualidade-eficiencia.md` e `diretrizes-frontend-9-eixos.md`) | Sincronizadas 1:1 com `C:\Users\melki\.gemini\config\rules\` |
| **Servidor MCP (`server.py`)** | **`13 Tools`**, **`8 Resources`** e **`2 Prompts`** (`franklin-skills`) | `mcp_config.json` $\leftrightarrow$ `C:\Users\melki\.gemini\config\mcp_config.json` |
| **Identidade A2A (`v1.0` JWS)** | `.well-known/agent-card.json` e `agent_card.json` com **29 skill IDs** e `tags` completas | `shared/a2a_bridge.py` (`HMAC-SHA256` + RFC 8785 JCS) |
| **Snapshot de Auditoria** | `memories/audit_report.json` (`100.0/100 APPROVED`, `29` skills, `13` agentes) | Regenerado automaticamente por `sync_gemini_ecosystem.py` |
| **Suíte de Testes** | **`83/83 PASS`** em 9 suítes (`tests/test_*.py`), precisão de disparo Top-1 `F1 = 1.0` | `uv run pytest -q` |

---

## 2. Travas Arquiteturais Imutáveis (*Architectural Locks* — Proibido Regredir)

1. **`[LOCK-01]` Fusão 3-em-1 em `auditoria-projetos-sistema` (`v6.0.0`):**
   - As antigas skills `antigravity-project-auditor` e `nav-x-func` foram **permanentemente fundidas** em [`skills/auditoria-projetos-sistema/SKILL.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/auditoria-projetos-sistema/SKILL.md).
   - **Proibido** recriar as pastas `skills/antigravity-project-auditor/` ou `skills/nav-x-func/`, ou fazer auditoria que leia apenas `.md` sem rodar `project_structure_and_code_auditor.py`, `deterministic_scorer.py` e `frontiercode_maintainability_guardrail.py`.
   - Os nomes legados (`antigravity-project-auditor`, `project-auditor`, `mvp`, `nav-x-func`, `nav`, `arquitetura`, `ilhas`) permanecem exclusivamente como **aliases de redirecionamento** em `shared/catalog_service.py` apontando para `auditoria-projetos-sistema`.
2. **`[LOCK-02]` Regra `60-30-10` com Cores `OKLCH` e Sombras em 3 Camadas Reais:**
   - Toda auditoria e implementação visual (incluindo `templates/universal-app/src/canvas/elevationRenderer.ts` e `globals.css`) deve aplicar a proporção **`60-30-10`** em **`oklch(L C H / alpha)`** + `light-dark()` e **3 níveis de elevação** (`elevation-1..3` + `sunken/inset`), combinando **Umbra de Contato + Penumbra Difusa (`spread` negativo) + Borda Especular Zenital (`inset 0 1px 0 0`)**.
3. **`[LOCK-03]` Sincronia Obrigatória Projeto $\leftrightarrow$ Memória Global (`~/.gemini` & `.agents/` / `.context/`):**
   - Toda alteração em `skills/`, `agents/`, `rules/`, `AGENTS.md`, `SPEC.md`, `CONTEXT.md` ou `CURRENT_STATE.md` deve ser seguida da execução de `uv run python scripts/sync_gemini_ecosystem.py`, que sincroniza `.agents/AGENTS.md`, `.context/context.md`, `.context/spec.md` (em `franklin-quebragalho` e nos repositórios com Tríade espelhada como `adk-go-mcp`, `adk-py-agents`, `adk-ts-agent`, `GoSTylo`, `PCM`), `C:\Users\melki\.gemini\config\rules\`, `C:\Users\melki\.gemini\config\plugins\franklin-skills\`, `.well-known/agent-card.json` e `memories/audit_report.json`.

---

## 3. Histórico de Evolução (Changelog Consolidado)

### `[2026-11-09]` — Fase 31: Padronização da Tríade de Governança v2.0 (`AGENTS.md`, `CONTEXT.md`, `SPEC.md` + `.agents/` e `.context/`), Higienização de Pastas & Organização `adk-tests`

- **Padronização Canônica v2.0:** Alinhamento estrutural de [`AGENTS.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/AGENTS.md) / [`.agents/AGENTS.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/AGENTS.md) (Kernel Operacional v2.0 + 7 Regras de Ouro + 8 Personas + 10 Subagentes + Memória Evolutiva + Fechamento Self-Refine), [`CONTEXT.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CONTEXT.md) / [`.context/context.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/context.md) (Visão Geral, Decisões Críticas, Changelog e Backlog) e [`SPEC.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/SPEC.md) / [`.context/spec.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/spec.md) (Scope Lock, Contratos I/O e Critério de Aceite).
- **Higienização e Sincronia Multi-Repo (`franklin-quebragalho`, `adk-tests` e `~/.agents/skills`):** Removidos arquivos redundantes/poluentes (`shared/{AGENTS,CLAUDE,CONTEXT,SPEC}.md`, `.context/{CURRENT_STATE,SESSION_LOG}.md`, `Indice_Google_Drive.html`, `workspace_index.json`, `skills/arquiteto-conteudo-solucoes/README.md`, `adk-tests/bin/adk_sessions.db*`, `adk-tests/go_agent/benchmark.json` e `.rea.backup`), restauradas as skills externas de `~/.agents/skills` sem arquivos sintéticos e espelhada a Tríade de Governança v2.0 também em `adk-tests` via `scripts/sync_gemini_ecosystem.py`.

### `[2026-11-03]` — Fase 30: Fusão Canônica de Auditoria (`v6.0.0`), Governança `rules/` + `CURRENT_STATE.md` e Sincronia Global

- **Fusão 3-em-1 (`auditoria-projetos-sistema` `v6.0.0`):** Incorporou `antigravity-project-auditor` (diagnóstico causal de MVP e 5 pilares) e `nav-x-func` (Navegação em 3 Camadas, `X ativa Y`, `SGA` + `TIF` e template `V1 vs V2`), adicionando o novo scanner real `scripts/project_structure_and_code_auditor.py` e reduzindo o catálogo de `31` para **`29 Skills Canônicas`** sem sobreposição.
- **Governança e Prevenção de Drift:** Criada a pasta `rules/` na raiz do projeto sincronizada com `~/.gemini/config/rules/`, criado `CURRENT_STATE.md` com travas anti-regressão e reescritos `AGENTS.md`, `SPEC.md` e `CONTEXT.md` de forma enxuta e interligada.
- **Correção de Sombras em Camadas (`elevationRenderer.ts`):** Refatorado o pipeline Canvas 2D e `globals.css` do `universal-app` para 3 níveis de elevação + recesso `sunken` com 3 camadas ópticas (Penumbra Difusa + Umbra de Contato + Rim Light Zenital + Anel 1px) em `OKLCH`.
- **Alinhamento de `server.py`, `mcp_config.json`, `agent-card.json` e `memories/audit_report.json`:** Enxugados `@mcp.resource` e `@mcp.prompt` em `server.py`, unificado `mcp_config.json`, garantidas `tags` completas nos 29 cards A2A e automatizada a atualização de `memories/audit_report.json` no `sync_gemini_ecosystem.py`.

### `[2026-10-27 a 2026-11-02]` — Fases 28 e 29: SSOT em 9 Eixos, A2A v1.0 JWS e Módulos Especialistas (`re-a-ndroid`, `android-agy-projects`, `plan-uiux`, `audit-skills-antigravity`, `complex-zero`)

- Consolidação do Guia Mestre SSOT em 9 Eixos (`Preferências de Trabalho com Agentes.md`), Topologia `3+1` de Subagentes de UI (`ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer`), assinatura criptográfica JCS/JWS no `AgentCard` e auditores poliglotas (`agent-server-auditor`, `test-quality-auditor` v1.3, `code-acceptability-auditor` v1.1).
