# Agentic Protocol Compliance Matrix (`MCP 2026-07-28`, `A2A v1.0`, `Gemini API` & `WebSockets/JSON-RPC 2.0`)

Technical reference document for **`agent-server-auditor`** supporting polyglot static and contractual inspection (**Python**, **TypeScript**, and **Go**).

---

## 0. Pre-Flight Documentation Grounding (Never Audit Blindly)

Before auditing any API client/server, model ID, or protocol layer, consult official active documentation:

- **Official Gemini API Docs & Antigravity Agent Portal:** [`https://aistudio.google.com/docs`](https://aistudio.google.com/docs) | [`https://aistudio.google.com/docs/antigravity-agent`](https://aistudio.google.com/docs/antigravity-agent)
- **Gemini API / Google AI Studio Docs Index (`llms.txt`):** [`https://aistudio.google.com/llms.txt`](https://aistudio.google.com/llms.txt)
- **Gemini API / Google AI Studio Full Corpus (`llms-full.txt`):** [`https://aistudio.google.com/llms-full.txt`](https://aistudio.google.com/llms-full.txt)
- **Google Gemini Cookbook (GitHub):** [`https://github.com/google-gemini/cookbook`](https://github.com/google-gemini/cookbook)
- **Google ADK Docs (`llms.txt` & `llms-full.txt`):** [`https://adk.dev/llms.txt`](https://adk.dev/llms.txt) | [`https://adk.dev/llms-full.txt`](https://adk.dev/llms-full.txt)
- **WebSockets & JSON-RPC 2.0 Sub-Spec:** [`audit_websocket_jsonrpc.md`](audit_websocket_jsonrpc.md)

---

## 1. Model Context Protocol (`MCP Spec 2026-07-28`)

### 1.1. Stream Hygiene on `STDIO` Transport

- **Canonical Rule:** On `STDIO` transport, file descriptor `stdout` is exclusively the `JSON-RPC 2.0` message bus. Any non-JSON-RPC byte written to `stdout` corrupts the MCP client parser.
- **Forbidden Patterns in STDIO Servers (`stdout_hygiene = "POLLUTED"`):**
  - **Python:** `print(...)` without `file=sys.stderr`.
  - **TypeScript / Node.js:** `console.log(...)` or `process.stdout.write(...)` with log output.
  - **Go:** `fmt.Println(...)`, `fmt.Printf(...)`, or `log.Println(...)` without redirecting `log.SetOutput(os.Stderr)`.
- **Safe Patterns (`stdout_hygiene = "CLEAN"`):**
  - **Python:** `logging.StreamHandler(sys.stderr)`, `print(..., file=sys.stderr)`.
  - **TypeScript:** `console.error(...)`, `process.stderr.write(...)`.
  - **Go:** `fmt.Fprintln(os.Stderr, ...)`, `slog.New(slog.NewJSONHandler(os.Stderr, nil))`.

### 1.2. MCP Primitives and Contracts

- **Exposed Primitives:** Explicit declaration of `tools` (`@mcp.tool`), `resources` (`@mcp.resource`), and `prompts` (`@mcp.prompt`).
- **Stateless Core & Metadata:** Support `_meta` with `io.modelcontextprotocol/protocolVersion` (`2026-07-28`).
- **Streamable HTTP Transport:** Require OAuth 2.1 validation, Resource Indicators (RFC 8707), and SSRF / DNS Rebinding protection.

---

## 2. Agent-to-Agent Protocol (`A2A v1.0`)

### 2.1. Mandatory `agent-card.json` Structure

Standard location: `/.well-known/agent-card.json` (or mirrored at `agent_card.json` at root).

- `name` (`string`): Human-readable identifier of the agentic node.
- `description` (`string`): Operational purpose of the agent.
- `version` (`string`): Semantic version of the manifest.
- `supportedInterfaces` (`array`): Endpoints declaring `url`, `protocolBinding` (`"JSONRPC"` or `"gRPC"`), and `protocolVersion` (`"1.0"`).
- `defaultInputModes` / `defaultOutputModes` (`array`): Supported MIME types (e.g., `["text/plain", "application/json"]`).
- `skills` (`array`): Exposed skill catalog with unique `id`, `name`, `description`, and `tags`.
- `signatures` (`array`): JWS signature over Canonical JSON (RFC 8785 JCS + RFC 7515 JWS) guaranteeing authenticity and anti-impersonation / anti-MITM integrity.

### 2.2. A2A Task State Machine (`TaskState`)

Valid state transitions enforced in A2A task managers:

- `TASK_STATE_SUBMITTED` $\rightarrow$ `TASK_STATE_WORKING`
- `TASK_STATE_WORKING` $\rightarrow$ `TASK_STATE_INPUT_REQUIRED` (HITL Gate for `RiskLevel.CRITICAL` actions)
- `TASK_STATE_WORKING` $\rightarrow$ `TASK_STATE_COMPLETED` | `TASK_STATE_FAILED`
- `TASK_STATE_SUBMITTED` $\rightarrow$ `TASK_STATE_REJECTED` (Immediate block by `SemanticGuard` on Prompt Injection)

---

## 3. WebSockets (`ws://` / `wss://`) & JSON-RPC 2.0 Contracts ([`audit_websocket_jsonrpc.md`](audit_websocket_jsonrpc.md))

- **Transport & Authentication:** Mandatory `wss://` (TLS 1.3) in production; credentials via `Authorization: Bearer <token>` header or Ephemeral Tokens (permanent API keys in query strings are forbidden).
- **Resilience & Reconnection:** `ping`/`pong` heartbeat (15–30s), Exponential Backoff with Jitter ($t_{\text{wait}} = \min(t_{\text{max}}, t_{\text{base}} \times 2^{\text{attempt}}) + \text{jitter}$), and bounded queue for pending outbound frames.
- **JSON-RPC 2.0 Contract:** Explicit `"jsonrpc": "2.0"`, mutual exclusivity between `"result"` and `"error"`, strict `"id"` matching (and omission of `"id"` on notifications), standard error codes `-32700` to `-32603`, max frame size $\le 1\text{ MB}$, $RTT_{\text{avg}} < 150\text{ ms}$, and $\text{Pass}@3 \ge 0.95$.

---

## 4. Cognitive Loop Patterns & Operational Guards

| Language | Recognized Frameworks | Reasoning Pattern Indicators | Depth Guards (`has_max_steps`) | Stop Conditions (`has_stop_condition`) |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | Google ADK 2.x, LangGraph (`StateGraph`), CrewAI, FastMCP, Custom Orchestrators | `ReAct`, `StateGraph`, `Chain-of-Thought`, `AgentOrchestrator`, `DAGEngine` | `max_steps`, `max_retries`, `max_turns`, `max_iterations`, `recursion_limit` | `stop_condition`, `END`, `Read-After-Write`, `COMPLETED`, `APPROVED` |
| **TypeScript** | `@modelcontextprotocol/sdk`, LangGraph.js, Genkit TS, OpenAI Agents SDK | `ReAct`, `StateGraph`, `defineFlow`, `tool_use` | `maxSteps`, `maxRetries`, `maxTurns`, `recursionLimit` | `stopCondition`, `isTerminal`, `COMPLETED` |
| **Go** | Google ADK Go v2 (`google.golang.org/adk`), `mcp-go`, Go Orchestrators | `ReAct`, `Dual-Track`, `CognitiveRouter`, `Runner` | `MaxSteps`, `MaxTurns`, `MaxRetries`, `context.WithTimeout` | `StopCondition`, `Verify`, `COMPLETED` |

---

## 5. Strict Data Contracts (Preventing Parameter Hallucination)

- **Pydantic v2 (Python):** `model_config = ConfigDict(extra="forbid")`
- **Zod (TypeScript):** `z.object({...}).strict()`
- **Go (`encoding/json`):** `dec.DisallowUnknownFields()`
- **JSON Schema / MCP Tool Input Schema:** `"additionalProperties": false`

---

## 6. Active Models & Official SDK Baseline (`SSOT Pointer`)

Do not duplicate model/SDK blocklists here; enforce the single authoritative baseline in:
- **Global Model & SDK SSOT:** `rules/authoring-rules-and-google-apis.md` (Gemini 4 `carbon`/`argon`/`hydrogen` + `xhigh`, `gemini-decision-1`, `gemini-3.8-live*`/`tts`, `antigravity-preview-09-2026` Managed Agent `generation_config` split, `v1` vs `v1beta` `HttpOptions`, and active `googleapis` / ADK v2 SDK minimums).
- **Executable Scanner Blocklist:** `scripts/protocol_policy_checks.py` (deterministic regexes blocking retired 1.x/2.0/2.5/3.1 previews, legacy `google-generativeai` SDKs, and disabled doc-search aliases).
- **Primary Docs:** `google-developer-knowledge`, `gemini_get_doc`, `https://aistudio.google.com/llms.txt`, and `https://antigravity.google/docs/models.md`.
