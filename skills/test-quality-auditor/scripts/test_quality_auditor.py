#!/usr/bin/env python3
"""
test_quality_auditor.py
Orquestrador e CLI do Auditor Determinístico de Qualidade de Testes & Esteira de Evals (v1.2.0).
Suporta 5 domínios modulares (<300 linhas por módulo) espelhados em evals/modules/*_evals.json:
  1. Python (Pytest / Unittest AST) -> python_ast_auditor.py   <-> python_evals.json
  2. TypeScript / JavaScript        -> ts_js_auditor.py        <-> ts_js_evals.json
  3. Go (*_test.go / testing.T)     -> go_test_auditor.py      <-> go_evals.json
  4. MCP (JSON-RPC 2.0 / FastMCP)   -> mcp_test_auditor.py     <-> mcp_evals.json
  5. Harness (Guard / Risk / Evals) -> harness_test_auditor.py <-> harness_evals.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from eval_harness import run_eval_harness as _run_eval_harness
from go_test_auditor import audit_go_test_file
from harness_test_auditor import audit_harness_test_file, enrich_with_harness_audit, is_harness_test_content
from mcp_test_auditor import audit_mcp_test_file, enrich_with_mcp_audit, is_mcp_test_content
from models import AuditIssue, FileAuditReport, TestDossierRecord, classify_quality_level
from python_ast_auditor import TestQualityASTVisitor, audit_python_test_file
from ts_js_auditor import audit_ts_js_test_file

__all__ = [
    "AuditIssue",
    "TestDossierRecord",
    "FileAuditReport",
    "classify_quality_level",
    "TestQualityASTVisitor",
    "audit_python_test_file",
    "audit_ts_js_test_file",
    "audit_go_test_file",
    "audit_mcp_test_file",
    "audit_harness_test_file",
    "audit_test_file",
    "run_eval_harness",
]


def audit_test_file(
    code_str: str,
    filename: str = "test_suite.py",
    domain: str = "auto",
) -> FileAuditReport:
    """Roteia a auditoria para o módulo especialista (Python, TS/JS, Go, MCP, Harness) e enriquece quando auto."""
    dom = domain.lower().strip()
    if dom == "mcp":
        return audit_mcp_test_file(code_str, filename)
    if dom == "harness":
        return audit_harness_test_file(code_str, filename)
    if dom == "go" or filename.endswith(".go"):
        report = audit_go_test_file(code_str, filename)
    elif dom in ("ts", "js", "typescript", "javascript") or filename.endswith((".ts", ".js", ".tsx", ".jsx")):
        report = audit_ts_js_test_file(code_str, filename)
    else:
        report = audit_python_test_file(code_str, filename)

    if dom == "auto":
        if is_mcp_test_content(code_str, filename):
            report = enrich_with_mcp_audit(report, code_str)
        if is_harness_test_content(code_str, filename):
            report = enrich_with_harness_audit(report, code_str)
    return report


def run_eval_harness(skill_root: Path, eval_module: str = "all") -> Dict[str, Any]:
    """Executa o Eval-Driven Harness com despachante multi-domínio e módulos espelhados."""
    return _run_eval_harness(
        skill_root,
        audit_fn=lambda code, fname: audit_test_file(code, fname, domain="auto"),
        eval_module=eval_module,
    )


def format_markdown_report(reports: List[FileAuditReport]) -> str:
    """Formata a lista de relatórios de arquivos em Markdown executivo."""
    total_files = len(reports)
    total_tests = sum(r.total_tests for r in reports)
    total_issues = sum(r.total_inconformidades for r in reports)
    all_scores = [d.score for r in reports for d in r.dossiers]
    global_score = sum(all_scores) / len(all_scores) if all_scores else 100.0
    global_level = classify_quality_level(global_score)
    global_status = "[PASS]" if total_issues == 0 and global_score >= 81.0 else "[FAIL]"

    lines = [
        "# 🛡️ Relatório Determinístico — `test-quality-auditor` (`v1.2.0`)",
        "",
        f"- **Status Global da Suíte:** `{global_status}`",
        f"- **Pontuação Média Global:** `{global_score:.1f}/100` (**{global_level}**)",
        f"- **Arquivos Auditados:** `{total_files}` | **Total de Testes Inspecionados:** `{total_tests}` | **Inconformidades:** `{total_issues}`",
        "",
        "## 📋 Dossiê Individualizado por Teste (Níveis 1 a 4)",
        "",
        "| Arquivo | Domínio | Caso de Teste | Linha | Asserções | Nota | Nível no Espectro | Status | Evidência (`[FATO]`) |",
        "| :--- | :---: | :--- | :---: | :---: | :---: | :--- | :---: | :--- |",
    ]

    for r in reports:
        short_file = Path(r.filename).name
        for d in r.dossiers:
            lines.append(
                f"| `{short_file}` | `{d.domain}` | `{d.test_name}` | L{d.line} | {d.assertion_count} | **{d.score}** | {d.level} | `{d.status}` | {d.evidence} |"
            )

    if total_issues > 0:
        lines.extend(["", "## 🚨 Inconformidades Detectadas pelo Analisador", ""])
        for r in reports:
            for iss in r.issues:
                lines.extend(
                    [
                        f"### `[{iss.id}]` {iss.title} — `{Path(iss.file).name}:L{iss.line}`",
                        f"- **Teste Afetado:** `{iss.test_name}` | **Categoria:** {iss.category} | **Severidade:** {iss.severity} (`-{iss.penalty} pts`)",
                        f"- **Diagnóstico:** {iss.description}",
                        f"- **Correção Recomendada:** {iss.recommendation}",
                        "",
                    ]
                )

    return "\n".join(lines)


def collect_target_files(target: Path) -> List[Path]:
    """Coleta arquivos de teste Python, TS/JS e Go (*_test.go) a partir de um arquivo ou diretório."""
    if target.is_file():
        return [target]
    files: List[Path] = []
    ignored_tokens = (
        ".venv",
        "node_modules",
        ".git",
        "__pycache__",
        "test_quality_auditor.py",
        "python_ast_auditor.py",
        "ts_js_auditor.py",
        "go_test_auditor.py",
        "mcp_test_auditor.py",
        "harness_test_auditor.py",
        "eval_harness.py",
    )
    for p in sorted(target.rglob("*")):
        if not p.is_file():
            continue
        p_str = str(p)
        if any(ignored in p_str for ignored in ignored_tokens):
            continue
        rel_parts = p.relative_to(target).parts if p != target else ()
        if len(rel_parts) >= 2 and rel_parts[0] == "skills":
            continue
        if (
            p.name.startswith("test_")
            or p.name.endswith(("_test.py", "_test.go", ".test.ts", ".test.js", ".spec.ts", ".spec.js"))
            or p.name == "physics_test_runner.py"
        ):
            files.append(p)
    return files


def _build_cli_parser() -> argparse.ArgumentParser:
    """Constrói o parser de argumentos de linha de comando do auditor."""
    parser = argparse.ArgumentParser(
        description="Auditor Determinístico de Qualidade de Testes e Evals (Python, TS/JS, Go, MCP, Harness)."
    )
    parser.add_argument("target", nargs="?", default="", help="Arquivo ou diretório de testes a auditar.")
    parser.add_argument(
        "--domain",
        choices=["auto", "python", "ts", "go", "mcp", "harness"],
        default="auto",
        help="Domínio do módulo de auditoria (padrão: auto).",
    )
    parser.add_argument(
        "--eval-module",
        choices=["all", "python", "ts_js", "go", "mcp", "harness"],
        default="all",
        help="Módulo espelhado de evals a executar com --run-evals (padrão: all).",
    )
    parser.add_argument("--markdown", action="store_true", help="Emite relatório formatado em Markdown.")
    parser.add_argument("--pretty", "--json", action="store_true", help="Formata saída JSON indentada (padrão).")
    parser.add_argument("--run-evals", action="store_true", help="Executa evals/evals.json e evals/modules/*_evals.json.")
    parser.add_argument("--self-test", action="store_true", help="Executa auto-teste rápido da suíte de evals.")
    return parser


def main() -> int:
    parser = _build_cli_parser()
    args = parser.parse_args()
    skill_root = SCRIPT_DIR.parent

    if args.run_evals or args.self_test:
        res = run_eval_harness(skill_root, eval_module=args.eval_module)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0 if res["grading"]["summary"]["failed"] == 0 else 1

    if not args.target:
        parser.print_help()
        return 1

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(json.dumps({"aprovado": False, "error": f"Caminho não encontrado: {target_path}"}, ensure_ascii=False))
        return 1

    files = collect_target_files(target_path)
    reports = [
        audit_test_file(f.read_text(encoding="utf-8", errors="replace"), str(f), domain=args.domain)
        for f in files
    ]

    if args.markdown:
        print(format_markdown_report(reports))
    elif len(reports) == 1:
        print(json.dumps(reports[0].to_dict(), indent=2, ensure_ascii=False))
    else:
        all_passed = all(r.aprovado for r in reports)
        avg_score = round(sum(r.score_medio for r in reports) / len(reports), 1) if reports else 0.0
        print(
            json.dumps(
                {
                    "aprovado_global": all_passed,
                    "score_medio_global": avg_score,
                    "nivel_espectro_global": classify_quality_level(avg_score),
                    "total_arquivos": len(reports),
                    "total_tests": sum(r.total_tests for r in reports),
                    "total_inconformidades": sum(r.total_inconformidades for r in reports),
                    "arquivos": [r.to_dict() for r in reports],
                },
                indent=2,
                ensure_ascii=False,
            )
        )

    return 0 if all(r.aprovado for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
