---
name: agent-server-auditor
description: "Audita sistemas agênticos, servidores MCP 2026-07-28 STDIO stdout, nós A2A agent-card JWS, binários, max_steps e memories/audit_report.json. Use para auditar agentes e MCP; não use para UI."
version: "1.2.0"
updated_at: "2026-11-12"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "1.2.0"
  updated_at: "2026-11-12"
  author: "SkillCraft, Franklin-Main & Melki"
  category: "Agent Architecture, Protocol Compliance & Static Code Auditing"
  tags: ["agent-server-auditor", "mcp-2026-07-28", "a2a-protocol", "least-privilege", "agent-card-jws", "stdio-hygiene", "max-steps", "audit-report"]
---
# Skill: `agent-server-auditor` — Auditoria Arquitetural de Agentes, Servidores MCP, WebSockets/JSON-RPC e Nós A2A (`v1.2.0`)

## 1. Objetivo, Gatilhos de Ativação e Ancoragem Pre-Flight

Fornece inspeção estática e contratual determinística para ecossistemas agênticos em **Python, TypeScript e Go**, auditando higiene de binários, conformidade real de **Agentes (8 eixos)**, **Skills (Progressive Disclosure Antigravity)**, **Servidores MCP (SDK + Comportamento)**, **WebSockets/JSON-RPC 2.0** e **Cartões A2A v1.0 JWS**, com snapshot auditável em `memories/audit_report.json`.

- **Quando Usar:** Auditoria de repositórios agênticos, pré-deploy de servidores MCP (`STDIO`/HTTP), validação de subagentes declarativos (`agents/*.md` / `.agents/agents/*.md`), inspeção de `.well-known/agent-card.json` e diagnóstico de loops ou corrupção JSON-RPC.
- **Ancoragem Pre-Flight Condicional (Zero Chegada às Cegas):** Antes de auditar integrações **Gemini API / Live API** ou **Google ADK**, consulte `gemini_search_docs` / `gemini_get_doc` (ou as referências canônicas consolidadas em [`references/protocol_matrix.md`](references/protocol_matrix.md)); quando houver **WebSockets (`ws://`/`wss://`) ou JSON-RPC 2.0**, aplique [`references/audit-websocket-jsonrpc.md`](references/audit-websocket-jsonrpc.md).

---

## 2. Entradas, Pré-requisitos e Parâmetros

- `--root` / `target_root` (obrigatório): Diretório raiz do projeto agêntico (padrão: `.`).
- `--persist` (opcional): Persiste o snapshot assinado/datado em `<target_root>/memories/audit_report.json`.
- `--output` (opcional): Caminho customizado para gravação do JSON.
- `--self-test` (opcional): Executa bateria de auto-validação determinística (`APPROVED` vs. `REJECTED`).

---

## 3. Fluxo de Processamento e As 4 Dimensões de Auditoria

### Dimensão 1: Higiene da Raiz e Segregação de Binários (`AUD-BIN-01`)
- Exige `.gitignore`, `.env.example` sem segredos reais e confinamento estrito de artefatos compilados (`.exe`, `.dll`, `.so`, `.dylib`, `.asar`, `.bin`) dentro de `bin/`, `dist/` ou `build/`.

### Dimensão 2: Auditoria de Agentes em 8 Eixos & Progressive Disclosure de Skills (`AUD-AGT-01` / `AUD-SKL-01`)
- **Agentes e Subagentes (8 Eixos Obrigatórios):**
  1. **Linguagem & Sintaxe**: Parsing real sem erro sintático (`ast.parse` em Python, tipagem TS/Go ou YAML frontmatter íntegro em `agents/*.md` e `.agents/agents/*.md`).
  2. **Objetivo & Função Real**: Presença de objetivo explícito e implementação executável real (reprovando funções placebo, `pass` isolado ou `NotImplementedError`).
  3. **Framework & SDK**: Validação de SDKs vigentes (`google-genai`, `@google/genai`, `google.golang.org/adk`, `google.adk`, `StateGraph`, `FastMCP`), bloqueando modelos depreciados (`gemini-2.5-*`) e `generation_config` rejeitado (`400`) no **Managed Antigravity Agent** (`temperature`, `top_p`, `top_k`, `stop_sequences`, `max_output_tokens` — observando que `max_output_tokens` é válido/recomendado em `generateContent` e `interactions.create` padrão).
  4. **Guardrails, Policy & Menor Privilégio (`Least Privilege`)**: Exige travas de contenção (`max_steps`, `max_turns`, `recursion_limit`), condição de parada verificável (`stop_condition` / *Read-After-Write*), política explícita (`commandExecutionPolicy` / portão HITL) e **Menor Privilégio** em ferramentas (auditores/observadores com `enable_write_tools: false` e vedação a `tools: ["*"]` em subagentes do Antigravity).
