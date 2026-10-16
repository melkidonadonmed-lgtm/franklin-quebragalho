# Minhas Skills (MY SKILLS)

> **Manifesto, Catálogo de Ciclo de Vida e Histórico de Versões de Skills**

Este repositório é a incubadora central de skills do **Franklin Quebra-Galho**. Cada skill encapsula um procedimento, automação ou runbook especializado que o agente pode carregar sob demanda (*progressive disclosure*).

---

## 🚦 Tabela de Ciclo de Vida das Skills

| Ícone | Status | Descrição |
| :---: | :--- | :--- |
| 💡 | **Ideia** | Rascunho de conceito ou necessidade levantada no dia a dia. |
| 🧪 | **Em Teste** | Implementada em `.agents/skills/<nome>/`, passando por cenários de teste reais. |
| ✅ | **Validada** | Fluxo testado com sucesso, documentação completa e tratamento de erros ok. |
| 🚀 | **Produção** | Skill consolidada, estável e ativada rotineiramente pelo orquestrador. |

---

## 📦 Catálogo de Skills do Workspace (25 Skills Canônicas)

| Skill | Versão | Status | Descrição Curta | Localização |
| :--- | :---: | :---: | :--- | :--- |
| **`test-quality-auditor`** | `v1.2.0` | 🚀 Produção | Auditor modular (`<300` linhas/módulo) em 5 domínios (Python, TS/JS, Go `*_test.go`, MCP `JSON-RPC 2.0` e Harness HITL/Evals) com espelhamento 1:1 em `evals/modules/*_evals.json`. | [.agents/skills/test-quality-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/test-quality-auditor/SKILL.md) |
| **`code-quality-audit-3d-physics`** | `v1.0.0` | 🚀 Produção | Auditoria de código e Física 3D em 3 ondas (5 subskills: sanitização AST Py/JS, hardcoded, 5 sub-dimensões de física, testes Pass@10 e observador $S_{\text{norm}}$). | [.agents/skills/code-quality-audit-3d-physics/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/code-quality-audit-3d-physics/SKILL.md) |
| **`organizador-fluxo-arvore-arquivos`** | `v1.1.0` | ✅ Validada | Converte ideias brutas em diagramas Mermaid, árvores de arquivos e planos de execução, com exportação direta em MD ou PDF. | [.agents/skills/organizador-fluxo-arvore-arquivos/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/organizador-fluxo-arvore-arquivos/SKILL.md) |
| **`arquiteto-conteudo-solucoes`** | `v2.2.0` | ✅ Validada | Arquiteto autônomo para engenharia de prompts, planos estruturados, roadmaps, código tipado e skills modulares anti-alucinação. | [.agents/skills/arquiteto-conteudo-solucoes/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/arquiteto-conteudo-solucoes/SKILL.md) |
| **`evoluir-skills`** | `v2.0.0` | 🚀 Produção | Orquestrador mestre do ciclo de vida (4 estágios: `expansao-contexto-adaptativa` ➔ `aprimoramento` ➔ `skill-creator` ➔ `auditor`), 3 Tiers e Trigger Matrix. | [.agents/skills/evoluir-skills/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/evoluir-skills/SKILL.md) |
| **`aprimoramento-expansibilidade-agentes-skills`** | `v2.0.0` | 🚀 Produção | Consultora de arquitetura agêntica (3 Tiers, Envelope Pattern, Context Forking, Memória 3 Camadas, MCP/A2A, Pass@k, FNR<0.001, Snorm, GEPA e Níveis 1-4). | [.agents/skills/aprimoramento-expansibilidade-agentes-skills/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/aprimoramento-expansibilidade-agentes-skills/SKILL.md) |
| **`arquitetura-design-implementacao-sistema`** | `v2.0.0` | 🚀 Produção | Diagnóstico severo de MVP, navegabilidade comentada, aglomeração por Ilhas Funcionais (Island UI/UX), tipografia linear `clamp()`, auditoria zero-hardcode, motor `SGA` determinístico (`deterministic_scorer.py`) e relatório HTML V1 vs V2 com metadados. | [.agents/skills/arquitetura-design-implementacao-sistema/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/arquitetura-design-implementacao-sistema/SKILL.md) |
| **`auditoria-projetos-sistema`** | `v2.2.0` | 🚀 Produção | Auditoria estrutural (`AGENTS.md`, desacoplamento, tipagem Pydantic, chunking semântico), coerência UI/UX e esteira `agent-browser` por aba/menu. | [.agents/skills/auditoria-projetos-sistema/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/auditoria-projetos-sistema/SKILL.md) |
| **`context-sentinel`** | `v1.0.0` | ✅ Validada | Auditoria de integridade da janela de contexto, mitigação de context rot e snapshots determinísticos estruturados. | [.agents/skills/context-sentinel/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/context-sentinel/SKILL.md) |
| **`design-interface-medica-minimalista`** | `v1.0.0` | ✅ Validada | Padrão executivo de UI/UX para aplicações médicas, prontuários, calculadoras clínicas e SaaS de saúde. | [.agents/skills/design-interface-medica-minimalista/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/design-interface-medica-minimalista/SKILL.md) |
| **`skill-auditor-refatorador-skills`** | `v1.3.0` | 🚀 Produção | Auditor estático (Estágio 4 SkillCraft): desacoplamento de monólitos, validação dos 3 Tiers, Trigger Matrix e Motor Tátil `v2.6.0-2026`. | [.agents/skills/skill-auditor-refatorador-skills/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/skill-auditor-refatorador-skills/SKILL.md) |
| **`skill-orquestrador-planos-encadeados`** | `v1.1.0` | ✅ Validada | Orquestrador de planos multifásicos com portão de qualidade de design tátil, paleta mineral e matriz de discrepâncias. | [.agents/skills/skill-orquestrador-planos-encadeados/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/skill-orquestrador-planos-encadeados/SKILL.md) |
| **`consultor-design-tatil-frontend`** | `v1.3.0` | 🚀 Produção | Mapeamento de frontend com `agent-browser`, orquestração dos 4 subagentes de UI (`Topologia 3+1`), consultoria tátil multidimensional (22 temas) e gerador de `DESIGN.md`. | [.agents/skills/consultor-design-tatil-frontend/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/consultor-design-tatil-frontend/SKILL.md) |
| **`refine-prompt`** | `v3.0.0` | ✅ Validada | Expansão cognitiva, auditoria de factibilidade e refinamento de prompts e ideias sob Zero-Trust, 3 módulos de saída e âncora 2026. | [.agents/skills/refine-prompt/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/refine-prompt/SKILL.md) |
| **`gap-analyzer-auditor`** | `v2.0.0` | ✅ Validada | Auditor técnico e analista de brechas em malha fechada (closed-loop), RCA em 4 vetores e hand-off estruturado para o planejador. | [.agents/skills/gap-analyzer-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/gap-analyzer-auditor/SKILL.md) |
| **`high-level-context-planner`** | `v2.0.0` | 🚀 Produção | Arquiteto estratégico e planejador de contexto em malha fechada, Fase 0 obrigatória, critérios Go/No-Go e replanning v2.0. | [.agents/skills/high-level-context-planner/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/high-level-context-planner/SKILL.md) |
| **`analise-design-tatil-frontend`** | `v1.2.0` | 🚀 Produção | Diagnóstico estrutural e visual de frontend, orquestração dos 4 subagentes de UI (`Topologia 3+1`), motor multidimensional 2026 (22 temas, 4 presets tipográficos, 5 geometrias) e Relatório Comparativo. | [.agents/skills/analise-design-tatil-frontend/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/analise-design-tatil-frontend/SKILL.md) |
| **`refatoracao-design-tatil-frontend`** | `v1.3.0` | 🚀 Produção | Refatoração de frontend por framework modular em 3 ondas (`Topologia 3+1`), injeção de 22 temas multidimensionais, física 3D, botões ergonômicos e relevo tátil. | [.agents/skills/refatoracao-design-tatil-frontend/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/refatoracao-design-tatil-frontend/SKILL.md) |
| **`gdrive-auditoria-limpeza`** | `v1.0.0` | ✅ Validada | Varredura de arquivos pesados (>100MB), identificação de duplicados por hash SHA-256 e quarentena segura no Google Drive. | [.agents/skills/gdrive-auditoria-limpeza/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/gdrive-auditoria-limpeza/SKILL.md) |
| **`gdrive-taxonomia-organizacao`** | `v1.1.0` | ✅ Validada | Estrutura canônica numerada real do Drive, padronização de nomenclatura com datas ISO (YYYY-MM-DD) e triagem documental. | [.agents/skills/gdrive-taxonomia-organizacao/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/gdrive-taxonomia-organizacao/SKILL.md) |
| **`manutencao-disco-windows`** | `v1.1.0` | ✅ Validada | Manutenção do SO Windows 11: triagem de Downloads, Desktop, isolamento de instaladores e arquivamento em `dev\` (`repos`, `sandbox`, `tools`, `notes`). | [.agents/skills/manutencao-disco-windows/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/manutencao-disco-windows/SKILL.md) |
| **`curadoria-obsidian-vault`** | `v1.1.0` | ✅ Validada | Curadoria do cofre Obsidian (`C:\Users\melki\dev\notes\`): validação de frontmatter YAML, `[[Wikilinks]]` e anexos órfãos. | [.agents/skills/curadoria-obsidian-vault/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/curadoria-obsidian-vault/SKILL.md) |
| **`redator-tecnico-markdown`** | `v1.2.0` | ✅ Validada | Redação técnica de relatórios executivos, notas técnicas e documentações compatíveis com `C:\Users\melki\dev\notes\Inbox\`. | [.agents/skills/redator-tecnico-markdown/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/redator-tecnico-markdown/SKILL.md) |
| **`conversor-html-pdf`** | `v1.0.0` | ✅ Validada | Conversão determinística de Markdown/HTML para PDF profissional via Edge headless com CSS de impressão calibrado. | [.agents/skills/conversor-html-pdf/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/conversor-html-pdf/SKILL.md) |
| **`_template`** | `v1.3.0` | 🚀 Produção | Modelo base oficial padrão 2026 com os 4 módulos canônicos de paleta mineral, design tátil e matriz de discrepâncias. | [.agents/skills/_template/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.agents/skills/_template/SKILL.md) |

---

## 📜 Histórico de Versões e Contexto (Changelog)

### [2026-10-16] - Fase 13: Integração da Topologia 3+1 de Subagentes de UI (`agents/ui-*.md`), Orquestração Assíncrona (`franklin_execute_dag`) e Sincronização Global `.gemini`
- **Acoplamento da Topologia 3+1 nas Skills de Frontend (`analise-design-tatil-frontend` `v1.2.0`, `consultor-design-tatil-frontend` `v1.3.0`, `refatoracao-design-tatil-frontend` `v1.3.0`)**:
  - Formalização dos 4 subagentes de UI sob `FrontCraftMaster`: `ui-shell-navigator` (Onda 1 — Módulos 1 e 2), `ui-controls-data` (Onda 2A — Módulos 3 e 4), `ui-motion-interaction` (Onda 2B — Módulos 5.1 e 5.2) e `ui-deterministic-observer` (Onda 3 Gatekeeper — Módulos 5.3 e 6).
  - Padronização de frontmatter YAML em `agents/ui-*.md` compatível com `agent_spec_loader.py` (validação determinística de delimitadores `---`) e catálogo MCP `franklin_get_agents(agent_name="ui")`.
- **Execução Assíncrona Concorrente e Sincronização do Ecossistema `.gemini`**:
  - Integração de `franklin_execute_dag` (`server.py` $\leftrightarrow$ `epic-volta`) com `asyncio.create_subprocess_exec`, `SQLiteStateManager` em modo WAL sem vazamento de descritores e `scripts/sync_gemini_ecosystem.py` sincronizando `lib/`, `doc/`, `docs/`, `plugins/`, `agents/` e `plans/`.

### [2026-10-15] - Fase 12: Evolução da Skill `arquitetura-design-implementacao-sistema` (`v2.0.0`) — Aglomeração por Ilhas Funcionais, Desacoplamento de Cores, Motor Determinístico `SGA` (`deterministic_scorer.py`) e Resolução `V1 vs V2` em HTML
- **Refatoração Arquitetural em 5 Módulos Funcionais Independentes de Cor (`SKILL.md` `v2.0.0`)**:
  - Remoção da poluição cosmética de paletas cromáticas do contrato de arquitetura (delegadas ao `DESIGN.md`), focando em: **(1) Navegabilidade, Grafo Comentado e 4 Estados de UI** (`INE` 25%), **(2) Aglomeração Funcional por Ilha e Isolamento Data/Render** (`ICI` 20%), **(3) Crítica Severa de MVP Anti-Bloat** (`IRM` 15%), **(4) Pureza de Código, SRP e Zero Hardcode** (`IPC` 25%) e **(5) Tipografia Linear Combinada** (`clamp()`, `65ch`, `tabular-nums`, `anti-squish` e `Ctrl+K` sem `alert()`) (`ICTE` 15%).
- **Motor Determinístico Zero-Placebo e Scanner AST/Regex (`modules/deterministic_scorer.py` & `scripts/deterministic_scorer.py`)**:
  - Implementação das 5 equações lineares exatas para cálculo do **Score Global de Arquitetura (`SGA`)**, acompanhado de scanner automático de árvore de arquivos (`.py`, `.ts`, `.tsx`, `.js`, `.html`, `.css`) via `--scan`, `--scan-v1`/`--scan-v2`, `--self-test` e gerador de relatório `--html-out`.
- **Modo de Resolução Auditável (`templates/resolution_diff_v1_v2.html`) + Governança (`rules/` & `evals/`)**:
  - Template HTML5 autocontido com `<meta>` tags de rastreabilidade (`score-v1-baseline`, `score-v2-resolved`, `score-delta`, `audit-timestamp`) e grafo Mermaid com semântica exclusiva de diff (`Vermelho` = removido da V1, `Amarelo` = refatorado, `Verde` = nova ilha V2), além da criação de `rules/criterios_auditoria.md` e `evals/evals.json` (4 cenários com *Trigger Matrix*).

### [2026-10-15] - Fase 11: Evolução da Skill `test-quality-auditor` (`v1.2.0`) — Módulo de Qualidade de Testes de Harness (`harness_test_auditor.py`) e Arquitetura de Evals Espelhados (`evals/modules/*_evals.json`)
- **Módulo de Testes de Harness (`scripts/harness_test_auditor.py` + `references/modulo_qualidade_testes_harness.md`)**:
  - Auditoria determinística de suítes de testes para **Harnesses de Governança (Zero-Trust / HITL)** (`SemanticGuard.sanitize_input`, `SecurityViolationError`, `evaluate_action_risk`, `CheckpointStore`) e **Eval-Driven Harness** (`run_eval_harness`), detectando `HARNESS_WEAK_INJECTION_GUARD_TEST`, `HARNESS_UNVERIFIED_RISK_TRANSITION`, `HARNESS_MISSING_TEARDOWN_CLEANUP`, `HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE` e `HARNESS_EVAL_MISSING_EVIDENCE_OR_DELTA`.
- **Espelhamento 1:1 de Evals (`scripts/*_auditor.py` $\leftrightarrow$ `evals/modules/*_evals.json`)**:
  - Criação dos 5 arquivos modulares espelhados (`python_evals.json`, `ts_js_evals.json`, `go_evals.json`, `mcp_evals.json`, `harness_evals.json`) gerando relatórios individuais em `evals/workspace/iteration-1/modules/<mod>_grading.json` e `<mod>_benchmark.json`, além do manifesto consolidado `evals/evals.json` com `20/20 PASS` (`100%`) e da suíte real `tests/test_harness_quality.py`.

### [2026-10-15] - Fase 10: Evolução da Skill `test-quality-auditor` (`v1.1.0`) — Módulos de Qualidade de Testes em Go (`*_test.go`) e MCP (`JSON-RPC 2.0` / `FastMCP`)
- **Desacoplamento Modular em 7 Componentes (`<300` linhas cada em `scripts/`)**:
  - `models.py`, `python_ast_auditor.py`, `ts_js_auditor.py`, `go_test_auditor.py`, `mcp_test_auditor.py`, `eval_harness.py` e `test_quality_auditor.py`.
- **Módulo Go (`go_test_auditor.py` + `references/modulo_qualidade_testes_go.md`)**:
  - Inspeção determinística de funções `func Test*(t *testing.T)` (incluindo *Table-Driven Tests*, goroutines e Google ADK Go v2), detectando `EMPTY_TEST_BODY`, `MISSING_ASSERTIONS`, `TAUTOLOGICAL_ASSERT`, `SILENCED_ERROR_IN_TEST` (`res, _ := sut()` e `if err != nil` sem `t.Fatal`/`t.Error`), `WEAK_NIL_ONLY_ASSERT`, `UNSAFE_GOROUTINE_FATAL` (`t.Fatalf` em goroutine filha), `GLOBAL_STATE_LEAKAGE` (`os.Setenv` sem `t.Setenv`/`t.Cleanup`) e `NON_DETERMINISTIC_TIME` (distinguindo sincronismo legítimo com `sync/atomic` / `Debouncer`).
- **Módulo MCP (`mcp_test_auditor.py` + `references/modulo_qualidade_testes_mcp.md`)**:
  - Auditoria de protocolo Model Context Protocol (JSON-RPC 2.0 `stdio`, FastMCP Python e Go `StdioServer`), detectando `MCP_INCOMPLETE_STDIO_HANDSHAKE` (`tools/call` sem `initialize` ou `notifications/initialized` com `id`), `MCP_TAUTOLOGICAL_RAW_RESPONSE` (tools JSON sem `json.loads`/`json.Unmarshal`), `MCP_WEAK_TOOLS_LIST_DISCOVERY`, `MCP_UNVERIFIED_ERROR_CODE_CONTRACT` (`-32601`) e `MCP_WEAK_SECURITY_GUARD_ASSERT` (Path Traversal / Prompt Injection sem checar `BLOCKED`).
- **Expansão do Eval-Driven Harness (`evals/evals.json`)**:
  - Ampliado de 8 para **15 casos de avaliação** multi-domínio (`6 python`, `3 go`, `3 mcp`, `3 near-miss`) com `15/15 PASS` (`pass_rate: 1.0`) em `grading.json` e `benchmark.json`, além da nova suíte de regressão `tests/test_quality_auditor_go_mcp.py`.

### [2026-10-15] - Fase 9: Implantação da Skill `test-quality-auditor` (`v1.0.0`) e Saneamento da Suíte de Testes do Franklin
- **Engenharia do Auditor de Qualidade de Testes e Esteira de Evals (`test-quality-auditor` `v1.0.0`)**:
  - Implementação de `scripts/test_quality_auditor.py` com analisador estático AST para Python (`TestQualityASTVisitor`) e parser estrutural para TypeScript/JavaScript (`audit_ts_js_test_file`), cobrindo `EMPTY_TEST_BODY`, `MISSING_ASSERTIONS`, `TAUTOLOGICAL_ASSERT`, `WEAK_IS_NOT_NONE_ASSERT`, `WEAK_SURFACE_ASSERT`, `NON_DETERMINISTIC_TIME`, `SILENCED_EXCEPTION_IN_TEST`, `GLOBAL_STATE_LEAKAGE` e `BRITTLE_CATALOG_COUNT`.
  - Classificação automática no **Espectro de Qualidade (Níveis 1 a 4)** e motor *Eval-Driven Harness* (`--run-evals`) que processa `evals/evals.json` (8 casos incluindo *Trigger Matrix* com *Near-Misses*) e emite `grading.json` e `benchmark.json` (`8/8 PASS`, $\Delta \text{Pass Rate} = +0.75$).
- **Auditoria e Refatoração das Suítes de Teste do Workspace**:
  - Elevação de `tests/test_server.py`, `google-drive-index-app/tests/driveService.test.ts` e `google-drive-index-app/tests/googleAuth.test.ts` para **100% Nível 4 (Determinístico & Resiliente)** (eliminação de 15 inconformidades AST: `BRITTLE_CATALOG_COUNT`, `GLOBAL_STATE_LEAKAGE`, `WEAK_SURFACE_ASSERT` e `NON_DETERMINISTIC_TIME`).

### [2026-10-15] - Fase 8: Implantação da Skill `code-quality-audit-3d-physics` (`v1.0.0`) e Esteira de 5 Subskills em 3 Ondas
- **Arquitetura de 5 Módulos em 3 Ondas (`Topologia 3+1+1`)**:
  - Implementação consolidada de `static-sanitization-auditor` ($w_1=20\%$), `architecture-hardcoded-auditor` ($w_2=15\%$), `physics-3d-math-auditor` ($w_3=25\%$ com decomposição nas 5 sub-dimensões $S_1..S_5$), `deterministic-tests-auditor` ($w_4=20\%$, $Pass@10$) e `state-checker-observer` ($w_5=20\%$, filtro anti-alucinação e consolidador $S_{\text{norm}}$).
- **Ferramental Executável Refatorado (`scripts/`)**:
  - `static_ast_parser.py`: Normalização estrutural de AST (`LocalIdentifierNormalizer`), guarda contextual em `UNCHECKED_NORMALIZE`, 12 regras estáticas e cálculo automático de $s_1, s_2, s_3$ e $S_1..S_5$.
  - `js_ts_ast_parser.js`: Rastreamento exato de profundidade de blocos `{}` (`braceDepth`) para escopo de `inAnimationLoop`, 12 regras e suporte a execução via `franklin_run_skill_script` (`node`).
  - `physics_test_runner.py`: Suporte a CLI `--target` e `--json`, sub-stepping determinístico e Continuous Collision Detection (CCD) contra colisores finos.
  - `state_checker_observer.py`: Validação cruzada no código-fonte para eliminação de falsos positivos e emissão do Relatório Final padronizado.
- **Plano DAG**: Adicionado `plans/physics_code_audit_dag.json` compatível com `franklin_execute_dag`.

### [2026-10-14] - Fase 7: Internalização do Pacote `shared`, Saneamento de Caminhos da Máquina e Remoção de Monólitos Legados (23 Skills Canônicas)
- **Internalização Standalone (`shared/`)**:
  - Criado o pacote local `shared/` (`shared/tools/frontmatter_parser.py` e `shared/harness.py` com `SemanticGuard`, `evaluate_action_risk` e `CheckpointStore` em SQLite WAL), tornando `server.py` e `pytest tests/test_server.py` 100% autônomos em `c:\Users\melki\dev\repos\franklin-quebragalho`.
- **Alinhamento de Caminhos Reais do Ambiente**:
  - Padronizados todos os contratos, `references/`, `rules/`, `evals/` e scripts para os diretórios reais desta máquina: `C:\Users\melki\dev\repos\franklin-quebragalho`, `C:\Users\melki\dev\notes\` (`Inbox`, `Diário`, `Medicina`, `Pessoal`, `Projetos`, `Interesses`, `Modelos`, `Arquivo`, `Memória`), `C:\Users\melki\dev\tools\`, `C:\Users\melki\dev\sandbox\` e a taxonomia real de `G:\Meu Drive\`.
- **Eliminação de Redundâncias**:
  - Removidas definitivamente as 3 skills monolíticas legadas (`organizar-gdrive`, `organizar-local` e `gerar-docs-pdf`), já substituídas pelas 6 skills atômicas especializadas (`gdrive-auditoria-limpeza`, `gdrive-taxonomia-organizacao`, `manutencao-disco-windows`, `curadoria-obsidian-vault`, `redator-tecnico-markdown` e `conversor-html-pdf`), consolidando **23 skills canônicas** com 100% de aprovação (`23/23 PASS`).

### [2026-10-14] - Fase 6: Reorganização da Esteira `SkillCraft` (`evoluir-skills` v2.0.0, `aprimoramento` v2.0.0, `skill-auditor` v1.3.0 e `auditoria-projetos` v2.2.0)
- **Eliminação de Redundâncias e Encadeamento Automático em 4 Estágios (`authorized_sub_skills`)**:
  - `evoluir-skills` (`v1.1.0` → `v2.0.0`): Transformada no Orquestrador Mestre do Ciclo de Vida (`Entrypoint`) que encadeia automaticamente: **[Estágio 1]** `expansao-contexto-adaptativa` (desambiguação e estruturação da ideia bruta) ➔ **[Estágio 2]** `aprimoramento-expansibilidade-agentes-skills` (consultoria de arquitetura em 3 Tiers, Envelope Pattern, Context Forking e engenharia de métricas) ➔ **[Estágio 3]** `skill-creator` + `_template` (scaffolding físico) ➔ **[Estágio 4]** `skill-auditor-refatorador-skills` + `validate_skills.py` (homologação determinística e espelhamento).
  - `aprimoramento-expansibilidade-agentes-skills` (`v1.0.0` → `v2.0.0`): Evoluída para biblioteca consultiva completa em 3 Tiers, incorporando `references/guia_expansibilidade_e_metricas_2026.md` ($\text{Pass}@k$, Matriz de Confusão $\text{FNR} < 0.001$, `LLM-as-a-Judge` $S_{\text{norm}}$, Diagnóstico de Transcrições, *Lean Instructions*, *Trigger Eval Matrix* `should-trigger` vs `near-misses`, `adk optimize`/GEPA, Densidade Atencional Softmax, *Envelope Pattern* Pydantic, *Context Forking*, Memória em 3 Camadas, MCP/A2A e Matriz de Maturidade Níveis 1 a 4), além da criação inédita de `rules/criterios_auditoria.md` (7 regras booleanas) e `evals/evals.json` (4 casos de teste).
  - `skill-auditor-refatorador-skills` (`v1.2.0` → `v1.3.0`): Sincronizada como Estágio 4 da esteira `SkillCraft`, auditando conformidade com os 3 Tiers, *Trigger Matrix*, extração de scripts de `transcript.jsonl` e os 22 temas multidimensionais (`v2.6.0-2026`).
  - `auditoria-projetos-sistema` (`v2.1.0` → `v2.2.0`): Incorporadas as anotações de governança (`AGENTS.md`, desacoplamento Domínio/I-O/UI, tipagem estrita `pydantic.BaseModel`, chunking sanitizado por fronteiras sintáticas com metadados `source_id`/`chunk_index`/`byte_range`, snapshot por aba/menu e subpesos detalhados na rubrica 0–100).

### [2026-10-14] - Fase 5: Sincronização com o Motor Multidimensional `v2.6.0-2026` do FrontCraft Studio
- **Propagação do Catálogo de 22 Temas e DNA Multidimensional**:
  - Atualizadas as 4 skills de engenharia de interface (`analise-design-tatil-frontend` `v1.1.0`, `refatoracao-design-tatil-frontend` `v1.2.0`, `consultor-design-tatil-frontend` `v1.2.0` e `arquitetura-design-implementacao-sistema` `v1.2.0`).
  - Atualizados `references/paleta_estilo_melki.md` e `references/tokens_frontcraft.json` com as **10 Paletas Canônicas Melki**, os **5 Temas Tendências 2026** (`warm-editorial-paper`, `quiet-luxury-titanium`, `neo-swiss-grid`, `biophilic-matcha-stone`, `tactile-carbon-2026`), os **7 Temas de Estúdio**, os **4 Pares Tipográficos (`TYPOGRAPHY_PRESETS`)**, as **5 Geometrias de Borda (`GEOMETRY_PRESETS`)** e a física de inclinação 3D (`calculateCardTilt`).
  - Sincronizados `.agents/skills/` e `skills/` com 100% de aprovação determinística em `scripts/validate_skills.py` (`26/26 PASS`).

### [2026-10-04] - Fase 4: Padronização Canônica de Metadata e Governança Oficial 2026
- **Injeção do Bloco `metadata` e Licença em 100% das Skills (26/26)**:
  - Todas as 26 skills do catálogo receberam o cabeçalho canônico oficial compatível com Google Antigravity e ADK Platform, contendo `license: MIT` e bloco estruturado `metadata` (`version`, `author`, `category`, `updated_at`, `tags`).
  - Preservada paridade retrocompatível com chaves de primeiro nível (`version`, `author`, `category`, `updated_at`).
- **Atualização dos Validadores Determinísticos**:
  - `scripts/validate_skills.py` e `server.py` atualizados para suportar parsing de YAML aninhado (PyYAML com fallback resiliente), promovendo `metadata.version` e validando a integridade estrutural.
  - `skill-auditor-refatorador-skills` (v1.2.0): Ensinada a auditar a conformidade do bloco `metadata` nas skills do catálogo.
- **Sincronização Tripla 1:1**:
  - Espelhamento atômico entre `.agents/skills/`, `skills/` e o plugin global `~/.gemini/config/plugins/franklin-skills/`.
  - Auditoria determinística via `franklin_skills_validate` e `validate_skills.py` com `26/26 PASS` (100%).

### [2026-10-04] - Lançamento do Servidor MCP Global: Franklin Skills MCP
- **Servidor FastMCP Dedicado (`server.py`)**:
  - Implementação do servidor MCP nativo do ecossistema Franklin Quebra-Galho, registrado globalmente em `~/.gemini/config/mcp_config.json`.
  - **Ferramentas Especializadas**: `franklin_skills_list` (filtros por status/persona), `franklin_skills_get` (divulgação progressiva: contract, rules, references, evals, scripts, all), `franklin_skills_search` (busca semântica por intenção), `franklin_skills_validate` (auditoria determinística com 100% PASS), `franklin_get_agents` (catálogo de personas) e `franklin_run_skill_script` (execução segura de scripts).
  - **Recursos e Prompts MCP**: `skills://catalog`, `skills://manifest`, `skills://agents`, `skills://skill/{name}`, `skills://rules/{name}`, prompt `activate_skill` e prompt `tactile_frontend_audit`.
- **Validação e Homologação**: Suíte de testes automatizados com `pytest` (10/10 PASS), schemas JSON gerados em `~/.gemini/antigravity/mcp/franklin-skills/` e ambiente virtual gerenciado via `uv`.

### [2026-10-04] - Fase 3: Desacoplamento de Redação Técnica e Conversor Headless para PDF
- **Desacoplamento de Documentação e Publicação (`DocMaker`)**:
  - `redator-tecnico-markdown` (v1.0.0): Especialista em redação técnica, formatação Obsidian, alertas estilizados (`> [!NOTE]`, `> [!IMPORTANT]`), tabelas ricas com alinhamento e conformidade estrita com a Lei da Linha em Branco.
  - `conversor-html-pdf` (v1.0.0): Especialista em conversão física para PDF via Microsoft Edge/Chrome headless nativo, injetando CSS de impressão `@page`, margens A4 e proteção contra corte de tabelas e códigos (`page-break-inside: avoid;`).
- **Validação Paritária 100% PASS**: Sincronização em `.agents/skills/` e `skills/`, validada por `validate_skills.py` com 26/26 skills aprovadas.

### [2026-10-04] - Fase 2: Desacoplamento dos Monólitos de Armazenamento Local e Cloud
- **Desacoplamento do Google Drive (`DriveMaster`)**:
  - `gdrive-auditoria-limpeza` (v1.0.0): Inspeção de arquivos pesados (>100MB), identificação determinística de duplicados via SHA-256 e simulação dry-run com quarentena preventiva (`_Quarentena_Descarte/YYYY-MM-DD/`).
  - `gdrive-taxonomia-organizacao` (v1.0.0): Aplicação de árvore canônica numerada (`01_Projetos` a `99_Arquivo`), sanitização de nomes ilegais e prefixos com datas ISO (`YYYY-MM-DD`).
- **Desacoplamento de Sistema Local e Base de Conhecimento**:
  - `manutencao-disco-windows` (v1.0.0 - `FileOpsLocal`): Foco em SO. Triagem de Downloads, Desktop, instaladores antigos para `_Instaladores/` e arquivamento seguro de projetos inativos em `dev/_arquivo/` com proteção estrita do Cockpit Melki.
  - `curadoria-obsidian-vault` (v1.0.0 - `VaultMaster`): Foco em PKM. Validação de frontmatter YAML, verificação de links quebrados `[[Wikilinks]]`, detecção e isolamento de anexos órfãos (`_anexos_orfaos/`) e proteção absoluta da pasta `.obsidian/`.
- **Validação Paritária 100% PASS**: Sincronização em `.agents/skills/` e `skills/`, validada por `validate_skills.py` com 24/24 skills aprovadas.

### [2026-10-03] - Desacoplamento e Concepção das Skills de Frontend e Subagente FrontCraftMaster
- **Desacoplamento Canônico em Duas Skills Especializadas**:
  - `analise-design-tatil-frontend` (v1.0.0): Estritamente Read-Only. Inspeção de menus claustrofóbicos, sidebar mínima (240px), tipografia, ícones Lucide, botões ergonômicos (>= 40px), anti-squish e cores minerais, com emissão do Relatório Comparativo determinístico.
  - `refatoracao-design-tatil-frontend` (v1.0.0): Estritamente mutação de código. Módulos por framework (React/Next, Tailwind, HTML5), injeção de tokens do FrontCraft Studio, descompactação de navegação e botões convexos com micro-interações táteis (`active:scale-95`).
- **Criação do Subagente FrontCraftMaster**: Registrado formalmente em `AGENTS.md` e `MY_AGENTS.md` como especialista em UI/UX e design tátil.
- **Atualização na Auditoria**: Inseridos critérios determinísticos de UI/UX em `auditoria-projetos-sistema/rules/criterios_auditoria.md` (`[FAIL: MENU_COMPACTADO_CLAUSTROFOBICO]`, `[FAIL: BOTAO_PEQUENO_OU_SQUISH]`, etc.).
- **Validação Paritária 100% PASS**: Sincronização em `.agents/skills/` e `skills/`, validada por `validate_skills.py` com 20/20 skills aprovadas.

### [2026-10-03] - Consolidação e Integração da Skill high-level-context-planner (v2.0.0)
- **Planejamento Estratégico em Malha Fechada**: Implementação do nó planejador de alto nível (`SKILL_HIGH_LEVEL_CONTEXT_PLANNER_V2`), conectado diretamente com o `gap-analyzer-auditor` e o `skill-orquestrador-planos-encadeados`.
- **Fase 0 Mandatória e Critérios Go/No-Go**: Decomposição estruturada com garantia de alinhamento prévio e portões de decisão determinísticos por fase.
- **Protocolo de Consumo de Hand-Off (Replanning v2.0)**: Capacidade de absorver o payload YAML do auditor e emitir o Plano de Ação Revisado com ações de patch (`REFATORAR`, `INSERIR_GUARDRAIL`, `REMOVER_DEPENDENCIA`, `ADICIONAR_RETRY`, `BLOQUEIO_HITL`).
- **Validação e Paridade Total**: Pacote modular completo (`SKILL.md`, `references/`, `rules/criterios_auditoria.md` e `evals/evals.json`), aprovado com 100% de conformidade determinística (`validate_skills.py` 18/18 PASS) e espelhado 1:1 em `skills/high-level-context-planner/`.

### [2026-10-03] - Consolidação e Integração da Skill gap-analyzer-auditor (v2.0.0)
- **Auditoria em Malha Fechada (Closed-Loop Reflection)**: Implementação do nó crítico/auditor stateless (`SKILL_GAP_ANALYZER_AUDITOR_V2`), projetado para orquestração reflexiva encadeada com o `high-level-context-planner` e `skill-orquestrador-planos-encadeados`.
- **Protocolo Determinístico de RCA (4 Fases e 4 Vetores)**: Isolamento de fatos com taxonomia epistêmica (`[FATO]`, `[INFERÊNCIA]`, `[LACUNA]`), dissecação de causa-raiz nos vetores de Contexto/Injeção, Ferramenta/MCP, Arquitetura e Segurança/Confiabilidade, e formulação obrigatória de Opção 1 (Cirúrgica) vs Opção 2 (Arquitetural).
- **Contrato de Hand-Off Padronizado (YAML)**: Emissão de payload estruturado contendo `incident_id`, `required_adjustments` (`step`, `action`, `patch_instructions`) e `contingency_trigger` para consumo automático pelo agente planejador.
- **Validação e Paridade Total**: Pacote modular com `SKILL.md`, `references/`, `rules/criterios_auditoria.md` e `evals/evals.json`, aprovado com 100% de conformidade determinística (`validate_skills.py` 17/17 PASS) e espelhado 1:1 em `skills/gap-analyzer-auditor/`.

### [2026-10-03] - Consolidação e Integração da Skill refine-prompt (v3.0.0)
- **Engenharia e Governança**: Concepção e implantação da skill `refine-prompt` (Identificador: `SKILL_REFINE_PROMPT_V3_MASTER`), integrando ancoragem temporal estrita em 03/10/2026, busca ativa em fontes primárias e taxonomia epistêmica (`[FATO]`, `[INFERÊNCIA]`, `[LACUNA]`).
- **Segurança Zero-Trust e OWASP**: Scaffolding com tags XML (`<system_instructions>`, `<context>`, `<untrusted_user_input>`), defesas contra injeção de prompt direta e indireta (OWASP Top 10 for LLM 2025/2026), MCP Spec 2026-07-28 e callbacks determinísticos.
- **3 Módulos de Saída Estruturados**: Implementação de fluxos para Módulo 1 (Resposta Direta com Nota Metodológica), Módulo 2 (Artefato Plug-and-Play em bloco único contínuo com variáveis `[NOME]`) e Módulo 3 (Entrevista Socrática com no máximo 3 perguntas cirúrgicas e esboço provisório).
- **Validação e Paridade**: Pacote modular completo (`SKILL.md`, `references/`, `rules/criterios_auditoria.md` e `evals/evals.json`), aprovado com 100% de conformidade determinística (`validate_skills.py`) e espelhado 1:1 em `skills/refine-prompt/`.

### [2026-10-03] - Adição dos 4 Módulos Canônicos de Design Tátil e Preferências Melki
- **Engenharia dos 4 Módulos Canônicos**: Implementação padronizada dos módulos: (1) Paleta de Cores Canônica (Superfícies Ardósia/Creme, Acentos Minerais, Banimento Anti-Cobalto `#0044FF`/`#233DFF`/`#1D4ED8`), (2) Design Tátil & Composição Visual (Tactile Matte 4K, Cards Lighter than Canvas, Sombras Multicamadas, Rim Light Zenital, Anti-Squish em botões, Suporte a TDAH sem alerts bloqueantes), (3) Opções das Preferências do Desenvolvedor (Consulta via `ask_question`, 5 arquétipos canônicos e componentes copy-paste do ecossistema shadcn/ui, Radix UI e Lucide Icons) e (4) Matriz de Detecção de Discrepâncias com as Preferências (Checklist determinístico com marcadores `[PASS]`, `[FAIL]`, `[UNVERIFIED]`).
- **Skills Atualizadas**: `consultor-design-tatil-frontend` (v1.1.0), `_template` (v1.2.0), `skill-auditor-refatorador-skills` (v1.1.0), `skill-orquestrador-planos-encadeados` (v1.1.0) e `arquitetura-design-implementacao-sistema` (v1.1.0).
- **Paridade Estrita**: Sincronização 1:1 entre `.agents/skills/`, `skills/` e o plugin global `franklin-skills`. Validação determinística 100% PASS via `validate_skills.py`.

### [2026-10-03] - Criação e Validação da Skill consultor-design-tatil-frontend (v1.0.0)
- **Consultoria Tátil Especializada**: Engenharia do sistema tátil Melki (Cards mais claros que o canvas no dark mode, profundidade Z de múltiplas camadas, rim-light linear no topo, paleta mineral sóbria e banimento estrito de azul cobalto saturado).
- **Mapeamento Ativo via agent-browser**: Integração completa com inspeção de DOM dinâmico (`agent-browser snapshot -i`), auditoria de acessibilidade por nós `@eX` e screenshots anotados.
- **Estrutura Canônica Antigravity 2026**: Pacote modular com `SKILL.md`, `references/paleta_estilo_melki.md`, `rules/criterios_auditoria.md` (7 regras determinísticas booleanas) e `evals/evals.json` (3 cenários reais).
- **Conformidade Contratual 100% PASS**: Aprovada pelo script de validação (`validate_skills.py`) e espelhada simultaneamente em `.agents/skills/` e `skills/` no Franklin Quebra-Galho e no plugin global.


### [2026-10-03] - Integração do agent-browser na Skill auditoria-projetos-sistema (v2.1.0)
- **Substituição de Esteira Visual**: Integração nativa com a CLI `agent-browser` para inspeção dinâmica do DOM vivo e automação de capturas.
- **Auditoria Dinâmica de Nós Interativos**: Incorporação do comando `agent-browser snapshot -i` para extração de nós `@eX`, detecção de botões sem handlers reais e verificação de acessibilidade ARIA sem divsoup.
- **Captura Anotada para Modelos de Visão**: Adição de screenshots anotados com rótulos numéricos (`agent-browser screenshot --annotate`) e testes automáticos de temas claro e escuro (`--color-scheme dark/light`).
- **Conexão com Chrome Ativo**: Suporte a depuração de abas abertas via `--cdp 9222` e `--auto-connect`.
- **Governança Determinística**: Atualizados `rules/criterios_auditoria.md` (Regra 5) e `evals/evals.json` (TC-03 e TC-04).

### [2026-10-03] - Auditoria e Refatoração Canônica das 14 Skills do Catálogo (100% PASS)
- **Refatoração Estrutural Completa**: Padronizadas as 5 seções canônicas obrigatórias (Gatilhos, Entradas, Processamento, Saídas e Limites/Exceções) em todas as skills.
- **Implementação Universal de Rules e Evals**: Criados `rules/criterios_auditoria.md` (com marcadores booleanos determinísticos `[PASS]` e `[FAIL]`) e `evals/evals.json` em todas as skills pendentes (`_template`, `context-sentinel`, `design-interface-medica-minimalista`, `evoluir-skills`, `gerar-docs-pdf`, `organizar-gdrive` e `organizar-local`).
- **Validação Automatizada Determinística**: O script `scripts/validate_skills.py` agora aprova 14/14 skills com 100% de conformidade contratual.
- **Espelhamento Paritário em `skills/`**: Sincronizadas as 14 skills completas entre `.agents/skills/` e a pasta raiz `skills/`.
- **Registro de Novas Skills**: Inclusão formal de `auditoria-projetos-sistema`, `skill-auditor-refatorador-skills` e `skill-orquestrador-planos-encadeados` no catálogo oficial.

### [2026-10-01] - Saneamento de Catálogo, Espelhamento e Integração Global
- **Saneamento de Caminhos e Links**: Eliminadas todas as referências residuais ao diretório obsoleto `wonderful-franklin`, unificando links com prefixo `c:/Users/melki/dev/repos/franklin-quebragalho/`.
- **Espelhamento Paritário em `skills/`**: Concluída a replicação das 4 novas skills (`aprimoramento-expansibilidade-agentes-skills`, `arquitetura-design-implementacao-sistema`, `context-sentinel` e `design-interface-medica-minimalista`) de `.agents/skills/` para a pasta raiz `skills/`, garantindo consistência total entre o agente nativo e a raiz do projeto.
- **Integração com Governança Global 2026**: Vinculação formal às diretrizes `00-unified-governance.md` e `02-layout-shielding.md`, inclusão das 11 skills no catálogo de ciclo de vida e ativação dos checkpoints de contexto.

### [2026-09-27] - Evolução da Skill `organizador-fluxo-arvore-arquivos` (v1.1.0)
- **Opção de Exportação Direta (MD/PDF)**: Adicionada a seção `### 6. Opção de Exportação (Arquivo Único / PDF)` ao final da entrega para oferecer geração direta em arquivo Markdown único ou PDF formatado, eliminando quebras de layout e diagramas ao copiar e colar.
- **Governança Determinística**: Criado `rules/criterios_auditoria.md` com validações booleanas e `evals/evals.json` com testes de preservação literal do prompt e oferta de exportação.
- **Espelhamento e Status**: Promovida para status `✅ Validada` e sincronizada em `.agents/skills/` e `skills/`.

### [2026-09-27] - Evolução da Engenharia de Skills e Atualização do Arquiteto (v2.2.0 / v1.1.0)
- **Skill `arquiteto-conteudo-solucoes` (v2.2.0)**:
  - Implementada a taxonomia canônica de 4 modos de operação (Modo A: Execução Direta, Modo B: Refinamento Colaborativo com máximo 2 perguntas, Modo C: Planejamento Estruturado com Fase 0 obrigatória, Modo D: Auto-Reflexão Pré-Entrega).
  - Criado o arquivo `rules/criterios_auditoria.md` estabelecendo critérios determinísticos falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) e eliminando validações vazias e auditorias inventadas.
  - Criado o conjunto de testes empíricos em `evals/evals.json` para validação de comportamento real.
  - Sincronização e espelhamento estrito entre `.agents/skills/` e `skills/`.
- **Skill `evoluir-skills` (v1.1.0)**:
  - Atualizada com as diretrizes consolidadas de 2026: divulgação progressiva, proibição de simulações sintéticas no chat e exigência de âncoras documentais falsificáveis.
- **Skill `_template` (v1.1.0)**:
  - Atualizado para incluir o catálogo completo de subpastas recomendadas (`rules/`, `evals/`, `references/`, `scripts/`) e seções de limites/exclusão.

### [2026-09-27] - Inclusão da Skill `arquiteto-conteudo-solucoes` (v1.0.0)
- **Nova Habilidade Registrada**: Adicionada a skill `arquiteto-conteudo-solucoes` com suporte a 4 modos de operação (Execução Direta, Refinamento Colaborativo, Planejamento Estruturado e Auto-Reflexão Pré-Entrega), além das referências técnicas complementares em `references/diretrizes_especializadas.md` e `references/checklist_validacao.md`.

### [2026-09-27] - Inclusão da Skill `organizador-fluxo-arvore-arquivos` (v1.0.0)
- **Nova Habilidade Registrada**: Adicionada a skill `organizador-fluxo-arvore-arquivos` para traduzir ideias de software e processos em diagramas Mermaid intuitivos e árvores ASCII comentadas de arquivos, com controle de versão semântico e preservação integral do pedido original.

### [2026-09-27] - Inicialização do Laboratório de Skills (v1.0.0)
- **Criação do Framework**: Estruturação inicial do workspace `franklin-quebra-galho`.
- **Skill `_template`**: Criado modelo com frontmatter oficial YAML (`name`, `description`) e subpastas recomendadas (`scripts/`, `references/`).
- **Skill `organizar-gdrive`**: Adicionado fluxo de inspeção no `G:\Meu Drive` com regras de dry-run e integração MCP `google-drive`.
- **Skill `organizar-local`**: Definidas rotinas de triagem para pastas Windows (`Downloads`, `Desktop`, `dev/`) usando cmdlets nativos do PowerShell.
- **Skill `gerar-docs-pdf`**: Desenvolvido fluxo de criação de notas compatíveis com Obsidian e script de conversão de Markdown para PDF via Edge/Chrome headless.
- **Skill `evoluir-skills`**: Documentado o procedimento de melhoria contínua de skills com histórico de evolução e métricas de ativação.

---

## 🛠️ Como Criar e Testar uma Nova Skill

1. **Duplique o Template**:
   Copie a pasta `.agents/skills/_template/` para `.agents/skills/<sua-nova-skill>/`.
2. **Defina o Frontmatter**:
   - `name`: Nome em minúsculas separado por hífens (ex.: `limpar-cache-dev`).
   - `description`: Descreva em terceira pessoa **o que** a skill faz e **quando** deve ser ativada.
3. **Adicione os Passos e Scripts**:
   - Mantenha o `SKILL.md` conciso (progressivo).
   - Coloque comandos pesados ou scripts em `scripts/`.
4. **Teste a Ativação**:
   - Faça uma pergunta de teste simulando a intenção do usuário e confirme se o agente ativa a skill.
5. **Registre no Manifesto**:
   - Adicione a linha correspondente na tabela acima e adicione uma entrada de changelog no histórico.
