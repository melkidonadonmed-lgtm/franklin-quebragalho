# Critérios Determinísticos de Auditoria — `agent-server-auditor` (`v1.0.0`)

Cada regra abaixo deve ser avaliada deterministicamente pelo script `scripts/agent_server_auditor.py` e reportada com os marcadores `[PASS]` ou `[FAIL: <RULE_ID>]`.

---

## Matriz de Regras Falsificáveis

| Rule ID | Dimensão | Severidade | Critério de Aprovação (`[PASS]`) | Condição de Falha (`[FAIL]`) |
| :--- | :--- | :---: | :--- | :--- |
| **`AUD-BIN-01`** | 1. Higiene & Binários | **CRÍTICO** | `[PASS]` Presença de `.gitignore` e zero binários compilados (`.exe`, `.dll`, `.so`, `.dylib`, `.asar`) fora de `bin/`, `dist/` ou `build/`. | `[FAIL: AUD-BIN-01]` Binários soltos na raiz/código-fonte ou ausência de `.gitignore`. |
| **`AUD-SKL-01`** | 2. Skills Modulares | **ALTO** | `[PASS]` Toda pasta em `skills/<nome>/` possui `SKILL.md` com frontmatter YAML válido (`name`, `description`, `version`) e subpastas modulares (`scripts/`, `references/`, `evals/`). | `[FAIL: AUD-SKL-01]` Manifesto `SKILL.md` sem frontmatter válido ou sem bateria `evals/evals.json`. |
| **`AUD-AGT-01`** | 2. Agentes & Loops | **CRÍTICO** | `[PASS]` Agentes e orquestradores (`Go`, `TypeScript`, `Python`) declaram trava explícita de iteração (`max_steps`, `max_turns`, `max_retries`, `recursion_limit`) e condição de parada. | `[FAIL: AUD-AGT-01]` Loop ReAct / StateGraph / ADK sem limite superior de passos configurado. |
| **`AUD-MCP-01`** | 3. Servidores MCP | **CRÍTICO** | `[PASS]` Servidores MCP em transporte `STDIO` mantêm `stdout` exclusivo para JSON-RPC 2.0 (logs direcionados a `stderr` ou logger estruturado). | `[FAIL: AUD-MCP-01]` Uso de `print()`, `console.log()` ou `fmt.Println()` direto em `stdout` num servidor MCP STDIO. |
| **`AUD-CNT-01`** | 4. Contratos de Dados | **ALTO** | `[PASS]` Esquemas de ferramentas e payloads aplicam contrato estrito (`extra="forbid"` em Pydantic v2, `.strict()` em Zod ou `additionalProperties: false` em JSON Schema). | `[FAIL: AUD-CNT-01]` Esquemas de entrada permissivos sem bloqueio de campos alucinados. |
| **`AUD-A2A-01`** | 3. Protocolo A2A v1.0 | **ALTO** | `[PASS]` Cartão de Agente (`/.well-known/agent-card.json` ou `agent_card.json`) declara `name`, `version`, `supportedInterfaces`, `skills` e assinatura JWS (`signatures`). | `[FAIL: AUD-A2A-01]` Cartão A2A ausente (quando aplicável) ou sem interfaces/assinatura JWS. |
| **`AUD-MEM-01`** | 4. Memória Auditável | **MÉDIO** | `[PASS]` Relatório final serializado com carimbo temporal UTC e persistido em `memories/audit_report.json`. | `[FAIL: AUD-MEM-01]` Execução sem emissão ou persistência do snapshot estruturado de auditoria. |
