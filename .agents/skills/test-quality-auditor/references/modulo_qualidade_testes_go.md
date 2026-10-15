# Módulo Canônico de Qualidade de Testes em Go (`go_test_auditor.py` — `v1.1.0`)

Este documento estabelece o padrão de auditoria em **7 Módulos Sequenciais** e o **Dossiê de Qualidade (Níveis 1 a 4)** para suítes de testes em **Go (`*_test.go`, pacote `testing`, Table-Driven Tests, Concorrência e Google ADK Go v2)**.

---

## 1. Diagnóstico da Problemática do Teste em Go

| Dimensão | Análise Crítica do Problema e Abordagem |
| :--- | :--- |
| **O Problema** | **Falsa Sensação de Segurança no `go test ./...` (*Green Go Test Illusion*):** Em Go, qualquer função `func TestX(t *testing.T)` que termine sua execução sem chamar `t.Fail()`, `t.Error()`, `t.Fatal()` ou entrar em `panic` é reportada como `PASS (ok)`. Isso permite que testes descartem erros com blank identifier (`res, _ := sut()`), ignorem o conteúdo de `if err != nil { t.Log(err) }` ou verifiquem apenas `if res == nil` deixando bugs críticos de domínio escaparem silenciosamente. |
| **A Abordagem** | **Auditoria Estrutural de Blocos `testing.T`, Tratamento de Erros e Concorrência:** O módulo [`scripts/go_test_auditor.py`](../scripts/go_test_auditor.py) disseca cada função `func Test*(t *testing.T)`, contabilizando guardas reais (`t.Fatalf`, `t.Errorf`, `errors.Is`, `assert.*`), rastreando descartes de erro (`_`), detectando chamadas ilegais a `t.Fatal` dentro de goroutines e exigindo isolamento via `t.TempDir()`, `t.Setenv()` e `t.Cleanup()`. |
| **O Que Esperava Conseguir** | **Guardrails Determinísticos & Imunidade a Race Conditions (*Mutation Score High*):** Garantir que qualquer violação de contrato de negócio, erro inesperado ou vazamento de recurso quebre deterministicamente o `go test -race ./...`. |

---

## 2. Análise da Montagem e Seus Elementos (Padrão AAA em Go)

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                  MONTAGEM DO TESTE EM GO (PADRÃO AAA)                         │
├───────────────────┬───────────────────────────────────────────────────────────┤
│ 1. ARRANGE        │ • Isolamento de diretórios via t.TempDir()                │
│ (Preparação)      │ • Variáveis de ambiente escopadas via t.Setenv(k, v)      │
│                   │ • Teardown registrado com t.Cleanup(func() { ... })       │
├───────────────────┼───────────────────────────────────────────────────────────┤
│ 2. ACT            │ • Invocação explícita capturando (res, err) sem usar '_'  │
│ (Execução)        │ • Sincronismo determinístico em goroutines (atomic/chan)  │
├───────────────────┼───────────────────────────────────────────────────────────┤
│ 3. ASSERT         │ • Guarda fatal de erro: if err != nil { t.Fatalf(...) }   │
│ (Verificação)     │ • Verificação de erro tipado: errors.Is(err, ErrExpected) │
│                   │ • Asserção estrita de campos de domínio com t.Errorf(...) │
└───────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 3. Análise do que o Teste Propõe — Por que Funcionou mas NÃO Resolveu o Problema?

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                  ANÁLISE DE FALHA TAUTOLÓGICA EM GO                           │
├───────────────────────────────────────────────────────────────────────────────┤
│ POR QUE FUNCIONOU? (Exit Code 0 no 'go test')                                 │
│ • O código compilou e executou:                                               │
│     res, _ := store.AnalyzeIssue("ISS-101")                                   │
│     if res == nil { t.Fatal("nil result") }                                   │
│ • Como AnalyzeIssue retornou uma struct inicializada com zeros (&Triage{}),   │
│   o ponteiro não era nil e o runner imprimiu '--- PASS: TestAnalyzeIssue'.    │
├───────────────────────────────────────────────────────────────────────────────┤
│ POR QUE NÃO RESOLVEU O PROBLEMA?                                              │
│ 1. O erro retornado foi engolido pelo blank identifier '_'.                   │
│ 2. Se a lógica de SLA quebrar e retornar SLABreached = false e ImpactScore=0  │
│    para um incidente P0 Enterprise, o teste continua PASSANDO 100%!           │
│ 3. O bug de produção sobrevive invisível na suíte Go.                         │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Por que o Problema Ainda Persiste em Go? (5 Fatores de Interferência)

