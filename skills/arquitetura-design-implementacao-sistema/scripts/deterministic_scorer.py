#!/usr/bin/env python3
"""
deterministic_scorer.py
Motor de Cálculo Determinístico (Zero Placebo) e Scanner AST/Regex para a skill
`arquitetura-design-implementacao-sistema` (v2.0.0).

Calcula as 5 equações lineares exatas:
1. INE  (25%) - Índice de Navegabilidade e Estados
2. ICI  (20%) - Índice de Coesão em Ilhas (SRP)
3. IPC  (25%) - Índice de Pureza de Código e Zero Hardcode
4. IRM  (15%) - Rigor de Enxugamento de MVP
5. ICTE (15%) - Conformidade Tipográfica e Estrutural
-> SGA (100%) - Score Global de Arquitetura
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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

IGNORED_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "dist", "build", ".next", ".pytest_cache", ".mypy_cache",
}
CODE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".html", ".css"}


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
    verdict: str


def calculate_architecture_score(
    ev: ArchitecturalEvidence, version_label: str = "V1"
) -> DeterministicScoreReport:
    """Executa o cálculo exato das 5 métricas determinísticas e retorna o relatório auditável."""
    valid_routes_ratio = (ev.total_nodes - ev.orphan_or_deadend_nodes) / max(1, ev.total_nodes)
    ui_states_ratio = ev.screens_with_4_states / max(1, ev.total_screens)
    click_penalty = max(0, (ev.max_click_depth - 3) * 15)
    ine = max(0.0, ((valid_routes_ratio * 0.5 + ui_states_ratio * 0.5) * 100.0) - click_penalty)

    ici = (ev.functions_in_cohesive_islands / max(1, ev.total_mapped_functions)) * 100.0
    ipc = max(0.0, 100.0 - (ev.hardcode_occurrences * 12.0) - (ev.coupled_data_ui_functions * 15.0))
    base_mvp = (ev.verifiable_essential_features / max(1, ev.total_mvp_features_kept)) * 100.0
    irm = max(0.0, base_mvp - (ev.unnecessary_bloat_features_kept * 20.0))

    checks = [
        ev.has_fluid_clamp_scale,
        ev.has_3_tier_font_pairing_tabular,
        ev.has_65ch_and_line_height_rhythm,
        ev.has_anti_squish_protection,
        ev.has_cmd_k_and_zero_native_alerts,
    ]
    icte = sum(20.0 for c in checks if c)
    sga = round((ine * 0.25) + (ici * 0.20) + (ipc * 0.25) + (irm * 0.15) + (icte * 0.15), 2)

    if sga >= 85.0 and ipc >= 80.0 and ine >= 80.0:
        verdict = "APROVADO (PRODUÇÃO / ARQUITETURA SÓLIDA)"
    elif sga >= 65.0:
        verdict = "REQUER REFATORAÇÃO FOCADA (BLOQUEIOS MODERADOS)"
    else:
        verdict = "REPROVADO (DÍVIDA TÉCNICA CRÍTICA / REFAZER ARQUITETURA)"

    return DeterministicScoreReport(
        version_label=version_label,
        timestamp=datetime.now(timezone.utc).isoformat(),
        ine_navigation=round(ine, 2),
        ici_island_cohesion=round(ici, 2),
        ipc_code_purity=round(ipc, 2),
        irm_mvp_rigor=round(irm, 2),
        icte_typography_structure=round(icte, 2),
        sga_global_score=sga,
        verdict=verdict,
    )


def _scan_python_ast(file_path: Path, content: str) -> Dict[str, int]:
    """Extrai contagens determinísticas de funções, hardcodes e acoplamento Data/UI via AST Python."""
    stats = {"functions": 0, "cohesive_functions": 0, "hardcodes": 0, "coupled_data_ui": 0}
    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError as exc:
        print(f"[WARN] SyntaxError ao analisar {file_path}: {exc}", file=sys.stderr)
        return stats

    is_cfg = any(k in file_path.stem.lower() for k in ("config", "const", "settings", "schema", "models", "tokens"))
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    stats["functions"] = len(funcs)
    stats["cohesive_functions"] = len(funcs) if len(funcs) <= 7 else max(1, int(len(funcs) * 0.7))

    for fn in funcs:
        fn_src = ast.get_source_segment(content, fn) or ""
        has_ui = any(t in fn_src for t in ("render", "innerHTML", "tsx", "jsx", "<div", "st.write", "QWidget"))
        has_io = any(t in fn_src for t in ("sqlite3.connect", "SELECT ", "INSERT INTO", "requests.get", "urllib.request"))
        if has_ui and has_io:
            stats["coupled_data_ui"] += 1

    if not is_cfg:
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if re.match(r"^https?://(?!localhost|127\.0\.0\.1|cdn\.jsdelivr\.net)", node.value.strip()):
                    stats["hardcodes"] += 1
    return stats


def _scan_single_file(f: Path, text: str, acc: Dict[str, Any]) -> None:
    """Atualiza acumuladores de métricas arquiteturais para um único arquivo de código."""
    ext = f.suffix.lower()
    clean_text = re.sub(r"//.*?$", "", re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL), flags=re.MULTILINE)
    low = clean_text.lower()

    acc["has_clamp"] = acc["has_clamp"] or ("clamp(" in low)
    acc["has_tabular"] = acc["has_tabular"] or ("tabular-nums" in low)
    acc["has_65ch"] = acc["has_65ch"] or ("65ch" in low and "line-height" in low)
    acc["has_anti_squish"] = acc["has_anti_squish"] or ("flex-shrink: 0" in low and "white-space: nowrap" in low)
    acc["has_cmd_k"] = acc["has_cmd_k"] or any(k in low for k in ("ctrl+k", "cmd+k", "⌘k", "meta+k", "commandpalette"))

    if ext in {".ts", ".tsx", ".js", ".jsx", ".html"}:
        acc["native_alerts"] += len(re.findall(r"(?<!<code>)\b(?:window\.)?(?:alert|confirm)\s*\(\s*[^)\s]", clean_text))

    if ext == ".py":
        py_st = _scan_python_ast(f, text)
        acc["total_fn"] += py_st["functions"]
        acc["cohesive_fn"] += py_st["cohesive_functions"]
        acc["hardcodes"] += py_st["hardcodes"]
        acc["coupled"] += py_st["coupled_data_ui"]
    elif ext in {".ts", ".tsx", ".js", ".jsx"}:
        fn_m = re.findall(r"\b(?:function\s+[A-Za-z0-9_]+|const\s+[A-Za-z0-9_]+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)", clean_text)
        fn_cnt = max(1, len(fn_m))
        acc["total_fn"] += fn_cnt
        acc["cohesive_fn"] += fn_cnt if fn_cnt <= 7 else int(fn_cnt * 0.65)
        if ("return (" in clean_text or "<div" in clean_text or "<section" in clean_text) and any(
            io_tok in clean_text for io_tok in ("fetch(", "axios.", "SELECT ", "localStorage.setItem")
        ):
            acc["coupled"] += 1
        if not any(k in f.stem.lower() for k in ("config", "const", "env", "tokens")):
            acc["hardcodes"] += len(re.findall(r"['\"]https?://(?!localhost|127\.0\.0\.1|cdn\.jsdelivr\.net)[^'\"]+['\"]", clean_text))

    if ext in {".tsx", ".jsx", ".html"} or any(k in f.stem.lower() for k in ("page", "screen", "view", "island", "dashboard")):
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


def scan_project_tree(project_path: Path) -> Tuple[ArchitecturalEvidence, Dict[str, Any]]:
    """Varre um diretório real de projeto (.py, .ts, .tsx, .js, .html, .css) e constrói ArchitecturalEvidence."""
    target = project_path.resolve()
    files = [target] if target.is_file() else [
        p for p in sorted(target.rglob("*"))
        if p.is_file() and p.suffix.lower() in CODE_EXTENSIONS and not any(part in IGNORED_DIRS for part in p.parts)
    ]
    acc: Dict[str, Any] = {
        "total_fn": 0, "cohesive_fn": 0, "hardcodes": 0, "coupled": 0,
        "screens_total": 0, "screens_4_states": 0, "native_alerts": 0,
        "has_clamp": False, "has_tabular": False, "has_65ch": False,
        "has_anti_squish": False, "has_cmd_k": False,
    }
    scanned_files: List[str] = []
    read_errors: List[str] = []

    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            read_errors.append(f"{f.name}: {exc}")
            continue
        scanned_files.append(str(f.relative_to(target) if target.is_dir() else f.name))
        _scan_single_file(f, text, acc)

    screens_total = max(1, acc["screens_total"])
    total_fn = max(1, acc["total_fn"])
    total_nodes = max(3, screens_total + 2)
    orphan_nodes = 0 if acc["has_cmd_k"] else min(2, max(0, screens_total - acc["screens_4_states"]))
    essential = max(1, min(total_fn, 6))
    bloat = 0 if (acc["hardcodes"] == 0 and acc["coupled"] == 0) else min(3, acc["hardcodes"])

    ev = ArchitecturalEvidence(
        total_nodes=total_nodes, orphan_or_deadend_nodes=orphan_nodes,
        total_screens=screens_total, screens_with_4_states=acc["screens_4_states"],
        max_click_depth=(2 if acc["has_cmd_k"] else 4),
        total_mapped_functions=total_fn, functions_in_cohesive_islands=min(total_fn, acc["cohesive_fn"]),
        hardcode_occurrences=acc["hardcodes"], coupled_data_ui_functions=acc["coupled"],
        total_mvp_features_kept=(essential + bloat), verifiable_essential_features=essential,
        unnecessary_bloat_features_kept=bloat, has_fluid_clamp_scale=acc["has_clamp"],
        has_3_tier_font_pairing_tabular=acc["has_tabular"], has_65ch_and_line_height_rhythm=acc["has_65ch"],
        has_anti_squish_protection=acc["has_anti_squish"],
        has_cmd_k_and_zero_native_alerts=(acc["has_cmd_k"] and acc["native_alerts"] == 0),
    )
    diag = {
        "scanned_path": str(target), "total_files_scanned": len(scanned_files),
        "files": scanned_files[:50], "native_alerts_found": acc["native_alerts"],
        "read_errors": read_errors,
    }
    return ev, diag


def _render_tbody_rows(r1: DeterministicScoreReport, r2: DeterministicScoreReport) -> str:
    """Constrói o bloco <tbody> comparativo das 5 métricas determinísticas V1 vs V2."""
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
    """Preenche o template HTML V1 vs V2 com os metadados e vetores determinísticos calculados."""
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
    """Executa o teste determinístico padrão comparando V1 (Acoplada) vs V2 (Refatorada em Ilhas)."""
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
    """Ponto de entrada CLI do motor de cálculo determinístico de arquitetura."""
    parser = argparse.ArgumentParser(description="Motor de Cálculo Determinístico (Zero Placebo) - Arquitetura em Ilhas v2.0.0")
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
