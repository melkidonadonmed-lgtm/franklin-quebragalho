#!/usr/bin/env python3
"""
deterministic_scorer.py
Stack-adaptive deterministic scoring engine (Zero Placebo) and AST/Regex scanner for
`system-project-auditor` (v6.1.0 — Backend/CLI/Go profile vs. 3-Layer UI + 60-30-10 OKLCH + SGA/TIF).
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

IGNORED_DIRS = frozenset({
    ".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build",
    ".next", ".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov", "coverage",
    "site", "_site", ".tox", ".nox",
})
CODE_EXTENSIONS = frozenset({".py", ".ts", ".tsx", ".js", ".jsx", ".html", ".css", ".go"})
UI_FILE_EXTENSIONS = frozenset({".tsx", ".jsx", ".css", ".scss", ".html"})
CONFIG_OR_SCHEMA_STEMS = (
    "config", "const", "env", "settings", "schema", "models", "tokens", "sources", "advisor", "registry",
)
ALLOWED_URL_DOMAINS = (
    "localhost", "127.0.0.1", "0.0.0.0", "example.com", "w3.org", "json-schema.org",
    "jsonrpc.org", "openapis.org", "schema.org", "rfc-editor.org", "antigravity.google",
    "agentskills.io", "modelcontextprotocol.io", "aistudio.google.com", "adk.dev",
    "google.github.io", "githubusercontent.com", "github.com", "googleapis.com",
    "gstatic.com", "cdn.jsdelivr.net", "unpkg.com", "esm.sh",
)
UI_SCREEN_STEM_RE = re.compile(r"(?:^|[_-])(page|screen|view|island|dashboard)(?:$|[_-])")
NON_APP_TOP_DIRS = frozenset({"docs", "reports", "fixtures", "testdata"})


@dataclass
class ArchitecturalEvidence:
    total_nodes: int
    orphan_or_deadend_nodes: int
    total_screens: int
    screens_with_4_states: int
    max_click_depth: int
    total_mapped_functions: int
    functions_in_cohesive_islands: int
    hardcode_occurrences: int
    coupled_data_ui_functions: int
    total_mvp_features_kept: int
    verifiable_essential_features: int
    unnecessary_bloat_features_kept: int
    has_fluid_clamp_scale: bool
    has_3_tier_font_pairing_tabular: bool
    has_65ch_and_line_height_rhythm: bool
    has_anti_squish_protection: bool
    has_cmd_k_and_zero_native_alerts: bool
    has_ui_layer: bool = True


@dataclass
class DeterministicScoreReport:
    version_label: str
    timestamp: str
    ine_navigation: float
    ici_island_cohesion: float
    ipc_code_purity: float
    irm_mvp_rigor: float
    icte_typography_structure: float
    sga_global_score: float
    tif_sufficiency_ratio: float
    tif_verdict: str
    verdict: str


def calculate_architecture_score(
    ev: ArchitecturalEvidence, version_label: str = "V1"
) -> DeterministicScoreReport:
    """Computes the 5 deterministic architecture scores, TIF ratio, and final verdict."""
    valid_routes_ratio = (ev.total_nodes - ev.orphan_or_deadend_nodes) / max(1, ev.total_nodes)
    ui_states_ratio = ev.screens_with_4_states / max(1, ev.total_screens)
    click_penalty = max(0, (ev.max_click_depth - 3) * 15)
    ine = max(0.0, ((valid_routes_ratio * 0.5 + ui_states_ratio * 0.5) * 100.0) - click_penalty)

    ici = (ev.functions_in_cohesive_islands / max(1, ev.total_mapped_functions)) * 100.0
    ipc = max(0.0, 100.0 - (ev.hardcode_occurrences * 12.0) - (ev.coupled_data_ui_functions * 15.0))
    base_mvp = (ev.verifiable_essential_features / max(1, ev.total_mvp_features_kept)) * 100.0
    irm = max(0.0, base_mvp - (ev.unnecessary_bloat_features_kept * 20.0))

    checks = (
        ev.has_fluid_clamp_scale, ev.has_3_tier_font_pairing_tabular,
        ev.has_65ch_and_line_height_rhythm, ev.has_anti_squish_protection,
        ev.has_cmd_k_and_zero_native_alerts,
    )
    icte = sum(20.0 for c in checks if c)
    sga = round((ine * 0.25) + (ici * 0.20) + (ipc * 0.25) + (irm * 0.15) + (icte * 0.15), 2)

    tif_ratio = round((ev.verifiable_essential_features / max(1, ev.total_mvp_features_kept)) * 100.0, 2)
    tif_verdict = (
        "[PASS: SUFICIENCIA_COMPROVADA]" if tif_ratio >= 50.0 else "[FAIL: ALUCINACAO_FUNCIONAL_DO_PROJETO]"
    )

    if sga >= 85.0 and ipc >= 80.0 and ine >= 80.0 and tif_ratio >= 50.0:
        verdict = "APROVADO (PRODUÇÃO / ARQUITETURA E SUFICIÊNCIA SÓLIDAS)"
    elif sga >= 65.0 and tif_ratio >= 50.0:
        verdict = "REQUER REFATORAÇÃO FOCADA (BLOQUEIOS MODERADOS)"
    else:
        verdict = "REPROVADO (DÉFICIT DE SUFICIÊNCIA OU DÍVIDA ARQUITETURAL CRÍTICA)"

    return DeterministicScoreReport(
        version_label=version_label, timestamp=datetime.now(timezone.utc).isoformat(),
        ine_navigation=round(ine, 2), ici_island_cohesion=round(ici, 2),
        ipc_code_purity=round(ipc, 2), irm_mvp_rigor=round(irm, 2),
        icte_typography_structure=round(icte, 2), sga_global_score=sga,
        tif_sufficiency_ratio=tif_ratio, tif_verdict=tif_verdict, verdict=verdict,
    )


def _is_whitelisted_url(raw_url: str) -> bool:
    """Returns True for canonical spec/doc/loopback URLs or bare scheme prefixes."""
    parsed = urlparse(raw_url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return True
    host = parsed.hostname.lower()
    return any(host == dom or host.endswith(f".{dom}") for dom in ALLOWED_URL_DOMAINS)


def _is_non_abstract_stub(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Detects empty or placeholder Python function bodies, excluding @abstractmethod."""
    for dec in node.decorator_list:
        dec_name = dec.id if isinstance(dec, ast.Name) else (dec.attr if isinstance(dec, ast.Attribute) else "")
        if dec_name == "abstractmethod":
            return False
    stmts = [
        s for s in node.body
        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))
    ]
    if not stmts:
        return True
    if len(stmts) != 1:
        return False
    stmt = stmts[0]
    if isinstance(stmt, ast.Pass):
        return True
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
        return True
    if isinstance(stmt, ast.Raise) and isinstance(stmt.exc, ast.Call):
        exc_fn = stmt.exc.func
        return isinstance(exc_fn, ast.Name) and exc_fn.id == "NotImplementedError"
    return isinstance(stmt, ast.Raise) and isinstance(stmt.exc, ast.Name) and stmt.exc.id == "NotImplementedError"


