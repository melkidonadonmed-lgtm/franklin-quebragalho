# Dossiê Canônico de Auditoria de Qualidade de Testes e Engenharia de Evals (`test-quality-auditor` v1.2.0)

Este documento consolida a fundamentação técnica, matrizes diagnósticas e arquitetura de *Eval-Driven Harness* utilizadas pela skill `test-quality-auditor`.

---

## 1. Diagnóstico da Problemática do Teste

| Dimensão | Análise Crítica do Problema e Abordagem |
| :--- | :--- |
| **O Problema** | **Falsa Sensação de Segurança (*Green Build Illusion*):** Agentes de IA e desenvolvedores frequentemente geram suítes de teste que passam em 100% das execuções (*green builds*), mas são incapazes de capturar regressões reais em produção. O código de teste executa a função sob análise, mas contém asserções fracas, mocks tautológicos, vazamento de estado global ou captura de exceções que mascaram falhas. |
| **A Abordagem** | **Auditoria de Integridade da Asserção e Determinismo:** Em vez de avaliar apenas a cobertura de linhas (*Line Coverage*), o auditor inspeciona a qualidade e rigor das asserções via AST, o isolamento do estado (`try/finally` e fixtures), o nível de mock dos componentes e a imunidade ao não-determinismo (tempo real, ordem de execução e concorrência). |
| **O Que Esperava Conseguir** | **Garantir a Eficácia do Teste (*Mutation Score High*):** Transformar testes superficiais em **Guardrails Determinísticos**, onde qualquer alteração indesejada na regra de negócio quebre imediatamente a suíte de testes (eliminando falsos positivos). |

---

## 2. Análise da Montagem e Seus Elementos (Padrão AAA)

