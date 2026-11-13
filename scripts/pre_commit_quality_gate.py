#!/usr/bin/env python3
"""
pre_commit_quality_gate.py
Gancho determinístico de pré-commit (Esteira de 3 Portões + Governança Zero-Trust):
1. Verifica a presença dos arquivos de governança (.gitignore, .env.example, .geminiignore).
2. Bloqueia qualquer tentativa de commit de arquivos sensíveis (.env, *.pem, *.key, *.pfx).
3. Executa o Portão 1 (code_acceptability_auditor.py, Score >= 75, 0 críticas) nos arquivos .py.
4. Executa o Portão 2 (test_quality_auditor.py, Nível 4 >= 81.0) nos arquivos de teste test_*.py.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
CODE_AUDITOR_DIR = ROOT_DIR / "skills" / "code-acceptability-auditor" / "scripts"
TEST_AUDITOR_DIR = ROOT_DIR / "skills" / "test-quality-auditor" / "scripts"

for p in (str(ROOT_DIR), str(CODE_AUDITOR_DIR), str(TEST_AUDITOR_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from code_acceptability_auditor import CodeAcceptabilityAuditor  # noqa: E402
from test_quality_auditor import audit_test_file  # noqa: E402

FORBIDDEN_STAGED_PATTERNS = (".env", ".pem", ".key", ".pfx", ".p12")
REQUIRED_GOVERNANCE_FILES = (".gitignore", ".env.example", ".geminiignore")


def get_staged_files(repo_root: Path) -> List[Path]:
    """Retorna a lista de arquivos staged no Git (Added, Copied, Modified, Renamed)."""
    try:
        res = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
    except OSError:
        return []
    if res.returncode != 0:
        return []
    files: List[Path] = []
    for line in res.stdout.splitlines():
        clean = line.strip()
        if clean:
            candidate = (repo_root / clean).resolve()
            if candidate.is_file():
                files.append(candidate)
    return files


def check_governance_and_secrets(repo_root: Path, target_files: List[Path]) -> List[str]:
    """Verifica arquivos obrigatórios de governança e bloqueia segredos no stage."""
    errors: List[str] = []
    for req_name in REQUIRED_GOVERNANCE_FILES:
        if not (repo_root / req_name).is_file():
            errors.append(f"[GOV-MISSING] Arquivo obrigatório de governança ausente: {req_name}")

    for fpath in target_files:
        name_low = fpath.name.lower()
        if name_low == ".env" or (name_low.startswith(".env.") and name_low != ".env.example"):
            errors.append(f"[SEC-BLOCK] Tentativa de versionar arquivo de variáveis sensíveis: {fpath.name}")
        elif name_low.endswith(FORBIDDEN_STAGED_PATTERNS):
            errors.append(f"[SEC-BLOCK] Tentativa de versionar chave/certificado privado: {fpath.name}")
    return errors


def _run_skill_and_ecosystem_gates(repo_root: Path, target_files: List[Path], gov_errors: List[str]) -> None:
    """Executa validate_skills em SKILL.md alterados e validate_ecosystem quando rules/hooks/agents mudarem."""
    scripts_dir = repo_root / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from validate_skills import validate_ecosystem, validate_skill_dir

    touched_skills = {
        f.parent for f in target_files
        if f.name == "SKILL.md" and f.parent.parent == repo_root / "skills"
    }
    for s_dir in sorted(touched_skills):
        for err in validate_skill_dir(s_dir):
            gov_errors.append(f"[SKILL-GATE-FAIL] {s_dir.name}: {err}")

    eco_roots = ("rules", "agents", "hooks")
    touches_eco = any(
        f == repo_root / "plugin.json" or any(p in eco_roots for p in f.relative_to(repo_root).parts[:1])
        for f in target_files
        if repo_root in f.parents
    )
    if touches_eco:
        for err in validate_ecosystem(repo_root):
            gov_errors.append(f"[ECO-GATE-FAIL] {err}")


def run_quality_gates(repo_root: Path, target_files: List[Path], min_score: float = 75.0) -> Dict[str, Any]:
    """Executa os Portões 1 (AST), 2 (Test Quality) e 3 (Contratos Skills/Ecosystem) nos arquivos alvo."""
    gov_errors = check_governance_and_secrets(repo_root, target_files)
    _run_skill_and_ecosystem_gates(repo_root, target_files, gov_errors)
    code_auditor = CodeAcceptabilityAuditor(min_quality_score=min_score)
    code_reports: List[Dict[str, Any]] = []
    test_reports: List[Dict[str, Any]] = []

    py_files = [f for f in target_files if f.suffix.lower() == ".py" and f.is_file()]
    for py_file in py_files:
        c_rep = code_auditor.audit_file(py_file)
        code_reports.append({
            "file": py_file.name,
            "score": c_rep.quality_score,
            "critical": c_rep.critical_violations,
            "status": c_rep.status,
        })
        if c_rep.status != "APPROVED":
            gov_errors.append(
                f"[GATE-1-FAIL] {py_file.name} reprovado no CodeAcceptabilityAuditor (score={c_rep.quality_score})"
            )

        if py_file.name.startswith("test_") or py_file.name.endswith("_test.py"):
            source = py_file.read_text(encoding="utf-8", errors="replace")
            t_rep = audit_test_file(source, str(py_file), domain="auto")
            test_reports.append({
                "file": py_file.name,
                "score": t_rep.score_medio,
                "level": t_rep.nivel_espectro,
                "approved": t_rep.aprovado,
            })
            if not t_rep.aprovado:
                gov_errors.append(
                    f"[GATE-2-FAIL] {py_file.name} reprovado no TestQualityAuditor (score={t_rep.score_medio})"
                )

    return {
        "approved": len(gov_errors) == 0,
        "files_checked": len(py_files),
        "governance_errors": gov_errors,
        "gate1_code_reports": code_reports,
        "gate2_test_reports": test_reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Pre-Commit Quality Gate (Franklin Ecosystem)")
    parser.add_argument("--files", nargs="*", default=None, help="Arquivos explícitos para auditar (opcional).")
    parser.add_argument("--min-score", type=float, default=75.0, help="Score mínimo para o Portão 1 AST.")
    args = parser.parse_args()

    if args.files is not None and len(args.files) > 0:
        targets = [Path(p).resolve() for p in args.files if Path(p).is_file()]
    else:
        targets = get_staged_files(ROOT_DIR)
        if not targets:
            targets = [
                ROOT_DIR / "shared" / "polymorphic_skill_envelope.py",
                ROOT_DIR / "tests" / "test_polymorphic_skill_envelope.py",
            ]

    summary = run_quality_gates(ROOT_DIR, targets, min_score=args.min_score)
    sys.stderr.write(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    return 0 if summary["approved"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
