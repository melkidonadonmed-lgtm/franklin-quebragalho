"""
_physics_ast_rules.py
Catalog of 3D Physics AST issue templates and weighted S1..S5 scoring engine
extracted from static_ast_parser to keep modules concise (<= 600 lines).
"""

from __future__ import annotations

from typing import Any, Dict, List


def make_issue(
    issue_id: str,
    title: str,
    category: str,
    subskill: str,
    severity: str,
    penalty: int,
    filename: str,
    line: int,
    col: int,
    description: str,
    recommendation: str,
    root_cause: str = "",
    best_fix_code: str = "",
    why_best_fix: str = "",
    expected_result: str = "",
    physics_subdimension: str | None = None,
    subdimension_penalty: int = 0,
) -> Dict[str, Any]:
    """Constructs a standardized static AST issue dictionary."""
    return {
        "id": issue_id,
        "title": title,
        "category": category,
        "subskill": subskill,
        "severity": severity,
        "penalty": penalty,
        "physics_subdimension": physics_subdimension,
        "subdimension_penalty": subdimension_penalty,
        "file": filename,
        "line": line,
        "col": col,
        "description": description,
        "recommendation": recommendation,
        "root_cause": root_cause or description,
        "best_fix_code": best_fix_code,
        "why_best_fix": why_best_fix or recommendation,
        "expected_result": expected_result,
    }


def build_rigid_constructor_issue(filename: str, cls_name: str, attr_list: str, line: int, col: int) -> Dict[str, Any]:
    """Builds a RIGID_CONSTRUCTOR issue payload."""
    return make_issue(
        issue_id="RIGID_CONSTRUCTOR",
        title="Entidade Física com Construtor Rígido (Sem Injeção de Configuração)",
        category="Modularidade & Ausência de Hardcoded",
        subskill="architecture-hardcoded-auditor",
        severity="Média",
        penalty=15,
        filename=filename,
        line=line,
        col=col,
        description=(
            f"A classe '{cls_name}' define propriedades físicas rígidas ({attr_list}) "
            "no '__init__' sem permitir injeção via parâmetros ou objeto de configuração."
        ),
        recommendation="Injete os coeficientes físicos ('damping', 'gravity', 'restitution') no construtor ou receba um objeto tipado 'PhysicsConfig'.",
        root_cause=f"Atributos físicos ({attr_list}) estão chumbados no construtor de '{cls_name}', impedindo parametrização por cena ou testes de estresse.",
        best_fix_code=(
            "def __init__(self, mass: float = 1.0, damping: float = 0.99, gravity: Vector3 | None = None):\n"
            "    self.mass = mass\n"
            "    self.damping = damping\n"
            "    self.gravity = gravity if gravity is not None else Vector3(0.0, -9.81, 0.0)"
        ),
        why_best_fix="Habilita Inversão de Controle (IoC) e testes parametrizados sem alterar a classe de domínio.",
        expected_result="100% dos parâmetros físicos configuráveis por injeção no construtor.",
    )


def build_missing_damping_issue(filename: str, fn_name: str, line: int, col: int) -> Dict[str, Any]:
    """Builds a MISSING_DAMPING issue payload."""
    return make_issue(
        issue_id="MISSING_DAMPING",
        title="Ausência de Amortecimento Físico (Drag / Damping) no Integrador",
        category="Física 3D & Matemática Numérica",
        subskill="physics-3d-math-auditor",
        severity="Média",
        penalty=15,
        filename=filename,
        physics_subdimension="S3_conservation_stability",
        subdimension_penalty=30,
        line=line,
        col=col,
        description=f"O integrador físico '{fn_name}' atualiza movimento sem aplicar coeficiente de amortecimento ('damping' ou 'drag').",
        recommendation="Aplique amortecimento exponencial ou linear (ex: body.velocity *= body.damping ** dt ou F -= c_drag * v) para dissipar energia numérica residual.",
        root_cause="Integradores explícitos/semi-implícitos acumulam erro de truncamento ao longo do tempo; sem fator de amortecimento, corpos podem ganhar energia fantasma.",
        best_fix_code=(
            "damping_factor = math.pow(body.damping, dt * 60.0)\n"
            "body.velocity.x *= damping_factor\n"
            "body.velocity.y *= damping_factor\n"
            "body.velocity.z *= damping_factor"
        ),
        why_best_fix="Garante conservação/dissipação realista de energia mecânica (E_final <= E_inicial) e convergência de repouso.",
        expected_result="Energia mecânica total estritamente limitada (E_final <= E_inicial) em 100% dos passos.",
    )