Um teste automatizado de alta qualidade exige o cumprimento estrito do padrão **Arrange-Act-Assert (AAA)**. A degradação ocorre quando os elementos dessa montagem são corrompidos:

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                    MONTAGEM DO TESTE (PADRÃO AAA)                         │
├───────────────────┬───────────────────────────────────────────────────────┤
│ 1. ARRANGE        │ • Configuração de massa de dados determinística       │
│ (Preparação)      │ • Mocking isolado APENAS de I/O externa (banco/rede)  │
│                   │ • Preservação do estado global para teardown seguro   │
├───────────────────┼───────────────────────────────────────────────────────┤
│ 2. ACT            │ • Invocação pontual da unidade ou contrato sob teste  │
│ (Execução)        │ • Captura do resultado e de exceções sem mascarar     │
├───────────────────┼───────────────────────────────────────────────────────┤
│ 3. ASSERT         │ • Asserção estrita de valores de retorno              │
│ (Verificação)     │ • Validação de efeitos colaterais e contratos de tipo │
└───────────────────┴───────────────────────────────────────────────────────┘
```

### Elementos Críticos Inspecionados na Montagem:
1. **Qualidade do Arranjo (*Arrange*):** Mocks instalados diretamente na lógica interna da unidade sob teste corrompem a validação, fazendo o teste testar o próprio mock em vez do código real. Além disso, mutações em objetos globais (`globalThis.window`, `globalThis.fetch`, `os.environ`) sem bloco `try/finally` contaminam os testes subsequentes.
2. **Escopo da Ação (*Act*):** Invocar múltiplas funções mutáveis independentes no mesmo bloco de teste sem isolamento impede identificar a causa raiz imediata quando o teste quebra.
3. **Rigidez da Asserção (*Assert*):** A asserção é o único elemento que garante a validade do teste. Testes sem `assert`, com asserções tautológicas (`assert True`) ou puramente superficiais (`assert res is not None`, `assert len(str) > 5`) tornam o teste inútil contra regressões semânticas.

---

## 3. Análise do que o Teste Propõe — Por que Funcionou mas NÃO Resolveu o Problema?

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                      ANÁLISE DE FALHA TAUTOLÓGICA                         │
├───────────────────────────────────────────────────────────────────────────┤
│ POR QUE FUNCIONOU?                                                        │
│ • O executor de testes (Pytest / Node Test Runner) retorna Código 0       │
│   porque a sintaxe é válida e nenhuma exceção não tratada foi disparada.  │
│ • O teste continha 'assert True', 'assert resultado is not None' ou       │
│   'assert.ok(formatted.length > 5)'.                                      │
├───────────────────────────────────────────────────────────────────────────┤
│ POR QUE NÃO RESOLVEU O PROBLEMA?                                          │
│ • O teste não validou o CONTEÚDO, FORMATO ou a REGRA DE NEGÓCIO.          │
│ • Se um bug alterar o valor retornado de R$ 100,00 para R$ 0,00 (ou se    │
│   formatDate retornar "Invalid Date" que tem 12 caracteres > 5), a        │
│   asserção continuará PASSANDO normalmente!                               │
│ • O erro de produção persiste invisível na suíte de testes.               │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Por que o Problema Ainda Persiste? (Outros Fatores & Espectro Geral)

O problema dos testes ineficazes persiste devido a **5 fatores ocultos de contaminação**:
1. **Acoplamento de Implementação e Constantes Voláteis:** Testes que validam detalhes internos ou contagens estáticas quebradiças (ex.: `assert len(skills) == 24` que falha assim que uma nova skill é criada, sem testar a paridade real com o diretório canônico `skills/`).
2. **Não-Determinismo Temporal (*Flaky Tests*):** Testes que dependem de `time.sleep()`, `datetime.now()` ou medição de tempo real (`const duration = Date.now() - start; assert.ok(duration >= 140 && duration < 800)`), falhando intermitentemente sob carga de CPU no CI/CD.
3. **Mocks Tautológicos:** Substituir serviços ou bancos por mocks que sempre retornam o valor literal esperado na asserção, ignorando constraints reais de tipo e schema.
4. **Falta de Limpeza de Estado (*State Leakage*):** Testes que sobrescrevem `(globalThis as any).window = mockWindow` ou gravam checkpoints em disco sem bloco `try/finally` para restaurar o estado inicial caso uma asserção intermediária falhe.
5. **Extremos de Asserção (Vagueza vs. Fragilidade):** Oscilação entre checagens vagas (`is not None`) e correspondência literal de textos longos cosméticos.

---

## 5. Dossiê de Qualidade de Testes (Espectro por Níveis 1 a 4)

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                    DOSSIÊ E ESPECTRO DE QUALIDADE                         │
├───────────────────────────────────────────────────────────────────────────┤
│ NÍVEL 1: ILUSÓRIO / PLACEBO (Nota: 0 - 25)                                │
│ • Sem asserções, 'assert True', 'try...except: pass' silenciando falhas.  │
│                                                                           │
│ NÍVEL 2: SUPERFICIAL / FRÁGIL (Nota: 26 - 50)                             │
│ • Checagens fracas ('assert x is not None', 'length > 5'), mocks da       │
│   própria regra ou vazamento severo de estado global.                     │
│                                                                           │
│ NÍVEL 3: FUNCIONAL RÍGIDO (Nota: 51 - 80)                                 │
│ • Valida caminho feliz com valores estritos, mas ignora bordas/teardown,  │
│   usa contagens estáticas quebradiças ou relógio real.                    │
│                                                                           │
│ NÍVEL 4: DETERMINÍSTICO & RESILIENTE (Nota: 81 - 100)                     │
│ • Padrão AAA estrito, tempo congelado/controlado, teardown garantido via  │
│   try/finally, validação explícita de exceções e bordas.                  │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Arquitetura do Avaliador de Evals (*Eval-Driven Harness*)

### 6.1. Estrutura de `evals/evals.json` e Workspace de Iteração
```text
test-quality-auditor/
├── SKILL.md
├── rules/criterios_auditoria.md
├── scripts/test_quality_auditor.py
└── evals/
    ├── evals.json
    └── workspace/
        └── iteration-1/
            ├── grading.json     # Avaliação individual com Evidência Concreta
            └── benchmark.json   # Estatísticas agregadas Baseline vs. Treatment
