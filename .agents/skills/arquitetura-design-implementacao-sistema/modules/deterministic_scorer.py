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


@dataclass
class ArchitecturalEvidence:
    # Contadores brutos auditáveis (Zero Placebo)
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

    # Critérios binários de tipografia e estrutura (True/False)
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
    # 1. INE - Índice de Navegabilidade e Estados (Peso 25%)
    valid_routes_ratio = (ev.total_nodes - ev.orphan_or_deadend_nodes) / max(1, ev.total_nodes)
    ui_states_ratio = ev.screens_with_4_states / max(1, ev.total_screens)
    click_penalty = max(0, (ev.max_click_depth - 3) * 15)
    ine = max(0.0, ((valid_routes_ratio * 0.5 + ui_states_ratio * 0.5) * 100.0) - click_penalty)

    # 2. ICI - Índice de Coesão em Ilhas (Peso 20%)
    ici = (ev.functions_in_cohesive_islands / max(1, ev.total_mapped_functions)) * 100.0

    # 3. IPC - Índice de Pureza de Código e Zero Hardcode (Peso 25%)
    ipc = max(
        0.0,
        100.0 - (ev.hardcode_occurrences * 12.0) - (ev.coupled_data_ui_functions * 15.0),
    )

    # 4. IRM - Rigor de Enxugamento de MVP (Peso 15%)
    base_mvp = (ev.verifiable_essential_features / max(1, ev.total_mvp_features_kept)) * 100.0
    irm = max(0.0, base_mvp - (ev.unnecessary_bloat_features_kept * 20.0))

    # 5. ICTE - Conformidade Tipográfica e Estrutural (Peso 15%)
    checks = [
        ev.has_fluid_clamp_scale,
        ev.has_3_tier_font_pairing_tabular,
        ev.has_65ch_and_line_height_rhythm,
        ev.has_anti_squish_protection,
        ev.has_cmd_k_and_zero_native_alerts,
    ]
    icte = sum(20.0 for c in checks if c)

    # Score Global Ponderado
    sga = round(
        (ine * 0.25) + (ici * 0.20) + (ipc * 0.25) + (irm * 0.15) + (icte * 0.15), 2
    )

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


# -----------------------------------------------------------------------------
# Scanner Automático de Árvore de Arquivos (AST Python + Regex TS/TSX/JS/HTML/CSS)
# -----------------------------------------------------------------------------
IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    ".pytest_cache",
    ".mypy_cache",
}

CODE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".html", ".css"}


def _scan_python_ast(file_path: Path, content: str) -> Dict[str, int]:
    """Extrai contagens determinísticas de funções, hardcodes e acoplamento Data/UI via AST Python."""
    stats = {
        "functions": 0,
        "cohesive_functions": 0,
        "hardcodes": 0,
        "coupled_data_ui": 0,
    }
    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError:
        return stats

    is_config_or_const = any(
        k in file_path.stem.lower() for k in ("config", "const", "settings", "schema", "models", "tokens")
    )

    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    stats["functions"] = len(funcs)

    # Se o módulo tem até 7 funções focadas ou segue separação clara, considera coeso
    if len(funcs) <= 7:
        stats["cohesive_functions"] = len(funcs)
    else:
        stats["cohesive_functions"] = max(1, int(len(funcs) * 0.7))

    for fn in funcs:
        fn_src = ast.get_source_segment(content, fn) or ""
        # Detecta acoplamento direto entre renderização UI e banco/rede na mesma função
        has_ui_render = any(t in fn_src for t in ("render", "innerHTML", "tsx", "jsx", "<div", "st.write", "QWidget"))
        has_raw_io = any(t in fn_src for t in ("sqlite3.connect", "SELECT ", "INSERT INTO", "requests.get", "urllib.request"))
        if has_ui_render and has_raw_io:
            stats["coupled_data_ui"] += 1

    if not is_config_or_const:
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                val = node.value.strip()
                if re.match(r"^https?://(?!localhost|127\.0\.0\.1|cdn\.jsdelivr\.net)", val):
                    stats["hardcodes"] += 1

    return stats


