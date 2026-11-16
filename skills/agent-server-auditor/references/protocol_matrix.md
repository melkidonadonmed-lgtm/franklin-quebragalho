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
- **WebSockets & JSON-RPC 2.0 Sub-Spec:** [`audit-websocket-jsonrpc.md`](audit-websocket-jsonrpc.md)

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

## 3. WebSockets (`ws://` / `wss://`) & JSON-RPC 2.0 Contracts ([`audit-websocket-jsonrpc.md`](audit-websocket-jsonrpc.md))

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

## 6. Active Baseline — Gemini 4 Models, Decisions API, Live API & Official SDKs (`https://github.com/googleapis`)

- **Canonical Sources (never invoke disabled doc-search aliases):** `google-developer-knowledge` (`search_documents`/`get_documents`), `gemini_get_doc` (`chunk_id`), [`https://aistudio.google.com/llms.txt`](https://aistudio.google.com/llms.txt), [`https://aistudio.google.com/docs/models.md`](https://aistudio.google.com/docs/models.md), [`https://aistudio.google.com/docs/deprecations.md`](https://aistudio.google.com/docs/deprecations.md), [`https://aistudio.google.com/docs/libraries.md`](https://aistudio.google.com/docs/libraries.md), [`https://aistudio.google.com/docs/decisions-api.md`](https://aistudio.google.com/docs/decisions-api.md), [`https://antigravity.google/docs/models.md`](https://antigravity.google/docs/models.md), and [`https://antigravity.google/docs/sdk/overview.md`](https://antigravity.google/docs/sdk/overview.md).
- **Gemini 4 (1M unified context, implicit caching >= 4,096 tokens, no `cachedContents`, `temperature`/`top_p`/`top_k` ignored, 64K default `max_output_tokens` or 1M long decode with `background=True`; note Managed Antigravity Agent `antigravity-preview-09-2026` rejects `generation_config` sampling & `max_output_tokens` with HTTP 400 while standard `generateContent`/`interactions.create` supports `max_output_tokens`):**
  - `gemini-4-carbon`: maximum reasoning (`thinking_level`: `low`, `medium` default, `high`).
  - `gemini-4-argon`: efficient frontier (`thinking_level`: `low`, `medium` default, `high`).
  - `gemini-4-hydrogen`: fast coding/agent default and default model of `antigravity-preview-09-2026` (`thinking_level`: `low`, `medium`, `high` default, **`xhigh`**; `minimal` unsupported).
- **Decisions, Live & Audio/Media:** `gemini-decision-1` (`client.decisions.create` / `POST /v1beta/decisions`, `noul` `0.01-0.99`, `choice`/`score`, 0 output tokens); Live `gemini-3.8-live`, `gemini-3.8-live-extended-thinking` (`NON_BLOCKING`, `interaction_status=="IDLE"`, `proactive_video`, `send_context_update`), `gemini-3.5-transcribe-live`, `gemini-3.5-live-translate-preview`; TTS `gemini-3.8-flash-tts` / `gemini-3.8-flash-lite-tts`; Video `gemini-omni-1.2-flash`.
- **Mandatory Blocklist (Retired / Non-Existent):** `gemini-1.0-*`/`1.5-*`, `gemini-2.0-*`, `gemini-2.5-flash`/`2.5-pro` (shutdown `2026-12-01`; **`gemini-2.5-flash-lite` is NOT deprecated**), `2.5-*-preview-tts` / `gemini-3.1-flash-tts-preview` (`2026-12-18`), `2.5-flash-native-audio*` (`2027-03-31`), `2.5-flash-image` (`2027-03-15`), `gemini-3.1-flash-live-preview` (legacy preview without shutdown -> `gemini-3.8-live`), `gemini-live-2.5-*`, `gemini-omni-1.1-flash` (`2026-12-03`), `antigravity-preview-05-2026` (`2026-10-05`), closed previews (`gemini-3-pro-preview`, `3.1-flash-lite-preview`, `3-pro-image-preview`, `3.1-flash-image-preview`, `2.0-flash-preview-image-generation`, `embedding-2-preview`, `omni-flash-preview`, `deep-research-pro-preview-12-2025`, `2.5-computer-use-preview-10-2025`, `robotics-er-1.[56]-preview`, `text-embedding-004`/`embedding-*`, `imagen-[34].0-*`, `veo-[23].*`), and `gemini-3.8-flash-lite` (non-existent).
- **Official SDKs (`googleapis`), Antigravity SDK & ADK v2:** `google-genai>=3.3.0` (`httpx2`, `--flavor=interactions-eap`), `@google/genai>=3.3.0`, `com.google.genai:google-genai>=2.3.0`, `googleapis/kotlin-genai>=2.1.0`, `google.golang.org/genai>=1.77.0` (`main`: `gemini-4-hydrogen`/`XHIGH`/Decisions/BYOS/`AutomaticContinuation`/`send_context_update`), `Google.GenAI>=2.1.0`, `google-antigravity>=0.1.23` (`from google.antigravity import Agent, LocalAgentConfig`, `vertex=True`), and `gemini-api` CLI (`beta`); block legacy SDKs (`google-generativeai`, `@google/generativeai`, `@google/generative-ai`, `@google-cloud/vertexai`, `google.golang.org/generative-ai`). Since `python/js-genai>=3.0.0` and `java/kotlin/dotnet-genai>=2.0.0`, Developer API default changed to **`v1`** (`vertexai=True`/`enterprise=True` stays `v1beta1`), requiring `HttpOptions(api_version='v1beta')` or `GOOGLE_GENAI_API_VERSION=v1beta` for `decisions`/`interactions`/`antigravity-preview-09-2026`/`*-latest`; `google-adk>=2.14.1` (still pins `google-genai<3`), `google.golang.org/adk/v2>=2.7.1`, `@google/adk>=2.5.0` (pins `@google/genai ^2.29.1`), `google/adk-java>=1.14.0`, `google/adk-kotlin>=1.5.0`, `google/agents-cli>=1.14.0`; `Api-Revision: 2026-05-20`; BYOS environments (`system_instruction`, `custom_config`, `environment_key`).
