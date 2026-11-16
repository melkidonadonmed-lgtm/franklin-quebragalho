# Operational Modes & 7 Domain Modules — `solution-content-architect`

Detailed execution reference for Modes A–D and Modules M1–M7 consumed by [`SKILL.md`](../SKILL.md), complementing [`enterprise_prompt_library.md`](enterprise_prompt_library.md), [`validation_checklist.md`](validation_checklist.md), and [`domain_specialized_guidelines.md`](domain_specialized_guidelines.md).

## The 4 Operational Modes

- **MODE A — DIRECT EXECUTION:** Triggered by explicit, well-scoped imperative commands ("build", "implement", "generate", "optimize"). Ask zero questions; deliver the complete solution immediately.
- **MODE B — ITERATIVE REFINEMENT:** Triggered by vague objectives, critical `[GAP]` parameters, or exploratory requests ("help me think through"). Ask **1 to 3 high-leverage strategic questions** and attach a structured preliminary draft.
- **MODE C — STRUCTURED PLANNING (`Phase 0 + CoT + ToT`):** Triggered by architectural blueprints, multi-module roadmaps, or trade-off comparisons. Open with **Phase 0 (Premises & Ambiguities)**, compare 2–3 branches in **ToT** (*what changes, how it changes, trade-offs, and optimal cost/risk/outcome branch*), and detail sequential **CoT** stages (Objective, Method, Dependencies, Deliverables, Effort).
- **MODE D — PRE-DELIVERY SELF-REFLECTION:** Apply [`validation_checklist.md`](validation_checklist.md) prior to finalizing the output and attach a concise verification summary.

## The 7 Domain Modules (`domain_specialized_guidelines.md`)

1. **`M1` — Execution, Code & Agents:** Modules `<= 600` lines, Early Return (`<= 3` nesting levels), `Pydantic v2 extra="forbid"` / `Zod .strict()`, non-interactive `argparse` CLIs, structured `stdout` + diagnostic `stderr`, `recovery_hint`, `max_steps`/`deadline_seconds`, and Read-After-Write verification.
2. **`M2` — Design & Layouts:** Decouple Macrolayout (`@media`) from Microlayout (`container-type: inline-size` + `@container`), Flexbox/Grid, and logical CSS properties (`inline-size`, `padding-inline`, `box-sizing: border-box`).
3. **`M3` — Frontend, UI & Styling:** Semantic HTML5, anti-XSS (no raw `innerHTML`), WCAG 2.1 AA, `tabular-nums`, real 4-state FSM (`idle`, `loading`, `empty`/`success`, `error` — zero placebos) aligned with `design-md` and `rules/frontend-9-axes-guidelines.md`.
4. **`M4` — Research & Source of Truth:** Strict precedence: **(1st)** disk code/AST/manifests (`pyproject.toml`, `go.mod`, `package.json`, `.context/spec.md`); **(2nd)** official docs via MCP (`google-developer-knowledge`, `gemini_get_doc`; never use `gemini_search_docs`, which is disabled locally) or official web specs; **(3rd)** Obsidian vault notes. Tag **`[FACT]`** (`file:line`/URL), **`[INFERENCE]`**, and **`[GAP]`**, isolating untrusted inputs inside `<untrusted_user_input>`.
5. **`M5` — Image Generation:** Final prompt in **ENGLISH** with all **8 Visual Pillars** and `--no text, watermark, blur, low quality`.
6. **`M6` — Video Generation:** Final prompt in **ENGLISH** with **1 dominant action + 1 camera movement** and physical continuity.
7. **`M7` — Clinical & Healthcare:** PII/PHI anonymization, **4-Step Causal Chain** (*Pathophysiology -> Presentation -> Workup -> Conduct*), **6-Pillar Prescribing** (*Drug, Dose, Route, Frequency, Duration, Contraindications*), Institution/Year guideline citation, and explicit disclaimers.
