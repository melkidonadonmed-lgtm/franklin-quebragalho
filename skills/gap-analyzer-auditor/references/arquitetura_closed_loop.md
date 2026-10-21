# Arquitetura de Orquestração em Malha Fechada e Esteira de 3 Portões (`Closed-Loop Reflection` v2.1.0)

Este documento descreve a topologia e dinâmica operacional da reflexão em malha fechada (*closed-loop reflection*) integrando os **3 Portões Determinísticos de Qualidade e Convergência** (`code-acceptability-auditor` -> `test-quality-auditor` -> `gap-analyzer-auditor`) ao planejador estratégico (`high-level-context-planner`).

---

## 1. Topologia da Esteira de 3 Portões e Grafos de Estado (State Graphs)

No ecossistema multiagente (Google ADK / LangGraph / Antigravity), a orquestração desacoplada previne que o agente executor ou planejador sofra de viés de confirmação (*self-confirmation bias*) ou da *Ilusão do Build Verde*:

```text
        ┌────────────────────────────────────────────────────────┐
        │             HIGH-LEVEL CONTEXT PLANNER                 │
        │   (Fase 0, Decomposição de Fases, Spec.md & Tasks.md)  │
        └───────────────────────────┬────────────────────────────┘
                                    │
                            [Código & Suítes]
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │   PORTÃO 1: CODE-ACCEPTABILITY-AUDITOR (v1.1.0)        │
        │   (AST + Pydantic v2: 12 Regras, Score >= 75.0, 0 Crit)│
        └───────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │   PORTÃO 2: TEST-QUALITY-AUDITOR (v1.2.0)              │
        │   (5 Domínios Py/TS/Go/MCP/Harness + PerfKit, Nível 4) │
        └───────────────────────────┬────────────────────────────┘
                                    │
                  [Violação AST / Falha AAA / Diff Spec]
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │   PORTÃO 3: GAP-ANALYZER-AUDITOR (v2.1.0)              │
        │   (Isolamento [FATO]/[INFERÊNCIA]/[LACUNA], RCA 4 Vet.,│
        │    /speckit-converge Append-Only & Hand-off YAML)      │
        └───────────────────────────┬────────────────────────────┘
                                    │
               [CONVERGED | APPEND_CONVERGENCE_TASKS YAML]
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │            REVISÃO E CONVERGÊNCIA DO PLANO             │
        │       (Anexação Imutável de Tasks ou Homologação)      │
        └────────────────────────────────────────────────────────┘
```

---

## 2. Princípios de Desacoplamento e Statelessness

1. **Auditor Stateless**: O `gap-analyzer-auditor` não retém estado persistente de turnos anteriores. Ele avalia o payload de contexto imediato fornecido na chamada, garantindo que o diagnóstico seja puramente baseado nas evidências factuais atuais.
2. **Separação de Preocupações (SoC) nos 3 Portões**:
   - **Portão 1 (`code-acceptability-auditor`)**: Inspeciona o código de produção via AST (`SYN001`, `SEC001..003`, `ERR001..003`, `TYP001..002`, `ARCH001..003`).
   - **Portão 2 (`test-quality-auditor`)**: Inspeciona a suíte de testes e `evals/` (`python`, `ts_js`, `go`, `mcp`, `harness`, `perfkit_stats.py`) contra a *Ilusão do Build Verde*.
   - **Portão 3 (`gap-analyzer-auditor`)**: Diagnostica onde e por que o fluxo ou a convergência Spec-to-Code falhou, classifica a severidade e aponta alternativas conceituais (Opção 1 vs Opção 2) + Hand-off YAML.
   - **Planejador (`high-level-context-planner`)**: Absorve as recomendações e anexa tasks corretivas (*append-only*) ou atualiza a esteira de execução.

---

## 3. Dinâmica do Hand-Off Estruturado

O canal de comunicação entre o auditor e o planejador não utiliza linguagem natural difusa. Ele opera via contrato YAML padronizado:
- `handoff_target`: Define o nó receptor no grafo (`high-level-context-planner`).
- `incident_id`: Identificador único do ciclo de auditoria para rastreabilidade.
- `recommended_option`: Seleção entre correção cirúrgica (`Opção 1`) ou refatoração arquitetural (`Opção 2`).
- `required_adjustments`: Lista de ações cirúrgicas mapeadas por etapa (`step`, `action`, `patch_instructions`), incluindo `APPEND_CONVERGENCE_TASKS` com notação `[ID] [P?] [CONV] caminho/exato.ext`.
- `contingency_trigger`: Condição determinística para ativação do plano B em tempo de execução.
