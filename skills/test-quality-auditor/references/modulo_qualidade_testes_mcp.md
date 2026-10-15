# Módulo Canônico de Qualidade de Testes para MCP (`mcp_test_auditor.py` — `v1.1.0`)

Este documento estabelece o padrão de auditoria em **7 Módulos Sequenciais** e o **Dossiê de Qualidade (Níveis 1 a 4)** para suítes de testes de **Servidores, Clientes e Pontes MCP (Model Context Protocol — JSON-RPC 2.0, FastMCP Python, Go `StdioServer` e TypeScript MCP)**.

---

## 1. Diagnóstico da Problemática do Teste em MCP

| Dimensão | Análise Crítica do Problema e Abordagem |
| :--- | :--- |
| **O Problema** | **Falsa Sensação de Segurança em Tools MCP (*Green MCP Tool Illusion*):** Suítes de teste para servidores MCP frequentemente invocam a função da tool diretamente ou enviam uma string para o servidor `stdio` e validam apenas `assert len(res) > 0` ou `assert res is not None`. Isso oculta quebras críticas de protocolo: falhas na negociação `initialize`, notificações `notifications/initialized` malformadas com `id`, ausência do código JSON-RPC `-32601` para tools inexistentes, payloads JSON corrompidos ou brechas de Path Traversal (`../`). |
| **A Abordagem** | **Auditoria de Contrato JSON-RPC 2.0, Descoberta de Schema e Fronteira Zero-Trust:** O módulo [`scripts/mcp_test_auditor.py`](../scripts/mcp_test_auditor.py) inspeciona testes MCP em Python, Go e TypeScript/JS, exigindo validação completa do ciclo de vida (`initialize` ➔ `notifications/initialized` ➔ `tools/list` ➔ `tools/call`), decodificação estrutural (`json.loads` / `json.Unmarshal`), checagem de códigos de erro (`-32601`) e asserções explícitas de bloqueio em payloads adversariais. |
| **O Que Esperava Conseguir** | **Interoperabilidade Determinística e Blindagem Zero-Trust:** Garantir que qualquer regressão no transporte `stdio`/HTTP, no schema de ferramentas ou nos guardrails de segurança (`SemanticGuard` / `CheckpointStore`) quebre imediatamente a suíte de testes. |

---

## 2. Análise da Montagem e Seus Elementos (Padrão AAA em MCP)

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                  MONTAGEM DO TESTE MCP (PADRÃO AAA)                           │
├───────────────────┬───────────────────────────────────────────────────────────┤
│ 1. ARRANGE        │ • Isolamento de sessão/checkpoints (t.TempDir / try-finally)│
│ (Preparação)      │ • Montagem da sequência JSON-RPC 2.0 (initialize id:1,    │
│                   │   notifications/initialized SEM id, tools/list, tools/call)│
├───────────────────┼───────────────────────────────────────────────────────────┤
│ 2. ACT            │ • Execução via buffer stdio (Serve) ou chamada da tool MCP│
│ (Execução)        │ • Coleta das linhas JSON-RPC ou do payload retornado      │
├───────────────────┼───────────────────────────────────────────────────────────┤
│ 3. ASSERT         │ • Decodificação obrigatória (json.loads / json.Unmarshal) │
│ (Verificação)     │ • Verificação de nomes reais em tools/list                │
│                   │ • Validação de erro JSON-RPC (-32601) e trava Zero-Trust  │
└───────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 3. Análise do que o Teste Propõe — Por que Funcionou mas NÃO Resolveu o Problema?

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                  ANÁLISE DE FALHA TAUTOLÓGICA EM MCP                          │
├───────────────────────────────────────────────────────────────────────────────┤
│ POR QUE FUNCIONOU? (Exit Code 0 no Pytest / Go Test)                          │
│ • O teste executou:                                                           │
│     res = server.franklin_execute_dag("../secrets.json")                      │
│     assert len(res) > 0                                                       │
│ • Como a função retornou uma string JSON de erro com 68 caracteres (> 0),     │
│   a asserção passou com código 0!                                             │
├───────────────────────────────────────────────────────────────────────────────┤
│ POR QUE NÃO RESOLVEU O PROBLEMA?                                              │
│ 1. O teste nunca decodificou o JSON (json.loads) para verificar o campo       │
│    'status' nem validou se o Path Traversal foi bloqueado.                    │
│ 2. Em testes stdio JSON-RPC, disparar 'tools/call' sem 'initialize' não       │
│    detecta falhas de handshake ou respostas indevidas a notificações sem id.  │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Por que o Problema Ainda Persiste em MCP? (5 Fatores de Interferência)

