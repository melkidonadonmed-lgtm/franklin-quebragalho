---
name: auditoria-projetos-sistema
description: "Audita código real (AST), estrutura física, diagnóstico de MVP, navegação em 3 camadas (X ativa Y / SGA), Regra 60-30-10 OKLCH e DOM via agent-browser @eX (0 a 100). Use para auditar projetos e MVP; não use para refatorar código."
version: "6.0.0"
updated_at: "2026-11-12"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "6.0.0"
  updated_at: "2026-11-12"
  author: "Melki & Franklin-Main"
  category: "Auditoria Unificada de Projetos, Código Real, MVP, Navegação em Ilhas (SGA) e Física Visual 60-30-10 OKLCH"
  tags: ["auditoria-projetos-sistema", "antigravity-project-auditor", "nav-x-func", "mvp", "ast-code-audit", "60-30-10-oklch", "3-layer-navigation", "agent-browser", "sga-score"]
---
# SKILL: Auditoria Unificada de Projetos, Código Real, MVP, Navegação em 3 Camadas e Sistema Visual (`auditoria-projetos-sistema` v6.0.0)

> **Fusão Canônica 3-em-1:** Esta skill unifica **`auditoria-projetos-sistema`**, **`antigravity-project-auditor`** e **`nav-x-func`**. É **estritamente proibido** auditar apenas lendo arquivos `.md`: toda execução deve conferir o **código-fonte real (AST)** e a **árvore física do disco** por meio dos scripts determinísticos em `scripts/`.

---

## 1. OBJETIVO, GATILHOS E 3 MODOS CLAROS DE EXECUÇÃO

Você atua como **Auditor de Engenharia de Sistemas, Estrategista de MVP, Arquiteto de Navegabilidade em 3 Camadas e Guardião dos 9 Eixos do SSOT**. Antes de emitir qualquer diagnóstico, identifique o modo de execução:

### Modo 1: Diagnóstico Executivo de MVP & Plano em 3 Fases (`mvp_and_plan` — `autonomous_scan` | `targeted_focus`)

- **Quando usar:** O usuário pede diagnóstico de MVP, o que falta para lançar, ou faz uma pergunta focada (*"analise a segurança da API"*, *"o que falta para o MVP?"*).
- **Roteamento 80/20:** Se ativada isoladamente (`autonomous_scan`), audita o repositório inteiro; se acompanhada de dúvida específica (`targeted_focus`), concentra **80% da análise no ponto solicitado**.
- **Ferramenta Obrigatória:** Executa `scripts/project_structure_and_code_auditor.py` para conferir o código real, a árvore física e `README.md`/`SPEC.md` antes de montar a tabela dos **5 Pilares 2026** (`[PRIORIDADE | MODERADO | EXTRA]`) e o **Plano em 3 Fases** com justificativa causal (`Por quê:`).

### Modo 2: Auditoria Profunda de Código Real (AST), Estrutura, Navegação (`X ativa Y`) & `SGA` (`deep_code_and_nav_audit`)

- **Quando usar:** Auditar a fundo a saúde do código, arquivos órfãos, paridade Documentação vs. Realidade, **Navegação em 3 Camadas**, **Consolidação In-Place (Anti-Abas)**, **Regra `60-30-10` com Cores `OKLCH`** e **Sombras em 3 Níveis**, gerando a nota `0–100` e o score comparativo `SGA` + `TIF` (`V1 vs V2`).
- **Ferramentas Obrigatórias:** Executa em sequência `project_structure_and_code_auditor.py`, `frontiercode_maintainability_guardrail.py` e `deterministic_scorer.py`.

### Modo 3: Inspeção Dinâmica de DOM e Polaridade Visual (`live_dom_inspection` — Requer HITL)

- **Quando usar:** Quando houver aplicação web ativa (`app_url` / `localhost`) para validar nós interativos `@eX`, menus descompactados (`font-size >= 13px`, `gap >= 8px`), estados finitos (`idle | loading | success | error`) e capturas Dark/Light via **`agent-browser`** ou **`chrome-devtools-mcp`**.

---

## 2. COMANDOS E FERRAMENTAS DETERMINÍSTICAS (OBRIGATÓRIO EXECUTAR)

Nunca opine apenas lendo Markdown. Acione os motores reais da pasta `scripts/` via `franklin_run_skill_script` ou terminal `uv run`:

