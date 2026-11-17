"""
test_system_project_auditor.py
Deterministic unit and adversarial tests for stack-adaptive auditing in
`system-project-auditor` v6.1.0 (`deterministic_scorer.py` & `project_structure_and_code_auditor.py`).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "system-project-auditor" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import deterministic_scorer  # noqa: E402
import project_structure_and_code_auditor  # noqa: E402


def test_backend_only_scan_scores_clean_code_without_ui_penalties() -> None:
    """Verifies pure Python backend directories pass SGA without UI typography/screen penalties."""
    target = ROOT_DIR / "shared"

    ev, diag = deterministic_scorer.scan_project_tree(target)
    rep = deterministic_scorer.calculate_architecture_score(ev, "SHARED_BACKEND")

    assert diag["has_ui_layer"] is False
    assert diag["stack_profile"] == "backend_only"
    assert ev.has_ui_layer is False
    assert rep.sga_global_score >= 85.0
    assert "APROVADO" in rep.verdict


def test_empty_syntax_error_and_stub_repos_fail_closed(tmp_path: Path) -> None:
    """Adversarial gate: empty directories, SyntaxErrors, and stub-only files must fail closed."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    syn_dir = tmp_path / "syntax_broken"
    syn_dir.mkdir()
    (syn_dir / "bad.py").write_text("def broken(:\n    return 1\n", encoding="utf-8")

    stub_dir = tmp_path / "stub_only"
    stub_dir.mkdir()
    (stub_dir / "stub.py").write_text("def broken() -> None:\n    pass\n", encoding="utf-8")

    for case_dir in (empty_dir, syn_dir, stub_dir):
        ev, diag = deterministic_scorer.scan_project_tree(case_dir)
        rep = deterministic_scorer.calculate_architecture_score(ev, case_dir.name)
        assert diag["has_ui_layer"] is False
        assert rep.sga_global_score < 25.0
        assert rep.tif_verdict == "[FAIL: ALUCINACAO_FUNCIONAL_DO_PROJETO]"


def test_go_packages_and_non_goals_doc_parity(tmp_path: Path) -> None:
    """Verifies Go multi-file package detection, HTTP route exclusion, and Non-Goals parity."""
    (tmp_path / "go.mod").write_text("module example.com/demo\n\ngo 1.24\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_text(".env\nbin/\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# Agents\n`go test ./...` verification baseline.\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "# Demo Go API\nStore implemented in `internal/store/repo.go` serving `api/v1/items`.\n",
        encoding="utf-8",
    )
    (tmp_path / ".context").mkdir()
    (tmp_path / ".context" / "context.md").write_text("# Context\nActive Go store service.\n", encoding="utf-8")
    (tmp_path / ".context" / "spec.md").write_text(
        "# Spec\n## In Scope\n- Store handler\n## Non-Goals\n- Do not create `src/unused.py`\n",
        encoding="utf-8",
    )
    (tmp_path / "cmd" / "api").mkdir(parents=True)
    (tmp_path / "cmd" / "api" / "main.go").write_text(
        'package main\n\nimport "example.com/demo/internal/store"\n\nfunc main() { _ = store.FetchItem("1") }\n',
        encoding="utf-8",
    )
    (tmp_path / "internal" / "store").mkdir(parents=True)
    (tmp_path / "internal" / "store" / "repo.go").write_text(
        'package store\n\nfunc FetchItem(id string) string { return id }\n',
        encoding="utf-8",
    )
    (tmp_path / "internal" / "store" / "models.go").write_text(
        'package store\n\nfunc NewItem() string { return "ok" }\n',
        encoding="utf-8",
    )

    rep = project_structure_and_code_auditor.audit_project_structure_and_code(tmp_path)

    assert rep.verdict == "[PASS]"
    assert rep.orphan_files == []
    assert rep.real_code_metrics["real_functions_count"] >= 2
    assert rep.oklch_and_60_30_10_status["status"] == "[PASS: N/A_BACKEND_ONLY]"
    assert not any(p.classification == "[INEXISTENTE_DOCUMENTADO]" for p in rep.doc_vs_code_parity)


def test_micro_repo_advisory_triad_and_direct_templates_scan(tmp_path: Path) -> None:
    """Verifies standalone micro-CLI advisory Triad status while preserving direct template UI scans."""
    (tmp_path / ".gitignore").write_text(".env\n.venv/\n__pycache__/\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Micro CLI\nRun `uv run python cli.py`.\n", encoding="utf-8")
    (tmp_path / "cli.py").write_text("def run_cli(arg: str) -> str:\n    return arg.strip()\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_cli.py").write_text(
        "from cli import run_cli\n\ndef test_run() -> None:\n    assert run_cli('ok') == 'ok'\n",
        encoding="utf-8",
    )

    rep = project_structure_and_code_auditor.audit_project_structure_and_code(tmp_path)
    ev_tpl, diag_tpl = deterministic_scorer.scan_project_tree(
        ROOT_DIR / "skills" / "system-project-auditor" / "templates"
    )
    rep_tpl = deterministic_scorer.calculate_architecture_score(ev_tpl, "TEMPLATES_UI")

    assert rep.vital_files_status["AGENTS.md"] == "[ADVISORY: OPTIONAL_MICRO_REPO]"
    assert rep.vital_files_status["SPEC.md"] == "[ADVISORY: OPTIONAL_MICRO_REPO]"
    assert rep.verdict == "[PASS]"
    assert diag_tpl["has_ui_layer"] is True
    assert rep_tpl.icte_typography_structure == 100.0
