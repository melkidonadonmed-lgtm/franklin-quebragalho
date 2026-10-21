# ESPECIFICAÇÃO TÉCNICA (`SPEC.md`) — `franklin-quebragalho`

## 1. Visão Geral do Sistema
O `franklin-quebragalho` provê o servidor MCP (`franklin-skills`), o barramento **Agent2Agent (`A2A v1.0`)** assinado via JWS, a malha de **7 Subagentes Declarativos** (Topologia `3+1` de UI + Memória Híbrida + Intermediários HITL/Read-After-Write) e o repositório mestre das **29 Agent Skills** em arquitetura de 3 camadas (*Progressive Disclosure*).

---

## 2. Módulos e Contratos Técnicos

| Módulo / Arquivo | Responsabilidade e Contrato |
| :--- | :--- |
| **`server.py`** | Servidor FastMCP (`stdio`) com **13 ferramentas**, 8 recursos (`skills://catalog`, `skills://a2a/agent-card`, `skills://mcp-2026/spec`, `skills://harness/checkpoints`, etc.) e 2 prompts (`activate_skill`, `tactile_frontend_audit`). |
| **`shared/catalog_service.py`** | Descoberta, indexação de metadados, busca ranqueada, leitura progressiva em 3 Tiers e validação determinística das 29 skills. |
| **`shared/compass_topology.py`** | Bússola semântica (`franklin_smart_compass`), Topologia Multi-Repo em 5 camadas e catálogo de personas/subagentes (`franklin_get_agents`). |
| **`shared/execution_orchestrator.py`** | Execução isolada de scripts (`.py`, `.js`, `.ps1`, `.cmd`), resolução/execução de planos DAG no `epic-volta` e orquestração HITL/A2A. |
| **`shared/harness.py` & `harness2_*.py`** | `SemanticGuard.sanitize_input`, `evaluate_action_risk` (`LOW`, `MEDIUM`, `CRITICAL`), `CheckpointStore` HITL (`.sessions/harness_checkpoints.json`) e motor recursivo Harness² (`harness2_engine.py` + `harness2_tree.py`). |
| **`shared/a2a_bridge.py`** | Valida `AgentCard` via Protobuf (`a2a.types.AgentCard`), assina com JCS (RFC 8785) + JWS (`HMAC-SHA256` via `FRANKLIN_A2A_SIGNING_SECRET`) e gerencia ciclo de vida de tarefas (`FranklinA2ATaskManager`). |
| **`shared/mcp_2026_advisor.py`** | Implementa `franklin_mcp_build_advisor` (Pattern A `<15` tools vs Pattern B *Search + Execute* `>=15` tools, `ui://` MCP Apps e manifesto `.mcpb` v0.4). |
| **`shared/tools/frontmatter_parser.py`** | Parser determinístico de frontmatter YAML com suporte a `metadata` aninhado e fallback resiliente sem dependências externas. |
| **`agents/*.md`** | Contratos declarativos dos **7 Subagentes**: Topologia `3+1` de UI (`ui-shell-navigator.md`, `ui-controls-data.md`, `ui-motion-interaction.md`, `ui-deterministic-observer.md`), Memória (`vault-memory-retriever.md`) e Intermediários Distribuídos (`intent-hitl-mediator.md`, `read-after-write-verifier.md`). |
| **`plans/*.json`** | Planos DAG executáveis no motor Kahn (`epic-volta`): `ui_composition_dag.json`, `physics_code_audit_dag.json` e `distributed_agent_mediation_dag.json`. |
| **`tests/test_*.py`** | 5 suítes de testes Nível 4 (`52/52 PASS`): `test_server.py`, `test_a2a_protocol.py`, `test_harness_quality.py`, `test_perfkit_stats.py` e `test_quality_auditor_go_mcp.py`. |

---

## 3. Catálogo das 13 Ferramentas MCP (`franklin-skills`)
1. `franklin_skills_list` — Lista as 29 skills (Tier 1: `name` + `description`).
2. `franklin_skills_get` — Carrega o contrato completo `SKILL.md` (Tier 2) e inventário de `scripts/` e `references/` (Tier 3).
3. `franklin_skills_search` — Busca textual e por tags no catálogo de skills.
4. `franklin_skills_validate` — Valida frontmatter YAML e limite `<500` linhas em todas as skills.
5. `franklin_get_agents` — Retorna os perfis de personas e subagentes (`MY_AGENTS.md` + `agents/*.md`).
6. `franklin_smart_compass` — Roteador heurístico que recomenda a skill ideal para uma intenção.
7. `franklin_run_skill_script` — Executa scripts auxiliares de uma skill com confinamento de segurança.
8. `franklin_execute_dag` — Dispara planos DAG (`plans/*.json`) integrados ao motor Kahn do `epic-volta`.
9. `franklin_harness_guard` — Avalia risco operacional e sanitiza entradas contra Prompt Injection.
10. `franklin_harness_checkpoint` — Cria, consulta, aprova ou rejeita checkpoints Human-in-the-Loop.
11. `franklin_a2a_agent_card` — Gera e verifica criptograficamente o `AgentCard` A2A v1.0 do Franklin.
12. `franklin_a2a_dispatch_task` — Despacha tarefas A2A v1.0 com proteção Zero-Trust e HITL.
13. `franklin_mcp_build_advisor` — Consultor arquitetural MCP Spec `2026-07-28`.
