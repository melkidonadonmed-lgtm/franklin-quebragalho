# MCP Test Quality Module (`mcp_test_auditor.py` — `v1.3.0`)

Defines the **7 Sequential Modules** and **Quality Spectrum (Levels 1–4)** for **MCP (Model Context Protocol — JSON-RPC 2.0, FastMCP Python, Go `StdioServer`, TypeScript MCP, and WebSockets)** test suites, operating alongside `agent-server-auditor` (`references/audit-websocket-jsonrpc.md`) and grounded via `google-developer-knowledge` / `gemini_get_doc` (`aistudio.google.com/llms.txt`; never invoke disabled doc-search aliases) when Gemini SDKs are involved.

---

## 1. MCP Testing Problem Statement

| Dimension | Critical Analysis & Engineering Approach |
| :--- | :--- |
| **The Problem** | **False Sense of Security in MCP Tools (*Green MCP Tool Illusion*):** MCP server tests frequently invoke tool functions directly or send a raw string over `stdio` and assert only `assert len(res) > 0` or `assert res is not None`. This hides critical protocol breaks: failed `initialize` negotiation, malformed `notifications/initialized` containing an `id`, missing JSON-RPC `-32601` for unknown tools, corrupted JSON payloads, or Path Traversal (`../`) leaks. |
| **The Approach** | **JSON-RPC 2.0 Contract, Schema Discovery & Zero-Trust Boundary Auditing:** [`scripts/mcp_test_auditor.py`](scripts/mcp_test_auditor.py) inspects Python, Go, and TS/JS MCP tests, enforcing full lifecycle coverage (`initialize` $\rightarrow$ `notifications/initialized` $\rightarrow$ `tools/list` $\rightarrow$ `tools/call`), structural JSON parsing (`json.loads` / `json.Unmarshal`), `-32601` error verification, and explicit rejection of adversarial inputs. |
| **Target Outcome** | **Deterministic Interoperability & Zero-Trust Hardening:** Ensure any regression in `stdio`/HTTP transport, tool schemas, or `SemanticGuard`/`CheckpointStore` immediately fails the test suite. |

---

## 2. MCP Test AAA Anatomy

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                    MCP TEST ANATOMY (AAA PATTERN)                             │
├───────────────────┬───────────────────────────────────────────────────────────┤
│ 1. ARRANGE        │ • Session/checkpoint isolation (t.TempDir / try-finally)  │
│ (Preparation)     │ • JSON-RPC 2.0 sequence (initialize id:1,                 │
│                   │   notifications/initialized WITHOUT id, tools/list, call) │
├───────────────────┼───────────────────────────────────────────────────────────┤
│ 2. ACT            │ • Run via stdio buffer (Serve) or MCP tool invocation     │
│ (Execution)       │ • Capture JSON-RPC response lines or returned payload     │
├───────────────────┼───────────────────────────────────────────────────────────┤
│ 3. ASSERT         │ • Mandatory decoding (json.loads / json.Unmarshal)        │
│ (Verification)    │ • Verify canonical tool names in tools/list               │
│                   │ • Assert JSON-RPC error (-32601) and Zero-Trust blocks    │
└───────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 3. Tautological Failure Analysis in MCP

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                   MCP TAUTOLOGICAL FAILURE ANALYSIS                           │
├───────────────────────────────────────────────────────────────────────────────┤
│ WHY DID IT PASS? (Pytest / Go Test Exit Code 0)                               │
│ • The test executed:                                                          │
│     res = server.franklin_execute_dag("../secrets.json")                      │
│     assert len(res) > 0                                                       │
│ • Because the function returned a 68-char error JSON string (> 0), the        │
│   assertion exited 0!                                                         │
├───────────────────────────────────────────────────────────────────────────────┤
│ WHY DID IT FAIL THE REAL REQUIREMENT?                                         │
│ 1. It never decoded JSON (json.loads) to verify 'status' or confirm that      │
│    Path Traversal was actually blocked.                                       │
│ 2. Firing 'tools/call' over stdio without 'initialize' misses handshake bugs  │
│    or illegal replies to notifications lacking an id.                         │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Why Defects Persist in MCP (5 Interference Factors)

