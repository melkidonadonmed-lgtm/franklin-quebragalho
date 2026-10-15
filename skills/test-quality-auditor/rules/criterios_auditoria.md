# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`test-quality-auditor` v1.2.0)

Toda auditoria executada por esta skill deve emitir marcadores determinísticos baseados em evidências reais extraídas da Árvore Sintática Abstrata (AST), dos analisadores estruturais multi-domínio (Python, TypeScript/JS, Go, Protocolo MCP e Harness) e da execução da suíte de testes:
- `[PASS]`: Requisito estrutural, semântico ou de determinismo comprovado sem violações.
- `[FAIL]`: Violação confirmada pelo analisador ou runner com apontamento exato de `arquivo:linha` e código da anomalia.
- `[UNVERIFIED]`: Impossibilidade de verificação por ausência do arquivo alvo ou erro de sintaxe bloqueante (`SYNTAX_ERROR`).

---

### Regra 1: Integridade do Corpo e Densidade de Asserções (Proibição de Testes Placebos)
- **Critério**: Toda função de teste (`test_*` em Python, `test(...)`/`it(...)` em JS/TS ou `func Test*(t *testing.T)` em Go) deve conter pelo menos uma asserção verificável sobre o resultado ou efeito colateral da unidade sob teste.
- **Verificação Determinística**:
  - Função de teste contendo apenas `pass`, `return`, `t.Log` ou corpo vazio -> `[FAIL: EMPTY_TEST_BODY]` (Severidade: Crítica | `-85 pts` | Rebaixa para Nível 1)
  - Função de teste que executa código (`Act`) mas possui `assertion_count == 0` -> `[FAIL: MISSING_ASSERTIONS]` (Severidade: Crítica | `-80 pts` | Rebaixa para Nível 1)
  - Presença de asserções explícitas verificando retorno ou contrato -> `[PASS]`

### Regra 2: Rigor da Asserção e Proibição de Tautologias (`TAUTOLOGICAL_ASSERT` / `WEAK_ASSERT`)
- **Critério**: Asserções devem ser falsificáveis por mutações na regra de negócio. Asserções constantes ou puramente superficiais são rejeitadas.
- **Verificação Determinística**:
  - Presença de `assert True`, `self.assertTrue(True)`, `assert.ok(true)` ou `if false { t.Fatal(...) }` -> `[FAIL: TAUTOLOGICAL_ASSERT]` (Severidade: Crítica | `-80 pts` | Rebaixa para Nível 1)
  - Asserção única/principal restrita a `assert x is not None` sem validar atributos ou valor de negócio -> `[FAIL: WEAK_IS_NOT_NONE_ASSERT]` (Severidade: Média | `-55 pts`)
  - Asserção superficial de comprimento/tipo genérico (`assert.ok(str.length > 5)`) -> `[FAIL: WEAK_SURFACE_ASSERT]` (Severidade: Média | `-22 pts`)
  - Comparação estrita de valor (`==`, `assert.strictEqual`, `t.Errorf`), estrutura ou contrato tipado -> `[PASS]`

### Regra 3: Tratamento Explícito de Exceções e Erros (`SILENCED_EXCEPTION_IN_TEST`)
- **Critério**: Testes nunca devem engolir exceções ou erros com `try...except: pass`, `catch {}` vazio ou descarte silencioso `_`. Exceções/erros esperados devem ser validados via `pytest.raises(...)`, `await assert.rejects(...)` ou `errors.Is(err, ErrExpected)`.
- **Verificação Determinística**:
  - Bloco `ExceptHandler` ou `catch` em teste contendo apenas `pass` ou vazio -> `[FAIL: SILENCED_EXCEPTION_IN_TEST]` (Severidade: Crítica | `-75 pts` | Rebaixa para Nível 1)
  - Uso explícito de `pytest.raises` / `assert.rejects` / `errors.Is` validando tipo e mensagem do erro -> `[PASS]`

