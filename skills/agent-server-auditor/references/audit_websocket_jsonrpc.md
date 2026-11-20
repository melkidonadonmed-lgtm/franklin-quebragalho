# Specialist Reference: `audit-websocket-jsonrpc` — WebSockets & JSON-RPC 2.0 Auditing (`v1.2.0`)

## 0. Pre-Flight Documentation Grounding (Protocol-Conditional)

Before auditing or implementing WebSocket (`ws://` / `wss://`) endpoints, **Gemini Live API** sessions, or **JSON-RPC 2.0** buses (`MCP` / `A2A`), verify active specifications and models via `google-developer-knowledge` (`search_documents`/`get_documents`) or `gemini_get_doc` (`chunk_id`; never invoke disabled doc-search aliases), [`protocol_matrix.md`](protocol_matrix.md), and local contracts (`openapi.json`, `.well-known/agent-card.json`, `tools.json`).

---

## 1. Objective and Architectural Mission

This specialist reference defines the operational procedure and engineering checklists to audit, test, and certify bidirectional asynchronous transport over **WebSockets (`ws://` and `wss://`)** and **JSON-RPC 2.0** message contracts.

### Primary Objectives

1. **Handshake & Transport Inspection:** Validate TLS 1.3 (`wss://`), HTTP upgrade headers, JWT/Ephemeral Tokens in authentication headers, and strict CA/mTLS verification (no `rejectUnauthorized: false` or `InsecureSkipVerify: true`).
2. **Connection Resilience:** Audit `ping`/`pong` heartbeat logic, automatic reconnection with Exponential Backoff + Jitter (`SessionResumption` / `GoAway` for Live API), and graceful disconnect handling.
3. **JSON-RPC 2.0 Contract Validation:** Audit parsing of `request`, `response`, `error`, and `notification` frames, ensuring strict request/response `id` correlation (and omission of `id` on notifications).
4. **Quality of Service (QoS):** Measure Round-Trip Time ($RTT_{\text{avg}}$), message throughput, and bounded memory usage under load.
5. **Zero-Trust Security:** Sanitize inputs against injection payloads and prevent PII leakage.

---

## 2. Cognitive Architecture & Subagent Topology

