---
trigger: model_decision
description: "Load when creating, editing, debugging, or validating Antigravity Plugins (plugin.json JSONC, config.json enablement, agy plugin validate, assets) or Lifecycle Hooks (hooks.json, PreToolUse, PostToolUse, SessionStart, PreInvocation, PostInvocation, Stop, CORTEX_STEP_TYPE_* matchers, and camelCase stdin/stdout contracts). Do NOT load for standard skill execution or application coding."
---

# Official Rules for Plugins (`plugin.json`) & Lifecycle Hooks (`hooks.json`)

## 1. Plugins (`plugins/<plugin-dir>/plugin.json`)

- **Identity & Deduplication:** `plugin.json` (JSONC) accepts strictly these top-level keys: `name` (globally unique kebab-case — `name` collisions cause the second plugin to be **silently dropped**), `description`, `logo`, `suggestedPrompts` (max `3`), `displayName`, `version`, `author`, `homepage`, `repository`, and `disabled`. **Unknown fields are silently ignored** by the loader.
- **Logo & Assets:** `logo` must be a relative path inside the plugin directory (`.png`, `.svg`, `.jpg`, `.jpeg`, or `.webp`, square `>= 128x128` with ~10% margin); external URLs and absolute paths fail silently.
- **Hook Placement:** The native plugin runtime loads `hooks.json` **directly at the plugin root** (`<plugin_dir>/hooks.json`); verify bundles with `agy plugin validate <dir> --strict --json`.
- **Enablement:** `config.json` (`plugins.<dir>.enabled`) always overrides `disabled` in `plugin.json`. Root `README.md` is ignored by the agent runtime.

## 2. Lifecycle Hooks (`hooks.json`)

- **Schema:** JSON object mapping `<hook-name>` to `enabled` (`bool`) and event arrays:
  - **Grouped by `matcher` regex + `hooks[]`:** `PreToolUse` and `PostToolUse` (`"matcher": "*"`, `"run_command"`, `"run_command|edit_file"`, `"browser_.*"` — lowercase `CORTEX_STEP_TYPE_*` names).
  - **Flat arrays:** `SessionStart`, `PreInvocation`, `PostInvocation`, and `Stop`.
- **Handlers (`type: "command"` only):** Fields `type`, `command` (`sh -c` Unix / `cmd /c` Windows; CWD is `hooks.json`'s directory), and `timeout` (default `30s`). Plugins expose `PLUGIN_ROOT` and `PLUGIN_DATA`; execution is always synchronous and blocking.
- **`camelCase` I/O Contract (`stdin` -> pure JSON `stdout`):**
  - Common input provides `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName`, `lastUserInput`, `hookEventName`, and `cwd` (agent working directory).
  - **`PreToolUse`:** return `{"decision": "allow"|"deny"|"ask"|"force_ask", "reason"?: "...", "permissionOverrides"?: [...], "overwrite"?: {...}}` (`overwrite` shallow-merges into `toolCall` arguments).
  - **`PostToolUse`:** receives `"toolCall"` and optional `"error"`; **MUST print exactly `{}`** to `stdout` (never emit unsupported `"result"` keys).
  - **`SessionStart` / `PreInvocation` / `PostInvocation`:** return `{"injectSteps": [{"systemMessage": {"systemMessage": "...", "metadata": {"user_markdown"?: "..."}}}], "terminationBehavior"?: ""|"terminate"|"force_continue"}` (`systemMessage` requires a nested object; `ephemeralMessage` is deprecated; `errorMessage` requires `{"userMessage": "..."}` and stops only with `"terminationBehavior": "terminate"`).
  - **`Stop`:** check `continuationActive` before continuing to avoid infinite loops; return `{"decision": "continue", "reason": "..."}` to re-enter the loop.
