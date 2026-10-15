# ESPECIFICAÇÃO TÉCNICA (`SPEC.md`) — `franklin-quebragalho/shared`

## 1. Contratos de Segurança e Interconectividade (`shared/`)
1. **`SemanticGuard` (`harness.py`)**:
   - Bloqueia injeções de prompt (`ignore previous instructions`, `<script>`, `system prompt override`) e *Path Traversal* (`..`) levantando `SecurityViolationError`.
2. **`CheckpointStore` (`harness.py`)**:
   - Persiste checkpoints HITL em `.sessions/harness_checkpoints.json` com estados `PENDING`, `APPROVED`, `REJECTED` e `EXPIRED`.
3. **`FranklinA2ATaskManager` (`a2a_bridge.py`)**:
   - Valida `AgentCard` contra Protobuf (`a2a.types.AgentCard`), assina com JCS (RFC 8785) + HMAC-SHA256 e isola `user_id` de `context_id` externo:
     - Ações `READ_ONLY` / `REVERSIBLE_WRITE` -> `TASK_STATE_COMPLETED`
     - Ações `CRITICAL_MUTATION` -> `TASK_STATE_INPUT_REQUIRED` (cria checkpoint HITL)
     - Violação `SemanticGuard` -> `TASK_STATE_REJECTED`
