---
name: high-level-context-planner
description: "Planejador de contexto de alto nível decompondo metas em fases numeradas com Fase 0, tasks paralelizáveis e Complexity Tracking. Use para planejar épicos complexos; não use para comando único."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "3.0.0"
  updated_at: "2026-11-13"
  author: "LoopPlanner & Melki"
  category: "Análise de Intenção, Planejamento Cognitivo Não-Linear & Engenharia de Contexto"
  tags: ["planejamento", "dag", "cot-tot", "react", "complexity-wall", "convergencia"]
---
# SKILL: `high-level-context-planner` (`v3.0.0`) — Planejamento Não-Linear (DAG)

Motor cognitivo de diagnóstico de intenção, seleção de frameworks, blindagem contra a *Parede de Complexidade* ($\le 5$ regras/nó) e planejamento em grafo não-linear (Fase 0, tasks `[ID] [P?] [US#]` e Convergência *Append-Only*). Quadros e detalhamento constam em [`references/planner_frameworks_e_quadrantes.md`](references/planner_frameworks_e_quadrantes.md).

## 1. Quando Usar (Gatilhos) e Quando NÃO Usar

- **Quando Usar:** Solicitações complexas/multifásicas com decomposição atômica e precedência DAG; combinação de frameworks (`CLAREZA`, `CREATE`, `RTF`, `TAG`, `TASS`) com `CoT`, `ReAct`, `ToT` e `Self-Refine`; auditoria/subdivisão contra teto $\le 5$ regras/nó; ou replanejamento *Append-Only* a partir de `Hand-off Payload (YAML)` do `gap-analyzer-auditor`.
- **Quando NÃO Usar:** Tarefas simples (`1. direta`) entregues imediatamente; mutações destrutivas sem subagente/portão HITL; RCA forense inicial de logs/stack traces (use primeiro `gap-analyzer-auditor`).

## 2. Entradas e Parâmetros Esperados

- `strategic_goal` / `user_query` (obrigatório): Pedido, requisito ou ideia bruta.
- `handoff_payload` (condicional): YAML de [`references/protocolo_consumo_handoff.md`](references/protocolo_consumo_handoff.md).
- `operational_constraints` (opcional): Limites de ambiente, caminhos (`target_dir`) e `max_rules_per_node = 5`.

## 3. Processamento e Fluxo em 5 Módulos

1. **Módulo 1 — Triagem & Gestão de Ambiguidade:** Classifique entre `1. direta`, `2. estruturada`, `3. ambigua` (esclareça lacunas antes de consolidar etapas) ou `4. mutacao_critica_hitl` (`requer_hitl: true`).
2. **Módulo 2 — Frameworks (`CLAREZA`/`CREATE`/...) + Cognitivo (`CoT`/`ReAct`/`ToT`/`Self-Refine`).**
3. **Módulo 3 — Complexity Wall Shield:** Mantenha `regras_ativas_count <= 5` por nó (dividindo nós pesados), `L1->L2->L3`, Pydantic v2 `extra="forbid"` e isolamento Context Fork em tasks `[P]`.
4. **Módulo 4 — DAG Fase 0 & Append-Only:** Exija `step_00_fase_zero`, `[ID] [P?] [US#]` em arquivos disjuntos, `ramo_fallback` em incerteza e append-only `/speckit-converge` sem alterar tasks concluídas.
5. **Módulo 5 — Validação Determinística:**
   ```powershell
   uv run python skills/high-level-context-planner/scripts/cognitive_plan_builder.py --self-test
   uv run python skills/high-level-context-planner/scripts/cognitive_plan_builder.py --intent "<objetivo>" --framework CLAREZA
   uv run python skills/high-level-context-planner/scripts/cognitive_plan_builder.py --validate-file plano.json --export-dag dag_plan.json
   ```

## 4. Saídas e Entregáveis

1. **Contrato JSON** conforme [`references/schema_plano_contexto.json`](references/schema_plano_contexto.json) (`max_regras_por_no <= 5`, `ramo_fallback`, `target_files`).
2. **Plano Markdown:** Diagrama Mermaid (`flowchart TD`), checklist `[ID] [P?] [US#]`, Matriz Go/No-Go ([`references/matriz_decisao_go_no_go.md`](references/matriz_decisao_go_no_go.md)) e tabela `Complexity Tracking`.

## 5. Limites, Self-Refine e Guardrails ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md))

- Proibido planejamento linear cego em incerteza (declare `ReAct`/`ToT` + `ramo_fallback`), violar `>5` regras/nó, pular Fase 0, reescrever histórico na convergência, colidir `target_files` em `[P]` ou bypassar `requer_hitl: true`.
