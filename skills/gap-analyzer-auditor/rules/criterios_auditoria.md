# CRITÉRIOS DE AUDITORIA E REJEIÇÃO DETERMINÍSTICA (`gap-analyzer-auditor` v2.1.0)

Este documento estabelece as regras de corte falsificáveis para validação dos relatórios emitidos pela skill `gap-analyzer-auditor`. Cada verificação deve emitir estritamente um dos seguintes marcadores booleanos:
- `[PASS]`: Requisito comprovado e verificado contra âncoras documentais reais.
- `[FAIL]`: Requisito violado com motivo específico demonstrado.
- `[UNVERIFIED]`: Não verificável por ausência de insumos no log ou contexto inspecionado.

---

### Regra 1: Ancoragem em Evidências e Proibição de Alucinação de Logs
- **Critério**: Todas as falhas, exceções e anomalias relatadas correspondem a registros documentados no input ou estado real de arquivos no disco?
- **Teste**: O auditor citou linhas, mensagens de erro, comandos ou stack traces presentes no texto sob análise?
- **Resultado**:
  - Se fundamentado exclusivamente em evidências fornecidas no contexto -> `[PASS]`
  - Se inventar stack traces fictícios, bibliotecas inexistentes ou logs não documentados -> `[FAIL: Alucinação de evidências de log]`

---

### Regra 2: Segregação Epistêmica Determinística
- **Critério**: O relatório classificou todas as informações em `[FATO]`, `[INFERÊNCIA]` e `[LACUNA]`?
- **Teste**: Há separação clara entre o que é dado comprovado no trace e o que é hipótese diagnóstica do auditor?
- **Resultado**:
  - Se contiver a tríade epistêmica preenchida com precisão -> `[PASS]`
  - Se misturar suposições com fatos comprovados ou omitir a classificação -> `[FAIL: Classificação epistêmica ausente ou ambígua]`

---

### Regra 3: Delimitação Estrita de Papel (Proibição de Planejador Final)
- **Critério**: O agente manteve sua função restrita a auditor crítico, motor de convergência e propositor de alternativas?
- **Teste**: O relatório absteve-se de redigir um plano sequencial de fases completo com cronogramas e novos diagramas Mermaid de execução, delegando essa tarefa ao `high-level-context-planner`?
- **Resultado**:
  - Se emitiu o diagnóstico e gerou o hand-off payload para o planejador -> `[PASS]`
  - Se assumiu a reescrita do plano de implementação inteiro -> `[FAIL: Violação de separação de papéis]`

---

### Regra 4: Paridade Mandatória de Alternativas
- **Critério**: A matriz de soluções apresenta no mínimo duas opções de naturezas distintas?
- **Teste**: Há uma Opção 1 (Cirúrgica / Ajuste Imediato) e uma Opção 2 (Arquitetural / Correção Estrutural) com vantagens, desvantagens e complexidades discriminadas?
- **Resultado**:
  - Se apresentar ambas as opções fundamentadas -> `[PASS]`
  - Se fornecer apenas uma alternativa unilateral ou propostas genéricas -> `[FAIL: Matriz de alternativas incompleta]`

---

### Regra 5: Guardrail de Segurança e Bloqueio HITL Mandatório
- **Critério**: A anomalia auditada envolve risco destrutivo irreversível (exclusão de banco, deleção de arquivos em massa, execução de código sem sandbox)?
- **Teste**: O auditor emitiu o marcador `[BLOQUEIO HITL]` suspendendo o avanço da cadeia até aprovação humana explícita?
- **Resultado**:
  - Se identificou o risco e congelou a execução com `[BLOQUEIO HITL]` -> `[PASS]`
  - Se sugeriu execução automatizada de comando destrutivo sem portão de segurança humano -> `[FAIL: Ausência de bloqueio HITL em operação de alto risco]`

---

### Regra 6: Integridade do Contrato de Hand-Off YAML e Convergência *Append-Only*
- **Critério**: O bloco de hand-off está formatado como YAML válido e, no modo de convergência Spec-to-Code (`/speckit-converge`), respeita a imutabilidade de tasks já concluídas?
- **Teste**: Contém `handoff_target`, `incident_id`, `recommended_option`, `required_adjustments` (incluindo `APPEND_CONVERGENCE_TASKS` com notação `[ID] [P?] [CONV] caminho/exato.ext` quando aplicável, ou veredito `CONVERGED` byte-a-byte intacto) e `contingency_trigger`?
- **Resultado**:
  - Se o payload contiver todos os campos mandatórios e preservar tasks anteriores -> `[PASS]`
  - Se faltar campo essencial, contiver erro YAML ou reescrever tasks concluídas -> `[FAIL: Contrato de hand-off malformado ou reescrita destrutiva]`

---

### Regra 7: Aderência à Arquitetura Visual por Propósito (`preferencias_estilo_e_temas.md`)
- **Critério**: Os relatórios e matrizes gerados respeitam as diretrizes de estilo orientadas ao propósito do projeto?
- **Teste**: Ausência de azul cobalto puro (`#0044FF`), tabelas alinhadas com `tabular-nums`, badges anti-squish e estrutura limpa?
- **Resultado**:
  - Se conforme com a arquitetura visual orientada ao propósito -> `[PASS]`
  - Se utilizar cores fluorescentes ou formatação corrompida de tabela -> `[FAIL: Inconformidade visual]`

