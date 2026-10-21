# Franklin Quebra-Galho 🛠️

> **Agente Principal & Laboratório de Automação Diária e Engenharia de Skills**

O **Franklin Quebra-Galho** (`franklin-quebragalho`) é o assistente principal de produtividade pessoal do desenvolvedor (Melki). Ele atua como orquestrador multitarefa para o dia a dia e como incubadora de desenvolvimento, homologação e evolução de **Skills personalizadas** do Google Antigravity sob os padrões consolidados de 2026.

---

## 🎯 Missões Principais

1. **Organização do Google Drive (`DriveMaster`)**:
   - Gestão e higienização estruturada da unidade montada `G:\Meu Drive` (`gdrive-auditoria-limpeza` e `gdrive-taxonomia-organizacao`).
   - Integração com MCP Server `google-drive` para pesquisas semânticas, metadados e manipulação segura de arquivos.
   - Rotinas de triagem, categorização, quarentena e renomeação padronizada.

2. **Organização de Pastas Locais e PKM (`FileOpsLocal` & `VaultMaster`)**:
   - Manutenção preventiva de diretórios de alto fluxo (`Downloads`, `Área de Trabalho`) via `manutencao-disco-windows`.
   - Gestão da pasta raiz de desenvolvimento (`C:\Users\melki\dev\`: `repos\`, `sandbox\`, `tools\`, `notes\`).
   - Curadoria e organização de notas no **Obsidian Vault** (`C:\Users\melki\dev\notes\`) via `curadoria-obsidian-vault`.

3. **Geração e Conversão de Documentos (`DocMaker`)**:
   - Redação de relatórios, documentações e anotações ricas em Markdown compatíveis com Obsidian (`redator-tecnico-markdown`).
   - Conversão automatizada de arquivos `.md` e `.html` para PDF profissional via Edge/Chrome headless (`conversor-html-pdf` e `scripts/md-to-pdf.ps1`).

4. **Laboratório e Incubadora de Skills (`SkillCraft` - Padrão 2026)**:
   - Desenvolvimento de automações modulares orientadas por **divulgação progressiva** (3 Tiers).
   - Governança anti-alucinação: proibição de validações vazias e auditorias inventadas.
   - Verificação determinística baseada em regras de corte falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).
   - Testes empíricos com casos reais em `evals/evals.json`.

---

## 📦 Catálogo Rápido de Skills (29 Skills Canônicas)

| Skill | Versão | Status | Propósito Principal | Link |
| :--- | :---: | :---: | :--- | :--- |
| **`organizador-projetos-ideias`** | `v1.0.0` | 🚀 Produção | Organizador de ideias do zero (`ideation_to_v1` + fallback *"não sei"* -> `v1.0`) e sincronizador completo de projetos (`project_organizer_sync`: `README.md` fiel ao disco, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `DESIGN.md`, contratos `MCP`/`FastAPI`/`RPC`, Mermaid e limpeza da raiz). | [skills/organizador-projetos-ideias/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-projetos-ideias/SKILL.md) |
| **`antigravity-project-auditor`** | `v2.0.0` | 🚀 Produção | Auditor arquitetural, diagnóstico de MVP (causa-efeito) e planejamento em 3 fases (`autonomous_scan` \| `targeted_focus`). | [skills/antigravity-project-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/antigravity-project-auditor/SKILL.md) |
| **`minimal-impact-ui`** | `v1.0.0` | 🚀 Produção | Design System Anti-TDAH (`atlas_ex_umbris_winui.html`): 3 temas (`#57545d` + `#8e8999`, `#09090B`, `#F3F3F5`), 6 Arquétipos e 28 efeitos WinUI 3. | [skills/minimal-impact-ui/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/minimal-impact-ui/SKILL.md) |
| **`code-acceptability-auditor`** | `v1.1.0` | 🚀 Produção | Portão 1 AST/Pydantic de código Python (`12` regras: `SEC001..003`, `SYN001`, `ERR001..003`, `TYP001..002`, `ARCH001..003`), Quality Gate (`>=75/100`) e Trigger Matrix ($F_1=1.0$). | [skills/code-acceptability-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-acceptability-auditor/SKILL.md) |
| **`design-md`** | `v5.0.0` | 🚀 Produção | Gerador de contratos `DESIGN.md` (`v5.0`) orientado ao propósito do projeto (`preferencias_estilo_e_temas.md`). | [skills/design-md/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/design-md/SKILL.md) |
| **`frontend-code-architect`** | `v5.0.0` | 🚀 Produção | Arquiteto de código Frontend em Atomic Design (5 camadas), `<SurfaceCard />` esculpido e tokens por objetivo. | [skills/frontend-code-architect/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-code-architect/SKILL.md) |
| **`frontend-testing-auditor`** | `v3.0.0` | 🚀 Produção | Auditor determinístico de testes e arquitetura visual Frontend: FSM 4 estados, WCAG 2.1 AA/AAA e `AUDIT-VIS-01`. | [skills/frontend-testing-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-testing-auditor/SKILL.md) |
| **`test-quality-auditor`** | `v1.2.0` | 🚀 Produção | Portão 2 modular em 5 domínios (Python, TS/JS, Go, MCP e Harness) + estatística `perfkit_stats.py` e evals espelhados 1:1. | [skills/test-quality-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/test-quality-auditor/SKILL.md) |
| **`code-quality-audit-3d-physics`** | `v1.0.0` | 🚀 Produção | Auditoria de código e Física 3D em 3 ondas (5 subskills, Pass@10 e observador $S_{\text{norm}}$). | [skills/code-quality-audit-3d-physics/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/SKILL.md) |
| **`evoluir-skills`** | `v2.2.0` | 🚀 Produção | Orquestrador mestre da esteira SkillCraft em 3 passos, 3 Tiers e Trigger Matrix. | [skills/evoluir-skills/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/evoluir-skills/SKILL.md) |
| **`aprimoramento-expansibilidade-agentes-skills`** | `v2.2.0` | 🚀 Produção | Consultora de arquitetura agêntica, métricas Pass@k, FNR, Snorm, GEPA e maturidade Níveis 1-4. | [skills/aprimoramento-expansibilidade-agentes-skills/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/aprimoramento-expansibilidade-agentes-skills/SKILL.md) |
| **`skill-auditor-refatorador-skills`** | `v2.3.0` | 🚀 Produção | Auditoria estática (Estágio 3 SkillCraft), 5 Eixos Transversais, 7 Módulos (`M1..M7`) e Trigger Matrix. | [skills/skill-auditor-refatorador-skills/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/skill-auditor-refatorador-skills/SKILL.md) |
| **`auditoria-projetos-sistema`** | `v3.0.0` | 🚀 Produção | Auditoria estrutural (`AGENTS.md`, tipagem Pydantic), diagnóstico do propósito do projeto, encaixe de tema e `agent-browser`. | [skills/auditoria-projetos-sistema/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/auditoria-projetos-sistema/SKILL.md) |
| **`arquiteto-conteudo-solucoes`** | `v2.4.0` | 🚀 Produção | Geração técnica sob 4 modos (A, B, C, D), prompts enterprise, código tipado e roadmaps. | [skills/arquiteto-conteudo-solucoes/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/arquiteto-conteudo-solucoes/SKILL.md) |
| **`organizador-fluxo-arvore-arquivos`** | `v1.2.0` | 🚀 Produção | Converte ideias brutas em diagramas Mermaid, árvores ASCII e planos com exportação MD/PDF. | [skills/organizador-fluxo-arvore-arquivos/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-fluxo-arvore-arquivos/SKILL.md) |
| **`arquitetura-design-implementacao-sistema`** | `v3.0.0` | 🚀 Produção | Diagnóstico de propósito e MVP, Ilhas Funcionais, tipografia `clamp()` + `tabular-nums` e motor determinístico `SGA`. | [skills/arquitetura-design-implementacao-sistema/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/arquitetura-design-implementacao-sistema/SKILL.md) |
| **`design-interface-medica-minimalista`** | `v3.0.0` | 🚀 Produção | Arquitetura visual clínica/hospitalar por ambiente (Ambulatório, Enfermaria `#57545d`, UTI `Ex Umbris` + `IBM Plex`) e A4. | [skills/design-interface-medica-minimalista/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/design-interface-medica-minimalista/SKILL.md) |
| **`context-sentinel`** | `v1.1.0` | 🚀 Produção | Auditoria de contexto em conversas multi-turn, mitigação de context rot e snapshots determinísticos. | [skills/context-sentinel/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/context-sentinel/SKILL.md) |
| **`skill-orquestrador-planos-encadeados`** | `v2.0.0` | 🚀 Produção | Orquestração executiva de planos com portão de qualidade de arquitetura visual por propósito e matriz de discrepâncias. | [skills/skill-orquestrador-planos-encadeados/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/skill-orquestrador-planos-encadeados/SKILL.md) |
| **`high-level-context-planner`** | `v2.1.0` | 🚀 Produção | Planejador estratégico em malha fechada, Fase 0 obrigatória, tasks paralelizáveis e convergência *append-only*. | [skills/high-level-context-planner/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/high-level-context-planner/SKILL.md) |
| **`gap-analyzer-auditor`** | `v2.1.0` | 🚀 Produção | Portão 3 de RCA em 4 vetores, segregação `[FATO]`/`[INFERÊNCIA]`/`[LACUNA]`, convergência `/speckit-converge` e hand-off YAML. | [skills/gap-analyzer-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gap-analyzer-auditor/SKILL.md) |
| **`refine-prompt`** | `v3.2.0` | 🚀 Produção | Expansão cognitiva, auditoria de factibilidade e refinamento de prompts e ideias sob Zero-Trust. | [skills/refine-prompt/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/refine-prompt/SKILL.md) |
| **`gdrive-auditoria-limpeza`** | `v1.0.0` | 🚀 Produção | Varredura de arquivos pesados (>100MB), duplicados SHA-256 e quarentena segura no Google Drive. | [skills/gdrive-auditoria-limpeza/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-auditoria-limpeza/SKILL.md) |
| **`gdrive-taxonomia-organizacao`** | `v1.1.0` | 🚀 Produção | Estrutura canônica numerada real do Drive, datas ISO (`YYYY-MM-DD`) e triagem documental. | [skills/gdrive-taxonomia-organizacao/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-taxonomia-organizacao/SKILL.md) |
| **`manutencao-disco-windows`** | `v1.1.0` | 🚀 Produção | Triagem de Downloads, Desktop e organização de `C:\Users\melki\dev\` com dry-run. | [skills/manutencao-disco-windows/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/manutencao-disco-windows/SKILL.md) |
| **`curadoria-obsidian-vault`** | `v1.1.0` | 🚀 Produção | Curadoria do cofre Obsidian (`C:\Users\melki\dev\notes\`), YAML, `[[Wikilinks]]` e anexos órfãos. | [skills/curadoria-obsidian-vault/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/curadoria-obsidian-vault/SKILL.md) |
| **`redator-tecnico-markdown`** | `v1.2.0` | 🚀 Produção | Redação técnica de relatórios, notas técnicas e atas em Markdown compatíveis com Obsidian. | [skills/redator-tecnico-markdown/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/redator-tecnico-markdown/SKILL.md) |
| **`conversor-html-pdf`** | `v1.0.0` | 🚀 Produção | Conversão determinística de Markdown/HTML para PDF profissional via Edge headless. | [skills/conversor-html-pdf/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/conversor-html-pdf/SKILL.md) |
| **`_template`** | `v3.0.0` | 🚀 Produção | Molde canônico oficial com `preferencias_estilo_e_temas.md`, 7 Módulos (`M1..M7`), `rules/`, `evals/`, `references/`. | [skills/_template/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/_template/SKILL.md) |

---

## 📁 Estrutura do Workspace

```text
franklin-quebragalho/
├── agents/                                      # 7 Subagentes Declarativos (Topologia 3+1 de UI + Memória + Mediação HITL/RAW)
├── plans/                                       # 3 Planos DAG (ui_composition_dag.json, physics_code_audit_dag.json, distributed_agent_mediation_dag.json)
├── shared/                                      # Pacote interno autônomo de domínio (A2A, Catálogo, Bússola, Orquestrador e Harness)
│   ├── a2a_bridge.py                            # Motor Agent2Agent v1.0 (AgentCard Protobuf, assinatura JCS/JWS e TaskManager)
│   ├── catalog_service.py                       # Descoberta, busca ranqueada, leitura progressiva e validação de skills
│   ├── compass_topology.py                      # Smart Compass, Topologia Multi-Repo (5 camadas) e Subagentes
│   ├── execution_orchestrator.py                # Executor isolado de scripts, motor DAG Kahn e despacho A2A/Harness²
│   ├── harness.py                               # SemanticGuard, evaluate_action_risk e CheckpointStore HITL
│   ├── harness2_engine.py                       # Motor recursivo Harness² e avaliação de mutações
│   ├── harness2_tree.py                         # Árvore editável c1..c8 e validador Answer-Free
│   ├── mcp_2026_advisor.py                      # Consultor arquitetural MCP Spec 2026-07-28 e manifesto .mcpb v0.4
│   └── tools/
│       └── frontmatter_parser.py                # Parser de YAML Frontmatter com fallback determinístico
├── google-drive-index-app/                      # Aplicação local de indexação e testes do Google Drive
├── server.py                                    # Servidor FastMCP Global (Franklin Skills MCP — 13 Ferramentas)
├── pyproject.toml                               # Configuração de dependências uv/hatchling e pytest
├── .env.example                                 # Exemplo de variáveis de ambiente (assinatura HMAC A2A v1.0)
├── .venv/                                       # Ambiente virtual Python isolado
├── skills/                                      # Catálogo canônico de 29 skills em 3 Tiers
├── scripts/                                     # Scripts utilitários de suporte (PowerShell / Python)
│   ├── validate_skills.py                       # Validador determinístico de conformidade (--targets)
│   ├── sync_gemini_ecosystem.py                 # Sincronizador 1:1 (skills, agents, plans, lib, doc e plugin global)
│   ├── standardize_skills_metadata.py           # Utilitário de padronização de frontmatter YAML
│   └── md-to-pdf.ps1                            # Conversor de Markdown para PDF via Chrome/Edge headless
├── tests/                                       # Suíte de testes automatizados Nível 4 (pytest — 52 testes em 5 arquivos)
│   ├── test_server.py                           # Testes determinísticos do servidor MCP, DAG, Bússola e Paridade Documental
│   ├── test_a2a_protocol.py                     # Testes de assinatura JCS/JWS, Protobuf AgentCard e Zero-Trust A2A v1.0
│   ├── test_harness_quality.py                  # Testes de SemanticGuard, RiskMatrix, CheckpointStore e Harness²
│   ├── test_perfkit_stats.py                    # Testes estatísticos de Pass@k, Welch t-test e Cohen's d
│   └── test_quality_auditor_go_mcp.py           # Testes de regressão dos auditores AST Go (*_test.go) e MCP JSON-RPC 2.0
├── GEMINI.md                                    # Regras de comportamento e integridade do workspace
├── AGENTS.md                                    # Arquitetura e contratos de orquestração de subagentes
├── MY_AGENTS.md                                 # Catálogo detalhado das personas e papéis dos agentes
├── MY_SKILLS.md                                 # Manifesto, ciclo de vida e changelog oficial das 29 skills
├── CONTEXT.md                                   # Resumo executivo de contexto operacional do repositório
├── SPEC.md                                      # Especificação técnica de módulos e ferramentas MCP
└── README.md                                    # Este documento
```

---

## 🌐 Servidor MCP Global: Franklin Skills MCP

O ecossistema conta com um servidor MCP dedicado baseado em **FastMCP** integrado globalmente ao Antigravity (`~/.gemini/config/mcp_config.json`):

### Ferramentas Expostas (13 Tools)
- **`franklin_skills_list`**: Lista o catálogo de skills com filtros por status (`validada`, `producao`), persona (`FrontCraftMaster`, `DriveMaster`, etc.) e busca textual.
- **`franklin_skills_get`**: Recupera a skill de forma granular (`contract`, `rules`, `references`, `evals`, `scripts`, `all`) preservando o *Token Budget*.
- **`franklin_skills_search`**: Busca inteligente por intenção operacional, pontuação de relevância e recomendação do subagente especialista.
- **`franklin_skills_validate`**: Executa a auditoria determinística estrutural de todas as 29 skills com relatório `[PASS]`/`[FAIL]`.
- **`franklin_get_agents`**: Retorna a matriz operacional dos subagentes especialistas (incluindo a Topologia 3+1 de UI).
- **`franklin_smart_compass`**: Roteador cognitivo que recomenda a skill ideal para uma intenção livre.
- **`franklin_run_skill_script`**: Executa scripts utilitários com trava contra Path Traversal, SemanticGuard e isolamento de processo.
- **`franklin_execute_dag`**: Executa planos de orquestração em grafo acíclico dirigido (DAG) via motor do Epic-Volta (`C:\Users\melki\dev\repos\epic-volta`).
- **`franklin_harness_guard`**: Valida comandos e caminhos antes da execução com base no protocolo Zero-Trust.
- **`franklin_harness_checkpoint`**: Gerencia checkpoints transacionais HITL (`.sessions/harness_checkpoints.json`) e sub-ações recursivas Harness² (`validate_tree`, `evolve`, `record_experience`).
- **`franklin_a2a_agent_card`**: Gera e verifica criptograficamente o `AgentCard` A2A v1.0 do Franklin.
- **`franklin_a2a_dispatch_task`**: Despacha tarefas A2A v1.0 com proteção Zero-Trust e HITL.
- **`franklin_mcp_build_advisor`**: Consultor arquitetural MCP Spec `2026-07-28`.

---

## ⚡ Comandos e Referências Rápidas

- **Executar Servidor MCP Localmente**: `uv run python server.py`
- **Executar Suíte Completa de Testes (`52/52`)**: `uv run pytest -q`
- **Auditar Todas as Skills**: `uv run python scripts/validate_skills.py`
- **Sincronizar Catálogo e Plugin Global**: `uv run python scripts/sync_gemini_ecosystem.py`
- **Visualizar Agentes Próprios**: Consulte [MY_AGENTS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_AGENTS.md)
- **Consultar Catálogo de Skills e Versões**: Consulte [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md)
- **Regras Operacionais e Anti-Alucinação**: Consulte [GEMINI.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/GEMINI.md)
- **Contratos de Subagentes**: Consulte [AGENTS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/AGENTS.md)
