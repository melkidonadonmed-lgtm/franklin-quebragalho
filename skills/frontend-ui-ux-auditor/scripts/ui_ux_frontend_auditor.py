#!/usr/bin/env python3
"""
ui_ux_frontend_auditor.py
Motor determinístico de análise estática de HTML/CSS/JSX/TSX para a Skill
`frontend-ui-ux-auditor` (v1.0.0).

Calcula o Score_UI/UX ponderado (0 a 100) nas 6 dimensões da rubrica:
  Score = 0.20 * S_Tokens + 0.20 * S_Typo + 0.15 * S_DOM
        + 0.15 * S_Icons  + 0.15 * S_Light + 0.15 * S_Motion
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VOID_ELEMENTS: Set[str] = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
SEMANTIC_TAGS: Set[str] = {
    "main", "header", "nav", "aside", "section", "article", "footer",
}
VALID_8PX_SCALE: Set[int] = {0, 1, 2, 4, 8, 12, 16, 20, 24, 32, 40, 44, 48, 56, 64, 80, 96, 128, 240, 280}
STANDARD_ICON_PX: Set[int] = {16, 20, 24}

TW_ARBITRARY_PX_RE = re.compile(
    r"\b(?:p|px|py|pt|pr|pb|pl|m|mx|my|mt|mr|mb|ml|gap|gap-x|gap-y|w|h|top|left|right|bottom)-\[(\d+)px\]"
)
CSS_SPACING_PX_RE = re.compile(
    r"(?:padding(?:-(?:top|right|bottom|left))?|margin(?:-(?:top|right|bottom|left))?|gap)\s*:\s*([^;}{]+)",
    re.IGNORECASE,
)
PX_VAL_RE = re.compile(r"(\d+)\s*px", re.IGNORECASE)
FONT_SIZE_PX_RE = re.compile(r"font-size\s*:\s*(\d+)\s*px", re.IGNORECASE)
HEX_COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b")
COLOR_PAIR_RE = re.compile(
    r"\{[^{}]*?(?:color\s*:\s*(#[0-9a-fA-F]{3,6}))[^{}]*?(?:background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6}))"
    r"|\{[^{}]*?(?:background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6}))[^{}]*?(?:(?<!-)color\s*:\s*(#[0-9a-fA-F]{3,6}))",
    re.IGNORECASE | re.DOTALL,
)
REFLOW_TRANSITION_RE = re.compile(
    r"transition(?:-property)?\s*:[^;}{]*\b(width|height|padding|margin|top|left|right|bottom)\b",
    re.IGNORECASE,
)
BOX_SHADOW_RE = re.compile(r"box-shadow\s*:\s*([^;}{]+)", re.IGNORECASE)
TW_ICON_CLASS_RE = re.compile(r"\bw-(4|5|6)\b(?=[^\"']*?\bh-\1\b)|\bh-(4|5|6)\b(?=[^\"']*?\bw-\2\b)")


@dataclass
class UIUXAuditReport:
    target_name: str
    final_score: float
    grade: str
    verdict: str
    total_tags: int
    max_dom_depth: int
    divsoup_ratio: float
    icons_count: int
    standard_icon_sizes: bool
    token_adherence_pct: float
    arbitrary_values: List[str] = field(default_factory=list)
    contrast_violations: List[str] = field(default_factory=list)
    min_contrast_ratio: float = 21.0
    light_physics_135: bool = False
    elevation_shadows: bool = False
    zero_reflow_motion: bool = True
    reduced_motion_support: bool = False
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class DOMStructureParser(HTMLParser):
    """Analisa profundidade da árvore DOM, divsoup ratio, meta viewport e ícones SVG."""

    def __init__(self) -> None:
        super().__init__()
        self.total_tags: int = 0
        self.div_count: int = 0
        self.semantic_count: int = 0
        self.current_depth: int = 0
        self.max_depth: int = 0
        self.viewport_present: bool = False
        self.aria_current_present: bool = False
        self.icons_count: int = 0
        self.asymmetric_or_nonstd_icons: int = 0

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        t = tag.lower()
        self.total_tags += 1
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        if t == "div":
            self.div_count += 1
        elif t in SEMANTIC_TAGS:
            self.semantic_count += 1
        if t == "meta" and attr_map.get("name", "").lower() == "viewport":
            if "width=device-width" in attr_map.get("content", "").lower():
                self.viewport_present = True
        if attr_map.get("aria-current") == "page":
            self.aria_current_present = True
        if t == "svg":
            self._inspect_svg_icon(attr_map)
        if t not in VOID_ELEMENTS:
            self.current_depth += 1
            if self.current_depth > self.max_depth:
                self.max_depth = self.current_depth

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() not in VOID_ELEMENTS and self.current_depth > 0:
            self.current_depth -= 1

    def _inspect_svg_icon(self, attr_map: Dict[str, str]) -> None:
        self.icons_count += 1
        cls = attr_map.get("class", "")
        w_str = re.sub(r"[^0-9]", "", attr_map.get("width", ""))
        h_str = re.sub(r"[^0-9]", "", attr_map.get("height", ""))
        if w_str and h_str:
            w_px, h_px = int(w_str), int(h_str)
            if w_px != h_px or w_px not in STANDARD_ICON_PX:
                self.asymmetric_or_nonstd_icons += 1
            return
        if not TW_ICON_CLASS_RE.search(cls):
            vb = attr_map.get("viewbox", "")
            parts = vb.split()
            if len(parts) == 4 and parts[2] == parts[3] and int(float(parts[2])) in STANDARD_ICON_PX:
                return
            self.asymmetric_or_nonstd_icons += 1


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Converte string hexadecimal (#RGB ou #RRGGBB) para tupla (R, G, B) de 8 bits."""
    clean = hex_color.lstrip("#")
    if len(clean) == 3:
        clean = "".join(ch * 2 for ch in clean)
    return int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)


