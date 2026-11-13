# Estágios do Motor DAG e Context Fork — Orquestrador de Planos Encadeados

Referência detalhada dos 5 estágios executivos usada por [`../SKILL.md`](../SKILL.md) e pelo contrato [`schema_transicao_contexto.json`](schema_transicao_contexto.json).

## Diagrama de Compilação e Despacho

```mermaid
flowchart TD
    A["Entrada: Grafo de Execução (JSON) ou Plano Multifásico"] --> B["Estágio 1: Compilação Topológica de Kahn (scripts/dag_chain_validator.py)"]
    B -->|Ciclo, Lacuna ou Colisão| B1["[FAIL] Bloqueio Imediato na Fase 0"]
    B -->|Grafo Válido| C["Estágio 2: Agrupamento em Ondas Paralelas (Wave 0 -> Wave 1 -> Wave 2)"]
    C --> D["Estágio 3: Montagem do Envelope Context Fork (<= 5 regras, isolated_state_key)"]
    D --> E{"Estágio 4: Despacho e Avaliação do Nó"}
    E -->|Go (Critério Aprovado)| F["Estágio 5: Verificação Read-After-Write e Avanço"]
    E -->|No-Go Recuperável| G["Acionar ramo_fallback Não-Linear ou 1 Ciclo Self-Refine"]
    E -->|Risco Destrutivo| H["[BLOCKED_HITL] Suspender no Harness (franklin_harness_checkpoint)"]
```

## Detalhamento dos Estágios

1. **Estágio 1 — Kahn, Ambiguidade & Anti-Colisão (`dag_chain_validator.py`):**
   - **Gestão de Ambiguidade:** Bloquear `[LACUNA]` em aberto devolvendo ao planejador/usuário antes de compilar ondas.
   - **Detecção de Ciclos (DAG):** Calcular `in_degree`; se `visited_nodes < total_nodes`, abortar com `[FAIL: CYCLE_DETECTED]`.
   - **Anti-Colisão `[P]` (`target_files`):** Interceptar nós na mesma `Wave K` com interseção em `target_files` (`[FAIL: PARALLEL_FILE_COLLISION]` ou serialização).
   - **Validação de Catálogo:** Confirmar que `responsible_skill`/`target_skill` existe no catálogo.
2. **Estágio 2 — *Context Fork* (`schema_transicao_contexto.json`):** Instanciar `ContextTransitionPayload` (`phase_id`, `wave_index`, `sequence_index`, `target_skill`, `cognitive_pattern`, `isolated_state_key`, `input_payload`, `active_rules <= 5`, `target_files`, `expected_outputs`, `acceptance_criteria`, `fallback_branch`, `status`) sem histórico bruto.
3. **Estágio 3 — *Fan-Out* & *Fan-In*:** `invoke_subagent` isolado por `isolated_state_key` ou `franklin_execute_dag` (`shared/execution_orchestrator.py` com `run_id`, `--resume`, `idempotency_key`).
4. **Estágio 4 — Roteamento Não-Linear & HITL:** `COMPLETED` (libera próxima onda após *Read-After-Write*), `RETRYING`/`FALLBACK_ROUTED` (`max_retries = 1` -> `fallback_branch`/`ramo_fallback`), `BLOCKED_HITL` (`franklin_harness_guard`/`franklin_harness_checkpoint`) ou `FAILED` (escala ao `gap-analyzer-auditor`).
