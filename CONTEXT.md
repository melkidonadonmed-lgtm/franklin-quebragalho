# CONTEXTO OPERACIONAL — `franklin-quebragalho` (Catálogo de 28 Skills + 7 Subagentes + FastMCP + Ponte A2A v1.0 JWS)

Este documento resume a arquitetura, as 28 skills canônicas, os 7 subagentes (incluindo intermediários de intenção/HITL e Read-After-Write) e o estado operacional do repositório **`franklin-quebragalho`**.

---

## 1. Papel e Arquitetura
O `franklin-quebragalho` é a incubadora central de habilidades agênticas (**Agent Skills** em 3 Tiers), servidor **FastMCP (`server.py`)** e ponte oficial **Agent2Agent (`A2A v1.0` + assinatura criptográfica JWS em `shared/a2a_bridge.py`)**.
- **Catálogo de 28 Skills Canônicas (`skills/`)**: Sincronizado com o plugin global `C:\Users\melki\.gemini\config\plugins\franklin-skills\`.
- **Servidor MCP (`server.py` — 13 Ferramentas)**: Expõe listagem, busca, validação de skills, bússola semântica (`franklin_smart_compass`), executor de scripts (`franklin_run_skill_script`), disparador DAG (`franklin_execute_dag`), guardas Zero-Trust (`franklin_harness_guard` / `franklin_harness_checkpoint`), consultor MCP `2026-07-28` (`franklin_mcp_build_advisor`) e ponte A2A (`franklin_a2a_agent_card` / `franklin_a2a_dispatch_task`).
- **Esquadrão de 7 Subagentes (`agents/*.md` & `plans/*.json`)**:
  - **UI `Topologia 3+1`**: `ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer`.
  - **Memória Híbrida (`~35ms`)**: `vault-memory-retriever`.
  - **Intermediários Distribuídos (`plans/distributed_agent_mediation_dag.json`)**: `intent-hitl-mediator` (Triagem Pydantic + HITL + Resource Attribution DAK) e `read-after-write-verifier` (Validação pós-escrita e Fan-In).

---

## 2. Estado Operacional (Outubro/2026)
1. **Autonomia Modular (`shared/`)**: Contém `shared/catalog_service.py`, `shared/compass_topology.py`, `shared/execution_orchestrator.py`, `shared/harness.py`, `shared/harness2_engine.py`, `shared/harness2_tree.py`, `shared/a2a_bridge.py`, `shared/mcp_2026_advisor.py` e `shared/tools/frontmatter_parser.py`.
2. **Qualidade de Testes Nível 4 (`100.0/100`)**:
   - **52/52 testes aprovados** em `uv run pytest -q` (distribuídos em 5 suítes em `tests/`).
   - **28/28 skills validadas** em `python scripts/validate_skills.py`.
   - **20/20 casos de avaliação (`evals/evals.json`)** aprovados no `test-quality-auditor` v1.2.0 com espelhamento 1:1 dos 5 módulos analisadores (`python`, `ts_js`, `go`, `mcp`, `harness`).
