# Technical Dossier & Master Specification: 3D Physics Code Quality Audit (`code-quality-audit-3d-physics` v1.0.0)

Master specification for **3D Physics, Computer Graphics, and Numerical Simulation Code Quality Auditing & Sanitization**, covering verification rules, scoring mathematics, subagent topology, static/dynamic tooling, and diagnostic templates.

---

## 1. Overview & Global Audit Architecture

Designed to inspect physics engines, numerical simulations, and 3D graphics apps (Python, C++, WebGL, Three.js, JavaScript, or TypeScript) for real-time GC stalls, numerical instability, framerate dependence, non-determinism, and architectural coupling.

### Global Weighted Normalized Score ($S_{\text{norm}}$)

Final project score on a **0–100** scale:

$$S_{\text{norm}} = \sum_{j=1}^{M} w_j \cdot s_j$$

Where:
- $M = 5$ audit dimensions/modules.
- $w_j$ is the relative weight of dimension $j$, with $\sum w_j = 1.0$ ($100\%$).
- $s_j \in [0, 100]$ is the raw score obtained in dimension $j$.

### Global Dimensions & Weights

| Audit Dimension | Responsible Subskill Module | Global Weight ($w_j$) | Primary Focus |
| :--- | :--- | :---: | :--- |
| **1. Static Sanitization & Memory Cleanup** | `static-sanitization-auditor` | **20%** | Dead code, duplicate functions, memory leaks, and allocations inside 3D loops (`render`/`update`). |
| **2. Modularity & Anti-Hardcoding** | `architecture-hardcoded-auditor` | **15%** | Physics-render decoupling, named constants (no magic numbers), and config injection. |
| **3. 3D Physics & Numerical Math** | `physics-3d-math-auditor` | **25%** | Framerate independence, Delta Time (`dt`), Quaternions, float tolerances, and conservation laws. |
| **4. Testability & Deterministic Tests** | `deterministic-tests-auditor` | **20%** | Dynamic runtime simulation batteries and reproducibility rate $\text{Pass}@k$. |
| **5. Observability & State Verification** | `state-checker-observer` | **20%** | Cross-validation (false-positive pruning), file coverage, and final $S_{\text{norm}}$ consolidation. |

---

## 2. Dimension 3 Deep-Dive: 3D Physics & Numerical Math (25%)

Dimension 3 ($s_{\text{Physics}} \in [0, 100]$) decomposes internally into 5 sub-dimensions:

$$s_{\text{Physics}} = \sum_{k=1}^{5} w_k \cdot S_k$$

| Technical Sub-Dimension | Weight ($w_k$) | Required Variables | Formal Equations / Checks |
| :--- | :---: | :--- | :--- |
| **1. Temporal Integration & Delta Time** | **25%** | `dt` / `deltaTime`, `accumulator`, `fixedDeltaTime`, `subSteps`. | $\vec{p}_{t+dt} = \vec{p}_t + \vec{v}_t \cdot dt$<br>$\vec{p}_{t+dt} = 2\vec{p}_t - \vec{p}_{t-dt} + \vec{a}_t \cdot dt^2$ |
| **2. Vector Algebra & 3D Rotations** | **25%** | Quaternions ($q = w + xi + yj + zk$), $4 \times 4$ Matrices, `dot()`, `cross()`. | $\hat{v} = \frac{\vec{v}}{\|\vec{v}\|}$<br>Gimbal Lock prevention |
| **3. Conservation Laws & Stability** | **20%** | `mass` ($m > 0$), `invMass` ($1/m$), `gravity` ($\vec{g}$), `drag`, `restitution` ($e$). | $\vec{F} = m\vec{g} - c_{\text{drag}}\vec{v}$<br>$J = \frac{-(1+e)(\vec{v}_{\text{rel}} \cdot \hat{n})}{\frac{1}{m_A} + \frac{1}{m_B}}$ |
| **4. Collision Detection & CCD** | **15%** | Broadphase (AABB / Octree), `collisionNormal`, `penetrationDepth`, `CCD`. | High-speed tunneling prevention |
| **5. Numerical & Float Robustness** | **15%** | `EPSILON` ($10^{-6}$), `maxSpeed`, `Number.isNaN()`. | $\|\vec{a} - \vec{b}\| < \epsilon$<br>Zero-division immunity |

