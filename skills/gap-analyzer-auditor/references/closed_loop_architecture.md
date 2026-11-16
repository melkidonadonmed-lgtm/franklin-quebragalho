# Closed-Loop Architecture & 3-Gate Quality Pipeline (`gap-analyzer-auditor` v2.2.0)

This reference defines the decoupled closed-loop reflection topology connecting the **3 Deterministic Quality & Convergence Gates** (`code-acceptability-auditor` -> `test-quality-auditor` -> `gap-analyzer-auditor`) back to `high-level-context-planner`.

---

## 1. 3-Gate Topology & Decoupled State Graphs

In multi-agent orchestration (Google ADK / LangGraph / Antigravity), decoupled reflection prevents executor confirmation bias and **Green Build Illusion**:

```text
        ┌────────────────────────────────────────────────────────┐
        │             HIGH-LEVEL CONTEXT PLANNER                 │
        │   (Phase 0, Task Decomposition, Spec.md & Tasks.md)    │
        └───────────────────────────┬────────────────────────────┘
                                    │
                            [Code & Suites]
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │   GATE 1: CODE-ACCEPTABILITY-AUDITOR                   │
        │   (AST + Pydantic v2: 12 Rules, Score >= 75.0, 0 Crit) │
        └───────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │   GATE 2: TEST-QUALITY-AUDITOR                         │
        │   (5 Modules Py/TS/Go/MCP/Harness + PerfKit, Level 4)  │
        └───────────────────────────┬────────────────────────────┘
                                    │
                  [AST Violation / AAA Fault / Spec Drift]
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │   GATE 3: GAP-ANALYZER-AUDITOR (v2.2.0)                │
        │   ([FACT]/[INFERENCE]/[GAP] Isolation, 4-Vector RCA,   │
        │    /speckit-converge Append-Only & YAML Hand-Off)      │
        └───────────────────────────┬────────────────────────────┘
                                    │
               [CONVERGED | APPEND_CONVERGENCE_TASKS YAML]
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────────┐
        │          PLAN REVISION & APPEND-ONLY CONVERGENCE       │
        │     (Immutable Task Append or Final Release Sign-Off)  │
        └────────────────────────────────────────────────────────┘
```

---

## 2. Decoupling & Statelessness Principles

1. **Stateless Analyzer:** `gap-analyzer-auditor` holds no persistent cross-turn memory. It evaluates only the immediate evidence payload and verified disk state, keeping diagnostics purely factual.
2. **Separation of Concerns (SoC) Across the 3 Gates:**
   - **Gate 1 (`code-acceptability-auditor`):** Static AST inspection of production Python code (`SYN001`, `SEC001..003`, `ERR001..003`, `TYP001..002`, `ARCH001..003`).
   - **Gate 2 (`test-quality-auditor`):** Test suite and `evals/` inspection (`python`, `ts_js`, `go`, `mcp`, `harness`, `perfkit_stats.py`) preventing Green Build Illusion.
   - **Gate 3 (`gap-analyzer-auditor`):** Root-cause diagnostics on runtime failures and Spec-to-Code drift, Option 1 vs. Option 2 parity, and YAML hand-off emission.
   - **Planner (`high-level-context-planner`):** Consumes adjustments append-only without altering completed history.

---

## 3. Structured Hand-Off Contract Dynamics

Auditor-to-planner communication never relies on loose prose; it flows through the validated YAML contract:

- `handoff_target`: Downstream receiver (`high-level-context-planner` or `chained-plan-orchestrator`).
- `incident_id`: Unique audit identifier (`AUDIT-YYYY-MM-DD-XX`) for traceability.
- `recommended_option`: Selection between immediate patch (`Option 1`) and structural fix (`Option 2`).
- `required_adjustments`: List of atomic patch actions (`step`, `action`, `patch_instructions`), including `APPEND_CONVERGENCE_TASKS` with `[ID] [P?] [CONV] exact/path.ext`.
- `contingency_trigger`: Deterministic runtime fallback trigger.
