# Arquitetura de Agentes: Franklin Quebra-Galho

Este documento estabelece o modelo operacional, comandos executáveis, papéis e contratos de orquestração para o workspace `franklin-quebragalho`.

## ⚡ Comandos Executáveis (Command-First)
- **Testes Unitários & Contratos MCP (`52/52`)**: `uv run pytest -q`
- **Validador Determinístico do Catálogo (`28/28` skills)**: `uv run python scripts/validate_skills.py`
- **Auditoria AST de Qualidade (`Quality Score >= 75`)**: `uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py server.py`
- **Sincronização do Ecossistema (`~/.gemini` & Plugins)**: `uv run python scripts/sync_gemini_ecosystem.py`

---

## 🧭 Agente Principal: Franklin Quebra-Galho

- **Tipo**: Orquestrador Geral e Par de Programação / Automação.
- **Responsabilidade**:
  - Receber pedidos em linguagem natural do usuário.
  - Avaliar o escopo do pedido e selecionar as ferramentas ou subagentes adequados.
  - Executar tarefas rápidas diretamente ou delegar tarefas especializadas/pesadas para subagentes.
  - Assegurar que os princípios de segurança, integridade de dados e linguagem (pt-BR) sejam seguidos rigidamente.

---

## 👥 Especialistas e Subagentes (Personas)

| Agente / Persona | Foco Principal | Ferramentas Típicas | Gatilho de Uso |
| :--- | :--- | :--- | :--- |
| **`FrontCraftMaster`** | Arquitetura Visual por Propósito, Temas & Frontend (`preferencias_estilo_e_temas.md` & `minimal-impact-ui`) | `agent-browser`, `minimal-impact-ui`, `design-md`, `frontend-code-architect`, `frontend-testing-auditor`, `auditoria-projetos-sistema`, `design-interface-medica-minimalista` | Diagnóstico do propósito do projeto, seleção de atmosfera (*Ad Lucem*, *Cinza Monolítico `#57545d` + Menus `#8e8999`*, *Preto Terminal IBM `Ex Umbris` + `IBM Plex`* ou *AETHER 2027*), 6 Arquétipos de Página, 28 efeitos WinUI 3 + Ex Umbris, zero texto vermelho borrado no cinza/escuro (`.highlight-surgical`) e auditoria `AUDIT-VIS-01` / FSM. |
| **`DriveMaster`** | Organização do Google Drive | Unidade `G:\Meu Drive`, `gdrive-auditoria-limpeza`, `gdrive-taxonomia-organizacao`, MCP `workspace-mcp` | Pedidos de triagem de pastas no Drive, auditoria de arquivos pesados, duplicações ou padronização de nomenclatura. |
| **`FileOpsLocal`** | Manutenção de Pastas no Windows | PowerShell 7 (`pwsh`), `manutencao-disco-windows`, `tools\agent-hub.ps1`, `Get-ChildItem`, `Move-Item` | Limpeza de Downloads, organização de Desktop, arquivamento de projetos em `dev/`. |
| **`VaultMaster`** | Gestão do Obsidian Vault (PKM) | `curadoria-obsidian-vault`, `obsidian-vault`, MemPalace (`wing: notes`), frontmatter YAML, links bidirecionais | Curadoria de notas, limpeza de anexos órfãos, integridade de metadados e sincronização com MemPalace. |
| **`DocMaker`** | Criação e Conversão de Documentos | `redator-tecnico-markdown`, `conversor-html-pdf`, `organizador-fluxo-arvore-arquivos`, Edge/Chrome headless | Criação de notas técnicas, relatórios executivos, fluxos Mermaid e geração de PDFs profissionais. |
| **`SkillCraft`** | Engenharia, Auditoria e Evolução de Skills & Código | `evoluir-skills`, `skill-auditor-refatorador-skills`, `aprimoramento-expansibilidade-agentes-skills`, `code-acceptability-auditor`, `test-quality-auditor`, `_template`, [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md) | Desenvolvimento e refatoração de skills, auditoria estática AST/Pydantic (`Quality Score >= 75`), Pass@k e qualidade de suítes de testes. |
| **`LoopPlanner`** | Orquestração Closed-Loop | `high-level-context-planner`, `gap-analyzer-auditor`, `skill-orquestrador-planos-encadeados` | Planejamento em malha fechada, decomposição em fases com Fase 0, RCA determinístico e replanejamento v2.0. |
| **`Franklin-Main`** | Orquestrador Geral, Arquitetura & Física 3D | `arquiteto-conteudo-solucoes`, `arquitetura-design-implementacao-sistema`, `auditoria-projetos-sistema`, `antigravity-project-auditor`, `code-quality-audit-3d-physics`, `context-sentinel`, `refine-prompt` | Execução direta de baixo atrito, auditoria estrutural e diagnóstico de MVP de repositórios, física 3D/WebGL (`Snorm`), sentinela de contexto e refinamento de prompts. |

