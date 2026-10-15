"""
static_ast_parser.py
Analisador Estático AST para Python focado em Motores de Física 3D, Computação Gráfica
e Simulações Numéricas.

Cobre os Módulos 1, 2 e 3 da Especificação Mestra:
- Módulo 1 (static-sanitization-auditor, w1 = 20%):
    ALLOC_IN_LOOP (-30), DUPLICATE_FUNCTION (-20), DEAD_CODE_FUNCTION (-10), UNUSED_VARIABLE (-5)
- Módulo 2 (architecture-hardcoded-auditor, w2 = 15%):
    PHYSICS_RENDER_COUPLING (-35), RIGID_CONSTRUCTOR (-15), HARDCODED_MAGIC_NUMBER (-10)
- Módulo 3 (physics-3d-math-auditor, w3 = 25% + 5 Sub-dimensões S1..S5):
    MISSING_DELTA_TIME (-40 / S1 -100), UNCHECKED_NORMALIZE (-25 / S2 -40),
    EULER_GIMBAL_LOCK (-20 / S2 -50), STRICT_FLOAT_COMPARE (-15 / S5 -40),
    MISSING_DAMPING (-15 / S3 -30), MISSING_CCD_TUNNELING (-20 / S4 -40)
"""

from __future__ import annotations

import argparse
import ast
import copy
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


class LocalIdentifierNormalizer(ast.NodeTransformer):
    """Normaliza identificadores de variáveis locais e argumentos para detecção estrutural
    de funções duplicadas (mesmo quando variáveis locais foram renomeadas)."""

    def __init__(self) -> None:
        super().__init__()
        self.var_map: Dict[str, str] = {}
        self.counter = 0

    def _get_norm_name(self, name: str) -> str:
        if name in ("self", "cls", "True", "False", "None"):
            return name
        if name not in self.var_map:
            self.var_map[name] = f"_v{self.counter}"
            self.counter += 1
        return self.var_map[name]

    def visit_arg(self, node: ast.arg) -> ast.arg:
        new_node = copy.copy(node)
        new_node.arg = self._get_norm_name(node.arg)
        new_node.annotation = None
        return new_node

    def visit_Name(self, node: ast.Name) -> ast.Name:
        new_node = copy.copy(node)
        if isinstance(node.ctx, (ast.Store, ast.Load, ast.Del)):
            if node.id in self.var_map or isinstance(node.ctx, ast.Store):
                new_node.id = self._get_norm_name(node.id)
        return new_node


def _normalize_function_ast(node: ast.FunctionDef | ast.AsyncFunctionDef) -> Optional[str]:
    """Retorna o dump AST normalizado do corpo da função, ignorando docstrings e funções triviais."""
    body = list(node.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]

    # Ignorar funções triviais (pass, ellipsis ou 1 linha simples de getter/setter)
    if len(body) <= 1:
        if not body or isinstance(body[0], (ast.Pass, ast.Return, ast.Raise)):
            return None

    normalizer = LocalIdentifierNormalizer()
    for arg in node.args.args:
        normalizer.visit_arg(arg)

    norm_stmts = [normalizer.visit(copy.deepcopy(stmt)) for stmt in body]
    return ast.dump(ast.Module(body=norm_stmts, type_ignores=[]), include_attributes=False)


