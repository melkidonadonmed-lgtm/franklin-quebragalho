# CRITÉRIOS DETERMINÍSTICOS DE ORQUESTRAÇÃO E COMPILAÇÃO DAG (`skill-orquestrador-planos-encadeados` v3.0.0)

Para assegurar a compilação em ondas paralelas (Kahn), prevenir colisões de escrita e eliminar *context rot*, o orquestrador aplica as seguintes regras determinísticas avaliadas sob:

- `[PASS]`: Requisito comprovado e verificado por `scripts/dag_chain_validator.py`.
- `[FAIL]`: Requisito violado com bloqueio imediato do avanço.
- `[UNVERIFIED]`: Dado não verificável por ausência de insumos.

---

### Regra 1: Ordenação Topológica de Kahn e Ausência de Ciclos (DAG)

- **Critério**: O grafo do plano forma um Grafo Acíclico Dirigido (DAG) compilável em ondas (`Wave 0..Wave N`)?
- **Teste**:
  - `scripts/dag_chain_validator.py` comprova `has_cycle == False` e agrupa os nós em ondas topológicas válidas.
- **Classificação**:
  - Se a ordenação topológica for estrita -> `[PASS]`
  - Se houver ciclo detectado -> `[FAIL: Loop circular de dependência identificado (CYCLE_DETECTED)]`

---

### Regra 2: Guarda Anti-Colisão de Escrita em Ondas Paralelas (`[P]`)

- **Critério**: Nós alocados na mesma onda paralela (`Wave K`) tocam conjuntos disjuntos de arquivos (`target_files`)?
- **Teste**:
  - Dois subagentes ou tasks rodando em paralelo na mesma onda não disputam escrita simultânea no mesmo caminho de arquivo.
- **Classificação**:
  - Se `file_collisions` for vazio -> `[PASS]`
  - Se houver interseção de `target_files` na mesma onda -> `[FAIL: Colisão de escrita paralela detectada (PARALLEL_FILE_COLLISION)]`

---

### Regra 3: Isolamento Estrito de Contexto (*Context Fork*) e Teto de $\le 5$ Regras

- **Critério**: O envelope `ContextTransitionEnvelope` contém apenas os dados necessários (`input_payload`), chave isolada (`isolated_state_key`) e no máximo 5 regras ativas (`active_rules <= 5`)?
- **Teste**:
  - O histórico bruto da conversa (`full_chat_history`, `raw_transcript`) NÃO é injetado nos subagentes e nenhum nó excede 5 regras simultâneas.
- **Classificação**:
  - Se o payload for isolado, tipado e respeitar $\le 5$ regras -> `[PASS]`
  - Se houver injeção de histórico bruto ou $> 5$ regras ativas -> `[FAIL: Violação de higiene de contexto ou Parede de Complexidade]`

---

### Regra 4: Roteamento Não-Linear (`fallback_branch`) e Verificação *Read-After-Write*

- **Critério**: O entregável de cada onda passa por verificação de estado real antes de avançar, desviando para `fallback_branch` em falhas recuperáveis?
- **Teste**:
  - O output gerado atende aos `acceptance_criteria` ou aciona `RETRYING` / `FALLBACK_ROUTED` de forma determinística.
- **Classificação**:
  - Se validado com evidência mensurável -> `[PASS]`
  - Se falhar após retry e fallback sem rota -> `[FAIL: Critério de aceite não atingido]`

---

### Regra 5: Salvaguardas Human-in-the-Loop (`BLOCKED_HITL`)

- **Critério**: Nós do tipo `hitl_gate` ou ações destrutivas foram pausados em `BLOCKED_HITL` aguardando aprovação humana?
- **Teste**:
  - Mutações críticas exigem checkpoint ativo e `approval_token` antes da execução.
- **Classificação**:
  - Se respeitar os pontos de parada HITL -> `[PASS]`
  - Se disparar ações críticas sem consentimento -> `[FAIL: Violação de salvaguarda HITL]`
