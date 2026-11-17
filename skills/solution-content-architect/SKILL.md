---
name: solution-content-architect
description: "Design and implement minimal, strictly typed production code, OpenAPI/JSON-RPC contracts, SQL/data optimizations, and domain blueprints. Use when solving concrete engineering problems, comparing real architectural trade-offs, or crafting structured enterprise prompts. Do NOT use for isolated epistemic prompt audits, Socratic entropy rewriting, codebase-wide AST scoring, greenfield scaffolding, or DAG scheduling."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
metadata:
  author: "Franklin"
  version: "2.6.0"
  updated_at: "2026-11-17"
  category: "Solution Architecture & Blueprints"
  tags: ["solution-content-architect", "solucao", "solucoes", "arquiteto", "enterprise", "prompts", "roadmaps", "roadmap", "modos", "guardrails", "modulos", "codigo", "api", "sql", "openapi", "contratos", "backend", "cot-tot", "structured-output", "architecture", "blueprints"]
---

# `solution-content-architect` (`v2.6.0`) — Right-Sized Engineering & Blueprints

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

Consult [`solution_modes_and_modules.md`](references/solution_modes_and_modules.md) and [`domain_specialized_guidelines.md`](references/domain_specialized_guidelines.md) selectively (`1–2` modules matching the domain):

1. **Step 0 — Scope & Proportionality Gate (YAGNI):** Identify the exact artifact requested and pick the smallest abstraction that runs end-to-end (stdlib and one cohesive module before extra packages or interfaces; wrap untrusted inputs in `<untrusted_user_input>`).
2. **3-Branch Execution Logic (Zero Ceremonial Banners):**
   - **Direct Execution (Default for clear scope):** Deliver runnable, strictly typed code and real CLI verification commands immediately. Omit `MODE A` banners, Phase 0 essays, `ToT` matrices, prompt wrappers, and artificial "1 simpler alternative" appendices—the primary deliverable MUST already be the simplest valid path.
   - **Blocking `[GAP]` Clarification:** Activate *only* when missing I/O contracts, constraints, or destructive paths would cause rework; ask `1–3` focused decision questions alongside a minimal working skeleton.
   - **Architectural Fork Blueprint (`Phase 0 + ToT + CoT`):** Activate *only* for multi-service migrations or irreversible protocol/storage forks; lock `In-Scope` vs. `Non-Goals`, compare `2–3` concrete branches against a **stdlib / SQLite / modular-monolith Simpler Baseline**, and sequence `CoT` steps so each step consumes the prior step's output.
3. **Selective Domain Loading & Silent Gate:** Load [`enterprise_prompt_library.md`](references/enterprise_prompt_library.md) *only* when authoring reusable prompts or OpenAPI/SQL contracts; verify silently against [`validation_checklist.md`](references/validation_checklist.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 4. Gotchas & Edge Cases

- **Zero Dead Abstractions & Fake Audits:** Ban single-implementation interfaces, pass-through wrappers, unrequested dependencies, stubs, and invented percentages.
- **HITL & Scope Discipline:** Pause before mass disk/DB mutations; emit explicit `[PASS]`/`[FAIL]`/`[UNVERIFIED]` markers only when an audit or architectural blueprint report is requested.

## 5. Output Schema & Validation Criteria

1. **Direct Code / Contracts:** Complete typed implementation matching existing repo patterns plus verified CLI test/lint commands.
2. **Fork Blueprints / Prompts:** Structured comparison against a simpler baseline or strict JSON/YAML / `[VARIABLE_NAME]` blueprint checked against [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

Internal blueprints, schemas, and code identifiers stay in Technical English; **all user-facing explanations, trade-off comparisons, clarifying questions, and Self-Refine summaries MUST be delivered in Portuguese (Brazil / `pt-BR`)**, unless requested otherwise.
