---
trigger: glob
globs: "**/agents/*.md"
description: "Load when authoring, configuring, or auditing declarative Antigravity subagents (agents/*.md, explicit native tools, Least Privilege read-only auditors, commandExecutionPolicy, max_steps/HITL gates, Context Fork, or parallel [P] waves). Do NOT load when merely calling invoke_subagent or send_message."
---

# Official Guidelines for Declarative Subagents (`agents/*.md`) & Orchestration

1. **Discovery Paths & Safe Names:**
   - Workspace: `.agents/agents/<name>.md`; Global: `~/.gemini/config/agents/<name>.md`; Plugin: `plugins/<plugin>/agents/<name>.md`.
   - Never collide `name` with built-in agents (`self`, `research`, `browser`, `deepagent`, `review-agent`) or existing manifest subagents.

2. **Frontmatter, Language & Least Privilege:**
   - Write all subagent manifests and instructions in **Technical English**, adding `## User Communication Rule` so user-facing summaries remain in **Portuguese (`pt-BR`)**.
   - Canonical fields: `name`, `description` (required — guides coordinator delegation), `subagent: true`, `mainAgent: false` (`mainAgent: true` only for top-level entry-point agents invoked via `--agent`), and `inheritCustomizations: true` (unified master switch in Antigravity 2.x that propagates skills, rules, plugins, subagents, and MCP servers; omitting or setting `false` isolates the subagent).
   - **Explicit Native Tools (`tools: [...]` MANDATORY):** Always declare `tools` explicitly using native Antigravity 2.0 tool names (`read_file`, `edit_file`, `write_file`, `run_command`, `manage_task`, `search_web`, `invoke_subagent`, `send_message`), because omitting `tools:` falls back to a minimal read-only toolset. Bind MCP tools via `mcpServers`/`inheritMcp` — **do not list `call_mcp_tool` in `tools:`**. **Strictly forbid** `tools: ["*"]`, `call_mcp_tool`, and legacy Antigravity 1.x tool names (`view_file`, `list_dir`, `find_by_name`, `grep_search`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`). Never emit legacy keys (`enable_write_tools`, `enable_mcp_tools`, `enable_subagent_tools`, `wave`, `parent_persona`, `covered_modules`).
   - **Auditors / Observers / Gatekeepers:** Enforce read-only least privilege by omitting `write_file` and `edit_file` from `tools:` (`tools: [read_file, run_command, send_message]` or `[read_file, send_message]`), setting `commandExecutionPolicy: sandbox` or `"off"`, and omitting `invoke_subagent` unless the subagent is an explicit coordinator.
   - **Model & Policy:** Use `model: inherit` (never hardcode deprecated models such as `gemini-2.5-flash`/`2.5-pro`, `antigravity-preview-05-2026`, or `3.1-flash-live-preview`; the host/Orchestrator routes between `Gemini 4 Carbon`/`Argon` for planning and `Gemini 4 Hydrogen` for execution), and set `commandExecutionPolicy: auto | sandbox | "off"`, `inheritMcp`, and `inheritCustomizations` accurately.

3. **Containment, Loops & HITL Gates:**
   - Subagents operating loops or tools must define deterministic limits (`max_steps`, `max_turns`, or `recursion_limit`), a verifiable `stop_condition`, and mandatory HITL pause before destructive mutations, `.env`/secret changes, or external side effects.

4. **Context Fork & Parallel Collision Prevention (`[P]`):**
   - Never pass raw chat transcripts between coordinator and subagents; inject only a compact state envelope and `<= 5` operational rules.
   - In parallel waves (`invoke_subagent` or `swarm` with `workspace: "share"` for concurrent authors and `"inherit"` for readers/verifiers), forbid concurrent writes to the same file and always perform **Read-After-Write** verification upon fan-in.
