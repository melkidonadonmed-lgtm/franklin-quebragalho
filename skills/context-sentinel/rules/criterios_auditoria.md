# Critérios Determinísticos de Auditoria — `context-sentinel` (`v1.1.0`)

Regras booleanas e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar a extração de checkpoints e integridade da janela de contexto (Módulo **M1**).

---

## Regra 1: Validação Estrita do Schema Pydantic v2 (`extra="forbid"`)
- **`[PASS]`**: O payload gerado é serializável em JSON e satisfaz 100% dos campos obrigatórios de `StateCheckpointSchema` (`session_id`, `turn_number`, `context_health`, `facts`, `variables`, `next_action`, `requires_context_flush`).
- **`[FAIL: SCHEMA_PYDANTIC_INVALIDO]`**: Campos obrigatórios ausentes, tipos incompatíveis ou chaves extras não declaradas.
- **`[UNVERIFIED]`**: Histórico de sessão inacessível ou turno inicial sem eventos registráveis.

## Regra 2: Classificação Epistêmica Estrita (`[FATO]`, `[PENDENCIA]`, `[LACUNA]`)
- **`[PASS]`**: Todos os itens em `facts` possuem tag válida (`FATO`, `PENDENCIA` ou `LACUNA`), separando ações comprovadas de pendências e parâmetros ausentes.
- **`[FAIL: ALUCINACAO_DE_ESTADO]`**: Registro de inferência não verificada como `FATO` ou omissão de parâmetros desconhecidos que deveriam ser `LACUNA`.

## Regra 3: Isolamento Zero-Trust e Preservação de Histórico
- **`[PASS]`**: Mantém isolamento de `<untrusted_user_input>` e sinaliza `pruning_recommended` sem apagar artefatos silenciosamente.
- **`[FAIL: MUTACAO_SILENCIOSA_OU_INJECAO]`**: Descarte destrutivo de logs sem confirmação ou contaminação das instruções do sistema por dados externos.
