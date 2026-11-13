---
trigger: model_decision
description: "Diretrizes oficiais do Google Antigravity para criar e validar Plugins (plugin.json JSONC, namespaces, assets) e Lifecycle Hooks (hooks.json, contratos camelCase PreToolUse, PostToolUse, SessionStart, PreInvocation, PostInvocation e Stop)."
---

# Regras Oficiais para Plugins (`plugin.json`) e Hooks (`hooks.json`)

## 1. Plugins (`plugins/<plugin-dir>/plugin.json`)

- **Identidade & Deduplicação:** `plugin.json` (JSONC) aceita exclusivamente os campos top-level: `name` (kebab-case globalmente único — colisão de `name` faz o segundo plugin ser **descartado silenciosamente**), `description`, `logo`, `suggestedPrompts` (máx. `3`), `displayName`, `version`, `author`, `homepage`, `repository` e `disabled`. **Campos desconhecidos são ignorados em silêncio** pelo loader.
- **Logo & Assets:** `logo` deve ser caminho relativo ao diretório do plugin (`.png`, `.svg`, `.jpg`, `.jpeg` ou `.webp`, quadrado `>= 128x128` com ~10% de margem); URLs externas e caminhos absolutos falham silenciosamente.
- **Staging de Hooks no Plugin:** Runtime nativo de plugins carrega `hooks.json` **diretamente na raiz do plugin** (`<plugin_dir>/hooks.json`); extensões convertidas via `agy plugin install` usam staging, mas bundles nativos com `plugin.json` devem garantir `hooks.json` na raiz do pacote instalado (`agy plugin validate <dir> --strict --json`).
- **Habilitação:** `config.json` (`plugins.<dir>.enabled`) sempre vence `disabled` do `plugin.json`. `README.md` na raiz é ignorado pelo agente.

## 2. Lifecycle Hooks (`hooks.json`)

- **Formato:** Objeto JSON mapeando `<hook-name>` para `enabled` (`bool`) e arrays de eventos:
  - **Agrupados por `matcher` regex + `hooks[]`:** `PreToolUse` e `PostToolUse` (`"matcher": "*"`, `"run_command"`, `"run_command|edit_file"`, `"browser_.*"` — nomes derivados do `CORTEX_STEP_TYPE_*` em minúsculas).
  - **Planos (array direto de handlers):** `SessionStart`, `PreInvocation`, `PostInvocation` e `Stop`.
- **Handlers (`type: "command"` único suportado):** Campos `type`, `command` (`sh -c` Unix / `cmd /c` Windows; CWD é o diretório de `hooks.json`) e `timeout` (padrão `30s`). Plugins expõem env vars `PLUGIN_ROOT` e `PLUGIN_DATA`; execução é sempre síncrona e bloqueante.
- **Contrato I/O em `camelCase` (`stdin` $\to$ `stdout` JSON puro):**
  - Input comum traz `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName`, `lastUserInput`, `hookEventName` e `cwd` (diretório do agente, diferente do CWD do hook).
  - **`PreToolUse`:** retorna `{"decision": "allow"|"deny"|"ask"|"force_ask", "reason"?: "...", "permissionOverrides"?: [...], "overwrite"?: {...}}` (`overwrite` faz merge raso nos argumentos de `toolCall`).
  - **`PostToolUse`:** recebe `"toolCall"` e `"error"` opcional; **DEVE imprimir exatamente `{}`** em `stdout` (nunca envie campo `"result"` não suportado!).
  - **`SessionStart` / `PreInvocation` / `PostInvocation`:** retorna `{"injectSteps": [{"systemMessage": {"systemMessage": "...", "metadata": {"user_markdown"?: "..."}}}], "terminationBehavior"?: ""|"terminate"|"force_continue"}` (`systemMessage` exige objeto aninhado; `ephemeralMessage` é depreciado; `errorMessage` requer `{"userMessage": "..."}` e só interrompe com `"terminationBehavior": "terminate"`).
  - **`Stop`:** cheque `continuationActive` antes de continuar para evitar loop infinito; retorne `{"decision": "continue", "reason": "..."}` para reentrar no loop.
