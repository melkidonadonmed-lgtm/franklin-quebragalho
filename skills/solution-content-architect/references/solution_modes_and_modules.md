# Operational Branches & Selective Domain Modules — `solution-content-architect` (`v2.6.0`)

Detailed execution reference consumed selectively by `SKILL.md`, complementing [`domain_specialized_guidelines.md`](domain_specialized_guidelines.md), [`enterprise_prompt_library.md`](enterprise_prompt_library.md), and [`validation_checklist.md`](validation_checklist.md).

## Task Signal -> Execution Branch -> Forbidden Ceremony

| Task Signal | Active Branch | Required Deliverable | Forbidden Ceremony |
| :--- | :--- | :--- | :--- |
| Clear coding, bugfix, API, or SQL task | **Direct Execution** (`Mode A` implicit) | Typed, runnable code + real CLI verification command | `MODE A` banners, Phase 0 essays, `ToT` matrices, prompt wrappers, or fake "simpler alternatives" |
| Missing I/O schema, security boundary, or conflicting constraints | **Blocking `[GAP]` Clarification** (`Mode B`) | `1–3` concrete decision questions + minimal typed skeleton | Broad questionnaires (`> 3` questions) or greenfield repo bootstrapping |
| Multi-service migration, storage choice, or protocol fork | **Architectural Fork Blueprint** (`Mode C`) | `In-Scope`/`Non-Goals` + `2–3` `ToT` branches vs. Simpler Baseline + sequential `CoT` | Abstract prose decoupled from runtime costs, dependencies, or consumer paths |
| Explicit audit or blueprint self-check requested | **Pre-Delivery Verification** (`Mode D`) | Concise `[PASS]` / `[FAIL]` / `[UNVERIFIED]` check table | Visible checklist bloat on routine direct coding turns |

## Selective Domain Modules (`1–2` Active Modules Max per Task)

Load **only** the modules directly required by the task domain:

1. **`M1` — Execution, Code & Agents (Code/API/CLI tasks):** Modules `<= 600` lines, Early Return (`<= 3` nesting levels), `Pydantic v2 extra="forbid"` / `Zod .strict()` / Go `DisallowUnknownFields()`, `argparse` on CLIs, structured `stdout` + diagnostic `stderr`, `max_steps`/`deadline_seconds` on agent/retry loops, and Read-After-Write verification.
2. **`M2` — Layout & Information Density (UI components only):** Decouple Macrolayout (`@media`) from Microlayout (`@container`), logical CSS (`inline-size`, `padding-inline`), `<= 35` words per card block.
3. **`M3` — Frontend Visual Physics (Federated to `shredded-shape`):** Semantic HTML5, anti-XSS (no raw `innerHTML`), WCAG 2.2 AA, `tabular-nums`, real 4-state FSM (`idle`, `loading`, `success`, `error`), aligned with `shredded-shape` (`ui-brand-ux-planner` / `DESIGN.md` and `frontend-9-axes-guidelines.md`).
4. **`M4` — Research & Source of Truth (Investigation/Architecture tasks):** **(1st)** disk code/AST/manifests (`pyproject.toml`, `go.mod`, `package.json`, `.context/spec.md`); **(2nd)** official docs via `google-developer-knowledge` / `gemini_get_doc`; **(3rd)** Obsidian notes. Tag `[FACT]`/`[INFERENCE]`/`[GAP]` and isolate external data inside `<untrusted_user_input>`.
5. **`M5` — Image Generation Prompts (*Explicit media prompt requests only*):** Prompt in **ENGLISH** with all **8 Visual Pillars** and `--no text, watermark, blur, low quality`.
6. **`M6` — Video Generation Prompts (*Explicit video prompt requests only*):** Prompt in **ENGLISH** with **1 dominant action + 1 camera movement** and physical continuity.
7. **`M7` — Clinical & Healthcare (*Explicit clinical workflows only*):** PII/PHI anonymization, **4-Step Causal Chain**, **6-Pillar Prescribing**, Institution/Year guideline citations, and disclaimers.
