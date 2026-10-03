# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA (GERAR DOCS PDF)

---

### Regra 1: Validação de Existência do PDF
- **Critério**: O arquivo PDF foi gerado fisicamente no disco e possui tamanho maior que zero?
- **Resultado**:
  - Arquivo PDF presente com tamanho > 0 bytes -> `[PASS]`
  - Falha na conversão ou arquivo não encontrado -> `[FAIL: Arquivo PDF não gerado]`

### Regra 2: Fidelidade de Layout e Quebras de Página
- **Critério**: O CSS contém regras para evitar corte inadequado de tabelas e blocos (`page-break-inside: avoid;`)?
- **Resultado**:
  - CSS com regras de impressão válidas -> `[PASS]`
  - Layout quebrado sem regras de impressão -> `[FAIL: CSS sem controle de quebra de página]`
