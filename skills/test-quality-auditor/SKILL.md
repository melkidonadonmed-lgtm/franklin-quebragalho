---
name: test-quality-auditor
description: >-
  Executa auditoria de qualidade, determinismo e eficácia de suítes de testes com 5 módulos (Python, TS/JS, Go, MCP JSON-RPC e Harnesses/Evals). Detecta Green Build Illusion, falhas AAA e asserções tautológicas, classifica testes (Níveis 1-4) e gera grading.json.
license: MIT
metadata:
  version: "1.2.0"
  author: "SkillCraft, Franklin-Main & Melki"
  category: "Auditoria de Qualidade de Testes e Engenharia de Evals"
  updated_at: "2026-10-21"
  tags:
    - "test-quality"
    - "ast-auditor"
    - "go-testing"
    - "mcp-testing"
    - "harness-testing"
    - "mirrored-evals"
    - "aaa-pattern"
    - "mutation-score"
    - "evals"
    - "grading-json"
    - "benchmark-json"
version: 1.2.0
updated_at: 2026-10-21
author: SkillCraft, Franklin-Main & Melki
category: Auditoria de Qualidade de Testes e Engenharia de Evals
---

# `test-quality-auditor` — Auditor Determinístico de Qualidade de Testes & Esteira de Evals (`v1.2.0`) 🛡️

Motor analítico estático e semântico modular (`<300` linhas por módulo) para auditoria de suítes de testes automatizados em **5 domínios especializados** com **espelhamento 1:1 em `evals/modules/*_evals.json`**:

1. **Python (`test_*.py`, `*_test.py`):** Pytest & Unittest via AST ([`scripts/python_ast_auditor.py`](scripts/python_ast_auditor.py) $\leftrightarrow$ [`evals/modules/python_evals.json`](evals/modules/python_evals.json)).
2. **TypeScript / JavaScript (`*.test.ts`, `*.test.js`):** Node Test Runner, Vitest & Jest ([`scripts/ts_js_auditor.py`](scripts/ts_js_auditor.py) $\leftrightarrow$ [`evals/modules/ts_js_evals.json`](evals/modules/ts_js_evals.json)).
3. **Go (`*_test.go`):** Pacote `testing` (`testing.T`), *Table-Driven Tests*, goroutines e Google ADK Go v2 ([`scripts/go_test_auditor.py`](scripts/go_test_auditor.py) $\leftrightarrow$ [`evals/modules/go_evals.json`](evals/modules/go_evals.json) e [`references/modulo_qualidade_testes_go.md`](references/modulo_qualidade_testes_go.md)).
4. **Protocolo MCP (`JSON-RPC 2.0` / `FastMCP` / `StdioServer` / `McpBridge`):** Ciclo de vida `initialize` ➔ `notifications/initialized` ➔ `tools/list` ➔ `tools/call`, códigos `-32601`, decodificação JSON e fronteiras Zero-Trust ([`scripts/mcp_test_auditor.py`](scripts/mcp_test_auditor.py) $\leftrightarrow$ [`evals/modules/mcp_evals.json`](evals/modules/mcp_evals.json) e [`references/modulo_qualidade_testes_mcp.md`](references/modulo_qualidade_testes_mcp.md)).
5. **Harness de Governança & Evals (`shared/harness.py` / `eval_harness.py`):** Guardas semânticas (`SemanticGuard.sanitize_input` / `SecurityViolationError`), *Policy Gates* HITL (`evaluate_action_risk` / `RiskLevel.CRITICAL`), isolamento e ciclo de vida de `CheckpointStore` (`create` ➔ `get` ➔ `update_status` ➔ `clear`) e validação de delta/evidência em `run_eval_harness` ([`scripts/harness_test_auditor.py`](scripts/harness_test_auditor.py) $\leftrightarrow$ [`evals/modules/harness_evals.json`](evals/modules/harness_evals.json) e [`references/modulo_qualidade_testes_harness.md`](references/modulo_qualidade_testes_harness.md)).

Desmascara a **Falsa Sensação de Segurança (*Green Build Illusion*)**, diagnostica nos **7 Módulos** por que um teste passa com código 0 sem proteger a regra de negócio, classifica cada teste no **Espectro de Qualidade (Níveis 1 a 4)** e executa a validação científica via `evals/evals.json` e espelhos `evals/modules/*_evals.json`.

---

## 🎯 Gatilhos de Ativação (Quando Usar)