def srgb_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Calcula a luminância relativa W3C: L = 0.2126*R' + 0.7152*G' + 0.0722*B'."""
    channels: List[float] = []
    for c in rgb:
        norm = c / 255.0
        lin = norm / 12.92 if norm <= 0.04045 else ((norm + 0.055) / 1.055) ** 2.4
        channels.append(lin)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def wcag_contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    """Calcula a razão de contraste WCAG 2.1: CR = (L_claro + 0.05) / (L_escuro + 0.05)."""
    l1 = srgb_relative_luminance(hex_to_rgb(fg_hex))
    l2 = srgb_relative_luminance(hex_to_rgb(bg_hex))
    lighter, darker = max(l1, l2), min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def audit_color_contrast_pairs(source: str) -> Tuple[List[str], float]:
    """Extrai pares explícitos de cor/fundo em blocos CSS e valida CR >= 4.5:1."""
    violations: List[str] = []
    min_cr = 21.0
    for match in COLOR_PAIR_RE.finditer(source):
        fg = match.group(1) or match.group(4)
        bg = match.group(2) or match.group(3)
        if not fg or not bg:
            continue
        cr = wcag_contrast_ratio(fg, bg)
        min_cr = min(min_cr, cr)
        if cr < 4.5:
            violations.append(f"{fg} sobre {bg} (CR={cr}:1 < 4.5:1)")
    return violations, min_cr


def audit_design_tokens_8px(source: str, recs: List[str]) -> Tuple[float, float, List[str]]:
    """Audita aderência à escala de 8px, detecção de valores arbitrários e variáveis CSS."""
    arbitrary: List[str] = []
    total_checks = 0
    valid_checks = 0

    for m in TW_ARBITRARY_PX_RE.finditer(source):
        total_checks += 1
        px = int(m.group(1))
        if px in VALID_8PX_SCALE:
            valid_checks += 1
        else:
            arbitrary.append(m.group(0))

    for decl in CSS_SPACING_PX_RE.finditer(source):
        for px_m in PX_VAL_RE.finditer(decl.group(1)):
            total_checks += 1
            px = int(px_m.group(1))
            if px in VALID_8PX_SCALE:
                valid_checks += 1
            else:
                arbitrary.append(f"{px}px")

    token_vars = set(re.findall(r"var\(--[a-zA-Z0-9_-]+\)", source))
    total_checks += max(len(token_vars), 3)
    valid_checks += len(token_vars)
    adherence = round((valid_checks / max(total_checks, 1)) * 100.0, 1)
    score = max(0.0, min(100.0, adherence - (len(arbitrary) * 8.0) + (10.0 if token_vars else -15.0)))
    if arbitrary:
        recs.append(f"Substituir {len(arbitrary)} valores arbitrários ({', '.join(arbitrary[:4])}) por tokens da escala de 8px.")
    if not token_vars:
        recs.append("Adotar variáveis semânticas CSS (ex.: var(--border-muted), var(--accent)) conforme DESIGN.md.")
    return round(score, 1), adherence, arbitrary


