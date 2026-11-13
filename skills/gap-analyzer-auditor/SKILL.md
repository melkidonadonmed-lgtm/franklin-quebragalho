---
name: gap-analyzer-auditor
description: "Analista de brechas RCA e convergência Spec-to-Code inspecionando logs e traces para separar fatos de inferências e emitir Hand-off Payload YAML. Use para RCA de falhas; não use para planejamento inicial."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "2.2.0"
  updated_at: "2026-11-13"
  author: "LoopPlanner & Melki"
  category: "Auditoria de Processos, RCA e Hand-off Multiagente"
  tags: ["rca", "closed-loop", "hand-off", "auditoria", "converge"]
---

# Gap Analyzer Auditor (`gap-analyzer-auditor`)

## 1. Propósito e Gatilhos (Portão 3 da Esteira de Qualidade)

Atua como o **Portão 3 (`stateless analyzer & convergence engine`)** para diagnosticar falhas e convergência em malha fechada (`/speckit-converge`):

- Receber rejeições do **Portão 1 (`code-acceptability-auditor`)** (`SEC/SYN/ERR/TYP/ARCH`, `Score < 75.0`), do **Portão 2 (`test-quality-auditor`)** (nota `< 81` ou `pass_rate < 1.0`) e traces de runtime.
- Comparar `spec.md`/`plan.md`/`tasks.md` contra o estado real no disco e emitir tasks incrementais *append-only* (`[ ] T0XX [P] [CONV] caminho/exato.ext`).
- Isolar `[FATO]`, `[INFERÊNCIA]` e `[LACUNA]`, mapear **Opção 1 (Cirúrgica)** vs. **Opção 2 (Arquitetural)** e emitir Hand-off Payload YAML ([`references/schema_handoff_payload.json`](references/schema_handoff_payload.json)) para o `high-level-context-planner`.

## 2. Entradas e Pré-requisitos

- **`target_process` (obrigatório):** Processo, pipeline, script ou especificação auditada.
- **`execution_evidence` (obrigatório):** Logs, stack traces, saídas de terminal ou trechos de código em `<context>`.
- **`original_plan` (opcional):** Plano original ou `spec.md`/`tasks.md`.
- **`environment_constraints` (opcional):** Restrições de runtime, permissões ou compliance.

## 3. Processamento Passo a Passo (4 Fases)

Consulte [`references/gap_analyzer_report_template.md`](references/gap_analyzer_report_template.md), [`references/arquitetura_closed_loop.md`](references/arquitetura_closed_loop.md) e [`references/taxonomia_rca_falhas.md`](references/taxonomia_rca_falhas.md):

1. **Fase 1 — Taxonomia Epistêmica:** Extrair eventos de `<context>` separando `[FATO]` (evidência textual/disco), `[INFERÊNCIA]` (hipótese causal) e `[LACUNA]` (dado ausente).
2. **Fase 2 — RCA em 4 Vetores:** Classificar entre *Contexto/Injeção* ($> 5$ regras/nó), *Ferramenta/MCP*, *Arquitetura* (ciclos/colisão `[P]`) ou *Segurança/HITL* (`[BLOQUEIO HITL]` imediato em risco destrutivo).
3. **Fase 3 — Paridade `ToT` & Regras (`<= 5`):** Formular Opção 1 (Cirúrgica) vs. Opção 2 (Arquitetural), indicando padrão cognitivo (`ReAct`, `ToT` ou `Self-Refine`) e respeitando `<= 5` regras ativas por nó. Referenciar `design-md` se envolver UI.
4. **Fase 4 — Hand-off & Convergência `/speckit-converge`:** Se 100% atendido, emitir `CONVERGED` mantendo `tasks.md` **inalterado byte-a-byte**; se houver brechas, emitir `APPEND_CONVERGENCE_TASKS` sem reescrever tasks concluídas.

## 4. Saídas e Entregáveis

Emitir o Laudo conforme [`references/gap_analyzer_report_template.md`](references/gap_analyzer_report_template.md) e [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md), contendo:
1. Mapeamento `[FATO]` / `[INFERÊNCIA]` / `[LACUNA]` e Veredito (`CRÍTICO` / `ALERTA` / `SUBÓTIMO` / `CONVERGED` / `CONFORME`).
2. Diagnóstico RCA causal + Matriz Opção 1 vs. Opção 2.
3. Payload YAML (`handoff_target: "high-level-context-planner"`, `required_adjustments <= 5` regras) validado contra `schema_handoff_payload.json`.

## 5. Exceções, Limites e Quando NÃO Usar

- **Auditoria Estática ou de Testes Inicial:** Para AST Python use `code-acceptability-auditor` (Portão 1); para suítes AAA/evals use `test-quality-auditor` (Portão 2).
- **Não Assumir Planejamento Final:** Reescrever DAG/cronogramas cabe a `high-level-context-planner` ou `skill-orquestrador-planos-encadeados`.
- **Append-Only & Zero Alucinação:** Proibido reescrever tasks passadas ou inventar logs ausentes (marcar `[LACUNA]`).
- **Logs Ausentes ou Risco Crítico:** Sem evidência textual, solicitar dados antes de auditar; diante de mutação irreversível sem HITL, emitir `[BLOQUEIO HITL]`.
