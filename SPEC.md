# SPEC.MD — Contrato de Implementação: Franklin Quebra-Galho (`franklin-quebragalho` v2.0)

> Referenciado diretamente em [`AGENTS.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/AGENTS.md) e sincronizado com [`.context/spec.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/spec.md) e [`CURRENT_STATE.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CURRENT_STATE.md).

## 1. Objetivo e Fronteiras (Scope Lock)
- **O que construir:**
  1. **Servidor FastMCP (`server.py`) & Domínio Modular (`shared/`):** Servidor MCP oficial (`franklin-skills` sob protocolo `2026-07-28` em `stdio`) expondo **13 ferramentas**, **8 recursos passivos** e **2 prompts estruturados**.
  2. **Catálogo Mestre das 29 Agent Skills (`skills/`):** Arquitetura em 3 camadas de *Progressive Disclosure* (Tier 1 XML `<available_skills>`, Tier 2 `SKILL.md` `< 500` linhas, Tier 3 `scripts/`, `references/`, `rules/`, `evals/`) validada por `scripts/validate_skills.py` e `shared/trigger_eval_suite.py` ($F_1 = 1.0$).
  3. **Barramento Agent2Agent (`A2A v1.0` JWS) & Harness² Zero-Trust (`shared/a2a_bridge.py` + `shared/harness.py`):** Validação Protobuf (`a2a.types.AgentCard`), assinatura canônica RFC 8785 (JCS) + HMAC-SHA256 JWS (`.well-known/agent-card.json`), `SemanticGuard`, `CheckpointStore` HITL (`.sessions/harness_checkpoints.json`), idempotência MCP e motor recursivo Harness² (`shared/harness2_engine.py` + `shared/harness2_tree.py`).
  4. **Malha de 10 Subagentes Declarativos (`agents/*.md`), Planos DAG (`plans/*.json`) & Governança SSOT (`rules/*.md`):** Topologia `3+1` de UI (`agents/ui-shell-navigator.md`, `agents/ui-controls-data.md`, `agents/ui-motion-interaction.md`, `agents/ui-deterministic-observer.md`), governança/memória/operações (`agents/intent-hitl-mediator.md`, `agents/read-after-write-verifier.md`, `agents/review-squad.md`, `agents/vault-memory-retriever.md`, `agents/adk-go-operator.md`, `agents/dev-workspace-publisher.md`) e sincronia via `scripts/sync_gemini_ecosystem.py`.
- **Não-Objetivos (Proibido fazer):**
  - Proibido recriar as pastas legadas `antigravity-project-auditor` ou `nav-x-func` (consolidadas em `skills/auditoria-projetos-sistema/SKILL.md` `v6.0.0` sob `[LOCK-01]`).
  - Proibido emitir logs de depuração em `stdout` em servidores MCP `stdio` ou usar symlinks/junctions em vez de cópias físicas na sincronização de skills.
  - Proibido ultrapassar `600` linhas em módulos de orquestração (`server.py`, `shared/*.py`) ou afrouxar validações Zero-Trust/HITL em testes automatizados.

---

## 2. Contratos de Dados e Interfaces (I/O)

### 2.1 Módulos e Contratos Técnicos

| Módulo / Arquivo | Responsabilidade e Contrato |
| :--- | :--- |
| **`server.py`** | Servidor FastMCP (`stdio`) com **13 ferramentas**, **8 recursos** (`skills://catalog`, `skills://catalog/xml`, `skills://manifest`, `skills://agents`, `skills://agent/{agent_name}`, `skills://skill/{skill_name}`, `skills://a2a/agent-card`, `skills://mcp-2026/spec`, `skills://harness/checkpoints`) e **2 prompts** (`activate_skill`, `tactile_frontend_audit`). |
| **`shared/catalog_service.py`** | Descoberta, indexação de metadados, busca ranqueada, leitura progressiva em 3 Tiers, aliases retrocompatíveis (`nav-x-func` / `antigravity-project-auditor` $\to$ `auditoria-projetos-sistema`) e validação determinística das **29 Agent Skills**. |
| **`shared/compass_topology.py`** | Bússola semântica Zero-LLM (`franklin_smart_compass`), Topologia Multi-Repo em 5 camadas e catálogo de 8 personas e 10 subagentes (`franklin_get_agents`). |
| **`shared/execution_orchestrator.py`** | Execução isolada de scripts (`.py`, `.js`, `.ps1`, `.cmd`), resolução/execução de planos DAG no `epic-volta` e orquestração HITL/A2A. |
| **`shared/modular_orchestrator.py`** | Orquestrador em 6 papéis (`Intent`, `Planner`, `Worker`, `HITL Gate`, `Critic Loop`, `Reporter`) e `ProgressiveSkillRegistry`. |
| **`shared/harness.py` & `shared/harness2_engine.py` & `shared/harness2_tree.py`** | `SemanticGuard.sanitize_input`, `evaluate_action_risk` (`LOW`, `MEDIUM`, `CRITICAL`), `CheckpointStore` HITL, `execute_with_idempotency`, `IntentBoundTokenValidator` e motor recursivo Harness². |
| **`shared/a2a_bridge.py`** | Valida `AgentCard` via Protobuf (`a2a.types.AgentCard`) garantindo `id` kebab-case e `tags` obrigatórias nas **29 Agent Skills**, assina com JCS (RFC 8785) + JWS (`HMAC-SHA256` via `FRANKLIN_A2A_SIGNING_SECRET`) e gerencia tarefas (`FranklinA2ATaskManager`). |
| **`shared/mcp_2026_advisor.py`** | Implementa `franklin_mcp_build_advisor` (Pattern A `<15` tools vs Pattern B *Search + Execute* `>=15` tools, `ui://` MCP Apps e manifesto `.mcpb` v0.4). |
| **`shared/agent_spec_loader.py` & `shared/tools/frontmatter_parser.py`** | Parsers determinísticos de contratos de subagentes (`agents/*.md`) e frontmatter YAML com fallback resiliente sem dependências externas. |
| **`rules/diretrizes-qualidade-eficiencia.md` & `rules/diretrizes-frontend-9-eixos.md`** | Diretrizes versionadas do projeto sincronizadas automaticamente com `~/.gemini/config/rules/` via `scripts/sync_gemini_ecosystem.py`. |
| **`plans/ui_composition_dag.json` & `plans/physics_code_audit_dag.json` & `plans/distributed_agent_mediation_dag.json`** | Planos DAG executáveis no motor Kahn (`epic-volta`). |
| **`tests/test_server.py` & `tests/test_a2a_protocol.py` & `tests/test_harness_quality.py` & `tests/test_skill_trigger_precision.py`** | Suítes de testes Nível 4 (`83/83 PASS` no total da pasta `tests/`). |

### 2.2 Catálogo das 13 Ferramentas MCP (`franklin-skills` • Protocolo `2026-07-28`)
1. `franklin_skills_list` (`readOnlyHint=True`) — Lista as **29 Agent Skills** em Markdown, JSON ou XML Nível 1 (`<available_skills>`).
2. `franklin_skills_get` (`readOnlyHint=True`) — Carrega o contrato `SKILL.md` (Tier 2: `contract` / `activate`) e recursos sob demanda (`resource:<path>`, `rules`, `references`, `evals`, `scripts`, `all` em Tier 3) com proteção anti-Path Traversal.
3. `franklin_skills_search` (`readOnlyHint=True`) — Busca ranqueada por intenção, domínio ou tags com penalização de cláusulas negativas (`não use para`).
4. `franklin_skills_validate` (`readOnlyHint=True`) — Audita frontmatter YAML, kebab-case, seções obrigatórias e orçamento `<500` linhas nas **29 Agent Skills**.
5. `franklin_get_agents` (`readOnlyHint=True`) — Retorna os perfis das 8 personas (`MY_AGENTS.md`), Topologia Multi-Repo (`ecosystem`) e 10 subagentes declarativos (`agents/*.md`).
6. `franklin_smart_compass` (`readOnlyHint=True`) — Bússola determinística Zero-LLM que recomenda a skill, persona, script e plano DAG exatos para uma intenção.
7. `franklin_run_skill_script` (`readOnlyHint=False`, `idempotency_key`) — Executa scripts auxiliares de uma skill com confinamento de diretório, suporte a `target_dir` cross-project e guarda Zero-Trust.
8. `franklin_execute_dag` (`readOnlyHint=False`, `idempotency_key`) — Valida ou dispara planos DAG (`ui`, `physics`, `mediation`) integrados ao motor Kahn com persistência SQLite WAL.
9. `franklin_harness_guard` (`readOnlyHint=False`) — Avalia risco operacional (`LOW`/`MEDIUM`/`CRITICAL`) e sanitiza entradas contra Prompt Injection e XSS.
10. `franklin_harness_checkpoint` (`readOnlyHint=False`, `idempotency_key`) — Cria, consulta, aprova ou rejeita checkpoints Human-in-the-Loop e despacha ações Harness² (`validate_tree`, `evolve`, `record_experience`).
11. `franklin_a2a_agent_card` (`readOnlyHint=True`) — Gera e verifica criptograficamente o `AgentCard` A2A v1.0 do Franklin (`.well-known/agent-card.json`).
12. `franklin_a2a_dispatch_task` (`readOnlyHint=False`, `idempotency_key`) — Despacha, consulta, retoma ou cancela tarefas A2A v1.0 com proteção Zero-Trust e HITL.
13. `franklin_mcp_build_advisor` (`readOnlyHint=True`) — Consultor arquitetural MCP Spec `2026-07-28` (`build-with-agent-skills`).

---

## 3. Critério de Aceite e Parada (Definition of Done)
- [x] Passar em 100% da suíte determinística Pytest (`uv run pytest -q` — `83/83` testes aprovados).
- [x] Validar 100% das **29 Agent Skills** canônicas (`uv run python scripts/validate_skills.py` — `29/29 PASS`, precisão de disparo Top-1 $F_1 = 1.0$).
- [x] Passar nos auditores determinísticos AST e estruturais (`uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --file server.py` com `Score >= 75/100` e `uv run python skills/auditoria-projetos-sistema/scripts/project_structure_and_code_auditor.py --self-test` com `[PASS]`).
- [x] Sincronizar ecossistema global e local sem divergência (`uv run python scripts/sync_gemini_ecosystem.py` retornando `"status": "SYNCHRONIZED"` e `memories/audit_report.json` com `100.0/100 APPROVED`).
