# Deterministic Audit and Rejection Criteria (`code-quality-audit-3d-physics` v1.0.0)

Every audit executed by this skill MUST emit deterministic verdicts backed by AST inspection and dynamic runtime evidence:

- `[PASS]`: Mathematical, architectural, or memory requirement verified with zero violations.
- `[FAIL]`: Violation confirmed by the Observer citing exact `file:line` or failed runtime metric.
- `[UNVERIFIED]`: Cannot be verified due to missing target file or blocking syntax error.

---

### Rule 1: Static Sanitization & Loop Memory Leaks (Dimension 1 — Weight 20%)

- **Criterion**: Code MUST be free of heap allocations inside animation/physics loops (`update`, `render`, `step`, `animate`, `requestAnimationFrame`), duplicate functions, and dead code.
- **Deterministic Check**:
  - `new THREE.Vector3()`, `Matrix4()`, `Quaternion()`, or `np.zeros()` inside a loop -> `[FAIL: ALLOC_IN_LOOP]` (`-30 pts` in $s_1$)
  - Two functions with identical normalized AST -> `[FAIL: DUPLICATE_FUNCTION]` (`-20 pts` in $s_1$)
  - Declared function never invoked in call graph -> `[FAIL: DEAD_CODE_FUNCTION]` (`-10 pts` in $s_1$)
  - Local variable assigned and never read -> `[FAIL: UNUSED_VARIABLE]` (`-5 pts` in $s_1$)
  - Zero loop allocations (static Scratchpad reuse) and zero dead code -> `[PASS]`

### Rule 2: Physics-Render Decoupling & Hardcoding Ban (Dimension 2 — Weight 15%)

- **Criterion**: Physics/math engines MUST be 100% decoupled from DOM/Canvas/WebGL primitives and accept parameters via dependency injection.
- **Deterministic Check**:
  - Physics function/class manipulating `document`, `canvas`, `WebGLRenderingContext`, or `THREE.Mesh` -> `[FAIL: PHYSICS_RENDER_COUPLING]` (`-35 pts` in $s_2$)
  - Entity constructor hardcoding coefficients without config injection -> `[FAIL: RIGID_CONSTRUCTOR]` (`-15 pts` in $s_2$)
  - Magic numeric literals embedded directly in equations -> `[FAIL: HARDCODED_MAGIC_NUMBER]` (`-10 pts` in $s_2$)
  - Decoupled, parameterized physics domain with named constants -> `[PASS]`

### Rule 3: 3D Physics & Numerical Integrity (Dimension 3 — Weight 25%)

- **Criterion**: All kinematic integration MUST scale by `dt`, normalizations MUST check $\|\vec{v}\| > \epsilon$, continuous rotations MUST use Quaternions, float comparisons MUST use $\epsilon$ tolerance, and rigid bodies MUST include damping.
- **Deterministic Check**:
  - Position/velocity increment missing `dt` multiplier -> `[FAIL: MISSING_DELTA_TIME]` (`-40 pts` in $s_3$ / `-100 pts` in $S_1$)
  - `.normalize()` without zero-magnitude guard -> `[FAIL: UNCHECKED_NORMALIZE]` (`-25 pts` in $s_3$ / `-40 pts` in $S_2$)
  - Continuous Euler angle accumulation (`rotation.x/y/z +=`) -> `[FAIL: EULER_GIMBAL_LOCK]` (`-20 pts` in $s_3$ / `-50 pts` in $S_2$)
  - Fast rigid-body motion lacking CCD or sub-stepping -> `[FAIL: MISSING_CCD_TUNNELING]` (`-20 pts` in $s_3$ / `-40 pts` in $S_4$)
  - Strict floating-point equality (`==` / `===`) -> `[FAIL: STRICT_FLOAT_COMPARE]` (`-15 pts` in $s_3$ / `-40 pts` in $S_5$)
  - Integrator missing damping/drag -> `[FAIL: MISSING_DAMPING]` (`-15 pts` in $s_3$ / `-30 pts` in $S_3$)
  - All 5 sub-dimensions ($S_1..S_5$) mathematically compliant -> `[PASS]`

### Rule 4: Deterministic Runtime Test Battery (Dimension 4 — Weight 20%)

- **Criterion**: Engine MUST pass all 5 batteries executed by `physics_test_runner.py`.
- **Deterministic Check**:
  - Final position divergence between 60Hz and 120Hz $\ge 0.1\text{m}$ -> `[FAIL: TEST_FPS_INDEPENDENCE]`
  - Final mechanical energy $> 1.01 \times E_{\text{initial}}$ -> `[FAIL: TEST_ENERGY_CONSERVATION]`
  - `NaN` or `Inf` under zero-vector input -> `[FAIL: TEST_NAN_IMMUNITY]`
  - Fast projectile tunneling through collider ($y < -0.05\text{m}$) -> `[FAIL: TEST_COLLISION_TUNNELING]`
  - State hash divergence across $k=10$ identical runs -> `[FAIL: TEST_DETERMINISM_PASS_AT_K]`
  - 5/5 runtime batteries passed ($s_4 = 100$) -> `[PASS]`

### Rule 5: Observer Cross-Validation & $S_{\text{norm}}$ Computation (Dimension 5 — Weight 20%)

- **Criterion**: `state-checker-observer` MUST verify all Wave 1–3 alerts against real source code, eliminate false positives (e.g., `.normalize()` preceded by `if length > EPSILON`), and emit the Official Report Template.
- **Deterministic Check**:
  - Report emitted without cross-validation or without computing $S_{\text{norm}}$ -> `[FAIL: OBSERVER_BYPASS]`
  - 100% target file coverage, false positives filtered, and $S_{\text{norm}}$ consolidated -> `[PASS]`
