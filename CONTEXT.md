# CONTEXTO OPERACIONAL — `franklin-quebragalho` (Catálogo de 26 Skills + FastMCP + Ponte A2A v1.0 JWS)

Este documento resume a arquitetura, as 26 skills canônicas, os subagentes e o estado operacional do repositório **`franklin-quebragalho`**.

---

## 1. Papel e Arquitetura
O `franklin-quebragalho` é a incubadora central de habilidades agênticas (**Agent Skills** em 3 Tiers), servidor **FastMCP (`server.py`)** e ponte oficial **Agent2Agent (`A2A v1.0` + assinatura criptográfica JWS em `shared/a2a_bridge.py`)**.
- **Catálogo de 26 Skills Canônicas (`skills/`)**: Sincronizado com o plugin global `C:\Users\melki\.gemini\config\plugins\franklin-skills\`.
- **Servidor MCP (`server.py` — 13 Ferramentas)**: Expõe listagem, busca, validação de skills, bússola semântica (`franklin_smart_compass`), executor de scripts (`franklin_run_skill_script`), disparador DAG (`franklin_execute_dag`), guardas Zero-Trust (`franklin_harness_guard` / `franklin_harness_checkpoint`), consultor MCP `2026-07-28` (`franklin_mcp_build_advisor`) e ponte A2A (`franklin_a2a_agent_card` / `franklin_a2a_dispatch_task`).
- **Esquadrão de UI `Topologia 3+1` (`agents/*.md` & `plans/ui_composition_dag.json`)**: 4 subagentes especialistas (`ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer`) orquestrados em 3 ondas paralelas (Kahn) sob o paradigma de **Preferências de Estilo e Temas por Objetivo (`preferencias_estilo_e_temas.md`)**.

---

## 2. Estado Operacional (Outubro/2026)
1. **Autonomia Standalone (`shared/`)**: Contém `shared/harness.py` (`SemanticGuard`, `evaluate_action_risk`, `CheckpointStore` HITL), `shared/a2a_bridge.py` (`FranklinA2ATaskManager` + JCS/JWS HMAC-SHA256) e `shared/mcp_2026_advisor.py`.
2. **Qualidade de Testes Nível 4 (`100.0/100`)**:
   - **44/44 testes aprovados** em `pytest tests/ -q`.
   - **26/26 skills validadas** em `python scripts/validate_skills.py`.
   - **20/20 casos de avaliação (`evals/evals.json`)** aprovados no `test-quality-auditor` v1.2.0 com espelhamento 1:1 dos 5 módulos analisadores (`python`, `ts_js`, `go`, `mcp`, `harness`).
