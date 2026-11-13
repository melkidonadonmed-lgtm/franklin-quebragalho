---
name: audit-websocket-jsonrpc
description: >-
  Sub-skill especialista para auditoria estatica e dinamica de conexoes persistentes WebSockets (ws:// e wss://) e contratos de mensagens JSON-RPC 2.0. Inspeciona ancoragem documental pre-flight (Gemini API llms.txt / llms-full.txt, MCP e A2A), handshakes TLS 1.3, reconexao dinamica (Exponential Backoff + Jitter), integridade de RPC, esquemas Pydantic/Zod e seguranca contra injecoes. Use ao auditar WebSockets, Live API, MCP ou JSON-RPC 2.0; nao use para CSS estatico.
version: "1.2.0"
updated_at: "2026-11-12"
compatibility: "Node.js 20+, Python 3.12+, Go 1.24+, Agent Skills Spec 2026, MCP 2026-07-28, A2A v1.0, Gemini Live API"
metadata:
  author: "SkillCraft & Melki"
  category: "network-protocol-auditing"
  frameworks: "CoT, ReAct, Self-Refine, Progressive Disclosure, Zero-Trust"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
---

# Sub-Skill de Referência: `audit-websocket-jsonrpc` — Auditoria de WebSockets & Contratos JSON-RPC 2.0 (`v1.2.0`)

## 0. ANCORAGEM DOCUMENTAL PRE-FLIGHT (CONDICIONAL AO PROTOCOLO)

Antes de auditar ou implementar endpoints WebSocket (`ws://` / `wss://`), sessões **Gemini Live API** ou barramentos **JSON-RPC 2.0** (`MCP` / `A2A`), valide as especificações e modelos vigentes na sessão via `gemini_search_docs` / `gemini_get_doc` (sem fixar versões estáticas) e os índices oficiais consolidados em [`protocol_matrix.md`](protocol_matrix.md), além dos contratos locais (`openapi.json`, `.well-known/agent-card.json`, `tools.json`).

---

## 1. OBJETIVO E MISSÃO ARQUITETURAL

Esta **Sub-Skill Especialista** estabelece o procedimento operacional e os checklists de engenharia para auditar, testar e homologar comunicação bidirecional assíncrona via **WebSockets (`ws://` e `wss://`)** e a especificação de mensagens **JSON-RPC 2.0**.

### Objetivos Principais

1. **Inspeção de Handshake & Transporte:** Validar TLS 1.3 (`wss://`), headers de upgrade HTTP, tokens JWT/Ephemeral Tokens em headers de autenticação e validação estrita da cadeia CA / mTLS (sem `rejectUnauthorized: false` ou `InsecureSkipVerify: true`).
2. **Resiliência de Conexão:** Avaliar lógicas de heartbeat (`ping`/`pong`), reconexão automática com *Exponential Backoff com Jitter* (`SessionResumption` / `GoAway` quando em Live API) e tratamento de desconexões abruptas.
3. **Validação de Contratos JSON-RPC 2.0:** Auditar parsing de mensagens `request`, `response`, `error` e `notification`, garantindo casamento estrito entre `id` da requisição e `id` da resposta (e ausência de `id` em notificações).
4. **Qualidade & Performance (QoS):** Medir latência RTT (*Round-Trip Time*), throughput de mensagens por segundo e teto de consumo de memória sob estresse.
5. **Segurança Zero-Trust:** Sanitizar campos de entrada contra injeções de comandos ou payloads maliciosos e barrar a exposição de dados pessoais sensíveis (PII).

---

## 2. ARQUITETURA COGNITIVA & TOPOLOGIA DE SUBAGENTE

A execução roda em nó efêmero isolado (`ModeTask` / `context: fork`), reportando achados ao orquestrador apenas no encerramento:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ 0. PRE-FLIGHT DOCS (llms.txt / llms-full.txt / OpenAPI / AgentCard)     │
│ • Carregar contrato real da API (Gemini API, Live API, MCP, A2A)        │
└────────────────────┬────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. INSPEÇÃO DE PROTOCOLO E HANDSHAKE (wss:// & Headers)                │
│ • Validar TLS/mTLS, headers de upgrade e integridade da conexão inicial │
└────────────────────┬────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. ARQUITETURA REACT DE MENSAGENS (JSON-RPC 2.0 Validation)             │
│ • Parsing defensivo de RPC (jsonrpc: "2.0", method, params, result, error)│
│ • Validação de esquemas tipados via Pydantic v2 (extra="forbid") / Zod  │
└────────────────────┬────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. SELF-REFINE & READ-AFTER-WRITE AUDIT                                 │
│ • Execução de script de teste de carga e latência RTT (ping/pong)       │
│ • Cálculo de métricas determinísticas (Pass@k, Jank/Dropped Frames)     │
│ • Emissão do Laudo Técnico e Registro em agents.json / audit_report.json│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. MATRIZ DE AUDITORIA EM 5 MÓDULOS

### Módulo 1: Handshake HTTP e Transporte WebSocket

- **Criptografia & Upgrade:** Verificar uso de protocolo seguro (`wss://`) em ambiente de produção. Bloquear transmissões em texto claro sem túnel seguro.
- **Autenticação Inicial:** Validar envio de credenciais via headers `Authorization: Bearer <token>` ou *Ephemeral Tokens* (`auth_tokens.create` na Gemini Live API) em vez de query parameters permanentes expostos na URL.
- **Validação de Cadeia TLS / mTLS:** Confirmar verificação estrita de certificado contra CAs confiáveis do sistema (ou mTLS em malhas internas), bloqueando `InsecureSkipVerify: true` / `verify=False` e evitando *SSL Pinning* estático em endpoints cloud sujeitos à rotação automática de certificados.

### Módulo 2: Contratos e Sintaxe JSON-RPC 2.0

- **Estrutura de Requisição (`Request`):**
  - Exigir atributo fixo `"jsonrpc": "2.0"`.
  - Atributo `"method"` estruturado em formato kebab-case, slash-notation (`tools/call`, `initialize`) ou dot-notation (ex: `"orders.create"`).
  - Atributo `"params"` estritamente tipado (objeto nomeado `{}` ou array ordenado `[]`).
- **Estrutura de Resposta (`Response`):**
  - Mutualmente exclusivo: deve conter apenas `"result"` OU `"error"`, jamais ambos no mesmo payload.
  - O campo `"id"` deve corresponder exatamente ao `"id"` enviado na requisição associada (notificações como `notifications/initialized` não possuem `"id"` e não devem receber resposta).
- **Erros Padronizados (`Error Object`):**
  - Validar códigos reservados da especificação JSON-RPC 2.0:
    - `-32700`: Parse error (JSON inválido).
    - `-32600`: Invalid Request (estrutura RPC incorreta).
    - `-32601`: Method not found (método inexistente).
    - `-32602`: Invalid params (parâmetros fora do esquema).
    - `-32603`: Internal error (erro interno de servidor).

### Módulo 3: Resiliência, Heartbeat e Reconexão

- **Heartbeat (Ping/Pong):** Garantir envio de quadros de `ping` a cada 15-30 segundos para manter a tabela de conexões ativas da infraestrutura.
- **Reconexão Inteligente:** Implementar *Exponential Backoff* com a fórmula:
  $$t_{\text{wait}} = \min(t_{\text{max}}, t_{\text{base}} \times 2^{\text{tentativa}}) + \text{jitter}$$
- **Buffer de Mensagens Pendentes:** Avaliar se mensagens emitidas durante breves quedas de conexão são enfileiradas com limite de tamanho (*bounded queue*) para evitar estouro de memória.

### Módulo 4: Qualidade de Serviço (QoS) e Métricas Determinísticas

- **Latência RTT ($RTT_{\text{avg}}$):**
  $$RTT_{\text{avg}} = \frac{1}{N} \sum_{i=1}^N (t_{\text{pong}_i} - t_{\text{ping}_i})$$
  - Exigir $RTT_{\text{avg}} < 150\text{ ms}$ em conexões regionais.
- **Confiabilidade Funcional ($\text{Pass}@k$):**
  $$\text{Pass}@k = 1 - \prod_{i=1}^k \left(1 - \frac{c}{n - k + i}\right)$$
  - Exigir $\text{Pass}@3 \ge 0.95$ para chamadas de RPC críticas.

### Módulo 5: Segurança Zero-Trust e Sanitização de Payload

- **Teto de Tamanho de Quadro (*Max Frame Size*):** Limitar o tamanho máximo por mensagem (ex: $\le 1\text{ MB}$) para impedir ataques de Negação de Serviço (DoS).
- **Sanitização de Entradas:** Bloquear caracteres de controle e injeções de scripts dentro de valores de parâmetros string.

---

## 4. O QUE NÃO FAZER (PROIBIÇÕES ESTRITAS / GUARDRAILS)

1. **[PROIBIDO] NUNCA chegar às cegas na API:** Proibido auditar ou codificar chamadas Gemini API / Live API / JSON-RPC sem antes consultar `gemini_search_docs`, `https://aistudio.google.com/llms.txt` ou `https://aistudio.google.com/llms-full.txt`.
2. **[PROIBIDO] NUNCA usar transporte não criptografado em produção:** Toda comunicação remota exige transporte seguro (`wss://` / `https://`).
3. **[PROIBIDO] NUNCA passar credenciais estáticas na URL:** Tokens/API keys permanentes na Query String vazam em logs de proxy e histórico.
4. **[PROIBIDO] NUNCA ignorar reconexão sem Jitter:** Reconectar todos os clientes ao mesmo tempo causa ataques de tempestade de reconexão (*Thundering Herd Problem*).
5. **[PROIBIDO] NUNCA aceitar JSON-RPC sem validar o atributo `"jsonrpc": "2.0"`:** Retornar respostas flexíveis sem contrato quebra parsers cliente.
6. **[PROIBIDO] NUNCA retornar campos `"result"` e `"error"` no mesmo payload:** Viola estritamente a especificação JSON-RPC 2.0.
7. **[PROIBIDO] NUNCA deixar loops de escuta sem timeout de inatividade:** Sockets abertos indefinidamente causam vazamentos de descritores de arquivo.

---

## 5. INSTRUÇÕES PARA O AGENTE EXECUTOR / DEEP CODER

Ao implementar clientes ou servidores WebSockets com JSON-RPC 2.0 em **Node.js (`ws`/`socket.io`)**, **Python (`websockets`/`asyncio`)** ou **Go (`gorilla/websocket` / `nhooyr.io/websocket`)**:

1. **Tipagem Estrita de Mensagens:**
   - Em Python, use Pydantic v2 com `model_config = ConfigDict(extra="forbid")`.
   - Em TypeScript, use Zod com `.strict()`.
   - Em Go, use structs fortemente tipadas com `dec.DisallowUnknownFields()` e descarte mensagens inválidas com erro `-32602`.
2. **Script de Teste de Resiliência:**
   - Monte um script de teste simulando desconexão forçada para validar se a reconexão ocorre dentro da janela de backoff esperada ($t_{\text{wait}}$).
3. **Registro no `agents.json` / `agent-card.json`:**
   - Atualize a lista de protocolos no arquivo `agents.json` ou `/.well-known/agent-card.json` do projeto confirmando suporte aos esquemas `websockets` e `json-rpc`.