def build_alloc_in_loop_issue(filename: str, fn_name: str, loop_ctx: str, line: int, col: int) -> Dict[str, Any]:
    """Builds an ALLOC_IN_LOOP issue payload."""
    return make_issue(
        issue_id="ALLOC_IN_LOOP",
        title="Alocação de Memória dentro de Laço Crítico",
        category="Sanitização Estática & Memory Cleanup",
        subskill="static-sanitization-auditor",
        severity="Crítica",
        penalty=30,
        filename=filename,
        line=line,
        col=col,
        description=f"Instanciação/alocação de objeto '{fn_name}' dentro de um laço de atualização/renderização ('{loop_ctx}').",
        recommendation="Pré-aloque o objeto no escopo do módulo/classe (Scratchpad) e mutacione seus componentes in-place para evitar acionar o Garbage Collector.",
        root_cause=f"A chamada '{fn_name}(...)' aloca um novo objeto na Heap a cada frame/iteração.",
        best_fix_code=f"_TEMP_{fn_name.upper()} = {fn_name}(0.0, 0.0, 0.0)\nbody.position.x = next_x\nbody.position.y = next_y\nbody.position.z = next_z",
        why_best_fix="Zera as alocações dinâmicas no hot-loop, mantendo a latência de frame determinística.",
        expected_result="0 B/s de alocação de objetos temporários no laço de simulação.",
    )


def build_render_coupling_issue(filename: str, owner: str, line: int, col: int) -> Dict[str, Any]:
    """Builds a PHYSICS_RENDER_COUPLING issue payload."""
    return make_issue(
        issue_id="PHYSICS_RENDER_COUPLING",
        title="Acoplamento Direto entre Motor de Física e Camada de Renderização",
        category="Modularidade & Ausência de Hardcoded",
        subskill="architecture-hardcoded-auditor",
        severity="Crítica",
        penalty=35,
        filename=filename,
        line=line,
        col=col,
        description=f"Rotina de física '{owner}' invoca diretamente primitiva gráfica/DOM.",
        recommendation="Separe o estado físico (RigidBody3D) da malha visual (Mesh/Canvas), sincronizando via barramento de estado ou adapter.",
        root_cause="Violação de separação de preocupações: o motor numérico depende de objetos de UI/WebGL, impedindo execução headless.",
        best_fix_code="physics_world.step(dt)\nmesh.position.copy(rigid_body.position)",
        why_best_fix="Permite rodar a física em frequência fixa (ex: 120Hz headless) desacoplada da taxa de renderização da tela.",
        expected_result="Desacoplamento 100% entre domínio físico e engine visual.",
    )


def build_missing_delta_time_issue(filename: str, full_name: str, line: int, col: int) -> Dict[str, Any]:
    """Builds a MISSING_DELTA_TIME issue payload."""
    return make_issue(
        issue_id="MISSING_DELTA_TIME",
        title="Atualização Física Sem Delta Time (dt)",
        category="Física 3D & Matemática Numérica",
        subskill="physics-3d-math-auditor",
        severity="Crítica",
        penalty=40,
        filename=filename,
        physics_subdimension="S1_temporal_integration",
        subdimension_penalty=100,
        line=line,
        col=col,
        description=f"A propriedade física '{full_name}' é incrementada sem multiplicação pelo fator de tempo ('dt' ou 'delta_time').",
        recommendation="Multiplique a taxa de variação pelo delta time (ex: position += velocity * dt) para assegurar independência de framerate.",
        root_cause=f"A integração de '{full_name}' assume 1 frame = 1 unidade de tempo.",
        best_fix_code=f"{full_name} += velocity * dt",
        why_best_fix="Implementa integração de Euler Semi-Implícito parametrizada por dt, garantindo invariância temporal.",
        expected_result="Diferença de posição final < 0.01m entre simulações a 60Hz e 120Hz.",
    )


def build_unchecked_normalize_issue(filename: str, fn_name: str, line: int, col: int) -> Dict[str, Any]:
    """Builds an UNCHECKED_NORMALIZE issue payload."""
    return make_issue(
        issue_id="UNCHECKED_NORMALIZE",
        title="Normalização de Vetor Sem Validação de Magnitude Zero",
        category="Física 3D & Matemática Numérica",
        subskill="physics-3d-math-auditor",
        severity="Alta",
        penalty=25,
        filename=filename,
        physics_subdimension="S2_vector_algebra_rotations",
        subdimension_penalty=40,
        line=line,
        col=col,
        description=f"Chamada de '{fn_name}()' detectada sem verificação prévia de magnitude > EPSILON.",
        recommendation="Garanta que ||v|| > EPSILON (ex: if v.length_sq() > 1e-12:) antes de normalizar para prevenir divisão por zero e contaminação por NaN/Inf.",
        root_cause="A normalização divide cada componente pela norma Euclidiana ||v||. Se o vetor for nulo (0,0,0), ocorre divisão 0/0 = NaN, contaminando toda a cena 3D.",
        best_fix_code="EPSILON_SQ = 1e-12\nif velocity.length_sq() > EPSILON_SQ:\n    direction = velocity.normalize()",
        why_best_fix="Usa length_sq() (evitando sqrt desnecessário quando nulo) e blinda o pipeline contra propagação de NaN.",
        expected_result="100% de imunidade a NaN/Inf ao processar forças ou velocidades nulas.",
    )