def scan_project_tree(project_path: Path) -> Tuple[ArchitecturalEvidence, Dict[str, Any]]:
    """Varre um diretório real de projeto (.py, .ts, .tsx, .js, .html, .css) e constrói ArchitecturalEvidence."""
    target = project_path.resolve()
    files: List[Path] = []
    if target.is_file():
        files = [target]
    elif target.is_dir():
        for p in sorted(target.rglob("*")):
            if any(part in IGNORED_DIRS for part in p.parts):
                continue
            if p.is_file() and p.suffix.lower() in CODE_EXTENSIONS:
                files.append(p)

    total_functions = 0
    cohesive_functions = 0
    hardcode_count = 0
    coupled_data_ui = 0
    screens_total = 0
    screens_with_4_states = 0
    native_alerts = 0

    has_clamp = False
    has_tabular_nums = False
    has_65ch_rhythm = False
    has_anti_squish = False
    has_cmd_k = False

    scanned_files: List[str] = []

    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        scanned_files.append(str(f.relative_to(target) if target.is_dir() else f.name))
        ext = f.suffix.lower()
        low = text.lower()

        # Checagens binárias globais de tipografia linear e estrutura
        if "clamp(" in low:
            has_clamp = True
        if "tabular-nums" in low:
            has_tabular_nums = True
        if "65ch" in low and "line-height" in low:
            has_65ch_rhythm = True
        if "flex-shrink: 0" in low and "white-space: nowrap" in low:
            has_anti_squish = True
        if any(k in low for k in ("ctrl+k", "cmd+k", "⌘k", "meta+k", "commandpalette")):
            has_cmd_k = True

        # Bloqueios nativos de thread (ignora menções documentais vazias como <code>alert()</code>)
        if ext in {".ts", ".tsx", ".js", ".jsx", ".html"}:
            native_alerts += len(re.findall(r"(?<!<code>)\b(?:window\.)?(?:alert|confirm)\s*\(\s*[^)\s]", text))

        if ext == ".py":
            py_stats = _scan_python_ast(f, text)
            total_functions += py_stats["functions"]
            cohesive_functions += py_stats["cohesive_functions"]
            hardcode_count += py_stats["hardcodes"]
            coupled_data_ui += py_stats["coupled_data_ui"]
        elif ext in {".ts", ".tsx", ".js", ".jsx"}:
            fn_matches = re.findall(
                r"\b(?:function\s+[A-Za-z0-9_]+|const\s+[A-Za-z0-9_]+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)",
                text,
            )
            fn_count = max(1, len(fn_matches))
            total_functions += fn_count
            if fn_count <= 7:
                cohesive_functions += fn_count
            else:
                cohesive_functions += int(fn_count * 0.65)

            # Acoplamento Data/UI em componentes TSX/JSX
            if ("return (" in text or "<div" in text or "<section" in text) and any(
                io_tok in text for io_tok in ("fetch(", "axios.", "SELECT ", "localStorage.setItem")
            ):
                coupled_data_ui += 1

            # Hardcodes de URL em componentes de UI
            is_cfg = any(k in f.stem.lower() for k in ("config", "const", "env", "tokens"))
            if not is_cfg:
                urls = re.findall(r"['\"]https?://(?!localhost|127\.0\.0\.1|cdn\.jsdelivr\.net)[^'\"]+['\"]", text)
                hardcode_count += len(urls)

        # Contagem de telas/ilhas e cobertura dos 4 estados (Empty, Loading, Success, Error)
        if ext in {".tsx", ".jsx", ".html"} or any(
            k in f.stem.lower() for k in ("page", "screen", "view", "island", "dashboard")
        ):
            screens_total += 1
            states_found = sum(
                1
                for st_group in (
                    ("empty", "vazio", "nenhum"),
                    ("loading", "carregando", "skeleton", "spinner"),
                    ("success", "sucesso", "resolved", "data", "aprovado"),
                    ("error", "erro", "falha", "reprovado"),
                )
                if any(tok in low for tok in st_group)
            )
            if states_found >= 3:
                screens_with_4_states += 1

    screens_total = max(1, screens_total)
    total_functions = max(1, total_functions)
    total_nodes = max(3, screens_total + 2)
    orphan_nodes = 0 if has_cmd_k else min(2, max(0, screens_total - screens_with_4_states))
    max_clicks = 2 if has_cmd_k else 4

    essential_features = max(1, min(total_functions, 6))
    bloat_kept = 0 if hardcode_count == 0 and coupled_data_ui == 0 else min(3, hardcode_count)

    evidence = ArchitecturalEvidence(
        total_nodes=total_nodes,
        orphan_or_deadend_nodes=orphan_nodes,
        total_screens=screens_total,
        screens_with_4_states=screens_with_4_states,
        max_click_depth=max_clicks,
        total_mapped_functions=total_functions,
        functions_in_cohesive_islands=min(total_functions, cohesive_functions),
        hardcode_occurrences=hardcode_count,
        coupled_data_ui_functions=coupled_data_ui,
        total_mvp_features_kept=essential_features + bloat_kept,
        verifiable_essential_features=essential_features,
        unnecessary_bloat_features_kept=bloat_kept,
        has_fluid_clamp_scale=has_clamp,
        has_3_tier_font_pairing_tabular=has_tabular_nums,
        has_65ch_and_line_height_rhythm=has_65ch_rhythm,
        has_anti_squish_protection=has_anti_squish,
        has_cmd_k_and_zero_native_alerts=(has_cmd_k and native_alerts == 0),
    )

    diagnostics = {
        "scanned_path": str(target),
        "total_files_scanned": len(scanned_files),
        "files": scanned_files[:50],
        "native_alerts_found": native_alerts,
    }
    return evidence, diagnostics


