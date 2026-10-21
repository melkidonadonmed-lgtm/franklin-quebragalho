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

### 📦 Catálogo de Skills do Workspace (29 Skills Canônicas)

| Skill | Versão | Status | Descrição Curta | Localização |
| :--- | :---: | :---: | :--- | :--- |
| **`organizador-projetos-ideias`** | `v1.0.0` | 🚀 Produção | Organizador de ideias do zero (`ideation_to_v1`: perguntas guiadas, sugestão de MVP quando o usuário responde *"não sei"*, design e criação da `v1.0` com data) e sincronizador completo de projetos (`project_organizer_sync`: `README.md` fiel ao disco, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `DESIGN.md`, `.env`/`.gitignore`, contratos `MCP`/`tools.json`, `FastAPI`/`RPC`, Mermaid, limpeza da raiz e memória). | [skills/organizador-projetos-ideias/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-projetos-ideias/SKILL.md) |
| **`antigravity-project-auditor`** | `v2.0.0` | 🚀 Produção | Auditor arquitetural, diagnóstico de MVP (justificativa causal `Por quê:`) e planejamento em 3 fases (`autonomous_scan` vs. `targeted_focus` 80/20) sob 5 pilares técnicos (*Design/UI*, *Segurança*, *Atualização 2026*, *Code Quality*, *Árvore & Componentes*) e níveis `[PRIORIDADE \| MODERADO \| EXTRA]`. | [skills/antigravity-project-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/antigravity-project-auditor/SKILL.md) |
| **`minimal-impact-ui`** | `v1.0.0` | 🚀 Produção | Sistema e Atlas Interativo de Design de Impacto Mínimo Anti-TDAH (`atlas_ex_umbris_winui.html`): 3 temas (Cinza `#57545d` + Menus `#8e8999` padrão, Escuro `#09090B`, Claro `#F3F3F5`), 4 acentos 2% (tinta escura `#091318`/`#062016` em Azul/Verde), zero texto vermelho ou serifa fina no cinza/escuro (`.highlight-surgical`), 6 Arquétipos de Página e 28 efeitos WinUI 3 + Ex Umbris. | [skills/minimal-impact-ui/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/minimal-impact-ui/SKILL.md) |
| **`code-acceptability-auditor`** | `v1.0.0` | 🚀 Produção | Auditoria estática AST e Pydantic v2 de código Python (`SEC001..003`, `SYN001`, `ERR001..003`, `TYP001..002`, `ARCH001`), Quality Gate ($\ge 75/100$), Trigger Matrix (`TRIG-01..20`, $F_1 = 1.0$) e `SkillFailureAuditor`. | [skills/code-acceptability-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-acceptability-auditor/SKILL.md) |
| **`design-md`** | `v5.0.0` | 🚀 Produção | Gerador de contratos `DESIGN.md` (`v5.0`) orientado ao propósito do projeto e às preferências de estilo (`preferencias_estilo_e_temas.md` e `minimal-impact-ui`: *Ad Lucem*, *Cinza Monolítico `#57545d` + Menus `#8e8999`*, *Preto Terminal IBM `Ex Umbris` + `IBM Plex`*, *AETHER 2027* e 6 Arquétipos de Página). | [skills/design-md/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/design-md/SKILL.md) |
| **`frontend-code-architect`** | `v5.0.0` | 🚀 Produção | Arquiteto de código Frontend em **Atomic Design (5 camadas)**, tipagem estrita (`strict: true`, zero `any`), `<SurfaceCard />` (sombra esculpida 3 camadas + `1px` Rim Light), 6 Arquétipos de Página, 28 efeitos WinUI 3 + Ex Umbris e tokens por objetivo (`minimal-impact-ui`). | [skills/frontend-code-architect/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-code-architect/SKILL.md) |
| **`frontend-testing-auditor`** | `v3.0.0` | 🚀 Produção | Gatekeeper determinístico de testes e arquitetura visual Frontend: `scripts/audit_tactile_ui.py` (`v3.0`), FSM 4 estados (`idle`, `loading`, `error`, `pressed`), WCAG 2.1 AA/AAA (`jest-axe`), `tabular-nums`, `prefers-reduced-motion` e rubrica `AUDIT-VIS-01` (0-100 pts). | [skills/frontend-testing-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-testing-auditor/SKILL.md) |
| **`test-quality-auditor`** | `v1.2.0` | 🚀 Produção | Auditor modular (`<300` linhas/módulo) em 5 domínios (Python, TS/JS, Go `*_test.go`, MCP `JSON-RPC 2.0` e Harness HITL/Evals) com espelhamento 1:1 em `evals/modules/*_evals.json`. | [skills/test-quality-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/test-quality-auditor/SKILL.md) |
| **`code-quality-audit-3d-physics`** | `v1.0.0` | 🚀 Produção | Auditoria de código e Física 3D em 3 ondas (5 subskills: sanitização AST Py/JS, hardcoded, 5 sub-dimensões de física, testes Pass@10 e observador $S_{\text{norm}}$). | [skills/code-quality-audit-3d-physics/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/SKILL.md) |
| **`organizador-fluxo-arvore-arquivos`** | `v1.2.0` | 🚀 Produção | Converte ideias brutas em diagramas Mermaid, árvores de arquivos e planos de execução, com exportação direta em MD ou PDF. | [skills/organizador-fluxo-arvore-arquivos/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-fluxo-arvore-arquivos/SKILL.md) |
| **`arquiteto-conteudo-solucoes`** | `v2.4.0` | 🚀 Produção | Arquiteto autônomo em 4 modos (Execução Direta, Refinamento, Planejamento Fase 0 e Auto-Reflexão), Biblioteca de 5 Prompts Enterprise e 7 Módulos de Guardrails por Domínio (`M1`..`M7`). | [skills/arquiteto-conteudo-solucoes/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/arquiteto-conteudo-solucoes/SKILL.md) |
| **`evoluir-skills`** | `v2.2.0` | 🚀 Produção | Orquestrador Forward Builder & TDD (3 passos: `expansao-contexto-adaptativa` ➔ `_template` `M1..M7` ➔ `skill-auditor-refatorador-skills`) sem duplicação de regras. | [skills/evoluir-skills/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/evoluir-skills/SKILL.md) |
| **`aprimoramento-expansibilidade-agentes-skills`** | `v2.2.0` | 🚀 Produção | Arquiteto de sistemas agênticos em 5 Módulos (`A..E`): Ontologia/Frameworks, Loop Cognitivo 8 passos + 5 Camadas de Memória, Tools Pydantic/`PolyExtensibleSkillEngine`/MCP 2026-07-28, Theranostic Gate e Auditoria Matemática (`Pass@k`, `D_cos`, `FNR<0.001`, `Snorm`, `TEI`). | [skills/aprimoramento-expansibilidade-agentes-skills/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/aprimoramento-expansibilidade-agentes-skills/SKILL.md) |
| **`arquitetura-design-implementacao-sistema`** | `v3.0.0` | 🚀 Produção | Diagnóstico de propósito e MVP, navegabilidade comentada, Ilhas Funcionais (Island UI/UX), seleção de atmosfera por objetivo, tipografia linear `clamp()` + `tabular-nums`, motor `SGA` determinístico e relatório HTML V1 vs V2. | [skills/arquitetura-design-implementacao-sistema/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/arquitetura-design-implementacao-sistema/SKILL.md) |
| **`auditoria-projetos-sistema`** | `v3.0.0` | 🚀 Produção | Auditoria estrutural (`AGENTS.md`, desacoplamento, tipagem Pydantic, chunking semântico), diagnóstico do propósito do projeto, adequação de tema/atmosfera, espaçamento, contraste, tipografia, camadas esculpidas e esteira `agent-browser` (0-100 pts). | [skills/auditoria-projetos-sistema/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/auditoria-projetos-sistema/SKILL.md) |
| **`context-sentinel`** | `v1.1.0` | 🚀 Produção | Auditoria de integridade da janela de contexto, mitigação de context rot e snapshots determinísticos estruturados Pydantic/SQLite. | [skills/context-sentinel/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/context-sentinel/SKILL.md) |
| **`design-interface-medica-minimalista`** | `v3.0.0` | 🚀 Produção | Arquitetura visual clínica/hospitalar orientada ao turno/ambiente (Ambulatório `Ad Lucem`, Enfermaria Monolítica `#57545d` + `#8e8999`, UTI/Radiologia `Ex Umbris` + `IBM Plex`), `tabular-nums`, zero emojis e impressão A4 sob `preferencias_estilo_e_temas.md`. | [skills/design-interface-medica-minimalista/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/design-interface-medica-minimalista/SKILL.md) |
| **`skill-auditor-refatorador-skills`** | `v2.3.0` | 🚀 Produção | Cirurgião estrutural e Gatekeeper determinístico do Checklist Mestre (5 Eixos Transversais + 7 Módulos de Domínio `M1..M7`), eliminação de redundâncias e desacoplamento de monólitos. | [skills/skill-auditor-refatorador-skills/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/skill-auditor-refatorador-skills/SKILL.md) |
| **`skill-orquestrador-planos-encadeados`** | `v2.0.0` | 🚀 Produção | Orquestrador de planos multifásicos com portão de qualidade de arquitetura visual orientada ao propósito (`preferencias_estilo_e_temas.md`) e matriz de discrepâncias. | [skills/skill-orquestrador-planos-encadeados/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/skill-orquestrador-planos-encadeados/SKILL.md) |
| **`refine-prompt`** | `v3.2.0` | 🚀 Produção | Auditoria de factibilidade (`[VEREDITO]`), classificação epistêmica (`[FATO]`, `[INFERÊNCIA]`, `[LACUNA]`), modulação de entropia (*Determinismo na Borda vs. Fluidez Cognitiva* + contratos e micro-prompts de Baixa Entropia) e refinamento Zero-Trust em 3 módulos. | [skills/refine-prompt/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/refine-prompt/SKILL.md) |
| **`gap-analyzer-auditor`** | `v2.0.0` | 🚀 Produção | Auditor técnico e analista de brechas em malha fechada (closed-loop), RCA em 4 vetores e hand-off estruturado para o planejador. | [skills/gap-analyzer-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gap-analyzer-auditor/SKILL.md) |
| **`high-level-context-planner`** | `v2.0.0` | 🚀 Produção | Arquiteto estratégico e planejador de contexto em malha fechada, Fase 0 obrigatória, critérios Go/No-Go e replanning v2.0. | [skills/high-level-context-planner/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/high-level-context-planner/SKILL.md) |
| **`gdrive-auditoria-limpeza`** | `v1.0.0` | 🚀 Produção | Varredura de arquivos pesados (>100MB), identificação de duplicados por hash SHA-256 e quarentena segura no Google Drive. | [skills/gdrive-auditoria-limpeza/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-auditoria-limpeza/SKILL.md) |
| **`gdrive-taxonomia-organizacao`** | `v1.1.0` | 🚀 Produção | Estrutura canônica numerada real do Drive, padronização de nomenclatura com datas ISO (YYYY-MM-DD) e triagem documental. | [skills/gdrive-taxonomia-organizacao/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-taxonomia-organizacao/SKILL.md) |
| **`manutencao-disco-windows`** | `v1.1.0` | 🚀 Produção | Manutenção do SO Windows 11: triagem de Downloads, Desktop, isolamento de instaladores e arquivamento em `dev\` (`repos`, `sandbox`, `tools`, `notes`). | [skills/manutencao-disco-windows/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/manutencao-disco-windows/SKILL.md) |
| **`curadoria-obsidian-vault`** | `v1.1.0` | 🚀 Produção | Curadoria do cofre Obsidian (`C:\Users\melki\dev\notes\`): validação de frontmatter YAML, `[[Wikilinks]]` e anexos órfãos. | [skills/curadoria-obsidian-vault/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/curadoria-obsidian-vault/SKILL.md) |
| **`redator-tecnico-markdown`** | `v1.2.0` | 🚀 Produção | Redação técnica de relatórios executivos, notas técnicas e documentações compatíveis com `C:\Users\melki\dev\notes\Inbox\`. | [skills/redator-tecnico-markdown/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/redator-tecnico-markdown/SKILL.md) |
| **`conversor-html-pdf`** | `v1.0.0` | 🚀 Produção | Conversão determinística de Markdown/HTML para PDF profissional via Edge headless com CSS de impressão calibrado. | [skills/conversor-html-pdf/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/conversor-html-pdf/SKILL.md) |
| **`_template`** | `v3.0.0` | 🚀 Produção | Fonte Única de Verdade (SSOT) da anatomia de 9 pontos de uma skill, Checklist Transversal de 5 Eixos, 7 Módulos de Guardrails por Domínio (`M1`..`M7`) e `preferencias_estilo_e_temas.md`. | [skills/_template/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/_template/SKILL.md) |

---

## 📜 Histórico de Versões e Contexto (Changelog)

### [2026-10-21] - Fase 23: Implantação da Skill `organizador-projetos-ideias` (`v1.0.0`) — Concepção de Ideias (`ideation_to_v1` + Fallback *"Não sei"*) e Sincronização Integral de Projetos (`project_organizer_sync`) (`29/29 PASS`)
- **Nova Skill Canônica ([`skills/organizador-projetos-ideias/SKILL.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-projetos-ideias/SKILL.md))**:
  - **Modo 1 (`ideation_to_v1`)**: Refinamento de ideias iniciais com perguntas sobre intenção/objetivo, protocolo inteligente quando o usuário responde *"não sei"* às funções (propondo automaticamente o MVP mínimo), alinhamento de design, estrutura de pastas e repositório online, e geração da **Versão `1.0.0`** com metadados datados.
  - **Modo 2 (`project_organizer_sync`)**: Leitura completa de projetos existentes, diagrama de funcionamento em Mermaid, sincronização dos documentos-chave (`AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `DESIGN.md`, `GEMINI.md`/`CLAUDE.md` e `README.md` batendo 100% com os arquivos reais do disco), checagem de `.env`/`.gitignore`, padronização de componentes e contratos (`tools.json` MCP, FastAPI, RPC com métodos), limpeza segura da raiz e atualização da memória/contexto.
  - Homologação determinística via [`rules/criterios_auditoria.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-projetos-ideias/rules/criterios_auditoria.md), [`evals/evals.json`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-projetos-ideias/evals/evals.json) e [`references/guia_contratos_mcp_fastapi_rpc_e_documentos.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/organizador-projetos-ideias/references/guia_contratos_mcp_fastapi_rpc_e_documentos.md).

### [2026-10-21] - Fase 22: Implantação da Skill `antigravity-project-auditor` (`v2.0.0`) — Diagnóstico de MVP, Roteamento Dinâmico (`autonomous_scan` | `targeted_focus`) e Planejamento em 3 Fases (`28/28 PASS`)
- **Nova Skill Canônica ([`skills/antigravity-project-auditor/SKILL.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/antigravity-project-auditor/SKILL.md))**:
  - Implementação do **Auditor de Projeto, Diagnóstico de MVP e Planejamento (`v2.0.0`)** com roteamento dinâmico entre **Modo 1 (`autonomous_scan` — varredura completa sem conversa)** e **Modo 2 (`targeted_focus` — 80% de foco na pergunta específica)**.
  - Inspeção prioritária de `CONTEXT.md`, `AGENTS.md`, `SPEC.md`/`TODO.md`, `README.md` (com fallback para `package.json`, `pyproject.toml` e `/src` e marcação explícita `[ARQUIVO AUSENTE]`) e consulta à memória ativa.
  - Avaliação estruturada nos **5 Pilares Obrigatórios** (*Design e UI/UX*, *Segurança AppSec & IA*, *Atualização Temporal 2026*, *Qualidade de Código* e *Componentização & Árvore de Arquivos*) com classificação `[PRIORIDADE | MODERADO | EXTRA]`, regras determinísticas em [`rules/criterios_auditoria.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/antigravity-project-auditor/rules/criterios_auditoria.md) e casos de teste em [`evals/evals.json`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/antigravity-project-auditor/evals/evals.json).

### [2026-10-20] - Fase 21: Evolução da Skill `refine-prompt` (`v3.2.0`) — Engenharia de Fluidez vs. Rigor e Referências de Baixa Entropia (`27/27 PASS`)
- **Nova Referência Canônica ([`references/engenharia_fluidez_e_baixa_entropia.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/refine-prompt/references/engenharia_fluidez_e_baixa_entropia.md))**:
  - **Auditoria de Literatura Primária (Padrão 2026)**: Ancoragem formal em Wallace et al. (*Instruction Hierarchy*, 3 estratos + *Prompt Caching*), Liu et al. (*Lost in the Middle* & *Sandwiching*), Zhou et al. (*IFEval* & *Prompt Complexity Wall*), Madaan et al. / Shinn et al. (*Self-Refine* autorregressivo realista via *Thinking* nativo ou campo preliminar JSON `"_pre_flight_check"`) e Sumers et al. (*CoALA*, 4 estratos de memória híbrida).
  - **Engenharia de Fluidez vs. Rigor**: Separação entre *Determinismo na Borda* (schemas `Pydantic v2`/`Zod`/`Go structs` com `agent_hint`) e *Fluidez Cognitiva no Centro* (*Why-First Principle*, roteamento dinâmico de formato prosa/tabela/lista e banimento de rótulos mecânicos que causam *Prompt-Induced Mode Collapse*).
  - **Catálogo de Contratos e Micro-Prompts de Baixa Entropia**: Matriz de 5 rotinas recorrentes ($H(Y \mid X) \to 0$), 4 micro-prompts plug-and-play (conversão de notas brutas com token de escape `[NÃO INFORMADO: dado]`, triagem rápida de stack trace em 10s, higienização de arquivos em lote e extração JSON Zero-Trust com `"_pre_flight_check"`), contratos poliglotas corrigidos (Python, TypeScript Zod, Go) e o bloco de bolso `<core_operating_rules>`.
