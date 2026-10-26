"""
test_ui_ux_frontend_auditor.py
Suíte de testes unitários automatizados para validar o motor determinístico
`ui_ux_frontend_auditor.py` da skill `frontend-ui-ux-auditor`.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT_DIR / "skills" / "frontend-ui-ux-auditor" / "scripts" / "ui_ux_frontend_auditor.py"

spec = importlib.util.spec_from_file_location("ui_ux_frontend_auditor", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
auditor = importlib.util.module_from_spec(spec)
sys.modules["ui_ux_frontend_auditor"] = auditor
spec.loader.exec_module(auditor)


def test_wcag_luminance_and_contrast_math() -> None:
    """Valida o cálculo exato de luminância relativa W3C e razão de contraste WCAG 2.1."""
    assert auditor.srgb_relative_luminance((0, 0, 0)) == 0.0
    assert round(auditor.srgb_relative_luminance((255, 255, 255)), 4) == 1.0
    assert auditor.wcag_contrast_ratio("#ffffff", "#000000") == 21.0
    assert auditor.wcag_contrast_ratio("#f8fafc", "#0f172a") >= 15.0
    assert auditor.wcag_contrast_ratio("#777777", "#888888") < 4.5


def test_detects_contrast_violations_in_css() -> None:
    """Garante que pares de cor com contraste insuficiente (< 4.5:1) são sinalizados."""
    bad_css = """
    .low-contrast { color: #666666; background-color: #777777; }
    .high-contrast { color: #ffffff; background: #0f172a; }
    """
    violations, min_cr = auditor.audit_color_contrast_pairs(bad_css)
    assert len(violations) == 1
    assert "#666666 sobre #777777" in violations[0]
    assert min_cr < 2.0


def test_detects_arbitrary_values_outside_8px_scale() -> None:
    """Verifica a detecção de classes Tailwind arbitrárias e CSS fora da grade de 8px."""
    source = """
    <div class="p-[13px] w-[37px] gap-[7px] p-[16px]"></div>
    <style>.box { margin: 11px; padding: 24px 16px; border: 1px solid var(--border-muted); }</style>
    """
    recs: list[str] = []
    score, adherence, arbitrary = auditor.audit_design_tokens_8px(source, recs)
    assert "p-[13px]" in arbitrary
    assert "w-[37px]" in arbitrary
    assert "gap-[7px]" in arbitrary
    assert "11px" in arbitrary
    assert "p-[16px]" not in arbitrary
    assert adherence < 80.0
    assert score < 70.0
    assert any("valores arbitrários" in r for r in recs)


def test_dom_depth_divsoup_and_asymmetric_icons() -> None:
    """Valida detecção de divsoup (> 0.45), profundidade DOM (> 12) e ícone assimétrico."""
    deep_divs = "".join("<div>" for _ in range(14)) + "<svg width='22' height='18'></svg>" + "".join("</div>" for _ in range(14))
    report = auditor.evaluate_source(deep_divs, "BrokenDOM.html")
    assert report.max_dom_depth == 15
    assert report.divsoup_ratio > 0.45
    assert report.standard_icon_sizes is False
    assert report.verdict == "FAIL"


def test_reflow_transitions_and_elite_pass() -> None:
    """Garante reprovação de transições que causam reflow e aprovação de componente elite."""
    reflow_html = "<style>.bad { transition: width 200ms ease, margin 150ms linear; }</style><main></main>"
    bad_rep = auditor.evaluate_source(reflow_html, "Reflow.html")
    assert bad_rep.zero_reflow_motion is False
    assert bad_rep.verdict == "FAIL"

    assert auditor._run_self_test() == 0