Execution runs in an isolated context (`context: fork`), returning concise findings to the orchestrator on completion:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ 0. PRE-FLIGHT DOCS (llms.txt / llms-full.txt / OpenAPI / AgentCard)     │
│ • Load real API contract (Gemini API, Live API, MCP, A2A)               │
└────────────────────┬────────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. PROTOCOL & HANDSHAKE INSPECTION (wss:// & Headers)                   │
│ • Validate TLS/mTLS, upgrade headers, and initial connection integrity  │
└────────────────────┬────────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. REACT MESSAGE ARCHITECTURE (JSON-RPC 2.0 Validation)                 │
│ • Defensive RPC parsing (jsonrpc: "2.0", method, params, result, error) │
│ • Strict schema validation via Pydantic v2 (extra="forbid") / Zod       │
└────────────────────┬────────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. SELF-REFINE & READ-AFTER-WRITE AUDIT                                 │
│ • Run load and RTT latency test script (ping/pong)                      │
│ • Compute deterministic metrics (Pass@k, Jank/Dropped Frames)           │
│ • Emit Technical Report and persist audit_report.json                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 5-Module Audit Matrix

### Module 1: HTTP Handshake & WebSocket Transport

- **Encryption & Upgrade:** Enforce `wss://` in production; reject unencrypted `ws://` traffic outside localhost sandboxes.
- **Initial Authentication:** Send credentials via `Authorization: Bearer <token>` headers or Ephemeral Tokens (`auth_tokens.create` in Gemini Live API) rather than query parameters in the URL.
- **TLS / mTLS Chain Validation:** Verify certificates against trusted system CAs (or mTLS in internal meshes), blocking `InsecureSkipVerify: true` / `verify=False` and avoiding static SSL pinning against rotating cloud certificates.

### Module 2: JSON-RPC 2.0 Contracts & Syntax

- **Request Structure:**
  - Require fixed `"jsonrpc": "2.0"`.
  - `"method"` formatted in kebab-case, slash-notation (`tools/call`, `initialize`), or dot-notation (e.g., `"orders.create"`).
  - Strictly typed `"params"` (named object `{}` or ordered array `[]`).
- **Response Structure:**
  - Mutually exclusive: MUST contain `"result"` OR `"error"`, never both in one payload.
  - `"id"` MUST exactly match the request `"id"` (notifications such as `notifications/initialized` omit `"id"` and expect no response).
- **Standardized Error Codes (`Error Object`):**
  - `-32700`: Parse error (invalid JSON).
  - `-32600`: Invalid Request (malformed RPC structure).
  - `-32601`: Method not found.
  - `-32602`: Invalid params (schema violation).
  - `-32603`: Internal error.

### Module 3: Resilience, Heartbeat & Reconnection

- **Heartbeat (`Ping`/`Pong`):** Send `ping` frames every 15–30 seconds to keep NAT/proxy mappings alive.
- **Smart Reconnection:** Apply Exponential Backoff with Jitter:
  $$t_{\text{wait}} = \min(t_{\text{max}}, t_{\text{base}} \times 2^{\text{attempt}}) + \text{jitter}$$
- **Bounded Pending Queue:** Verify outbound messages during transient disconnects use a bounded queue to avoid OOM.

### Module 4: Quality of Service (QoS) & Deterministic Metrics

- **RTT Latency ($RTT_{\text{avg}}$):**
  $$RTT_{\text{avg}} = \frac{1}{N} \sum_{i=1}^N (t_{\text{pong}_i} - t_{\text{ping}_i})$$
  - Require $RTT_{\text{avg}} < 150\text{ ms}$ on regional connections.
- **Functional Reliability ($\text{Pass}@k$):**
  $$\text{Pass}@k = 1 - \prod_{i=1}^k \left(1 - \frac{c}{n - k + i}\right)$$
  - Require $\text{Pass}@3 \ge 0.95$ for critical RPC calls.

### Module 5: Zero-Trust Security & Payload Sanitization

- **Max Frame Size:** Cap incoming message size (e.g., $\le 1\text{ MB}$) to prevent DoS exhaustion.
- **Input Sanitization:** Strip control characters and block script/command injections inside string parameters.

---

## 4. Forbidden Practices (Guardrails)

1. **[FORBIDDEN] NEVER audit blindly:** Never audit or implement Gemini API / Live API / Decisions API / JSON-RPC calls without first consulting `google-developer-knowledge` (`search_documents`), `gemini_get_doc` (`chunk_id`), `https://aistudio.google.com/llms.txt`, or `https://aistudio.google.com/llms-full.txt` (never invoke disabled search aliases).
2. **[FORBIDDEN] NEVER use unencrypted remote transport:** Production endpoints require `wss://` / `https://`.
3. **[FORBIDDEN] NEVER pass static credentials in URLs:** Query string API keys leak via proxy and server logs.
4. **[FORBIDDEN] NEVER reconnect without Jitter:** Synchronized reconnect loops trigger Thundering Herd storms.
5. **[FORBIDDEN] NEVER skip `"jsonrpc": "2.0"` validation.**
6. **[FORBIDDEN] NEVER return both `"result"` and `"error"` in the same payload.**
7. **[FORBIDDEN] NEVER leave listen loops without idle timeouts:** Unbounded open sockets leak file descriptors.

---

## 5. Deep Coder / Implementation Instructions

When building WebSocket + JSON-RPC 2.0 clients or servers in **Node.js (`ws`/`socket.io`)**, **Python (`websockets`/`asyncio`)**, or **Go (`gorilla/websocket` / `nhooyr.io/websocket`)**:

1. **Strict Message Typing:**
   - Python: Pydantic v2 with `model_config = ConfigDict(extra="forbid")`.
   - TypeScript: Zod with `.strict()`.
   - Go: strongly typed structs with `dec.DisallowUnknownFields()` rejecting invalid frames with `-32602`.
2. **Resilience Verification Script:** Test forced disconnects and assert reconnect delay falls inside the expected $t_{\text{wait}}$ window.
3. **Manifest Registration:** Update `agents.json` or `/.well-known/agent-card.json` confirming `websockets` and `json-rpc` support.