- **Atualização de Contrato, Regras e Evals (`SKILL.md`, `rules/criterios_auditoria.md` Regra 8, `evals/evals.json` `TC-07` e `TC-08`)**:
  - Saneado o ponteiro legado de `paleta_estilo_melki.md` para `preferencias_estilo_e_temas.md` e adicionados os testes `TC-07-BAIXA-ENTROPIA-CONVERSOR-NOTAS-BRUTAS` e `TC-08-DESENGESSAMENTO-E-BUFFER-SELF-REFINE`.

### [2026-10-19] - Fase 20: Incorporação da Skill `minimal-impact-ui` (`v1.0.0`) e Atlas Canônico `Ex Umbris // WinUI 3` (`atlas_ex_umbris_winui.html`) no Catálogo (`27/27 PASS`)
- **Implantação da Skill `minimal-impact-ui` (`v1.0.0` — `skills/minimal-impact-ui/`)**:
  - Adicionada ao catálogo canônico como referência central de **Design de Impacto Mínimo, Anti-TDAH e Ergonomia WinUI 3 + Ex Umbris**, contendo o Atlas Interativo [`references/atlas_ex_umbris_winui.html`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/minimal-impact-ui/references/atlas_ex_umbris_winui.html) (`Readiness Score: 100.0/100.0 PASS` em `audit_tactile_ui.py`) e o Compêndio All-in-One [`references/compendio_completo_ex_umbris_winui.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/minimal-impact-ui/references/compendio_completo_ex_umbris_winui.md).
  - Consolidadas em todo o ecossistema (`preferencias_estilo_e_temas.md`, `design-md`, `frontend-code-architect`, `frontend-testing-auditor`, `auditoria-projetos-sistema`, `design-interface-medica-minimalista` e subagentes `agents/ui-*.md`) as regras do Atlas: **3 Temas com Cinza `#57545d` + Menus `#8e8999` padrão**, **4 Cores de Acento 2%** (`Crimson #D9383A`, `Azul #35acd8`, `Esmeralda #10B981`, `Violeta #8B5CF6`) com **tinta escura obrigatória nos botões Azul (`#091318`) e Verde (`#062016`)**, **proibição absoluta de texto vermelho corrido ou serifa fina em fundos cinzas/escuros** (substituídos por `.highlight-surgical` e `.accent-text`), **6 Arquétipos Estruturais de Página** além de formulários/gráficos e **28 efeitos catalogados WinUI 3 + Ex Umbris**.

### [2026-10-19] - Fase 19: Transição de "Paleta de Cores Fixa" para Preferências de Estilo, Arquitetura Visual & Temas por Objetivo (`preferencias_estilo_e_temas.md`), Exclusão das 3 Skills Táteis Redundantes e Evolução de `auditoria-projetos-sistema` (`v3.0.0`) (`26/26 PASS`)
- **Substituição de Paletas Fixas por Preferências de Estilo e Temas Orientados ao Propósito (`skills/_template/references/preferencias_estilo_e_temas.md`)**:
  - Removido `paleta_estilo_melki.md` (que deixava todos os projetos com aparência repetitiva) e criado `preferencias_estilo_e_temas.md`, estabelecendo que a atmosfera e o tema devem ser selecionados **de acordo com o propósito/objetivo do projeto** (*Conversão/SaaS*, *Editorial*, *FinTech*, *IA Nativa*, *MedTech*, *DevTools/Terminal IBM*).
  - Documentadas as **4 Famílias Atmosféricas Adaptativas**: **(1) Ad Lucem** (`#F3F3F5` / `#FFFFFF` + card de contraste `#18181C`), **(2) Cinza sobre Cinza Monolítico** (`#57545d` + menus em pílula `#8e8999` com tinta escura de alto contraste `#16151A`), **(3) Preto Terminal IBM (`Ex Umbris`)** (`#070709` + tipografia obrigatória **`IBM Plex Sans` + `IBM Plex Mono`**) e **(4) AETHER 2027** (`oklch()` + APCA), mantendo `design_md_v4_5_studio.html` como referência opcional junto aos novos catálogos `ex_umbris_ad_lucem_studio.html` e `aether_2027_design_system.html` em `skills/design-md/references/`.
- **Exclusão das 3 Skills Táteis Redundantes (`29 -> 26 Skills Canônicas`)**:
  - Removidas `analise-design-tatil-frontend`, `consultor-design-tatil-frontend` e `refatoracao-design-tatil-frontend`, consolidando toda a inteligência de diagnóstico por propósito, geração de contrato, scaffolding modular e auditoria determinística nas skills canônicas **`auditoria-projetos-sistema` (`v3.0.0`)**, **`design-md` (`v5.0.0`)**, **`frontend-code-architect` (`v5.0.0`)**, **`frontend-testing-auditor` (`v3.0.0`)** e **`design-interface-medica-minimalista` (`v3.0.0`)**, além dos 4 subagentes `agents/ui-*.md` (`v3.0.0`).
- **Adaptação de `auditoria-projetos-sistema` (`v3.0.0`) e `audit_tactile_ui.py` (`v3.0.0`)**:
  - `auditoria-projetos-sistema` agora avalia na Dimensão 5 (20 pts) o **diagnóstico do propósito do projeto**, encaixe do melhor tema, espaçamento/respiro ($\ge 25\%$), contraste perceptual, tipografia fluida (`clamp()` + `tabular-nums` + `IBM Plex` em terminal escuro), camadas esculpidas em 3 níveis + `1px` Rim Light e FSM em 4 estados.

### [2026-10-19] - Fase 18: Auditoria Estrutural Integral das 29 Skills do Catálogo, Eliminação de Duplicatas SHA-256, Padronização `<= 300` Linhas e `Quality Score: 100.0/100.0` em 100% dos Scripts Python (`29/29 PASS`)
- **Desacoplamento e Eliminação de Redundâncias nas 8 Skills de Frontend (`Topologia 3+1`)**:
  - Eliminados 100% dos arquivos `references/` duplicados por hash SHA-256 entre `analise-design-tatil-frontend` (Fase 1), `consultor-design-tatil-frontend` (Fase 2) e `refatoracao-design-tatil-frontend` (Fase 3), unificando a SSOT de tokens e presets em `consultor-design-tatil-frontend/references/` (`--surface-canvas: #F1F4F8`, `--surface-inset: #E5E9F0`).
  - Saneadas contradições legadas (`border: 1px solid`, `font-size: 0.75rem`) em `design-interface-medica-minimalista` (`v2.2.0`) com criação de `references/guia_tokens_clinicos_a4.md`.
  - Refatorados `audit_tactile_ui.py` (262 linhas) e `deterministic_scorer.py` (272 linhas, com fachada de re-exportação em `modules/deterministic_scorer.py`) para atingir `Quality Score: 100.0/100.0`.
- **Divulgação Progressiva em 3 Tiers, `SKILL.md <= 300` Linhas e *Trigger Matrix* em 100% do Catálogo**:
  - Enxugado `auditoria-projetos-sistema/SKILL.md` (`v2.3.0`, de 306 para 105 linhas) com extração para `references/rubrica_auditoria_e_agent_browser.md`.
  - Criados os arquivos `references/` dedicados em `context-sentinel` (`v1.1.0`, `schema_context_sentinel.md`) e `organizador-fluxo-arvore-arquivos` (`v1.2.0`, `padroes_mermaid_e_arvore.md`).
  - Enriquecidos todos os `rules/criterios_auditoria.md` com marcadores `[PASS]`/`[FAIL]`/`[UNVERIFIED]` e Módulos `M1..M5` e adicionados casos negativos `should-not-trigger` (*near-misses*) em 100% dos 29 arquivos `evals/evals.json`.
- **Saneamento AST 100% em Todos os Scripts Python (`code_acceptability_auditor.py`)**:
  - Refatorados todos os 22 scripts Python em `skills/**/scripts/*.py` (funções $\le 60$ linhas, zero `except Exception:` genérico, zero blocos `except` silenciosos e tipagem estrita), atingindo **`Status: APPROVED | Quality Score: 100.0/100.0 | Críticas: 0`** em 100% dos scripts do catálogo.

### [2026-10-19] - Fase 17: Eliminação de Redundâncias e Consolidação Modular nas Skills de Criação, Evolução, Aprimoramento e Template (`29/29 PASS`)
- **Fonte Única de Verdade (SSOT) por Módulo em `_template` (`v2.0.0`)**:
  - Criado `skills/_template/references/guardrails_por_modulo.md` consolidando o **Checklist Transversal de Aceite (5 Eixos)** e os **7 Módulos de Guardrails por Domínio** (`M1` Execução/Código/ReAct, `M2` Design/Densidade $\le 35$ palavras, `M3` Frontend/UI `DESIGN.md v4.5-soft`, `M4` Pesquisa/RAG, `M5` Imagem 8 Pilares em Inglês, `M6` Vídeo Temporal em Inglês e `M7` Saúde/Clínica 4 Passos + 6 Pilares).
  - Despoluído o Tier 2 de `_template/SKILL.md` e `refine-prompt/SKILL.md` (`v3.1.0`), removendo blocos duplicados de CSS/paletas do corpo principal e carregando os módulos sob demanda.
- **Alinhamento da Esteira `SkillCraft` (`evoluir-skills` `v2.2.0`, `skill-auditor-refatorador-skills` `v2.2.0`, `skill-creator` `v1.2.0` e `expansao-contexto-adaptativa` `v2.7.0`)**:
  - Eliminada a contradição de estágios entre `SKILL.md` e `rules/` em `evoluir-skills` e sincronizado `rules/criterios_auditoria.md` em `skill-auditor-refatorador-skills`.
  - Atualizado `skill-creator/scripts/new-skill.ps1` para gerar pacotes 100% compatíveis com `validate_skills.py` (com `rules/`, `evals/`, seção de *Gotchas* e orçamento operacional).
  - Adicionados o framework `TASS` e a matriz comparativa completa de frameworks cognitivos (`CoT`, `ToT`, `ReAct`, `Self-Refine / Reflexion`, `DSPy`) em `expansao-contexto-adaptativa`.
- **Engenharia de Agentes e Suíte Matemática Determinística (`aprimoramento-expansibilidade-agentes-skills` `v2.2.0` & `arquiteto-conteudo-solucoes` `v2.3.0`)**:
  - Organizado `references/guia_expansibilidade_e_metricas_2026.md` nos **5 Módulos A..E** (Ontologia & Matriz de Frameworks, Loop Cognitivo de 8 Passos + 5 Camadas de Memória + 11 Modos de Falha, Contratos Pydantic `extra="forbid"` + MCP `2026-07-28`, Theranostic Gate e Auditoria Matemática).
  - Implementado `scripts/agentic_math_and_engine_auditor.py` (`<= 300` linhas) com `PolyExtensibleSkillEngine` (`recovery_hint`), $\text{Pass}@k$ iterativo estável, $D_{\cos} \le 0.18$, $\text{FNR} < 0.001$, $S_{\text{norm}}$ e $\text{TEI}$, além da criação de `references/biblioteca_prompts_enterprise.md` em `arquiteto-conteudo-solucoes`.

### [2026-10-18] - Fase 16: Saneamento Integral `DESIGN.md v4.5-soft`, Deduplicação Global de Skills e Orçamento de Contexto (`29/29 PASS`)
- **Unificação de Tokens `DESIGN.md v4.5-soft` em 100% das Skills**:
  - Eliminados todos os tokens legados de fundo marinho antigo, bordas rígidas de topo e versões antigas em `_template`, `high-level-context-planner`, `gap-analyzer-auditor`, `refine-prompt`, `skill-orquestrador-planos-encadeados`, `test-quality-auditor`, `arquitetura-design-implementacao-sistema`, `skill-auditor-refatorador-skills` e nos 3 arquivos `references/paleta_estilo_melki.md`, padronizando Iluminação Direcional a **135°** (`.ui-card-soft`, `surface-inset`), **Cerulean Sapphire (`#0284C7`)**, zero cobalto e zero bordas duras de `1px`.
- **Deduplicação e Enxugamento de `description` (`<= 300` chars)**:
  - Atualizado `scripts/sync_gemini_ecosystem.py` para desduplicar automaticamente `C:\Users\melki\.gemini\config\skills\` e sincronizar metadados dinâmicos das **29 Skills Canônicas** em `agent_card.json`, `plugin.json`, `CONTEXT.md`, `SPEC.md` e `shared/a2a_bridge.py`.

### [2026-10-18] - Fase 15: Implantação da Skill `code-acceptability-auditor` (`v1.0.0`) — Motor AST + Pydantic v2, Matriz de Gatilhos (`TRIG-01..20`, $F_1 = 1.0$) e `SkillFailureAuditor`
- **Engenharia do Motor de Auditoria de Aceite (`scripts/code_acceptability_auditor.py`)**:
  - Inspeção estática AST e Regex para 10 regras determinísticas (`SYN001`, `SEC001`, `SEC002`, `SEC003`, `ERR001`, `ERR002`, `ERR003`, `TYP001`, `TYP002`, `ARCH001`), cálculo exato do `Quality Score` ($\ge 75.0/100.0$, zero violações críticas) e auto-auditoria `100.0/100.0` em todos os 5 scripts da skill.
- **Avaliação de Roteamento e Modos de Falha (`scripts/trigger_eval_runner.py` & `scripts/skill_failure_auditor.py`)**:
  - Dataset canônico `TRIG-01..20` (`12 train` / `8 validation`, com *Near-Misses* e *Clear Negatives*) atingindo `Accuracy = 100%`, `F1 = 1.0` e `Overfitting = False`; homologada no Eval Harness Go (`dispatch_skill_deterministic_tests`: `Pass@3 = 100%`, `t = 6.71`, `TEI = +0.364`).

### [2026-10-18] - Fase 14: Consolidação do Paradigma Minimalist Impact & Soft Tactile (`DESIGN.md v4.5-soft`), Novas Skills (`frontend-code-architect` v4.0.0, `frontend-testing-auditor` v2.5.0) e Banimento Total de Cobalto por Azuis Minerais (`Cerulean` / `Ocean Sapphire`)
- **Evolução de `design-md` (`v4.5.0`) e Estúdio Interativo (`references/design_md_v4_5_studio.html`)**:
  - Formalização do paradigma **Minimalist Impact & Soft Tactile Elevation (`DESIGN.md v4.5-soft`)**: economia tonal **60-30-10** (60% `canvas`, 30% `surface-base`/`elevated`, $\le 10\%$ acento cirúrgico), **4+1 camadas de elevação** (`canvas`, `surface-inset`, `surface-base`, `surface-elevated`, `surface-floating`), iluminação direcional a **135°**, **Tactile Companion Sidebar** (`256px` em `surface-inset` com pill móvel `#sidebar-active-tracker` em `surface-elevated`), **8 Kits de Componentes `SOFT / SYSTEM`** (`KIT-01`..`KIT-08`) e **Inversão Tonal Recortada (`TERRIXA`)**.
  - **Substituição Integral de Cobalto por Azuis Minerais Calmos**: Banimento estrito de `#0044FF`, `#0057FF`, `#1D4ED8` e `#233DFF`, substituídos por **Cerulean Sapphire (`#0284C7`, hover `#0369A1`)** no preset `slate`, **Ocean Sapphire (`#1E6091`) + Glacier Sky (`#69ADC6`)** no preset `sapphire` (*Soft Sapphire*) e **Mineral Ice (`#38BDF8`)** no `obsidian`.
- **Implantação de Duas Novas Skills Canônicas (`frontend-code-architect` `v4.0.0` e `frontend-testing-auditor` `v2.5.0`)**:
  - `frontend-code-architect` (`v4.0.0`): Arquitetura **Atomic Design em 5 camadas** (`atoms/`, `molecules/`, `organisms/`, `templates/`, `pages/`), desacoplamento `UI vs. Hooks/Services`, tipagem estrita (`strict: true`, zero `any`) e consumo exclusivo de tokens `DESIGN.md v4.5-soft`.
  - `frontend-testing-auditor` (`v2.5.0`): Matriz de testes determinísticos cobrindo as **4 transições de estado (FSM: `idle`, `loading`, `success`, `error`)**, seletores semânticos (`getByRole`), auditoria `jest-axe` WCAG 2.2 AA (`0 violations`) e rubrica determinística **`AUDIT-VIS-01` (0–100 pts)**.
- **Sincronização das Skills de UI (`v2.1.0`) e Subagentes (`agents/ui-*.md` `v1.2.0`)**:
  - Atualizadas `analise-design-tatil-frontend`, `consultor-design-tatil-frontend`, `refatoracao-design-tatil-frontend`, `design-interface-medica-minimalista` (`v2.1.0`), `_template` (`v1.4.0`) e os 4 subagentes da Topologia 3+1 (`ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer` `v1.2.0`).

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
  - `skill-auditor-refatorador-skills` (`v1.2.0` → `v2.1.0`): Sincronizada como Estágio 4 da esteira `SkillCraft`, auditando conformidade com os 3 Tiers, *Trigger Matrix*, extração de scripts de `transcript.jsonl` e os 4 Presets Soft UI + 22 temas minerais (`DESIGN.md v4.5-soft`).
  - `auditoria-projetos-sistema` (`v2.1.0` → `v2.2.0`): Incorporadas as anotações de governança (`AGENTS.md`, desacoplamento Domínio/I-O/UI, tipagem estrita `pydantic.BaseModel`, chunking sanitizado por fronteiras sintáticas com metadados `source_id`/`chunk_index`/`byte_range`, snapshot por aba/menu e subpesos detalhados na rubrica 0–100).

### [2026-10-14] - Fase 5: Sincronização com o Motor Multidimensional do FrontCraft Studio (`DESIGN.md v4.5-soft`)
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