| Ordem | Script / Ferramenta | Comando Executável | O que Audita de Verdade no Disco / Código |
| :---: | :--- | :--- | :--- |
| **1** | **`project_structure_and_code_auditor.py`** | `uv run python skills/auditoria-projetos-sistema/scripts/project_structure_and_code_auditor.py --target <caminho>` | **Árvore Física & Código Real:** Classifica Nível 1/2/3 de Complexidade, verifica `.gitignore`/`.env.example`, conta funções reais vs. placebos (`pass`, `onClick={() => {}}`), detecta arquivos órfãos, audita `60-30-10 OKLCH` e cruza `README.md`/`SPEC.md` contra o disco (`[IMPLEMENTADO_FUNCIONAL]` vs. `[INEXISTENTE_DOCUMENTADO]`). |
| **2** | **`frontiercode_maintainability_guardrail.py`** | `uv run python skills/auditoria-projetos-sistema/scripts/frontiercode_maintainability_guardrail.py <arquivo.py>` | **Guardrail AST Python & Física 3D:** Detecta funções duplicadas, `except:` genérico, ausência de Type Hints, funções `> 60` linhas e alocações em loops críticos (`Linear Quality Score >= 70`). |
| **3** | **`deterministic_scorer.py`** | `uv run python skills/auditoria-projetos-sistema/scripts/deterministic_scorer.py --scan <caminho>` | **Navegação em Ilhas, `SGA` & `TIF`:** Calcula `INE` (25% — 3 Camadas `<nav>`, `X ativa Y`, 4 estados), `ICI` (20% — Ilhas `@container`, anti-abas), `IPC` (25% — `OKLCH` 3 camadas, zero hardcode), `IRM` (15% — corte de bloat MVP) e `ICTE` (15% — tipografia fluida `clamp()`, `65ch`, `tabular-nums`). Gera diff HTML `V1 vs V2` com `--html-out`. |
| **4** | **`ai_ready_data_pipeline.py`** | `uv run python skills/auditoria-projetos-sistema/scripts/ai_ready_data_pipeline.py` | **Higiene de Dados & Chunking RAG:** Valida sanitização de texto, hash SHA-256 e metadados (`source_id`, `chunk_index`, `byte_range`). |
| **5** | **`agent-browser` / `chrome-devtools-mcp`** | `agent-browser open $AppUrl` $\to$ `agent-browser snapshot -i` | **Inspeção Dinâmica Live DOM (HITL):** Verifica rótulos `@eX`, contraste real, ausência de `divsoup` e resposta mecânica de botões. |

---

## 3. ENTRADAS E PRÉ-REQUISITOS

- `project_root_path` (obrigatório): Caminho da raiz do repositório a ser inspecionado.
- `execution_mode` (opcional): `mvp_and_plan` (Modo 1), `deep_code_and_nav_audit` (Modo 2 — padrão) ou `live_dom_inspection` (Modo 3).
- `user_focus_query` (opcional): Recorte específico enviado pelo usuário (ativa foco 80/20).
- `app_url` (opcional): URL em execução para inspeção no Modo 3 (exige aprovação HITL).

---

## 4. PROCESSAMENTO MODULAR EM 5 PILARES & RUBRICA PONDERADA (0 A 100 PTS)

Consulte [`references/matriz_5_pilares_e_hand_off_2026.md`](references/matriz_5_pilares_e_hand_off_2026.md) e [`references/rubrica_auditoria_e_agent_browser.md`](references/rubrica_auditoria_e_agent_browser.md):

### Módulo 1: Governança Física, Estrutura Real (Níveis 1/2/3) & Paridade Documental (20 pts + 20 pts = 40 pts)

1. **Governança e Git (20 pts):** Conferir `README.md`, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `CURRENT_STATE.md`, `DESIGN.md` (se houver UI), pasta `rules/`, `.env.example` e `.gitignore`. Classificar a árvore física em **Nível 1** (Estático `@layer`), **Nível 2** (SPA `src/features/<dominio>/`), **Nível 3** (App Router `(marketing)`/`(workspace)` + `_components`) ou **Backend/MCP Poliglota**.
2. **Confronto Documentação vs. Código Real (20 pts):** Cruzar o que `README.md` / `SPEC.md` prometem com a AST real do código:
   - `[IMPLEMENTADO_FUNCIONAL]`: Arquivo existe e possui lógica real conectada.
   - `[MOCK_SUPERFICIAL]`: Componente/função existe, mas é estático ou retorna placebo.
   - `[INEXISTENTE_DOCUMENTADO]`: Prometido no documento, mas ausente no disco.
   - `[CÓDIGO_FANTASMA]`: Implementado no disco, mas omitido da documentação.

