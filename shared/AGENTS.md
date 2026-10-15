# AGENTS.md — `franklin-quebragalho/shared`

## 1. Governança de Agentes no Pacote `shared/`
- Qualquer subagente ou ferramenta exposta em `franklin-quebragalho/server.py` passa obrigatoriamente pelos guardas de `shared/harness.py` e `shared/a2a_bridge.py`.
- A suíte de qualidade `tests/test_harness_quality.py` e o módulo `harness_test_auditor.py` auditam as transições de risco e o ciclo de vida completo do `CheckpointStore` com nota `100.0/100` (Nível 4).