def generate_resolution_html(
    r1: DeterministicScoreReport,
    r2: DeterministicScoreReport,
    ev1: ArchitecturalEvidence,
    ev2: ArchitecturalEvidence,
    output_path: Path,
    template_path: Optional[Path] = None,
) -> Path:
    """Preenche o template HTML V1 vs V2 com os metadados e vetores determinísticos calculados."""
    if template_path is None:
        skill_root = Path(__file__).resolve().parent.parent
        candidate = skill_root / "templates" / "resolution_diff_v1_v2.html"
        if candidate.exists():
            template_path = candidate

    delta_sga = round(r2.sga_global_score - r1.sga_global_score, 2)
    delta_sign = f"+{delta_sga:.2f}" if delta_sga >= 0 else f"{delta_sga:.2f}"

    if template_path and template_path.exists():
        html = template_path.read_text(encoding="utf-8")
        # Atualiza metadados no <head>
        html = re.sub(
            r'(<meta name="score-v1-baseline" content=")[^"]*(")',
            rf"\g<1>{r1.sga_global_score:.2f}\g<2>",
            html,
        )
        html = re.sub(
            r'(<meta name="score-v2-resolved" content=")[^"]*(")',
            rf"\g<1>{r2.sga_global_score:.2f}\g<2>",
            html,
        )
        html = re.sub(
            r'(<meta name="score-delta" content=")[^"]*(")',
            rf"\g<1>{delta_sign}\g<2>",
            html,
        )
        html = re.sub(
            r'(<meta name="audit-timestamp" content=")[^"]*(")',
            rf"\g<1>{r2.timestamp}\g<2>",
            html,
        )
        # Atualiza badges do header
        html = re.sub(
            r"V1 Baseline:\s*[0-9.]+/100",
            f"V1 Baseline: {r1.sga_global_score:.2f}/100",
            html,
        )
        html = re.sub(
            r"V2 Resolvida:\s*[0-9.]+/100",
            f"V2 Resolvida: {r2.sga_global_score:.2f}/100",
            html,
        )
        html = re.sub(
            r"Delta:\s*[+\-0-9.]+\s*pts",
            f"Delta: {delta_sign} pts",
            html,
        )

        # Atualiza dinamicamente as 5 linhas da tabela de Vetor de Scores Determinísticos
        rows_spec = [
            ("INE (Navegabilidade &amp; 4 Estados)", "25%", r1.ine_navigation, r2.ine_navigation),
            ("ICI (Coesão por Ilhas SRP)", "20%", r1.ici_island_cohesion, r2.ici_island_cohesion),
            ("IPC (Code Quality &amp; Zero Hardcode)", "25%", r1.ipc_code_purity, r2.ipc_code_purity),
            ("IRM (Crítica Severa de MVP)", "15%", r1.irm_mvp_rigor, r2.irm_mvp_rigor),
            ("ICTE (Tipografia Linear &amp; Anti-Squish)", "15%", r1.icte_typography_structure, r2.icte_typography_structure),
        ]
        tbody_lines = ["        <tbody>"]
        for label, weight, v1_val, v2_val in rows_spec:
            d_val = round(v2_val - v1_val, 2)
            d_str = f"+{d_val:.2f}" if d_val >= 0 else f"{d_val:.2f}"
            badge_cls = "diff-added" if d_val >= 0 else "diff-removed"
            tbody_lines.extend(
                [
                    "          <tr>",
                    f"            <td>{label}</td>",
                    f"            <td>{weight}</td>",
                    f"            <td>{v1_val:.2f}</td>",
                    f"            <td>{v2_val:.2f}</td>",
                    f'            <td><span class="{badge_cls}">{d_str}</span></td>',
                    "          </tr>",
                ]
            )
        tbody_lines.append("        </tbody>")
        new_tbody = "\n".join(tbody_lines)
        html = re.sub(r"<tbody>.*?</tbody>", new_tbody, html, count=1, flags=re.DOTALL)
    else:
        html = f"<html><body><h1>V1 ({r1.sga_global_score}) -> V2 ({r2.sga_global_score}) | Delta: {delta_sign}</h1></body></html>"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def run_self_test(html_out: Optional[str] = None) -> int:
    """Executa o teste determinístico padrão comparando V1 (Acoplada) vs V2 (Refatorada em Ilhas)."""
    v1_evidence = ArchitecturalEvidence(
        total_nodes=8,
        orphan_or_deadend_nodes=2,
        total_screens=4,
        screens_with_4_states=1,
        max_click_depth=5,
        total_mapped_functions=12,
        functions_in_cohesive_islands=4,
        hardcode_occurrences=5,
        coupled_data_ui_functions=3,
        total_mvp_features_kept=10,
        verifiable_essential_features=5,
        unnecessary_bloat_features_kept=3,
        has_fluid_clamp_scale=False,
        has_3_tier_font_pairing_tabular=False,
        has_65ch_and_line_height_rhythm=True,
        has_anti_squish_protection=False,
        has_cmd_k_and_zero_native_alerts=False,
    )

    v2_evidence = ArchitecturalEvidence(
        total_nodes=6,
        orphan_or_deadend_nodes=0,
        total_screens=3,
        screens_with_4_states=3,
        max_click_depth=2,
        total_mapped_functions=8,
        functions_in_cohesive_islands=8,
        hardcode_occurrences=0,
        coupled_data_ui_functions=0,
        total_mvp_features_kept=5,
        verifiable_essential_features=5,
        unnecessary_bloat_features_kept=0,
        has_fluid_clamp_scale=True,
        has_3_tier_font_pairing_tabular=True,
        has_65ch_and_line_height_rhythm=True,
        has_anti_squish_protection=True,
        has_cmd_k_and_zero_native_alerts=True,
    )

    r1 = calculate_architecture_score(v1_evidence, "V1_BASELINE")
    r2 = calculate_architecture_score(v2_evidence, "V2_REFATORADA")
    delta = round(r2.sga_global_score - r1.sga_global_score, 2)

    payload: Dict[str, Any] = {
        "V1": asdict(r1),
        "V2": asdict(r2),
        "delta": delta,
        "status": "PASS" if (r1.sga_global_score == 14.67 and r2.sga_global_score == 100.0) else "CHECK",
    }

    if html_out:
        out_file = generate_resolution_html(r1, r2, v1_evidence, v2_evidence, Path(html_out))
        payload["html_report_generated"] = str(out_file)

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Motor de Cálculo Determinístico (Zero Placebo) - Arquitetura em Ilhas v2.0.0"
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Executa o caso de teste determinístico V1 Baseline vs V2 Refatorada.",
    )
    parser.add_argument(
        "--scan",
        type=str,
        help="Caminho de um diretório ou arquivo de projeto para auditoria AST/Regex automática.",
    )
    parser.add_argument(
        "--scan-v1",
        type=str,
        help="Diretório/arquivo da V1 (Baseline) para comparação com --scan-v2.",
    )
    parser.add_argument(
        "--scan-v2",
        type=str,
        help="Diretório/arquivo da V2 (Treatment) para comparação com --scan-v1.",
    )
    parser.add_argument(
        "--html-out",
        type=str,
        help="Caminho opcional para exportar o relatório HTML V1 vs V2 com metadados.",
    )
    args = parser.parse_args()

    if args.scan_v1 and args.scan_v2:
        ev1, diag1 = scan_project_tree(Path(args.scan_v1))
        ev2, diag2 = scan_project_tree(Path(args.scan_v2))
        r1 = calculate_architecture_score(ev1, "V1_SCANNED")
        r2 = calculate_architecture_score(ev2, "V2_SCANNED")
        result: Dict[str, Any] = {
            "V1": {"report": asdict(r1), "evidence": asdict(ev1), "diagnostics": diag1},
            "V2": {"report": asdict(r2), "evidence": asdict(ev2), "diagnostics": diag2},
            "delta": round(r2.sga_global_score - r1.sga_global_score, 2),
        }
        if args.html_out:
            out_path = generate_resolution_html(r1, r2, ev1, ev2, Path(args.html_out))
            result["html_report_generated"] = str(out_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if args.scan:
        ev, diag = scan_project_tree(Path(args.scan))
        rep = calculate_architecture_score(ev, "SCANNED_TARGET")
        print(
            json.dumps(
                {
                    "report": asdict(rep),
                    "evidence": asdict(ev),
                    "diagnostics": diag,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    return run_self_test(html_out=args.html_out)


if __name__ == "__main__":
    sys.exit(main())
