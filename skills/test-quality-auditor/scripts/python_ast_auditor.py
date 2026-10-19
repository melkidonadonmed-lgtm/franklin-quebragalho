#!/usr/bin/env python3
"""
python_ast_auditor.py
Analisador Estático AST para Auditoria de Qualidade de Testes em Python (Pytest / Unittest).
"""

from __future__ import annotations

import ast
from typing import List, Optional, Tuple

from models import AuditIssue, FileAuditReport, TestDossierRecord, classify_quality_level


class TestQualityASTVisitor(ast.NodeVisitor):
    """Analisador AST Python para detecção de asserções fracas/tautológicas, vazamento de estado e não-determinismo."""

    __test__ = False

    def __init__(self, filename: str = "test_suite.py") -> None:
        self.filename = filename
        self.issues: List[AuditIssue] = []
        self.dossiers: List[TestDossierRecord] = []
        self.current_test: Optional[str] = None
        self.current_test_line: int = 1
        self.assertion_count: int = 0
        self.strong_assertion_count: int = 0
        self.has_time_sleep_or_now: bool = False
        self.has_try_finally: bool = False
        self.mutates_shared_state: bool = False
        self.current_test_issues: List[AuditIssue] = []
        self.not_none_vars: List[Tuple[str, int, int]] = []
        self.strongly_asserted_vars: set[str] = set()

    def add_issue(
        self,
        issue_id: str,
        title: str,
        category: str,
        severity: str,
        line: int,
        col: int,
        penalty: int,
        description: str,
        recommendation: str,
    ) -> None:
        issue = AuditIssue(
            id=issue_id,
            title=title,
            category=category,
            severity=severity,
            file=self.filename,
            test_name=self.current_test or "<module>",
            line=line,
            col=col,
            penalty=penalty,
            description=description,
            recommendation=recommendation,
        )
        self.issues.append(issue)
        self.current_test_issues.append(issue)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._inspect_test_function(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._inspect_test_function(node)

    def _reset_test_state(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self.current_test = node.name
        self.current_test_line = node.lineno
        self.assertion_count = 0
        self.strong_assertion_count = 0
        self.has_time_sleep_or_now = False
        self.has_try_finally = any(isinstance(stmt, ast.Try) and bool(stmt.finalbody) for stmt in ast.walk(node))
        self.mutates_shared_state = False
        self.current_test_issues = []
        self.not_none_vars = []
        self.strongly_asserted_vars = set()

        exec_body = [
            stmt
            for stmt in node.body
            if not (
                isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)
            )
        ]
        if len(exec_body) == 0 or (len(exec_body) == 1 and isinstance(exec_body[0], (ast.Pass, ast.Return))):
            self.add_issue(
                "EMPTY_TEST_BODY",
                "Teste Vazio / Placebo",
                "Integridade do Teste",
                "Crítica",
                node.lineno,
                node.col_offset,
                85,
                f"[FATO] O teste '{node.name}' está vazio ou contém apenas 'pass'/'return'.",
                "Implemente a lógica completa de teste seguindo o padrão Arrange-Act-Assert.",
            )

    def _evaluate_post_visit_issues(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        for var_name, ln, col in self.not_none_vars:
            if var_name not in self.strongly_asserted_vars:
                self.add_issue(
                    "WEAK_IS_NOT_NONE_ASSERT",
                    "Asserção Superficial Isolada (assert x is not None)",
                    "Qualidade da Asserção",
                    "Média",
                    ln,
                    col,
                    55,
                    f"[FATO] O teste '{node.name}' verifica apenas se '{var_name}' não é None (linha {ln}) sem validar nenhum atributo ou valor de negócio.",
                    f"Valide as propriedades ou valor exato de '{var_name}' (ex: assert {var_name}.status == 'EXPECTED').",
                )
        if self.assertion_count == 0 and not any(i.id == "EMPTY_TEST_BODY" for i in self.current_test_issues):
            self.add_issue(
                "MISSING_ASSERTIONS",
                "Teste Sem Asserções (False Positive Potential)",
                "Eficácia da Verificação",
                "Crítica",
                node.lineno,
                node.col_offset,
                80,
                f"[FATO] O teste '{node.name}' executa código (Act) mas não realiza nenhuma asserção (Assert).",
                "Adicione asserções explícitas sobre o valor retornado, contrato de tipo ou efeito colateral.",
            )
        if self.has_time_sleep_or_now:
            self.add_issue(
                "NON_DETERMINISTIC_TIME",
                "Uso de Tempo Real ou Sleep em Teste (Flaky Test Risk)",
                "Determinismo & Reprodutibilidade",
                "Alta",
                node.lineno,
                node.col_offset,
                25,
                f"[FATO] O teste '{node.name}' invoca time.sleep() ou datetime.now() diretamente.",
                "Substitua o tempo real por congeladores/injeção de tempo (ex: monkeypatch ou mock de relógio).",
            )
        if self.mutates_shared_state and not self.has_try_finally:
            self.add_issue(
                "GLOBAL_STATE_LEAKAGE",
                "Mutação de Estado Compartilhado sem Bloco try/finally",
                "Isolamento de Estado (AAA)",
                "Média",
                node.lineno,
                node.col_offset,
                18,
                f"[FATO] O teste '{node.name}' cria/altera checkpoints ou estado global sem proteção 'try/finally'.",
                "Envolva a limpeza de estado em um bloco 'try...finally' para evitar contaminação.",
            )

    def _inspect_test_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        is_test_fn = node.name.startswith("test_") or node.name.startswith("_test_")
        if not is_test_fn:
            self.generic_visit(node)
            return

        prev_test = self.current_test
        self._reset_test_state(node)
        self.generic_visit(node)
        self._evaluate_post_visit_issues(node)

        total_penalty = sum(i.penalty for i in self.current_test_issues)
        score = max(0, 100 - total_penalty)
        evidence_str = (
            f"{self.assertion_count} asserção(ões) detectada(s), 0 anomalias AST."
            if not self.current_test_issues
            else "; ".join(f"{i.id} (L{i.line})" for i in self.current_test_issues)
        )
        self.dossiers.append(
            TestDossierRecord(
                test_name=node.name,
                file=self.filename,
                line=node.lineno,
                assertion_count=self.assertion_count,
                score=score,
                level=classify_quality_level(score),
                status="[PASS]" if len(self.current_test_issues) == 0 and score >= 81 else "[FAIL]",
                issues=[i.id for i in self.current_test_issues],
                evidence=evidence_str,
                domain="python",
            )
        )
        self.current_test = prev_test

    def _handle_is_not_none_assert(self, left_expr: ast.expr, lineno: int, col_offset: int) -> None:
        is_regex_call = (
            isinstance(left_expr, ast.Call)
            and isinstance(left_expr.func, ast.Attribute)
            and left_expr.func.attr in ("match", "search", "fullmatch")
        )
        if is_regex_call:
            self.strong_assertion_count += 1
            for sub in ast.walk(left_expr):
                if isinstance(sub, ast.Name):
                    self.strongly_asserted_vars.add(sub.id)
        else:
            var_id = left_expr.id if isinstance(left_expr, ast.Name) else ast.unparse(left_expr)
            self.not_none_vars.append((var_id, lineno, col_offset))

    @staticmethod
    def _extract_brittle_catalog_len(test_expr: ast.expr) -> Optional[int]:
        if (
            isinstance(test_expr, ast.Compare)
            and len(test_expr.ops) == 1
            and isinstance(test_expr.ops[0], ast.Eq)
            and isinstance(test_expr.left, ast.Call)
            and isinstance(test_expr.left.func, ast.Name)
            and test_expr.left.func.id == "len"
            and isinstance(test_expr.comparators[0], ast.Constant)
            and isinstance(test_expr.comparators[0].value, int)
            and test_expr.comparators[0].value >= 15
        ):
            return int(test_expr.comparators[0].value)
        return None

    def visit_Assert(self, node: ast.Assert) -> None:
        if self.current_test:
            self.assertion_count += 1
            brittle_len = self._extract_brittle_catalog_len(node.test)
            if isinstance(node.test, ast.Constant) and node.test.value is True:
                self.add_issue(
                    "TAUTOLOGICAL_ASSERT",
                    "Asserção Tautológica (assert True)",
                    "Qualidade da Asserção",
                    "Crítica",
                    node.lineno,
                    node.col_offset,
                    80,
                    f"[FATO] O teste '{self.current_test}' contém 'assert True', que sempre passa sem validar nenhuma regra.",
                    "Substitua por uma comparação explícita do valor ou contrato retornado.",
                )
            elif (
                isinstance(node.test, ast.Compare)
                and len(node.test.ops) == 1
                and isinstance(node.test.ops[0], ast.IsNot)
                and isinstance(node.test.comparators[0], ast.Constant)
                and node.test.comparators[0].value is None
            ):
                self._handle_is_not_none_assert(node.test.left, node.lineno, node.col_offset)
            elif brittle_len is not None:
                self.add_issue(
                    "BRITTLE_CATALOG_COUNT",
                    f"Contagem Literal Rígida de Catálogo (assert len(...) == {brittle_len})",
                    "Acoplamento de Implementação",
                    "Média",
                    node.lineno,
                    node.col_offset,
                    22,
                    f"[FATO] O teste '{self.current_test}' fixa 'len(...) == {brittle_len}' na linha {node.lineno}.",
                    "Compare contra a contagem dinâmica real de diretórios válidos no filesystem.",
                )
            else:
                self.strong_assertion_count += 1
                for sub in ast.walk(node.test):
                    if isinstance(sub, ast.Name):
                        self.strongly_asserted_vars.add(sub.id)
                    elif isinstance(sub, (ast.Attribute, ast.Subscript, ast.Call)):
                        self.strongly_asserted_vars.add(ast.unparse(sub))

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if self.current_test:
            fn_name = ""
            if isinstance(node.func, ast.Attribute):
                fn_name = node.func.attr
                if fn_name.startswith("assert") or fn_name == "raises":
                    self.assertion_count += 1
                    if fn_name == "assertTrue" and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value is True:
                        self.add_issue(
                            "TAUTOLOGICAL_ASSERT",
                            "Asserção Tautológica (assertTrue(True))",
                            "Qualidade da Asserção",
                            "Crítica",
                            node.lineno,
                            node.col_offset,
                            80,
                            f"[FATO] O teste '{self.current_test}' invoca assertTrue(True).",
                            "Valide uma expressão booleana derivada do estado do SUT.",
                        )
            elif isinstance(node.func, ast.Name):
                fn_name = node.func.id
                if fn_name.startswith("assert"):
                    self.assertion_count += 1

            if fn_name in ("sleep", "now", "utcnow"):
                self.has_time_sleep_or_now = True

            if (
                fn_name == "append"
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Attribute)
                and node.func.value.attr == "results"
            ):
                self.assertion_count += 1
                self.strong_assertion_count += 1

            if fn_name == "franklin_harness_guard":
                for kw in node.keywords:
                    if kw.arg == "proposed_tool_or_action" and isinstance(kw.value, ast.Constant):
                        if "Remove-Item" in str(kw.value.value):
                            self.mutates_shared_state = True

        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if self.current_test and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.add_issue(
                "SILENCED_EXCEPTION_IN_TEST",
                "Exceção Silenciada em Teste (try-except pass)",
                "Tratamento de Erros & Robustez",
                "Crítica",
                node.lineno,
                node.col_offset,
                75,
                f"[FATO] O teste '{self.current_test}' captura uma exceção e executa 'pass' na linha {node.lineno}.",
                "Use pytest.raises(ExcecaoEsperada) para validar falhas explicitamente.",
            )
        self.generic_visit(node)


def audit_python_test_file(code_str: str, filename: str = "test_suite.py") -> FileAuditReport:
    """Executa o visitor AST sobre um arquivo de teste Python."""
    try:
        tree = ast.parse(code_str, filename=filename)
        visitor = TestQualityASTVisitor(filename=filename)
        visitor.visit(tree)
        avg_score = (
            sum(d.score for d in visitor.dossiers) / len(visitor.dossiers)
            if visitor.dossiers
            else (0.0 if visitor.issues else 100.0)
        )
        return FileAuditReport(
            aprovado=len(visitor.issues) == 0 and avg_score >= 81.0,
            filename=filename,
            total_tests=len(visitor.dossiers),
            score_medio=avg_score,
            nivel_espectro=classify_quality_level(avg_score),
            total_inconformidades=len(visitor.issues),
            dossiers=visitor.dossiers,
            issues=visitor.issues,
            language="python",
        )
    except SyntaxError as e:
        syn_issue = AuditIssue(
            id="SYNTAX_ERROR",
            title=f"Erro de Sintaxe: {e.msg}",
            category="Integridade Sintática",
            severity="Crítica",
            file=filename,
            test_name="<syntax>",
            line=e.lineno or 1,
            col=e.offset or 1,
            penalty=100,
            description=f"[FATO] Falha ao construir árvore AST em {filename}:{e.lineno}.",
            recommendation="Corrija o erro de sintaxe antes de executar a suíte.",
        )
        return FileAuditReport(
            aprovado=False,
            filename=filename,
            total_tests=0,
            score_medio=0.0,
            nivel_espectro="NÍVEL 1: ILUSÓRIO / PLACEBO",
            total_inconformidades=1,
            dossiers=[],
            issues=[syn_issue],
            language="python",
        )
