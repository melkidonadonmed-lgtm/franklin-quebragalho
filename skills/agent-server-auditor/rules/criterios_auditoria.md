# Critérios Determinísticos de Auditoria — `agent-server-auditor` (`v1.0.0`)

Cada regra abaixo deve ser avaliada deterministicamente pelo script `scripts/agent_server_auditor.py` e reportada com os marcadores `[PASS]` ou `[FAIL: <RULE_ID>]`.

---

## Matriz de Regras Falsificáveis

| Rule ID | Dimensão | Severidade | Critério de Aprovação (`[PASS]`) | Condição de Falha (`[FAIL]`) |
| :--- | :--- | :---: | :--- | :--- |
| **`AUD-BIN-01`** | 1. Higiene & Binários | **CRÍTICO** | `[PASS]` Presença de `.gitignore` e zero binários compilados (`.exe`, `.dll`, `.so`, `.dylib`, `.asar`) fora de `bin/`, `dist/` ou `build/`. | `[FAIL: AUD-BIN-01]` Binários soltos na raiz/código-fonte ou ausência de `.gitignore`. |
| **`AUD-SKL-01`** | 2. Skills Modulares | **ALTO** | `[PASS]` Toda pasta em `skills/<nome>/` ou `.agents/skills/<nome>/` possui `SKILL.md` com frontmatter YAML válido (`name`, `description`) e aplica *Progressive Disclosure* L3 (`references/`/`scripts/`) quando L2 > `1.200` tokens. | `[FAIL: AUD-SKL-01]` Manifesto `SKILL.md` sem frontmatter válido ou com *Context Bloat* sem desacoplamento L3. |
| **`AUD-AGT-01`** | 2. Agentes & Loops (8 Eixos) | **CRÍTICO** | `[PASS]` Agentes (`Go`, `TypeScript`, `Python`, `agents/*.md`) possuem sintaxe válida, objetivo/função real sem placebos, SDK vigente, `max_steps`/`stop_condition`, policy explícita e **Menor Privilégio** (zero `tools: ["*"]` em subagentes Antigravity). | `[FAIL: AUD-AGT-01]` Loop sem `max_steps`, sintaxe inválida, função placebo ou violação de menor privilégio. |
| **`AUD-MCP-01`** | 3. Servidores MCP (SDK + Comportamento) | **CRÍTICO** | `[PASS]` Servidor MCP declara SDK válido no manifesto e mantém `stdout` exclusivo para JSON-RPC 2.0 no transporte `STDIO` (logs em `stderr`). | `[FAIL: AUD-MCP-01]` Uso de `print()`, `console.log()` ou `fmt.Println()` direto em `stdout` num servidor MCP STDIO ou SDK ausente. |
| **`AUD-CNT-01`** | 4. Contratos de Dados | **ALTO** | `[PASS]` Esquemas de ferramentas e payloads aplicam contrato estrito (`extra="forbid"` em Pydantic v2, `.strict()` em Zod ou `additionalProperties: false` em JSON Schema). | `[FAIL: AUD-CNT-01]` Esquemas de entrada permissivos sem bloqueio de campos alucinados. |
| **`AUD-A2A-01`** | 3. Protocolo A2A v1.0 | **ALTO** | `[PASS]` Cartão de Agente (`/.well-known/agent-card.json` ou `agent_card.json`) declara metadados (`name`, `description`, `version`), `supportedInterfaces`, IDs únicos em `skills[].id` e assinatura JWS (`signatures`). | `[FAIL: AUD-A2A-01]` Cartão A2A sem metadados, com `skills[].id` duplicados/vazios ou sem assinatura JWS. |
| **`AUD-MEM-01`** | 4. Memória Auditável | **MÉDIO** | `[PASS]` Relatório final serializado com carimbo temporal UTC e persistido em `memories/audit_report.json`. | `[FAIL: AUD-MEM-01]` Execução sem emissão ou persistência do snapshot estruturado de auditoria. |
