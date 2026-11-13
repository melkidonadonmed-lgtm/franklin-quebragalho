# Estrutura de Projeto Agêntico e 4 Dimensões — `agent-server-auditor`

Referência operacional de pastas e requisitos detalhados usados por [`../SKILL.md`](../SKILL.md), complementando [`protocol_matrix.md`](protocol_matrix.md), [`audit-websocket-jsonrpc.md`](audit-websocket-jsonrpc.md) e [`audit_report_schema.md`](audit_report_schema.md).

## Estrutura Canônica Antigravity / ADK

```text
projeto-agentico-raiz/
├── AGENTS.md / GEMINI.md              # Kernel operacional na raiz (sem frontmatter)
├── .agents/
│   ├── AGENTS.md                      # Governança espelhada e perfil do workspace
│   ├── rules/*.md                     # Regras modulares (frontmatter trigger obrigatório, <= 24KB)
│   ├── skills/<nome>/SKILL.md         # Skills locais (Progressive Disclosure L1-L3)
│   └── agents/*.md                    # Subagentes declarativos com Menor Privilégio
├── .context/                          # context.md (estado vivo) e spec.md (contratos I/O)
├── mcp_config.json / plugin.json      # Servidores MCP (binários compilados) e manifesto de plugin
├── hooks/hooks.json & sidecars/       # Hooks determinísticos e sidecar.json (quando aplicável)
├── bin/                               # Destino exclusivo de executáveis compilados (.exe, .so)
├── .well-known/agent-card.json        # Identidade pública A2A v1.0 com IDs únicos e JWS
├── memories/audit_report.json         # Snapshot auditável com metadados, timestamp UTC e score
└── tests/                             # Suíte determinística (happy-path + adversarial Zero-Trust)
```

## Critérios por Dimensão

- **Dimensão 1 — Binários (`AUD-BIN-01`):** `.gitignore`, `.env.example` sem segredos, artefatos `.exe`/`.dll`/`.so`/`.dylib`/`.asar`/`.bin` confinados a `bin/`, `dist/` ou `build/`.
- **Dimensão 2 — Agentes & Skills (`AUD-AGT-01` / `AUD-SKL-01`):** `ast.parse`/TS/Go/YAML válidos; implementação real (zero `pass`/`NotImplementedError`); SDKs vigentes (`google-genai>=3.3.0`, `@google/genai>=3.3.0`, `google.golang.org/genai>=1.77.0`, `com.google.genai:google-genai>=2.3.0`, `googleapis/kotlin-genai>=2.1.0`, `Google.GenAI>=2.1.0`, `google-adk>=2.14.1` `<3` GenAI, `google.golang.org/adk/v2>=2.7.1`, `@google/adk>=2.5.0`, `StateGraph`, `FastMCP`; lembrar que `python/js>=3.0` e `java/kotlin/dotnet>=2.0` mudaram o padrão Developer API de `v1beta` para `v1`, exigindo `api_version='v1beta'` em `decisions`/`interactions`); bloqueio de `gemini-2.5-*`, `3.1-*tts-preview`, `3.1-flash-live-preview`, `antigravity-preview-05-2026`, `gemini-omni-1.1-flash`, `gemini-3.8-flash-lite` e `generation_config` rejeitado no Managed Antigravity Agent (`max_output_tokens` ok em `generateContent`/`interactions.create`); `max_steps`/`max_turns`/`recursion_limit`, `stop_condition`, HITL e Menor Privilégio (`commandExecutionPolicy: "readOnly"` em auditores, zero `tools: ["*"]`/`call_mcp_tool`, sem chaves legadas `enable_write_tools`/`wave`/`parent_persona`). Skills com `name <= 64`, sem `.agents/workflows/*.md`, L3 sob demanda (`<= 1200t` L2).
- **Dimensão 3 — MCP `2026-07-28`, WS/JSON-RPC & A2A v1.0 (`AUD-MCP-01` / `AUD-A2A-01`):** SDK nos manifestos (`mcp`/`fastmcp`, `@modelcontextprotocol/sdk`, `mcp-go`/ADK); higiene STDIO (zero `print()`/`console.log()`/`fmt.Println()` em `stdout`); `extra="forbid"` / `.strict()` / `additionalProperties: false`, `_meta`/`MCP-Protocol-Version`, OAuth 2.1/anti-SSRF; `wss://` TLS 1.3 com CA/mTLS (sem pinning estático em cloud), Ephemeral Tokens, Jitter, JSON-RPC 2.0 exclusivo (`result` vs `error`); A2A `name`/`description`/`version`/`supportedInterfaces`/`skills[].id` únicos + `signatures` JWS RFC 7515/8785.