- **Skills (`agentskills.io` & `antigravity.google/docs/skills`):**
  - Localizadas em `skills/<nome>/SKILL.md` ou `.agents/skills/<nome>/SKILL.md` (`.agents/workflows/*.md` é depreciado no Antigravity 2.12+).
  - **Progressive Disclosure L1–L3:** Apenas `SKILL.md` com frontmatter válido (`name <= 64`, `description`) é obrigatório; subpastas Nível 3 (`scripts/`, `references/`, `rules/`, `evals/`) são carregadas sob demanda e exigidas apenas quando o corpo L2 ultrapassar `1.200` tokens.

### Dimensão 3: Protocolos MCP (`SDK + Comportamento`), WebSockets/JSON-RPC 2.0 e A2A v1.0 (`AUD-MCP-01` / `AUD-A2A-01`)
- **Servidores MCP (Revisão `2026-07-28` validada por SDK + Comportamento):**
  - Não audite apenas uma string de data estática: verifique a **versão do SDK MCP nos manifestos** (`mcp` / `fastmcp` em `pyproject.toml`, `@modelcontextprotocol/sdk` em `package.json`, `mcp-go`/ADK em `go.mod`) somada à **conformidade comportamental**:
    - **Higiene `STDIO`:** `stdout` exclusivo para quadros JSON-RPC 2.0 (`print()` sem `sys.stderr`, `console.log()` ou `fmt.Println()` em servidor STDIO $\rightarrow$ `POLLUTED` / `REJECTED`).
    - **Contratos & Transporte:** Schemas estritos de entrada (`extra="forbid"`, `.strict()`, `additionalProperties: false`), negociação de versão (`_meta` / `MCP-Protocol-Version`) e proteção OAuth 2.1 / anti-SSRF em HTTP.
- **WebSockets (`wss://`) e JSON-RPC 2.0 ([`references/audit-websocket-jsonrpc.md`](references/audit-websocket-jsonrpc.md)):**
  - Exige TLS 1.3 (`wss://`) com validação de cadeia CA do sistema ou mTLS (evitando *SSL Pinning* estático em endpoints cloud com rotação automática de certificados), `Authorization: Bearer` / *Ephemeral Tokens*, *Exponential Backoff + Jitter*, `"jsonrpc": "2.0"` e exclusividade mútua entre `"result"` e `"error"`.
- **Nós A2A (`/.well-known/agent-card.json` ou `agent_card.json`):**
  - Audita **Metadados obrigatórios** (`name`, `description`, `version`), **`supportedInterfaces`**, **IDs únicos e não-vazios em `skills[].id`** e **Assinatura JWS (`signatures` RFC 7515 sobre RFC 8785 JCS)**.

### Dimensão 4: Execução CLI e Estrutura Real Antigravity (`AUD-CNT-01` / `AUD-MEM-01`)

```powershell
uv run python skills/agent-server-auditor/scripts/agent_server_auditor.py --root . --persist --json
uv run python skills/agent-server-auditor/scripts/agent_server_auditor.py --self-test
```

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

---

## 4. Saídas, Entregáveis e Esquema Persistido em Memória

Emite diagnóstico JSON validado por Pydantic (`extra="forbid"`) e grava `memories/audit_report.json` conforme [`references/audit_report_schema.md`](references/audit_report_schema.md) (`timestamp` UTC, `audit_version`, `target_root`, `summary`, `binary_hygiene`, `audit_details` e `gap_analysis`).

---

## 5. Limites, Exceções e Guardrails (Quando NÃO Usar)

1. **Fronteira Limpa:** Não use para auditar qualidade AAA de suítes de testes (`test-quality-auditor`) nem para auditar UI, contraste `OKLCH` ou DOM (`frontend-testing-auditor` / `complex-zero`).
2. **Separação Estático vs. Dinâmico:** `agent_server_auditor.py` executa análise estática determinística sem mutações de rede; métricas de latência viva ($RTT_{\text{avg}}$) só são medidas quando um endpoint local/homologação for explicitamente fornecido.
3. **Portões Críticos de Reprovação (`rules/criterios_auditoria.md`):** Poluição de `stdout` em MCP STDIO (`AUD-MCP-01`), binários soltos fora de `bin/dist/build` (`AUD-BIN-01`) ou loops agênticos sem `max_steps` (`AUD-AGT-01`) reprovam imediatamente (`REJECTED`).
