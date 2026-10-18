#!/usr/bin/env python3
"""
code_acceptability_auditor.py
Motor determinístico de auditoria estática de código Python via AST, Regex e Pydantic v2.
Valida segurança (SEC001-003), sintaxe (SYN001), tratamento de erros (ERR001-003),
tipagem estática (TYP001-002) e modularidade (ARCH001).
"""

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Literal, Optional, Set, Tuple
from pydantic import BaseModel, ConfigDict, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

SeverityType = Literal["CRÍTICO", "ALTO", "MÉDIO", "BAIXO"]
RuleIdType = Literal[
    "SYN001", "SEC001", "SEC002", "SEC003",
    "ERR001", "ERR002", "ERR003", "TYP001", "TYP002", "ARCH001"
]

RULE_PENALTIES: Dict[str, float] = {
    "SYN001": 25.0,
    "SEC001": 25.0,
    "SEC002": 25.0,
    "SEC003": 25.0,
    "ERR001": 10.0,
    "ERR002": 5.0,
    "ERR003": 25.0,
    "TYP001": 5.0,
    "TYP002": 5.0,
    "ARCH001": 2.0,
}

SECRET_VAR_REGEX = re.compile(
    r"(?:^|_)(api[_-]?key|secret[_-]?key|secret|password|passwd|pwd|access[_-]?token|"
    r"auth[_-]?token|private[_-]?key|client[_-]?secret|jwt[_-]?secret|bearer[_-]?token)(?:$|_)",
    re.IGNORECASE,
)

SECRET_VALUE_SIGNATURES = re.compile(
    r"(sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{20,}|"
    r"AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,})"
)

SAFE_PLACEHOLDERS: Set[str] = {
    "", "none", "null", "changeme", "your_api_key", "your-api-key",
    "example", "dummy", "test", "todo", "redacted", "<api_key>", "<token>", "<secret>"
}


class CodeViolation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    rule_id: RuleIdType
    category: str
    severity: SeverityType
    penalty: float = Field(ge=0.0)
    line: int = Field(ge=1)
    symbol: str
    message: str
    recommendation: str


class FileAuditReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    file_path: str
    passed_syntax: bool
    quality_score: float = Field(ge=0.0, le=100.0)
    critical_violations: int = Field(ge=0)
    total_violations: int = Field(ge=0)
    status: Literal["APPROVED", "REJECTED"]
    violations: List[CodeViolation] = Field(default_factory=list)
    deterministic_markers: List[str] = Field(default_factory=list)


class DirectoryAuditSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    root_dir: str
    total_files: int
    approved_files: int
    rejected_files: int
    average_score: float
    overall_status: Literal["APPROVED", "REJECTED"]
    reports: List[FileAuditReport]