1. **Descarte Silencioso de `error` (`SILENCED_ERROR_IN_TEST`):** Uso de `res, _ := fn()` na etapa *Act* ou blocos `if err != nil { t.Log(err) }` que apenas registram texto no log sem marcar o teste como falho.
2. **Violação de Concorrência em Goroutines (`UNSAFE_GOROUTINE_FATAL`):** Invocar `t.Fatalf` ou `t.FailNow` dentro de uma goroutine secundária (`go func() { t.Fatalf(...) }()`). Como `t.FailNow()` chama `runtime.Goexit()`, executá-la fora da goroutine principal do teste encerra apenas a goroutine filha sem abortar o teste de forma segura (e falha no `go vet` / `go test -race`).
3. **Vazamento de Ambiente de Processo (`GLOBAL_STATE_LEAKAGE`):** Uso de `os.Setenv("KEY", "VAL")` ou `os.Chdir(...)` direto, contaminando outros testes do pacote ou causando *data race* com `t.Parallel()`, em vez de usar `t.Setenv("KEY", "VAL")` e `t.TempDir()`.
4. **Espera Cega com `time.Sleep` (`NON_DETERMINISTIC_TIME`):** Testes unitários que usam `time.Sleep(500 * time.Millisecond)` sem primitivas de sincronismo (`sync/atomic`, canais, `WaitGroup` ou `FlushAndClose`).
5. **Checagem Superficial de Ponteiro (`WEAK_NIL_ONLY_ASSERT`):** Restringir a validação a `if got == nil { t.Fatal(...) }` sem verificar os valores dos campos da struct retornada.

---

## 5. Dossiê de Qualidade de Testes em Go (Espectro Níveis 1 a 4)

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                DOSSIÊ E ESPECTRO DE QUALIDADE — GO (*_test.go)                │
├───────────────────────────────────────────────────────────────────────────────┤
│ NÍVEL 1: ILUSÓRIO / PLACEBO (Nota: 0 - 25)                                    │
│ • Corpo vazio, apenas t.Log(), sem t.Error/t.Fatal (`MISSING_ASSERTIONS`),    │
│   condição `if false { t.Fatal() }` ou erro descartado com `_` + nil check.   │
│                                                                               │
│ NÍVEL 2: SUPERFICIAL / FRÁGIL (Nota: 26 - 50)                                 │
│ • Checagem exclusiva `if res == nil` (`WEAK_NIL_ONLY_ASSERT`), ou chamada     │
│   ilegal a `t.Fatalf` dentro de `go func()` (`UNSAFE_GOROUTINE_FATAL`).       │
│                                                                               │
│ NÍVEL 3: FUNCIONAL RÍGIDO (Nota: 51 - 80)                                     │
│ • Valida campos de retorno, mas muta ambiente com `os.Setenv` sem `t.Cleanup` │
│   (`GLOBAL_STATE_LEAKAGE`) ou usa `time.Sleep` arbitrário sem sincronismo.    │
│                                                                               │
│ NÍVEL 4: DETERMINÍSTICO & RESILIENTE (Nota: 81 - 100)                         │
│ • Padrão AAA estrito com `t.TempDir()` / `t.Setenv()` / `t.Cleanup()`,        │
│   validação explícita `if err != nil { t.Fatalf(...) }`, checagem de erros    │
│   de domínio via `errors.Is(err, ErrExpected)` e asserção de invariantes.     │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Correção Cirúrgica Antes vs. Depois (Go)

### ❌ ANTES (Nível 1 — Nota 0/100: `SILENCED_ERROR_IN_TEST` + `WEAK_NIL_ONLY_ASSERT`)
```go
func TestAnalyzeIssueSilenced(t *testing.T) {
	store := domain.NewDefaultStore()
	triage, _ := store.AnalyzeIssue("ISS-101")
	if triage == nil {
		t.Fatal("expected non-nil triage")
	}
}
```

### ✅ DEPOIS (Nível 4 — Nota 100/100: Determinístico & Resiliente)
```go
func TestStoreAnalyzeIssueAndSLABreach(t *testing.T) {
	store := domain.NewDefaultStore()

	triage, err := store.AnalyzeIssue("ISS-101")
	if err != nil {
		t.Fatalf("unexpected error analyzing ISS-101: %v", err)
	}
	if !triage.SLABreached || !triage.EscalationRequired || triage.ImpactScore < 90 {
		t.Errorf("expected P0 SLA breach with score >= 90, got %+v", triage)
	}

	_, err = store.AnalyzeIssue("ISS-999")
	if !errors.Is(err, domain.ErrIssueNotFound) {
		t.Fatalf("expected ErrIssueNotFound for unknown ID, got %v", err)
	}
}
```

---

## 7. Matriz Comparativa de Engenharia de Asserções em Go (`testing.T`)

| Tipo de Checagem | ❌ Asserção Fraca / Frágil | ✅ Asserção Robusta (Nível 4) | Regra do Auditor |
| :--- | :--- | :--- | :--- |
| **Retorno de Erro** | `res, _ := svc.Run(ctx)` | `res, err := svc.Run(ctx); if err != nil { t.Fatalf("...: %v", err) }` | `SILENCED_ERROR_IN_TEST` |
| **Erro Esperado** | `if err == nil { t.Error("erro") }` | `if !errors.Is(err, domain.ErrIssueNotFound) { t.Fatalf(...) }` | `WEAK_NIL_ONLY_ASSERT` |
| **Goroutines** | `go func() { t.Fatalf("fail") }()` | `errCh <- err` na goroutine filha + `if err := <-errCh; err != nil { t.Fatal(err) }` | `UNSAFE_GOROUTINE_FATAL` |
| **Ambiente / FS** | `os.Setenv("K", "V")` / `/tmp/test` | `t.Setenv("K", "V")` / `t.TempDir()` + `t.Cleanup(...)` | `GLOBAL_STATE_LEAKAGE` |
| **Debounce / Tempo** | `time.Sleep(1 * time.Second)` solto | `atomic.AddInt32(&count, 1)` + `debouncer.FlushAndClose()` | `NON_DETERMINISTIC_TIME` |