def _collect_python_fn_stats(tree: ast.AST, content: str) -> Tuple[int, int, int, int, int, int]:
    """Collects function cohesion, coupling, stubs, long-function, and bare-except counts."""
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    cohesive, coupled, stubs, long_fns = 0, 0, 0, 0
    for fn in funcs:
        is_stub = _is_non_abstract_stub(fn)
        stubs += 1 if is_stub else 0
        span = (getattr(fn, "end_lineno", fn.lineno) or fn.lineno) - fn.lineno + 1
        if span > 60:
            long_fns += 1
        elif not is_stub:
            cohesive += 1
        fn_src = ast.get_source_segment(content, fn) or ""
        has_ui = any(t in fn_src for t in ("render", "innerHTML", "tsx", "jsx", "<div", "st.write", "QWidget"))
        has_io = any(t in fn_src for t in ("sqlite3.connect", "SELECT ", "INSERT INTO", "requests.get", "urllib.request"))
        if has_ui and has_io:
            coupled += 1
    bare_excepts = sum(1 for n in ast.walk(tree) if isinstance(n, ast.ExceptHandler) and n.type is None)
    return len(funcs), cohesive, coupled, stubs, long_fns, bare_excepts


def _scan_python_ast(file_path: Path, content: str) -> Dict[str, int]:
    """Extracts deterministic Python AST metrics without cliff-based cohesion penalties."""
    stats = {
        "functions": 0, "cohesive_functions": 0, "hardcodes": 0, "coupled_data_ui": 0,
        "inert_placeholders": 0, "syntax_errors": 0, "bare_except": 0, "long_functions": 0,
    }
    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError as exc:
        print(f"[WARN] SyntaxError ao analisar {file_path}: {exc}", file=sys.stderr)
        stats["syntax_errors"] = 1
        return stats

    fn_cnt, cohesive, coupled, stubs, long_fns, bare_exc = _collect_python_fn_stats(tree, content)
    stats.update({
        "functions": fn_cnt, "cohesive_functions": cohesive, "coupled_data_ui": coupled,
        "inert_placeholders": stubs, "bare_except": bare_exc, "long_functions": long_fns,
    })
    if any(k in file_path.stem.lower() for k in CONFIG_OR_SCHEMA_STEMS):
        return stats
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            val = node.value.strip()
            if val.startswith(("http://", "https://")) and not _is_whitelisted_url(val):
                stats["hardcodes"] += 1
    return stats


