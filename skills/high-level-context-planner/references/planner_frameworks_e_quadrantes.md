# Matriz de Quadrantes, Frameworks & Blindagem (`high-level-context-planner`)

Complemento detalhado de [`SKILL.md`](../SKILL.md). Veja também [`matriz_decisao_go_no_go.md`](matriz_decisao_go_no_go.md), [`protocolo_consumo_handoff.md`](protocolo_consumo_handoff.md) e [`schema_plano_contexto.json`](schema_plano_contexto.json).

## 1. Matriz de 4 Quadrantes de Intenção

| Categoria | Definição | Despacho | Padrão Cognitivo |
| :--- | :--- | :--- | :--- |
| **`1. direta`** | Comando único, consulta ou ajuste pontual sem ambiguidade | Entrega direta sem fases | `Zero-Shot` / `CoT` leve |
| **`2. estruturada`** | Demanda multifacetada com dependências ou múltiplos módulos | Grafo DAG com Fase 0, `[ID] [P?] [US#]` e `ramo_fallback` | `ReAct` ou `CoT` + `ToT` |
| **`3. ambigua`** | Pedido exploratório ou lacunas críticas (*gestão de ambiguidade*) | Hipóteses concorrentes, poda e definição de MVP | `CREATE` + `ToT` |
| **`4. mutacao_critica_hitl`** | Ação destrutiva, drop/alteração DB, deploy ou segredos | Pausa imediata + checkpoint (`requer_hitl: true`) | `ReAct` + Approval Gate |

## 2. Frameworks Estruturais + Padrões Cognitivos

- **Estruturais:** `CLAREZA` (código/auditorias zero-alucinação), `CREATE` (ideação/SPEC/MVP), `RTF` (tabelas/extrações), `TAG` (automações diretas), `TASS` (docs executivos).
- **Cognitivos:** `CoT` (causa-consequência), `ReAct` (Thought -> Tool -> Observation), `ToT` (ramos concorrentes Opção 1 vs. Opção 2 + poda Go/No-Go), `Self-Refine` (revisão contra critérios).

## 3. As 4 Salvaguardas contra *Prompt Complexity Wall* & Append-Only

1. **Teto `regras_ativas_count <= 5` por nó:** Subdividir em `step_02a`/`step_02b` ao exceder 5 regras.
2. **Progressive Disclosure (`L1 -> L2 -> L3`):** L1 ~100 tokens, L2 etapa ativa, L3 scripts/schemas sob demanda.
3. **Hard Constraints em Código:** Pydantic v2 `extra="forbid"` / scripts em `scripts/`.
4. **Context Fork `[P]` + Append-Only (`/speckit-converge`):** Tasks paralelas só em arquivos disjuntos; nunca reescrever `[x] T001` concluídas — anexar `## Fase N: Convergência & Mitigação` com `- [ ] T0XX [P] [CONV] caminho/exato.ext`.
