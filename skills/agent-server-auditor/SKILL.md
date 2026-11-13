---
name: agent-server-auditor
description: "Audita sistemas agênticos, servidores MCP 2026-07-28 STDIO stdout, nós A2A agent-card JWS, binários, max_steps e memories/audit_report.json. Use para auditar agentes e MCP; não use para UI."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
metadata:
  version: "1.2.0"
  updated_at: "2026-11-13"
  author: "SkillCraft, Franklin-Main & Melki"
  category: "Agent Architecture, Protocol Compliance & Static Code Auditing"
  tags: ["agent-server-auditor", "mcp-2026-07-28", "a2a-protocol", "least-privilege", "agent-card-jws", "stdio-hygiene", "max-steps", "audit-report"]
---

# `agent-server-auditor` — Auditoria de Agentes, MCP, WS/JSON-RPC e A2A

## 1. Objetivo, Gatilhos e Pre-Flight Condicional

Executa inspeção estática e contratual determinística de projetos agênticos (**Python, TypeScript, Go**):

- Auditar repositórios agênticos, servidores **MCP (`2026-07-28` SDK + Comportamento STDIO/HTTP)**, subagentes (`agents/*.md`), **A2A v1.0 JWS** (`/.well-known/agent-card.json`) e higiene de binários.
- **Pre-Flight Condicional:** Antes de auditar **Gemini API / Google ADK**, consulte `google-developer-knowledge` (`search_documents`/`get_documents`), `gemini_get_doc` (`chunk_id`), `aistudio.google.com/llms.txt` ou [`references/protocol_matrix.md`](references/protocol_matrix.md) (nunca use `gemini_search_docs`, desabilitada no servidor local); havendo **WebSockets (`ws://`/`wss://`) ou JSON-RPC 2.0**, aplique [`references/audit-websocket-jsonrpc.md`](references/audit-websocket-jsonrpc.md).

## 2. Entradas e Parâmetros CLI

- **`--root` / `target_root` (obrigatório):** Raiz do projeto agêntico (padrão: `.`).
- **`--persist` / `--output` (opcional):** Grava snapshot em `<target_root>/memories/audit_report.json` ou caminho alvo.
- **`--self-test` (opcional):** Executa auto-validação `APPROVED` vs. `REJECTED`.

## 3. Processamento nas 4 Dimensões e Execução

Consulte a árvore canônica e requisitos detalhados em [`references/estrutura_projeto_agentico.md`](references/estrutura_projeto_agentico.md):

1. **D1 — Binários (`AUD-BIN-01`):** `.gitignore`, `.env.example` limpo e `.exe`/`.so`/`.asar` confinados a `bin/`, `dist/` ou `build/`.
2. **D2 — Agentes & Skills (`AUD-AGT-01` / `AUD-SKL-01`):** Sintaxe real, zero placebos, SDKs/modelos vigentes (`google-genai>=3.3.0`, `@google/genai>=3.3.0`, `com.google.genai>=2.3.0`, `kotlin-genai>=2.1.0`, `Google.GenAI>=2.1.0`, `google.golang.org/genai>=1.77.0` — exigindo `api_version="v1beta"` para `decisions`/`interactions` desde `3.0`/`2.0` que mudaram Developer API padrão para `v1` — e Gemini 4 `hydrogen`/`argon`/`carbon`, bloqueando `gemini-2.5-*`, `3.1-*tts-preview`, `3.1-flash-live-preview` e `antigravity-preview-05-2026`), `max_steps`/HITL, menor privilégio (auditores `commandExecutionPolicy: "readOnly"`, zero `tools: ["*"]`/`call_mcp_tool`, sem `enable_write_tools` legado) e Skills com Progressive Disclosure (`<= 1.200t` L2).
3. **D3 — MCP, WS/JSON-RPC & A2A (`AUD-MCP-01` / `AUD-A2A-01`):** SDK real no manifesto + STDIO `stdout` puro + schemas estritos (`extra="forbid"` / `.strict()`) + A2A `supportedInterfaces` / `skills[].id` únicos / JWS RFC 7515.
4. **D4 — Execução (`AUD-CNT-01` / `AUD-MEM-01`):**

```powershell
uv run python skills/agent-server-auditor/scripts/agent_server_auditor.py --root . --persist --json
uv run python skills/agent-server-auditor/scripts/agent_server_auditor.py --self-test
```

## 4. Saídas e Entregáveis

Diagnóstico JSON validado por Pydantic (`extra="forbid"`) e persistido em `memories/audit_report.json` conforme [`references/audit_report_schema.md`](references/audit_report_schema.md).

## 5. Exceções, Limites e Quando NÃO Usar

- **Fora de Escopo:** Suítes de testes (`test-quality-auditor`) ou UI/DOM/OKLCH (`frontend-testing-auditor`, `complex-zero`).
- **Estático vs. Dinâmico:** `agent_server_auditor.py` é estático; latência viva ($RTT_{\text{avg}}$) requer endpoint explícito.
- **Reprovação Imediata ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)):** Poluição de `stdout` em STDIO (`AUD-MCP-01`), binário fora de `bin/dist/build` (`AUD-BIN-01`) ou loop sem `max_steps` (`AUD-AGT-01`) geram `REJECTED`.