def audit_typography_and_wcag(
    source: str, parser: DOMStructureParser, recs: List[str]
) -> Tuple[float, List[str], float]:
    """Audita nitidez tipográfica mobile, meta viewport, tamanho mínimo >= 12px e contraste WCAG."""
    score = 100.0
    low = source.lower()
    if not parser.viewport_present and "<html" in low:
        score -= 25.0
        recs.append("Configurar <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">.")
    if "antialiased" not in low:
        score -= 15.0
        recs.append("Ativar suavização subpixel (-webkit-font-smoothing: antialiased / class 'antialiased').")
    if "optimizelegibility" not in low:
        score -= 10.0
        recs.append("Adicionar text-rendering: optimizeLegibility para nitidez em telas Retina/OLED.")

    tiny_fonts = [int(m.group(1)) for m in FONT_SIZE_PX_RE.finditer(source) if int(m.group(1)) < 11]
    if tiny_fonts:
        score -= 20.0
        recs.append(f"Remover tamanhos de fonte inferiores a 11-12px ({tiny_fonts[0]}px detectado).")

    violations, min_cr = audit_color_contrast_pairs(source)
    if violations:
        score -= min(40.0, len(violations) * 20.0)
        recs.append(f"Corrigir {len(violations)} violação(ões) de contraste WCAG 2.1 AA: {violations[0]}.")
    return max(0.0, round(score, 1)), violations, min_cr


def audit_dom_and_navigation(source: str, parser: DOMStructureParser, recs: List[str]) -> Tuple[float, float]:
    """Audita profundidade DOM <= 12, divsoup ratio <= 0.45 e foco/navegação acessível."""
    score = 100.0
    divsoup = round(parser.div_count / max(parser.total_tags, 1), 2)
    if parser.max_depth > 12:
        score -= min(40.0, (parser.max_depth - 12) * 8.0)
        recs.append(f"Reduzir a profundidade da árvore DOM ({parser.max_depth} níveis) para <= 12.")
    if divsoup > 0.45:
        score -= min(35.0, (divsoup - 0.45) * 100.0)
        recs.append(f"Reduzir divsoup ratio ({divsoup}) para <= 0.45 usando HTML5 semântico (<main>, <nav>, <section>).")
    if parser.total_tags > 0 and parser.semantic_count == 0:
        score -= 20.0
        recs.append("Inserir marcos estruturais HTML5 (<header>, <nav>, <main>, <section>).")
    if "focus-visible" not in source.lower():
        score -= 15.0
        recs.append("Incluir indicadores de foco de teclado via :focus-visible.")
    return max(0.0, round(score, 1)), divsoup


def audit_light_and_motion(
    source: str, recs: List[str]
) -> Tuple[float, bool, bool, float, bool, bool]:
    """Audita luz zenital (90°–120° / chanfro especular), sombras em camadas, zero-reflow GPU e prefers-reduced-motion."""
    low = source.lower()
    has_zenithal_light = bool(
        re.search(r"border-top\s*:\s*1px\s+solid\s+(?:rgba\(\s*255\s*,\s*255\s*,\s*255|oklch\(\s*1\s+0\s+0)", low)
        or re.search(r"inset\s+0(?:px)?\s+1px\s+0(?:px)?(?:\s+0(?:px)?)?\s+(?:rgba\(\s*255\s*,\s*255\s*,\s*255|oklch\(\s*1\s+0\s+0|light-dark\()", low)
        or "--specular-rim" in low
        or "--catch-light" in low
        or "--shadow-inset" in low
        or ("border-t" in low and "white/" in low)
    )
    shadows = [m.group(1) for m in BOX_SHADOW_RE.finditer(source)]
    has_layered_shadow = (
        any("," in s for s in shadows)
        or any(
            tok in low
            for tok in (
                "--shadow-elevation-1",
                "--shadow-elevation-2",
                "--shadow-elevation-3",
                "--shadow-inset",
                "--elevation-1",
                "--elevation-2",
                "--elevation-3",
                "--elevation-low",
                "--elevation-medium",
                "--elevation-high",
                "--elevation-pressed",
                "tactile-low",
                "tactile-md",
                "tactile-lg",
                "tactile-pressed",
                "shadow-lg",
                "shadow-xl",
                "shadow-2xl",
            )
        )
    )
    light_score = (55.0 if has_zenithal_light else 20.0) + (45.0 if has_layered_shadow else 15.0)
    if not has_zenithal_light:
        recs.append(
            "Adicionar chanfro especular zenital 90°–120° (--catch-light: inset 0 1px 0 0 oklch(1 0 0 / 0.12..0.85))."
        )
    if not has_layered_shadow:
        recs.append(
            "Empregar sombras em 3 níveis (Umbra + Penumbra com spread negativo via --shadow-elevation-1..3)."
        )

    reflow_hits = [m.group(1) for m in REFLOW_TRANSITION_RE.finditer(source)]
    zero_reflow = len(reflow_hits) == 0
    has_reduced_motion = "prefers-reduced-motion" in low or "motion-reduce:" in low
    motion_score = 100.0
    if not zero_reflow:
        motion_score -= 45.0
        recs.append(f"Proibido animar propriedades de reflow ({', '.join(set(reflow_hits))}); use apenas transform e opacity.")
    if not has_reduced_motion:
        motion_score -= 25.0
        recs.append("Incluir suporte a '@media (prefers-reduced-motion: reduce)' ou 'motion-reduce:transition-none' para acessibilidade motora.")
    return round(light_score, 1), has_zenithal_light, has_layered_shadow, max(0.0, round(motion_score, 1)), zero_reflow, has_reduced_motion


def evaluate_source(source: str, target_name: str = "Componente") -> UIUXAuditReport:
    """Executa a auditoria determinística completa sobre um código-fonte HTML/CSS/JSX."""
    parser = DOMStructureParser()
    parser.feed(source)
    recs: List[str] = []

    s_tokens, adherence, arbitrary = audit_design_tokens_8px(source, recs)
    s_typo, contrast_Violations, min_cr = audit_typography_and_wcag(source, parser, recs)
    s_dom, divsoup = audit_dom_and_navigation(source, parser, recs)

    std_icons = parser.asymmetric_or_nonstd_icons == 0
    s_icons = 100.0 if std_icons else max(0.0, 100.0 - parser.asymmetric_or_nonstd_icons * 35.0)
    if not std_icons:
        recs.append("Padronizar ícones SVG em proporção quadrada 1:1 com bounding box de 16px, 20px ou 24px.")

    s_light, has_135, has_shadows, s_motion, zero_reflow, has_rm = audit_light_and_motion(source, recs)

    final_score = round(
        0.20 * s_tokens + 0.20 * s_typo + 0.15 * s_dom + 0.15 * s_icons + 0.15 * s_light + 0.15 * s_motion,
        1,
    )
    grade = "A+ (Produção de Elite)" if final_score >= 92.0 else ("A (Aprovado)" if final_score >= 85.0 else ("B (Requer Ajustes)" if final_score >= 70.0 else "C/F (Reprovado)"))
    verdict = "PASS" if final_score >= 85.0 and not contrast_Violations and zero_reflow else "FAIL"

    return UIUXAuditReport(
        target_name=target_name, final_score=final_score, grade=grade, verdict=verdict,
        total_tags=parser.total_tags, max_dom_depth=parser.max_depth, divsoup_ratio=divsoup,
        icons_count=parser.icons_count, standard_icon_sizes=std_icons, token_adherence_pct=adherence,
        arbitrary_values=arbitrary, contrast_violations=contrast_Violations, min_contrast_ratio=min_cr,
        light_physics_135=has_135, elevation_shadows=has_shadows, zero_reflow_motion=zero_reflow,
        reduced_motion_support=has_rm,
        dimension_scores={
            "design_tokens": s_tokens, "typography_mobile": s_typo, "structure_semantics": s_dom,
            "iconography": s_icons, "light_elevation": s_light, "motion_transitions": s_motion,
        },
        recommendations=recs,
    )


def format_cli_report(report: UIUXAuditReport) -> str:
    """Formata o relatório determinístico de auditoria UI/UX para saída no terminal."""
    lines = [
        "=" * 65,
        f"RELATÓRIO DETERMINÍSTICO DE AUDITORIA UI/UX: {report.target_name}",
        f"SCORE FINAL: {report.final_score} / 100 | NOTA: {report.grade} | [{report.verdict}]",
        "=" * 65,
        f"Tags Totais: {report.total_tags} | Profundidade DOM: {report.max_dom_depth} | Divsoup Ratio: {report.divsoup_ratio}",
        f"Ícones Identificados: {report.icons_count} | Tamanho Padrão (1:1): {report.standard_icon_sizes}",
        f"Escala de Tokens (8px): {report.token_adherence_pct}% de aderência",
        f"Luz Zenital (90°–120°) Presente: {report.light_physics_135} | Sombras de Elevação: {report.elevation_shadows}",
        f"Transições Zero-Reflow (GPU): {report.zero_reflow_motion} | Reduced Motion: {report.reduced_motion_support}",
    ]
    if report.recommendations:
        lines.append("Recomendações:")
        for rec in report.recommendations:
            lines.append(f"  - {rec}")
    lines.append("=" * 65)
    return "\n".join(lines)


def _run_self_test() -> int:
    """Executa autoteste determinístico da suíte interna (Elite vs Violação)."""
    demo_html = """<!DOCTYPE html><html lang="pt-BR"><head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      body { -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; color: #f8fafc; background-color: #0f172a; padding: 16px; margin: 8px; }
      .card { border: 1px solid var(--border-muted); border-top: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2); padding: 24px; gap: 16px; transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1), opacity 200ms ease; }
      .btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
      @media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 0.01ms !important; } }
    </style></head><body><header><nav><a href="/" aria-current="page" class="btn">Home</a></nav></header>
    <main><section class="card"><svg width="20" height="20" viewBox="0 0 20 20"></svg><h1>Dashboard</h1></section></main></body></html>"""
    rep = evaluate_source(demo_html, "DashboardDemo.html")
    assert rep.final_score >= 92.0 and rep.verdict == "PASS", f"Self-test falhou: {rep}"
    print(format_cli_report(rep))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Motor determinístico de auditoria UI/UX Frontend.")
    parser.add_argument("--target", type=str, default="", help="Arquivo ou diretório frontend a inspecionar.")
    parser.add_argument("--json", action="store_true", help="Emite saída em formato JSON.")
    parser.add_argument("--self-test", action="store_true", help="Executa autoteste determinístico integrado.")
    args = parser.parse_args()

    if args.self_test or not args.target:
        return _run_self_test()

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(f"[FAIL] Caminho não encontrado: {target_path}", file=sys.stderr)
        return 1

    if target_path.is_file():
        content = target_path.read_text(encoding="utf-8", errors="replace")
    else:
        exts = {".html", ".css", ".jsx", ".tsx", ".vue"}
        files = sorted(p for p in target_path.rglob("*") if p.is_file() and p.suffix.lower() in exts and "node_modules" not in p.parts)
        content = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in files)

    report = evaluate_source(content, target_path.name)
    if args.json:
        print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
    else:
        print(format_cli_report(report))
    return 0 if report.verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
