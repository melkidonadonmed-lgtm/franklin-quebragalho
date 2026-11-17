# Stack-Adaptive Rubric, OKLCH Visual Criteria & Output Template (`system-project-auditor` v6.1.0)

Detailed Level 3 reference complementing [`pillars_5_matrix_and_handoff_2026.md`](pillars_5_matrix_and_handoff_2026.md), [`audit_rubric_and_agent_browser.md`](audit_rubric_and_agent_browser.md), and [`ui_subagent_taxonomy_6_layers.md`](ui_subagent_taxonomy_6_layers.md).

## 1. Conditional Criteria for UI Targets (`has_ui_layer == True`)

If `has_ui_layer == False`, skip this section completely, emit **`[PASS: N/A_BACKEND_ONLY]`**, and reallocate the `20` UI points to AST, Contract, and Docs-vs-Disk Parity health:

- **60-30-10 Ratio (`OKLCH` + `light-dark()`):**
  - **60% Canvas** (`--surface-canvas`, Dark Mode $L = 0.16$, zero `#000000`).
  - **30% Cards & Surfaces** (`--surface-card` $L = 0.22$, `--surface-elevated` $L = 0.27$, 4 variants + `@container`).
  - **10% Surgical Accent** (`--brand-primary` via `oklch(from ...)` / `color-mix(in oklab, ...)`), focus rings, and `6px`/`2px` status indicators.
- **3-Level Shadows:** Primitives (`--shadow-layer-sm/md/lg`) + Semantics (`--shadow-elevation-1..3`, `--shadow-inset`) combining Contact Umbra + negative-spread Penumbra (`-1px..-8px`) + Top Specular Rim (`inset 0 1px 0 0` / `--catch-light`) + Ambient Brand Glow in dark theme.
- **Navigation & Typography:** `<= 3` `<nav>` landmarks (*Global* Bottom Bar with `env(safe-area-inset-bottom)` $\leftrightarrow$ `240px` `100dvh` Sidebar at `>= 48em`; *Local*; *Breadcrumbs* `<ol role="list">` + silent `::before` + `aria-current="page"` only at `>= 3` levels), DOM order = visual order, unpacked menus (`>= 13px`, `gap >= 8px`, touch targets `>= 44px` / `48px` coarse), `--space-*` scale, Concentric Radii ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$), `subgrid` + `.card:has(> img)`, `clamp()`, `60ch–65ch`, `tabular-nums`, `antialiased`, and `font-synthesis: none`.

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
| **1. Design 60-30-10 OKLCH & 3-Level Shadows (UI Only)** | ... | `[PRIORITY | MODERATE | N/A]` | ... |
| **2. Navigation (`X activates Y` / CLI & Entrypoint Coherence)** | ... | ... | ... |
| **3. AST Code Quality, Stubs & Orphans** | ... | ... | ... |
| **4. Security, `.gitignore`/`.env` & MCP/RPC Contracts** | ... | ... | ... |
| **5. Temporal Baseline & Physical Tree** | ... | ... | ... |

## 3. DEFECT-DRIVEN REMEDIATION LIST (1:1 Evidence-Traced; 0 items if clean)
- If `verdict == [PASS]` and zero blockers exist, output: `No structural remediation required.`
- Otherwise, list concrete tasks strictly referencing `[file:line]` or scanner findings:
  - [ ] **[Priority]:** [Concrete fix + exact file:line]
```
