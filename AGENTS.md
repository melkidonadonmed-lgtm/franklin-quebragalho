# Arquitetura de Agentes: Franklin Quebra-Galho

Este documento estabelece o modelo operacional, papéis e contratos de orquestração para os agentes e subagentes dentro do workspace `franklin-quebra-galho`.

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
| **`FrontCraftMaster`** | Design System Tátil (`DESIGN.md v4.5-soft`) & Frontend | `agent-browser`, `design-md`, `frontend-code-architect`, `frontend-testing-auditor`, `analise-design-tatil-frontend`, `consultor-design-tatil-frontend`, `refatoracao-design-tatil-frontend`, `design-interface-medica-minimalista` | Diagnóstico comparativo de interfaces, Atomic Design (5 camadas), Economia 60-30-10, luz 135°, zero cobalto (`Cerulean Sapphire #0284C7`) e auditoria `AUDIT-VIS-01` / FSM. |
| **`DriveMaster`** | Organização do Google Drive | Unidade `G:\Meu Drive`, `gdrive-auditoria-limpeza`, `gdrive-taxonomia-organizacao`, MCP `workspace-mcp` | Pedidos de triagem de pastas no Drive, auditoria de arquivos pesados, duplicações ou padronização de nomenclatura. |
| **`FileOpsLocal`** | Manutenção de Pastas no Windows | PowerShell 7 (`pwsh`), `manutencao-disco-windows`, `tools\agent-hub.ps1`, `Get-ChildItem`, `Move-Item` | Limpeza de Downloads, organização de Desktop, arquivamento de projetos em `dev/`. |
| **`VaultMaster`** | Gestão do Obsidian Vault (PKM) | `curadoria-obsidian-vault`, `obsidian-vault`, MemPalace (`wing: notes`), frontmatter YAML, links bidirecionais | Curadoria de notas, limpeza de anexos órfãos, integridade de metadados e sincronização com MemPalace. |
| **`DocMaker`** | Criação e Conversão de Documentos | `redator-tecnico-markdown`, `conversor-html-pdf`, `organizador-fluxo-arvore-arquivos`, Edge/Chrome headless | Criação de notas técnicas, relatórios executivos, fluxos Mermaid e geração de PDFs profissionais. |
| **`SkillCraft`** | Engenharia, Auditoria e Evolução de Skills & Código | `evoluir-skills`, `skill-auditor-refatorador-skills`, `aprimoramento-expansibilidade-agentes-skills`, `code-acceptability-auditor`, `test-quality-auditor`, `_template`, [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md) | Desenvolvimento e refatoração de skills, auditoria estática AST/Pydantic (`Quality Score >= 75`), Pass@k e qualidade de suítes de testes. |
| **`LoopPlanner`** | Orquestração Closed-Loop | `high-level-context-planner`, `gap-analyzer-auditor`, `skill-orquestrador-planos-encadeados` | Planejamento em malha fechada, decomposição em fases com Fase 0, RCA determinístico e replanejamento v2.0. |
| **`Franklin-Main`** | Orquestrador Geral, Arquitetura & Física 3D | `arquiteto-conteudo-solucoes`, `arquitetura-design-implementacao-sistema`, `auditoria-projetos-sistema`, `code-quality-audit-3d-physics`, `context-sentinel`, `refine-prompt` | Execução direta de baixo atrito, auditoria estrutural de repositórios, física 3D/WebGL (`Snorm`), sentinela de contexto e refinamento de prompts. |

---

## ⚡ Matriz de Orquestração Eficiente & Interativa (5 Camadas Multi-Repo)

