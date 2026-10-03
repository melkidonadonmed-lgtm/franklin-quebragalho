# CRITÉRIOS DE AUDITORIA E REJEIÇÃO (TEMPLATE PADRÃO 2026)

Toda execução desta skill deve ser verificada contra critérios determinísticos falsificáveis:

---

### Regra 1: Validação de Pré-requisitos
- **Critério**: O ambiente atende às dependências necessárias para a tarefa?
- **Resultado**:
  - Dependências atendidas e confirmadas -> `[PASS]`
  - Dependência ausente ou comando indisponível -> `[FAIL: Dependência não encontrada]`

### Regra 2: Ausência de Dados Inventados (Zero Alucinação)
- **Critério**: Todas as métricas, arquivos ou retornos citados correspondem à realidade?
- **Resultado**:
  - Dados verificados em disco/sistema -> `[PASS]`
  - Menção a dados simulados ou fictícios sem validação -> `[FAIL: Dados não verificados]`