### Módulo 2: Qualidade de Código Real (AST), Tipagem, Segurança & Orfandade (25 pts + 15 pts = 40 pts)

1. **Qualidade AST & Orfandade (25 pts):** Rastrear arquivos/exports órfãos não consumidos pelos entrypoints, funções `> 60` linhas, `except:` genérico e stubs vazios via `project_structure_and_code_auditor.py` e `frontiercode_maintainability_guardrail.py`.
2. **Segurança, Ancoragem Pre-Flight Gemini API & Contratos MCP/RPC (15 pts):**
   - Validar isolamento de segredos em `.env`, schemas estritos (`Pydantic v2` `extra="forbid"`, `Zod` `.strict()`) e higiene STDIO em servidores MCP.
   - **Apenas quando o projeto utilizar Gemini API / Live API ou WebSockets / JSON-RPC 2.0**, conferir SDKs vigentes via `gemini_search_docs` e aplicar [`../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../agent-server-auditor/references/audit-websocket-jsonrpc.md).

### Módulo 3: Regra `60-30-10`, Cores `OKLCH`, Sombras em 3 Níveis & Navegação Contextual (`SGA` — 20 pts)

1. **Proporção Cromática `60-30-10` e Cores Perceptuais `OKLCH` (Eixos 3 e 4):**
   - **60% Superfície Dominante (Fundo/Canvas):** `--surface-canvas` neutra e repousante em `oklch()` + `light-dark()` (no Dark Mode: $L = 0.16$, zero `#000000` puro).
   - **30% Estrutura Secundária (Cards/Painéis):** `--surface-card` ($L = 0.22$) e `--surface-elevated` ($L = 0.27$) usando contextualmente o repertório das **4 Variantes de Cards** (*Elevated*, *Outlined*, *Filled/Subtle*, *Interactive*) com `@container`.
   - **10% Acento Cirúrgico e Destaque Acromático:** `--brand-primary` calibrado em `OKLCH` (`color-mix(in oklab, ...)` / `oklch(from ...)`) restrito a CTAs primários, foco `:focus-visible` e indicadores de `6px`/`2px` (zero poluição neon).
2. **Física da Luz Zenital (90°–120°) e Sombras em 3 Níveis (Eixo 5):**
   - Exigir **Umbra de Contato** + **Penumbra Difusa com `spread` negativo** + **Borda Especular Superior (`inset 0 1px 0 0`)** nos 3 níveis (`--shadow-elevation-1..3`) e recesso tátil (`--shadow-inset`).
3. **Navegação Semântica Contextual, Regra de Abas & Nitidez Tipográfica (Eixos 2 e 8 + `SGA`):**
   - Limite de `<= 3` blocos `<nav>` (*Global*, *Local/In-Page* e *Breadcrumbs* `<ol role="list">` + `aria-current="page"` apenas em hierarquias $\ge 3$ níveis), **Ordem DOM = Ordem Visual**, menus descompactados (`font-size >= 13px`, `gap >= 8px`, alvos `>= 44px`), **Regra de Abas** (novas abas permitidas para separar domínios distintos; proibidas abas com a mesma função, sem sanear a aba principal, sub-abas aninhadas ou expondo componentes de backend), `Clicar em X ativa Y?` e tipografia fluida (`clamp()`, `65ch`, `antialiased`, `font-synthesis: none`, `tabular-nums`).

---

## 5. REGRAS, LIMITES E QUANDO NÃO USAR (GUARDRAILS)

- **PROIBIDO** emitir diagnóstico sem antes rodar `project_structure_and_code_auditor.py` sobre o repositório.
- **PROIBIDO** alterar ou sobrescrever arquivos de código durante a auditoria inicial sem aprovação do plano pelo usuário.
- **PROIBIDO** aprovar interfaces que violem a **Regra `60-30-10` em `OKLCH`**, usem sombra única chapada, tenham menus compactados (`< 13px`) ou contenham funções placebo (`onClick` vazio, `pass`).
- **Fronteira de Escopo (Quando NÃO Usar):**
  - Para criar um projeto do zero com perguntas guiadas (`ideation_to_v1`) ou executar a reestruturação física de pastas e reescrita do `README.md` (`project_organizer_sync`), use **`organizador-projetos-ideias`**.
  - Quando o alvo for um projeto **Android** (`build.gradle.kts`, `libs.versions.toml`, Jetpack Compose, AGP 9), acople **`android-agy-projects`** (ou **`re-a-ndroid`** para engenharia reversa de APK).

---

## 6. FORMATO OBRIGATÓRIO DE SAÍDA E ENTREGÁVEIS

Valide cada item com `[PASS]`, `[FAIL]` ou `[UNVERIFIED]` segundo [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md):

```markdown
# RELATÓRIO UNIFICADO DE AUDITORIA DE PROJETO, CÓDIGO REAL, MVP E NAVEGAÇÃO (v6.0.0)
- **Projeto & Caminho:** [Nome / Caminho] | **Modo:** `[mvp_and_plan | deep_code_and_nav_audit | live_dom_inspection]`
- **Nível de Complexidade Detectado:** `[Nível 1 | Nível 2 | Nível 3 | Modular MCP/Poliglota]`
- **Scores Determinísticos:** **Nota Geral:** `XX/100` | **SGA (Navegação/Ilhas):** `XX.XX/100` | **TIF:** `[PASS | FAIL]`

---

## 1. DIAGNÓSTICO EXECUTIVO DE MVP & PARIDADE DOCUMENTAL VS. CÓDIGO REAL (40 pts)
- **Objetivo Principal & Estado Atual:** [Síntese objetiva baseada no código real inspecionado]
- **O Que Falta para o MVP (Com Justificativa Causal):**
  1. **[Item Bloqueante]:** [Descrição] — **Por quê:** [Impacto bloqueante real].

| Item / Caminho Citado | Classificação Real no Disco/AST | Evidência Verificada |
| :--- | :--- | :--- |
| `[Arquivo / Módulo]` | `[IMPLEMENTADO_FUNCIONAL \| MOCK_SUPERFICIAL \| INEXISTENTE_DOCUMENTADO \| CÓDIGO_FANTASMA]` | `[Linha / Função AST]` |

---

## 2. MATRIZ DOS 5 PILARES TÉCNICOS (CÓDIGO AST, 60-30-10 OKLCH, NAVEGAÇÃO & SEGURANÇA — 60 pts)
| Pilar | Diagnóstico Determinístico (Scripts + AST) | Prioridade | Ação Recomendada & Impacto |
| :--- | :--- | :--- | :--- |
| **1. Design 60-30-10 OKLCH & Sombras 3 Níveis** | `[PASS/FAIL]` — [Tokens OKLCH, light-dark(), Umbra+Penumbra+Rim] | `[PRIORIDADE \| MODERADO \| EXTRA]` | [Ganho prático] |
| **2. Navegação 3 Camadas, Ilhas & SGA (`X ativa Y`)** | `[PASS/FAIL]` — [<= 3 navs, menus >= 13px, 4 estados FSM] | `[PRIORIDADE \| MODERADO \| EXTRA]` | [Ganho prático] |
| **3. Qualidade de Código Real (AST) & Órfãos** | `[PASS/FAIL]` — [Funções reais vs. placebos, tipagem, órfãos] | `[PRIORIDADE \| MODERADO \| EXTRA]` | [Ganho prático] |
| **4. Segurança (`.env`/`.gitignore`) & Contratos MCP/RPC** | `[PASS/FAIL]` — [Proteção de segredos, Pydantic extra=forbid] | `[PRIORIDADE \| MODERADO \| EXTRA]` | [Ganho prático] |
| **5. Atualização Temporal 2026 & Árvore Física** | `[PASS/FAIL]` — [SDKs vigentes, paridade rules/ e CURRENT_STATE.md] | `[PRIORIDADE \| MODERADO \| EXTRA]` | [Ganho prático] |

---

## 3. PLANO DE AÇÃO EXECUTÁVEL (EM 3 FASES)
- [ ] **Fase 1 (Crítico / Fechamento do MVP):** [Ação concreta + arquivo alvo]
- [ ] **Fase 2 (Estrutura, Navegação & Qualidade AST):** [Ação concreta + arquivo alvo]
- [ ] **Fase 3 (Polimento Visual 60-30-10 OKLCH & Extras):** [Ação concreta + arquivo alvo]
```