### Regra 4: Imunidade a Não-Determinismo Temporal e Concorrência (`NON_DETERMINISTIC_TIME`)
- **Critério**: Testes devem ser independentes da velocidade da CPU, carga do sistema operacional ou relógio de parede (*wall-clock*).
- **Verificação Determinística**:
  - Invocação direta de `time.sleep()`, `datetime.now()`, `Date.now()` ou `time.Sleep()` sem primitiva de sincronismo/injeção de relógio -> `[FAIL: NON_DETERMINISTIC_TIME]` (Severidade: Alta | `-25 pts`)
  - Tempo injetado, congelado ou sincronizado via primitiva atômica/canal -> `[PASS]`

### Regra 5: Isolamento de Estado Global e Limpeza de Recursos (`GLOBAL_STATE_LEAKAGE`)
- **Critério**: Qualquer teste que sobrescreva estado global (`globalThis.window`, `globalThis.fetch`, `os.environ`, `os.Setenv`, singletons ou arquivos de sessão) deve garantir a restauração do estado original em bloco `try...finally`, `t.Setenv`, `t.TempDir()` ou `t.Cleanup`.
- **Verificação Determinística**:
  - Mutação direta de estado global/ambiente sem restauração garantida na mesma função de teste -> `[FAIL: GLOBAL_STATE_LEAKAGE]` (Severidade: Alta | `-25 pts`)
  - Isolamento e restauração garantida via `try...finally`, `t.TempDir()` ou `t.Cleanup` -> `[PASS]`

### Regra 6: Desacoplamento de Constantes Voláteis de Catálogo (`BRITTLE_CATALOG_COUNT`)
- **Critério**: Testes de listagem de catálogos vivos não devem usar números mágicos estáticos quebradiços (`assert len(data) == 24`), devendo validar contra a fonte canônica de verdade no disco (`len(data) == len(expected_dirs)`).
- **Verificação Determinística**:
  - Igualdade literal fixa `len(data) == N` acoplada a catálogo mutável sem derivar do filesystem -> `[FAIL: BRITTLE_CATALOG_COUNT]` (Severidade: Média | `-22 pts`)
  - Validação dinâmica contra a fonte de verdade e contratos de itens -> `[PASS]`

### Regra 7: Conformidade do Módulo de Testes em Go (`go_test_auditor.py` $\leftrightarrow$ `evals/modules/go_evals.json`)
- **Critério**: Suítes de teste em Go (`testing.T`, Table-Driven Tests, ADK Go v2) devem verificar todos os erros retornados pelo SUT, validar atributos de negócio além de `nil` e nunca invocar `t.Fatal`/`t.FailNow` dentro de goroutines secundárias.
- **Verificação Determinística**:
  - Descarte de erro retornado pelo SUT com blank identifier (`res, _ := sut(...)`) ou bloco `if err != nil` sem `t.Fatal`/`t.Error` -> `[FAIL: SILENCED_ERROR_IN_TEST]` (Severidade: Crítica | `-65 pts`)
  - Checagem única restrita a `if res == nil { t.Fatal(...) }` ou `assert.NotNil(t, res)` sem validar campos de domínio -> `[FAIL: WEAK_NIL_ONLY_ASSERT]` (Severidade: Média | `-55 pts`)
  - Invocação de `t.Fatal`, `t.Fatalf` ou `t.FailNow` dentro de `go func() { ... }()` -> `[FAIL: UNSAFE_GOROUTINE_FATAL]` (Severidade: Alta | `-40 pts`)
  - Verificação completa de `(res, err)`, `errors.Is`, campos de negócio e sincronismo seguro -> `[PASS]`