Para máxima eficiência (zero desperdício de tokens e zero fricção cognitiva TDAH), os agentes de todo o workspace (`C:\Users\melki\dev\repos\`) operam em **5 camadas coordenadas**:

| Camada | Escopo & Agentes | Repositórios / Runtimes | Gatilho Interativo / Comando Rápido | Custo de Tokens |
| :---: | :--- | :--- | :--- | :---: |
| **0** | **Bússola & Heartbeat Zero-LLM** (`Smart Compass`, `FastNodeHealthGate`, `AgentHub`) | `franklin-quebragalho`, `adk-tests`, `dev\tools\agent-hub.ps1` | `franklin_smart_compass(intent_or_path)` \| `pwsh C:\Users\melki\dev\tools\agent-hub.ps1` \| `POST /rpc` (`mesh/heartbeat`) | **0 tokens** (Determinístico) |
| **1** | **Execução Direta & Loop Fechado** (`Franklin-Main`, `LoopPlanner`, `IntentRouterAgent`) | `franklin-quebragalho`, `adk-tests/py_agent` | Pedidos simples: entrega direta sem entrevista (`<user_rules>` > `franklin-skills` > `superpowers`). Complexos: Fase 0 (`high-level-context-planner`) $\to$ RCA (`gap-analyzer-auditor`). | Baixo / Proporcional |
| **2** | **Esquadrão de UI/UX Soft Tactile** (`FrontCraftMaster` + Topologia `3+1`) | `franklin-quebragalho/agents`, `frontcraft-studio`, `epic-volta` | Nativo: `invoke_subagent` (`ui-shell-navigator` $\to$ `ui-controls-data` + `ui-motion-interaction` $\to$ `ui-deterministic-observer`) \| DAG: `franklin_execute_dag("ui")` | Médio (Ondas Paralelas) |
| **3** | **Gatekeepers Determinísticos AST/Pass@k** (`SkillCraft`, `CodeAcceptability`, `TestQuality`, `3DPhysics`) | `franklin-quebragalho`, `adk-go-mcp` (`eval_subagent.go`) | `franklin_run_skill_script("code-auditor", "code_acceptability_auditor.py")` \| `franklin_execute_dag("physics")` \| `dispatch_skill_deterministic_tests` | **0 tokens** (AST / Go Harness) |
| **4** | **Malha Multiagente Cloud/Web & Clínica** (`ADK Mesh`, `Epic-Volta`, `MCP-Web-Agents 4+1`, `PresCMed Reviewer`) | `adk-tests`, `epic-volta`, `mcp-web-agents`, `PCM`, `scoreboard` | Cockpit Voz/1-Clique (`:3000` / `:8080/mcp/ui`) \| `execute_autonomous_mesh_cycle` \| `python mcp_bridge_agent.py --diagnose` \| `agy_deterministic_calc_suite` | Sob Demanda + Fallback Ollama |

---

## 🔄 Esquadrão de Subagentes de UI (`Topologia 3+1` sob `FrontCraftMaster`)

Os 6 módulos de engenharia visual e interação ficam consolidados em **4 Subagentes Especialistas** na pasta [`agents/`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/) e orquestrados em **3 ondas determinísticas** tanto pelo **Modo Nativo Antigravity (`invoke_subagent`)** quanto pelo **Modo Motor DAG Assíncrono (Kahn)** via [`plans/ui_composition_dag.json`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/plans/ui_composition_dag.json) no Epic-Volta:

| Onda | Subagente (`agents/*.md`) | Módulos Cobertos | Entregável Determinístico (`upstream_mapping`) |
| :---: | :--- | :--- | :--- |
| **1** | **[`ui-shell-navigator`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-shell-navigator.md)** | **1. Arquitetura Visual e Layout**<br/>**2. Navegação e Menus** | `layout_contract` (*UI Islands*, Grid/SplitView, `AppWindow`, `Shadow DOM`, $\text{CLS} < 0.1$) + `navigation_contract` (`MenuBar`, `TabView` lazy, `TreeView` async, `SemanticZoom`, `Ctrl+K`) |
| **2A** | **[`ui-controls-data`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-controls-data.md)** | **3. Entrada, Seleção e Ações**<br/>**4. Exibição de Dados e Feedback** | `controls_contract` ($\ge 44\times44\text{px}$, anti-squish, Regra 1+2, WAI-ARIA inline) + `data_feedback_contract` (`ListView`/`ItemsView` virtualizados a $60\text{fps}$, `aria-live`, links/ícones WCAG) |
| **2B** | **[`ui-motion-interaction`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-motion-interaction.md)** | **5.1 Efeitos Visuais e Transições**<br/>**5.2 Gestos e Interações** | `motion_contract` (`ConnectedAnimation`, `ImplicitTransition` via GPU, `prefers-reduced-motion`) + `interaction_contract` (`Touch/Pen/Mouse/Key`, `PullToRefresh`) |
| **3** | **[`ui-deterministic-observer`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/ui-deterministic-observer.md)** | **5.3 Coordenador Determinístico**<br/>**6. Diretrizes e Boas Práticas** | `observer_audit_report` (*State Bus*, WCAG 2.1 AA/AAA, CWV $\text{LCP}<2.5\text{s}/\text{INP}<200\text{ms}/\text{CLS}<0.1$, Web Workers, Tipagem/DI **Hilt**, Testes e Fidelidade Física de Luz/Sombra) |

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

## Diretrizes Globais de Qualidade, Eficiência, Orquestração de Agentes e Execução Adaptativa
Este repositório segue as diretrizes globais do workspace:
- **Regras do Workspace (`dev`)**: [AGENTS.md](file:///C:/Users/melki/dev/AGENTS.md), [GEMINI.md](file:///C:/Users/melki/dev/GEMINI.md) e Hub Interativo [`tools\agent-hub.ps1`](file:///C:/Users/melki/dev/tools/agent-hub.ps1)
- **Preferências e Memória Canônica**: [Preferências de Trabalho com Agentes.md](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md)
- **Regra Global (`always_on`)**: [diretrizes-qualidade-eficiencia.md](file:///C:/Users/melki/.gemini/config/rules/diretrizes-qualidade-eficiencia.md) (1. Qualidade e Tipagem Estrita <= 300 linhas; 2. Eficiência, Zero Preâmbulo e Portões HITL; 3. Flexibilidade Anti-Engessamento; 4. Self-Refine Silencioso; 5. Proatividade com 1 Próximo Passo Concreto; 6. Minimalist Impact `DESIGN.md v4.5-soft` — Luz 135°, `Cerulean Sapphire #0284C7`, Zero Cobalto/Glassmorphism).
- **Orquestração Interativa de Agentes (5 Camadas)**:
  1. **Bússola & Heartbeat (`0 tokens`)**: `franklin_smart_compass(intent_or_path)` | `pwsh C:\Users\melki\dev\tools\agent-hub.ps1` | `POST /rpc` (`mesh/heartbeat`).
  2. **Execução Direta vs. Loop Fechado**: Precedência `<user_rules>` **>** `franklin-skills` **>** `superpowers` (entrega direta sem entrevista em baixo risco; `LoopPlanner` Fase 0 + `gap-analyzer-auditor` em missões críticas).
  3. **Esquadrão Frontend (`FrontCraftMaster` + Topologia `3+1`)**: `invoke_subagent` (`ui-shell-navigator` -> `ui-controls-data` + `ui-motion-interaction` -> `ui-deterministic-observer`) ou `franklin_execute_dag("ui")`.
  4. **Gatekeepers Determinísticos**: `code-acceptability-auditor` (AST Python >= 75), `test-quality-auditor`, `franklin_execute_dag("physics")` (`Snorm >= 80`) e `dispatch_skill_deterministic_tests` (Go Pass@k).
  5. **Malha Multiagente Cloud/Web & Clínica**: `adk-tests` (Watchdog SRE + A2A `:8080`), `epic-volta` (DAG Kahn + `MCPBridgeAgent`), `mcp-web-agents` (Gateway 4+1) e `PCM`/`scoreboard` (`prescmed-clinical-reviewer`).
