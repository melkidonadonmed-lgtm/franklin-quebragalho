"""
frontiercode_maintainability_guardrail.py
Guardrail Adaptativo FrontierCode 1.1 + Performance 3D (Não-Engessado / Qualidade Linear Alta).

Princípios para Alta Variedade de Projetos (TDAH-Friendly):
1. Detecção Automática de Perfil (profile="auto"):
   - Se o arquivo contém primitivas 3D/Simulação (Vector3, Matrix4, Quaternion, THREE, RigidBody, dt),
     ativa o motor de Física 3D + Sanitização.
   - Caso contrário, opera em modo Geral (FrontierCode Maintainability: Tipagem, Bare Except, Código Morto),
     sem cobrar regras de Física 3D em scripts de backend, IA ou automação.
2. Separação entre Hard Gates (Erros Críticos/Altos) e Soft Advisories (Avisos de Manutenibilidade):
   - Funções curtas (<= 6 linhas), dunders (__init__) ou helpers privados (_fn) não exigem docstring burocrática.
   - A aprovação é baseada na ausência de falhas críticas e no Escore de Qualidade Linear (>= 75.0),
     e nunca em um bloqueio rígido de "zero avisos".
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


def detect_code_profile(code_str: str) -> str:
    """Detecta automaticamente se o arquivo é de Física 3D/Gráficos ou Código Geral."""
    lower = code_str.lower()
    physics_tokens = (
        "vector3",
        "matrix4",
        "quaternion",
        "rigidbody",
        "three.",
        "webgl",
        "deltatime",
        "step_physics",
        "restitution",
        "collider",
    )
    matches = sum(1 for tok in physics_tokens if tok in lower)
    return "3d_physics" if matches >= 2 else "general"


class _LocalVarNormalizer(ast.NodeTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.var_map: Dict[str, str] = {}
        self.counter = 0

    def _norm(self, name: str) -> str:
        if name in ("self", "cls", "True", "False", "None"):
            return name
        if name not in self.var_map:
            self.var_map[name] = f"_v{self.counter}"
            self.counter += 1
        return self.var_map[name]

    def visit_arg(self, node: ast.arg) -> ast.arg:
        n = copy.copy(node)
        n.arg = self._norm(n.arg)
        n.annotation = None
        return n

    def visit_Name(self, node: ast.Name) -> ast.Name:
        n = copy.copy(node)
        if node.id in self.var_map or isinstance(node.ctx, ast.Store):
            n.id = self._norm(node.id)
        return n


class FrontierCodeMaintainabilityVisitor(ast.NodeVisitor):
    """
    AST Visitor Adaptativo integrando FrontierCode 1.1 (Manutenibilidade, Tipagem, Exceções)
    com Sanitização e Física 3D sob demanda.
    """

    GUARDRAIL_TOKENS = ("length", "length_sq", "mag", "magnitude", "norm", "epsilon", "eps", "1e-")

    def __init__(
        self,
        filename: str = "script.py",
        max_function_lines: int = 60,
        profile: str = "auto",
        source_lines: Optional[List[str]] = None,
    ) -> None:
        self.filename = filename
        self.max_function_lines = max_function_lines
        self.profile = profile
        self.source_lines = source_lines or []
        self.issues: List[Dict[str, Any]] = []
        self.defined_functions: Dict[str, str] = {}
        self.function_meta: Dict[str, Dict[str, Any]] = {}
        self.called_functions: Set[str] = set()
        self.in_loop = False
        self.current_function: Optional[str] = None
        self.current_class: Optional[str] = None
        self.loop_depth = 0
        self.in_default_args = False

    def add_issue(
        self,
        issue_id: str,
        title: str,
        category: str,
        severity: str,
        line: int,
        col: int,
        description: str,
        recommendation: str,
        tier: str = "hard",
    ) -> None:
        self.issues.append(
            {
                "id": issue_id,
                "title": title,
                "category": category,
                "severity": severity,
                "tier": tier,  # "hard" (impacta aprovação) vs "advisory" (orientação leve sem travar)
                "file": self.filename,
                "line": line,
                "col": col,
                "description": description,
                "recommendation": recommendation,
            }
        )

    def _has_nearby_guardrail(self, lineno: int) -> bool:
        if not self.source_lines:
            return False
        start_idx = max(0, lineno - 4)
        end_idx = min(len(self.source_lines), lineno)
        window = " ".join(self.source_lines[start_idx:end_idx]).lower()
        return any(tok in window for tok in self.GUARDRAIL_TOKENS)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        prev_cls = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = prev_cls

    def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        prev_function = self.current_function
        self.current_function = node.name

        line_count = (node.end_lineno or node.lineno) - node.lineno
        is_private_or_dunder = node.name.startswith("_")
        is_visitor_or_test = node.name.startswith(("visit_", "test_"))
        is_short_helper = line_count <= 6

        self.function_meta[node.name] = {
            "line": node.lineno,
            "col": node.col_offset,
            "is_method": self.current_class is not None,
            "has_decorators": len(node.decorator_list) > 0,
        }

        # 1. Checagem de Docstring (Apenas para funções públicas não-triviais -> Advisory suave)
        if not ast.get_docstring(node) and not is_private_or_dunder and not is_visitor_or_test and not is_short_helper:
            self.add_issue(
                "MISSING_DOCSTRING",
                "Função Pública Sem Docstring Explicativa",
                "Manutenibilidade & Documentação (FrontierCode)",
                "Baixa",
                node.lineno,
                node.col_offset,
                f"A função pública '{node.name}' ({line_count} linhas) não possui docstring explicativa.",
                "Adicione uma docstring concisa descrevendo o propósito e contrato da função.",
                tier="advisory",
            )

        # 2. Checagem de Type Hints nos Parâmetros (Advisory)
        if not is_visitor_or_test:
            for arg in node.args.args:
                if arg.arg not in ("self", "cls") and arg.annotation is None:
                    self.add_issue(
                        "MISSING_TYPE_HINT",
                        "Parâmetro Sem Anotação de Tipo (Type Hint)",
                        "Tipagem Estrita (FrontierCode)",
                        "Média",
                        arg.lineno,
                        arg.col_offset,
                        f"O parâmetro '{arg.arg}' na função '{node.name}' não possui Type Hint.",
                        f"Especifique o tipo esperado (ex: '{arg.arg}: Any' ou tipo concreto).",
                        tier="advisory",
                    )

        # 3. Checagem de Type Hint no Retorno (Advisory)
        if node.returns is None and not is_private_or_dunder and not is_visitor_or_test:
            self.add_issue(
                "MISSING_RETURN_TYPE_HINT",
                "Retorno Sem Anotação de Tipo",
                "Tipagem Estrita (FrontierCode)",
                "Baixa",
                node.lineno,
                node.col_offset,
                f"A função '{node.name}' não declara o tipo de retorno esperado.",
                "Adicione anotação de retorno explícita (ex: '-> None' ou '-> Dict[str, Any]').",
                tier="advisory",
            )

        # 4. Checagem de Comprimento da Função (Tolerância confortável)
        if line_count > self.max_function_lines:
            self.add_issue(
                "EXCESSIVE_FUNCTION_LENGTH",
                "Função Extensa (Candidata a Modularização)",
                "Manutenibilidade (FrontierCode)",
                "Média",
                node.lineno,
                node.col_offset,
                f"A função '{node.name}' possui {line_count} linhas (referência recomendada: <= {self.max_function_lines}).",
                "Considere extrair blocos lógicos independentes para funções auxiliares se a leitura ficar densa.",
                tier="advisory",
            )

        # 5. Duplicatas Sintáticas Reais (ignorando funções triviais <= 2 statements)
        body_no_doc = list(node.body)
        if (
            body_no_doc
            and isinstance(body_no_doc[0], ast.Expr)
            and isinstance(body_no_doc[0].value, ast.Constant)
            and isinstance(body_no_doc[0].value.value, str)
        ):
            body_no_doc = body_no_doc[1:]

        if len(body_no_doc) >= 2:
            norm = _LocalVarNormalizer()
            for a in node.args.args:
                norm.visit_arg(a)
            norm_stmts = [norm.visit(copy.deepcopy(s)) for s in body_no_doc]
            normalized_body = ast.dump(ast.Module(body=norm_stmts, type_ignores=[]), include_attributes=False)
            if normalized_body in self.defined_functions.values():
                orig_fn = [name for name, dump in self.defined_functions.items() if dump == normalized_body][0]
                self.add_issue(
                    "DUPLICATE_FUNCTION",
                    "Função Duplicada Identificada",
                    "Sanitização",
                    "Alta",
                    node.lineno,
                    node.col_offset,
                    f"A função '{node.name}' possui estrutura idêntica à função '{orig_fn}'.",
                    f"Reaproveite '{orig_fn}' ou extraia a lógica compartilhada.",
                    tier="hard",
                )
            else:
                self.defined_functions[node.name] = normalized_body

        is_render_loop_fn = (
            any(kw in node.name.lower() for kw in ("update", "render", "step", "animate", "loop", "tick"))
            and not is_visitor_or_test
        )
        if is_render_loop_fn:
            self.loop_depth += 1

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

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.type is None:
            self.add_issue(
                "BARE_EXCEPT",
                "Captura Genérica de Exceção (Bare Except)",
                "Robustez & Tratamento de Erros (FrontierCode)",
                "Alta",
                node.lineno,
                node.col_offset,
                "Uso de 'except:' genérico sem especificar a classe de exceção.",
                "Use 'except Exception as e:' ou exceções específicas para não engolir SystemExit/KeyboardInterrupt.",
                tier="hard",
            )
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

        is_test_fn = bool(self.current_function and self.current_function.lower().startswith("test_"))

        # Checks de Performance Gráfica / Física 3D
        if (self.in_loop or self.loop_depth > 0) and not is_test_fn:
            alloc_indicators = ("Vector3", "Vector2", "Matrix4", "Matrix3", "Quaternion", "zeros", "ones")
            if fn_name in alloc_indicators or any(fn_name.endswith(alloc) for alloc in alloc_indicators):
                self.add_issue(
                    "ALLOC_IN_LOOP",
                    "Alocação de Objeto 3D/Vetorial dentro de Laço Crítico",
                    "Performance & Memória",
                    "Crítica",
                    node.lineno,
                    node.col_offset,
                    f"Instanciação de '{fn_name}' dentro de laço de simulação/renderização.",
                    "Pré-aloque o objeto fora do laço (Scratchpad) e reutilize-o.",
                    tier="hard",
                )

        if self.profile == "3d_physics" and fn_name in ("normalize", "normalized"):
            if not self._has_nearby_guardrail(node.lineno):
                self.add_issue(
                    "UNCHECKED_NORMALIZE",
                    "Normalização de Vetor Sem Validação de Magnitude Zero",
                    "Física 3D & Matemática",
                    "Alta",
                    node.lineno,
                    node.col_offset,
                    f"Chamada de '{fn_name}()' sem verificação próxima de magnitude > EPSILON.",
                    "Garanta ||v|| > EPSILON antes de normalizar para prevenir NaN.",
                    tier="hard",
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

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        if self.profile == "3d_physics" and isinstance(node.target, (ast.Name, ast.Attribute)):
            var_name = node.target.id if isinstance(node.target, ast.Name) else node.target.attr
            if any(p in var_name.lower() for p in ("pos", "position", "vel", "velocity")):
                right_text = ast.dump(node.value).lower()
                if not any(tok in right_text for tok in ("dt", "delta", "time", "step", "damping")):
                    self.add_issue(
                        "MISSING_DELTA_TIME",
                        "Atualização Física Sem Delta Time (dt)",
                        "Física 3D & Matemática",
                        "Crítica",
                        node.lineno,
                        node.col_offset,
                        f"Variável '{var_name}' atualizada sem fator de tempo ('dt').",
                        "Multiplique por dt (ex: position += velocity * dt) para garantir independência de FPS.",
                        tier="hard",
                    )
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        if self.profile == "3d_physics":
            for op in node.ops:
                if isinstance(op, (ast.Eq, ast.NotEq)):
                    has_float_literal = isinstance(node.left, ast.Constant) and isinstance(node.left.value, float)
                    has_float_literal |= any(
                        isinstance(c, ast.Constant) and isinstance(c.value, float) for c in node.comparators
                    )
                    if has_float_literal:
                        self.add_issue(
                            "STRICT_FLOAT_COMPARE",
                            "Comparação Estrita de Ponto Flutuante (IEEE 754)",
                            "Física 3D & Matemática",
                            "Média",
                            node.lineno,
                            node.col_offset,
                            "Comparação direta com '==' ou '!=' em floats.",
                            "Utilize tolerância por EPSILON: abs(a - b) < EPSILON.",
                            tier="hard",
                        )
        self.generic_visit(node)


def audit_code_snippet(
    code: str,
    filename: str = "agent_code.py",
    profile: str = "auto",
    max_function_lines: int = 60,
) -> Dict[str, Any]:
    """
    Executa a auditoria adaptativa FrontierCode + Física 3D.
    Não engessa o desenvolvedor: distingue 'hard_issues' (bloqueantes) de 'advisories' (melhoria linear).
    """
    resolved_profile = detect_code_profile(code) if profile == "auto" else profile

    try:
        tree = ast.parse(code, filename=filename)
        source_lines = code.splitlines()
        auditor = FrontierCodeMaintainabilityVisitor(
            filename=filename,
            max_function_lines=max_function_lines,
            profile=resolved_profile,
            source_lines=source_lines,
        )
        auditor.visit(tree)

        # Detectar funções de topo não utilizadas (ignorando métodos de classe públicos e entrypoints)
        exempt_names = {"main", "run", "audit_code_snippet", "analyze_code"}
        for fn_name, meta in auditor.function_meta.items():
            if (
                fn_name not in auditor.called_functions
                and not meta["is_method"]
                and not meta["has_decorators"]
                and not fn_name.startswith(("__", "test_", "visit_"))
                and fn_name not in exempt_names
            ):
                auditor.add_issue(
                    "DEAD_CODE_FUNCTION",
                    "Função de Topo Não Referenciada Internamente",
                    "Sanitização",
                    "Baixa",
                    meta["line"],
                    meta["col"],
                    f"A função '{fn_name}' (linha {meta['line']}) não é chamada dentro deste módulo.",
                    "Verifique se ela é consumida externamente ou se pode ser removida.",
                    tier="advisory",
                )

        hard_issues = [i for i in auditor.issues if i.get("tier") == "hard"]
        advisories = [i for i in auditor.issues if i.get("tier") == "advisory"]

        # Cálculo de Nota de Qualidade Linear (Penalidades fortes para hard, suaves para advisories)
        penalty = 0.0
        for iss in hard_issues:
            sev = iss["severity"]
            penalty += 30.0 if sev == "Crítica" else (20.0 if sev == "Alta" else 10.0)
        for adv in advisories:
            penalty += 2.5  # Avisos de estilo/tipagem descontam suavemente sem reprovar código funcional

        linear_quality_score = round(max(0.0, 100.0 - penalty), 2)
        aprovado = len(hard_issues) == 0 and linear_quality_score >= 70.0

        return {
            "aprovado": aprovado,
            "profile_detected": resolved_profile,
            "linear_quality_score": linear_quality_score,
            "filename": filename,
            "total_inconformidades": len(auditor.issues),
            "hard_issues_count": len(hard_issues),
            "advisories_count": len(advisories),
            "problemas": auditor.issues,
        }
    except SyntaxError as e:
        return {
            "aprovado": False,
            "profile_detected": resolved_profile,
            "linear_quality_score": 0.0,
            "filename": filename,
            "total_inconformidades": 1,
            "hard_issues_count": 1,
            "advisories_count": 0,
            "problemas": [
                {
                    "id": "SYNTAX_ERROR",
                    "title": "Erro de Sintaxe no Código",
                    "category": "Sintaxe",
                    "severity": "Crítica",
                    "tier": "hard",
                    "file": filename,
                    "line": e.lineno or 1,
                    "col": e.offset or 0,
                    "description": f"Erro de sintaxe Python: {e.msg}",
                    "recommendation": "Corrija a sintaxe antes de executar.",
                }
            ],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Guardrail Adaptativo FrontierCode 1.1 (Sem Engessamento).")
    parser.add_argument("filepath", nargs="?", help="Arquivo Python opcional para auditar.")
    parser.add_argument("--profile", choices=["auto", "general", "3d_physics"], default="auto")
    args = parser.parse_args()

    if args.filepath:
        path = Path(args.filepath)
        code_content = path.read_text(encoding="utf-8")
        res = audit_code_snippet(code_content, filename=str(path), profile=args.profile)
    else:
        exemplo = """
def processar_dados(registro, flag):
    # Função sem docstring, sem type hints e com bare except
    try:
        return registro.upper() if flag else registro.lower()
    except:
        return ""
"""
        res = audit_code_snippet(exemplo, profile=args.profile)
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
