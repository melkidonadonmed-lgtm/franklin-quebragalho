# Estado Atual do Workspace: Franklin Quebra-Galho

> **Última Atualização**: 2026-10-15  
> **Nível de Persistência**: Nível 2 (Resumo de Contexto)  
> **Status Geral**: 🟢 100% Operacional e Conforme com a Governança 2026 (25/25 PASS + Servidor MCP Global Autônomo com `shared/` + Motor DAG Integrado + `test-quality-auditor` `v1.0.0`)  

---

## 1. Visão Geral e Fase do Projeto
- **Repositório**: `c:\Users\melki\dev\repos\franklin-quebragalho\`
- **Objetivo**: Incubadora central de automações de produtividade, runbooks e skills personalizadas do agente Franklin Quebra-Galho para o Google Antigravity.
- **Servidor MCP Global Ativo**: Servidor FastMCP dedicado (`server.py`) com pacote interno `shared/` (`frontmatter_parser` e `harness` Zero-Trust), expondo 9 ferramentas (`franklin_skills_list`, `franklin_skills_get`, `franklin_skills_search`, `franklin_skills_validate`, `franklin_get_agents`, `franklin_run_skill_script`, `franklin_execute_dag`, `franklin_harness_guard` e `franklin_harness_checkpoint`), 5 recursos e 2 prompts MCP.
- **Integração Global de Skills**: O diretório `.agents/skills/` é sincronizado fisicamente 1:1 com `skills/`, com o plugin global `C:\Users\melki\.gemini\config\plugins\franklin-skills\skills` e com o catálogo em `G:\Meu Drive\Franklin_Skills_Docs_2026`.
- **Fase**: Fases 1 a 9 concluídas (25 skills canônicas incluindo `code-quality-audit-3d-physics` e `test-quality-auditor`, com 100% das suítes de testes em Nível 4 Determinístico & Resiliente).

---

## 2. Catálogo Consolidado de Skills (25 Ativas - 100% PASS)

| Skill | Versão | Status | Paridade (`.agents` ➔ `skills/`) | Subagente Operador |
| :--- | :---: | :---: | :---: | :--- |
| `evoluir-skills` | `v2.0.0` | 🚀 Produção | ✅ Sincronizado | `SkillCraft` |
| `aprimoramento-expansibilidade-agentes-skills` | `v2.0.0` | 🚀 Produção | ✅ Sincronizado | `SkillCraft` |
| `skill-auditor-refatorador-skills` | `v1.3.0` | 🚀 Produção | ✅ Sincronizado | `SkillCraft` |
| `test-quality-auditor` | `v1.0.0` | 🚀 Produção | ✅ Sincronizado | `SkillCraft` / `Franklin-Main` |
| `code-quality-audit-3d-physics` | `v1.0.0` | 🚀 Produção | ✅ Sincronizado | `Franklin-Main` |
| `auditoria-projetos-sistema` | `v2.2.0` | 🚀 Produção | ✅ Sincronizado | `Franklin-Main` |
| `redator-tecnico-markdown` | `v1.2.0` | ✅ Validada | ✅ Sincronizado | `DocMaker` / `VaultMaster` |
| `conversor-html-pdf` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `DocMaker` |
| `gdrive-auditoria-limpeza` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `DriveMaster` |
| `gdrive-taxonomia-organizacao` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `DriveMaster` |
| `manutencao-disco-windows` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `FileOpsLocal` |
| `curadoria-obsidian-vault` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `VaultMaster` |
| `analise-design-tatil-frontend` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `FrontCraftMaster` |
| `refatoracao-design-tatil-frontend` | `v1.2.0` | ✅ Validada | ✅ Sincronizado | `FrontCraftMaster` |
| `consultor-design-tatil-frontend` | `v1.2.0` | ✅ Validada | ✅ Sincronizado | `FrontCraftMaster` |
| `arquitetura-design-implementacao-sistema` | `v1.2.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `design-interface-medica-minimalista` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `FrontCraftMaster` |
| `high-level-context-planner` | `v2.0.0` | ✅ Validada | ✅ Sincronizado | `LoopPlanner` |
| `skill-orquestrador-planos-encadeados` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `LoopPlanner` |
| `gap-analyzer-auditor` | `v2.0.0` | ✅ Validada | ✅ Sincronizado | `LoopPlanner` |
| `organizador-fluxo-arvore-arquivos` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `DocMaker` |
| `arquiteto-conteudo-solucoes` | `v2.2.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `context-sentinel` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `refine-prompt` | `v3.0.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `_template` | `v1.3.0` | 🚀 Produção | ✅ Sincronizado | Base Padrão 2026 |

---

## 3. Decisões Arquiteturais Vigentes
- **KISS & Local-First**: Operações diretas no SO, scripts nativos em PowerShell (`pwsh`) e browser headless nativo (`msedge.exe`).
- **Autonomia Standalone (`shared/`)**: O pacote `shared/` reside dentro do repositório (`shared/harness.py` e `shared/tools/frontmatter_parser.py`), eliminando dependências externas quebradas após a migração para `dev/repos/franklin-quebragalho`.
- **Caminhos Reais da Máquina**: Cofre Obsidian em `C:\Users\melki\dev\notes\`, projetos em `C:\Users\melki\dev\repos\`, utilitários em `C:\Users\melki\dev\tools\` e experimentos em `C:\Users\melki\dev\sandbox\`.
- **Cópias Físicas para Skills**: Proibido o uso de junctions/symlinks (`d----l`) em pastas de skills do Antigravity; a sincronização é feita via cópia física por `scripts/standardize_skills_metadata.py`.