def build_euler_gimbal_lock_issue(filename: str, full_name: str, line: int, col: int) -> Dict[str, Any]:
    """Builds an EULER_GIMBAL_LOCK issue payload."""
    return make_issue(
        issue_id="EULER_GIMBAL_LOCK",
        title="Acúmulo Contínuo de Rotação 3D via Ângulos de Euler (Risco de Gimbal Lock)",
        category="Física 3D & Matemática Numérica",
        subskill="physics-3d-math-auditor",
        severity="Alta",
        penalty=20,
        filename=filename,
        physics_subdimension="S2_vector_algebra_rotations",
        subdimension_penalty=50,
        line=line,
        col=col,
        description=f"Incremento direto em ângulo de Euler ('{full_name}') detectado.",
        recommendation="Represente rotações acumuladas usando Quaternions (q = q * dq normalizado) ou matrizes ortonormalizadas.",
        root_cause="A composição sequencial de ângulos de Euler (X-Y-Z) sofre perda de um grau de liberdade rotacional quando o eixo intermediário atinge +-90 graus (Gimbal Lock).",
        best_fix_code="delta_q = Quaternion.from_axis_angle(angular_axis, angular_speed * dt)\nbody.orientation = (body.orientation * delta_q).normalize()",
        why_best_fix="Quaternions unitários interpolam suavemente em SO(3) sem singularidades topológicas.",
        expected_result="Eliminação total de Gimbal Lock e deriva rotacional em 360 graus.",
    )


def compute_module_scores(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcula os escores s1, s2, s3 e as 5 sub-dimensões internas S1..S5 de Física 3D."""
    penalties_by_subskill = {
        "static-sanitization-auditor": 0,
        "architecture-hardcoded-auditor": 0,
        "physics-3d-math-auditor": 0,
    }
    subdim_penalties = {
        "S1_temporal_integration": 0,
        "S2_vector_algebra_rotations": 0,
        "S3_conservation_stability": 0,
        "S4_collision_ccd": 0,
        "S5_numerical_robustness": 0,
    }

    for issue in issues:
        sub = issue.get("subskill", "")
        if sub in penalties_by_subskill:
            penalties_by_subskill[sub] += int(issue.get("penalty", 0))
        p_sub = issue.get("physics_subdimension")
        if p_sub in subdim_penalties:
            subdim_penalties[p_sub] += int(issue.get("subdimension_penalty", 0))

    s1 = max(0.0, 100.0 - penalties_by_subskill["static-sanitization-auditor"])
    s2 = max(0.0, 100.0 - penalties_by_subskill["architecture-hardcoded-auditor"])
    s3_direct = max(0.0, 100.0 - penalties_by_subskill["physics-3d-math-auditor"])

    subdim_scores = {k: max(0.0, 100.0 - v) for k, v in subdim_penalties.items()}
    subdim_weights = {
        "S1_temporal_integration": 0.25,
        "S2_vector_algebra_rotations": 0.25,
        "S3_conservation_stability": 0.20,
        "S4_collision_ccd": 0.15,
        "S5_numerical_robustness": 0.15,
    }
    s3_subdim_weighted = sum(subdim_scores[k] * subdim_weights[k] for k in subdim_weights)

    return {
        "s1_static_sanitization": round(s1, 2),
        "s2_architecture_hardcoded": round(s2, 2),
        "s3_physics_3d_math": round(s3_direct, 2),
        "s3_subdimensions_weighted": round(s3_subdim_weighted, 2),
        "physics_3d_subdimensions": {
            "S1_integracao_temporal_dt": {"score": subdim_scores["S1_temporal_integration"], "weight": 0.25},
            "S2_algebra_vetorial_rotacoes": {"score": subdim_scores["S2_vector_algebra_rotations"], "weight": 0.25},
            "S3_conservacao_estabilidade": {"score": subdim_scores["S3_conservation_stability"], "weight": 0.20},
            "S4_colisao_ccd": {"score": subdim_scores["S4_collision_ccd"], "weight": 0.15},
            "S5_robustez_numerica_float": {"score": subdim_scores["S5_numerical_robustness"], "weight": 0.15},
        },
    }
