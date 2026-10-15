# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`code-quality-audit-3d-physics`)

Toda auditoria executada por esta skill deve emitir marcadores determinísticos baseados em evidências reais de AST e execução dinâmica:
- `[PASS]`: Requisito matemático, arquitetural ou de memória comprovado sem violações.
- `[FAIL]`: Violação confirmada pelo Observador com apontamento exato de `arquivo:linha` ou métrica de runtime reprovada.
- `[UNVERIFIED]`: Impossibilidade de verificação por ausência de arquivo alvo ou erro de sintaxe bloqueante.

---

### Regra 1: Sanitização Estática e Vazamento de Memória em Laço 3D (Dimensão 1 — Peso 20%)
- **Critério**: O código deve ser livre de instanciações na Heap dentro de laços de animação/física (`update`, `render`, `step`, `animate`, `requestAnimationFrame`), funções duplicadas e código morto.
- **Verificação Determinística**:
  - Presença de `new THREE.Vector3()`, `Matrix4()`, `Quaternion()` ou `np.zeros()` dentro de laço -> `[FAIL: ALLOC_IN_LOOP]` (-30 pts em $s_1$)
  - Duas funções com AST normalizada idêntica -> `[FAIL: DUPLICATE_FUNCTION]` (-20 pts em $s_1$)
  - Função declarada e nunca invocada no grafo de chamadas -> `[FAIL: DEAD_CODE_FUNCTION]` (-10 pts em $s_1$)
  - Variável local atribuída e nunca lida -> `[FAIL: UNUSED_VARIABLE]` (-5 pts em $s_1$)
  - Laço 3D 100% livre de alocações temporárias (uso de Scratchpad estático) e sem código morto -> `[PASS]`

### Regra 2: Modularidade Física-Visual e Ausência de Hardcoded (Dimensão 2 — Peso 15%)
- **Critério**: O motor de física/matemática deve ser 100% desacoplado de primitivas de DOM/Canvas/WebGL e receber parâmetros por injeção de configuração.
- **Verificação Determinística**:
  - Classe/função de física manipulando `document`, `canvas`, `WebGLRenderingContext` ou `THREE.Mesh` -> `[FAIL: PHYSICS_RENDER_COUPLING]` (-35 pts em $s_2$)
  - Construtor de entidade física com coeficientes chumbados sem injeção de parâmetros -> `[FAIL: RIGID_CONSTRUCTOR]` (-15 pts em $s_2$)
  - Constantes numéricas literais soltas em equações operacionais -> `[FAIL: HARDCODED_MAGIC_NUMBER]` (-10 pts em $s_2$)
  - Domínio físico isolado, parametrizado e constantes nomeadas -> `[PASS]`

### Regra 3: Integridade Matemática e Física 3D (Dimensão 3 — Peso 25%)
- **Critério**: Toda integração cinemática deve ser escalada por `dt`, normalizações devem validar $\|\vec{v}\| > \epsilon$, rotações contínuas devem usar Quaternions, comparações de float devem usar tolerância $\epsilon$ e corpos rígidos devem ter amortecimento (`damping`).
- **Verificação Determinística**:
  - Incremento de posição/velocidade sem multiplicar por `dt` -> `[FAIL: MISSING_DELTA_TIME]` (-40 pts em $s_3$ / -100 pts em $S_1$)
  - Chamada a `.normalize()` sem guarda de magnitude zero -> `[FAIL: UNCHECKED_NORMALIZE]` (-25 pts em $s_3$ / -40 pts em $S_2$)
  - Acúmulo contínuo de ângulos de Euler (`rotation.x/y/z +=`) -> `[FAIL: EULER_GIMBAL_LOCK]` (-20 pts em $s_3$ / -50 pts em $S_2$)
  - Igualdade estrita (`==` / `===`) em ponto flutuante -> `[FAIL: STRICT_FLOAT_COMPARE]` (-15 pts em $s_3$ / -40 pts em $S_5$)
  - Integrador sem amortecimento (`damping` / `drag`) -> `[FAIL: MISSING_DAMPING]` (-15 pts em $s_3$ / -30 pts em $S_3$)
  - Cinco sub-dimensões ($S_1..S_5$) em conformidade física e numérica -> `[PASS]`

### Regra 4: Bateria de Testes Determinísticos em Runtime (Dimensão 4 — Peso 20%)
- **Critério**: O motor deve aprovar as 5 baterias executadas por `physics_test_runner.py`.
- **Verificação Determinística**:
  - Divergência de posição final entre 60Hz e 120Hz $\ge 0.1\text{m}$ -> `[FAIL: TEST_FPS_INDEPENDENCE]`
  - Energia mecânica final $> 1.01 \times E_{\text{inicial}}$ -> `[FAIL: TEST_ENERGY_CONSERVATION]`
  - Surgimento de `NaN` ou `Inf` sob vetor nulo -> `[FAIL: TEST_NAN_IMMUNITY]`
  - Projétil rápido atravessando o colisor ($y < -0.05\text{m}$) -> `[FAIL: TEST_COLLISION_TUNNELING]`
  - Divergência de estado entre $k=10$ execuções idênticas -> `[FAIL: TEST_DETERMINISM_PASS_AT_K]`
  - 5/5 baterias aprovadas ($s_4 = 100$) -> `[PASS]`

### Regra 5: Validação Cruzada do Observador e Cálculo de $S_{\text{norm}}$ (Dimensão 5 — Peso 20%)
- **Critério**: O `state-checker-observer` deve reinspecionar no código-fonte todos os alertas das Ondas 1–3, descartar falsos positivos (ex: `.normalize()` precedido por `if length > EPSILON`) e emitir o relatório no Template Oficial.
- **Verificação Determinística**:
  - Relatório emitido sem validação cruzada ou sem cálculo de $S_{\text{norm}}$ -> `[FAIL: OBSERVER_BYPASS]`
  - Cobertura de 100% dos arquivos auditados, falsos positivos filtrados e nota $S_{\text{norm}}$ consolidada -> `[PASS]`