### Regra 8: Conformidade do Módulo de Testes MCP (`mcp_test_auditor.py` $\leftrightarrow$ `evals/modules/mcp_evals.json`)
- **Critério**: Suítes de teste para servidores, ferramentas e pontes MCP devem validar o ciclo de vida JSON-RPC 2.0 (`initialize` ➔ `notifications/initialized` sem `id` ➔ `tools/list` ➔ `tools/call`), decodificar payloads JSON, verificar códigos de erro (`-32601`) e testar fronteiras Zero-Trust.
- **Verificação Determinística**:
  - Chamada a `tools/call` via `stdio` sem handshake `initialize` prévio ou envio de `notifications/initialized` com campo `id` -> `[FAIL: MCP_INCOMPLETE_STDIO_HANDSHAKE]` (Severidade: Alta | `-30 pts`)
  - Chamada a tool MCP JSON validada apenas como string bruta (`len(res) > 0` / `is not None`) sem `json.loads` / `json.Unmarshal` -> `[FAIL: MCP_TAUTOLOGICAL_RAW_RESPONSE]` (Severidade: Crítica | `-55 pts`)
  - Inspeção de `tools/list` verificando apenas contagem `> 0` sem validar nomes canônicos de tools -> `[FAIL: MCP_WEAK_TOOLS_LIST_DISCOVERY]` (Severidade: Média | `-25 pts`)
  - Teste de `nonexistent_tool` sem verificar o código JSON-RPC `-32601` -> `[FAIL: MCP_UNVERIFIED_ERROR_CODE_CONTRACT]` (Severidade: Alta | `-30 pts`)
  - Envio de payload adversarial (`../` ou Prompt Injection) sem asserção explícita de bloqueio (`BLOCKED` / `Erro de Segurança`) -> `[FAIL: MCP_WEAK_SECURITY_GUARD_ASSERT]` (Severidade: Alta | `-35 pts`)
  - Validação integral do protocolo JSON-RPC 2.0, schema JSON e fronteiras Zero-Trust -> `[PASS]`

### Regra 9: Conformidade do Módulo de Testes de Harness (`harness_test_auditor.py` $\leftrightarrow$ `evals/modules/harness_evals.json`)
- **Critério**: Testes de Harnesses de Governança (`SemanticGuard`, `evaluate_action_risk`, `CheckpointStore`) e de Avaliação (`run_eval_harness`) devem comprovar bloqueio de injeção, transição para `RiskLevel.CRITICAL`, isolamento em `tmp_path`, ciclo completo de checkpoints e cálculo de `pass_rate_gain`.
- **Verificação Determinística**:
  - Teste de `SemanticGuard.sanitize_input` com payload de injeção sem `pytest.raises(SecurityViolationError)` / `"BLOCKED"` -> `[FAIL: HARNESS_WEAK_INJECTION_GUARD_TEST]` (Severidade: Crítica | `-50 pts`)
  - Teste de `evaluate_action_risk` / `franklin_harness_guard` com comando destrutivo sem validar `RiskLevel.CRITICAL` / `"APPROVAL_REQUIRED"` -> `[FAIL: HARNESS_UNVERIFIED_RISK_TRANSITION]` (Severidade: Crítica | `-45 pts`)
  - Mutação de `CheckpointStore` ou `franklin_harness_guard` sem `tmp_path`/`TempDir`/`try...finally` -> `[FAIL: HARNESS_MISSING_TEARDOWN_CLEANUP]` (Severidade: Alta | `-35 pts`)
  - Chamada a `CheckpointStore.create()` sem validar leitura (`.get()` / `.list()`) ou transição (`.update_status()`) -> `[FAIL: HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE]` (Severidade: Média | `-25 pts`)
  - Chamada a `run_eval_harness()` sem inspecionar `pass_rate`, `pass_rate_gain` ou `evidence` -> `[FAIL: HARNESS_EVAL_MISSING_EVIDENCE_OR_DELTA]` (Severidade: Alta | `-35 pts`)
  - Validação integral do Harness de Governança e Avaliação no Nível 4 -> `[PASS]`

### Regra 10: Conformidade da Esteira de Evals Espelhados (`evals/modules/*_evals.json` & `evals/evals.json`)
- **Critério**: Cada um dos 5 módulos analisadores (`python`, `ts_js`, `go`, `mcp`, `harness`) deve possuir um arquivo espelho em `evals/modules/<mod>_evals.json` gerando `<mod>_grading.json` e `<mod>_benchmark.json` em `evals/workspace/iteration-1/modules/`, além do manifesto consolidado `evals/evals.json` (20 casos).
- **Verificação Determinística**:
  - Qualquer módulo espelhado ausente, sem `evidence` concreta ou com `pass_rate < 1.0` -> `[FAIL: INVALID_EVAL_HARNESS]`
  - Todos os 5 módulos espelhados (17 casos modulares) + 3 Near-Misses (20 casos consolidados) aprovados com `100% PASS` -> `[PASS]`
