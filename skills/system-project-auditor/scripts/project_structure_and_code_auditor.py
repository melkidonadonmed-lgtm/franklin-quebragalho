#!/usr/bin/env python3
"""
project_structure_and_code_auditor.py
Deterministic physical layout, polyglot AST (Python, TS/JS, Go), orphan detection,
Docs-vs-Disk parity, and conditional 60-30-10 OKLCH scanner for `system-project-auditor` (v6.1.0).
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
    "htmlcov", "coverage", "site", "_site", ".tox", ".nox",
})
CODE_EXTENSIONS: frozenset[str] = frozenset({".py", ".ts", ".tsx", ".js", ".jsx", ".go"})
STYLE_EXTENSIONS: frozenset[str] = frozenset({".css", ".scss", ".html", ".tsx", ".jsx"})
ENTRYPOINT_STEMS: frozenset[str] = frozenset({
    "server", "main", "index", "app", "__init__", "__main__", "cli", "conftest", "google",
    "page", "layout", "route", "loading", "error", "middleware",
})
VERIFIABLE_DOC_PREFIXES = (
    "src|app|api|cmd|internal|pkg|lib|core|domain|contracts|components|features|services|"
    "shared|scripts|skills|agents|plans|tests|templates|rules|hooks|config"
)
VERIFIABLE_EXTENSIONS: frozenset[str] = frozenset({
    ".py", ".go", ".ts", ".tsx", ".js", ".jsx", ".rs", ".kt", ".kts",
    ".md", ".json", ".yaml", ".yml", ".toml", ".sql", ".ps1", ".sh", ".css", ".scss", ".html", ".proto",
})
NON_PARITY_HEADING_TOKENS = ("non-goals", "out of scope", "roadmap", "deferred")


@dataclass
class DocParityItem:
    reference: str
    classification: str  # [IMPLEMENTED_FUNCTIONAL] | [SUPERFICIAL_MOCK] | [INEXISTENTE_DOCUMENTADO] | [CÓDIGO_FANTASMA]
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
    """Collects non-ignored physical files across the target project."""
    return sorted(
        p for p in root.rglob("*")
        if p.is_file() and not any(part in IGNORED_DIRS for part in p.parts)
    )


def _detect_complexity_level(root: Path, files: List[Path]) -> str:
    """Classifies real physical architecture complexity."""
    rel_paths = {f.relative_to(root).as_posix() for f in files}
    if any("(marketing)" in p or "(workspace)" in p for p in rel_paths):
        return "Nível 3 (Fullstack App Router & PWA)"
    if any(p.startswith("src/features/") for p in rel_paths):
        return "Nível 2 (SPA Modular Feature-Driven)"
    if (root / "server.py").exists() or (root / "skills").is_dir():
        return "Arquitetura Modular MCP / Agent Skills (Poliglota)"
    if any(p.endswith(".go") for p in rel_paths):
        return "Arquitetura Backend / CLI Go"
    return "Nível 1 (Estático / Standalone @layer)"


def _check_vital_files_and_git(
    root: Path, code_files_count: int = 10, has_mcp_or_skills: bool = False
) -> Tuple[Dict[str, str], Dict[str, Any], List[Dict[str, str]]]:
    """Audits vital governance files, .env.example, and .gitignore credential guards."""
    vitals: Dict[str, Tuple[str, ...]] = {
        "README.md": ("README.md",),
        "AGENTS.md": ("AGENTS.md", ".agents/AGENTS.md"),
        "SPEC.md": (".context/spec.md", "SPEC.md"),
        "CONTEXT.md": (".context/context.md", "CONTEXT.md"),
    }
    is_micro_standalone = code_files_count <= 4 and not has_mcp_or_skills and not (root / ".context").is_dir()
    vital_status: Dict[str, str] = {}
    blockers: List[Dict[str, str]] = []
    for key, candidates in vitals.items():
        exists = any((root / c).is_file() and (root / c).stat().st_size > 20 for c in candidates)
        if exists:
            vital_status[key] = "[PASS]"
        elif key != "README.md" and is_micro_standalone:
            vital_status[key] = "[ADVISORY: OPTIONAL_MICRO_REPO]"
        else:
            vital_status[key] = "[ARQUIVO AUSENTE]"
        if key == "README.md" and not exists:
            blockers.append({
                "item": "README.md ausente ou vazio",
                "why": "Impede onboarding, validação de comandos e paridade documental do MVP.",
            })

    gitignore_path = root / ".gitignore"
    gi_text = gitignore_path.read_text(encoding="utf-8", errors="replace") if gitignore_path.exists() else ""
    protects_env = ".env" in gi_text
    protects_deps = any(tok in gi_text for tok in ("node_modules", ".venv", "__pycache__"))
    if not protects_env:
        blockers.append({
            "item": "Proteção .env ausente no .gitignore",
            "why": "Risco crítico de vazamento de chaves e credenciais no controle de versão.",
        })
    git_hygiene = {
        "has_gitignore": gitignore_path.is_file(),
        "ignores_dotenv": protects_env,
        "ignores_dependencies": protects_deps,
        "has_env_example": (root / ".env.example").is_file(),
        "status": "[PASS]" if (gitignore_path.is_file() and protects_env) else "[FAIL: GITIGNORE_INADEQUADO]",
    }
    return vital_status, git_hygiene, blockers


def _collect_abstract_method_ids(tree: ast.AST) -> Set[int]:
    """Returns object ids of methods inside Protocol/ABC classes or marked @abstractmethod."""
    abstract_ids: Set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        base_names = {
            (b.id if isinstance(b, ast.Name) else (b.attr if isinstance(b, ast.Attribute) else ""))
            for b in node.bases
        }
        if not (base_names & {"Protocol", "ABC"}):
            continue
        for stmt in node.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                abstract_ids.add(id(stmt))
    return abstract_ids


def _is_python_stub(node: ast.FunctionDef | ast.AsyncFunctionDef, abstract_ids: Set[int]) -> bool:
    """Checks whether a Python function is an empty stub (Pass/Ellipsis) outside abstract protocols."""
    if id(node) in abstract_ids:
        return False
    for dec in node.decorator_list:
        dec_name = dec.id if isinstance(dec, ast.Name) else (dec.attr if isinstance(dec, ast.Attribute) else "")
        if dec_name == "abstractmethod":
            return False
    body = [
        s for s in node.body
        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))
    ]
    if not body:
        return True
    if len(body) != 1:
        return False
    stmt = body[0]
    return isinstance(stmt, ast.Pass) or (
        isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis
    )


def _inspect_python_ast(text: str, rel: str, is_fixture: bool, metrics: Dict[str, int]) -> None:
    """Updates real-function, stub, and bare-except metrics via Python AST."""
    try:
        tree = ast.parse(text, filename=rel)
    except SyntaxError:
        if not is_fixture:
            metrics["placebo_or_stub_functions"] += 1
        return
    abstract_ids = _collect_abstract_method_ids(tree)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if _is_python_stub(node, abstract_ids) and not is_fixture:
                metrics["placebo_or_stub_functions"] += 1
            else:
                metrics["real_functions_count"] += 1
        elif isinstance(node, ast.ExceptHandler) and node.type is None and not is_fixture:
            metrics["bare_except_count"] += 1


def _inspect_go_source(text: str, is_fixture: bool, metrics: Dict[str, int], imported_go_dirs: Set[str]) -> bool:
    """Parses Go imports, real func declarations, and empty stubs; returns True if package main."""
    for block in re.findall(r"import\s*\((.*?)\)", text, flags=re.DOTALL):
        for imp in re.findall(r'"([^"]+)"', block):
            imported_go_dirs.add(Path(imp).name)
    for imp in re.findall(r'import\s+(?:[A-Za-z_]\w*\s+)?"([^"]+)"', text):
        imported_go_dirs.add(Path(imp).name)

    funcs = re.findall(r"\bfunc\s+(?:\([^)]+\)\s*)?[A-Za-z_]\w*\s*\(", text)
    stubs = re.findall(r"\bfunc\s+(?:\([^)]+\)\s*)?[A-Za-z_]\w*\([^)]*\)[^{]*\{\s*\}", text)
    stub_cnt = 0 if is_fixture else len(stubs)
    metrics["real_functions_count"] += max(0, len(funcs) - len(stubs))
    metrics["placebo_or_stub_functions"] += stub_cnt
    return bool(re.search(r"^\s*package\s+main\b", text, re.MULTILINE))


def _inspect_ts_js_source(text: str, is_fixture: bool, metrics: Dict[str, int]) -> None:
    """Parses JS/TS functions and empty placeholder handlers."""
    fns = re.findall(r"\b(?:function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)", text)
    stubs = [] if is_fixture else re.findall(r"(?:=>\s*\{\s*\}|onClick=\{\(\)\s*=>\s*\{\s*\}\})", text)
    metrics["real_functions_count"] += max(0, len(fns) - len(stubs))
    metrics["placebo_or_stub_functions"] += len(stubs)


def _is_orphan_candidate(rel: str, f: Path) -> bool:
    """Returns True if file should be checked for cross-file import usage."""
    if any(rel.startswith(p) for p in ("tests/", "scripts/", "skills/", "templates/", "hooks/")):
        return False
    if "/tests/" in f"/{rel}" or rel.endswith((".d.ts", ".config.js", ".config.ts", "_test.go")):
        return False
    return f.stem not in ENTRYPOINT_STEMS


def _inspect_real_code_ast(root: Path, files: List[Path]) -> Tuple[Dict[str, int], List[str], Set[str]]:
    """Inspects polyglot source files for real functions, stubs, and true orphan modules."""
    metrics = {"code_files_count": 0, "real_functions_count": 0, "placebo_or_stub_functions": 0, "bare_except_count": 0}
    imported_modules: Set[str] = set()
    imported_go_dirs: Set[str] = set()
    defined_py_js: Dict[str, Path] = {}
    defined_go: List[Tuple[str, Path]] = []

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
        is_fixture = "test" in f.name.lower() or rel.startswith(("tests/", "skills/")) or "/tests/" in f"/{rel}"

        if ext == ".py":
            _inspect_python_ast(text, rel, is_fixture, metrics)
            if _is_orphan_candidate(rel, f):
                defined_py_js[f.stem] = f
        elif ext == ".go":
            is_main = _inspect_go_source(text, is_fixture, metrics, imported_go_dirs)
            if _is_orphan_candidate(rel, f) and not is_main and not rel.startswith("cmd/"):
                defined_go.append((f.parent.name, f))
        else:
            _inspect_ts_js_source(text, is_fixture, metrics)
            if _is_orphan_candidate(rel, f):
                defined_py_js[f.stem] = f

    orphans = [p.relative_to(root).as_posix() for stem, p in defined_py_js.items() if stem not in imported_modules]
    orphans.extend(p.relative_to(root).as_posix() for pkg, p in defined_go if pkg not in imported_go_dirs)
    return metrics, sorted(orphans), imported_modules


def _audit_oklch_and_60_30_10(root: Path, files: List[Path]) -> Dict[str, Any]:
    """Verifies OKLCH, light-dark(), 3-level shadows, and 60-30-10 tokens when real UI files exist."""
    is_franklin_root = (root / "server.py").is_file() or (root / "skills").is_dir()
    skip_dirs = {"docs", "reports", "tests", "fixtures", "testdata"}
    style_files: List[Path] = []
    for f in files:
        if f.suffix.lower() not in STYLE_EXTENSIONS and f.name != "DESIGN.md":
            continue
        rel = f.relative_to(root).as_posix()
        top_dir = rel.split("/", 1)[0]
        if root.name.lower() != "templates" and (
            top_dir in skip_dirs
            or (rel.startswith("skills/") and "/templates/" in f"/{rel}")
            or (is_franklin_root and top_dir == "templates")
        ):
            continue
        style_files.append(f)

    if not style_files:
        return {"applicable": False, "status": "[PASS: N/A_BACKEND_ONLY]"}

    combined = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in style_files).lower()
    has_oklch = "oklch(" in combined
    has_light_dark = "light-dark(" in combined or "data-theme" in combined
    has_3_surfaces = any(k in combined for k in ("--surface-canvas", "--bg-canvas")) and any(
        k in combined for k in ("--surface-card", "--bg-surface-1")
    )
    has_3_shadows = any(
        k in combined
        for k in ("--shadow-elevation-1", "--shadow-elevation-low", "--shadow-layer-sm", "--shadow-tactile-card", "inset 0")
    )
    return {
        "applicable": True,
        "has_oklch_colors": has_oklch,
        "has_light_dark_polarity": has_light_dark,
        "has_60_30_10_surfaces": has_3_surfaces,
        "has_3_layer_shadows": has_3_shadows,
        "status": "[PASS]" if (has_oklch and has_3_surfaces and has_3_shadows) else "[WARN: AJUSTAR_OKLCH_60_30_10]",
    }


def _strip_non_parity_sections(text: str) -> str:
    """Strips fenced code blocks and Non-Goals/Roadmap/Deferred sections before parity checks."""
    no_fences = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    kept_lines: List[str] = []
    skip_level = 0
    for line in no_fences.splitlines():
        heading_m = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if heading_m:
            lvl = len(heading_m.group(1))
            title_low = heading_m.group(2).lower()
            if any(tok in title_low for tok in NON_PARITY_HEADING_TOKENS):
                skip_level = lvl
                continue
            if skip_level and lvl <= skip_level:
                skip_level = 0
        if not skip_level:
            kept_lines.append(line)
    return "\n".join(kept_lines)


def _is_verifiable_repo_path(cand: str) -> bool:
    """Filters out HTTP routes, globs, placeholders, and non-file expressions from doc backticks."""
    if any(ch in cand for ch in ("*", "<", ">", "{", "}", "[", "]", "...", ":")):
        return False
    if re.match(r"^api/v\d+/", cand):
        return False
    return cand.endswith("/") or Path(cand).suffix.lower() in VERIFIABLE_EXTENSIONS


def _cross_check_docs_vs_disk(root: Path, code_metrics: Dict[str, int]) -> List[DocParityItem]:
    """Cross-checks real repository paths documented in README.md and .context/spec.md against disk."""
    parity: List[DocParityItem] = []
    seen_paths: Set[str] = set()
    pattern = rf"`((?:{VERIFIABLE_DOC_PREFIXES})/[a-zA-Z0-9_./\-]+)`"
    for doc_name in ("README.md", ".context/spec.md", "SPEC.md"):
        doc_path = root / doc_name
        if not doc_path.is_file():
            continue
        cleaned = _strip_non_parity_sections(doc_path.read_text(encoding="utf-8", errors="replace"))
        for cand in re.findall(pattern, cleaned):
            if cand in seen_paths or not _is_verifiable_repo_path(cand):
                continue
            seen_paths.add(cand)
            target = root / cand
            skill_matches = list((root / "skills").glob(f"*/{cand}")) if (root / "skills").is_dir() else []
            if target.exists() or skill_matches:
                parity.append(DocParityItem(cand, "[IMPLEMENTED_FUNCTIONAL]", f"Verificado fisicamente em {doc_name} -> {cand}"))
            else:
                parity.append(DocParityItem(cand, "[DOCUMENTED_MISSING]", f"Prometido em {doc_name}, mas ausente no disco: {cand}"))
    if not parity and code_metrics["real_functions_count"] > 0:
        parity.append(DocParityItem("src/", "[IMPLEMENTED_FUNCTIONAL]", f"{code_metrics['real_functions_count']} funções reais verificadas via AST."))
    return parity


def audit_project_structure_and_code(root_path: Path) -> ProjectStructureAuditReport:
    """Executes complete deterministic audit of physical layout, AST code, and documentation parity."""
    root = root_path.resolve()
    files = _collect_project_files(root)
    complexity = _detect_complexity_level(root, files)
    code_metrics, orphans, _ = _inspect_real_code_ast(root, files)
    has_mcp_or_skills = (root / "server.py").is_file() or (root / "skills").is_dir()
    vitals, git_hygiene, blockers = _check_vital_files_and_git(root, code_metrics["code_files_count"], has_mcp_or_skills)
    oklch_status = _audit_oklch_and_60_30_10(root, files)
    parity = _cross_check_docs_vs_disk(root, code_metrics)

    missing_docs = [p for p in parity if p.classification in ("[DOCUMENTED_MISSING]", "[INEXISTENTE_DOCUMENTADO]")]
    for md in missing_docs:
        blockers.append({"item": f"Divergência Documental: {md.reference}", "why": md.evidence})
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
    """Runs deterministic self-test verifying real code vs. documented missing paths."""
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
        assert classifications.get("shared/core.py") == "[IMPLEMENTED_FUNCTIONAL]"
        assert classifications.get("shared/ghost.py") == "[DOCUMENTED_MISSING]"
        assert rep.real_code_metrics["real_functions_count"] == 1

        (root / "README.md").write_text("# Projeto Teste\nMódulo real em `shared/core.py`.\n", encoding="utf-8")
        clean_rep = audit_project_structure_and_code(root)
        assert clean_rep.verdict == "[PASS]"
        assert clean_rep.overall_score == 100.0

    print(json.dumps({"status": "[PASS]", "self_test": "STRUCTURE_AND_CODE_AUDITOR_OK", "score": 100.0}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditor determinístico de estrutura real e código-fonte (v6.1.0).")
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
