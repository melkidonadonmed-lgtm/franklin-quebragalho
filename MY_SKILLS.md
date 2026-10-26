# Minhas Skills (MY SKILLS)

> **Manifesto, Catálogo de Ciclo de Vida e Histórico de Versões de Skills**

Este repositório é o catálogo canônico de skills do **Franklin Quebra-Galho**. Para preferências globais de design, composição e engenharia, consulte a Fonte Única de Verdade (SSOT) em [`Preferências de Trabalho com Agentes.md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md).

---

## Tabela de Ciclo de Vida das Skills

| Status | Descrição |
| :--- | :--- |
| **Ideia** | Rascunho de conceito ou necessidade levantada no dia a dia. |
| **Em Teste** | Implementada em `skills/<nome>/`, passando por cenários de teste reais. |
| **Validada** | Fluxo testado com sucesso, documentação completa e tratamento de erros ok. |
| **Produção** | Skill consolidada, estável e ativada rotineiramente pelo orquestrador. |

---

### Catálogo de Skills do Workspace (26 Skills Canônicas)

| Skill | Versão | Status | Descrição Curta | Localização |
| :--- | :---: | :---: | :--- | :--- |
| **`agent-server-auditor`** | `v1.0.0` | 🚀 Produção | Auditor arquitetural poliglota (`Go`, `TypeScript`, `Python`) para sistemas agênticos, servidores MCP (`2026-07-28`, higiene `STDIO`), nós A2A (`v1.0`, `agent-card.json` JWS), segregação de binários, travas `max_steps` e persistência em `memories/audit_report.json`. | [skills/agent-server-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/agent-server-auditor/SKILL.md) |
| **`organizador-projetos-ideias`** | `v1.0.0` | 🚀 Produção | Organizador de ideias do zero (`ideation_to_v1`) e sincronizador completo de projetos (`project_organizer_sync`: `README.md` fiel ao disco, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `DESIGN.md`, contratos `MCP`/`FastAPI`/`RPC` e limpeza da raiz). | [skills/organizador-projetos-ideias/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-projetos-ideias/SKILL.md) |
| **`antigravity-project-auditor`** | `v2.0.0` | 🚀 Produção | Auditor arquitetural, diagnóstico de MVP e planejamento em 3 fases (`autonomous_scan` vs. `targeted_focus` 80/20) sob 5 pilares técnicos. | [skills/antigravity-project-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/antigravity-project-auditor/SKILL.md) |
| **`code-acceptability-auditor`** | `v1.1.0` | 🚀 Produção | Portão 1 de auditoria estática AST e Pydantic v2 de código Python (`12` regras), Quality Gate (`>= 75/100`) e Trigger Matrix ($F_1 = 1.0$). | [skills/code-acceptability-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-acceptability-auditor/SKILL.md) |
| **`design-md`** | `v5.0.0` | 🚀 Produção | Cria ou atualiza o contrato `DESIGN.md` na raiz do projeto, definindo tokens semânticos, escala tipográfica modular, hierarquia em 3 níveis e composição espacial (`Grid`, `Stack`, `Cluster`, `Split-View`) sem travar cores. | [skills/design-md/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/design-md/SKILL.md) |
| **`frontend-code-architect`** | `v3.0.0` | 🚀 Produção | Implementa e refatora interfaces web (standalone HTML/CSS/JS ou React/Next.js/Tailwind) consumindo o `DESIGN.md`, preservando referências funcionais e garantindo estados FSM e acessibilidade sem engessar estilos. | [skills/frontend-code-architect/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-code-architect/SKILL.md) |
| **`frontend-testing-auditor`** | `v4.0.0` | 🚀 Produção | Gatekeeper determinístico de qualidade Frontend (`scripts/audit_tactile_ui.py` `v4.0`): audita tokens semânticos, composição, WCAG 2.1 AA/AAA, `tabular-nums`, zero emojis, zero bloat Base64, estados FSM e anti-XSS. | [skills/frontend-testing-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-testing-auditor/SKILL.md) |
| **`frontend-ui-ux-auditor`** | `v1.0.0` | 🚀 Produção | Auditor matemático de UI/UX (`scripts/ui_ux_frontend_auditor.py`): escala modular de 8px, contraste WCAG 2.1 AA, densidade DOM (`divsoup <= 0.45`), ícones 1:1, física da luz 135° e transições GPU sem reflow. | [skills/frontend-ui-ux-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-ui-ux-auditor/SKILL.md) |
| **`test-quality-auditor`** | `v1.2.0` | 🚀 Produção | Portão 2 modular em 5 domínios (Python, TS/JS, Go, MCP `JSON-RPC 2.0` e Harness HITL/Evals) + estatística `perfkit_stats.py`. | [skills/test-quality-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/test-quality-auditor/SKILL.md) |
| **`code-quality-audit-3d-physics`** | `v1.0.0` | 🚀 Produção | Auditoria de código e Física 3D em 3 ondas (sanitização AST Py/JS, 5 sub-dimensões de física, testes Pass@10 e observador $S_{\text{norm}}$). | [skills/code-quality-audit-3d-physics/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/SKILL.md) |
| **`organizador-fluxo-arvore-arquivos`** | `v1.2.0` | 🚀 Produção | Converte ideias brutas em diagramas Mermaid, árvores de arquivos e planos de execução, com exportação direta em MD ou PDF. | [skills/organizador-fluxo-arvore-arquivos/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-fluxo-arvore-arquivos/SKILL.md) |
| **`arquiteto-conteudo-solucoes`** | `v2.4.0` | 🚀 Produção | Arquiteto autônomo em 4 modos (Execução Direta, Refinamento, Planejamento Fase 0 e Auto-Reflexão), Prompts Enterprise e Guardrails por Domínio. | [skills/arquiteto-conteudo-solucoes/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/arquiteto-conteudo-solucoes/SKILL.md) |
| **`nav-x-func`** | `v4.0.0` | 🚀 Produção | Planejamento de MVP (`CLAREZA/CREATE`), Ilhas Funcionais (Island UI/UX), navegação real (`Clicar em X ativa Y`, *Dead Ends*), purga de pseudo-complexidade, suficiência funcional (Tabela TIF: Meios vs. Fins) e motor `SGA` determinístico `V1 vs V2` (fusão com `arquitetura-design-implementacao-sistema`). | [skills/nav-x-func/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/nav-x-func/SKILL.md) |
| **`auditoria-projetos-sistema`** | `v3.0.0` | 🚀 Produção | Auditoria estrutural (`AGENTS.md`, desacoplamento, tipagem Pydantic, chunking semântico), alinhamento de composição ao propósito do projeto e esteira `agent-browser` (0-100 pts). | [skills/auditoria-projetos-sistema/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/auditoria-projetos-sistema/SKILL.md) |
| **`context-sentinel`** | `v1.1.0` | 🚀 Produção | Auditoria de integridade da janela de contexto, mitigação de context rot e snapshots determinísticos estruturados Pydantic/SQLite. | [skills/context-sentinel/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/context-sentinel/SKILL.md) |
| **`design-interface-medica-minimalista`** | `v4.0.0` | 🚀 Produção | Arquitetura especializada para interfaces clínicas, PEP, formulários A4 vetoriais (`.sus-grid`) e calculadoras médicas com `tabular-nums`, proteção de unidades e zero emojis. | [skills/design-interface-medica-minimalista/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/design-interface-medica-minimalista/SKILL.md) |
| **`skill-orquestrador-planos-encadeados`** | `v3.0.0` | 🚀 Produção | Compilador e orquestrador executivo de grafos DAG em ondas paralelas (Kahn via `scripts/dag_chain_validator.py`), detector de colisão de arquivos `[P]`, isolamento *Context Fork* ($\le 5$ regras/nó) e roteamento de `fallback_branch` / HITL. | [skills/skill-orquestrador-planos-encadeados/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/skill-orquestrador-planos-encadeados/SKILL.md) |
| **`refine-prompt`** | `v3.2.0` | 🚀 Produção | Auditoria de factibilidade (`[VEREDITO]`), classificação epistêmica (`[FATO]`, `[INFERÊNCIA]`, `[LACUNA]`), modulação de entropia e refinamento Zero-Trust. | [skills/refine-prompt/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/refine-prompt/SKILL.md) |
| **`gap-analyzer-auditor`** | `v2.2.0` | 🚀 Produção | Portão 3 de auditoria de brechas (RCA em 4 vetores), segregação `[FATO]`/`[INFERÊNCIA]`/`[LACUNA]` e convergência Spec-to-Code *append-only*. | [skills/gap-analyzer-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gap-analyzer-auditor/SKILL.md) |
| **`high-level-context-planner`** | `v3.0.0` | 🚀 Produção | Motor cognitivo não-linear (`intent-cognitive-planner` via `scripts/cognitive_plan_builder.py`): triagem de intenção em 4 quadrantes, frameworks (`CLAREZA`/`CREATE` + `CoT`/`ReAct`/`ToT`/`Self-Refine`), blindagem da Parede de Complexidade ($\le 5$ regras/nó), Fase 0 e convergência *append-only*. | [skills/high-level-context-planner/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/high-level-context-planner/SKILL.md) |
| **`gdrive-auditoria-limpeza`** | `v1.0.0` | 🚀 Produção | Varredura de arquivos pesados (>100MB), identificação de duplicados por hash SHA-256 e quarentena segura no Google Drive. | [skills/gdrive-auditoria-limpeza/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-auditoria-limpeza/SKILL.md) |
| **`gdrive-taxonomia-organizacao`** | `v1.1.0` | 🚀 Produção | Estrutura canônica numerada real do Drive, padronização de nomenclatura com datas ISO (YYYY-MM-DD) e triagem documental. | [skills/gdrive-taxonomia-organizacao/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-taxonomia-organizacao/SKILL.md) |
| **`manutencao-disco-windows`** | `v1.1.0` | 🚀 Produção | Manutenção do SO Windows 11: triagem de Downloads, Desktop, isolamento de instaladores e arquivamento em `dev\`. | [skills/manutencao-disco-windows/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/manutencao-disco-windows/SKILL.md) |
| **`curadoria-obsidian-vault`** | `v1.1.0` | 🚀 Produção | Curadoria do cofre Obsidian (`C:\Users\melki\dev\notes\`): validação de frontmatter YAML, `[[Wikilinks]]` e anexos órfãos. | [skills/curadoria-obsidian-vault/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/curadoria-obsidian-vault/SKILL.md) |
| **`redator-tecnico-markdown`** | `v1.2.0` | 🚀 Produção | Redação técnica de relatórios executivos, notas técnicas e documentações compatíveis com `C:\Users\melki\dev\notes\Inbox\`. | [skills/redator-tecnico-markdown/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/redator-tecnico-markdown/SKILL.md) |
| **`conversor-html-pdf`** | `v1.0.0` | 🚀 Produção | Conversão determinística de Markdown/HTML para PDF profissional via Edge headless com CSS de impressão calibrado. | [skills/conversor-html-pdf/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/conversor-html-pdf/SKILL.md) |

---

## Histórico de Versões Recentes (Changelog)

### [2026-10-26] - Fase 26: Incorporação do Motor `intent-cognitive-planner`, Compilador Kahn DAG e Sanitização Geral (`25/25 PASS`)
- **`high-level-context-planner` `v3.0.0` (Motor Cognitivo Não-Linear `intent-cognitive-planner`)**:
  - Incorporada a triagem semântica em 4 quadrantes (`direta`, `estruturada`, `ambigua`, `mutacao_critica_hitl`), seleção combinada de frameworks estruturais (`CLAREZA`, `CREATE`, `RTF`, `TAG`, `TASS`) e cognitivos não-lineares (`CoT`, `ReAct`, `ToT`, `Self-Refine`) e blindagem contra a Parede de Complexidade de Prompts ($\le 5$ regras ativas por nó).
  - Adicionado script determinístico [`scripts/cognitive_plan_builder.py`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/high-level-context-planner/scripts/cognitive_plan_builder.py) (`100.0/100.0` AST Score) com auto-subdivisão de nós sobrecarregados e exportação direta para `DAGExecutionPlan`.
- **`skill-orquestrador-planos-encadeados` `v3.0.0` (Compilador de Ondas DAG Kahn & Context Fork)**:
  - Adicionado script determinístico [`scripts/dag_chain_validator.py`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/skill-orquestrador-planos-encadeados/scripts/dag_chain_validator.py) (`100.0/100.0` AST Score) para compilação em ondas paralelas (Kahn), detecção de ciclos (`CYCLE_DETECTED`), guarda contra colisão de escrita em arquivos paralelos (`PARALLEL_FILE_COLLISION`) e isolamento de estado (*Context Fork*).
- **Sanitização Geral de Links Legados e Runtime (`shared/modular_orchestrator.py`)**:
  - Removidos todos os links quebrados para `../_template` e `../minimal-impact-ui` e blocos de cores hexadecimais duplicados em `high-level-context-planner`, `skill-orquestrador-planos-encadeados` e `gap-analyzer-auditor` (`v2.2.0`).

### [2026-10-22] - Fase 25: Auditoria Forense REA, Desengessamento Visual das Skills de Frontend, Exclusão das Meta-Skills de Criação de Skills e Consolidação da SSOT (`24/24 PASS`)
- **Remoção Definitiva de Meta-Skills de Criação de Skills e Duplicatas Visuais (`29 -> 24 Skills Canônicas`)**:
  - Excluídas `_template`, `evoluir-skills`, `aprimoramento-expansibilidade-agentes-skills`, `skill-auditor-refatorador-skills`, `minimal-impact-ui`, `expansao-contexto-adaptativa` e `skill-creator`, além dos 3 arquivos HTML pesados em `skills/design-md/references/` (`~330 KB`), que replicavam tabelas rígidas de cores e regras redundantes em múltiplos pontos.
- **Unificação das Preferências de Design e Estilo em um Único Lugar (SSOT)**:
  - Consolidado o Roadmap e Guia Canônico de Preferências exclusivamente em [`C:\Users\melki\dev\notes\Memória\Preferências de Trabalho com Agentes.md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md), eliminando todas as repetições de paletas hexadecimais nas demais skills.
- **Reescrita e Simplificação das 4 Skills de Frontend (`design-md` `v5.0.0`, `frontend-code-architect` `v3.0.0`, `frontend-testing-auditor` `v4.0.0`, `design-interface-medica-minimalista` `v4.0.0`)**:
  - Foco em **composição espacial** (`Grid`, `Stack`, `Cluster`, `Split-View`), **hierarquia visual em 3 níveis (Squint Test)**, **escala tipográfica modular** (`1.2`/`1.25` + `clamp()` + `tabular-nums`) e **tokens semânticos livres de cores travadas**.
  - Substituída a persona `FrontCraftMaster` por **`UI-Architect`** (desvinculando o catálogo do projeto em construção `frontcraft-studio`).
