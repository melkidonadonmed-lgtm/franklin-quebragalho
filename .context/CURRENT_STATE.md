# Estado Atual do Workspace: Franklin Quebra-Galho

> **Última Atualização**: 2026-10-22  
> **Nível de Persistência**: Nível 2 (Resumo de Contexto)  
> **Status Geral**: 🟢 100% Operacional e Conforme com a Governança 2026 (24/24 PASS + 7 Subagentes Declarativos + Servidor MCP Global Autônomo com `shared/` + Motor DAG Integrado)  

---

## 1. Visão Geral e Fase do Projeto
- **Repositório**: `c:\Users\melki\dev\repos\franklin-quebragalho\`
- **Objetivo**: Incubadora central de automações de produtividade, runbooks e skills personalizadas do agente Franklin Quebra-Galho para o Google Antigravity.
- **Servidor MCP Global Ativo**: Servidor FastMCP dedicado (`server.py`) com pacote interno `shared/`, expondo 13 ferramentas (`franklin_skills_list`, `franklin_skills_get`, `franklin_skills_search`, `franklin_skills_validate`, `franklin_get_agents`, `franklin_smart_compass`, `franklin_run_skill_script`, `franklin_execute_dag`, `franklin_harness_guard`, `franklin_harness_checkpoint`, `franklin_a2a_agent_card`, `franklin_a2a_dispatch_task` e `franklin_mcp_build_advisor`), 5 recursos e 2 prompts MCP.
- **Integração Global de Skills**: O diretório `skills/` é sincronizado fisicamente 1:1 com o plugin global `C:\Users\melki\.gemini\config\plugins\franklin-skills\skills` e com o catálogo em `G:\Meu Drive\Franklin_Skills_Docs_2026`.
- **Fase**: Fase 25 concluída (Consolidação para 24 skills canônicas e 7 subagentes declarativos, unificando a trinca de Frontend em `design-md`, `frontend-code-architect` e `frontend-testing-auditor`, e removendo skills redundantes/meta).

---

## 2. Catálogo Consolidado de Skills (24 Ativas - 100% PASS)

| Skill | Versão | Status | Paridade (`skills/` ➔ Plugin Global) | Subagente Operador |
| :--- | :---: | :---: | :---: | :--- |
| `antigravity-project-auditor` | `v2.0.0` | 🚀 Produção | ✅ Sincronizado | `Franklin-Main` / `LoopPlanner` |
| `arquiteto-conteudo-solucoes` | `v2.2.0` | 🚀 Produção | ✅ Sincronizado | `Franklin-Main` |
| `nav-x-func` | `v4.0.0` | 🚀 Produção | ✅ Sincronizado | `Franklin-Main` / `UI-Architect` |
| `auditoria-projetos-sistema` | `v2.2.0` | 🚀 Produção | ✅ Sincronizado | `Franklin-Main` |
| `code-acceptability-auditor` | `v1.0.0` | 🚀 Produção | ✅ Sincronizado | `SkillCraft` |
| `code-quality-audit-3d-physics` | `v1.0.0` | 🚀 Produção | ✅ Sincronizado | `Franklin-Main` |
| `context-sentinel` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `conversor-html-pdf` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `DocMaker` |
| `curadoria-obsidian-vault` | `v1.2.0` | ✅ Validada | ✅ Sincronizado | `VaultMaster` / `vault-memory-retriever` |
| `design-interface-medica-minimalista` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `UI-Architect` |
| `design-md` | `v2.0.0` | 🚀 Produção | ✅ Sincronizado | `UI-Architect` / `ui-shell-navigator` |
| `frontend-code-architect` | `v2.0.0` | 🚀 Produção | ✅ Sincronizado | `UI-Architect` / `ui-controls-data` / `ui-motion-interaction` |
| `frontend-testing-auditor` | `v2.0.0` | 🚀 Produção | ✅ Sincronizado | `UI-Architect` / `ui-deterministic-observer` |
| `gap-analyzer-auditor` | `v2.0.0` | ✅ Validada | ✅ Sincronizado | `LoopPlanner` |
| `gdrive-auditoria-limpeza` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `DriveMaster` |
| `gdrive-taxonomia-organizacao` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `DriveMaster` |
| `high-level-context-planner` | `v2.0.0` | ✅ Validada | ✅ Sincronizado | `LoopPlanner` |
| `manutencao-disco-windows` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `FileOpsLocal` |
| `organizador-fluxo-arvore-arquivos` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `DocMaker` |
| `organizador-projetos-ideias` | `v1.0.0` | 🚀 Produção | ✅ Sincronizado | `Franklin-Main` / `DocMaker` |
| `redator-tecnico-markdown` | `v1.2.0` | ✅ Validada | ✅ Sincronizado | `DocMaker` / `VaultMaster` |
| `refine-prompt` | `v3.2.0` | 🚀 Produção | ✅ Sincronizado | `Franklin-Main` |
| `skill-orquestrador-planos-encadeados` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `LoopPlanner` |
| `test-quality-auditor` | `v1.2.0` | 🚀 Produção | ✅ Sincronizado | `SkillCraft` / `Franklin-Main` |

---

## 3. Decisões Arquiteturais Vigentes
- **KISS & Local-First**: Operações diretas no SO, scripts nativos em PowerShell (`pwsh`) e browser headless nativo (`msedge.exe`).
- **Autonomia Standalone (`shared/`)**: O pacote `shared/` reside dentro do repositório (`shared/harness.py`, `shared/catalog_service.py`, `shared/compass_topology.py`, `shared/execution_orchestrator.py`, `shared/a2a_bridge.py` e `shared/tools/frontmatter_parser.py`).
- **Caminhos Reais da Máquina**: Cofre Obsidian em `C:\Users\melki\dev\notes\`, projetos em `C:\Users\melki\dev\repos\`, utilitários em `C:\Users\melki\dev\tools\` e experimentos em `C:\Users\melki\dev\sandbox\`.
- **Cópias Físicas para Skills**: Proibido o uso de junctions/symlinks (`d----l`) em pastas de skills do Antigravity; a sincronização é feita via cópia física por `scripts/sync_gemini_ecosystem.py`.
