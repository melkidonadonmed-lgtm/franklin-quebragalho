# CRITÉRIOS DE AUDITORIA E REJEIÇÃO DETERMINÍSTICA (`high-level-context-planner` v3.0.0)

Este documento estabelece as regras de conformidade e critérios de corte falsificáveis para validação dos planos emitidos pela skill `high-level-context-planner`. Toda verificação emite obrigatoriamente um dos três marcadores padronizados:

- `[PASS]`: Requisito comprovado e verificado contra âncoras documentais e schemas reais.
- `[FAIL]`: Requisito violado com motivo específico demonstrado.
- `[UNVERIFIED]`: Não verificável por ausência de insumos no briefing inicial.

---

### Regra 1: Triagem de Intenção em 4 Quadrantes e Seleção de Frameworks

- **Critério**: O plano classifica explicitamente a intenção (`direta`, `estruturada`, `ambigua`, `mutacao_critica_hitl`) e seleciona a combinação de framework estrutural (`CLAREZA`, `CREATE`, `RTF`, `TAG`, `TASS`) e padrões cognitivos não-lineares (`CoT`, `ReAct`, `ToT`, `Self-Refine`)?
- **Teste**: Presença dos blocos `intencao` e `frameworks_selecionados` coerentes com a natureza da demanda?
- **Resultado**:
  - Se classificar a intenção e declarar os frameworks -> `[PASS]`
  - Se omitir o diagnóstico de intenção ou aplicar planejamento linear cego em tarefas com incerteza empírica -> `[FAIL: Diagnóstico de intenção ou seleção de frameworks ausente]`

---

### Regra 2: Blindagem contra a Parede de Complexidade ($\le 5$ Regras por Nó)

- **Critério**: Nenhum nó do `grafo_execucao` acumula mais de 5 regras operacionais ativas simultaneamente (`regras_ativas_count <= 5`)?
- **Teste**: Execução de `scripts/cognitive_plan_builder.py` confirma `max_regras_por_no <= 5` e status `SHIELDED` ou `SUBDIVIDED`?
- **Resultado**:
  - Se todos os nós respeitarem o teto de $\le 5$ regras ativas -> `[PASS]`
  - Se qualquer nó contiver $> 5$ restrições simultâneas sem subdivisão -> `[FAIL: Violação da Parede de Complexidade (> 5 regras/nó)]`

---

### Regra 3: Presença Mandatória da Fase 0 e Ramo de Fallback Não-Linear

- **Critério**: O grafo de execução inicia pela Fase 0 (validação de pré-requisitos, schemas e higiene L1/L2) e define rotas de contingência (`ramo_fallback`) para nós sujeitos a falha empírica?
- **Teste**: O primeiro nó é a Fase 0 e os nós críticos possuem `ramo_fallback` e critérios de aceite falsificáveis?
- **Resultado**:
  - Se iniciar na Fase 0 com ramos de fallback definidos -> `[PASS]`
  - Se pular a Fase 0 ou carecer de rotas de contingência -> `[FAIL: Ausência mandatória da Fase 0 ou de ramo_fallback]`

---

### Regra 4: Decomposição Falsificável, Notação `[ID] [P?] [US#]` e Ausência de Colisão

- **Critério**: Todas as fases possuem tasks no formato `[ID] [P?] [US#] caminho/exato.ext` e critérios Go/No-Go objetivos?
- **Teste**: As tasks paralelizadas (`[P]`) tocam arquivos distintos (`target_files` disjuntos) sem conflito de escrita?
- **Resultado**:
  - Se todas as fases possuírem tasks estruturadas sem colisão de arquivo -> `[PASS]`
  - Se contiver critérios vagos ou paralelismo conflitante no mesmo arquivo -> `[FAIL: Tasks sem caminho exato ou paralelismo conflitante]`

---

### Regra 5: Consumo Integral do Hand-Off Payload e Convergência *Append-Only*

- **Critério**: Diante de uma entrada contendo o payload YAML do `gap-analyzer-auditor`, o novo plano incorporou todos os ajustes solicitados em modo *Append-Only*?
- **Teste**: O plano v2.0+ anexa a seção de Convergência (`APPEND_CONVERGENCE_TASKS`) sem apagar ou renumerar tasks já concluídas?
- **Resultado**:
  - Se todas as mitigações forem anexadas sem destruir histórico -> `[PASS]`
  - Se ignorar qualquer ajuste do payload ou reescrever tasks concluídas -> `[FAIL: Violação de hand-off ou reescrita destrutiva de histórico]`

---

### Regra 6: Portão HITL para Mutações Críticas e `Complexity Tracking` (YAGNI)

- **Critério**: Intenções da categoria `mutacao_critica_hitl` ativam `requer_hitl: true` com nó `hitl_gate`, e o plano inclui a tabela `Complexity Tracking` justificando eventuais abstrações extras?
- **Teste**: O plano não executou mutações diretas no disco, interceptou ações irreversíveis com HITL e documentou a vacina YAGNI?
- **Resultado**:
  - Se respeitar o Gate HITL e incluir `Complexity Tracking` -> `[PASS]`
  - Se omitir o Gate HITL em ação destrutiva ou introduzir over-engineering não justificado -> `[FAIL: Violação de segurança HITL ou over-engineering YAGNI]`
