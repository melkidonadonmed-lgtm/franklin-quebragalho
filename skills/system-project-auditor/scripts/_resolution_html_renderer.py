"""
_resolution_html_renderer.py
V1 vs V2 HTML resolution diff report renderer extracted from deterministic_scorer
to keep modules concise (<= 600 lines).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Optional


def _render_tbody_rows(r1: Any, r2: Any) -> str:
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
    r1: Any,
    r2: Any,
    ev1: Any,
    ev2: Any,
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