Ative esta skill quando o usuário solicitar:
- "Audite a qualidade dos testes deste repositório / arquivo (`test_*.py`, `*.test.ts`, `*_test.go`, `test_server.py`, `test_harness_quality.py`)"
- "Analise os testes Go (`testing.T`), testes MCP (`JSON-RPC 2.0` / `FastMCP`) ou testes de Harness (`SemanticGuard`, `CheckpointStore`, `evaluate_action_risk`, `run_eval_harness`) sob o padrão AAA e Dossiê Níveis 1 a 4"
- "Analise qual era o problema do teste, qual foi a abordagem, a montagem AAA e por que funcionou mas não resolveu o problema"
- "Detecte falsos positivos, asserções tautológicas (`assert True`), superficiais (`is not None`, `if res == nil`), erros descartados em Go (`res, _ := sut()`), `t.Fatal` em goroutines, handshake MCP `stdio` incompleto ou testes de Harness sem `pytest.raises(SecurityViolationError)` / `RiskLevel.CRITICAL`"
- "Execute os módulos espelhados de Evals (`evals/modules/*_evals.json`) gerando `grading.json` e `benchmark.json` por módulo e consolidado"

---

## 🚫 Limites, Exceções e Fronteira da Esteira de 3 Portões (`2026-10-21`)

- **Fronteira na Esteira de Qualidade e Convergência (3 Portões)**:
  1. **Portão 1 — Código de Produção (`code-acceptability-auditor` `v1.1.0`)**: Audita arquivos Python de aplicação/domínio via AST e Pydantic (`12` regras: `SEC001..003`, `SYN001`, `ERR001..003`, `TYP001..002`, `ARCH001..003`, `Score >= 75.0`).
  2. **Portão 2 — Suítes de Testes & Evals (`test-quality-auditor` `v1.2.0` — Esta Skill)**: Audita a eficácia, padrão AAA, falsificabilidade e determinismo de testes (`Python`, `TS/JS`, `Go`, `MCP JSON-RPC` e `Harness`) + telemetria estatística PerfKit (`perfkit_stats.py`: $P_{50}..P_{99.9}$, `stddev` `ddof=1`, `geomean`), exigindo Nível 4 (`81–100 pts`).
  3. **Portão 3 — RCA & Convergência Spec-to-Code (`gap-analyzer-auditor` `v2.1.0`)**: Quando os Portões 1 ou 2 reprovam um artefato ou ocorrem falhas de runtime/divergências em `SPEC.md`/`tasks.md`, consome as evidências factuais para RCA epistêmico (`[FATO]`, `[INFERÊNCIA]`, `[LACUNA]`) e convergência *append-only* (`/speckit-converge`).
- **Não usar** para auditoria matemática exclusiva de motores de Física 3D/WebGL sem relação com suítes de testes ou Evals (use `code-quality-audit-3d-physics`).
- **Não usar** para compilar binários Go ou fazer deploy de containers no Cloud Run sem auditoria de testes.
- **Não usar** para auditoria estrutural de pastas do Google Drive ou limpeza de disco Windows (use `gdrive-auditoria-limpeza` ou `manutencao-disco-windows`).
- **Não aprovar** suítes de testes baseando-se apenas em cobertura de linhas (*Line Coverage*) ou retorno `Exit Code 0` sem inspecionar a densidade e rigor das asserções.

---

## 📥 Entradas e Pré-requisitos

- **`target_path` (obrigatório):** Caminho do arquivo de teste (`tests/test_server.py`, `*.test.ts`, `*_test.go`, `tests/test_harness_quality.py`), diretório de testes (`tests/`, `go_agent/`) ou manifesto `evals/evals.json`.
- **`domain` (opcional):** `auto` (padrão — detecta linguagem e enriquece automaticamente testes MCP e Harness), `python`, `ts`, `go`, `mcp` ou `harness`.
- **`eval_module` (opcional com `--run-evals`):** `all` (padrão — executa os 5 espelhos em `evals/modules/` + manifesto consolidado de 20 casos), `python`, `ts_js`, `go`, `mcp` ou `harness`.

---

## 🔄 Processamento Interno e Fluxo de Execução (7 Módulos)