1. **Asserção em String Crua Sem Parse JSON (`MCP_TAUTOLOGICAL_RAW_RESPONSE`):** Testar tools que retornam JSON serializado (`format="json"`, `franklin_execute_dag`, `franklin_harness_guard`) usando apenas `len(res) > 0` ou `res is not None` sem `json.loads` / `json.Unmarshal`.
2. **Handshake Stdio Incompleto (`MCP_INCOMPLETE_STDIO_HANDSHAKE`):** Testes de servidor `stdio` que enviam `tools/call` sem testar `initialize` + `notifications/initialized` (ou que colocam `"id"` em uma notificação JSON-RPC 2.0, que por especificação não deve ter `id` nem gerar resposta).
3. **Descoberta Cega em `tools/list` (`MCP_WEAK_TOOLS_LIST_DISCOVERY`):** Verificar apenas se `len(tools) > 0` sem confirmar se as ferramentas canônicas esperadas estão registradas e serializáveis.
4. **Omissão do Contrato de Erro JSON-RPC (`MCP_UNVERIFIED_ERROR_CODE_CONTRACT`):** Chamar uma `nonexistent_tool` sem validar se o envelope de resposta contém `error.code == -32601` (*Method not found*).
5. **Falta de Asserção em Payloads Zero-Trust (`MCP_WEAK_SECURITY_GUARD_ASSERT`):** Enviar `../secrets.txt` ou `Ignore all previous instructions` sem exigir explicitamente `"Erro de Segurança"` ou `status == "BLOCKED"`.

---

## 5. Dossiê de Qualidade de Testes MCP (Espectro Níveis 1 a 4)

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                DOSSIÊ E ESPECTRO DE QUALIDADE — MCP (JSON-RPC 2.0)            │
├───────────────────────────────────────────────────────────────────────────────┤
│ NÍVEL 1: ILUSÓRIO / PLACEBO (Nota: 0 - 25)                                    │
│ • Chama tool MCP sem asserção ou valida apenas `len(res) > 0` em payload      │
│   adversarial sem decodificar JSON nem checar bloqueio de segurança.          │
│                                                                               │
│ NÍVEL 2: SUPERFICIAL / FRÁGIL (Nota: 26 - 50)                                 │
│ • Envia `tools/call` via stdio sem handshake `initialize` e sem validar       │
│   código de erro `-32601`, ou omite `json.loads`/`json.Unmarshal`.            │
│                                                                               │
│ NÍVEL 3: FUNCIONAL RÍGIDO (Nota: 51 - 80)                                     │
│ • Decodifica JSON do caminho feliz, mas valida `tools/list` apenas por        │
│   `len > 0` ou muta `.sessions/harness_checkpoints.json` sem `try/finally`.   │
│                                                                               │
│ NÍVEL 4: DETERMINÍSTICO & RESILIENTE (Nota: 81 - 100)                         │
│ • Valida ciclo completo (`initialize` ➔ `notifications/initialized` sem id    │
│   ➔ `tools/list` com nomes reais ➔ `tools/call` sucesso e erro `-32601`),     │
│   fronteiras Zero-Trust (`BLOCKED`/`APPROVAL_REQUIRED`) e teardown garantido. │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Correção Cirúrgica Antes vs. Depois (MCP)

### ❌ ANTES (Nível 2 — Nota 40/100: `MCP_INCOMPLETE_STDIO_HANDSHAKE` + `MCP_UNVERIFIED_ERROR_CODE_CONTRACT`)
```go
func TestMCPBrokenStdio(t *testing.T) {
	req := `{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"nonexistent_tool"}}`
	resp := runStdioServer(req)
	if len(resp) == 0 {
		t.Fatalf("empty response")
	}
}
```

### ✅ DEPOIS (Nível 4 — Nota 100/100: Handshake JSON-RPC 2.0 Completo + Erro `-32601`)
```go
func TestMCPStdioComplete(t *testing.T) {
	reqs := []string{
		`{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}`,
		`{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}`,
		`{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}`,
		`{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"nonexistent_tool"}}`,
	}
	out := serveMCP(t.TempDir(), reqs)
	var errResp JSONRPCResponse
	if err := json.Unmarshal([]byte(out[2]), &errResp); err != nil {
		t.Fatalf("unmarshal failed: %v", err)
	}
	if !strings.Contains(out[1], "go_fast_dispatch") || errResp.Error.Code != -32601 {
		t.Errorf("invalid mcp contract: %+v", errResp)
	}
}
```

---

## 7. Matriz Comparativa de Engenharia de Asserções em MCP

| Dimensão MCP | ❌ Asserção Fraca / Frágil | ✅ Asserção Robusta (Nível 4) | Regra do Auditor |
| :--- | :--- | :--- | :--- |
| **Handshake Stdio** | Dispara `tools/call` isolado | Sequência `initialize` (`id:1`) + `notifications/initialized` (sem `id`) + `len(lines)` exato | `MCP_INCOMPLETE_STDIO_HANDSHAKE` |
| **Payload de Tool JSON** | `assert len(res) > 0` | `data = json.loads(res); assert data["status"] == "COMPLETED"` | `MCP_TAUTOLOGICAL_RAW_RESPONSE` |
| **Descoberta `tools/list`** | `assert result["tool_count"] > 0` | `assert "go_fast_dispatch" in tools and "analyze_issue_triage" in tools` | `MCP_WEAK_TOOLS_LIST_DISCOVERY` |
| **Tool Inexistente** | `assert "error" in line` | `json.Unmarshal` + `errResp.Error != nil && errResp.Error.Code == -32601` | `MCP_UNVERIFIED_ERROR_CODE_CONTRACT` |
| **Guardrail Zero-Trust** | `franklin_run_skill_script("..", "x")` | `assert "Erro de Segurança" in res` / `assert blocked["status"] == "BLOCKED"` | `MCP_WEAK_SECURITY_GUARD_ASSERT` |