class _ASTCodeVisitor(ast.NodeVisitor):
    def __init__(self, max_function_lines: int = 60) -> None:
        self.max_function_lines = max_function_lines
        self.violations: List[CodeViolation] = []
        self._reported_secret_lines: Set[int] = set()

    def _add(
        self,
        rule_id: RuleIdType,
        category: str,
        severity: SeverityType,
        line: int,
        symbol: str,
        message: str,
        recommendation: str,
    ) -> None:
        self.violations.append(
            CodeViolation(
                rule_id=rule_id,
                category=category,
                severity=severity,
                penalty=RULE_PENALTIES[rule_id],
                line=max(1, line),
                symbol=symbol,
                message=message,
                recommendation=recommendation,
            )
        )

    def _is_suspect_secret_literal(self, val: object) -> bool:
        if not isinstance(val, str):
            return False
        stripped = val.strip()
        if len(stripped) < 4:
            return False
        if stripped.lower() in SAFE_PLACEHOLDERS:
            return False
        if stripped.startswith("${") or stripped.startswith("{{"):
            return False
        return True

    def visit_Call(self, node: ast.Call) -> None:
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            base = node.func.value.id if isinstance(node.func.value, ast.Name) else ""
            func_name = f"{base}.{node.func.attr}" if base else node.func.attr

        if func_name in {"eval", "exec", "builtins.eval", "builtins.exec"}:
            self._add(
                "SEC001", "Segurança", "CRÍTICO", node.lineno, func_name,
                f"Chamada perigosa a '{func_name}()' permite execução arbitrária de código.",
                "Substituir por ast.literal_eval() ou parsing estruturado com Pydantic.",
            )

        if func_name in {"os.system", "os.popen"}:
            self._add(
                "SEC002", "Segurança", "CRÍTICO", node.lineno, func_name,
                f"Execução de comando via shell com '{func_name}()'.",
                "Usar subprocess.run([...], shell=False, check=True).",
            )
        elif func_name.startswith("subprocess.") or func_name in {"run", "Popen", "call", "check_call", "check_output"}:
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self._add(
                        "SEC002", "Segurança", "CRÍTICO", node.lineno, func_name,
                        f"Subprocesso '{func_name}' invocado com shell=True.",
                        "Definir shell=False e passar argumentos em lista.",
                    )

        self.generic_visit(node)

    def _check_secret_target_and_value(self, target_name: str, value_node: Optional[ast.AST], line: int) -> None:
        if value_node is None or line in self._reported_secret_lines:
            return
        if isinstance(value_node, ast.Constant) and isinstance(value_node.value, str):
            str_val = value_node.value
            if SECRET_VALUE_SIGNATURES.search(str_val) or (
                SECRET_VAR_REGEX.search(target_name) and self._is_suspect_secret_literal(str_val)
            ):
                self._reported_secret_lines.add(line)
                self._add(
                    "SEC003", "Segurança", "CRÍTICO", line, target_name,
                    f"Suspeita de credencial ou segredo hardcodeado em '{target_name}'.",
                    "Mover credenciais para variáveis de ambiente (.env) via os.getenv().",
                )

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name):
                self._check_secret_target_and_value(target.id, node.value, node.lineno)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name):
            self._check_secret_target_and_value(node.target.id, node.value, node.lineno)
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:
        for k, v in zip(node.keys, node.values):
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                self._check_secret_target_and_value(k.value, v, k.lineno)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, str) and node.lineno not in self._reported_secret_lines:
            if SECRET_VALUE_SIGNATURES.search(node.value):
                self._reported_secret_lines.add(node.lineno)
                self._add(
                    "SEC003", "Segurança", "CRÍTICO", node.lineno, "token_literal",
                    "Padrão de token/chave de API detectado diretamente em literal string.",
                    "Remover o token literal e carregar do ambiente (.env).",
                )
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        effective_body = [
            stmt for stmt in node.body
            if not (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str))
        ]
        is_silent = len(effective_body) > 0 and all(
            isinstance(stmt, (ast.Pass, ast.Continue))
            or (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis)
            for stmt in effective_body
        )

        if node.type is None:
            self._add(
                "ERR001", "Tratamento de Erros", "ALTO", node.lineno, "except:",
                "Captura de exceção genérica nua ('except:' sem classe).",
                "Especifique a exceção exata (ex: except ValueError:).",
            )
        elif isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}:
            self._add(
                "ERR002", "Tratamento de Erros", "MÉDIO", node.lineno, f"except {node.type.id}:",
                f"Captura ampla de '{node.type.id}' pode mascarar bugs inesperados.",
                "Restrinja à exceção específica esperada pelo domínio.",
            )

        if is_silent:
            self._add(
                "ERR003", "Tratamento de Erros", "CRÍTICO", node.lineno, "except: pass",
                "Exceção ignorada silenciosamente com 'pass', '...' ou 'continue'.",
                "Adicionar logging estruturado, tratamento explícito ou relançar o erro.",
            )

        self.generic_visit(node)

    def _inspect_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        all_args = list(node.args.posonlyargs) + list(node.args.args) + list(node.args.kwonlyargs)
        if node.args.vararg:
            all_args.append(node.args.vararg)
        if node.args.kwarg:
            all_args.append(node.args.kwarg)

        for arg in all_args:
            if arg.arg in {"self", "cls"}:
                continue
            if arg.annotation is None:
                self._add(
                    "TYP001", "Tipagem", "MÉDIO", arg.lineno, f"{node.name}({arg.arg})",
                    f"Parâmetro '{arg.arg}' na função '{node.name}' não possui Type Hint.",
                    f"Adicione anotação de tipo explícita ao argumento '{arg.arg}'.",
                )

        if node.name != "__init__" and node.returns is None:
            self._add(
                "TYP002", "Tipagem", "MÉDIO", node.lineno, node.name,
                f"Função '{node.name}' não declara anotação de tipo de retorno (-> Type).",
                f"Declare explicitamente o retorno de '{node.name}' (ex: -> None, -> dict).",
            )

        end_line = getattr(node, "end_lineno", node.lineno) or node.lineno
        span = end_line - node.lineno + 1
        if span > self.max_function_lines:
            self._add(
                "ARCH001", "Arquitetura", "BAIXO", node.lineno, node.name,
                f"Função '{node.name}' possui {span} linhas (limite máximo: {self.max_function_lines}).",
                "Refatorar extraindo subfunções coesas (Princípio SRP).",
            )

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._inspect_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._inspect_function(node)


