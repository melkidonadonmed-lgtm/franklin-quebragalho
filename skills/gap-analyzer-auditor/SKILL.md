---
name: gap-analyzer-auditor
description: "Perform stateless 4-vector Root Cause Analysis (RCA) and Spec-to-Code convergence audits over logs, traces, and artifacts, separating [FACT]/[INFERENCE]/[GAP] and emitting YAML Hand-off Payloads. Use when diagnosing pipeline failures or Spec drift. Do NOT use for Phase 0 planning (high-level-context-planner), Python AST scans (code-acceptability-auditor), or test grading (test-quality-auditor)."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: read_file run_command
metadata:
  author: "Franklin"
  version: "2.2.0"
  updated_at: "2026-11-16"
  category: "Process Auditing, RCA & Convergence"
  tags: "gap-analyzer-auditor, brechas, rca, handoff, hand-off, convergencia, spec-to-code, closed-loop, yaml, logs, traces, auditoria"
---

# `gap-analyzer-auditor` (`v2.2.0`) — 4-Vector RCA & Convergence

## 1. Overview & Scope

Stateless **Gate 3** analyzer for closed-loop failure diagnostics and Spec-to-Code convergence (`/speckit-converge`):

- Diagnose Gate 1 (`code-acceptability-auditor`) rejections (`Score < 75.0`), Gate 2 (`test-quality-auditor`) failures, and runtime tracebacks.
- Diff `spec.md`/`plan.md`/`tasks.md` against disk state, emit append-only tasks (`- [ ] T0XX [P] [CONV] exact/path.ext`), separate `[FACT]`/`[INFERENCE]`/`[GAP]`, compare **Option 1 (Surgical)** vs. **Option 2 (Architectural)**, and emit YAML hand-offs for `high-level-context-planner`.

### When NOT to Use
- **Gate 1 / Gate 2 Scans:** Use `code-acceptability-auditor` (static Python AST) or `test-quality-auditor` (AAA test grading).
- **Final Execution Planning:** Delegate Phase 0 plans and Kahn wave dispatch to `high-level-context-planner` or `chained-plan-orchestrator`.

## 2. Inputs & Prerequisites

- **`target_process` (required):** Process, pipeline, or spec under audit.
- **`execution_evidence` (required):** Verbatim logs, traces, terminal output, or code in `<context>`.
- **`original_plan` / `environment_constraints` (optional):** Baseline plan, `spec.md`/`tasks.md`, runtime bounds.

## 3. Step-by-Step Procedure

Consult [`gap_analyzer_report_template.md`](references/gap_analyzer_report_template.md), [`closed_loop_architecture.md`](references/closed_loop_architecture.md), and [`rca_failure_taxonomy.md`](references/rca_failure_taxonomy.md):

1. **Phase 1 — Epistemic Typing:** Isolate verbatim `[FACT]` entries, `[INFERENCE]` deductions, and `[GAP]` missing telemetry.
2. **Phase 2 — Causal CoT & 4-Vector RCA:** Trace `Trigger -> Propagation -> Breakage Point` (`CoT`) and classify into *Context/Injection* (`> 5` rules/node), *Tooling/MCP*, *Architecture* (cycles/`[P]` collisions), or *Security/HITL* (emit `[HITL BLOCK]` on destructive risk).
3. **Phase 3 — ToT Parity (`<= 5` rules):** Contrast Option 1 (Surgical) vs. Option 2 (Architectural), suggest cognitive pattern (`ReAct`/`ToT`/`Self-Refine`), and reference `ui-brand-ux-planner` (`DESIGN.md`) for UI defects.
4. **Phase 4 — Hand-Off & `/speckit-converge`:** Emit `CONVERGED` (leaving `tasks.md` untouched) or `APPEND_CONVERGENCE_TASKS` append-only.

## 4. Gotchas & Edge Cases

- **No Fabricated Evidence:** Never invent unseen stack frames; tag truncated logs explicitly as `[GAP]`.
- **Append-Only & Role Lock:** Never erase completed `[x]` tasks or rewrite full execution timelines/Mermaid schedules.

## 5. Output Schema & Validation Criteria

Emit the report from [`gap_analyzer_report_template.md`](references/gap_analyzer_report_template.md) validated against [`rules/audit_criteria.md`](rules/audit_criteria.md) and [`handoff_payload_schema.json`](references/handoff_payload_schema.json) (`[FACT]`/`[INFERENCE]`/`[GAP]`, Verdict, Option 1 vs. 2, and YAML hand-off `<= 5` rules/patch).

## 6. User Communication Rule

All internal audit schemas and YAML hand-off payloads MUST stay in Technical English; however, **all user-facing audit explanations, `[HITL BLOCK]` alerts, Option 1 vs. 2 rationales, and Self-Refine summaries MUST be delivered in Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.
