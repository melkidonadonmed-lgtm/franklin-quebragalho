# Matriz de Conformidade de Protocolos Agênticos (`MCP 2026-07-28`, `A2A v1.0`, `Gemini API` & `WebSockets/JSON-RPC 2.0`)

Documento de referência técnica da skill **`agent-server-auditor`** para inspeção estática e contratual poliglota (**Python**, **TypeScript** e **Go**).

---

## 0. Ancoragem Documental Pre-Flight (Proibido Chegar às Cegas)

Antes de auditar qualquer cliente/servidor de API, modelo ou protocolo, consulte obrigatoriamente as fontes oficiais:

- **Portal Oficial Gemini API (`docs`) & Antigravity Agent:** [`https://aistudio.google.com/docs`](https://aistudio.google.com/docs) | [`https://aistudio.google.com/docs/antigravity-agent`](https://aistudio.google.com/docs/antigravity-agent)
- **Gemini API / Google AI Studio Docs Index (`llms.txt`):** [`https://aistudio.google.com/llms.txt`](https://aistudio.google.com/llms.txt)
- **Gemini API / Google AI Studio Full Corpus (`llms-full.txt`):** [`https://aistudio.google.com/llms-full.txt`](https://aistudio.google.com/llms-full.txt)
- **Google Gemini Cookbook (GitHub):** [`https://github.com/google-gemini/cookbook`](https://github.com/google-gemini/cookbook)
- **Google ADK Docs (`llms.txt` & `llms-full.txt`):** [`https://adk.dev/llms.txt`](https://adk.dev/llms.txt) | [`https://adk.dev/llms-full.txt`](https://adk.dev/llms-full.txt)
- **Sub-Skill WebSockets & JSON-RPC 2.0:** [`audit-websocket-jsonrpc.md`](audit-websocket-jsonrpc.md)

---

## 1. Model Context Protocol (`MCP Spec 2026-07-28`)

### 1.1. Higiene de Streams no Transporte `STDIO`

- **Regra Canônica:** No transporte `STDIO`, o descritor `stdout` é o barramento binário/textual de quadros `JSON-RPC 2.0`. Qualquer byte não pertencente a um envelope JSON-RPC válido corrompe o parser do cliente MCP.
- **Padrões Proibidos em Servidores STDIO (`stdout_hygiene = "POLLUTED"`):**
  - **Python:** `print(...)` sem `file=sys.stderr`.
  - **TypeScript / Node.js:** `console.log(...)` ou `process.stdout.write(...)` com texto de log.
  - **Go:** `fmt.Println(...)`, `fmt.Printf(...)` ou `log.Println(...)` sem redirecionar `log.SetOutput(os.Stderr)`.
- **Padrões Seguros (`stdout_hygiene = "CLEAN"`):**
  - **Python:** `logging.StreamHandler(sys.stderr)`, `print(..., file=sys.stderr)`.
  - **TypeScript:** `console.error(...)`, `process.stderr.write(...)`.
  - **Go:** `fmt.Fprintln(os.Stderr, ...)`, `slog.New(slog.NewJSONHandler(os.Stderr, nil))`.

### 1.2. Primitivas e Contratos MCP

- **Primitivas Expostas:** Declaração explícita de `tools` (`@mcp.tool`), `resources` (`@mcp.resource`) e `prompts` (`@mcp.prompt`).
- **Stateless Core & Metadados:** Suporte a `_meta` com `io.modelcontextprotocol/protocolVersion` (`2026-07-28`).
- **Transporte HTTP/SSE:** Exige validação de OAuth 2.1, Resource Indicators (RFC 8707) e proteção contra SSRF/DNS Rebinding.

---

## 2. Agent-to-Agent Protocol (`A2A v1.0`)

### 2.1. Estrutura Obrigatória do `agent-card.json`

Localização padrão: `/.well-known/agent-card.json` (ou espelho na raiz `agent_card.json`).

- `name` (`string`): Identificador legível do nó agêntico.
- `description` (`string`): Propósito operacional do agente.
- `version` (`string`): Versão semântica do manifesto.
- `supportedInterfaces` (`array`): Lista de endpoints contendo `url`, `protocolBinding` (`"JSONRPC"` ou `"gRPC"`) e `protocolVersion` (`"1.0"`).
- `defaultInputModes` / `defaultOutputModes` (`array`): MIME types suportados (ex: `["text/plain", "application/json"]`).
- `skills` (`array`): Catálogo de habilidades expostas pelo agente com `id`, `name`, `description` e `tags`.
- `signatures` (`array`): Assinatura JWS sobre JSON Canônico (RFC 8785 JCS + RFC 7515 JWS) garantindo autenticidade e integridade contra *impersonation* e MITM.

### 2.2. Máquina de Estados de Tarefas A2A (`TaskState`)

Transições válidas exigidas em gerenciadores de tarefas A2A:

- `TASK_STATE_SUBMITTED` $\rightarrow$ `TASK_STATE_WORKING`
- `TASK_STATE_WORKING` $\rightarrow$ `TASK_STATE_INPUT_REQUIRED` (Portão HITL para ações `RiskLevel.CRITICAL`)
- `TASK_STATE_WORKING` $\rightarrow$ `TASK_STATE_COMPLETED` | `TASK_STATE_FAILED`
- `TASK_STATE_SUBMITTED` $\rightarrow$ `TASK_STATE_REJECTED` (Bloqueio imediato pelo `SemanticGuard` contra *Prompt Injection*)

---

## 3. WebSockets (`ws://` / `wss://`) & Contratos JSON-RPC 2.0 ([`audit-websocket-jsonrpc.md`](audit-websocket-jsonrpc.md))

- **Transporte e Autenticação:** Uso obrigatório de `wss://` (TLS 1.3) em produção, credenciais via header `Authorization: Bearer <token>` ou *Ephemeral Tokens* (proibido passar chave permanente na Query String).
- **Resiliência e Reconexão:** Heartbeat `ping`/`pong` (15–30s), *Exponential Backoff com Jitter* ($t_{\text{wait}} = \min(t_{\text{max}}, t_{\text{base}} \times 2^{\text{tentativa}}) + \text{jitter}$) e fila limitada para mensagens pendentes.
- **Contrato JSON-RPC 2.0:** `"jsonrpc": "2.0"` explícito, exclusividade mútua entre `"result"` e `"error"`, casamento estrito de `"id"` (e ausência de `"id"` em notificações), códigos reservados `-32700` a `-32603`, quadro máximo $\le 1\text{ MB}$, $RTT_{\text{avg}} < 150\text{ ms}$ e $\text{Pass}@3 \ge 0.95$.

---

## 4. Padrões de Loops Cognitivos e Travas Operacionais

| Linguagem | Frameworks Reconhecidos | Indicadores de Padrão de Raciocínio | Travas de Profundidade (`has_max_steps`) | Condição de Parada (`has_stop_condition`) |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | Google ADK 2.x, LangGraph (`StateGraph`), CrewAI, FastMCP, Orquestradores Custom | `ReAct`, `StateGraph`, `Chain-of-Thought`, `AgentOrchestrator`, `DAGEngine` | `max_steps`, `max_retries`, `max_turns`, `max_iterations`, `recursion_limit` | `stop_condition`, `END`, `Read-After-Write`, `COMPLETED`, `APPROVED` |
| **TypeScript** | `@modelcontextprotocol/sdk`, LangGraph.js, Genkit TS, OpenAI Agents SDK | `ReAct`, `StateGraph`, `defineFlow`, `tool_use` | `maxSteps`, `maxRetries`, `maxTurns`, `recursionLimit` | `stopCondition`, `isTerminal`, `COMPLETED` |
| **Go** | Google ADK Go v2 (`google.golang.org/adk`), `mcp-go`, Orquestradores Go | `ReAct`, `Dual-Track`, `CognitiveRouter`, `Runner` | `MaxSteps`, `MaxTurns`, `MaxRetries`, `context.WithTimeout` | `StopCondition`, `Verify`, `COMPLETED` |

---

## 5. Contratos de Dados Estritos (Prevenção de Alucinação de Parâmetros)

- **Pydantic v2 (Python):** `model_config = ConfigDict(extra="forbid")`
- **Zod (TypeScript):** `z.object({...}).strict()`
- **Go (`encoding/json`):** `dec.DisallowUnknownFields()`
- **JSON Schema / MCP Tool Input Schema:** `"additionalProperties": false`

---

## 6. Baseline Vigente — Modelos Gemini 4, Decisions API, Live API e SDKs (`https://github.com/googleapis`)

- **Fontes Canônicas (nunca use `gemini_search_docs`, desabilitada no servidor local):** `google-developer-knowledge` (`search_documents`/`get_documents`), `gemini_get_doc` (`chunk_id`), [`https://aistudio.google.com/llms.txt`](https://aistudio.google.com/llms.txt), [`https://aistudio.google.com/docs/models.md`](https://aistudio.google.com/docs/models.md), [`https://aistudio.google.com/docs/deprecations.md`](https://aistudio.google.com/docs/deprecations.md), [`https://aistudio.google.com/docs/libraries.md`](https://aistudio.google.com/docs/libraries.md), [`https://aistudio.google.com/docs/decisions-api.md`](https://aistudio.google.com/docs/decisions-api.md), [`https://antigravity.google/docs/models.md`](https://antigravity.google/docs/models.md) e [`https://antigravity.google/docs/sdk/overview.md`](https://antigravity.google/docs/sdk/overview.md).
- **Gemini 4 (1M contexto unificado, cache implícito >= 4.096 tokens, sem `cachedContents`, `temperature`/`top_p`/`top_k` ignorados, 64K default ou 1M decode longo com `background=True`):**
  - `gemini-4-carbon`: raciocínio máximo (`thinking_level`: `low`, `medium` padrão, `high`).
  - `gemini-4-argon`: fronteira eficiente (`thinking_level`: `low`, `medium` padrão, `high`).
  - `gemini-4-hydrogen`: padrão ágil de código/agentes e default de `antigravity-preview-09-2026` (`thinking_level`: `low`, `medium`, `high` padrão, **`xhigh`**; `minimal` não suportado).
- **Decisions, Live & Áudio/Mídia:** `gemini-decision-1` (`client.decisions.create` / `POST /v1beta/decisions`, `noul` `0.01-0.99`, `choice`/`score`, 0 output tokens); Live `gemini-3.8-live`, `gemini-3.8-live-extended-thinking` (`NON_BLOCKING`, `interaction_status=="IDLE"`, `proactive_video`, `send_context_update`), `gemini-3.5-transcribe-live`, `gemini-3.5-live-translate-preview`; TTS `gemini-3.8-flash-tts` / `gemini-3.8-flash-lite-tts`; Vídeo `gemini-omni-1.2-flash`.
- **Bloqueio Obrigatório (Aposentados/Inexistentes):** `gemini-1.0-*`/`1.5-*`, `gemini-2.0-*`, `gemini-2.5-flash`/`2.5-pro` (shutdown `01/12/2026`; **`gemini-2.5-flash-lite` não é depreciado**), `2.5-*-preview-tts` / `gemini-3.1-flash-tts-preview` (`18/12/2026`), `2.5-flash-native-audio*` (`31/03/2027`), `2.5-flash-image` (`15/03/2027`), `gemini-3.1-flash-live-preview` (preview legado sem shutdown -> `gemini-3.8-live`), `gemini-live-2.5-*`, `gemini-omni-1.1-flash` (`03/12/2026`), `antigravity-preview-05-2026` (`05/10/2026`), previews encerrados (`gemini-3-pro-preview`, `3.1-flash-lite-preview`, `3-pro-image-preview`, `3.1-flash-image-preview`, `2.0-flash-preview-image-generation`, `embedding-2-preview`, `omni-flash-preview`, `deep-research-pro-preview-12-2025`, `2.5-computer-use-preview-10-2025`, `robotics-er-1.[56]-preview`, `text-embedding-004`/`embedding-*`, `imagen-[34].0-*`, `veo-[23].*`) e `gemini-3.8-flash-lite` (inexistente).
- **SDKs Oficiais (`googleapis`), Antigravity SDK & ADK v2:** `google-genai>=3.3.0` (`httpx2`, `--flavor=interactions-eap`), `@google/genai>=3.3.0`, `com.google.genai:google-genai>=2.3.0`, `googleapis/kotlin-genai>=2.1.0`, `google.golang.org/genai>=1.77.0` (`main`: `gemini-4-hydrogen`/`XHIGH`/Decisions/BYOS/`AutomaticContinuation`/`send_context_update`), `Google.GenAI>=2.1.0`, `google-antigravity>=0.1.23` (`from google.antigravity import Agent, LocalAgentConfig`, `vertex=True`) e `gemini-api` CLI (`beta`); bloqueie legados (`google-generativeai`, `@google/generativeai`, `@google/generative-ai`, `@google-cloud/vertexai`, `google.golang.org/generative-ai`). Desde `python/js-genai>=3.0.0` e `java/kotlin/dotnet-genai>=2.0.0`, Developer API padrão é **`v1`** (`vertexai=True`/`enterprise=True` segue `v1beta1`), exigindo `HttpOptions(api_version='v1beta')` ou `GOOGLE_GENAI_API_VERSION=v1beta` para `decisions`/`interactions`/`antigravity-preview-09-2026`/`*-latest`; `google-adk>=2.14.1` (ainda fixa `google-genai<3`), `google.golang.org/adk/v2>=2.7.1`, `@google/adk>=2.5.0` (fixa `@google/genai ^2.29.1`), `google/adk-java>=1.14.0`, `google/adk-kotlin>=1.5.0`, `google/agents-cli>=1.14.0`; `Api-Revision: 2026-05-20`; ambientes BYOS (`system_instruction`, `custom_config`, `environment_key`).
