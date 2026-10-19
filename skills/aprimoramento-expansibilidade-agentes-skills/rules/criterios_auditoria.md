# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA (`aprimoramento-expansibilidade-agentes-skills` v2.2.0)

Toda arquitetura de agente, seleção de framework, contrato de tool/MCP ou avaliação matemática conduzida por esta skill deve ser auditada contra as 6 regras booleanas abaixo, emitindo exclusivamente `[PASS]`, `[FAIL]` ou `[UNVERIFIED]`:

---

### Regra 1: Distinção Ontológica e Seleção pelo Gargalo Dominante (Módulo A)
- **Critério**: A arquitetura separa etapas determinísticas (Python/SQL/Workflow) das etapas agentivas (LLM em loop) e justifica a escolha do framework (`SDK direto`, `Google ADK 2.x`, `LangGraph`, `LlamaIndex`, `Microsoft Agent Framework`, `CrewAI`) sem sobre-engenharia?
- **Resultado**:
  - Etapas previsíveis mantidas determinísticas e framework adequado ao gargalo -> `[PASS]`
  - Uso de LLM ou multiagente para cálculos/fluxos fixos sem benchmark -> `[FAIL: Sobre-engenharia ou uso estocástico para etapa determinística]`

---

### Regra 2: Loop Cognitivo, Orçamento Operacional e 5 Camadas de Memória (Módulo B)
- **Critério**: O agente define limites explícitos (`max_steps`, `max_tool_calls`, `deadline_seconds`, `stop_when`) e separa as camadas de memória (*Turno, Trabalho, Curto Prazo, Longo Prazo*) da **Fonte de Verdade** transacional?
- **Resultado**:
  - Orçamento explícito definido e releitura da fonte de verdade antes de escritas -> `[PASS]`
  - Loop aberto sem `max_steps` ou uso da memória do agente como fonte de verdade -> `[FAIL: Loop desprotegido ou acoplamento indevido de memória]`

---

### Regra 3: Contratos Estritos de Tools (`Pydantic extra="forbid"`), Despacho Polimórfico e MCP (`2026-07-28`) (Módulo C)
- **Critério**: Tools utilizam schemas estritos (`extra="forbid"`), registro fechado (`REGISTRY`), `idempotency_key` em escritas, *Envelope Pattern* (`PolyExtensibleSkillEngine` com `recovery_hint`) quando há múltiplas suboperações, e servidores MCP `stdio` nunca escrevem logs em `stdout`?
- **Resultado**:
  - Schemas fechados, erros acionáveis e conformidade MCP `2026-07-28` -> `[PASS]`
  - Schemas abertos, proliferação de micro-tools diluindo Softmax ou logs em `stdout` no MCP `stdio` -> `[FAIL: Contrato de tool ou protocolo MCP inválido]`

---

### Regra 4: Defesa Zero-Trust, `Context Forking` e `Theranostic Gate` (Módulo D)
- **Critério**: Subtarefas pesadas rodam isoladas (`context: fork` / `invoke_subagent`), entradas externas usam `<untrusted_user_input>` e mutações críticas exigem `ConfidenceGate >= 0.95` / HITL e assinatura `HMAC-SHA256`?
- **Resultado**:
  - Isolamento de contexto, portão HITL/Theranostic e proveniência ativos -> `[PASS]`
  - Mutações destrutivas sem portão ou contaminação da janela principal -> `[FAIL: Violação Zero-Trust ou ausência de isolamento]`

---

### Regra 5: Auditoria Matemática Determinística (`Pass@k`, `D_cos`, `FNR`, `S_norm`, `TEI`) (Módulo E)
- **Critério**: As métricas são calculadas deterministicamente via `scripts/agentic_math_and_engine_auditor.py` (estimador iterativo $\text{Pass}@k$, distância de cosseno $D_{\cos} \le 0.18$, guardrail $\text{FNR} < 0.001$, juiz normalizado $S_{\text{norm}} \in [0, 100]$ e $\text{TEI}$)?
- **Resultado**:
  - Execução comprovada do script matemático com `[PASS]` -> `[PASS]`
  - Notas subjetivas inventadas sem cálculo formal -> `[FAIL: Ausência de auditoria matemática determinística]`

---

### Regra 6: Fronteira Limpa com `evoluir-skills` e `skill-auditor-refatorador-skills`
- **Critério**: A skill atuou exclusivamente em arquitetura de agentes, runtimes, tools e métricas, delegando criação ou auditoria de arquivos `SKILL.md` do catálogo para as skills irmãs?
- **Resultado**:
  - Fronteira respeitada sem sobreposição -> `[PASS]`
  - Mistura de responsabilidades de manutenção de catálogo -> `[FAIL: Violação de fronteira SSOT]`