```

### 6.2. Os 4 Eixos de Variabilidade de Prompts e Trigger Matrix
1. **Formatação e Estilo:** Formal, casual, direto ou com ruídos reais de conversa.
2. **Nível de Explicitude:** Pedidos diretos citando AST/auditoria vs. indiretos ("meus testes passam mas o sistema continua dando bug em produção").
3. **Densidade de Contexto:** Snippets curtos vs. arquivos completos de suíte Pytest/Node.
4. **Complexidade da Tarefa:** Inspeção unitária vs. auditoria multi-arquivo + refatoração + geração de `benchmark.json`.
5. **Matriz de Disparo (*Trigger Evals*):** Casos `Should-Trigger` (positivos) vs. `Should-Not-Trigger` (*Near-Misses* próximos, como auditoria visual CSS ou limpeza de arquivos duplicados no Drive).

### 6.3. Matriz Comparativa de Engenharia de Asserções
| Tipo de Checagem | ❌ Asserção Fraca / Frágil | ✅ Asserção Robusta | Mecanismo de Validação |
| :--- | :--- | :--- | :--- |
| **Formato de Saída** | "Responda em JSON adequado." | "A saída é um JSON válido contendo as chaves `aprovado`, `score_medio`, `nivel_espectro` e `issues`." | Script Python (`json.loads` + Schema) |
| **Formatação de Data** | `assert.ok(formatted.length > 5)` | `assert.match(formatted, /^\d{2}\/\d{2}\/\d{4}/)` | Expressão Regular Determinística |
| **Isolamento Global** | `globalThis.window = mockWindow` solto | Bloco `try { ... } finally { globalThis.window = originalWindow; }` | Inspeção AST (`GLOBAL_STATE_LEAKAGE`) |
| **Catálogo Vivo** | `assert len(data) == 24` fixo | `assert len(data) == len(expected_skill_dirs) and len(data) >= 24` | Paridade Dinâmica com Filesystem |
| **Teste Go (`*_test.go`)** | `res, _ := sut(); if res == nil { t.Fatal() }` | `res, err := sut(); if err != nil { t.Fatalf(...) }` + `errors.Is` + `t.TempDir()` | Módulo Go (`go_test_auditor.py`) |
| **Servidor/Tool MCP** | `res = call_mcp(); assert len(res) > 0` | Handshake `initialize` ➔ `tools/list` ➔ `json.loads`/`Unmarshal` + `-32601` + `BLOCKED` | Módulo MCP (`mcp_test_auditor.py`) |
| **Harness (HITL & Evals)** | `SemanticGuard.sanitize_input(inj)` sem `raises` / `CheckpointStore()` global | `pytest.raises(SecurityViolationError)` + `RiskLevel.CRITICAL` + `tmp_path` + `update_status` + `pass_rate_gain` | Módulo Harness (`harness_test_auditor.py`) |

---

## 7. Módulos Especialistas Por Domínio e Espelhos de Evals (`v1.2.0`)

- **[Módulo de Qualidade de Testes em Go (`modulo_qualidade_testes_go.md`)](modulo_qualidade_testes_go.md):** Dissecação nos 7 Módulos para suítes `*_test.go` (`testing.T`, Table-Driven Tests, ADK Go v2, `SILENCED_ERROR_IN_TEST`, `WEAK_NIL_ONLY_ASSERT`, `UNSAFE_GOROUTINE_FATAL`, `GLOBAL_STATE_LEAKAGE`) $\leftrightarrow$ espelho [`evals/modules/go_evals.json`](../evals/modules/go_evals.json).
- **[Módulo de Qualidade de Testes para MCP (`modulo_qualidade_testes_mcp.md`)](modulo_qualidade_testes_mcp.md):** Dissecação nos 7 Módulos para servidores e ferramentas **Model Context Protocol** (JSON-RPC 2.0 `stdio`, FastMCP Python, Go `StdioServer`, `MCP_INCOMPLETE_STDIO_HANDSHAKE`, `MCP_TAUTOLOGICAL_RAW_RESPONSE`, `MCP_WEAK_TOOLS_LIST_DISCOVERY`, `MCP_UNVERIFIED_ERROR_CODE_CONTRACT`, `MCP_WEAK_SECURITY_GUARD_ASSERT`) $\leftrightarrow$ espelho [`evals/modules/mcp_evals.json`](../evals/modules/mcp_evals.json).
- **[Módulo de Qualidade de Testes de Harness (`modulo_qualidade_testes_harness.md`)](modulo_qualidade_testes_harness.md):** Dissecação nos 7 Módulos para **Harnesses de Governança (Zero-Trust / HITL)** e **Eval-Driven Harness** (`HARNESS_WEAK_INJECTION_GUARD_TEST`, `HARNESS_UNVERIFIED_RISK_TRANSITION`, `HARNESS_MISSING_TEARDOWN_CLEANUP`, `HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE`, `HARNESS_EVAL_MISSING_EVIDENCE_OR_DELTA`) $\leftrightarrow$ espelho [`evals/modules/harness_evals.json`](../evals/modules/harness_evals.json).
- **Espelhos Base:** [`evals/modules/python_evals.json`](../evals/modules/python_evals.json) ($\leftrightarrow$ `python_ast_auditor.py`) e [`evals/modules/ts_js_evals.json`](../evals/modules/ts_js_evals.json) ($\leftrightarrow$ `ts_js_auditor.py`).

