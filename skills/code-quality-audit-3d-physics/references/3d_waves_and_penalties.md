# Waves, Penalties & Diagnostic Cards — `code-quality-audit-3d-physics`

Operational 3-wave reference consumed by [`SKILL.md`](../SKILL.md), complementing [`subskill_modules_spec.md`](subskill_modules_spec.md), [`3d_code_quality_audit_dossier.md`](3d_code_quality_audit_dossier.md), [`3d_physics_scoring_structure.md`](3d_physics_scoring_structure.md), and [`observer_agent_spec.yaml`](observer_agent_spec.yaml).

## 3+1+1 Envelope Topology

```text
┌───────────────────────────────────────────────────────────────────────────┐
│        ORCHESTRATOR: code-quality-audit-3d-physics (3+1+1 Topology)       │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│ WAVE 1 - MODULE 1 │       │ WAVE 1 - MODULE 2 │       │ WAVE 1 - MODULE 3 │
│ Sanitization & AST│       │ Architecture &    │       │ 3D Physics & Math │
│ (w1 = 20% | s1)   │       │ Anti-Hardcode 15% │       │ (w3 = 25% | s3)   │
└─────────┬─────────┘       └─────────┬─────────┘       └─────────┬─────────┘
          └───────────────────────────┼───────────────────────────┘
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ WAVE 2 - MODULE 4: deterministic-tests-auditor (w4 = 20% | s4)            │
│ • FPS Independence (60Hz vs 120Hz) • Energy Conservation • Anti-NaN       │
│ • Tunneling Prevention (CCD)       • Pass@k Reproducibility (k=10)        │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ WAVE 3 - MODULE 5 (GATEKEEPER): state-checker-observer (w5 = 20% | s5)    │
│ • Source Cross-Validation (False-Positive Filtering)                      │
│ • Compute S1..S5 & Global Score Snorm • Emit Final Report                 │
└───────────────────────────────────────────────────────────────────────────┘
```

## Module Penalties & Runtime Batteries

- **Wave 1 — AST:**
  - **Module 1 (`static-sanitization-auditor`, $w_1 = 20\%$):** `ALLOC_IN_LOOP` ($-30$), `DUPLICATE_FUNCTION` ($-20$), `DEAD_CODE_FUNCTION` ($-10$), `UNUSED_VARIABLE` ($-5$).
  - **Module 2 (`architecture-hardcoded-auditor`, $w_2 = 15\%$):** `PHYSICS_RENDER_COUPLING` ($-35$), `RIGID_CONSTRUCTOR` ($-15$), `HARDCODED_MAGIC_NUMBER` ($-10$).
  - **Module 3 (`physics-3d-math-auditor`, $w_3 = 25\%$ & $S_1..S_5$):** `MISSING_DELTA_TIME` ($-40$ in $s_3$ / $-100$ in $S_1$), `UNCHECKED_NORMALIZE` ($-25$ / $-40$ $S_2$), `EULER_GIMBAL_LOCK` ($-20$ / $-50$ $S_2$), `STRICT_FLOAT_COMPARE` ($-15$ / $-40$ $S_5$), `MISSING_DAMPING` ($-15$ / $-30$ $S_3$).
- **Wave 2 — 5 Runtime Batteries (`physics_test_runner.py`, $s_4 = \frac{\text{Pass}}{5} \times 100$):** `TEST_FPS_INDEPENDENCE` (`< 0.1m` 60Hz vs. 120Hz), `TEST_ENERGY_CONSERVATION` ($E_{\text{final}} \le E_{\text{initial}}$), `TEST_NAN_IMMUNITY` (zero-vector safe), `TEST_COLLISION_TUNNELING` (`-100 m/s` retained via CCD/substepping), `TEST_DETERMINISM_PASS_AT_K` ($Pass@10$ 100%).
- **Diagnostic Cards (`[ERR-XXX / PROBLEM_ID]`):** Dimension, Severity, `file:line`, Observer Verdict + `1. Root Cause`, `2. Recommended Fix with Code`, `3. Expected Metric`.
