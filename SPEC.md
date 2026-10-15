# ESPECIFICAÇÃO TÉCNICA (`SPEC.md`) — `franklin-quebragalho`

## 1. Visão Geral do Sistema
O `franklin-quebragalho` provê o servidor MCP (`franklin-skills`), o barramento **Agent2Agent (`A2A v1.0`)** assinado via JWS e o repositório mestre das **25 Agent Skills** em arquitetura de 3 camadas (*Progressive Disclosure*).

---

## 2. Módulos e Contratos Técnicos

| Módulo / Arquivo | Responsabilidade e Contrato |
| :--- | :--- |
| **`server.py`** | Servidor FastMCP (`stdio`) com **13 ferramentas** e recursos `skills://catalog/summary`, `skills://a2a/agent-card` e `skills://mcp-2026/spec`. Neutraliza conflito de import hook do `beartype` no Python 3.15. |
| **`shared/harness.py`** | `SemanticGuard.sanitize_input` (bloqueia Prompt Injection / Path Traversal), `evaluate_action_risk` (`READ_ONLY`, `REVERSIBLE_WRITE`, `CRITICAL_MUTATION`) e `CheckpointStore` HITL (`.sessions/harness_checkpoints.json`). |
| **`shared/a2a_bridge.py`** | Valida `AgentCard` via Protobuf (`a2a.types.AgentCard`), assina com JCS (RFC 8785) + JWS (`HMAC-SHA256`) e gerencia ciclo de vida de tarefas (`FranklinA2ATaskManager`: `COMPLETED`, `INPUT_REQUIRED`, `REJECTED`, `CANCELED`). |
| **`shared/mcp_2026_advisor.py`** | Implementa `franklin_mcp_build_advisor` (Pattern A `<15` tools vs Pattern B *Search + Execute* `>=15` tools, `ui://` MCP Apps e manifesto `.mcpb` v0.4). |
| **`agents/*.md`** | Contratos declarativos da **Topologia `3+1` de UI**: `ui-shell-navigator.md` (Onda 1), `ui-controls-data.md` (Onda 2A), `ui-motion-interaction.md` (Onda 2B) e `ui-deterministic-observer.md` (Onda 3 Gatekeeper). |
| **`skills/test-quality-auditor/`** | Auditor determinístico AST/Regex v1.2.0 com 5 módulos (`python`, `ts_js`, `go`, `mcp`, `harness`) e evals espelhados 1:1 (`20/20 PASS`). |

---

## 3. Catálogo das 13 Ferramentas MCP (`franklin-skills`)
1. `franklin_skills_list` — Lista as 25 skills (Tier 1: `name` + `description`).
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
