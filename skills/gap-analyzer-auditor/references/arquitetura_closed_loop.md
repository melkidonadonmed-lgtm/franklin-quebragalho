# Arquitetura de Orquestração em Malha Fechada (Closed-Loop Reflection)

Este documento descreve a topologia e dinâmica operacional da reflexão em malha fechada (*closed-loop reflection*) entre o `high-level-context-planner` e o `gap-analyzer-auditor`.

---

## 1. Topologia de Grafos de Estado (State Graphs)

No ecossistema multiagente (Google ADK / LangGraph), a orquestração desacoplada previne que o agente planejador sofra de viés de confirmação (*self-confirmation bias*). A presença de um nó auditor independente garante que planos de alta complexidade sejam estressados criticamente antes da implantação final.

```text
       ┌────────────────────────────────────────────────────────┐
       │             HIGH-LEVEL CONTEXT PLANNER                 │
       │    (Planejamento Estratégico, Decomposição de Fases)   │
       └───────────────────────────┬────────────────────────────┘
                                   │
                           [Plano Proposto]
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │              EXECUTION / SANDBOX RUNTIME               │
       │      (Dry-run, Compilação de Testes, Logs/Traces)      │
       └───────────────────────────┬────────────────────────────┘
                                   │
                        [Trace / Erros / Gargalo]
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 GAP-ANALYZER-AUDITOR                   │
       │      (Isolamento Epistêmico, RCA, Hand-off Payload)    │
       └───────────────────────────┬────────────────────────────┘
                                   │
                     [Contrato de Hand-Off YAML]
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │            REVISÃO E APROVAÇÃO DO PLANO                │
       │        (Atualização de Fases com Mitigações)           │
       └────────────────────────────────────────────────────────┘
```

---

## 2. Princípios de Desacoplamento e Statelessness

1. **Auditor Stateless**: O `gap-analyzer-auditor` não retém estado persistente de turnos anteriores. Ele avalia o payload de contexto imediato fornecido na chamada, garantindo que o diagnóstico seja puramente baseado nas evidências factuais atuais.
2. **Separação de Preocupações (SoC)**:
   - O **Auditor** diagnostica onde e por que o fluxo falhou, classifica a severidade e aponta alternativas conceituais (Opção 1 vs Opção 2).
   - O **Planejador** absorve as recomendações e reescreve a esteira de execução com dependências e diagramas atualizados.

---

## 3. Dinâmica do Hand-Off Estruturado

O canal de comunicação entre o auditor e o planejador não utiliza linguagem natural difusa. Ele opera via contrato YAML padronizado:
- `handoff_target`: Define o nó receptor no grafo.
- `incident_id`: Identificador único do ciclo de auditoria para rastreabilidade.
- `recommended_option`: Seleção entre correção cirúrgica ou refatoração arquitetural.
- `required_adjustments`: Lista de ações cirúrgicas mapeadas por etapa (`step`, `action`, `patch_instructions`).
- `contingency_trigger`: Condição determinística para ativação do plano B em tempo de execução.
