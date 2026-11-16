---
trigger: model_decision
description: "Official guidelines for configuring and implementing MCP servers (mcp_config.json, STDIO stdout reserved exclusively for JSON-RPC, Streamable HTTP without legacy SSE) and JSON-RPC 2.0 / WebSockets (wss:// TLS 1.3, strict validation, and backoff)."
---

# Official Rules for MCP (`mcp_config.json`), JSON-RPC 2.0 & WebSockets

## 1. `mcp_config.json` Governance in Antigravity

- **Sources & Naming:** Global config at `~/.gemini/config/mcp_config.json` (synced via Single Source `dev/tools/mcp-registry.json` -> `uv run dev/tools/mcp_registry.py apply` + `check`) or plugin-scoped at `plugins/<name>/mcp_config.json` (loaded only when the plugin is active). Server names in code/APIs must match `^[a-z0-9_-]+$`; preserve extension-generated prefixes (`datacloud_*_remote`).
- **Deterministic Binaries & Packages:** Always invoke pre-compiled local binaries (`gopls.exe`, `adk-go-mcp.exe`) — `go run ...@latest` is forbidden. `npx` packages require exact pinned versions published `>= 2` weeks ago (never `@latest`). On Windows, inject `PYTHONUTF8=1` for Python stdio subprocesses.
- **Verified CLI Flags:** Confirm every CLI binary supports a flag before placing it in `args` (e.g., omit `--eager` if the binary does not expose it).

## 2. MCP Transports & `STDIO` Hygiene

- **`stdio` (Local — `command`, `args`, `env`):** `stdout` is **100% exclusive to newline-delimited JSON-RPC 2.0 frames**. Forbid bare `print()` without `file=sys.stderr` in Python, `console.log()` in Node, and `fmt.Println()` in Go; route all logs to `stderr` or log files.
- **`Streamable HTTP` (Remote — `url` / `serverUrl`):** Point `url` to the Streamable HTTP endpoint (`/mcp`). **Legacy HTTP+SSE (`2024-11-05` `/sse`) is not directly supported** (wrap via a stdio bridge such as `mcp-remote` only when unavoidable). Enforce OAuth 2.1 / Bearer auth on protected endpoints, `MCP-Protocol-Version`/`_meta` support, and anti-SSRF URL validation.

## 3. JSON-RPC 2.0 & WebSocket (`wss://`) Contracts

- **Strict Contracts:** Every JSON-RPC envelope requires `"jsonrpc": "2.0"` and mutual exclusivity between `"result"` and `"error"` (`-32700` Parse, `-32600` Invalid Request, `-32601` Method not found, `-32602` Invalid params, `-32603` Internal error). Validate internal RPC/MCP DTOs with `extra="forbid"` (Pydantic), `z.strictObject()` (Zod), or `DisallowUnknownFields()` (Go — allowing documented tolerance for evolving external payloads).
- **WebSockets (`wss://`):** Forbid `ws://` in production; require TLS 1.3 validating the system CA bundle or mTLS (avoid brittle static SSL Pinning on cloud domains with frequent cert rotation). Never place secret tokens in URL query strings (use `Authorization` headers or Ephemeral Tokens) and apply *Exponential Backoff + Jitter* on reconnects.
- **Mandatory Zero-Trust Tests:** Every authenticated/guarded route or tool must have adversarial tests proving deterministic rejection (`400`/`401`/`403` without leaking secrets).
