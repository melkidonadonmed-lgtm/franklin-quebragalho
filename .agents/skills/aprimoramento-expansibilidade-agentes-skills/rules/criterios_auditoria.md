# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA (`aprimoramento-expansibilidade-agentes-skills` v2.0.0)

Toda arquitetura de agente ou especificação de skill avaliada por esta habilidade deve ser auditada contra as 7 regras booleanas abaixo, emitindo exclusivamente `[PASS]`, `[FAIL]` ou `[UNVERIFIED]`:

---

### Regra 1: Divulgação Progressiva em 3 Tiers e Orçamento de Contexto
- **Critério**: A arquitetura separa rigorosamente o Tier 1 (Catálogo ~50–100 tokens), Tier 2 (`SKILL.md` $< 500$ linhas / $< 5.000$ tokens) e Tier 3 (`references/`, `scripts/`, schemas Pydantic carregados sob demanda)?
- **Resultado**:
  - Separação em 3 Tiers respeitada e `SKILL.md` $< 500$ linhas -> `[PASS]`
  - Prompt ou `SKILL.md` monolítico com tabelas/código pesado embutidos no corpo principal -> `[FAIL: Violação da Divulgação Progressiva em 3 Tiers]`

---

### Regra 2: Densidade de Atenção (Softmax) e Instruções Baseadas no "Porquê" (*Lean Instructions*)
- **Critério**: As instruções evitam repetição de regras imperativas redundantes (*over-constraining*), explicam a razão causal ("Porquê") das restrições críticas e extraem lógica repetitiva de runtime para `scripts/`?
- **Resultado**:
  - Instruções enxutas, causais e sem código repetitivo inline -> `[PASS]`
  - Excesso de regras redundantes ou ausência de extração para `scripts/` quando aplicável -> `[FAIL: Baixa densidade atencional ou over-constraining detectado]`

---

### Regra 3: Desacoplamento Modular, Padrão Envelope e Context Forking
- **Critério**: Quando há múltiplas operações ou tarefas longas (20–50 passos), a arquitetura utiliza *Envelope Pattern* (`action` + `payload` tipado) e isola sub-tarefas pesadas via `context: fork` (`invoke_subagent`) com controle de fronteira (*boundary control*)?
- **Resultado**:
  - Roteamento polimórfico tipado e isolamento de contexto implementados -> `[PASS]`
  - Proliferação descontrolada de micro-tools soltas ou contaminação da thread principal -> `[FAIL: Ausência de Envelope Pattern ou isolamento de contexto]`

---

### Regra 4: Arquitetura de Memória em 3 Camadas
- **Critério**: O estado do agente distingue fisicamente o *Scratchpad Transitório*, o *Estado de Sessão* e o *Memory Bank de Longo Prazo* (com proveniência e integridade)?
- **Resultado**:
  - Camadas de memória separadas e persistência durável estruturada -> `[PASS]`
  - Mistura de raciocínio transitório com memória perene ou dependência exclusiva do histórico bruto de chat -> `[FAIL: Acoplamento indevido de camadas de memória]`

---

### Regra 5: Avaliação Estruturada (*Eval-Driven Iteration*) e Métricas Formais
- **Critério**: O plano de qualidade define casos `evals/evals.json` comparáveis (*Baseline vs. Treatment*), métricas de correção funcional ($\text{Pass}@k$), rubrica normalizada ($S_{\text{norm}} \in [0, 100]$) e, para guardrails críticos, tolerância $\text{FNR} < 0.001$?
- **Resultado**:
  - Suíte de avaliação empírica e métricas definidas -> `[PASS]`
  - Validação puramente subjetiva ("parece bom") sem baseline nem asserções -> `[FAIL: Ausência de ciclo Eval-Driven e métricas formais]`

---

### Regra 6: Matriz de Otimização de Gatilhos (*Trigger Eval Matrix*)
- **Critério**: Os testes de ativação incluem consultas positivas variadas (`should-trigger`) e consultas negativas limítrofes (`should-not-trigger` / *near-misses*) com separação conceitual contra *overfitting* da `description`?
- **Resultado**:
  - Consultas `should-trigger` e `should-not-trigger` (*near-misses*) documentadas -> `[PASS]`
  - Ausência de testes de falso positivo / *near-miss* -> `[FAIL: Matriz de gatilhos incompleta sem proteção contra near-misses]`

---

### Regra 7: Interoperabilidade Aberta (`MCP` / `A2A`) e Portões `HITL`
- **Critério**: As integrações externas priorizam protocolos abertos (`MCP` JSON-RPC 2.0, `A2A` Agent Cards) e impõem portões *Human-in-the-Loop (HITL)* antes de qualquer mutação destrutiva ou irreversível?
- **Resultado**:
  - Contratos tipados MCP/A2A e portões HITL ativos -> `[PASS]`
  - Mutações destrutivas sem confirmação ou acoplamento proprietário opaco -> `[FAIL: Violação de interoperabilidade ou ausência de portão HITL]`