Toda auditoria conduzida por esta skill executa o pipeline determinístico em **7 Módulos Sequenciais** (detalhados em [`references/dossie_qualidade_testes_e_evals.md`](references/dossie_qualidade_testes_e_evals.md), [`references/modulo_qualidade_testes_go.md`](references/modulo_qualidade_testes_go.md), [`references/modulo_qualidade_testes_mcp.md`](references/modulo_qualidade_testes_mcp.md) e [`references/modulo_qualidade_testes_harness.md`](references/modulo_qualidade_testes_harness.md)):

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│          PIPELINE DO AUDITOR DE QUALIDADE DE TESTES & EVALS ESPELHADOS (v1.2.0)     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Passo 1: Varredura Modular via scripts/test_quality_auditor.py                      │
│   ├── python_ast_auditor.py   <-> evals/modules/python_evals.json                   │
│   ├── ts_js_auditor.py        <-> evals/modules/ts_js_evals.json                    │
│   ├── go_test_auditor.py      <-> evals/modules/go_evals.json                       │
│   ├── mcp_test_auditor.py     <-> evals/modules/mcp_evals.json                      │
│   ├── harness_test_auditor.py <-> evals/modules/harness_evals.json                  │
│   └── perfkit_stats.py        --> Percentis P50..P99.9, stddev (ddof=1) & geomean   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Passo 2: Diagnóstico da Problemática (Problema ➔ Abordagem ➔ Meta)                 │
│ Passo 3: Dissecação da Montagem AAA (Arrange ➔ Act ➔ Assert)                       │
│ Passo 4: Análise de Falha Tautológica (Por que passou vs. Por que falhou)           │
│ Passo 5: Fatores de Persistência (Erros '_', Goroutines, MCP, Harness HITL...)     │
│ Passo 6: Espectro Geral e Dossiê Individualizado (Níveis 1 a 4 | Nota 0-100)        │
│ Passo 7: Correção Cirúrgica (Nível 4) + Execução dos Espelhos em evals/modules/     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Passo 1: Execução do Motor Modular (`test_quality_auditor.py`)
Dispare o script utilitário sobre qualquer arquivo ou diretório (Python, TS/JS, Go, MCP ou Harness):
```powershell
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py <caminho_alvo> --markdown
```
Para forçar um domínio específico (`go`, `mcp` ou `harness`):
```powershell
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py <caminho_alvo> --domain go --markdown
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py <caminho_alvo> --domain mcp --markdown
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py <caminho_alvo> --domain harness --markdown
```
Para validar todos os 5 módulos espelhados (`evals/modules/*_evals.json`) + a suíte consolidada (20 casos) ou um módulo isolado:
```powershell
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py --run-evals
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py --run-evals --eval-module harness
```

### Passo 2: Análise Estrutural dos 7 Módulos Obrigatórios
1. **Diagnóstico da Problemática do Teste:** Explicite **O Problema** (*Green Build / Green Go Test / Green MCP / Green Harness Illusion*), **A Abordagem** (Auditoria de Integridade de Asserção, Erros, Protocolo JSON-RPC, Guardas HITL e Isolamento) e **O Que Esperava Conseguir** (*Mutation Score High* / Guardrails Determinísticos).
2. **Análise da Montagem e Seus Elementos (Padrão AAA):**
   - **Em Go (`*_test.go`):** `1. ARRANGE` (`t.TempDir()`, `t.Setenv()`, `t.Cleanup()`), `2. ACT` (captura explícita `res, err := sut()` sem `_`), `3. ASSERT` (`if err != nil { t.Fatalf(...) }`, `errors.Is`, campos de negócio).
   - **Em MCP (`JSON-RPC 2.0` / `FastMCP`):** `1. ARRANGE` (isolamento e sequência JSON-RPC), `2. ACT` (`initialize` ➔ `notifications/initialized` sem `id` ➔ `tools/list` ➔ `tools/call`), `3. ASSERT` (`json.loads`/`json.Unmarshal`, nomes canônicos de tools, erro `-32601` e bloqueio Zero-Trust `BLOCKED`).
   - **Em Harness (`SemanticGuard` / `CheckpointStore` / `Eval Harness`):** `1. ARRANGE` (`CheckpointStore(tmp_path / "chk.json")`, payloads adversários de injeção e matriz de risco), `2. ACT` (`sanitize_input`, `evaluate_action_risk`, `create` ➔ `get` ➔ `update_status` ➔ `clear`, `run_eval_harness`), `3. ASSERT` (`pytest.raises(SecurityViolationError)`, `RiskLevel.CRITICAL`, persistência isolada e `pass_rate_gain > 0`).