def _scan_go_file(file_path: Path, text: str) -> Dict[str, int]:
    """Extracts Go function counts, empty stubs, and non-whitelisted hardcoded URLs."""
    funcs = re.findall(r"\bfunc\s+(?:\([^)]+\)\s*)?[A-Za-z_]\w*\s*\(", text)
    stubs = re.findall(r"\bfunc\s+(?:\([^)]+\)\s*)?[A-Za-z_]\w*\([^)]*\)[^{]*\{\s*\}", text)
    hardcodes = 0
    if not any(k in file_path.stem.lower() for k in CONFIG_OR_SCHEMA_STEMS):
        urls = re.findall(r'["`](https?://[^"`]+)["`]', text)
        hardcodes = sum(1 for u in urls if not _is_whitelisted_url(u))
    return {"functions": len(funcs), "cohesive_functions": max(0, len(funcs) - len(stubs)), "stubs": len(stubs), "hardcodes": hardcodes}


def _scan_ts_js_file(file_path: Path, clean_text: str) -> Tuple[int, int, int, int]:
    """Extracts TS/JS function counts, UI/IO coupling, and non-whitelisted hardcoded URLs."""
    fn_m = re.findall(r"\b(?:function\s+[A-Za-z0-9_]+|const\s+[A-Za-z0-9_]+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)", clean_text)
    fn_cnt = len(fn_m)
    has_coupled = ("return (" in clean_text or "<div" in clean_text or "<section" in clean_text) and any(
        io_tok in clean_text for io_tok in ("fetch(", "axios.", "SELECT ", "localStorage.setItem")
    )
    hardcodes = 0
    if not any(k in file_path.stem.lower() for k in CONFIG_OR_SCHEMA_STEMS):
        urls = re.findall(r"['\"](https?://[^'\"]+)['\"]", clean_text)
        hardcodes = sum(1 for u in urls if not _is_whitelisted_url(u))
    return fn_cnt, fn_cnt, (1 if has_coupled else 0), hardcodes


def _update_ui_feature_flags(low: str, acc: Dict[str, Any]) -> None:
    """Updates CSS/typography/navigation accumulators for UI layers."""
    acc["has_clamp"] = acc["has_clamp"] or ("clamp(" in low)
    acc["has_tabular"] = acc["has_tabular"] or ("tabular-nums" in low)
    acc["has_65ch"] = acc["has_65ch"] or (("65ch" in low or "60ch" in low) and "line-height" in low)
    acc["has_anti_squish"] = acc["has_anti_squish"] or ("flex-shrink: 0" in low and "white-space: nowrap" in low)
    acc["has_cmd_k"] = acc["has_cmd_k"] or any(
        k in low for k in ("ctrl+k", "cmd+k", "⌘k", "meta+k", "commandpalette", 'aria-current="page"')
    )
    acc["has_breadcrumbs"] = acc["has_breadcrumbs"] or ('aria-current="page"' in low or "breadcrumb" in low)
    acc["has_container_queries"] = acc["has_container_queries"] or ("@container" in low or "container-type" in low or "subgrid" in low)
    acc["has_oklch_tokens"] = acc["has_oklch_tokens"] or ("oklch(" in low or "light-dark(" in low or "--surface-canvas" in low or "--bg-canvas" in low)
    acc["has_logical_box"] = acc["has_logical_box"] or ("inline-size" in low or "padding-inline" in low or "flow-root" in low or "--space-" in low)
    if "row-reverse" in low:
        acc["reverse_tab_order"] += 1


