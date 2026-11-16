# OKLCH Visual Criteria, 3-Layer Navigation & Output Template (`system-project-auditor` v6.0.0)

Detailed Level 3 reference complementing [`SKILL.md`](../SKILL.md), [`pillars_5_matrix_and_handoff_2026.md`](pillars_5_matrix_and_handoff_2026.md), [`audit_rubric_and_agent_browser.md`](audit_rubric_and_agent_browser.md), and [`ui_subagent_taxonomy_6_layers.md`](ui_subagent_taxonomy_6_layers.md).

## 1. Detailed Criteria for Module 3 (60-30-10 OKLCH, Zenith Lighting & SGA Navigation)

- **60-30-10 Ratio (`OKLCH` + `light-dark()`):**
  - **60% Canvas** (`--surface-canvas`, Dark Mode $L = 0.16$, zero `#000000`).
  - **30% Cards & Surfaces** (`--surface-card` $L = 0.22$, `--surface-elevated` $L = 0.27$, 4 variants + `@container`).
  - **10% Surgical Accent** (`--brand-primary` via `oklch(from ...)` / `color-mix(in oklab, ...)`), focus rings, and `6px`/`2px` status indicators.
- **3-Level Shadows:** Primitives (`--shadow-layer-sm/md/lg`) + Semantics (`--shadow-elevation-1..3`, `--shadow-inset`) combining Contact Umbra + negative-spread Penumbra (`-1px..-8px`) + Top Specular Rim (`inset 0 1px 0 0` / `--catch-light`) + Ambient Brand Glow in dark theme.
- **Navigation & Typography:** `<= 3` `<nav>` landmarks (*Global* Bottom Bar with `env(safe-area-inset-bottom)` $\leftrightarrow$ `240px` `100dvh` Sidebar at `>= 48em`; *Local*; *Breadcrumbs* `<ol role="list">` + silent `::before` + `aria-current="page"` only at `>= 3` levels), DOM order = visual order, unpacked menus (`>= 13px`, `gap >= 8px`, touch targets `>= 44px` / `48px` coarse), `--space-*` scale, Concentric Radii ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$), `subgrid` + `.card:has(> img)`, `clamp()`, `60ch–65ch`, `tabular-nums`, `antialiased`, and `font-synthesis: none`.

## 2. Mandatory Output Format (`0–100 pts` + `SGA`)

```markdown
# UNIFIED PROJECT, REAL-CODE, MVP & NAVIGATION AUDIT REPORT (v6.0.0)
- **Project & Path:** [Name / Path] | **Mode:** `[mvp_and_plan | deep_code_and_nav_audit | live_dom_inspection]`
- **Detected Complexity Level:** `[Level 1 | Level 2 | Level 3 | Polyglot MCP]`
- **Deterministic Scores:** **Overall Score:** `XX/100` | **SGA:** `XX.XX/100` | **TIF:** `[PASS | FAIL]`

## 1. EXECUTIVE MVP DIAGNOSIS & DOCS-VS-REAL-CODE PARITY (40 pts)
- **Primary Objective & Current State:** [Summary from real source AST]
- **Missing for MVP:** 1. **[Blocker]:** [Description] — **Why:** [Real causal impact]

| Item / Path | Real Classification (AST/Disk) | Evidence |
| :--- | :--- | :--- |
| `[File / Module]` | `[IMPLEMENTED_FUNCTIONAL | SUPERFICIAL_MOCK | DOCUMENTED_MISSING | GHOST_CODE]` | `[Line / Symbol]` |

## 2. 5 TECHNICAL PILLARS MATRIX (60 pts)
| Pillar | Verdict (`[PASS/FAIL]`) | Priority | Action & Impact |
| :--- | :--- | :--- | :--- |
| **1. Design 60-30-10 OKLCH & 3-Level Shadows** | ... | `[PRIORITY | MODERATE | EXTRA]` | ... |
| **2. 3-Layer Navigation, Islands & SGA** | ... | ... | ... |
| **3. AST Code Quality & Orphans** | ... | ... | ... |
| **4. Security & MCP/RPC Contracts** | ... | ... | ... |
| **5. Temporal Baseline & Physical Tree** | ... | ... | ... |

## 3. EXECUTABLE 3-PHASE ACTION PLAN
- [ ] **Phase 1 (Critical / MVP):** [Action + file]
- [ ] **Phase 2 (Structure, Navigation & AST):** [Action + file]
- [ ] **Phase 3 (OKLCH Polish & Extras):** [Action + file]
```