3. **Análise do que o Teste Propõe (Falha Tautológica):** Demonstre tecnicamente **por que o teste funcionou** (`Exit Code 0`) e **por que NÃO resolveu o problema**.
4. **Por que o Problema Ainda Persiste (Fatores de Interferência):** Mapeie descartes de erro (`SILENCED_ERROR_IN_TEST`), `t.Fatal` em goroutines (`UNSAFE_GOROUTINE_FATAL`), handshake MCP incompleto (`MCP_INCOMPLETE_STDIO_HANDSHAKE`), JSON sem parse (`MCP_TAUTOLOGICAL_RAW_RESPONSE`), guarda de Harness sem exceção (`HARNESS_WEAK_INJECTION_GUARD_TEST`), risco destrutivo não verificado (`HARNESS_UNVERIFIED_RISK_TRANSITION`), checkpoints sem isolamento (`HARNESS_MISSING_TEARDOWN_CLEANUP`) e ciclo HITL incompleto (`HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE`).
5. **Espectro Geral e Dossiê por Qualidade (Níveis 1 a 4):**
   - **Nível 1 — Ilusório / Placebo (`0 – 25 pts`):** Sem asserções, `assert True`, `try/except: pass`, erro Go descartado com `_` + checagem apenas de `nil`, payload MCP sem parse, ou teste de Harness sem exigir `SecurityViolationError` e `RiskLevel.CRITICAL`.
   - **Nível 2 — Superficial / Frágil (`26 – 50 pts`):** Checagens rasas (`is not None`, `if res == nil`), `t.Fatal` dentro de goroutine, chamada MCP `stdio` sem handshake, ou `CheckpointStore` poluindo arquivo global sem validar transição de status.
   - **Nível 3 — Funcional Rígido (`51 – 80 pts`):** Valida caminho feliz com valores exatos, mas possui `os.Setenv` sem `t.Cleanup`, descoberta `tools/list` apenas por `len > 0` ou `run_eval_harness` sem checar `pass_rate_gain`/`evidence`.
   - **Nível 4 — Determinístico & Resiliente (`81 – 100 pts`):** Padrão AAA estrito, isolamento completo (`try/finally`, `tmp_path`, `t.TempDir()`, `t.Cleanup()`), validação de exceções/erros (`pytest.raises`, `errors.Is`, JSON-RPC `-32601`, `SecurityViolationError`) e contratos estritos.
6. **Correção Cirúrgica:** Apresente e aplique a refatoração elevando testes de Nível 1–3 para o **Nível 4**, reexecutando o auditor e o test runner (`pytest`, `go test ./...`, `node --test`) para comprovar `100% PASS`.
7. **Esteira de Evals Espelhados (*Mirrored Eval-Driven Harness*):** Execute [`scripts/eval_harness.py`](scripts/eval_harness.py) sobre `evals/modules/*_evals.json` e `evals/evals.json`, emitindo `evals/workspace/iteration-1/modules/<mod>_grading.json`, `<mod>_benchmark.json`, `grading.json` e `benchmark.json`.

---

## 🎨 Diretrizes de Estilo por Propósito e Arquitetura Visual (`preferencias_estilo_e_temas.md` & `minimal-impact-ui`)

Sempre que esta skill gerar relatórios visuais, dashboards HTML de cobertura/qualidade ou artefatos de interface, aplique obrigatoriamente os 4 módulos orientados ao **propósito do projeto** ([`../_template/references/preferencias_estilo_e_temas.md`](../_template/references/preferencias_estilo_e_temas.md) e [`../minimal-impact-ui/SKILL.md`](../minimal-impact-ui/SKILL.md)):

### Módulo 1: Seleção de Tema pelo Propósito e Isolamento 98/2 (`DESIGN.md v5.0`)
- **4 Famílias Atmosféricas Adaptativas**:
  1. **Cinza sobre Cinza Monolítico (Padrão Anti-TDAH para Dashboards de QA)**: Canvas `#57545d`, Cards `#49464f` e Menus/Pílulas `#8e8999` com **tinta escura `#16151A`** ($\ge 5.6:1$ AAA).
  2. **Preto Terminal IBM (`Ex Umbris` — Telemetria CLI/AST)**: Canvas `#070709`, Cards `#101014` ($L_{\text{card}} > L_{\text{canvas}}$) e tipografia obrigatória **`IBM Plex Sans` + `IBM Plex Mono`**.
  3. **Ad Lucem (Editorial / Relatórios de Homologação)**: Canvas `#F3F3F5` / `#F4F3EF`, Cards `#FFFFFF` e bloco de resumo executivo `#18181C`.
  4. **AETHER 2027**: Tokens `oklch()`, Bento Grid 12 colunas e *Spring Physics*.
