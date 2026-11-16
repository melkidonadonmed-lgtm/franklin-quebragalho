---
name: agent-server-auditor
description: "Audit agentic architectures, MCP 2026-07-28 STDIO stdout hygiene, A2A v1.0 JWS agent-cards, binary hygiene, max_steps loop guards, and persist memories/audit_report.json. Use for auditing agents, MCP/A2A tooling, and WebSockets/JSON-RPC. Do NOT use for frontend UI or unit-test suites."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
metadata:
  version: "1.2.0"
  updated_at: "2026-11-16"
  author: "Franklin"
  category: "Agent Architecture, MCP/A2A Protocol & Static Auditing"
  tags: ["agent-server-auditor", "auditar", "sistemas", "agenticos", "servidores", "agente", "skills", "mcp", "mcp-2026-07-28", "stdio", "stdout", "stdio-hygiene", "a2a", "a2a-protocol", "agent-card", "agent-card-jws", "jws", "binarios", "max_steps", "max-steps", "least-privilege", "audit_report", "audit-report"]
---

# `agent-server-auditor` (`v1.2.0`) — Agent, MCP, WS/JSON-RPC & A2A Auditor

## 1. Overview & Scope

Runs deterministic static and contractual audits across **Python, TypeScript, and Go** agentic projects, serving also as the architectural auditor for **MCP/A2A agent tooling** (legacy `audit-skills-antigravity` retired into `scripts/validate_skills.py`):
- Audits **MCP (`2026-07-28`)** servers, subagents (`agents/*.md`), **A2A v1.0 JWS** (`/.well-known/agent-card.json`), and binaries.
- **Pre-Flight:** Ground Gemini/ADK checks via `google-developer-knowledge`, `gemini_get_doc` (`chunk_id`), `aistudio.google.com/llms.txt`, or [`references/protocol_matrix.md`](references/protocol_matrix.md) (never disabled aliases); apply [`references/audit-websocket-jsonrpc.md`](references/audit-websocket-jsonrpc.md) for `ws://`/`wss://` or JSON-RPC 2.0.
- **When NOT to Use:** Do NOT use for UI/OKLCH (`frontend-testing-auditor`, `complex-zero`), test AAA grading (`test-quality-auditor`), or Python AST gates (`code-acceptability-auditor`).

## 2. Inputs & Prerequisites

- **`--root`** (default `.`), **`--persist` / `--output`** (`memories/audit_report.json`), **`--self-test`**.

## 3. Step-by-Step Procedure

Consult [`references/agentic_project_structure.md`](references/agentic_project_structure.md) and [`references/protocol_matrix.md`](references/protocol_matrix.md):
1. **D1 — Binaries (`AUD-BIN-01`):** Check `.gitignore`, clean `.env.example`, and isolate binaries in `bin/`/`dist/`/`build/`.
2. **D2 — Agents & Skills (`AUD-AGT-01` / `AUD-SKL-01`):** Verify valid syntax, zero placebos, active SDKs (`google-genai>=3.3.0`, `@google/genai>=3.3.0`, `google.golang.org/genai>=1.77.0`, `api_version='v1beta'` for `decisions`/`interactions`), Gemini 4 (`hydrogen` w/ `xhigh`, `argon`, `carbon`, `max_output_tokens` on `generateContent`/`interactions.create`), block retired `gemini-2.5-flash`/`2.5-pro`/`3.1-flash-live-preview`/`antigravity-preview-05-2026`, enforce `max_steps`, Least Privilege (`readOnly`, no `tools: ["*"]`/`call_mcp_tool`), and L3 disclosure.
3. **D3 — MCP & A2A (`AUD-MCP-01` / `AUD-A2A-01`):** Verify MCP SDK, clean STDIO `stdout`, strict schemas (`extra="forbid"` / `.strict()`), unique `skills[].id`, and JWS signatures.
4. **D4 — Run (`AUD-CNT-01` / `AUD-MEM-01`):**
```powershell
uv run python skills/agent-server-auditor/scripts/agent_server_auditor.py --root . --persist --json
uv run python skills/agent-server-auditor/scripts/agent_server_auditor.py --self-test
```

## 4. Gotchas & Edge Cases

- `agent_server_auditor.py` is static; live WebSocket latency ($RTT_{\text{avg}} < 150\text{ ms}$) requires a live endpoint.
- STDIO `stdout` pollution (`AUD-MCP-01`), loose binaries (`AUD-BIN-01`), or missing `max_steps` (`AUD-AGT-01`) yields `REJECTED`.

## 5. Output Schema & Validation Criteria

Emit Pydantic-validated (`extra="forbid"`) JSON in `memories/audit_report.json` per [`references/audit_report_schema.md`](references/audit_report_schema.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md) with `[PASS]` / `[FAIL: <RULE_ID>]`.

## 6. User Communication Rule

All direct responses, audit findings, clarifying questions, and summaries presented to the user MUST be written in **Portuguese (Brazil / `pt-BR`)**, unless explicitly requested otherwise.
