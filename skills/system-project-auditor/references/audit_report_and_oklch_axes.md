# Stack-Adaptive Rubric, Federated UI Criteria & Output Template (`system-project-auditor` v6.1.0)

Level 3 reference complementing [`pillars_5_matrix_and_handoff_2026.md`](pillars_5_matrix_and_handoff_2026.md) and [`audit_rubric_and_agent_browser.md`](audit_rubric_and_agent_browser.md).

## 1. Conditional Criteria for UI Targets (`has_ui_layer == True`)

If `has_ui_layer == False`, skip this section completely, emit **`[PASS: N/A_BACKEND_ONLY]`**, and reallocate the `20` UI points to AST, Contract, and Docs-vs-Disk Parity health.

When UI exists, enforce the **single canonical UI SSOT** in `shredded-shape/rules/frontend-9-axes-guidelines.md` (never duplicate divergent Dark Mode `L` or glow values here):
- **Perceptual 5-Plane `OKLCH 60-30-10`:** `oklch()` + `light-dark()`, `color-mix(in oklab, ...)`, zero `#000000`, `C <= 0.20` target (hard cap `0.22`, semantic red `15°..40° <= 0.24`), Dark Mode `well < canvas < card < card-lit` with zenithal sheen + top specular rim (zero neon card glows).
- **Navigation, Ergonomics & WCAG 2.2:** `<= 3` `<nav>` landmarks (`<= 6` items/nav, `gap >= 8px`, `>= 13px` labels), `44/48px` targets (`<40px` hard blocker), silent CSS breadcrumbs (`::before`), `@container`, `DOM == Tab Order`, and executable 5-state FSM.
- **Federated Deep UI Pipeline (`shredded-shape`):** Escalate deep visual refactors or judging to the **4-Stage Actor-Critic pipeline** (`ui-analyst -> ui-planner -> ui-worker <-> ui-judge`, plus `stitch-canvas` for Google Stitch CLI/MCP).

## 2. Unified `0–100 pts` Output Format (Defect-Driven Remediation)

```markdown
# UNIFIED PROJECT, REAL-CODE, MVP & NAVIGATION AUDIT REPORT (v6.1.0)
- **Project & Path:** [Name / Path] | **Stack Profile:** `[BACKEND_CLI_OR_LIB | AGENT_OR_MCP_SERVER | WEB_OR_FULLSTACK_UI | HYBRID_AGENT_UI]`
- **Detected Complexity Level:** `[Tier S Micro (1-4 files) | Level 1..3 | Polyglot MCP]`
- **Deterministic Scores:** **Overall Score:** `XX/100` | **SGA:** `XX.XX/100` | **TIF:** `[PASS | FAIL]`

## 1. EXECUTIVE MVP DIAGNOSIS & DOCS-VS-REAL-CODE PARITY (40 pts UI / 50 pts Headless)
- **Primary Objective & Current State:** [Summary from real source AST and `.context/{spec,context}.md`]
- **Missing for MVP (0 if clean):** 1. **[Blocker]:** [Description] — **Why:** [Real causal impact]

| Item / Path | Real Classification (AST/Disk) | Evidence |
| :--- | :--- | :--- |
| `[File / Module]` | `[IMPLEMENTED_FUNCTIONAL | SUPERFICIAL_MOCK | DOCUMENTED_MISSING | GHOST_CODE]` | `[Line / Symbol]` |

## 2. 5 TECHNICAL PILLARS MATRIX (60 pts UI / 50 pts Headless)
| Pillar | Verdict (`[PASS | FAIL | PASS: N/A_BACKEND_ONLY]`) | Priority | Action & Evidence (`file:line`) |
| :--- | :--- | :--- | :--- |
| **1. Design 60-30-10 OKLCH & Optics (UI Only)** | ... | `[PRIORITY | MODERATE | N/A]` | ... |
| **2. Navigation (`X activates Y` / CLI Entrypoint)** | ... | ... | ... |
| **3. AST Code Quality, Stubs & Orphans** | ... | ... | ... |
| **4. Security, `.gitignore`/`.env` & MCP/RPC Contracts** | ... | ... | ... |
| **5. Temporal Baseline & Physical Tree** | ... | ... | ... |

## 3. DEFECT-DRIVEN REMEDIATION LIST (1:1 Evidence-Traced; 0 items if clean)
- If `verdict == [PASS]` and zero blockers exist, output: `No structural remediation required.`
- Otherwise, list concrete tasks referencing `[file:line]` or scanner findings:
  - [ ] **[Priority]:** [Concrete fix + exact file:line]
```