class CodeAcceptabilityAuditor:
    def __init__(
        self,
        min_quality_score: float = 75.0,
        max_critical_violations: int = 0,
        max_function_lines: int = 60,
    ) -> None:
        self.min_quality_score = min_quality_score
        self.max_critical_violations = max_critical_violations
        self.max_function_lines = max_function_lines

    def audit_code(self, source_code: str, file_path: str = "<memory>") -> FileAuditReport:
        try:
            tree = ast.parse(source_code, filename=file_path)
        except SyntaxError as exc:
            violation = CodeViolation(
                rule_id="SYN001",
                category="Sintaxe",
                severity="CRÍTICO",
                penalty=RULE_PENALTIES["SYN001"],
                line=max(1, exc.lineno or 1),
                symbol="SyntaxError",
                message=f"Erro de sintaxe Python: {exc.msg}",
                recommendation="Corrigir a sintaxe antes de qualquer execução ou commit.",
            )
            return FileAuditReport(
                file_path=file_path,
                passed_syntax=False,
                quality_score=75.0,
                critical_violations=1,
                total_violations=1,
                status="REJECTED",
                violations=[violation],
                deterministic_markers=["[FAIL: SYN001]", "[FAIL: QUALITY_GATE_REJECTED]"],
            )

        visitor = _ASTCodeVisitor(max_function_lines=self.max_function_lines)
        visitor.visit(tree)

        violations = visitor.violations
        total_penalty = sum(v.penalty for v in violations)
        quality_score = round(max(0.0, 100.0 - total_penalty), 2)
        critical_count = sum(1 for v in violations if v.severity == "CRÍTICO")

        approved = (
            critical_count <= self.max_critical_violations
            and quality_score >= self.min_quality_score
        )
        status: Literal["APPROVED", "REJECTED"] = "APPROVED" if approved else "REJECTED"

        markers: List[str] = []
        triggered_rules = sorted({v.rule_id for v in violations})
        for r_id in triggered_rules:
            markers.append(f"[FAIL: {r_id}]")
        if approved:
            markers.append("[PASS]")
        else:
            markers.append("[FAIL: QUALITY_GATE_REJECTED]")

        return FileAuditReport(
            file_path=file_path,
            passed_syntax=True,
            quality_score=quality_score,
            critical_violations=critical_count,
            total_violations=len(violations),
            status=status,
            violations=violations,
            deterministic_markers=markers,
        )

    def audit_file(self, file_path: str | Path) -> FileAuditReport:
        path = Path(file_path)
        source = path.read_text(encoding="utf-8", errors="replace")
        return self.audit_code(source, file_path=str(path))

    def audit_directory(self, dir_path: str | Path) -> DirectoryAuditSummary:
        root = Path(dir_path)
        excluded = {".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache"}
        py_files = [
            p for p in sorted(root.rglob("*.py"))
            if not any(part in excluded for part in p.parts)
        ]
        reports = [self.audit_file(p) for p in py_files]
        total = len(reports)
        approved_count = sum(1 for r in reports if r.status == "APPROVED")
        rejected_count = total - approved_count
        avg_score = round(sum(r.quality_score for r in reports) / total, 2) if total > 0 else 100.0
        overall: Literal["APPROVED", "REJECTED"] = "APPROVED" if rejected_count == 0 else "REJECTED"

        return DirectoryAuditSummary(
            root_dir=str(root),
            total_files=total,
            approved_files=approved_count,
            rejected_files=rejected_count,
            average_score=avg_score,
            overall_status=overall,
            reports=reports,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Code Acceptability Auditor (AST + Pydantic v2)")
    parser.add_argument("--file", type=str, help="Caminho de um arquivo Python específico para auditar")
    parser.add_argument("--dir", type=str, help="Diretório para varredura recursiva de arquivos .py")
    parser.add_argument("--min-score", type=float, default=75.0, help="Quality Score mínimo (padrão: 75.0)")
    parser.add_argument("--json", action="store_true", help="Emitir saída em JSON puro")
    parser.add_argument("--self-test", action="store_true", help="Executar auto-auditoria determinística do motor AST")
    args = parser.parse_args()
    if args.self_test and not args.file and not args.dir:
        args.file = str(Path(__file__).resolve())

    auditor = CodeAcceptabilityAuditor(min_quality_score=args.min_score)

    if args.file:
        report = auditor.audit_file(args.file)
        if args.json:
            print(report.model_dump_json(indent=2))
        else:
            print(f"=== AUDITORIA DE ARQUIVO: {report.file_path} ===")
            print(f"Status: {report.status} | Quality Score: {report.quality_score}/100.0 | Críticas: {report.critical_violations}")
            print(f"Marcadores: {', '.join(report.deterministic_markers)}")
            for v in report.violations:
                print(f" - [L{v.line}] [{v.rule_id}] ({v.severity}, -{v.penalty}): {v.message} -> {v.recommendation}")
        return 0 if report.status == "APPROVED" else 1

    if args.dir:
        summary = auditor.audit_directory(args.dir)
        if args.json:
            print(summary.model_dump_json(indent=2))
        else:
            print(f"=== AUDITORIA DE DIRETÓRIO: {summary.root_dir} ===")
            print(f"Status Geral: {summary.overall_status} | Score Médio: {summary.average_score}/100.0")
            print(f"Arquivos: {summary.total_files} | Aprovados: {summary.approved_files} | Rejeitados: {summary.rejected_files}")
        return 0 if summary.overall_status == "APPROVED" else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
