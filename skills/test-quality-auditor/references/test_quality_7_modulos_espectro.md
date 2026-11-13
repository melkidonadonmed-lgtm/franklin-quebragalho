# Detalhamento dos 7 Módulos AAA & Espectro de Qualidade (`test-quality-auditor`)

Complemento de [`SKILL.md`](../SKILL.md). Consulte também [`dossie_qualidade_testes_e_evals.md`](dossie_qualidade_testes_e_evals.md), [`modulo_qualidade_testes_go.md`](modulo_qualidade_testes_go.md), [`modulo_qualidade_testes_mcp.md`](modulo_qualidade_testes_mcp.md) e [`modulo_qualidade_testes_harness.md`](modulo_qualidade_testes_harness.md).

## 1. Estrutura dos 7 Módulos de Diagnóstico

1. **Problemática do Teste:** Explique **O Problema** (*Green Build / Green Go / Green MCP / Green Harness Illusion*), **A Abordagem** (Integridade de Asserção, Erros, JSON-RPC, Guardas HITL, Isolamento) e **A Meta** (*Mutation Score High*).
2. **Montagem AAA por Domínio:**
   - **Go (`*_test.go`):** `ARRANGE` (`t.TempDir()`, `t.Setenv()`, `t.Cleanup()`), `ACT` (`res, err := sut()` sem `_`), `ASSERT` (`if err != nil { t.Fatalf(...) }`, `errors.Is`).
   - **MCP (`JSON-RPC 2.0`):** `ARRANGE` (isolamento), `ACT` (`initialize` -> `notifications/initialized` sem `id` -> `tools/list` -> `tools/call`), `ASSERT` (parse JSON, erro `-32601`, bloqueio Zero-Trust).
   - **Harness (`SemanticGuard` / `CheckpointStore` / `Eval Harness`):** `ARRANGE` (`tmp_path`, payloads adversários), `ACT` (`sanitize_input`, `evaluate_action_risk`, ciclo completo `create -> get -> update_status -> clear`, `run_eval_harness`), `ASSERT` (`pytest.raises(SecurityViolationError)`, `RiskLevel.CRITICAL`, `pass_rate_gain > 0`).
3. **Falha Tautológica:** Explique tecnicamente por que retornou `Exit Code 0` sem proteger a regra de negócio.
4. **Fatores de Persistência:** `SILENCED_ERROR_IN_TEST`, `UNSAFE_GOROUTINE_FATAL`, `MCP_INCOMPLETE_STDIO_HANDSHAKE`, `MCP_TAUTOLOGICAL_RAW_RESPONSE`, `HARNESS_WEAK_INJECTION_GUARD_TEST`, `HARNESS_UNVERIFIED_RISK_TRANSITION`, `HARNESS_MISSING_TEARDOWN_CLEANUP`, `HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE`.
5. **Espectro de Qualidade (Níveis 1 a 4):**
   - **Nível 1 (`0–25 pts` — Placebo):** Sem asserções, `assert True`, erro descartado `_`, JSON sem parse ou Harness sem exceção/risco crítico.
   - **Nível 2 (`26–50 pts` — Superficial):** `is not None`, `t.Fatal` em goroutine, `stdio` sem handshake, estado global sem cleanup.
   - **Nível 3 (`51–80 pts` — Rígido):** Happy-path exato, mas `os.Setenv` sem `t.Cleanup` ou `tools/list` apenas por `len > 0`.
   - **Nível 4 (`81–100 pts` — Determinístico):** AAA estrito, teardown isolado, validação de erros adversariais e contratos fechados.
6. **Correção Cirúrgica:** Antes vs. Depois elevando ao Nível 4 + reexecução real (`pytest`, `go test ./...`, `node --test`).
7. **Evals Espelhados:** [`scripts/eval_harness.py`](../scripts/eval_harness.py) gerando `grading.json` e `benchmark.json`.
