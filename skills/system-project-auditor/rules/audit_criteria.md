# Deterministic Audit and Rejection Criteria (`system-project-auditor` v6.1.0)

To eliminate superficial audits based solely on Markdown docs, the auditor MUST run the scanners in `scripts/` and emit strictly:

- `[PASS]`: Requirement verified in real AST source code, physical disk layout, or live DOM.
- `[PASS: N/A_BACKEND_ONLY]`: Target repository has no UI layer (`has_ui_layer == False`); visual/DOM checks skipped and their `20` points reallocated to AST, contract, and parity health.
- `[FAIL]`: Violated requirement with exact file path, line number, or metric evidence.
- `[UNVERIFIED]`: Cannot be verified due to missing inputs or inactive runtime.

---

### Rule 1: Mandatory Real-Code AST and Physical Structure Check (`project_structure_and_code_auditor.py` — 20 pts)

- **Criterion**: Did the auditor run `project_structure_and_code_auditor.py`, inspect `README.md`, `AGENTS.md`, `.context/spec.md`, `.context/context.md` (advisory on `1–4` file standalone micro-repos), `.gitignore`, and `.env.example` (if env vars exist), classify the Complexity Level, and verify real source ASTs?
- **Checks**:
  - Audit performed by reading `.md` files alone without inspecting real source code -> `[FAIL: SUPERFICIAL_AUDIT_WITHOUT_CODE]`
  - Exposed `.env` or `.gitignore` missing protection for `.env`/dependencies -> `[FAIL: GIT_CREDENTIALS_LEAK]`
  - Physical tree, vital governance files (or micro-repo advisory), and real source AST verified -> `[PASS]`

### Rule 2: Docs-vs-Implementation Parity and Causal MVP Diagnosis (20 pts)

- **Criterion**: Was every real file path promised in `README.md`/`.context/spec.md` (excluding `Non-Goals`/`Roadmap` and code fences) verified against disk (`[IMPLEMENTED_FUNCTIONAL]`, `[SUPERFICIAL_MOCK]`, `[DOCUMENTED_MISSING]`, `[GHOST_CODE]`), and does every MVP blocker carry causal justification (`Why:`)?
- **Checks**:
  - Real path or module claimed in `README.md`/`.context/spec.md` does not exist on disk -> `[FAIL: DOCUMENTED_MISSING]`
  - MVP item lacks causal justification (`Why:`) or suffers from Scope Creep -> `[FAIL: MVP_MISSING_CAUSE_EFFECT]`
  - 1:1 parity proven and lean MVP scope confirmed -> `[PASS]`

### Rule 3: Real-Code AST Quality, Zero Placebos, and Orphan Detection (25 pts; +10 pts when headless)

- **Criterion**: Do `project_structure_and_code_auditor.py` and `deterministic_scorer.py` (plus `frontiercode_maintainability_guardrail.py <file.py>` when Python exists) verify zero placebo functions (`pass`, `...`, `onClick={() => {}}`), zero bare `except:`, and zero true orphan files across Python, TS/JS, and Go?
- **Checks**:
  - Empty stub function or placebo UI control with no real action -> `[FAIL: PLACEBO_FUNCTION_REAL_STATE]`
  - Isolated source file with no consumer or framework entrypoint -> `[FAIL: ORPHAN_FILE]`
  - Strictly typed, cohesive code (`<= 60` lines/function), 100% wired -> `[PASS]`

### Rule 4: Conditional `60-30-10 OKLCH`, Shadows, and 3-Layer Navigation (`SGA` — 20 pts UI / Reallocated when Headless)

- **Criterion**: When `has_ui_layer == True`, does the UI enforce **60-30-10** (`60%` `--surface-canvas`, `30%` `--surface-card`/`--surface-elevated`, `10%` surgical accent), **Perceptual `OKLCH`** (`oklch()`, `light-dark()`, Dark Mode $L = 0.16 \to 0.22 \to 0.27$ without `#000000`), **3-Level Multi-Layer Shadows**, **3-Layer Navigation**, and `SGA >= 85`? When `has_ui_layer == False`, mark `[PASS: N/A_BACKEND_ONLY]` and evaluate backend `SGA >= 85` via AST cohesion and zero stubs (`+10` pts Rule 3 / `+10` pts Rule 5).
- **Checks**:
  - Target has no UI layer (`has_ui_layer == False`) -> `[PASS: N/A_BACKEND_ONLY]`
  - Violation of `60-30-10`, missing `oklch()`, pure `#000000`, or flat single-layer shadow -> `[FAIL: VIOLATION_60_30_10_OR_SHADOWS]`
  - Compacted menus (`< 13px`), tab sprawl (`> 4` or nested sub-tabs), Dead Ends, or `row-reverse` breaking `Tab` order -> `[FAIL: NAVIGATION_OR_SGA_REJECTED]`
  - Full UI compliance with all 9 SSOT Axes and `SGA >= 85` -> `[PASS]`

### Rule 5: MCP/RPC Security & Conditional HITL Gate for Live Browser (15 pts; +10 pts when headless)

- **Criterion**: Do MCP/FastAPI/RPC contracts enforce strict schema validation (`extra="forbid"` / `.strict()` / Go `DisallowUnknownFields()`), and—when `has_ui_layer == True` and live DOM inspection (`agent-browser` `@eX` / `chrome-devtools-mcp`) runs—was HITL approval obtained?
- **Checks**:
  - Target is headless (`has_ui_layer == False`) and strict contracts/CLI checks pass -> `[PASS: N/A_BACKEND_ONLY]`
  - Browser executed on a live URL without HITL confirmation or MCP server polluting `stdout` -> `[FAIL: HITL_OR_MCP_STDIO_VIOLATION]`
  - Strict contracts and visual pipeline verified safely -> `[PASS]`
