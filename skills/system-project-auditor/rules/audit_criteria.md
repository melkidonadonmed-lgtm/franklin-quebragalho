# Deterministic Audit and Rejection Criteria (`system-project-auditor` v6.0.0)

To eliminate superficial audits based solely on Markdown docs, the auditor MUST run the scanners in `scripts/` and emit strictly:

- `[PASS]`: Requirement verified in real AST source code, physical disk layout, or live DOM.
- `[FAIL]`: Violated requirement with exact file path, line number, or metric evidence.
- `[UNVERIFIED]`: Cannot be verified due to missing inputs or inactive runtime.

---

### Rule 1: Mandatory Real-Code AST and Physical Structure Check (`project_structure_and_code_auditor.py` — 20 pts)

- **Criterion**: Did the auditor run `project_structure_and_code_auditor.py`, inspect `README.md`, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `CURRENT_STATE.md`, `.gitignore`, and `.env.example`, classify the Complexity Level (1, 2, 3, or Polyglot MCP), and verify real function ASTs?
- **Checks**:
  - Audit performed by reading `.md` files alone without inspecting real source code -> `[FAIL: SUPERFICIAL_AUDIT_WITHOUT_CODE]`
  - Exposed `.env` or `.gitignore` missing protection for `.env`/`node_modules`/`.venv` -> `[FAIL: GIT_CREDENTIALS_LEAK]`
  - Physical tree, vital governance files, and real source AST verified -> `[PASS]`

### Rule 2: Docs-vs-Implementation Parity and Causal MVP Diagnosis (20 pts)

- **Criterion**: Was every module promised in `README.md`/`SPEC.md` verified against disk (`[IMPLEMENTED_FUNCTIONAL]`, `[SUPERFICIAL_MOCK]`, `[DOCUMENTED_MISSING]`, `[GHOST_CODE]`), and does every MVP blocker carry causal justification (`Why:`)?
- **Checks**:
  - Path or module claimed in `README.md`/`SPEC.md` does not exist on disk -> `[FAIL: DOCUMENTED_MISSING]`
  - MVP item lacks causal justification (`Why:`) or suffers from Scope Creep -> `[FAIL: MVP_MISSING_CAUSE_EFFECT]`
  - 1:1 parity proven and lean MVP scope confirmed -> `[PASS]`

### Rule 3: Real-Code AST Quality, Zero Placebos, and Orphan Detection (25 pts)

- **Criterion**: Do `project_structure_and_code_auditor.py` and `frontiercode_maintainability_guardrail.py` verify zero placebo functions (`pass`, `onClick={() => {}}`), zero bare `except:`, and zero orphan source files?
- **Checks**:
  - Empty stub function or placebo UI control with no real action -> `[FAIL: PLACEBO_FUNCTION_REAL_STATE]`
  - Isolated source file with no consumer or entrypoint -> `[FAIL: ORPHAN_FILE]`
  - Strictly typed, cohesive code (`<= 60` lines/function), 100% wired -> `[PASS]`

### Rule 4: `60-30-10` Rule, `OKLCH` Colors, 3-Level Shadows, and 3-Layer Navigation (`SGA` — 20 pts)

- **Criterion**: Does the UI enforce the **60-30-10 Proportion** (`60%` `--surface-canvas`, `30%` `--surface-card`/`--surface-elevated`, `10%` surgical accent), **Perceptual `OKLCH` Colors** (`oklch()`, `light-dark()`, Dark Mode $L = 0.16 \to 0.22 \to 0.27$ without `#000000`), **3-Level Multi-Layer Shadows** (Umbra + negative-spread Penumbra + Specular Rim `inset 0 1px 0 0`), **3-Layer Navigation** (`<= 3 <nav>`, unpacked menus `>= 13px`, `X activates Y`, in-place slot reuse without nested sub-tabs), and `SGA >= 85` via `deterministic_scorer.py`?
- **Checks**:
  - Violation of `60-30-10` ratio, missing `oklch()`, pure `#000000`, or neon sprawl -> `[FAIL: VIOLATION_60_30_10_OR_OKLCH]`
  - Flat single-layer shadow lacking Umbra + Penumbra + zenithal Rim Light -> `[FAIL: WASHED_SHADOW_OR_POOR_LAYERS]`
  - Compacted menus (`< 13px`), tab proliferation (`> 4` or nested sub-tabs), Dead Ends, or `row-reverse` breaking `Tab` order -> `[FAIL: NAVIGATION_OR_SGA_REJECTED]`
  - Full compliance with all 9 SSOT Axes, `60-30-10 OKLCH`, and `SGA` -> `[PASS]`

### Rule 5: MCP/RPC Security and HITL Gate for `agent-browser` / `chrome-devtools-mcp` (15 pts)

- **Criterion**: Do MCP/FastAPI/RPC contracts enforce strict schema validation (`extra="forbid"`) and did live DOM inspection (`agent-browser` `@eX` / `chrome-devtools-mcp`) honor HITL approval?
- **Checks**:
  - Browser executed on a live URL without HITL confirmation or MCP server polluting `stdout` -> `[FAIL: HITL_OR_MCP_STDIO_VIOLATION]`
  - Strict contracts and visual pipeline verified safely -> `[PASS]`