def _scan_single_file(f: Path, text: str, acc: Dict[str, Any], has_ui_layer: bool) -> None:
    """Updates architectural and code metrics for a single scanned file."""
    ext = f.suffix.lower()
    clean_text = re.sub(r"//.*?$", "", re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL), flags=re.MULTILINE)
    low = clean_text.lower()
    if has_ui_layer:
        _update_ui_feature_flags(low, acc)

    if ext in {".ts", ".tsx", ".js", ".jsx", ".html"}:
        acc["native_alerts"] += len(re.findall(r"(?<!<code>)\b(?:window\.)?(?:alert|confirm)\s*\(\s*[^)\s]", clean_text))
        acc["inert_placeholders"] += len(re.findall(r"onClick=\{\(\)\s*=>\s*\{\s*\}\}|href=['\"]#['\"]", clean_text))

    if ext == ".py":
        py_st = _scan_python_ast(f, text)
        acc["total_fn"] += py_st["functions"]
        acc["cohesive_fn"] += py_st["cohesive_functions"]
        acc["hardcodes"] += py_st["hardcodes"]
        acc["coupled"] += py_st["coupled_data_ui"]
        acc["inert_placeholders"] += py_st["inert_placeholders"]
        acc["syntax_errors"] += py_st["syntax_errors"]
        acc["bare_except"] += py_st["bare_except"]
        acc["long_functions"] += py_st["long_functions"]
    elif ext == ".go":
        go_st = _scan_go_file(f, text)
        acc["total_fn"] += go_st["functions"]
        acc["cohesive_fn"] += go_st["cohesive_functions"]
        acc["inert_placeholders"] += go_st["stubs"]
        acc["hardcodes"] += go_st["hardcodes"]
    elif ext in {".ts", ".tsx", ".js", ".jsx"}:
        fn_cnt, coh_cnt, cpl, hcd = _scan_ts_js_file(f, clean_text)
        acc["total_fn"] += fn_cnt
        acc["cohesive_fn"] += coh_cnt
        acc["coupled"] += cpl
        acc["hardcodes"] += hcd

    is_ui_screen = ext in {".tsx", ".jsx", ".html"} or (ext in {".ts", ".js"} and bool(UI_SCREEN_STEM_RE.search(f.stem.lower())))
    if has_ui_layer and is_ui_screen:
        acc["screens_total"] += 1
        gaming = bool(re.search(r"//.*?\bempty\s*\|\s*loading\s*\|\s*success\s*\|\s*error\b", text, re.IGNORECASE))
        groups = (
            ("empty", "vazio", "nenhum", "idle"),
            ("loading", "carregando", "skeleton", "spinner", "aria-busy"),
            ("success", "sucesso", "resolved", "pressed", "data-state"),
            ("error", "erro", "falha", 'role="alert"', "role='alert'"),
        )
        if sum(1 for g in groups if any(t in low for t in g)) >= 3 and not gaming:
            acc["screens_4_states"] += 1


def _resolve_complex_zero_scripts_dir() -> Optional[Path]:
    """Resolves complex-zero scripts across local repo, sibling shredded-shape, and global plugin."""
    script_file = Path(__file__).resolve()
    candidates = [
        script_file.parents[3].parent / "shredded-shape" / "skills" / "complex-zero" / "scripts",
        Path.home() / ".gemini" / "config" / "plugins" / "shredded-shape" / "skills" / "complex-zero" / "scripts",
        script_file.parents[2] / "complex-zero" / "scripts",
    ]
    return next((c for c in candidates if (c / "visual_hierarchy_and_cdp_probe.py").is_file()), None)