class PhysicsCodeASTVisitor(ast.NodeVisitor):
    """
    AST Visitor para análise estática determinística dos Módulos 1, 2 e 3.
    """

    LOOP_FN_KEYWORDS = ("update", "render", "step", "animate", "loop", "tick", "integrate", "simulate")
    ALLOC_INDICATORS = (
        "Vector3",
        "Vector2",
        "Vector4",
        "Matrix4",
        "Matrix3",
        "Quaternion",
        "Euler",
        "array",
        "zeros",
        "ones",
        "empty",
        "linspace",
    )
    RENDER_COUPLED_SYMBOLS = (
        "canvas",
        "webgl",
        "renderer",
        "three",
        "mesh",
        "document",
        "window",
        "tkinter",
        "pygame",
        "glclear",
        "gldraw",
    )
    PHYSICS_CLASS_KEYWORDS = ("rigidbody", "particle", "body", "physics", "collider", "simulator", "solver")
    GUARDRAIL_TOKENS = ("length", "length_sq", "mag", "magnitude", "norm", "epsilon", "eps", "1e-")

    def __init__(self, filename: str = "script.py", source_lines: Optional[List[str]] = None) -> None:
        self.filename = filename
        self.source_lines = source_lines or []
        self.issues: List[Dict[str, Any]] = []
        self.defined_functions: Dict[str, str] = {}  # fn_name -> normalized ast dump
        self.function_meta: Dict[str, Dict[str, Any]] = {}  # fn_name -> {line, col, is_method, has_decorators}
        self.called_functions: Set[str] = set()
        self.exported_symbols: Set[str] = set()
        self.in_loop = False
        self.loop_depth = 0
        self.current_function: Optional[str] = None
        self.current_class: Optional[str] = None
        self.in_default_args = False
        self.guardrail_depth = 0

    def add_issue(
        self,
        issue_id: str,
        title: str,
        category: str,
        subskill: str,
        severity: str,
        penalty: int,
        line: int,
        col: int,
        description: str,
        recommendation: str,
        root_cause: str = "",
        best_fix_code: str = "",
        why_best_fix: str = "",
        expected_result: str = "",
        physics_subdimension: Optional[str] = None,
        subdimension_penalty: int = 0,
    ) -> None:
        self.issues.append(
            {
                "id": issue_id,
                "title": title,
                "category": category,
                "subskill": subskill,
                "severity": severity,
                "penalty": penalty,
                "physics_subdimension": physics_subdimension,
                "subdimension_penalty": subdimension_penalty,
                "file": self.filename,
                "line": line,
                "col": col,
                "description": description,
                "recommendation": recommendation,
                "root_cause": root_cause or description,
                "best_fix_code": best_fix_code,
                "why_best_fix": why_best_fix or recommendation,
                "expected_result": expected_result,
            }
        )

    def _has_nearby_guardrail(self, lineno: int) -> bool:
        """Verifica se há guardrail numérico (ex: mag > EPSILON) no bloco condicional ativo ou nas 3 linhas anteriores."""
        if self.guardrail_depth > 0:
            return True
        if not self.source_lines:
            return False
        start_idx = max(0, lineno - 4)
        end_idx = min(len(self.source_lines), lineno)
        window_text = " ".join(self.source_lines[start_idx:end_idx]).lower()
        return any(tok in window_text for tok in self.GUARDRAIL_TOKENS)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        prev_class = self.current_class
        self.current_class = node.name

        # Check Módulo 2: RIGID_CONSTRUCTOR e Acoplamento Física-Renderização
        is_physics_cls = any(kw in node.name.lower() for kw in self.PHYSICS_CLASS_KEYWORDS)
        if is_physics_cls:
            self._check_rigid_constructor(node)

        self.generic_visit(node)
        self.current_class = prev_class

    def _check_rigid_constructor(self, class_node: ast.ClassDef) -> None:
        for item in class_node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                param_names = {a.arg.lower() for a in item.args.args if a.arg != "self"}
                has_varargs_or_kw = item.args.kwarg is not None or "config" in param_names or "params" in param_names
                hardcoded_attrs: List[Tuple[str, int, int, Any]] = []

                for stmt in item.body:
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if (
                                isinstance(target, ast.Attribute)
                                and isinstance(target.value, ast.Name)
                                and target.value.id == "self"
                            ):
                                attr_name = target.attr.lower()
                                if attr_name in ("damping", "drag", "gravity", "restitution", "friction", "timestep"):
                                    if attr_name not in param_names and not has_varargs_or_kw:
                                        # Verifica se o valor atribuído não usa nenhum parâmetro do __init__
                                        rhs_names = {
                                            n.id.lower() for n in ast.walk(stmt.value) if isinstance(n, ast.Name)
                                        }
                                        if not (rhs_names & param_names):
                                            hardcoded_attrs.append((target.attr, stmt.lineno, stmt.col_offset, ast.dump(stmt.value)))

                if hardcoded_attrs:
                    attr_list = ", ".join(a[0] for a in hardcoded_attrs)
                    first_line, first_col = hardcoded_attrs[0][1], hardcoded_attrs[0][2]
                    self.add_issue(
                        issue_id="RIGID_CONSTRUCTOR",
                        title="Entidade Física com Construtor Rígido (Sem Injeção de Configuração)",
                        category="Modularidade & Ausência de Hardcoded",
                        subskill="architecture-hardcoded-auditor",
                        severity="Média",
                        penalty=15,
                        line=first_line,
                        col=first_col,
                        description=(
                            f"A classe '{class_node.name}' define propriedades físicas rígidas ({attr_list}) "
                            "no '__init__' sem permitir injeção via parâmetros ou objeto de configuração."
                        ),
                        recommendation=(
                            "Injete os coeficientes físicos ('damping', 'gravity', 'restitution') no construtor "
                            "ou receba um objeto tipado 'PhysicsConfig'."
                        ),
                        root_cause=(
                            f"Atributos físicos ({attr_list}) estão chumbados no construtor de '{class_node.name}', "
                            "impedindo parametrização por cena ou testes de estresse sob gravidades/atritos distintos."
                        ),
                        best_fix_code=(
                            "def __init__(self, mass: float = 1.0, damping: float = 0.99, gravity: Vector3 | None = None):\n"
                            "    self.mass = mass\n"
                            "    self.damping = damping\n"
                            "    self.gravity = gravity if gravity is not None else Vector3(0.0, -9.81, 0.0)"
                        ),
                        why_best_fix="Habilita Inversão de Controle (IoC) e testes parametrizados sem alterar a classe de domínio.",
                        expected_result="100% dos parâmetros físicos configuráveis por injeção no construtor.",
                    )

    def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        prev_function = self.current_function
        self.current_function = node.name

        is_method = self.current_class is not None
        has_decorators = len(node.decorator_list) > 0
        self.function_meta[node.name] = {
            "line": node.lineno,
            "col": node.col_offset,
            "is_method": is_method,
            "has_decorators": has_decorators,
        }

        # Check 1 (Módulo 1): DUPLICATE_FUNCTION com AST normalizada
        norm_body = _normalize_function_ast(node)
        if norm_body is not None:
            if norm_body in self.defined_functions.values():
                orig_fn = [name for name, dump in self.defined_functions.items() if dump == norm_body][0]
                self.add_issue(
                    issue_id="DUPLICATE_FUNCTION",
                    title="Função Duplicada Identificada na AST",
                    category="Sanitização Estática & Memory Cleanup",
                    subskill="static-sanitization-auditor",
                    severity="Alta",
                    penalty=20,
                    line=node.lineno,
                    col=node.col_offset,
                    description=f"A função '{node.name}' possui estrutura sintática idêntica à função '{orig_fn}'.",
                    recommendation=f"Refatore para reutilizar '{orig_fn}' ou extraia a lógica comum para uma função parametrizada.",
                    root_cause=f"Duplicação estrutural de corpo AST entre '{node.name}' e '{orig_fn}', elevando o custo de manutenção e risco de divergência em correções numéricas.",
                    best_fix_code=f"def {node.name}(*args, **kwargs):\n    return {orig_fn}(*args, **kwargs)",
                    why_best_fix="Elimina redundância sintática mantendo uma única fonte da verdade para a rotina matemática.",
                    expected_result="Redução de 100% em blocos de código duplicados.",
                )
            else:
                self.defined_functions[node.name] = norm_body
        else:
            self.defined_functions[node.name] = f"__trivial_{node.name}_{node.lineno}"

        # Check (Módulo 1): UNUSED_VARIABLE dentro da função
        self._check_unused_variables(node)

        # Check (Módulo 3): MISSING_DAMPING em funções de passo de física
        is_physics_step_fn = any(kw in node.name.lower() for kw in ("step_physics", "integrate", "update_physics"))
        if is_physics_step_fn:
            self._check_missing_damping(node)

        is_render_loop_fn = any(kw in node.name.lower() for kw in self.LOOP_FN_KEYWORDS)
        if is_render_loop_fn:
            self.loop_depth += 1

        # Visitar defaults de argumentos sinalizando que não são magic numbers de cálculo
        self.in_default_args = True
        for d in node.args.defaults + node.args.kw_defaults:
            if d is not None:
                self.visit(d)
        self.in_default_args = False

        for stmt in node.body:
            self.visit(stmt)

        if is_render_loop_fn:
            self.loop_depth -= 1
        self.current_function = prev_function

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)

    def _check_unused_variables(self, fn_node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        assigned_vars: Dict[str, Tuple[int, int]] = {}
        loaded_vars: Set[str] = set()
        arg_names = {a.arg for a in fn_node.args.args}

        for sub in ast.walk(fn_node):
            if isinstance(sub, ast.Name):
                if isinstance(sub.ctx, ast.Store):
                    if not sub.id.startswith("_") and sub.id not in arg_names and sub.id not in assigned_vars:
                        assigned_vars[sub.id] = (getattr(sub, "lineno", fn_node.lineno), getattr(sub, "col_offset", 0))
                elif isinstance(sub.ctx, ast.Load):
                    loaded_vars.add(sub.id)

        for var_name, (line, col) in assigned_vars.items():
            if var_name not in loaded_vars:
                self.add_issue(
                    issue_id="UNUSED_VARIABLE",
                    title="Variável Local Declarada e Não Utilizada",
                    category="Sanitização Estática & Memory Cleanup",
                    subskill="static-sanitization-auditor",
                    severity="Baixa",
                    penalty=5,
                    line=line,
                    col=col,
                    description=f"A variável local '{var_name}' na função '{fn_node.name}' é atribuída mas nunca é lida.",
                    recommendation=f"Remova a variável '{var_name}' ou utilize '_' se o valor for intencionalmente descartado.",
                    root_cause=f"Alocação desnecessária de registrador/referência local '{var_name}' sem consumo posterior no fluxo de '{fn_node.name}'.",
                    best_fix_code=f"# Remova a atribuição morta de '{var_name}' ou conecte-a à equação de saída.",
                    why_best_fix="Limpa o frame de execução local e evita que variáveis calculadas (ex: direção normalizada) sejam esquecidas na equação final.",
                    expected_result="Zero variáveis mortas no escopo local da função.",
                )

    def _check_missing_damping(self, fn_node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        fn_dump = ast.dump(fn_node).lower()
        updates_motion = any(tok in fn_dump for tok in ("velocity", "position", "vel", "pos"))
        has_damping = any(tok in fn_dump for tok in ("damping", "drag", "friction", "air_resistance"))
        if updates_motion and not has_damping:
            self.add_issue(
                issue_id="MISSING_DAMPING",
                title="Ausência de Amortecimento Físico (Drag / Damping) no Integrador",
                category="Física 3D & Matemática Numérica",
                subskill="physics-3d-math-auditor",
                severity="Média",
                penalty=15,
                physics_subdimension="S3_conservation_stability",
                subdimension_penalty=30,
                line=fn_node.lineno,
                col=fn_node.col_offset,
                description=(
                    f"O integrador físico '{fn_node.name}' atualiza movimento sem aplicar coeficiente "
                    "de amortecimento ('damping' ou 'drag')."
                ),
                recommendation=(
                    "Aplique amortecimento exponencial ou linear (ex: body.velocity *= body.damping ** dt "
                    "ou F -= c_drag * v) para dissipar energia numérica residual."
                ),
                root_cause=(
                    "Integradores explícitos/semi-implícitos acumulam erro de truncamento ao longo do tempo; "
                    "sem fator de amortecimento, corpos rígidos podem ganhar energia fantasma e nunca estabilizar em repouso."
                ),
                best_fix_code=(
                    "# Aplicação de amortecimento físico independente de framerate\n"
                    "damping_factor = math.pow(body.damping, dt * 60.0)\n"
                    "body.velocity.x *= damping_factor\n"
                    "body.velocity.y *= damping_factor\n"
                    "body.velocity.z *= damping_factor"
                ),
                why_best_fix="Garante conservação/dissipação realista de energia mecânica (E_final <= E_inicial) e convergência de repouso (sleeping).",
                expected_result="Energia mecânica total estritamente limitada (E_final <= E_inicial) em 100% dos passos.",
            )

    def visit_If(self, node: ast.If) -> None:
        test_dump = ast.dump(node.test).lower()
        is_guard = any(tok in test_dump for tok in self.GUARDRAIL_TOKENS)

        # Verifica se o if testa mag == 0 e dá return/continue no body (protegendo o restante da função)
        has_early_exit = any(isinstance(s, (ast.Return, ast.Continue, ast.Break, ast.Raise)) for s in node.body)

        if is_guard:
            self.guardrail_depth += 1
            for s in node.body:
                self.visit(s)
            for s in node.orelse:
                self.visit(s)
            self.guardrail_depth -= 1
            if has_early_exit:
                # Protege linhas subsequentes via _has_nearby_guardrail
                pass
            return

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)
            fn_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            self.called_functions.add(node.func.attr)
            fn_name = node.func.attr
        else:
            fn_name = ""

        # Check 1 (Módulo 1): ALLOC_IN_LOOP (ignorando funções de suíte de teste test_*)
        is_test_fn = bool(self.current_function and self.current_function.lower().startswith("test_"))
        if (self.in_loop or self.loop_depth > 0) and not is_test_fn:
            if fn_name in self.ALLOC_INDICATORS or any(fn_name.endswith(alloc) for alloc in self.ALLOC_INDICATORS):
                # Evitar acusar Vector3 dentro de step_physics_bad se for parte de return default, mas no loop é crítico
                self.add_issue(
                    issue_id="ALLOC_IN_LOOP",
                    title="Alocação de Memória dentro de Laço Crítico",
                    category="Sanitização Estática & Memory Cleanup",
                    subskill="static-sanitization-auditor",
                    severity="Crítica",
                    penalty=30,
                    line=node.lineno,
                    col=node.col_offset,
                    description=f"Instanciação/alocação de objeto '{fn_name}' dentro de um laço de atualização/renderização ('{self.current_function or 'loop'}').",
                    recommendation="Pré-aloque o objeto no escopo do módulo/classe (Scratchpad) e mutacione seus componentes in-place para evitar acionar o Garbage Collector.",
                    root_cause=(
                        f"A chamada '{fn_name}(...)' aloca um novo objeto na Heap a cada frame/iteração. "
                        "A 60–120Hz com múltiplos corpos, isso gera milhares de objetos descartáveis por segundo e pausas de GC."
                    ),
                    best_fix_code=(
                        f"#Fora do laço (Scratchpad pré-alocado):\n"
                        f"_TEMP_{fn_name.upper()} = {fn_name}(0.0, 0.0, 0.0)\n\n"
                        f"# Dentro do laço:\n"
                        f"body.position.x = next_x\n"
                        f"body.position.y = next_y\n"
                        f"body.position.z = next_z"
                    ),
                    why_best_fix="Zera as alocações dinâmicas no hot-loop, mantendo a latência de frame determinística.",
                    expected_result="0 B/s de alocação de objetos temporários no laço de simulação.",
                )

        # Check 2 (Módulo 3): UNCHECKED_NORMALIZE (dentro OU fora de loops, mas respeitando guardrails!)
        if fn_name in ("normalize", "normalized"):
            if not self._has_nearby_guardrail(node.lineno):
                self.add_issue(
                    issue_id="UNCHECKED_NORMALIZE",
                    title="Normalização de Vetor Sem Validação de Magnitude Zero",
                    category="Física 3D & Matemática Numérica",
                    subskill="physics-3d-math-auditor",
                    severity="Alta",
                    penalty=25,
                    physics_subdimension="S2_vector_algebra_rotations",
                    subdimension_penalty=40,
                    line=node.lineno,
                    col=node.col_offset,
                    description=f"Chamada de '{fn_name}()' detectada sem verificação prévia de magnitude > EPSILON.",
                    recommendation="Garanta que ||v|| > EPSILON (ex: if v.length_sq() > 1e-12:) antes de normalizar para prevenir divisão por zero e contaminação por NaN/Inf.",
                    root_cause="A normalização divide cada componente pela norma Euclidiana ||v||. Se o vetor for nulo (0,0,0), ocorre divisão 0/0 = NaN, contaminando toda a cena 3D.",
                    best_fix_code=(
                        "EPSILON_SQ = 1e-12\n"
                        "if velocity.length_sq() > EPSILON_SQ:\n"
                        "    direction = velocity.normalize()"
                    ),
                    why_best_fix="Usa length_sq() (evitando sqrt desnecessário quando nulo) e blinda o pipeline contra propagação de NaN.",
                    expected_result="100% de imunidade a NaN/Inf ao processar forças ou velocidades nulas.",
                )

        # Check 3 (Módulo 2): PHYSICS_RENDER_COUPLING
        if self.current_class or self.current_function:
            ctx_name = f"{self.current_class or ''}_{self.current_function or ''}".lower()
            if any(k in ctx_name for k in ("physics", "rigidbody", "integrat", "solver", "collider")):
                call_dump = ast.dump(node.func).lower()
                if any(sym in call_dump for sym in self.RENDER_COUPLED_SYMBOLS):
                    self.add_issue(
                        issue_id="PHYSICS_RENDER_COUPLING",
                        title="Acoplamento Direto entre Motor de Física e Camada de Renderização",
                        category="Modularidade & Ausência de Hardcoded",
                        subskill="architecture-hardcoded-auditor",
                        severity="Crítica",
                        penalty=35,
                        line=node.lineno,
                        col=node.col_offset,
                        description=f"Rotina de física '{self.current_function or self.current_class}' invoca diretamente primitiva gráfica/DOM.",
                        recommendation="Separe o estado físico (RigidBody3D) da malha visual (Mesh/Canvas), sincronizando via barramento de estado ou adapter na camada de apresentação.",
                        root_cause="Violação de separação de preocupações: o motor numérico depende de objetos de UI/WebGL, impedindo execução headless em testes determinísticos ou Web Workers.",
                        best_fix_code=(
                            "# Camada de Física (Pura/Headless):\n"
                            "physics_world.step(dt)\n\n"
                            "# Camada de Renderização (Sincronização desacoplada):\n"
                            "mesh.position.copy(rigid_body.position)"
                        ),
                        why_best_fix="Permite rodar a física em frequência fixa (ex: 120Hz headless) desacoplada da taxa de renderização da tela.",
                        expected_result="Desacoplamento 100% entre domínio físico e engine visual.",
                    )

        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.in_loop = True
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = False

    def visit_While(self, node: ast.While) -> None:
        self.in_loop = True
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = False

    def _extract_target_name(self, target: ast.AST) -> str:
        if isinstance(target, ast.Name):
            return target.id
        if isinstance(target, ast.Attribute):
            base = self._extract_target_name(target.value)
            return f"{base}.{target.attr}" if base else target.attr
        return ""

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        full_name = self._extract_target_name(node.target)
        lower_name = full_name.lower()

        # Check (Módulo 3 / S1): MISSING_DELTA_TIME
        if any(p in lower_name for p in ("pos", "position", "vel", "velocity")):
            right_text = ast.dump(node.value).lower()
            if not any(tok in right_text for tok in ("dt", "delta", "time", "step", "damping")):
                self.add_issue(
                    issue_id="MISSING_DELTA_TIME",
                    title="Atualização Física Sem Delta Time (dt)",
                    category="Física 3D & Matemática Numérica",
                    subskill="physics-3d-math-auditor",
                    severity="Crítica",
                    penalty=40,
                    physics_subdimension="S1_temporal_integration",
                    subdimension_penalty=100,
                    line=node.lineno,
                    col=node.col_offset,
                    description=f"A propriedade física '{full_name}' é incrementada sem multiplicação pelo fator de tempo ('dt' ou 'delta_time').",
                    recommendation="Multiplique a taxa de variação pelo delta time (ex: position += velocity * dt) para assegurar independência de framerate.",
                    root_cause=f"A integração de '{full_name}' assume 1 frame = 1 unidade de tempo. Em 120Hz o objeto se moverá com o dobro da velocidade de 60Hz.",
                    best_fix_code=f"{full_name} += velocity * dt",
                    why_best_fix="Implementa integração de Euler Semi-Implícito parametrizada por dt, garantindo invariância temporal em qualquer monitor.",
                    expected_result="Diferença de posição final < 0.01m entre simulações a 60Hz e 120Hz.",
                )

        # Check (Módulo 3 / S2): EULER_GIMBAL_LOCK
        if any(r in lower_name for r in ("rotation.", "euler", "pitch", "yaw", "roll")):
            self.add_issue(
                issue_id="EULER_GIMBAL_LOCK",
                title="Acúmulo Contínuo de Rotação 3D via Ângulos de Euler (Risco de Gimbal Lock)",
                category="Física 3D & Matemática Numérica",
                subskill="physics-3d-math-auditor",
                severity="Alta",
                penalty=20,
                physics_subdimension="S2_vector_algebra_rotations",
                subdimension_penalty=50,
                line=node.lineno,
                col=node.col_offset,
                description=f"Incremento direto em ângulo de Euler ('{full_name}') detectado.",
                recommendation="Represente rotações acumuladas usando Quaternions (q = q * dq normalizado) ou matrizes ortonormalizadas.",
                root_cause="A composição sequencial de ângulos de Euler (X-Y-Z) sofre perda de um grau de liberdade rotacional quando o eixo intermediário atinge +-90 graus (Gimbal Lock).",
                best_fix_code=(
                    "delta_q = Quaternion.from_axis_angle(angular_axis, angular_speed * dt)\n"
                    "body.orientation = (body.orientation * delta_q).normalize()"
                ),
                why_best_fix="Quaternions unitários interpolam suavemente em SO(3) sem singularidades topológicas.",
                expected_result="Eliminação total de Gimbal Lock e deriva rotacional em 360 graus.",
            )

        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        # Check (Módulo 3 / S5): STRICT_FLOAT_COMPARE
        for op in node.ops:
            if isinstance(op, (ast.Eq, ast.NotEq)):
                has_float_literal = isinstance(node.left, ast.Constant) and isinstance(node.left.value, float)
                has_float_literal |= any(isinstance(c, ast.Constant) and isinstance(c.value, float) for c in node.comparators)

                left_dump = ast.dump(node.left).lower()
                is_float_expr = any(tok in left_dump for tok in ("length", "length_sq", "norm", "dot", "distance", "position", "velocity"))

                if has_float_literal or is_float_expr:
                    self.add_issue(
                        issue_id="STRICT_FLOAT_COMPARE",
                        title="Comparação Estrita de Ponto Flutuante (IEEE 754)",
                        category="Física 3D & Matemática Numérica",
                        subskill="physics-3d-math-auditor",
                        severity="Média",
                        penalty=15,
                        physics_subdimension="S5_numerical_robustness",
                        subdimension_penalty=40,
                        line=node.lineno,
                        col=node.col_offset,
                        description="Comparação direta com '==' ou '!=' em grandeza contínua/ponto flutuante.",
                        recommendation="Utilize aproximação por tolerância numérica com EPSILON: abs(a - b) < EPSILON (ex: 1e-6).",
                        root_cause="Erros de arredondamento de mantissa em IEEE 754 impedem que cálculos iterativos atinjam igualdade binária exata (ex: 0.1 + 0.2 != 0.3).",
                        best_fix_code="EPSILON = 1e-6\nif abs(value - target) < EPSILON:\n    ...",
                        why_best_fix="Substitui igualdade pontual instável por uma vizinhança métrica de raio EPSILON.",
                        expected_result="100% de estabilidade em condições de parada e detecção de repouso.",
                    )
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        # Check (Módulo 2): HARDCODED_MAGIC_NUMBER
        if self.in_default_args or not self.current_function:
            return
        if self.current_function in ("__init__", "main") or self.current_function.startswith("test_"):
            return

        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            val = node.value
            allowed_literals = {0, 1, -1, 0.0, 1.0, -1.0, 2, 2.0, 0.5, -0.5, 100.0, 1e-6, 1e-12}
            if val not in allowed_literals:
                self.add_issue(
                    issue_id="HARDCODED_MAGIC_NUMBER",
                    title="Uso de Número Mágico (Hardcoded Constant) em Rotina Operacional",
                    category="Modularidade & Ausência de Hardcoded",
                    subskill="architecture-hardcoded-auditor",
                    severity="Baixa",
                    penalty=10,
                    line=node.lineno,
                    col=node.col_offset,
                    description=f"O literal numérico '{val}' está chumbado diretamente dentro da função '{self.current_function}'.",
                    recommendation="Extraia o valor para uma constante nomeada no topo do módulo ou em um objeto de configuração física (ex: RESTITUTION_COEFF, GRAVITY_Y).",
                    root_cause=f"O valor '{val}' aparece em cálculo operacional sem semântica explícita, dificultando calibração física e leitura das equações.",
                    best_fix_code=f"DEFAULT_COEFFICIENT = {val}\n# Na função:\nresult = value * DEFAULT_COEFFICIENT",
                    why_best_fix="Documenta o significado físico da constante e centraliza ajustes de simulação em um único ponto.",
                    expected_result="Zero constantes mágicas não documentadas em equações de movimento.",
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
            "S1_integracao_temporal_dt": {
                "score": subdim_scores["S1_temporal_integration"],
                "weight": 0.25,
            },
            "S2_algebra_vetorial_rotacoes": {
                "score": subdim_scores["S2_vector_algebra_rotations"],
                "weight": 0.25,
            },
            "S3_conservacao_estabilidade": {
                "score": subdim_scores["S3_conservation_stability"],
                "weight": 0.20,
            },
            "S4_colisao_ccd": {
                "score": subdim_scores["S4_collision_ccd"],
                "weight": 0.15,
            },
            "S5_robustez_numerica_float": {
                "score": subdim_scores["S5_numerical_robustness"],
                "weight": 0.15,
            },
        },
    }


