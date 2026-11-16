# Hand-Off Payload Consumption & Append-Only Re-Planning Protocol

This reference specifies how `high-level-context-planner` ingests structured YAML hand-offs from `gap-analyzer-auditor` and synthesizes a revised action plan (`v2.0+`).

---

## 1. Deterministic Patch Action Mapping

When processing `required_adjustments` from an audit payload, apply these graph transformations:

| Action | Graph Operation | Practical Effect on Phase |
| :--- | :--- | :--- |
| **`REFACTOR`** (or legacy `REFATORAR`) | Replace node instructions or data contract | Updates inputs, schemas, or CLI commands on the targeted phase to fix root cause. |
| **`INSERT_GUARDRAIL`** (or `INSERIR_GUARDRAIL`) | Inject intermediate validation gate | Adds a `Phase X.5` gate (linter, schema check, timeout guard) before progression. |
| **`REMOVE_DEPENDENCY`** (or `REMOVER_DEPENDENCIA`) | Break circular coupling | Decouples mutually dependent phases using an asynchronous boundary or intermediate artifact. |
| **`ADD_RETRY`** (or `ADICIONAR_RETRY`) | Attach resilience policy | Configures bounded retries with exponential backoff and explicit `max_retries`. |
| **`HITL_BLOCK`** (or `BLOQUEIO_HITL`) | Insert mandatory approval stop | Halts automation and inserts an interactive `hitl_gate` checkpoint. |
| **`APPEND_CONVERGENCE_TASKS`** | Append-only task extension | Preserves all completed `[x]` tasks untouched and appends `Phase N: Convergence` with `- [ ] T0XX [P?] [CONV] exact/path.ext`. |

---

## 2. Semantic Plan Lifecycle

```text
[Plan v1.0.0: Initial Phase 0 Synthesis]
                   │
                   ▼
[Execution / Pipeline / Simulation]
                   │
          [Failure / Spec Drift]
                   │
                   ▼
[gap-analyzer-auditor: RCA & YAML Hand-Off Payload]
                   │
                   ▼
[high-level-context-planner: Patch & Append-Only Merge]
                   │
                   ▼
[Plan v2.0.0: Converged Plan with Integrated Mitigations]
```

---

## 3. Mitigation Traceability Ledger

Every post-audit plan revision MUST include a **Mitigation & Patch Log** recording:
- Source `incident_id` (e.g., `AUDIT-2026-11-16-01`).
- Selected resolution strategy (`Option 1: Surgical` or `Option 2: Architectural`).
- Exact adjustments applied to graph nodes, `ramo_fallback` routes, and Mermaid topology.