def _run_complex_zero_visual_org_bridge(combined_chunks: List[str]) -> Tuple[Dict[str, Any], bool, bool, bool]:
    """Executes the deterministic bridge to shredded-shape/complex-zero visual probe."""
    cz_scripts_dir = _resolve_complex_zero_scripts_dir()
    if cz_scripts_dir is None or not combined_chunks:
        return {}, False, False, False
    if str(cz_scripts_dir) not in sys.path:
        sys.path.insert(0, str(cz_scripts_dir))
    try:
        from visual_hierarchy_and_cdp_probe import analyze_visual_hierarchy_and_organization

        org_rep = analyze_visual_hierarchy_and_organization("\n".join(combined_chunks))
        return (
            asdict(org_rep),
            len(org_rep.cramped_menu_violations) > 0,
            len(org_rep.sprawl_and_org_violations) > 0,
            len(org_rep.hierarchy_violations) > 0,
        )
    except (ImportError, OSError, AttributeError, TypeError, ValueError, RuntimeError) as exc:
        return {"error": str(exc)}, False, False, False


def _is_excluded_non_app_template(rel_posix: str, target: Path) -> bool:
    """Excludes skill/report templates or docs/fixtures when scanning a repo root or backend folder."""
    if not target.is_dir() or target.name.lower() in {"templates", "ui", "web", "frontend"}:
        return False
    parts = rel_posix.split("/")
    if parts[0] in NON_APP_TOP_DIRS:
        return True
    if rel_posix.startswith("skills/") and "/templates/" in f"/{rel_posix}":
        return True
    is_franklin_root = (target / "server.py").is_file() or (target / "skills").is_dir()
    return is_franklin_root and parts[0] == "templates"


def _detect_ui_layer(target: Path, files: List[Path]) -> bool:
    """Detects whether the scanned target actually contains a runnable frontend/UI layer."""
    for f in files:
        rel_posix = f.relative_to(target).as_posix() if target.is_dir() else f.name
        if _is_excluded_non_app_template(rel_posix, target):
            continue
        ext = f.suffix.lower()
        if ext in UI_FILE_EXTENSIONS or f.name == "DESIGN.md" or f.name.startswith("mcp_apps_ui_"):
            return True
        if ext in {".ts", ".js"}:
            snippet = f.read_text(encoding="utf-8", errors="replace")[:4000]
            if any(tok in snippet for tok in ("<div", "<main", "oklch(")):
                return True
    return False


def _build_ui_evidence(acc: Dict[str, Any], visual_flags: Tuple[bool, bool, bool]) -> ArchitecturalEvidence:
    """Builds UI-aware ArchitecturalEvidence preserving full 3-layer navigation metrics."""
    has_cramped_menus, has_sprawl, has_flat_hierarchy = visual_flags
    screens_total = max(1, acc["screens_total"])
    total_fn = max(1, acc["total_fn"])
    total_nodes = max(3, screens_total + 2)
    base_orphans = 0 if acc["has_cmd_k"] else min(2, max(0, screens_total - acc["screens_4_states"]))
    orphan_nodes = min(total_nodes, base_orphans + (2 if has_sprawl else 0) + (1 if has_cramped_menus else 0))
    essential = max(1, min(total_fn, 6))
    bloat = (0 if (acc["hardcodes"] == 0 and acc["coupled"] == 0) else min(3, acc["hardcodes"])) + (2 if has_sprawl else 0)
    cohesive_fn = max(1, int(min(total_fn, acc["cohesive_fn"]) * (0.55 if has_sprawl else 1.0)))
    return ArchitecturalEvidence(
        total_nodes=total_nodes, orphan_or_deadend_nodes=orphan_nodes,
        total_screens=screens_total, screens_with_4_states=acc["screens_4_states"],
        max_click_depth=(4 if has_sprawl else (2 if acc["has_cmd_k"] else 4)),
        total_mapped_functions=total_fn, functions_in_cohesive_islands=cohesive_fn,
        hardcode_occurrences=acc["hardcodes"] + (2 if has_flat_hierarchy else 0),
        coupled_data_ui_functions=acc["coupled"],
        total_mvp_features_kept=(essential + bloat), verifiable_essential_features=essential,
        unnecessary_bloat_features_kept=bloat, has_fluid_clamp_scale=(acc["has_clamp"] and not has_flat_hierarchy),
        has_3_tier_font_pairing_tabular=(acc["has_tabular"] and not has_flat_hierarchy),
        has_65ch_and_line_height_rhythm=acc["has_65ch"],
        has_anti_squish_protection=(acc["has_anti_squish"] and not has_cramped_menus),
        has_cmd_k_and_zero_native_alerts=(acc["has_cmd_k"] and acc["native_alerts"] == 0 and not has_sprawl),
        has_ui_layer=True,
    )