### Primary Severity Deductions (3D Physics)

- **Position update without Delta Time (`MISSING_DELTA_TIME`):** **-100 pts** in sub-criterion (Critical).
- **Continuous Euler rotation accumulation (`EULER_GIMBAL_LOCK`):** **-50 pts**.
- **Unchecked vector normalization (`UNCHECKED_NORMALIZE`):** **-40 pts**.
- **Strict float equality (`STRICT_FLOAT_COMPARE`):** **-40 pts**.
- **Missing Continuous Collision Detection (`MISSING_CCD_TUNNELING`):** **-40 pts**.
- **Missing drag/damping coefficient (`MISSING_DAMPING`):** **-30 pts**.

---

## 3. Subagent & State Observer Topology

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                     AUDIT ORCHESTRATOR SUBAGENT                           │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│  SUBAGENT 1:      │       │  SUBAGENT 2:      │       │  SUBAGENT 3:      │
│  Static AST &     │       │  Architecture &   │       │  3D Physics &     │
│  Sanitization     │       │  Anti-Hardcoding  │       │  Numerical Math   │
└───────────────────┘       └───────────────────┘       └───────────────────┘
          │                           │                           │
          └───────────────────────────┼───────────────────────────┘
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                   SUBAGENT 4: DETERMINISTIC RUNTIME TESTS                 │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                   STATE CHECKER & AUDIT OBSERVER                          │
│  • Cross-validates findings • Eliminates false positives                  │
│  • Enforces 100% file coverage • Computes final normalized score S_norm   │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Bundled Deterministic Tooling (`scripts/`)

1. **Python AST Parser (`static_ast_parser.py`):** Inspects `.py` syntax trees safely without execution for loop allocations, missing `dt`, magic literals, strict float equality, and dead/duplicate functions.
2. **JS/TS AST Parser (`js_ts_ast_parser.js`):** Node.js analyzer targeting WebGL, Three.js, and Babylon.js for `THREE.Vector3`/`Matrix4` loop instantiations inside `requestAnimationFrame`, missing `dt`, and unguarded normalizations.
3. **3D Deterministic Test Runner (`physics_test_runner.py`):** Runs live rigid-body simulations validating FPS independence (60Hz vs. 120Hz), mechanical energy conservation, `NaN` immunity, tunneling prevention, and $\text{Pass}@10$ determinism.

---

## 5. Diagnostic Card & Final Report Templates

```markdown
### [ERR-001] — 3D Vector Allocation Inside Animation Loop
* **Affected Dimension:** Static Sanitization & Memory Cleanup
* **Severity:** Critical
* **Location:** `src/render/loop.ts:42`

#### 1. Root Cause Analysis
`new THREE.Vector3()` is instantiated inside `animate()`, creating hundreds of transient heap allocations per second and causing GC stutter.

#### 2. Recommended Fix & Technical Rationale
```typescript
const TEMP_VECTOR = new THREE.Vector3();

function animate(dt: number) {
  TEMP_VECTOR.copy(entity.position).addScaledVector(entity.velocity, dt);
  mesh.position.copy(TEMP_VECTOR);
}
```
* **Rationale:** Eliminates per-frame heap allocations (`0 B/s`), removing GC pauses.

#### 3. Expected Outcome
* **Allocation Rate:** Reduced from `15 MB/s` to `0 B/s` during animation.
```

```markdown
# Final 3D Code Quality Audit Report

**Final Normalized Score ($S_{\text{norm}}$):** **84.5 / 100** (Approved with Caveats)

### Subskill Module Breakdown:
- **Static Sanitization:** 90.0 / 100 (Weight: 20%) — 1 temporary loop allocation detected.
- **Architecture & Anti-Hardcoding:** 85.0 / 100 (Weight: 15%) — 2 magic literals in friction equations.
- **3D Physics & Math:** 73.5 / 100 (Weight: 25%) — Missing Fixed Timestep and unsafe normalization.
- **Deterministic Tests:** 100.0 / 100 (Weight: 20%) — 5/5 runtime tests passed.
- **Observability & Verification:** 80.0 / 100 (Weight: 20%) — Cross-validation complete with zero hallucinations.
```
