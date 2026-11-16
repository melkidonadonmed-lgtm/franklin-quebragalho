# 3D Physics & Numerical Math Scoring Structure

> **Canonical Reference — Subskill 3 (`physics-3d-math-auditor`)**
> Global Weight in Normalized Score ($w_3$): **25% to 30%**

---

## 1. Mathematical Decomposition of the 5 Sub-Dimensions ($s_{\text{Physics}}$)

The internal 3D Physics score ($s_{\text{Physics}} \in [0, 100]$) is the weighted sum of **5 technical sub-dimensions**:

$$s_{\text{Physics}} = \sum_{k=1}^{5} w_k \cdot S_k$$

Where $\sum_{k=1}^{5} w_k = 1.00$ ($100\%$):

| Technical Sub-Dimension ($S_k$) | Weight ($w_k$) | Mandatory Variables & Constructs | Formal Equations / Invariants |
| :--- | :---: | :--- | :--- |
| **1. Temporal Integration & Delta Time ($S_1$)** | **25%** | `dt` / `deltaTime`, `accumulator`, `fixedDeltaTime`, `subSteps`. | $\vec{p}_{t+dt} = \vec{p}_t + \vec{v}_t \cdot dt$ (Semi-Implicit Euler)<br>$\vec{p}_{t+dt} = 2\vec{p}_t - \vec{p}_{t-dt} + \vec{a}_t \cdot dt^2$ (Verlet) |
| **2. Vector Algebra & 3D Rotations ($S_2$)** | **25%** | Quaternions ($q = w + xi + yj + zk$), $4 \times 4$ Matrices, `dot()`, `cross()`. | $\hat{v} = \frac{\vec{v}}{\|\vec{v}\|}$ with $\|\vec{v}\| > \epsilon$<br>Anti-Gimbal-Lock guard |
| **3. Conservation Laws & Stability ($S_3$)** | **20%** | `mass` ($m > 0$), `invMass` ($1/m$), `gravity` ($\vec{g}$), `drag`/`damping`, `restitution` ($e$). | $\vec{F} = m\vec{g} - c_{\text{drag}}\vec{v}$<br>$J = \frac{-(1+e)(\vec{v}_{\text{rel}} \cdot \hat{n})}{\frac{1}{m_A} + \frac{1}{m_B}}$ |
| **4. Collision Detection & CCD ($S_4$)** | **15%** | Broadphase (AABB / Octree), `collisionNormal`, `penetrationDepth`, `CCD`. | Tunneling prevention via Sub-stepping or continuous Raycast |
| **5. Numerical & Float Robustness ($S_5$)** | **15%** | `EPSILON` ($10^{-6}$), `maxSpeed`, `math.isnan()` / `Number.isNaN()`. | $\|\vec{a} - \vec{b}\| < \epsilon$<br>Total zero-division immunity |

---

## 2. Severity Deduction Matrix

| Failure Severity | Sub-Criterion Impact ($S_k$) | Direct Impact on $s_3$ | Deterministic Action |
| :--- | :--- | :---: | :--- |
| **CRITICAL** | **-40 to -100 pts** | **-40 pts** | Rejects sub-criterion immediately and requires refactoring. |
| **HIGH** | **-25 to -50 pts** | **-20 to -25 pts** | Emits numerical instability risk warning (`NaN` / Gimbal Lock). |
| **MEDIUM** | **-15 to -40 pts** | **-15 pts** | Recommends mathematical stabilization (`EPSILON` / `damping`). |
| **LOW** | **-5 to -14 pts** | **-5 to -10 pts** | Recommends constant naming and standardization. |

---

## 3. Specific Rule Codes & Penalties

| Rule Code | Affected Sub-Dimension | Sub-Criterion Deduction ($S_k$) | Direct Score Deduction ($s_3$) | Technical Description |
| :--- | :--- | :---: | :---: | :--- |
| `MISSING_DELTA_TIME` | $S_1$ (Temporal Integration) | **-100 pts** | **-40 pts** | Position/velocity update missing `dt` scaling (FPS-dependent). |
| `EULER_GIMBAL_LOCK` | $S_2$ (Vector Algebra & Rotations) | **-50 pts** | **-20 pts** | Continuous 3D rotation accumulation via Euler angles (`rotation.x/y/z +=`). |
| `UNCHECKED_NORMALIZE` | $S_2$ / $S_5$ | **-40 pts** | **-25 pts** | Vector `.normalize()` invoked without checking $\|\vec{v}\| > \epsilon$. |
| `MISSING_CCD_TUNNELING` | $S_4$ (Collision & CCD) | **-40 pts** | **-20 pts** | Fast objects passing through thin colliders due to missing CCD / sub-stepping. |
| `STRICT_FLOAT_COMPARE` | $S_5$ (Numerical Robustness) | **-40 pts** | **-15 pts** | Strict float equality check using `==` or `===`. |
| `MISSING_DAMPING` | $S_3$ (Conservation & Stability) | **-30 pts** | **-15 pts** | Rigid-body integrator lacking damping/drag coefficient. |