- ❌ **Banimento Anti-Cobalto & Anti-Ruído (`AUDIT-VIS-01`):** Proibido azul cobalto puro (`#0044FF`, `#0057FF`, `#1D4ED8`, `#2563EB`), texto vermelho corrido em fundos cinzas/escuros (usar `.highlight-surgical`) e emojis decorativos em controles.

### Módulo 2: Camadas Esculpidas, Regra 1+2 e Tipografia Tabular (`tabular-nums`)
- **Superfícies Esculpidas**: Sombra física em 3 camadas (`--shadow-sculpted`) + `1px` Rim Light superior (`inset 0 1px 0 0 var(--rim-light)`).
- **Orçamento de Densidade (Regra 1+2 e $\ge 25\%$ de Respiro)**: No máximo **1 ação primária** e **2 secundárias** visíveis por card, com `font-variant-numeric: tabular-nums` obrigatório em todas as colunas de notas (`0–100`), percentis ($P_{50}, P_{95}, P_{99}$) e contagens de asserções.
- **Anti-Squish e Ergonomia TDAH**: Hierarquia escaneável em 3 segundos, badges com `flex-shrink: 0; white-space: nowrap;`, alvos interativos $\ge 44\times44\text{px}$ e zero `alert()` bloqueante.

### Módulo 3: Mapeamento de Opções e Arquitetura Modular (`<300` linhas/módulo)
- **Consulta Estruturada via `ask_question`:** Apenas em decisões destrutivas ou ambiguidades críticas (máx. 1–2 perguntas).
- **Arquitetura de Código:** Separação limpa em módulos de responsabilidade única (`<300` linhas cada, `100.0/100.0` no `code-acceptability-auditor`): Domínio ([`scripts/models.py`](scripts/models.py)), Analisadores ([`scripts/python_ast_auditor.py`](scripts/python_ast_auditor.py), [`scripts/ts_js_auditor.py`](scripts/ts_js_auditor.py), [`scripts/go_test_auditor.py`](scripts/go_test_auditor.py), [`scripts/mcp_test_auditor.py`](scripts/mcp_test_auditor.py), [`scripts/harness_test_auditor.py`](scripts/harness_test_auditor.py)), Estatística PerfKit ([`scripts/perfkit_stats.py`](scripts/perfkit_stats.py)), Evals ([`scripts/eval_harness.py`](scripts/eval_harness.py)) e CLI ([`scripts/test_quality_auditor.py`](scripts/test_quality_auditor.py)), com espelhamento 1:1 em `evals/modules/*_evals.json`.

### Módulo 4: Matriz de Detecção de Discrepâncias com as Preferências
- Checklist determinístico validado em toda entrega:
  * `[PASS / FAIL]` **Zero Exceção/Erro Silenciado (`except: pass` / `res, _ :=`):** Todos os blocos de erro nos testes e scripts tratam ou validam falhas explicitamente?
  * `[PASS / FAIL]` **Tipagem Estrita e Desacoplamento (<300 linhas):** Todos os módulos em `scripts/` possuem `<300` linhas e contratos `dataclass` estritos?
  * `[PASS / FAIL]` **Falsificabilidade Real Multi-Domínio (Python/TS/Go/MCP/Harness):** As asserções validam comportamento real, invariantes de negócio, protocolo JSON-RPC 2.0 e guardas HITL Zero-Trust?
  * `[PASS / FAIL]` **Espelhamento 1:1 de Evals (`scripts/*_auditor.py` $\leftrightarrow$ `evals/modules/*_evals.json`):** Todos os 5 módulos possuem suíte de eval espelhada validada com `100% PASS`?

---

## 📤 Saídas e Entregáveis (Modelo de Saída)

A resposta final da skill deve conter obrigatoriamente:
1. **Dossiê Executivo nos 7 Módulos (Python, TS/JS, Go, MCP ou Harness):** (1) Diagnóstico da Problemática, (2) Montagem AAA, (3) Análise de Falha Tautológica, (4) Fatores de Persistência, (5) Espectro Geral e Tabela do Dossiê por Teste (Níveis 1 a 4), (6) Correção Cirúrgica Antes vs. Depois e (7) Relatório de Evals Consolidado e por Módulo Espelhado (`grading.json` / `benchmark.json`).
2. **Veredito Determinístico do Script Modular:** Saída comprovada de `scripts/test_quality_auditor.py` com pontuação individual e global (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).
3. **Links Clicáveis `file:///`:** Apontamento direto para todos os arquivos de teste auditados, refatorados e artefatos gerados.
