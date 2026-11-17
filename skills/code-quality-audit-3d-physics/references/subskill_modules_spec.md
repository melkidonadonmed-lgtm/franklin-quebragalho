# Subskill Module Specifications (3D Physics, Sanitization & Deterministic Tests)

Details the **5 Subskill Modules** composing the 3D code-quality audit topology under Progressive Disclosure and isolated context (`context: fork`).

---

## 1. Module 1: `static-sanitization-auditor` ($w_1 = 20\%$)

- **Purpose:** Static AST sweep for dead code, duplicate functions, unreachable code, and heap allocations inside animation/physics loops (`update`, `render`, `step`, `animate`, `tick`, `requestAnimationFrame`).
- **Tools:** `static_ast_parser.py` (Python), `js_ts_ast_parser.js` (JS/TS Node.js).
- **Score Formula:** $s_1 = \max\left(0, 100 - \sum \text{Penalties}\right)$

| Failure Code | Description | Severity | Penalty |
| :--- | :--- | :--- | :--- |
| `ALLOC_IN_LOOP` | Object/vector allocation inside 3D loop | Critical | **-30 pts** |
| `DUPLICATE_FUNCTION` | Function with identical normalized AST | High | **-20 pts** |
| `DEAD_CODE_FUNCTION` | Declared function never invoked | Medium | **-10 pts** |
| `UNUSED_VARIABLE` | Assigned local variable never read | Low | **-5 pts** |

---

## 2. Module 2: `architecture-hardcoded-auditor` ($w_2 = 15\%$)

- **Purpose:** Verify strict separation between physics/math domain and DOM/Canvas/WebGL rendering, and eliminate magic numeric literals.
- **Score Formula:** $s_2 = \max\left(0, 100 - \sum \text{Penalties}\right)$

| Failure Code | Description | Severity | Penalty |
| :--- | :--- | :--- | :--- |
| `PHYSICS_RENDER_COUPLING` | Physics code directly touching DOM/Canvas/WebGL | Critical | **-35 pts** |
| `RIGID_CONSTRUCTOR` | Entity lacking dependency/config injection | Medium | **-15 pts** |
| `HARDCODED_MAGIC_NUMBER` | Magic numeric literal in equations without constant | Low/Medium | **-10 pts** |

---

## 3. Module 3: `physics-3d-math-auditor` ($w_3 = 25\%$)

- **Purpose:** Audit kinematic integration (`dt`/`deltaTime`), vector algebra, Quaternions, float tolerances, and rigid-body damping.
- **Score Formula:** $s_3 = \max\left(0, 100 - \sum \text{Penalties}\right)$

| Failure Code | Description | Severity | Penalty |
| :--- | :--- | :--- | :--- |
| `MISSING_DELTA_TIME` | Position/velocity step missing `dt` scaling | Critical | **-40 pts** |
| `UNCHECKED_NORMALIZE` | `.normalize()` missing $\|\vec{v}\| > \epsilon$ guard | High | **-25 pts** |
| `EULER_GIMBAL_LOCK` | Continuous 3D rotation via Euler angles | High | **-20 pts** |
| `MISSING_CCD_TUNNELING` | Fast motion missing CCD or sub-stepping | High | **-20 pts** |
| `STRICT_FLOAT_COMPARE` | Direct float comparison via `==` or `===` | Medium | **-15 pts** |
| `MISSING_DAMPING` | Missing drag/damping coefficient | Medium | **-15 pts** |

---

## 4. Module 4: `deterministic-tests-auditor` ($w_4 = 20\%$)

- **Purpose:** Execute dynamic physics invariants via `physics_test_runner.py` in isolated execution.
- **5 Runtime Batteries:**
  1. Framerate Independence (60Hz vs. 120Hz divergence $< 0.1\text{m}$).
  2. Total Mechanical Energy Conservation ($E_{\text{final}} \le E_{\text{initial}}$).
  3. `NaN` / `Infinity` Immunity under zero/extreme forces.
  4. High-Speed Collision Tunneling Prevention (CCD / substepping).
  5. $\text{Pass}@k$ ($k=10$) state-hash reproducibility.
- **Score Formula:** $s_4 = \left(\frac{\text{Passed Tests}}{\text{Total Tests}}\right) \times 100$

---

## 5. Module 5 (Gatekeeper): `state-checker-observer` ($w_5 = 20\%$)

- **Purpose:** Cross-validate alerts from Modules 1–4 against real source AST to prune false positives, enforce 100% file coverage, and compute final $S_{\text{norm}}$:

$$S_{\text{norm}} = \sum_{j=1}^{4} w_j \cdot s_j + w_5 \cdot s_{\text{observer}}$$