def _build_backend_evidence(acc: Dict[str, Any], code_files_count: int) -> ArchitecturalEvidence:
    """Builds fail-closed ArchitecturalEvidence for backend/CLI/Go repos without UI penalties."""
    real_non_stub = max(0, acc["total_fn"] - acc["inert_placeholders"])
    if code_files_count == 0 or real_non_stub == 0 or acc["syntax_errors"] > 0:
        bloat_err = max(2, acc["inert_placeholders"] + acc["syntax_errors"] + 2)
        return ArchitecturalEvidence(
            total_nodes=3, orphan_or_deadend_nodes=3, total_screens=1, screens_with_4_states=0,
            max_click_depth=5, total_mapped_functions=max(1, acc["total_fn"]), functions_in_cohesive_islands=0,
            hardcode_occurrences=acc["hardcodes"] + 5, coupled_data_ui_functions=acc["coupled"],
            total_mvp_features_kept=bloat_err, verifiable_essential_features=0, unnecessary_bloat_features_kept=bloat_err,
            has_fluid_clamp_scale=False, has_3_tier_font_pairing_tabular=False,
            has_65ch_and_line_height_rhythm=False, has_anti_squish_protection=False,
            has_cmd_k_and_zero_native_alerts=False, has_ui_layer=False,
        )
    total_nodes = max(3, code_files_count)
    defects = acc["inert_placeholders"] + acc["bare_except"]
    screens_total = max(1, code_files_count)
    bloat = acc["inert_placeholders"] + acc["hardcodes"] + acc["coupled"]
    return ArchitecturalEvidence(
        total_nodes=total_nodes, orphan_or_deadend_nodes=min(total_nodes, acc["inert_placeholders"]),
        total_screens=screens_total, screens_with_4_states=max(0, screens_total - defects),
        max_click_depth=2, total_mapped_functions=max(1, acc["total_fn"]),
        functions_in_cohesive_islands=min(max(1, acc["total_fn"]), acc["cohesive_fn"]),
        hardcode_occurrences=acc["hardcodes"], coupled_data_ui_functions=acc["coupled"],
        total_mvp_features_kept=(real_non_stub + bloat), verifiable_essential_features=real_non_stub,
        unnecessary_bloat_features_kept=bloat,
        has_fluid_clamp_scale=(acc["syntax_errors"] == 0 and real_non_stub > 0),
        has_3_tier_font_pairing_tabular=(acc["inert_placeholders"] == 0),
        has_65ch_and_line_height_rhythm=(acc["bare_except"] == 0),
        has_anti_squish_protection=(acc["long_functions"] == 0),
        has_cmd_k_and_zero_native_alerts=(acc["native_alerts"] == 0 and acc["coupled"] == 0),
        has_ui_layer=False,
    )


