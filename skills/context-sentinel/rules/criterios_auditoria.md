# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA (CONTEXT SENTINEL)

Para garantir que a extração de contexto não alucine nem degrade a sessão, aplique as regras determinísticas:

---

### Regra 1: Validação do Schema Pydantic v2
- **Critério**: O payload gerado é serializável e passa na validação do `StateCheckpointSchema`?
- **Resultado**:
  - Schema estritamente válido -> `[PASS]`
  - Falha de validação ou campos vitais ausentes -> `[FAIL: Schema Pydantic inválido]`

### Regra 2: Classificação Semântica Estrita (FATO / PENDENCIA / LACUNA)
- **Critério**: Todos os itens extraídos estão devidamente categorizados sem suposições genéricas?
- **Resultado**:
  - Classificação correta com evidência no histórico -> `[PASS]`
  - Menção a fatos não comprovados ou tags inválidas -> `[FAIL: Classificação semântica incorreta]`
