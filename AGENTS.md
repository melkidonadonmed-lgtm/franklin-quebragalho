# Arquitetura de Agentes: Franklin Quebra-Galho

Este documento estabelece o modelo operacional, comandos executáveis, papéis e contratos de orquestração para o workspace `franklin-quebragalho`.

## Comandos Executáveis (Command-First)
- **Testes Unitários & Contratos MCP (`52/52`)**: `uv run pytest -q`
- **Validador Determinístico do Catálogo (`26/26` skills)**: `uv run python scripts/validate_skills.py`
- **Auditoria AST de Qualidade (`Quality Score >= 75`)**: `uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py server.py`
- **Sincronização do Ecossistema (`~/.gemini` & Plugins)**: `uv run python scripts/sync_gemini_ecosystem.py`

---

## Agente Principal: Franklin Quebra-Galho

- **Tipo**: Orquestrador Geral e Par de Programação / Automação.
- **Responsabilidade**:
  - Receber pedidos em linguagem natural do usuário.
  - Avaliar o escopo do pedido e selecionar as ferramentas ou subagentes adequados.
  - Executar tarefas rápidas diretamente ou delegar tarefas especializadas/pesadas para subagentes.
  - Assegurar que os princípios de segurança, integridade de dados e linguagem (pt-BR) sejam seguidos rigidamente.

---

## Especialistas e Subagentes (Personas)

| Agente / Persona | Foco Principal | Ferramentas Típicas | Gatilho de Uso |
| :--- | :--- | :--- | :--- |
| **`UI-Architect`** | Arquitetura Visual por Propósito, Composição Espacial & Frontend (`DESIGN.md` & SSOT) | `agent-browser`, `design-md`, `frontend-code-architect`, `frontend-testing-auditor`, `frontend-ui-ux-auditor`, `auditoria-projetos-sistema`, `design-interface-medica-minimalista` | Diagnóstico do propósito do projeto, definição de tokens semânticos sem cores travadas, hierarquia visual em 3 níveis (Squint Test), escala modular `clamp()` + `tabular-nums`, composição (`Grid`, `Stack`, `Cluster`, `Split-View`) e auditoria `AUDIT-VIS-01` / FSM. |
| **`DriveMaster`** | Organização do Google Drive | Unidade `G:\Meu Drive`, `gdrive-auditoria-limpeza`, `gdrive-taxonomia-organizacao`, MCP `workspace-mcp` | Pedidos de triagem de pastas no Drive, auditoria de arquivos pesados, duplicações ou padronização de nomenclatura. |
| **`FileOpsLocal`** | Manutenção de Pastas no Windows | PowerShell 7 (`pwsh`), `manutencao-disco-windows`, `tools\agent-hub.ps1`, `Get-ChildItem`, `Move-Item` | Limpeza de Downloads, organização de Desktop, arquivamento de projetos em `dev/`. |
| **`VaultMaster`** | Gestão do Obsidian Vault (PKM) | `curadoria-obsidian-vault`, `obsidian-vault`, MemPalace (`wing: notes`), frontmatter YAML, links bidirecionais | Curadoria de notas, limpeza de anexos órfãos, integridade de metadados e sincronização com MemPalace. |
| **`DocMaker`** | Criação e Conversão de Documentos | `redator-tecnico-markdown`, `conversor-html-pdf`, `organizador-fluxo-arvore-arquivos`, Edge/Chrome headless | Criação de notas técnicas, relatórios executivos, fluxos Mermaid e geração de PDFs profissionais. |
| **`SkillCraft`** | Qualidade Determinística de Código, Testes & Servidores Agênticos | `code-acceptability-auditor`, `test-quality-auditor`, `agent-server-auditor`, [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md) | Auditoria estática AST/Pydantic (`Quality Score >= 75`), Pass@k, qualidade de suítes de testes em 5 módulos e auditoria arquitetural de agentes/MCP/A2A. |
| **`LoopPlanner`** | Orquestração Closed-Loop | `high-level-context-planner`, `gap-analyzer-auditor`, `skill-orquestrador-planos-encadeados` | Planejamento em malha fechada, decomposição em fases com Fase 0, RCA determinístico e replanejamento v2.0. |
| **`Franklin-Main`** | Orquestrador Geral, Arquitetura & Física 3D | `arquiteto-conteudo-solucoes`, `nav-x-func`, `auditoria-projetos-sistema`, `antigravity-project-auditor`, `organizador-projetos-ideias`, `code-quality-audit-3d-physics`, `context-sentinel`, `refine-prompt` | Execução direta de baixo atrito, organização de projetos e refinamento de ideias, auditoria de navegação e suficiência funcional (`nav-x-func`), auditoria estrutural e diagnóstico de MVP de repositórios, física 3D/WebGL (`Snorm`), sentinela de contexto e refinamento de prompts. |

---

## Matriz de Orquestração Eficiente & Interativa (5 Camadas Multi-Repo)