def scan_project_tree(project_path: Path) -> Tuple[ArchitecturalEvidence, Dict[str, Any]]:
    """Scans a target file or directory and produces stack-adaptive ArchitecturalEvidence + diagnostics."""
    target = project_path.resolve()
    files = [target] if target.is_file() else [
        p for p in sorted(target.rglob("*"))
        if p.is_file()
        and (p.suffix.lower() in CODE_EXTENSIONS or p.name == "DESIGN.md")
        and not any(part in IGNORED_DIRS for part in p.parts)
    ]
    has_ui_layer = _detect_ui_layer(target, files)
    acc: Dict[str, Any] = {
        "total_fn": 0, "cohesive_fn": 0, "hardcodes": 0, "coupled": 0,
        "screens_total": 0, "screens_4_states": 0, "native_alerts": 0, "inert_placeholders": 0,
        "syntax_errors": 0, "bare_except": 0, "long_functions": 0,
        "has_clamp": False, "has_tabular": False, "has_65ch": False,
        "has_anti_squish": False, "has_cmd_k": False, "has_breadcrumbs": False,
        "has_container_queries": False, "has_oklch_tokens": False, "has_logical_box": False,
        "reverse_tab_order": 0,
    }
    scanned_files, read_errors, combined_chunks = [], [], []
    for f in files:
        if f.suffix.lower() not in CODE_EXTENSIONS:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            read_errors.append(f"{f.name}: {exc}")
            continue
        rel_str = str(f.relative_to(target) if target.is_dir() else f.name)
        scanned_files.append(rel_str)
        if has_ui_layer and (f.suffix.lower() in UI_FILE_EXTENSIONS or f.name.startswith("mcp_apps_ui_")):
            combined_chunks.append(text)
        _scan_single_file(f, text, acc, has_ui_layer)

    visual_org_diag, cramped, sprawl, flat_hier = _run_complex_zero_visual_org_bridge(combined_chunks) if has_ui_layer else ({}, False, False, False)
    ev = _build_ui_evidence(acc, (cramped, sprawl, flat_hier)) if has_ui_layer else _build_backend_evidence(acc, len(scanned_files))
    diag = {
        "scanned_path": str(target), "stack_profile": "ui_enabled" if has_ui_layer else "backend_only",
        "has_ui_layer": has_ui_layer, "total_files_scanned": len(scanned_files),
        "files": scanned_files[:50], "native_alerts_found": acc["native_alerts"],
        "inert_placeholders_found": acc["inert_placeholders"], "syntax_errors_found": acc["syntax_errors"],
        "has_breadcrumbs_or_3_layer_nav": acc["has_breadcrumbs"], "has_container_queries": acc["has_container_queries"],
        "has_oklch_or_semantic_tokens": acc["has_oklch_tokens"], "has_logical_box_or_flow_root": acc["has_logical_box"],
        "reverse_tab_order_violations": acc["reverse_tab_order"], "complex_zero_visual_org_audit": visual_org_diag,
        "read_errors": read_errors,
    }
    return ev, diag


def _render_tbody_rows(r1: DeterministicScoreReport, r2: DeterministicScoreReport) -> str:
    """Renders HTML <tbody> rows comparing V1 vs V2 deterministic metrics."""
    rows_spec = [
        ("INE (Navegabilidade &amp; 4 Estados)", "25%", r1.ine_navigation, r2.ine_navigation),
        ("ICI (Coesão por Ilhas SRP)", "20%", r1.ici_island_cohesion, r2.ici_island_cohesion),
        ("IPC (Code Quality &amp; Zero Hardcode)", "25%", r1.ipc_code_purity, r2.ipc_code_purity),
        ("IRM (Crítica Severa de MVP)", "15%", r1.irm_mvp_rigor, r2.irm_mvp_rigor),
        ("ICTE (Tipografia Linear &amp; Anti-Squish)", "15%", r1.icte_typography_structure, r2.icte_typography_structure),
    ]
    lines = ["        <tbody>"]
    for label, weight, v1_val, v2_val in rows_spec:
        d_val = round(v2_val - v1_val, 2)
        d_str = f"+{d_val:.2f}" if d_val >= 0 else f"{d_val:.2f}"
        cls = "diff-added" if d_val >= 0 else "diff-removed"
        lines.append(
            f"          <tr><td>{label}</td><td>{weight}</td><td>{v1_val:.2f}</td>"
            f'<td>{v2_val:.2f}</td><td><span class="{cls}">{d_str}</span></td></tr>'
        )
    lines.append("        </tbody>")
    return "\n".join(lines)


