# Matriz de Conformidade de Protocolos Agênticos (`MCP 2026-07-28` & `A2A v1.0`)

Documento de referência técnica da skill **`agent-server-auditor`** para inspeção estática poliglota (**Python**, **TypeScript** e **Go**).

---

## 1. Model Context Protocol (`MCP Spec 2026-07-28`)

### 1.1. Higiene de Streams no Transporte `STDIO`
- **Regra Canônica:** No transporte `STDIO`, o descritor `stdout` é o barramento binário/textual de quadros `JSON-RPC 2.0`. Qualquer byte não pertencente a um envelope JSON-RPC válido corrompe o parser do cliente MCP.
- **Padrões Proibidos em Servidores STDIO (`stdout_hygiene = "POLLUTED"`):**
  - **Python:** `print(...)` sem `file=sys.stderr`.
  - **TypeScript / Node.js:** `console.log(...)` ou `process.stdout.write(...)` com texto de log.
  - **Go:** `fmt.Println(...)`, `fmt.Printf(...)` ou `log.Println(...)` sem redirecionar `log.SetOutput(os.Stderr)`.
- **Padrões Seguros (`stdout_hygiene = "CLEAN"`):**
  - **Python:** `logging.StreamHandler(sys.stderr)`, `print(..., file=sys.stderr)`.
  - **TypeScript:** `console.error(...)`, `process.stderr.write(...)`.
  - **Go:** `fmt.Fprintln(os.Stderr, ...)`, `slog.New(slog.NewJSONHandler(os.Stderr, nil))`.

### 1.2. Primitivas e Contratos MCP
- **Primitivas Expostas:** Declaração explícita de `tools` (`@mcp.tool`), `resources` (`@mcp.resource`) e `prompts` (`@mcp.prompt`).
- **Stateless Core & Metadados:** Suporte a `_meta` com `io.modelcontextprotocol/protocolVersion` (`2026-07-28`).
- **Transporte HTTP/SSE:** Exige validação de OAuth 2.1, Resource Indicators (RFC 8707) e proteção contra SSRF/DNS Rebinding.

---

## 2. Agent-to-Agent Protocol (`A2A v1.0`)

### 2.1. Estrutura Obrigatória do `agent-card.json`
Localização padrão: `/.well-known/agent-card.json` (ou espelho na raiz `agent_card.json`).
- `name` (`string`): Identificador legível do nó agêntico.
- `description` (`string`): Propósito operacional do agente.
- `version` (`string`): Versão semântica do manifesto.
- `supportedInterfaces` (`array`): Lista de endpoints contendo `url`, `protocolBinding` (`"JSONRPC"` ou `"gRPC"`) e `protocolVersion` (`"1.0"`).
- `defaultInputModes` / `defaultOutputModes` (`array`): MIME types suportados (ex: `["text/plain", "application/json"]`).
- `skills` (`array`): Catálogo de habilidades expostas pelo agente com `id`, `name`, `description` e `tags`.
- `signatures` (`array`): Assinatura JWS sobre JSON Canônico (RFC 8785 JCS + RFC 7515 JWS) garantindo autenticidade e integridade contra *impersonation* e MITM.

### 2.2. Máquina de Estados de Tarefas A2A (`TaskState`)
Transições válidas exigidas em gerenciadores de tarefas A2A:
- `TASK_STATE_SUBMITTED` $\rightarrow$ `TASK_STATE_WORKING`
- `TASK_STATE_WORKING` $\rightarrow$ `TASK_STATE_INPUT_REQUIRED` (Portão HITL para ações `RiskLevel.CRITICAL`)
- `TASK_STATE_WORKING` $\rightarrow$ `TASK_STATE_COMPLETED` | `TASK_STATE_FAILED`
- `TASK_STATE_SUBMITTED` $\rightarrow$ `TASK_STATE_REJECTED` (Bloqueio imediato pelo `SemanticGuard` contra *Prompt Injection*)

---

## 3. Padrões de Loops Cognitivos e Travas Operacionais

| Linguagem | Frameworks Reconhecidos | Indicadores de Padrão de Raciocínio | Travas de Profundidade (`has_max_steps`) | Condição de Parada (`has_stop_condition`) |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | Google ADK 2.x, LangGraph (`StateGraph`), CrewAI, FastMCP, Orquestradores Custom | `ReAct`, `StateGraph`, `Chain-of-Thought`, `AgentOrchestrator`, `DAGEngine` | `max_steps`, `max_retries`, `max_turns`, `max_iterations`, `recursion_limit` | `stop_condition`, `END`, `Read-After-Write`, `COMPLETED`, `APPROVED` |
| **TypeScript** | `@modelcontextprotocol/sdk`, LangGraph.js, Genkit TS, OpenAI Agents SDK | `ReAct`, `StateGraph`, `defineFlow`, `tool_use` | `maxSteps`, `maxRetries`, `maxTurns`, `recursionLimit` | `stopCondition`, `isTerminal`, `COMPLETED` |
| **Go** | Google ADK Go v2 (`google.golang.org/adk`), `mcp-go`, Orquestradores Go | `ReAct`, `Dual-Track`, `CognitiveRouter`, `Runner` | `MaxSteps`, `MaxTurns`, `MaxRetries`, `context.WithTimeout` | `StopCondition`, ` Verify`, `COMPLETED` |

---

## 4. Contratos de Dados Estritos (Prevenção de Alucinação de Parâmetros)

- **Pydantic v2 (Python):** `model_config = ConfigDict(extra="forbid")`
- **Zod (TypeScript):** `z.object({...}).strict()`
- **JSON Schema / MCP Tool Input Schema:** `"additionalProperties": false`
