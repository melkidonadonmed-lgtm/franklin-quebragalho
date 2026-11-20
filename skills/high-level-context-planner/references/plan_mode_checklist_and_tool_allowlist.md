# Plan Mode Variations, Read-Only Tool Allowlist & Minimum Checklist

Operational Playbook aligning `high-level-context-planner` with the canonical Plan Mode architecture (`DRAFT -> AWAITING_APPROVAL -> EXECUTING -> COMPLETED`).

## 1. Request-Driven Plan Mode & Read-Only Tool Allowlist

Select the matching Plan Mode variation and expose **only** its read-only tool allowlist while planning (`write_file`, `edit_file`, deletes, deploys, and DB writes stay disabled):

| Request Type | Plan Mode Variation | Allowed Read-Only Tools (Allowlist) | Blocked Until Approval |
| :--- | :--- | :--- | :--- |
| **Atomic / Single-Turn (`direta`)** | *Bypass Plan Mode* | Direct execution (no multi-phase overhead) | Destructive commands still require HITL |
| **Idea / PRD / Architecture (`ambigua`)** | **Idea / Concept Plan Mode** | `read_file`, `search_web`, `mempalace_search`, `ask_question` (`<= 3`), `CREATE`/`ToT` | Any repo scaffold, file creation, or external side effect |
| **UI / Screen / Design System** | **Visual Plan Mode** *(delegate to `ui-brand-ux-planner`)* | `read_file`, `modern-web-guidance`, `stitch`/`figma` read-only, `chrome-devtools` snapshot/screenshot | CSS/TSX edits, `DESIGN.md` writes, `npm run build` |
| **Multi-File Code / Refactor (`estruturada`)** | **Code & Files Plan Mode** | `read_file` (bounded ranges), `rg`/`Select-String`, `git status`/`log`/`diff`, AST/static inspectors (`code_acceptability_auditor`, `gopls`) | `write_file`, `edit_file`, refactors, migrations, `git push` |
| **Destructive / Clinical / Deploy (`mutacao_critica_hitl`)** | **HITL-Gated Plan Mode** | Read-only allowlist above + `ask_question` (`<= 3` surgical questions) | All mutations until explicit human `approval_token` |

## 2. Minimum Pre-Execution Checklist (Mandatory Before Leaving Plan Mode)

Every plan emitted by `high-level-context-planner` MUST verify these **6 minimum gates** tailored to the request before handing off to `chained-plan-orchestrator` or execution:

- [ ] **1. Read-Only Isolation:** Zero write/edit/destructive tools were invoked during planning.
- [ ] **2. Scope & Non-Goals:** Explicit 2-sentence **Objective** plus **Non-Goals / Risk Zones** (what must NOT be touched).
- [ ] **3. Verified Disk Targets:** Every file path, symbol, or endpoint cited in the plan was verified via read-only inspection (no invented paths).
- [ ] **4. Request-Matched Tool Allowlist & Fallback:** Each phase names the exact tools required for execution and a deterministic `ramo_fallback` on failure.
- [ ] **5. Complexity Wall Shield (`<= 5` rules/node):** No step exceeds `5` active constraints; parallel `[P]` tasks own disjoint `target_files`.
- [ ] **6. Measurable Acceptance & HITL Gate:** Every phase has a physical post-condition (`exit code 0`, test count, SHA-256) and `requer_hitl: true` on destructive/clinical/deploy steps.

## 3. Minimum Post-Execution Checklist (Read-After-Write)
- [ ] Ordered completion with `[DONE:n]` / checkbox tracking and `Read-After-Write` disk verification.
- [ ] Canonical linter/test suite passed (`exit code 0`), zero secrets leaked, and execution stayed within step/timeout budget.