1. **Raw String Check Without JSON Parse (`MCP_TAUTOLOGICAL_RAW_RESPONSE`):** Testing JSON-returning tools (`format="json"`, `franklin_execute_dag`, `franklin_harness_guard`) via `len(res) > 0` or `res is not None` without `json.loads` / `json.Unmarshal`.
2. **Incomplete Stdio Handshake (`MCP_INCOMPLETE_STDIO_HANDSHAKE`):** `stdio` server tests sending `tools/call` without `initialize` + `notifications/initialized`, or attaching `"id"` to a JSON-RPC 2.0 notification.
3. **Blind `tools/list` Discovery (`MCP_WEAK_TOOLS_LIST_DISCOVERY`):** Checking only `len(tools) > 0` without asserting expected canonical tool names.
4. **Missing JSON-RPC Error Code Contract (`MCP_UNVERIFIED_ERROR_CODE_CONTRACT`):** Calling `nonexistent_tool` without verifying `error.code == -32601` (*Method not found*).
5. **Unchecked Zero-Trust Payloads (`MCP_WEAK_SECURITY_GUARD_ASSERT`):** Passing `../secrets.txt` or `Ignore all previous instructions` without asserting `"Erro de Segurança"` or `status == "BLOCKED"`.

---

## 5. MCP Test Quality Spectrum (Levels 1 to 4)

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                MCP TEST QUALITY SPECTRUM (JSON-RPC 2.0)                       │
├───────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 1: ILLUSORY / PLACEBO (Score: 0 - 25)                                   │
│ • Invokes MCP tool without assertions or checks only `len(res) > 0` on        │
│   adversarial input without JSON decoding or security verification.           │
│                                                                               │
│ LEVEL 2: SUPERFICIAL / FRAGILE (Score: 26 - 50)                               │
│ • Sends `tools/call` over stdio without `initialize` handshake and without    │
│   checking `-32601`, or omits `json.loads`/`json.Unmarshal`.                  │
│                                                                               │
│ LEVEL 3: RIGID FUNCTIONAL (Score: 51 - 80)                                    │
│ • Decodes happy-path JSON, yet checks `tools/list` by `len > 0` only or       │
│   mutates `.sessions/harness_checkpoints.json` without `try/finally`.         │
│                                                                               │
│ LEVEL 4: DETERMINISTIC & RESILIENT (Score: 81 - 100)                          │
│ • Validates full lifecycle (`initialize` -> `notifications/initialized` no id │
│   -> `tools/list` real names -> `tools/call` success and `-32601`),           │
│   Zero-Trust blocks (`BLOCKED`/`APPROVAL_REQUIRED`), and guaranteed teardown. │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Surgical Refactoring Before vs. After (MCP)

### BEFORE (Level 2 — Score 40/100: `MCP_INCOMPLETE_STDIO_HANDSHAKE` + `MCP_UNVERIFIED_ERROR_CODE_CONTRACT`)
```go
func TestMCPBrokenStdio(t *testing.T) {
	req := `{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"nonexistent_tool"}}`
	resp := runStdioServer(req)
	if len(resp) == 0 {
		t.Fatalf("empty response")
	}
}
```

### AFTER (Level 4 — Score 100/100: Full JSON-RPC 2.0 Handshake + `-32601` Error)
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

## 7. MCP Assertion Engineering Comparison Matrix

| MCP Dimension | Weak / Fragile Assertion | Robust Assertion (Level 4) | Auditor Rule |
| :--- | :--- | :--- | :--- |
| **Stdio Handshake** | Isolated `tools/call` | `initialize` (`id:1`) + `notifications/initialized` (no `id`) + exact `len(lines)` | `MCP_INCOMPLETE_STDIO_HANDSHAKE` |
| **JSON Tool Payload** | `assert len(res) > 0` | `data = json.loads(res); assert data["status"] == "COMPLETED"` | `MCP_TAUTOLOGICAL_RAW_RESPONSE` |
| **`tools/list` Discovery** | `assert result["tool_count"] > 0` | `assert "go_fast_dispatch" in tools and "analyze_issue_triage" in tools` | `MCP_WEAK_TOOLS_LIST_DISCOVERY` |
| **Unknown Tool** | `assert "error" in line` | `json.Unmarshal` + `errResp.Error != nil && errResp.Error.Code == -32601` | `MCP_UNVERIFIED_ERROR_CODE_CONTRACT` |
| **Zero-Trust Guardrail** | `franklin_run_skill_script("..", "x")` | `assert "Erro de Segurança" in res` / `assert blocked["status"] == "BLOCKED"` | `MCP_WEAK_SECURITY_GUARD_ASSERT` |