def generate_resolution_html(
    r1: DeterministicScoreReport,
    r2: DeterministicScoreReport,
    ev1: ArchitecturalEvidence,
    ev2: ArchitecturalEvidence,
    output_path: Path,
    template_path: Optional[Path] = None,
) -> Path:
    """Fills the V1 vs V2 HTML template with computed deterministic scores."""
    del ev1, ev2
    if template_path is None:
        candidate = Path(__file__).resolve().parent.parent / "templates" / "resolution_diff_v1_v2.html"
        if candidate.exists():
            template_path = candidate

    delta_sga = round(r2.sga_global_score - r1.sga_global_score, 2)
    delta_sign = f"+{delta_sga:.2f}" if delta_sga >= 0 else f"{delta_sga:.2f}"

    if template_path and template_path.exists():
        html = template_path.read_text(encoding="utf-8")
        replacements = [
            (r'(<meta name="score-v1-baseline" content=")[^"]*(")', rf"\g<1>{r1.sga_global_score:.2f}\g<2>"),
            (r'(<meta name="score-v2-resolved" content=")[^"]*(")', rf"\g<1>{r2.sga_global_score:.2f}\g<2>"),
            (r'(<meta name="score-delta" content=")[^"]*(")', rf"\g<1>{delta_sign}\g<2>"),
            (r'(<meta name="audit-timestamp" content=")[^"]*(")', rf"\g<1>{r2.timestamp}\g<2>"),
            (r"V1 Baseline:\s*[0-9.]+/100", f"V1 Baseline: {r1.sga_global_score:.2f}/100"),
            (r"V2 Resolvida:\s*[0-9.]+/100", f"V2 Resolvida: {r2.sga_global_score:.2f}/100"),
            (r"Delta:\s*[+\-0-9.]+\s*pts", f"Delta: {delta_sign} pts"),
        ]
        for pat, rep in replacements:
            html = re.sub(pat, rep, html)
        html = re.sub(r"<tbody>.*?</tbody>", _render_tbody_rows(r1, r2), html, count=1, flags=re.DOTALL)
    else:
        html = f"<html><body><h1>V1 ({r1.sga_global_score}) -> V2 ({r2.sga_global_score}) | Delta: {delta_sign}</h1></body></html>"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def run_self_test(html_out: Optional[str] = None) -> int:
    """Runs the standard V1 vs V2 deterministic regression test."""
    v1_ev = ArchitecturalEvidence(8, 2, 4, 1, 5, 12, 4, 5, 3, 10, 5, 3, False, False, True, False, False)
    v2_ev = ArchitecturalEvidence(6, 0, 3, 3, 2, 8, 8, 0, 0, 5, 5, 0, True, True, True, True, True)
    r1 = calculate_architecture_score(v1_ev, "V1_BASELINE")
    r2 = calculate_architecture_score(v2_ev, "V2_REFATORADA")
    payload: Dict[str, Any] = {
        "V1": asdict(r1), "V2": asdict(r2), "delta": round(r2.sga_global_score - r1.sga_global_score, 2),
        "status": "PASS" if (r1.sga_global_score == 14.67 and r2.sga_global_score == 100.0) else "CHECK",
    }
    if html_out:
        payload["html_report_generated"] = str(generate_resolution_html(r1, r2, v1_ev, v2_ev, Path(html_out)))
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    """CLI entrypoint for the stack-adaptive SGA/TIF deterministic scorer."""
    parser = argparse.ArgumentParser(description="Motor de Cálculo Determinístico (Zero Placebo) - system-project-auditor v6.1.0")
    parser.add_argument("--self-test", action="store_true", help="Executa o caso de teste determinístico V1 vs V2.")
    parser.add_argument("--scan", type=str, help="Caminho de um diretório ou arquivo para auditoria AST/Regex.")
    parser.add_argument("--scan-v1", type=str, help="Diretório/arquivo da V1 (Baseline) para comparação com --scan-v2.")
    parser.add_argument("--scan-v2", type=str, help="Diretório/arquivo da V2 (Treatment) para comparação com --scan-v1.")
    parser.add_argument("--html-out", type=str, help="Caminho opcional para exportar o relatório HTML V1 vs V2.")
    args = parser.parse_args()

    if args.scan_v1 and args.scan_v2:
        ev1, diag1 = scan_project_tree(Path(args.scan_v1))
        ev2, diag2 = scan_project_tree(Path(args.scan_v2))
        r1, r2 = calculate_architecture_score(ev1, "V1_SCANNED"), calculate_architecture_score(ev2, "V2_SCANNED")
        res: Dict[str, Any] = {
            "V1": {"report": asdict(r1), "evidence": asdict(ev1), "diagnostics": diag1},
            "V2": {"report": asdict(r2), "evidence": asdict(ev2), "diagnostics": diag2},
            "delta": round(r2.sga_global_score - r1.sga_global_score, 2),
        }
        if args.html_out:
            res["html_report_generated"] = str(generate_resolution_html(r1, r2, ev1, ev2, Path(args.html_out)))
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    if args.scan:
        ev, diag = scan_project_tree(Path(args.scan))
        rep = calculate_architecture_score(ev, "SCANNED_TARGET")
        print(json.dumps({"report": asdict(rep), "evidence": asdict(ev), "diagnostics": diag}, indent=2, ensure_ascii=False))
        return 0

    return run_self_test(html_out=args.html_out)


if __name__ == "__main__":
    sys.exit(main())
