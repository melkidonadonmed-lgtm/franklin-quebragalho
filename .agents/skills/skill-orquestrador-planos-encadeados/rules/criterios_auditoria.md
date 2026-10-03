# CRITÉRIOS DETERMINÍSTICOS DE ORQUESTRAÇÃO DE PLANOS ENCADEADOS

Para assegurar a transição previsível entre etapas e prevenir alucinações de fluxo, o orquestrador deve aplicar as seguintes regras determinísticas avaliadas sob:
- `[PASS]`: Requisito comprovado e verificado sem ambiguidade.
- `[FAIL]`: Requisito violado com bloqueio imediato do avanço.
- `[UNVERIFIED]`: Dado não verificável por ausência de insumos.

---

### Regra 1: Validação Estrutural da Fase 0
- **Critério**: O plano possui fases numeradas coerentes e todas as skills citadas existem no catálogo?
- **Teste**:
  - Toda fase possui: objetivo, skill responsável, inputs declarados, outputs esperados e critérios de aceite.
  - As skills citadas estão presentes e ativas em `.agents/skills/` ou no catálogo oficial.
- **Classificação**:
  - Se todas as fases forem válidas e as skills existirem -> `[PASS]`
  - Se faltar insumo vital ou citar skill inexistente -> `[FAIL: Skill inexistente ou plano incompleto na Fase 0]`

---

### Regra 2: Detecção de Dependências Cíclicas
- **Critério**: A topologia do plano forma um grafo acíclico direcionado (DAG)?
- **Teste**:
  - Não há referências circulares onde uma fase depende do resultado de uma fase futura.
- **Classificação**:
  - Se a ordenação topológica for estrita -> `[PASS]`
  - Se houver ciclo detectado -> `[FAIL: Loop circular de dependência identificado]`

---

### Regra 3: Isolamento Estrito de Contexto (Context Hygiene)
- **Critério**: O payload transferido entre fases contém exclusivamente as variáveis necessárias?
- **Teste**:
  - O histórico bruto inteiro da conversa NÃO deve ser injetado nas skills filhas.
  - O payload deve obedecer à estrutura do `schema_transicao_contexto.json`.
- **Classificação**:
  - Se o payload for isolado e tipado -> `[PASS]`
  - Se houver injeção indiscriminada de contexto residual -> `[FAIL: Violação de higiene de contexto (context rot)]`

---

### Regra 4: Verificação dos Critérios de Aceite na Transição
- **Critério**: O entregável da fase atende a todos os critérios antes de disparar a próxima?
- **Teste**:
  - O output gerado pela skill contém os campos e artefatos requeridos pelo contrato.
- **Classificação**:
  - Se aprovado com evidência mensurável -> `[PASS]`
  - Se houver inconsistência recuperável -> Disparar 1 ciclo de auto-correção.
  - Se houver inconsistência irrecuperável -> `[FAIL: Critério de aceite não atingido]`

---

### Regra 5: Salvaguardas Human-in-the-Loop (HITL)
- **Critério**: Ações potencialmente destrutivas foram submetidas para aprovação humana prévia?
- **Teste**:
  - Exclusão em massa, alterações irreversíveis no sistema de arquivos ou deploys requerem parada com confirmação explícita.
- **Classificação**:
  - Se respeitar os pontos de parada HITL -> `[PASS]`
  - Se disparar ações críticas de forma autônoma sem consentimento -> `[FAIL: Violação de salvaguarda HITL]`
