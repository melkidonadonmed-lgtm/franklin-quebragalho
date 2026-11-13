---
name: skill-orquestrador-planos-encadeados
description: "Orquestrador executivo de planos encadeados DAG mapeando dependências entre skills especialistas e executando ondas sequenciais com Context Fork. Use para orquestrar planos DAG; não use para turno único."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "3.0.0"
  updated_at: "2026-11-13"
  author: "LoopPlanner & Melki"
  category: "Orquestração DAG, Compilação de Ondas, Context Fork & Transição de Estado"
  tags: ["orquestrador", "planos-encadeados", "dag", "kahn", "context-fork", "multiagente"]
---

# Orquestrador de Planos Encadeados DAG (`skill-orquestrador-planos-encadeados`)

## 1. Propósito e Gatilhos (Quando Usar)

Motor executivo de **Compilação Topológica (Kahn)**, isolamento **Context Fork** ($\le 5$ regras/nó) e roteamento de estado entre skills/subagentes:

- Compilar planos (`CognitiveAdaptivePlan` / `DAGExecutionPlan` / `plans/*.json`) do `high-level-context-planner` em ondas paralelas (`Wave 0..N`) via `invoke_subagent` ou `franklin_execute_dag`.
- Validar deterministicamente com `scripts/dag_chain_validator.py` antes do disparo: detecção de ciclos, anti-colisão de escrita (`[P]` `target_files`), gestão de ambiguidade (`[LACUNA]` zero), `ramo_fallback` e portões HITL.

## 2. Entradas e Parâmetros

- **`structured_plan` / `grafo_execucao` (obrigatório):** Plano `CognitiveAdaptivePlan` (`grafo_execucao`), `DAGExecutionPlan` (`tasks`) ou `phases`.
- **`execution_mode` (opcional):** `native_subagents`, `franklin_dag` (`franklin_execute_dag`) ou `step_by_step`.
- **`max_retries` (opcional):** Tentativas por nó antes de `ramo_fallback` ou escalonamento ao `gap-analyzer-auditor` (padrão: `1`).

## 3. Processamento em 5 Estágios e Automação

Consulte o fluxo completo em [`references/estagios_dag_e_context_fork.md`](references/estagios_dag_e_context_fork.md) e [`references/schema_transicao_contexto.json`](references/schema_transicao_contexto.json):

1. **Estágio 1 — Kahn, Ambiguidade & Colisão:** Bloquear `[LACUNA]` não esclarecida, detectar ciclos (`CYCLE_DETECTED`), impedir edição paralela no mesmo `target_files` (`PARALLEL_FILE_COLLISION`) e validar skills no catálogo.
2. **Estágio 2 — *Context Fork* (`<= 5` regras):** Instanciar `ContextTransitionPayload` enxuto por `isolated_state_key` (nunca repassar histórico bruto).
3. **Estágio 3 — *Fan-Out* / *Fan-In*:** Despachar ondas via `invoke_subagent` ou `franklin_execute_dag` (`run_id`, `--resume`, `idempotency_key`).
4. **Estágios 4–5 — Fallback, HITL & Read-After-Write:** Rotear `fallback_branch` (`ramo_fallback`) em falha recuperável, suspender `hitl_gate` em `franklin_harness_guard` / `franklin_harness_checkpoint` e escalar falhas finais ao `gap-analyzer-auditor`.

```powershell
uv run python skills/skill-orquestrador-planos-encadeados/scripts/dag_chain_validator.py --self-test
uv run python skills/skill-orquestrador-planos-encadeados/scripts/dag_chain_validator.py --plan plans/distributed_agent_mediation_dag.json
```

## 4. Saídas e Entregáveis

1. **Mapa de Ondas Topológicas (Kahn Waves)** com `isolated_state_key` por nó.
2. **Painel de Rastreabilidade:** `Onda | Nó | Skill | Padrão Cognitivo | Regras (<=5) | Status`.
3. **Veredito *Read-After-Write* (`post_condition_verified: true/false`)**.

## 5. Exceções, Limites e Quando NÃO Usar

- **Turno Único ou Concepção Inicial:** Não use para scripts isolados (turno único) nem para planejar do zero (use `high-level-context-planner`).
- **Proibição de Context Rot e Colisão ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)):** Proibido injetar transcrição bruta, disparar grafo com ciclo/`PARALLEL_FILE_COLLISION` ou bypassar `hitl_gate` sem `approval_token` válido.
