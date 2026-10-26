# Franklin Quebra-Galho

> **Agente Principal & Catálogo de Automação Diária e Engenharia de Software**

O **Franklin Quebra-Galho** (`franklin-quebragalho`) é o assistente principal de produtividade e engenharia do desenvolvedor (Melki), reunindo **26 Skills Canônicas**, **8 Subagentes Declarativos** e o servidor **Franklin Skills MCP** (`server.py`).

---

## Catálogo Rápido de Skills (26 Skills Canônicas)

| Skill | Versão | Status | Propósito Principal | Link |
| :--- | :---: | :---: | :--- | :--- |
| **`agent-server-auditor`** | `v1.0.0` | 🚀 Produção | Auditor arquitetural poliglota (Go, TS, Py) para agentes, servidores MCP (`2026-07-28`), nós A2A (`v1.0` JWS), binários, travas `max_steps` e `memories/audit_report.json`. | [skills/agent-server-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/agent-server-auditor/SKILL.md) |
| **`organizador-projetos-ideias`** | `v1.0.0` | 🚀 Produção | Organizador de ideias do zero (`ideation_to_v1`) e sincronizador completo de projetos (`project_organizer_sync`). | [skills/organizador-projetos-ideias/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-projetos-ideias/SKILL.md) |
| **`antigravity-project-auditor`** | `v2.0.0` | 🚀 Produção | Auditor arquitetural, diagnóstico de MVP e planejamento em 3 fases (`autonomous_scan` \| `targeted_focus`). | [skills/antigravity-project-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/antigravity-project-auditor/SKILL.md) |
| **`code-acceptability-auditor`** | `v1.1.0` | 🚀 Produção | Portão 1 AST/Pydantic de código Python (`12` regras), Quality Gate (`>=75/100`) e Trigger Matrix ($F_1=1.0$). | [skills/code-acceptability-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-acceptability-auditor/SKILL.md) |
| **`design-md`** | `v5.0.0` | 🚀 Produção | Cria ou atualiza o contrato `DESIGN.md` na raiz do projeto com tokens semânticos, escala tipográfica e composição espacial sem travar cores. | [skills/design-md/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/design-md/SKILL.md) |
| **`frontend-code-architect`** | `v3.0.0` | 🚀 Produção | Implementa e refatora interfaces web (standalone HTML/CSS/JS ou React/TS) consumindo o `DESIGN.md` sem engessar estilos. | [skills/frontend-code-architect/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-code-architect/SKILL.md) |
| **`frontend-testing-auditor`** | `v4.0.0` | 🚀 Produção | Auditor determinístico de qualidade Frontend (`audit_tactile_ui.py` `v4.0`): composição, WCAG 2.1 AA/AAA, zero emojis, zero bloat Base64 e FSM. | [skills/frontend-testing-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-testing-auditor/SKILL.md) |
| **`frontend-ui-ux-auditor`** | `v1.0.0` | 🚀 Produção | Auditor matemático de UI/UX (`ui_ux_frontend_auditor.py`): escala 8px, contraste WCAG 2.1 AA, densidade DOM, ícones 1:1, luz 135° e zero reflow. | [skills/frontend-ui-ux-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-ui-ux-auditor/SKILL.md) |
| **`test-quality-auditor`** | `v1.2.0` | 🚀 Produção | Portão 2 modular em 5 domínios (Python, TS/JS, Go, MCP e Harness) + estatística `perfkit_stats.py`. | [skills/test-quality-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/test-quality-auditor/SKILL.md) |
| **`code-quality-audit-3d-physics`** | `v1.0.0` | 🚀 Produção | Auditoria de código e Física 3D em 3 ondas (5 subskills, Pass@10 e observador $S_{\text{norm}}$). | [skills/code-quality-audit-3d-physics/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/SKILL.md) |
| **`auditoria-projetos-sistema`** | `v3.0.0` | 🚀 Produção | Auditoria estrutural (`AGENTS.md`, tipagem Pydantic), alinhamento de composição visual ao propósito do projeto e `agent-browser`. | [skills/auditoria-projetos-sistema/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/auditoria-projetos-sistema/SKILL.md) |
| **`arquiteto-conteudo-solucoes`** | `v2.4.0` | 🚀 Produção | Geração técnica sob 4 modos (A, B, C, D), prompts enterprise, código tipado e roadmaps. | [skills/arquiteto-conteudo-solucoes/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/arquiteto-conteudo-solucoes/SKILL.md) |
| **`organizador-fluxo-arvore-arquivos`** | `v1.2.0` | 🚀 Produção | Converte ideias brutas em diagramas Mermaid, árvores ASCII e planos com exportação MD/PDF. | [skills/organizador-fluxo-arvore-arquivos/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-fluxo-arvore-arquivos/SKILL.md) |
| **`nav-x-func`** | `v4.0.0` | 🚀 Produção | Planejamento de MVP (`CLAREZA/CREATE`), Ilhas Funcionais, navegação real (`X ativa Y`, *Dead Ends*), suficiência funcional (TIF) e motor determinístico `SGA` (`V1 vs V2`). | [skills/nav-x-func/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/nav-x-func/SKILL.md) |
| **`design-interface-medica-minimalista`** | `v4.0.0` | 🚀 Produção | Arquitetura especializada para interfaces clínicas, PEP, calculadoras médicas e impressão A4 vetorial (`.sus-grid`). | [skills/design-interface-medica-minimalista/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/design-interface-medica-minimalista/SKILL.md) |
| **`context-sentinel`** | `v1.1.0` | 🚀 Produção | Auditoria de contexto em conversas multi-turn, mitigação de context rot e snapshots determinísticos. | [skills/context-sentinel/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/context-sentinel/SKILL.md) |
| **`skill-orquestrador-planos-encadeados`** | `v2.0.0` | 🚀 Produção | Orquestração executiva de planos multifásicos com isolamento de estado compartilhado. | [skills/skill-orquestrador-planos-encadeados/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/skill-orquestrador-planos-encadeados/SKILL.md) |
| **`high-level-context-planner`** | `v2.1.0` | 🚀 Produção | Planejador estratégico em malha fechada, Fase 0 obrigatória, tasks paralelizáveis e convergência *append-only*. | [skills/high-level-context-planner/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/high-level-context-planner/SKILL.md) |
| **`gap-analyzer-auditor`** | `v2.1.0` | 🚀 Produção | Portão 3 de RCA em 4 vetores, segregação `[FATO]`/`[INFERÊNCIA]`/`[LACUNA]` e hand-off YAML. | [skills/gap-analyzer-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gap-analyzer-auditor/SKILL.md) |
| **`refine-prompt`** | `v3.2.0` | 🚀 Produção | Auditoria de factibilidade, modulação de entropia e refinamento de prompts sob Zero-Trust. | [skills/refine-prompt/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/refine-prompt/SKILL.md) |
| **`gdrive-auditoria-limpeza`** | `v1.0.0` | 🚀 Produção | Varredura de arquivos pesados (>100MB), duplicados SHA-256 e quarentena segura no Google Drive. | [skills/gdrive-auditoria-limpeza/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-auditoria-limpeza/SKILL.md) |
| **`gdrive-taxonomia-organizacao`** | `v1.1.0` | 🚀 Produção | Estrutura canônica numerada real do Drive, datas ISO (`YYYY-MM-DD`) e triagem documental. | [skills/gdrive-taxonomia-organizacao/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-taxonomia-organizacao/SKILL.md) |
| **`manutencao-disco-windows`** | `v1.1.0` | 🚀 Produção | Triagem de Downloads, Desktop e organização de `C:\Users\melki\dev\` com dry-run. | [skills/manutencao-disco-windows/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/manutencao-disco-windows/SKILL.md) |
| **`curadoria-obsidian-vault`** | `v1.1.0` | 🚀 Produção | Curadoria do cofre Obsidian (`C:\Users\melki\dev\notes\`), YAML, `[[Wikilinks]]` e anexos órfãos. | [skills/curadoria-obsidian-vault/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/curadoria-obsidian-vault/SKILL.md) |
| **`redator-tecnico-markdown`** | `v1.2.0` | 🚀 Produção | Redação técnica de relatórios, notas técnicas e atas em Markdown compatíveis com Obsidian. | [skills/redator-tecnico-markdown/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/redator-tecnico-markdown/SKILL.md) |
| **`conversor-html-pdf`** | `v1.0.0` | 🚀 Produção | Conversão determinística de Markdown/HTML para PDF profissional via Edge headless. | [skills/conversor-html-pdf/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/conversor-html-pdf/SKILL.md) |

---

## Comandos Rápidos

- **Executar Servidor MCP Localmente**: `uv run python server.py`
- **Executar Suíte Completa de Testes (`52/52`)**: `uv run pytest -q`
- **Auditar Todas as Skills (`26/26`)**: `uv run python scripts/validate_skills.py`
- **Sincronizar Catálogo e Plugin Global**: `uv run python scripts/sync_gemini_ecosystem.py`
- **Consultar SSOT de Preferências de Design e Estilo**: [Preferências de Trabalho com Agentes.md](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md)