---

## ⚡ Matriz de Orquestração Eficiente & Interativa (5 Camadas Multi-Repo)

Para máxima eficiência (zero desperdício de tokens e zero fricção cognitiva TDAH), os agentes de todo o workspace (`C:\Users\melki\dev\repos\`) operam em **5 camadas coordenadas**:

| Camada | Escopo & Agentes | Repositórios / Runtimes | Gatilho Interativo / Comando Rápido | Custo de Tokens |
| :---: | :--- | :--- | :--- | :---: |
| **0** | **Bússola & Heartbeat Zero-LLM** (`Smart Compass`, `FastNodeHealthGate`, `AgentHub`) | `franklin-quebragalho`, `adk-tests`, `dev\tools\agent-hub.ps1` | `franklin_smart_compass(intent_or_path)` \| `pwsh C:\Users\melki\dev\tools\agent-hub.ps1` \| `POST /rpc` (`mesh/heartbeat`) | **0 tokens** (Determinístico) |
| **1** | **Execução Direta & Loop Fechado** (`Franklin-Main`, `LoopPlanner`, `IntentRouterAgent`) | `franklin-quebragalho`, `adk-tests/py_agent` | Pedidos simples: entrega direta sem entrevista (`<user_rules>` > `franklin-skills` > `superpowers`). Complexos: Fase 0 (`high-level-context-planner`) $\to$ RCA (`gap-analyzer-auditor`). | Baixo / Proporcional |
| **2** | **Esquadrão de UI/UX Orientado ao Propósito** (`FrontCraftMaster` + Topologia `3+1`) | `franklin-quebragalho/agents`, `frontcraft-studio`, `epic-volta` | Nativo: `invoke_subagent` (`ui-shell-navigator` $\to$ `ui-controls-data` + `ui-motion-interaction` $\to$ `ui-deterministic-observer`) \| DAG: `franklin_execute_dag("ui")` | Médio (Ondas Paralelas) |
| **3** | **Gatekeepers Determinísticos AST/Pass@k** (`SkillCraft`, `CodeAcceptability`, `TestQuality`, `3DPhysics`) | `franklin-quebragalho`, `adk-go-mcp` (`eval_subagent.go`) | `franklin_run_skill_script("code-auditor", "code_acceptability_auditor.py")` \| `franklin_execute_dag("physics")` \| `dispatch_skill_deterministic_tests` | **0 tokens** (AST / Go Harness) |
| **4** | **Malha Multiagente Cloud/Web & Clínica** (`ADK Mesh`, `Epic-Volta`, `MCP-Web-Agents 4+1`, `PresCMed Reviewer`) | `adk-tests`, `epic-volta`, `mcp-web-agents`, `PCM`, `scoreboard` | Cockpit Voz/1-Clique (`:3000` / `:8080/mcp/ui`) \| `execute_autonomous_mesh_cycle` \| `python mcp_bridge_agent.py --diagnose` \| `agy_deterministic_calc_suite` | Sob Demanda + Fallback Ollama |

---

## 🔄 Esquadrão de Subagentes de UI (`Topologia 3+1` sob `FrontCraftMaster`)

Os 6 módulos de engenharia visual e interação ficam consolidados em **4 Subagentes Especialistas** na pasta [`agents/`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/) e orquestrados em **3 ondas determinísticas** tanto pelo **Modo Nativo Antigravity (`invoke_subagent`)** quanto pelo **Modo Motor DAG Assíncrono (Kahn)** via [`plans/ui_composition_dag.json`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/plans/ui_composition_dag.json) no Epic-Volta:

| Onda | Subagente (`agents/*.md`) | Módulos Cobertos | Entregável Determinístico (`upstream_mapping`) |
| :---: | :--- | :--- | :--- |
| **1** | **[`ui-shell-navigator`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-shell-navigator.md)** | **1. Propósito, Atmosfera & Layout**<br/>**2. Bento Grid & Navegação** | `layout_contract` (Atmosfera por objetivo, Bento Grid 12 col, respiro $\ge 25\%$, $\text{CLS} < 0.1$) + `navigation_contract` (Menus em pílula `#8e8999` com tinta escura nítida, `Ctrl+K`, $\le 3$ cliques) |
| **2A** | **[`ui-controls-data`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-controls-data.md)** | **3. Camadas Esculpidas & Acento**<br/>**4. Tipografia, Dados & FSM** | `controls_contract` (`<SurfaceCard />`, sombra 3 camadas + `1px` Rim Light, 1 CTA sólido vs `.btn-ghost`, $\ge 44\times44\text{px}$ anti-squish) + `data_feedback_contract` (`clamp()`, `tabular-nums`, FSM 4 estados, `aria-live`) |
| **2B** | **[`ui-motion-interaction`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-motion-interaction.md)** | **5.1 Física Spring & Transições**<br/>**5.2 Gestos & Multi-Input** | `motion_contract` (`--ease-spring`, micro-interações de elevação/pressão, `prefers-reduced-motion`) + `interaction_contract` (`Touch/Pen/Mouse/Key`, `:focus-visible`) |
| **3** | **[`ui-deterministic-observer`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-deterministic-observer.md)** | **5.3 Coordenador Determinístico**<br/>**6. Auditoria de Propósito & QA** | `observer_audit_report` (Alinhamento ao propósito, WCAG 2.1 AA/AAA, CWV $\text{LCP}<2.5\text{s}/\text{INP}<200\text{ms}/\text{CLS}<0.1$, FSM sem comment-gaming e `audit_tactile_ui.py` $\ge 90/100$) |

---

## 🔄 Protocolo de Delegação e Orquestração

1. **Triagem de Demanda**:
   O Franklin avalia se a tarefa pode ser executada em um único turno com ferramentas normais ou se demanda análise extensiva / pesquisa em segundo plano.

2. **Uso de Subagentes (`invoke_subagent` / `franklin_get_agents` / `franklin_execute_dag` / Epic-Volta CLI)**:
   - Para descoberta rápida da topologia completa de agentes e comandos prontos: `franklin_get_agents(agent_name="ecosystem")` ou `franklin_smart_compass(intent_or_path="...")`.
   - Para pesquisas longas ou exploração profunda no disco/Drive: acionar a skill especialista ou persona correspondente.
   - Para composições completas de UI/UX (`Topologia 3+1`):
     - **Modo Nativo Antigravity (`invoke_subagent` / `define_subagent`)**: acionar os subagentes registrados pelo plugin `franklin-skills` em `<subagents>` em 3 ondas (`Onda 1`: `invoke_subagent(TypeName="ui-shell-navigator")`; `Onda 2` paralela: `invoke_subagent(TypeName="ui-controls-data")` e `invoke_subagent(TypeName="ui-motion-interaction")`; `Onda 3`: `invoke_subagent(TypeName="ui-deterministic-observer")`).
     - **Modo Motor DAG Assíncrono (`franklin_execute_dag` / `franklin_get_agents` / `epic-volta`)**: carregar os contratos em `agents/*.md` via `franklin_get_agents(agent_name="ui")` e executar `franklin_execute_dag(plan_path_or_json="plans/ui_composition_dag.json")` (ou alias `"ui"`).

3. **Validação e Entrega**:
   - Todo relatório de ação deve conter links clicáveis para os arquivos gerados ou pastas organizadas.
   - Antes de aplicar alterações em massa, o agente deve apresentar a simulação dos impactos.

4. **Diretriz Anti-Sobre-Engenharia**:
   - É expressamente proibido disparar esteiras de subagentes para criar aplicações web (Node/React/Vite/OAuth) para tarefas que demandam apenas manipulação de arquivos, atalhos do Windows ou relatórios locais.

---

## 📚 Documentos Relacionados

- [MY_AGENTS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_AGENTS.md): Detalhamento dos perfis e prompts dos agentes.
- [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md): Catálogo de skills disponíveis para os agentes.
- [GEMINI.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/GEMINI.md): Regras globais de ambiente e segurança.

---

<!-- WORKSPACE-CONTEXT START -->
## Referências Globais do Workspace
- Diretrizes globais de engenharia, arquitetura visual por propósito e memória: [C:\Users\melki\dev\AGENTS.md](file:///C:/Users/melki/dev/AGENTS.md) e [Preferências de Trabalho com Agentes.md](file:///C:/Users/melki/dev/notes/Memória/Preferências%20de%20Trabalho%20com%20Agentes.md).
<!-- WORKSPACE-CONTEXT END -->
