#!/usr/bin/env python3
"""
project_structure_and_code_auditor.py
Scanner determinístico de árvore física real, AST de código-fonte, detecção de órfãos,
paridade Documentação (README.md/SPEC.md) vs. Implementação Real e Regra 60-30-10 OKLCH
para a skill unificada `auditoria-projetos-sistema` (v6.0.0).
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Dict, List, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

IGNORED_DIRS: frozenset[str] = frozenset({
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    "dist", "build", ".next", ".pytest_cache", ".mypy_cache", ".ruff_cache",
})
CODE_EXTENSIONS: frozenset[str] = frozenset({".py", ".ts", ".tsx", ".js", ".jsx", ".go"})
STYLE_EXTENSIONS: frozenset[str] = frozenset({".css", ".scss", ".html", ".tsx", ".jsx"})


@dataclass
class DocParityItem:
    reference: str
    classification: str  # [IMPLEMENTADO_FUNCIONAL] | [MOCK_SUPERFICIAL] | [INEXISTENTE_DOCUMENTADO] | [CÓDIGO_FANTASMA]
    evidence: str


@dataclass
class ProjectStructureAuditReport:
    project_root: str
    timestamp: str
    detected_complexity_level: str
    vital_files_status: Dict[str, str]
    git_and_env_hygiene: Dict[str, Any]
    real_code_metrics: Dict[str, int]
    oklch_and_60_30_10_status: Dict[str, Any]
    doc_vs_code_parity: List[DocParityItem] = field(default_factory=list)
    orphan_files: List[str] = field(default_factory=list)
    mvp_blockers: List[Dict[str, str]] = field(default_factory=list)
    overall_score: float = 100.0
    verdict: str = "[PASS]"


def _collect_project_files(root: Path) -> List[Path]:
    """Coleta todos os arquivos reais do projeto ignorando pastas de build/cache."""
    return sorted(
        p for p in root.rglob("*")
        if p.is_file() and not any(part in IGNORED_DIRS for part in p.parts)
    )


def _detect_complexity_level(root: Path, files: List[Path]) -> str:
    """Classifica a estrutura física real nos Níveis 1, 2 ou 3 do Eixo 9 (ou Backend/MCP Poliglota)."""
    rel_paths = {f.relative_to(root).as_posix() for f in files}
    has_app_router_groups = any("(marketing)" in p or "(workspace)" in p for p in rel_paths)
    has_features_dir = any(p.startswith("src/features/") for p in rel_paths)
    has_mcp_or_skills = (root / "server.py").exists() or (root / "skills").is_dir()
    if has_app_router_groups:
        return "Nível 3 (Fullstack App Router & PWA)"
    if has_features_dir:
        return "Nível 2 (SPA Modular Feature-Driven)"
    if has_mcp_or_skills:
        return "Arquitetura Modular MCP / Agent Skills (Poliglota)"
    return "Nível 1 (Estático / Standalone @layer)"


def _check_vital_files_and_git(root: Path) -> Tuple[Dict[str, str], Dict[str, Any], List[Dict[str, str]]]:
    """Audita presença real de arquivos vitais, .env.example e proteção .gitignore."""
    # Tríade v2.0: .context/ é canônico; a raiz fica só como fallback para repositórios legados.
    vitals: Dict[str, Tuple[str, ...]] = {
        "README.md": ("README.md",),
        "AGENTS.md": ("AGENTS.md", ".agents/AGENTS.md"),
        "SPEC.md": (".context/spec.md", "SPEC.md"),
        "CONTEXT.md": (".context/context.md", "CONTEXT.md"),
    }
    vital_status: Dict[str, str] = {}
    blockers: List[Dict[str, str]] = []
    for v, candidates in vitals.items():
        exists = any((root / c).is_file() and (root / c).stat().st_size > 20 for c in candidates)
        vital_status[v] = "[PASS]" if exists else "[ARQUIVO AUSENTE]"
        if v == "README.md" and not exists:
            blockers.append({
                "item": "README.md ausente ou vazio",
                "why": "Impede onboarding, validação de comandos e paridade documental do MVP.",
            })

    gitignore_path = root / ".gitignore"
    gi_text = gitignore_path.read_text(encoding="utf-8", errors="replace") if gitignore_path.exists() else ""
    protects_env = ".env" in gi_text
    protects_deps = any(tok in gi_text for tok in ("node_modules", ".venv", "__pycache__"))
    has_env_example = (root / ".env.example").is_file()
    if not protects_env:
        blockers.append({
            "item": "Proteção .env ausente no .gitignore",
            "why": "Risco crítico de vazamento de chaves e credenciais no controle de versão.",
        })

    git_hygiene = {
        "has_gitignore": gitignore_path.is_file(),
        "ignores_dotenv": protects_env,
        "ignores_dependencies": protects_deps,
        "has_env_example": has_env_example,
        "status": "[PASS]" if (gitignore_path.is_file() and protects_env) else "[FAIL: GITIGNORE_INADEQUADO]",
    }
    return vital_status, git_hygiene, blockers


def _inspect_real_code_ast(root: Path, files: List[Path]) -> Tuple[Dict[str, int], List[str], Set[str]]:
    """Analisa código real (Python AST e TS/JS) para contar funções reais vs. placebos e detectar órfãos."""
    metrics = {
        "code_files_count": 0,
        "real_functions_count": 0,
        "placebo_or_stub_functions": 0,
        "bare_except_count": 0,
    }
    imported_modules: Set[str] = set()
    defined_modules: Dict[str, Path] = {}

    for f in files:
        ext = f.suffix.lower()
        if ext not in CODE_EXTENSIONS:
            continue
        metrics["code_files_count"] += 1
        rel = f.relative_to(root).as_posix()
        text = f.read_text(encoding="utf-8", errors="replace")

        for m in re.findall(r"(?:from|import)\s+([a-zA-Z0-9_.]+)", text):
            imported_modules.add(m.split(".")[-1])
        for m in re.findall(r"from\s+['\"]([^'\"]+)['\"]", text):
            imported_modules.add(Path(m).stem)

        if (
            not any(rel.startswith(p) for p in ("tests/", "scripts/", "skills/", "templates/", "hooks/"))
            and "/tests/" not in f"/{rel}"
            and not rel.endswith((".d.ts", ".config.js", ".config.ts"))
            and f.stem not in {"server", "main", "index", "app", "__init__", "conftest", "google"}
        ):
            defined_modules[f.stem] = f

        is_test_or_auditor_fixture = (
            "test" in f.name.lower()
            or rel.startswith("tests/")
            or "/tests/" in f"/{rel}"
            or rel.startswith("skills/")
        )

        if ext == ".py":
            try:
                tree = ast.parse(text, filename=rel)
            except SyntaxError:
                if not is_test_or_auditor_fixture:
                    metrics["placebo_or_stub_functions"] += 1
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    body = [
                        s for s in node.body
                        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))
                    ]
                    if not body or (len(body) == 1 and isinstance(body[0], ast.Pass)):
                        if not is_test_or_auditor_fixture:
                            metrics["placebo_or_stub_functions"] += 1
                    else:
                        metrics["real_functions_count"] += 1
                elif isinstance(node, ast.ExceptHandler) and node.type is None and not is_test_or_auditor_fixture:
                    metrics["bare_except_count"] += 1
        else:
            fns = re.findall(r"\b(?:function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)", text)
            stubs = re.findall(r"(?:=>\s*\{\s*\}|onClick=\{\(\)\s*=>\s*\{\s*\}\})", text) if not is_test_or_auditor_fixture else []
            metrics["real_functions_count"] += max(0, len(fns) - len(stubs))
            metrics["placebo_or_stub_functions"] += len(stubs)

    orphans = [
        p.relative_to(root).as_posix()
        for stem, p in defined_modules.items()
        if stem not in imported_modules
    ]
    return metrics, orphans, imported_modules


def _audit_oklch_and_60_30_10(root: Path, files: List[Path]) -> Dict[str, Any]:
    """Verifica a presença de tokens OKLCH, light-dark(), sombras em 3 níveis e proporção 60-30-10."""
    style_files = [f for f in files if f.suffix.lower() in STYLE_EXTENSIONS or f.name == "DESIGN.md"]
    if not style_files:
        return {"applicable": False, "status": "[PASS: BACKEND_ONLY]"}

    combined = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in style_files).lower()
    has_oklch = "oklch(" in combined
    has_light_dark = "light-dark(" in combined or "data-theme" in combined
    has_3_surfaces = any(k in combined for k in ("--surface-canvas", "--bg-canvas")) and any(
        k in combined for k in ("--surface-card", "--bg-surface-1")
    )
    has_3_shadows = "--shadow-elevation-1" in combined or "--shadow-tactile-card" in combined or "inset 0" in combined
    return {
        "applicable": True,
        "has_oklch_colors": has_oklch,
        "has_light_dark_polarity": has_light_dark,
        "has_60_30_10_surfaces": has_3_surfaces,
        "has_3_layer_shadows": has_3_shadows,
        "status": "[PASS]" if (has_oklch and has_3_surfaces and has_3_shadows) else "[WARN: AJUSTAR_OKLCH_60_30_10]",
    }


def _cross_check_docs_vs_disk(root: Path, code_metrics: Dict[str, int]) -> List[DocParityItem]:
    """Confronta caminhos citados em README.md e SPEC.md contra os arquivos reais no disco."""
    parity: List[DocParityItem] = []
    seen_paths: Set[str] = set()
    for doc_name in ("README.md", ".context/spec.md", "SPEC.md"):
        doc_path = root / doc_name
        if not doc_path.is_file():
            continue
        text = doc_path.read_text(encoding="utf-8", errors="replace")
        candidates = re.findall(r"`((?:shared|scripts|skills|agents|plans|tests|templates|rules)/[a-zA-Z0-9_./\-]+)`", text)
        for cand in candidates:
            if "*" in cand or "<" in cand or cand in seen_paths:
                continue
            seen_paths.add(cand)
            target = root / cand
            skill_scoped_matches = list((root / "skills").glob(f"*/{cand}")) if (root / "skills").is_dir() else []
            if target.exists() or skill_scoped_matches:
                parity.append(DocParityItem(
                    reference=cand,
                    classification="[IMPLEMENTADO_FUNCIONAL]",
                    evidence=f"Verificado fisicamente em {doc_name} -> {cand}",
                ))
            else:
                parity.append(DocParityItem(
                    reference=cand,
                    classification="[INEXISTENTE_DOCUMENTADO]",
                    evidence=f"Prometido em {doc_name}, mas ausente no disco: {cand}",
                ))
    if not parity and code_metrics["real_functions_count"] > 0:
        parity.append(DocParityItem(
            reference="src/",
            classification="[IMPLEMENTADO_FUNCIONAL]",
            evidence=f"{code_metrics['real_functions_count']} funções reais verificadas via AST.",
        ))
    return parity


def audit_project_structure_and_code(root_path: Path) -> ProjectStructureAuditReport:
    """Executa a auditoria determinística completa de estrutura física, código real e documentação."""
    root = root_path.resolve()
    files = _collect_project_files(root)
    complexity = _detect_complexity_level(root, files)
    vitals, git_hygiene, blockers = _check_vital_files_and_git(root)
    code_metrics, orphans, _ = _inspect_real_code_ast(root, files)
    oklch_status = _audit_oklch_and_60_30_10(root, files)
    parity = _cross_check_docs_vs_disk(root, code_metrics)

    missing_docs = [p for p in parity if p.classification == "[INEXISTENTE_DOCUMENTADO]"]
    for md in missing_docs:
        blockers.append({
            "item": f"Divergência Documental: {md.reference}",
            "why": md.evidence,
        })
    if code_metrics["placebo_or_stub_functions"] > 0:
        blockers.append({
            "item": f"{code_metrics['placebo_or_stub_functions']} funções placebo/vazias detectadas",
            "why": "Viola a diretriz de Engenharia Real-State (Tolerância Zero a Funções Falsas).",
        })

    penalties = (
        (len(missing_docs) * 10.0)
        + (code_metrics["placebo_or_stub_functions"] * 8.0)
        + (code_metrics["bare_except_count"] * 5.0)
        + (len(orphans) * 4.0)
        + (0.0 if git_hygiene["status"] == "[PASS]" else 15.0)
    )
    score = round(max(0.0, 100.0 - penalties), 2)
    verdict = "[PASS]" if (score >= 80.0 and not missing_docs) else "[FAIL]"

    return ProjectStructureAuditReport(
        project_root=root.as_posix(),
        timestamp=datetime.now(timezone.utc).isoformat(),
        detected_complexity_level=complexity,
        vital_files_status=vitals,
        git_and_env_hygiene=git_hygiene,
        real_code_metrics=code_metrics,
        oklch_and_60_30_10_status=oklch_status,
        doc_vs_code_parity=parity[:25],
        orphan_files=orphans,
        mvp_blockers=blockers,
        overall_score=score,
        verdict=verdict,
    )


def run_self_test() -> int:
    """Executa auto-teste determinístico validando detecção de código real vs. inexistente."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".gitignore").write_text(".env\n.venv/\nnode_modules/\n", encoding="utf-8")
        (root / ".env.example").write_text("GEMINI_MODEL=\n", encoding="utf-8")
        (root / "README.md").write_text(
            "# Projeto Teste\nMódulo real em `shared/core.py` e fantasma em `shared/ghost.py`.\n",
            encoding="utf-8",
        )
        (root / "AGENTS.md").write_text("# Agents\nComandos executáveis de verificação.\n", encoding="utf-8")
        (root / ".context").mkdir()
        (root / ".context" / "spec.md").write_text("# Spec\nContratos de sistema validados.\n", encoding="utf-8")
        (root / ".context" / "context.md").write_text("# Context\nEstado atual do projeto.\n", encoding="utf-8")
        (root / "shared").mkdir()
        (root / "shared" / "core.py").write_text(
            "def compute_total(x: int, y: int) -> int:\n    return x + y\n",
            encoding="utf-8",
        )
        (root / "server.py").write_text("from shared.core import compute_total\n", encoding="utf-8")

        rep = audit_project_structure_and_code(root)
        classifications = {p.reference: p.classification for p in rep.doc_vs_code_parity}
        assert classifications.get("shared/core.py") == "[IMPLEMENTADO_FUNCIONAL]"
        assert classifications.get("shared/ghost.py") == "[INEXISTENTE_DOCUMENTADO]"
        assert rep.real_code_metrics["real_functions_count"] == 1

        # Corrige o README removendo o caminho fantasma -> deve aprovar com 100.0
        (root / "README.md").write_text("# Projeto Teste\nMódulo real em `shared/core.py`.\n", encoding="utf-8")
        clean_rep = audit_project_structure_and_code(root)
        assert clean_rep.verdict == "[PASS]"
        assert clean_rep.overall_score == 100.0

    print(json.dumps({"status": "[PASS]", "self_test": "STRUCTURE_AND_CODE_AUDITOR_OK", "score": 100.0}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditor determinístico de estrutura real e código-fonte.")
    parser.add_argument("--target", type=str, default=".", help="Diretório raiz do projeto a auditar.")
    parser.add_argument("--self-test", action="store_true", help="Executa auto-teste determinístico.")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    report = audit_project_structure_and_code(Path(args.target))
    print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
    return 0 if report.verdict == "[PASS]" else 1


if __name__ == "__main__":
    sys.exit(main())
