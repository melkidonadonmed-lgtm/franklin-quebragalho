---
name: solution-content-architect
description: "Design and implement minimal, strictly typed production code, OpenAPI/JSON-RPC contracts, SQL optimizations, and trade-off blueprints. Use for concrete engineering solutions and enterprise prompts. Do NOT use for standalone prompt audits (refine-prompt), repo AST audits (system-project-auditor), scaffolding, or DAG waves."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
allowed-tools: read_file write_file edit_file run_command
metadata:
  author: "Franklin"
  version: "2.6.1"
  updated_at: "2026-11-18"
  category: "Solution Architecture & Blueprints"
  tags: "solution-content-architect, solucao, solucoes, arquiteto, enterprise, prompts, roadmaps, roadmap, modos, guardrails, modulos, codigo, api, sql, openapi, contratos, backend, cot-tot, structured-output, architecture, blueprints"
---

# `solution-content-architect` (`v2.6.1`) — Right-Sized Engineering & Blueprints

## 1. Overview & Scope

Designs and implements minimal, runnable solutions: strictly typed production code, OpenAPI/JSON-RPC contracts, SQL/storage optimizations, architectural trade-off blueprints, and structured enterprise prompts.

### When NOT to Use
- **Standalone Prompt Auditing:** Delegate epistemic prompt audits or Socratic entropy rewriting to `refine-prompt`.
- **Greenfield Bootstrapping & Repo Sync:** Use `project-idea-organizer` for new-repo scaffolding, `README.md` sync, and Triad v2.1 alignment.
- **DAG Scheduling or Repo AST Audits:** Use `high-level-context-planner` / `chained-plan-orchestrator` for task DAGs, and `system-project-auditor` / `agent-server-auditor` for repo audits.

## 2. Inputs & Prerequisites

- **`technical_request` (required):** Concrete engineering task, API/SQL problem, architectural decision, or structured prompt request.
- **`target_context` (optional):** Existing manifests, schemas, or files read before designing so solutions fit the real stack.

## 3. Step-by-Step Procedure

Selectively load `1–2` domain modules from [`solution_modes_and_modules.md`](references/solution_modes_and_modules.md) and [`domain_specialized_guidelines.md`](references/domain_specialized_guidelines.md):

1. **Phase 1 (`CoT` — Scope & Proportionality Gate):** Pick the simplest runnable abstraction (stdlib and one cohesive module before extra packages or interfaces; wrap untrusted inputs in `<untrusted_user_input>`).
2. **Phase 2 & 3 (`ToT / ReAct + RAW` — Zero Ceremonial Banners):**
   - **Direct Execution (Default for clear scope):** Deliver runnable, strictly typed code, run real CLI/test verification, and execute `Read-After-Write` checks immediately. Omit ceremonial banners, `Phase 0` essays, and redundant alternative appendices—always ship the simplest valid path first.
   - **Blocking `[GAP]` Clarification:** Pause *only* when missing I/O contracts or destructive paths risk rework; ask `1–3` focused questions alongside a minimal working skeleton.
   - **Architectural Fork (`Phase 0 + ToT`):** Activate *only* for multi-service migrations or irreversible storage/protocol forks; lock `In-Scope` vs. `Non-Goals`, compare `2–3` branches against a stdlib/SQLite/monolith baseline, and chain dependent steps.
3. **Phase 4 (`RAW` — Selective Modules & Silent Gate):** Load [`enterprise_prompt_library.md`](references/enterprise_prompt_library.md) *only* for reusable prompts or OpenAPI/SQL contracts; verify silently against [`validation_checklist.md`](references/validation_checklist.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 4. Gotchas & Edge Cases

- **Zero Dead Abstractions & Fake Audits:** Ban single-implementation interfaces, pass-through wrappers, unrequested dependencies, stubs, and invented percentages.
- **HITL & Scope Discipline:** Pause before mass disk/DB mutations; emit explicit `[PASS]`/`[FAIL]`/`[UNVERIFIED]` markers only when an audit or architectural blueprint report is requested.

## 5. Output Schema & Validation Criteria

1. **Direct Code / Contracts:** Complete typed implementation matching existing repo patterns plus verified CLI test/lint commands.
2. **Fork Blueprints / Prompts:** Structured comparison against a simpler baseline or strict JSON/YAML / `[VARIABLE_NAME]` blueprint checked against [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

Internal blueprints, schemas, and code identifiers stay in Technical English; **all user-facing explanations, trade-off comparisons, clarifying questions, and Self-Refine summaries MUST be delivered in Portuguese (Brazil / `pt-BR`)**, unless requested otherwise.
