---
name: code-quality-audit-3d-physics
description: "Audit and sanitize 3D physics engines, WebGL, Three.js, Babylon.js, shaders, collision stability, and Snorm Pass@10 scores in 3+1+1 envelope topology. Use to review 3D graphics and numerical simulation loops. Do NOT use for web CRUD, CSS styling, or unit-test AAA audits."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "1.0.0"
  updated_at: "2026-11-16"
  author: "Franklin"
  category: "3D Physics, WebGL Graphics & Numerical Simulation Auditing"
  tags: ["code-quality-audit-3d-physics", "3d", "fisica", "fisica-3d", "auditar", "sanitizar", "codigo", "computacao", "grafica", "webgl", "three", "threejs", "babylon", "babylonjs", "shaders", "colisoes", "snorm", "pass", "pass-at-k", "ast-parser", "auditoria-codigo", "testes-deterministicos"]
---

# `code-quality-audit-3d-physics` (`v1.0.0`) — 3D/WebGL & Numerical Physics Audit

## 1. Overview & Scope

Orchestrates static and dynamic auditing of 3D physics engines, WebGL/Three.js/Babylon.js renderers, shaders, and numerical simulations in **3+1+1 Envelope Topology**:
- Detects `ALLOC_IN_LOOP`, physics-render coupling, `MISSING_DELTA_TIME`, `EULER_GIMBAL_LOCK`, `UNCHECKED_NORMALIZE`, and `STRICT_FLOAT_COMPARE`.
- Runs AST parsers (`static_ast_parser.py` / `js_ts_ast_parser.js`), runtime tests (`physics_test_runner.py`, `Pass@10`), and Observer cross-validation (`state_checker_observer.py`).
- **When NOT to Use:** Do NOT use for CRUD/web repos (`system-project-auditor`), pure CSS/UI (`frontend-ui-ux-auditor`, `plan-uiux`), or general unit-test AAA audits (`test-quality-auditor`).

## 2. Inputs & Prerequisites

- **`target_path` (required):** Target `.py`/`.js`/`.ts`/`.tsx` file or 3D engine directory.
- **`step_function` (optional):** Step symbol (`step_physics_good`, `update`, `integrate`).
- **`output_format` (optional):** `markdown` (default) or `json`.

## 3. Step-by-Step Procedure

Consult [`references/3d_waves_and_penalties.md`](references/3d_waves_and_penalties.md), [`references/subskill_modules_spec.md`](references/subskill_modules_spec.md), [`references/3d_code_quality_audit_dossier.md`](references/3d_code_quality_audit_dossier.md), [`references/3d_physics_scoring_structure.md`](references/3d_physics_scoring_structure.md), and [`references/observer_agent_spec.yaml`](references/observer_agent_spec.yaml):

```powershell
uv run python skills/code-quality-audit-3d-physics/scripts/static_ast_parser.py <file.py>
node skills/code-quality-audit-3d-physics/scripts/js_ts_ast_parser.js <file.ts>
uv run python skills/code-quality-audit-3d-physics/scripts/physics_test_runner.py --target <file.py> --json
uv run python skills/code-quality-audit-3d-physics/scripts/state_checker_observer.py <file_or_dir>
```

Or run via DAG: `franklin_execute_dag(plan_path_or_json="physics", target_dir="<target_path>")`.

$$S_{\text{norm}} = 0.20 \cdot s_1 + 0.15 \cdot s_2 + 0.25 \cdot s_3 + 0.20 \cdot s_4 + 0.20 \cdot s_5$$

## 4. Gotchas & Edge Cases

- `state-checker-observer` MUST inspect real lines to filter false positives (e.g., `.normalize()` guarded by `length > EPSILON`, or constructor allocations).
- Never apply destructive refactoring without first presenting the Observer report and getting human approval.

## 5. Output Schema & Validation Criteria

Emit verdicts per [`rules/audit_criteria.md`](rules/audit_criteria.md): $S_{\text{norm}} / 100$ header with $s_1..s_5$, sub-dimension table $S_1..S_5$ ($25\%, 25\%, 20\%, 15\%, 15\%$) + 5 runtime tests (`Pass@10`), and `[ERR-XXX / PROBLEM_ID]` cards with `file:line`, fix, and metric.

## 6. User Communication Rule

All direct responses, diagnostic cards, clarifying questions, and delivery summaries addressed to the end user MUST be written in **Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.