def analyze_code(code_str: str, filename: str = "script.py") -> Dict[str, Any]:
    try:
        tree = ast.parse(code_str, filename=filename)
    except SyntaxError as e:
        return {
            "filename": filename,
            "error": f"Erro de Sintaxe ao analisar o arquivo {filename}: {str(e)}",
            "total_issues": 0,
            "issues": [],
            "scores": compute_module_scores([]),
        }

    source_lines = code_str.splitlines()
    visitor = PhysicsCodeASTVisitor(filename=filename, source_lines=source_lines)
    visitor.visit(tree)

    # Detectar código morto (funções de topo declaradas mas nunca invocadas no módulo)
    exempt_prefixes = ("__", "test_", "visit_", "step_physics_")
    exempt_names = {"main", "run", "analyze_code", "compute_module_scores"}

    for fn_name, meta in visitor.function_meta.items():
        if (
            fn_name not in visitor.called_functions
            and not meta["is_method"]
            and not meta["has_decorators"]
            and fn_name not in exempt_names
            and not fn_name.startswith(exempt_prefixes)
        ):
            visitor.add_issue(
                issue_id="DEAD_CODE_FUNCTION",
                title="Função Não Utilizada (Código Morto)",
                category="Sanitização Estática & Memory Cleanup",
                subskill="static-sanitization-auditor",
                severity="Média",
                penalty=10,
                line=meta["line"],
                col=meta["col"],
                description=f"A função '{fn_name}' foi declarada na linha {meta['line']} mas nunca é invocada.",
                recommendation="Remova a função órfã ou exporte-a explicitamente em '__all__' se fizer parte da API pública.",
                root_cause=f"A função '{fn_name}' permanece na árvore sintática sem consumidores internos, aumentando a superfície cognitiva do módulo.",
                best_fix_code=f"# Remova a função '{fn_name}' ou integre sua chamada ao pipeline principal.",
                why_best_fix="Reduz código morto e mantém apenas símbolos ativos no grafo de chamadas.",
                expected_result="100% das funções declaradas no módulo possuem consumidores ou testes vinculados.",
            )

    scores = compute_module_scores(visitor.issues)
    return {
        "filename": filename,
        "language": "python",
        "total_issues": len(visitor.issues),
        "scores": scores,
        "issues": visitor.issues,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analisador AST Python para Auditoria de Código e Física 3D.")
    parser.add_argument("filepath", help="Caminho do arquivo Python (.py) a ser analisado.")
    args = parser.parse_args()

    filepath = Path(args.filepath)
    if not filepath.exists():
        print(json.dumps({"error": f"Arquivo não encontrado: {filepath}", "issues": []}, ensure_ascii=False))
        sys.exit(1)

    try:
        code_str = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(json.dumps({"error": f"Erro ao ler arquivo: {e}", "issues": []}, ensure_ascii=False))
        sys.exit(1)

    result = analyze_code(code_str, filename=str(filepath))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