Para máxima eficiência (zero desperdício de tokens e zero fricção cognitiva TDAH), os agentes de todo o workspace (`C:\Users\melki\dev\repos\`) operam em **5 camadas coordenadas**:

| Camada | Escopo & Agentes | Repositórios / Runtimes | Gatilho Interativo / Comando Rápido | Custo de Tokens |
| :---: | :--- | :--- | :--- | :---: |
| **0** | **Bússola & Heartbeat Zero-LLM** (`Smart Compass`, `FastNodeHealthGate`, `AgentHub`) | `franklin-quebragalho`, `adk-tests`, `dev\tools\agent-hub.ps1` | `franklin_smart_compass(intent_or_path)` \| `pwsh C:\Users\melki\dev\tools\agent-hub.ps1` \| `POST /rpc` (`mesh/heartbeat`) | **0 tokens** (Determinístico) |
| **1** | **Execução Direta & Loop Fechado** (`Franklin-Main`, `LoopPlanner`, `IntentRouterAgent`) | `franklin-quebragalho`, `adk-tests/py_agent` | Pedidos simples: entrega direta sem entrevista (`<user_rules>` > `franklin-skills` > `superpowers`). Complexos: Fase 0 (`high-level-context-planner`) $\to$ RCA (`gap-analyzer-auditor`). | Baixo / Proporcional |
| **2** | **Esquadrão de UI/UX Orientado ao Propósito** (`UI-Architect` + Topologia `3+1`) | `franklin-quebragalho/agents`, `epic-volta` | Nativo: `invoke_subagent` (`ui-shell-navigator` $\to$ `ui-controls-data` + `ui-motion-interaction` $\to$ `ui-deterministic-observer`) \| DAG: `franklin_execute_dag("ui")` | Médio (Ondas Paralelas) |
| **3** | **Gatekeepers Determinísticos AST/Pass@k** (`SkillCraft`, `CodeAcceptability`, `TestQuality`, `3DPhysics`) | `franklin-quebragalho`, `adk-go-mcp` (`eval_subagent.go`) | `franklin_run_skill_script("code-auditor", "code_acceptability_auditor.py")` \| `franklin_execute_dag("physics")` \| `dispatch_skill_deterministic_tests` | **0 tokens** (AST / Go Harness) |
| **4** | **Malha Multiagente Cloud/Web & Clínica** (`ADK Mesh`, `Epic-Volta`, `MCP-Web-Agents 4+1`, `PresCMed Reviewer`) | `adk-tests`, `epic-volta`, `mcp-web-agents`, `PCM`, `scoreboard` | Cockpit Voz/1-Clique (`:3000` / `:8080/mcp/ui`) \| `execute_autonomous_mesh_cycle` \| `python mcp_bridge_agent.py --diagnose` \| `agy_deterministic_calc_suite` | Sob Demanda + Fallback Ollama |

---

## Esquadrão de Subagentes de UI (`Topologia 3+1` sob `UI-Architect`)

Os módulos de engenharia visual e interação ficam consolidados em **4 Subagentes Especialistas** na pasta [`agents/`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/) e orquestrados em **3 ondas determinísticas** tanto pelo **Modo Nativo Antigravity (`invoke_subagent`)** quanto pelo **Modo Motor DAG Assíncrono (Kahn)** via [`plans/ui_composition_dag.json`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/plans/ui_composition_dag.json) no Epic-Volta:

| Onda | Subagente (`agents/*.md`) | Módulos Cobertos | Entregável Determinístico (`upstream_mapping`) |
| :---: | :--- | :--- | :--- |
| **1** | **[`ui-shell-navigator`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-shell-navigator.md)** | **1. Propósito & Tokens Semânticos**<br/>**2. Composição Espacial & Navegação** | `layout_contract` (Tokens semânticos sem cores travadas, Bento Grid 12 col, Stack, Cluster, Split-View, $\text{CLS} < 0.1$) + `navigation_contract` (`Ctrl+K`, $\le 3$ cliques) |
| **2A** | **[`ui-controls-data`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-controls-data.md)** | **3. Superfícies & Equilíbrio 90/8/2**<br/>**4. Tipografia, Dados & FSM** | `controls_contract` (Hierarquia em 3 níveis, 1 CTA sólido vs `.btn-ghost`, $\ge 44\times44\text{px}$) + `data_feedback_contract` (`clamp()`, `tabular-nums`, FSM 5 estados, `aria-live`) |
| **2B** | **[`ui-motion-interaction`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-motion-interaction.md)** | **5.1 Transições & Micro-interações**<br/>**5.2 Ergonomia Multi-Input** | `motion_contract` (`--ease-spring`, `prefers-reduced-motion`) + `interaction_contract` (`Touch/Pen/Mouse/Key`, `:focus-visible`) |
| **3** | **[`ui-deterministic-observer`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-deterministic-observer.md)** | **5.3 Coordenador Determinístico**<br/>**6. Auditoria de Composição & QA** | `observer_audit_report` (Alinhamento ao propósito, WCAG 2.1 AA/AAA, zero emojis, zero bloat Base64, FSM executável e `audit_tactile_ui.py` $\ge 90/100$) |

---

## Protocolo de Delegação e Orquestração

1. **Triagem de Demanda**:
   O Franklin avalia se a tarefa pode ser executada em um único turno com ferramentas normais ou se demanda análise extensiva / pesquisa em segundo plano.

2. **Uso de Subagentes (`invoke_subagent` / `franklin_get_agents` / `franklin_execute_dag` / Epic-Volta CLI)**:
   - Para descoberta rápida da topologia completa de agentes e comandos prontos: `franklin_get_agents(agent_name="ecosystem")` ou `franklin_smart_compass(intent_or_path="...")`.
   - Para composições multi-tela de UI/UX (`Topologia 3+1`): acionar `invoke_subagent` ou `franklin_execute_dag(plan_path_or_json="plans/ui_composition_dag.json")` (ou alias `"ui"`).

3. **Diretriz Anti-Sobre-Engenharia**:
   - Pedidos simples ou de arquivo único exigem resposta direta e rápida, sem burocracia de múltiplos subagentes.

---

## Documentos Relacionados

- [MY_AGENTS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_AGENTS.md): Detalhamento dos perfis e prompts dos agentes.
- [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md): Catálogo de skills disponíveis para os agentes.
- [GEMINI.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/GEMINI.md): Regras globais de ambiente e segurança.
- [Preferências de Trabalho com Agentes.md](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md): Fonte Única de Verdade (SSOT) de preferências de design, composição e engenharia.
