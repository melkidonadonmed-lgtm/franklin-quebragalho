# Deterministic Audit and Rejection Criteria (`agent-server-auditor` v1.2.0)

Every rule below MUST be evaluated deterministically by `scripts/agent_server_auditor.py` and reported using `[PASS]` or `[FAIL: <RULE_ID>]`.

---

## Falsifiable Rule Matrix

| Rule ID | Dimension | Severity | Approval Criterion (`[PASS]`) | Failure Condition (`[FAIL]`) |
| :--- | :--- | :---: | :--- | :--- |
| **`AUD-BIN-01`** | 1. Hygiene & Binaries | **CRITICAL** | `[PASS]` `.gitignore` present and zero compiled binaries (`.exe`, `.dll`, `.so`, `.dylib`, `.asar`) outside `bin/`, `dist/`, or `build/`. | `[FAIL: AUD-BIN-01]` Loose binaries in root/source directories or missing `.gitignore`. |
| **`AUD-SKL-01`** | 2. Modular Skills | **HIGH** | `[PASS]` Every directory in `skills/<name>/` or `.agents/skills/<name>/` has `SKILL.md` with valid YAML frontmatter (`name`, `description`) and applies Level 3 Progressive Disclosure (`references/`/`scripts/`) when L2 > `1,000` tokens. | `[FAIL: AUD-SKL-01]` `SKILL.md` missing valid frontmatter or suffering from Context Bloat without L3 decoupling. |
| **`AUD-AGT-01`** | 2. Agents & Loops (8 Axes) | **CRITICAL** | `[PASS]` Agents (`Go`, `TypeScript`, `Python`, `agents/*.md`) have valid syntax, real non-placebo implementation, active SDK/models, `max_steps`/`stop_condition`, explicit policy, and **Least Privilege** (zero `tools: ["*"]` in Antigravity subagents). | `[FAIL: AUD-AGT-01]` Loop missing `max_steps`, syntax error, placebo function, retired model/SDK, or Least Privilege violation. |
| **`AUD-MCP-01`** | 3. MCP Servers (SDK + Runtime) | **CRITICAL** | `[PASS]` MCP server declares valid SDK in manifest and reserves `stdout` exclusively for JSON-RPC 2.0 over `STDIO` (logs routed to `stderr`). | `[FAIL: AUD-MCP-01]` Direct `print()`, `console.log()`, or `fmt.Println()` to `stdout` in an STDIO MCP server or missing SDK. |
| **`AUD-CNT-01`** | 4. Data Contracts | **HIGH** | `[PASS]` Tool schemas and payloads enforce strict validation (`extra="forbid"` in Pydantic v2, `.strict()` in Zod, `DisallowUnknownFields()` in Go, or `additionalProperties: false` in JSON Schema). | `[FAIL: AUD-CNT-01]` Permissive input schemas allowing hallucinated fields. |
| **`AUD-A2A-01`** | 3. A2A v1.0 Protocol | **HIGH** | `[PASS]` Agent Card (`/.well-known/agent-card.json` or `agent_card.json`) declares metadata (`name`, `description`, `version`), `supportedInterfaces`, unique `skills[].id`, and JWS `signatures`. | `[FAIL: AUD-A2A-01]` A2A card missing metadata, with duplicate/empty `skills[].id`, or unsigned (missing JWS). |
| **`AUD-MEM-01`** | 4. Auditable Memory | **MEDIUM** | `[PASS]` Final report serialized with UTC timestamp and persisted at `memories/audit_report.json`. | `[FAIL: AUD-MEM-01]` Audit run without emitting or persisting the structured audit snapshot. |
