---
trigger: model_decision
description: "Diretrizes oficiais para configurar e implementar servidores MCP (mcp_config.json, Stdio stdout exclusivo JSON-RPC, Streamable HTTP sem SSE legado) e integrações JSON-RPC 2.0 / WebSockets (wss:// TLS 1.3, validação estrita e backoff)."
---

# Regras Oficiais para MCP (`mcp_config.json`), JSON-RPC 2.0 e WebSockets

## 1. Governança `mcp_config.json` no Antigravity

- **Fontes e Nomes:** Config global em `~/.gemini/config/mcp_config.json` (sincronizada via Fonte Única `dev/tools/mcp-registry.json` -> `uv run dev/tools/mcp_registry.py apply` + `check`) ou escopada em `plugins/<name>/mcp_config.json` (carrega apenas quando o plugin está ativo). Nomes de servidores em código/API seguem `^[a-z0-9_-]+$`; preserve prefixos gerados por extensões (`datacloud_*_remote`).
- **Binários & Pacotes Determinísticos:** Use executáveis locais pré-compilados (`gopls.exe`, `adk-go-mcp.exe`) — proibido `go run ...@latest`. Pacotes `npx` exigem versão exata publicada há `>= 2` semanas (proibido `@latest`). Em subprocessos stdio Python no Windows, injete `PYTHONUTF8=1`.
- **Flags CLI Reais:** Verifique se o CLI binário suporta flags antes de passá-las em `args` (ex.: omita `--eager` se o binário não expuser a flag).

## 2. Transportes MCP & Higiene `STDIO`

- **`stdio` (Local — `command`, `args`, `env`):** O canal `stdout` é **100% exclusivo para mensagens JSON-RPC 2.0 delimitadas**. Proíba `print()` sem `file=sys.stderr`, `console.log()` em Node ou `fmt.Println()` em Go; envie logs somente para `stderr` ou arquivo.
- **`Streamable HTTP` (Remoto — `url` / `serverUrl`):** Aponte `url` para o endpoint Streamable HTTP (`/mcp`). **HTTP+SSE legado (spec `2024-11-05` `/sse`) não é suportado diretamente** (use bridge stdio como `mcp-remote` quando inevitável). Exija OAuth 2.1 / Bearer em endpoints protegidos, suporte a `MCP-Protocol-Version`/`_meta` e validação anti-SSRF em URLs externas.

## 3. Contratos JSON-RPC 2.0 & WebSockets (`wss://`)

- **Contratos Estritos:** Todo envelope JSON-RPC exige `"jsonrpc": "2.0"` e exclusividade mútua entre `"result"` e `"error"` (`-32700` Parse, `-32600` Invalid Request, `-32601` Method not found, `-32602` Invalid params, `-32603` Internal error). Valide DTOs internos em fronteiras RPC/MCP com `extra="forbid"` (Pydantic), `z.strictObject()` (Zod) ou `DisallowUnknownFields()` (Go — tolerando apenas payloads externos evolutivos quando documentado).
- **WebSockets (`wss://`):** Proíba `ws://` em produção; exija TLS 1.3 validando cadeia CA do sistema ou mTLS (evite *SSL Pinning* estático em domínios cloud com rotação frequente de certificado). Nunca coloque tokens secretos na query string da URL (use cabeçalho `Authorization` / *Ephemeral Tokens*) e aplique *Exponential Backoff + Jitter* na reconexão.
- **Testes Zero-Trust Obrigatórios:** Toda rota/tool autenticada ou protegida deve possuir testes adversariais provando rejeição determinística (`400`/`401`/`403` sem vazar segredos).
