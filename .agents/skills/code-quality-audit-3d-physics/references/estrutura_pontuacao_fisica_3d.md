# Estrutura da Pontuação da Dimensão de Física 3D & Matemática Numérica

> **Referência Canônica — Subskill 3 (`physics-3d-math-auditor`)**
> Peso Global no Escore Normalizado ($w_3$): **25% a 30%**

---

## 1. Decomposição Matemática das 5 Sub-dimensões ($s_{\text{Física}}$)

A pontuação interna da dimensão de Física 3D ($s_{\text{Física}} \in [0, 100]$) é calculada pela soma ponderada de **5 sub-dimensões técnicas**:

$$s_{\text{Física}} = \sum_{k=1}^{5} w_k \cdot S_k$$

Onde $\sum_{k=1}^{5} w_k = 1.00$ ($100\%$):

| Sub-dimensão Técnica ($S_k$) | Peso Interno ($w_k$) | Requisitos e Variáveis Obrigatórias | Equações Formais / Invariantes |
| :--- | :---: | :--- | :--- |
| **1. Integração Temporal & Delta Time ($S_1$)** | **25%** | `dt` / `deltaTime`, `accumulator`, `fixedDeltaTime`, `subSteps`. | $\vec{p}_{t+dt} = \vec{p}_t + \vec{v}_t \cdot dt$ (Euler Semi-Implícito)<br>$\vec{p}_{t+dt} = 2\vec{p}_t - \vec{p}_{t-dt} + \vec{a}_t \cdot dt^2$ (Verlet) |
| **2. Álgebra Vetorial & Rotações 3D ($S_2$)** | **25%** | Quaternions ($q = w + xi + yj + zk$), Matrizes $4 \times 4$, `dot()`, `cross()`. | $\hat{v} = \frac{\vec{v}}{\|\vec{v}\|}$ com $\|\vec{v}\| > \epsilon$<br>Vedação contra *Gimbal Lock* |
| **3. Leis de Conservação & Estabilidade ($S_3$)** | **20%** | `mass` ($m > 0$), `invMass` ($1/m$), `gravity` ($\vec{g}$), `drag`/`damping`, `restitution` ($e$). | $\vec{F} = m\vec{g} - c_{\text{drag}}\vec{v}$<br>$J = \frac{-(1+e)(\vec{v}_{\text{rel}} \cdot \hat{n})}{\frac{1}{m_A} + \frac{1}{m_B}}$ |
| **4. Detecção de Colisão & CCD ($S_4$)** | **15%** | Broadphase (AABB / Octree), `collisionNormal`, `penetrationDepth`, `CCD`. | Prevenção de *Tunneling* em corpos rápidos via Sub-stepping ou Raycast contínuo |
| **5. Robustez Numérica & Float ($S_5$)** | **15%** | `EPSILON` ($10^{-6}$), `maxSpeed`, `math.isnan()` / `Number.isNaN()`. | $\|\vec{a} - \vec{b}\| < \epsilon$<br>Imunidade total a divisão por zero |

---

## 2. Matriz de Deduções de Física 3D por Severidade

| Nível de Falha | Impacto no Subcritério ($S_k$) | Impacto Direto em $s_3$ | Ação Determinística do Subagente |
| :--- | :--- | :---: | :--- |
| **CRÍTICO** | Dedução de **-40 a -100 pontos** | **-40 pontos** | Reprova o subcritério imediatamente e exige refatoração obrigatória. |
| **ALTO** | Dedução de **-25 a -50 pontos** | **-20 a -25 pontos** | Alerta de risco de instabilidade numérica (`NaN` ou *Gimbal Lock*). |
| **MÉDIO** | Dedução de **-15 a -40 pontos** | **-15 pontos** | Recomendação de estabilização matemática (`EPSILON` / `damping`). |
| **BAIXO** | Dedução de **-5 a -14 pontos** | **-5 a -10 pontos** | Sugestão de padronização e documentação de constantes. |

---

## 3. Tabela de Códigos de Falha e Penalidades Específicas

| Código da Regra | Sub-dimensão Afetada | Dedução no Subcritério ($S_k$) | Dedução Direta na Nota ($s_3$) | Descrição Técnica |
| :--- | :--- | :---: | :---: | :--- |
| `MISSING_DELTA_TIME` | $S_1$ (Integração Temporal) | **-100 pts** | **-40 pts** | Atualização de posição/velocidade sem multiplicar por `dt` (dependência de FPS). |
| `EULER_GIMBAL_LOCK` | $S_2$ (Álgebra Vetorial & Rotações) | **-50 pts** | **-20 pts** | Uso de Ângulos de Euler (`rotation.x/y/z +=`) para acúmulo contínuo de rotação 3D. |
| `UNCHECKED_NORMALIZE` | $S_2$ (Álgebra Vetorial) / $S_5$ | **-40 pts** | **-25 pts** | Normalização de vetor (`.normalize()`) sem checar magnitude zero ($\|\vec{v}\| > \epsilon$). |
| `MISSING_CCD_TUNNELING` | $S_4$ (Colisão & CCD) | **-40 pts** | **-20 pts** | Objetos velozes atravessando colisores finos por ausência de CCD / Sub-stepping. |
| `STRICT_FLOAT_COMPARE` | $S_5$ (Robustez Numérica) | **-40 pts** | **-15 pts** | Comparação direta de ponto flutuante com igualdade estrita (`==` ou `===`). |
| `MISSING_DAMPING` | $S_3$ (Conservação & Estabilidade) | **-30 pts** | **-15 pts** | Ausência de coeficiente de amortecimento (*drag/damping*) em corpos rígidos. |
