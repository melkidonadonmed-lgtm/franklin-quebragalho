# Agentic Project Structure & 4 Audit Dimensions — `agent-server-auditor`

Operational directory and requirement reference used by [`SKILL.md`](../SKILL.md), complementing [`protocol_matrix.md`](protocol_matrix.md), [`audit-websocket-jsonrpc.md`](audit-websocket-jsonrpc.md), and [`audit_report_schema.md`](audit_report_schema.md).

## Canonical Antigravity / ADK Project Layout

```text
agentic-project-root/
├── AGENTS.md / GEMINI.md              # Root operational kernel (no frontmatter)
├── .agents/
│   ├── AGENTS.md                      # Mirrored governance & workspace profile (external repos)
│   ├── rules/*.md                     # Modular rules (YAML trigger required, <= 24KB)
│   ├── skills/<name>/SKILL.md         # Local skills (Progressive Disclosure L1-L3)
│   └── agents/*.md                    # Declarative subagents enforcing Least Privilege
├── .context/                          # context.md (live state) and spec.md (I/O contracts)
├── mcp_config.json / plugin.json      # MCP servers (pre-compiled binaries) and plugin manifest
├── hooks/hooks.json & sidecars/       # Deterministic camelCase hooks and sidecar.json
├── bin/                               # Exclusive destination for compiled binaries (.exe, .so)
├── .well-known/agent-card.json        # Public A2A v1.0 identity with unique IDs & JWS
├── memories/audit_report.json         # Auditable snapshot with metadata, UTC timestamp & score
└── tests/                             # Deterministic test suite (happy-path + Zero-Trust adversarial)
```

## Dimension Criteria

- **Dimension 1 — Binaries (`AUD-BIN-01`):** `.gitignore`, clean `.env.example` without secrets, and `.exe`/`.dll`/`.so`/`.dylib`/`.asar`/`.bin` artifacts confined to `bin/`, `dist/`, or `build/`.
- **Dimension 2 — Agents & Skills (`AUD-AGT-01` / `AUD-SKL-01`):** Valid `ast.parse`/TS/Go/YAML syntax; real non-placebo implementation (no `pass`/`NotImplementedError`); active SDKs (`google-genai>=3.3.0`, `@google/genai>=3.3.0`, `google.golang.org/genai>=1.77.0`, `com.google.genai:google-genai>=2.3.0`, `googleapis/kotlin-genai>=2.1.0`, `Google.GenAI>=2.1.0`, `google-adk>=2.14.1` `<3` GenAI, `google.golang.org/adk/v2>=2.7.1`, `@google/adk>=2.5.0`, `StateGraph`, `FastMCP`; remember `python/js>=3.0` and `java/kotlin/dotnet>=2.0` switched Developer API default from `v1beta` to `v1`, requiring `api_version='v1beta'` for `decisions`/`interactions`); block `gemini-2.5-flash`/`2.5-pro`, `3.1-*tts-preview`, `3.1-flash-live-preview`, `antigravity-preview-05-2026`, `gemini-omni-1.1-flash`, `gemini-3.8-flash-lite`, and `generation_config` on Managed Antigravity Agent (`max_output_tokens` is supported on `generateContent`/`interactions.create`); enforce `max_steps`/`max_turns`/`recursion_limit`, `stop_condition`, HITL, and Least Privilege (`commandExecutionPolicy: "readOnly"` for auditors, zero `tools: ["*"]`/`call_mcp_tool`, no legacy `enable_write_tools`/`wave`/`parent_persona`). Skills enforce `name <= 64`, no `.agents/workflows/*.md`, and L3 on demand (`<= 1,200` tokens in L2).
- **Dimension 3 — MCP `2026-07-28`, WS/JSON-RPC & A2A v1.0 (`AUD-MCP-01` / `AUD-A2A-01`):** Valid SDK in manifests (`mcp`/`fastmcp`, `@modelcontextprotocol/sdk`, `mcp-go`/ADK); STDIO hygiene (zero `print()`/`console.log()`/`fmt.Println()` to `stdout`); `extra="forbid"` / `.strict()` / `additionalProperties: false`, `_meta`/`MCP-Protocol-Version`, OAuth 2.1/anti-SSRF; `wss://` TLS 1.3 with CA/mTLS (no static pinning on rotating cloud certs), Ephemeral Tokens, Exponential Backoff + Jitter, mutually exclusive JSON-RPC 2.0 (`result` vs. `error`); A2A `name`/`description`/`version`/`supportedInterfaces`/unique `skills[].id` + JWS RFC 7515/8785 `signatures`.
