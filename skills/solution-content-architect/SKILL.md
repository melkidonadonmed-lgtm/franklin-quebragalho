---
name: solution-content-architect
description: "Architect end-to-end technical solutions, enterprise prompt libraries, typed code, and 4-mode execution roadmaps (Modes A-D) with 7 Domain Guardrail Modules. Use when solving multi-domain engineering problems, generating structured outputs, or designing system blueprints. Do NOT use for isolated epistemic prompt audits, Socratic entropy rewriting, or DAG scheduling."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
metadata:
  author: "Franklin"
  version: "2.5.0"
  updated_at: "2026-11-16"
  category: "Solution Architecture & Blueprints"
  tags: ["solution-content-architect", "solucao", "solucoes", "arquiteto", "enterprise", "roadmaps", "roadmap", "modos", "guardrails", "modulos", "codigo", "cot-tot", "structured-output", "architecture", "blueprints"]
---

# `solution-content-architect` (`v2.5.0`) — 4-Mode Solution Architect

## 1. Overview & Scope

Designs verifiable technical blueprints, typed code, enterprise prompt libraries, and `CoT + ToT` roadmaps across **4 Modes (A–D)** and **7 Domain Modules (`M1..M7`)**.

### When NOT to Use
- **Standalone Prompt Auditing:** Delegate epistemic prompt audits or entropy rewriting to `refine-prompt`.
- **DAG Scheduling:** Use `high-level-context-planner` (Phase 0 graphs) and `chained-plan-orchestrator` (Kahn waves).
- **Skill / Repo Audits:** Use `agent-server-auditor` or `system-project-auditor`.

## 2. Inputs & Prerequisites

- **`technical_request` (required):** Engineering, API, or multi-domain design demand.
- **`target_mode` (optional):** Declare one mode on **line 1**: **`MODE A`** (Direct Execution -> zero questions), **`MODE B`** (Iterative Refinement -> `1–3` strategic questions + draft), **`MODE C`** (Structured Planning -> Phase 0 + `ToT` + `CoT`), **`MODE D`** (Self-Reflection via [`validation_checklist.md`](references/validation_checklist.md)).

## 3. Step-by-Step Procedure

Consult [`solution_modes_and_modules.md`](references/solution_modes_and_modules.md), [`domain_specialized_guidelines.md`](references/domain_specialized_guidelines.md), and [`enterprise_prompt_library.md`](references/enterprise_prompt_library.md):

1. **Classify & Isolate:** Declare Mode A/B/C and wrap untrusted data in `<untrusted_user_input>`.
2. **Apply `ToT` & Modules (`M1..M7`):**
   - **`M1` Code/Agents:** `<= 600` lines, Early Return (`<= 3` levels), `Pydantic v2 extra="forbid"` / `Zod .strict()`, `argparse`, `stdout`/`stderr` split, `max_steps`.
   - **`M2`/`M3` UI/Design:** `@media` + `@container`, logical CSS, WCAG 2.1 AA, real FSM states, `design-md` alignment.
   - **`M4` Truth Hierarchy:** Disk/AST -> official MCP docs (`google-developer-knowledge`/`gemini_get_doc`) -> Obsidian; tag `[FACT]`/`[INFERENCE]`/`[GAP]`.
   - **`M5`/`M6` Media (EN):** 8 Pillars (Image) / 1 action + 1 camera move (Video). **`M7` Clinical:** PII masking, 4-step chain, 6-pillar prescribing, disclaimers.
3. **Run Mode D:** Verify via [`validation_checklist.md`](references/validation_checklist.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 4. Gotchas & Edge Cases

- **Zero Synthetic Audits:** Ban fake percentages or hashes; emit `[PASS]`/`[FAIL]`/`[UNVERIFIED]`.
- **HITL & Context:** Pause before mass disk/DB mutations; suggest `/compact` after 10 dense turns.

## 5. Output Schema & Validation Criteria

1. **Code & Roadmaps (`Mode A/C`):** Declared mode, Phase 0 + `ToT` trade-offs, zero-placebo typed code, real CLI commands, and **1 simpler alternative**.
2. **Structured Output / Prompts:** Strict JSON/YAML or `[VARIABLE_NAME]` blueprint checked via [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

Internal blueprints, schemas, and code identifiers stay in Technical English; **all user-facing explanations, ToT comparisons, clarifying questions, and Self-Refine summaries MUST be delivered in Portuguese (Brazil / `pt-BR`)**, unless requested otherwise.
