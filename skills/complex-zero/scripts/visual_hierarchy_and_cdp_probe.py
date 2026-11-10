#!/usr/bin/env python3
"""
visual_hierarchy_and_cdp_probe.py
Motor compartilhado de auditoria estrutural, hierarquia visual, descompactação de menus,
anti-proliferação de abas (reuso de slots existentes) e sonda Chrome DevTools / CDP
para a fusão operacional `complex-zero` (v3.0.0) <-> `nav-x-func` (v6.0.0).
"""

from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List

INLINE_FONT_SIZE_PX_RE = re.compile(
    r"style\s*=\s*['\"][^'\"]*?\bfont-size\s*:\s*(\d+(?:\.\d+)?)\s*px",
    re.IGNORECASE,
)
CSS_BLOCK_RE = re.compile(r"([^{};]+)\{([^{}]*)\}", re.DOTALL)
FONT_SIZE_DECL_RE = re.compile(r"\bfont-size\s*:\s*(\d+(?:\.\d+)?)\s*px\b", re.IGNORECASE)
GAP_DECL_RE = re.compile(r"\bgap\s*:\s*(\d+(?:\.\d+)?)\s*px\b", re.IGNORECASE)
MIN_BLOCK_DECL_RE = re.compile(
    r"\b(?:min-block-size|min-height)\s*:\s*(\d+(?:\.\d+)?)\s*px\b",
    re.IGNORECASE,
)
PADDING_COMPACT_RE = re.compile(
    r"<button\b[^>]*?style\s*=\s*['\"][^'\"]*?\bpadding\s*:\s*([0-5])px\s+([0-9])px\b",
    re.IGNORECASE,
)
NAV_TAG_RE = re.compile(r"<nav\b[^>]*>", re.IGNORECASE)
ROLE_TAB_RE = re.compile(r"\brole\s*=\s*['\"]tab['\"]", re.IGNORECASE)
SUBTAB_CALL_RE = re.compile(
    r"\b(?:switchNodesSubview|setCatalogTreeMode|setCatalogCategoryFilter|switchSubTab)\s*\(",
    re.IGNORECASE,
)
PRIMARY_TAB_CALL_RE = re.compile(
    r"\b(?:switchCanvasTab|switchTab|setActiveTab)\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
    re.IGNORECASE,
)
TEXT_INPUT_RE = re.compile(
    r"<(?:textarea\b|input\b[^>]*?\btype\s*=\s*['\"](?:text|search)['\"])",
    re.IGNORECASE,
)
HARDCODED_NODE_PASS_RE = re.compile(
    r"(?:tag\s*\+\s*['\"]\s*\[PASS\]['\"]|\[(?:DIR|FILE|IMG|MD)\]\s*\[PASS\])"
)
METRIC_BADGE_OCCURRENCE_RE = re.compile(r"class\s*=\s*['\"][^'\"]*\bmetric-badge\b", re.IGNORECASE)

MENU_SELECTOR_TOKENS = (
    ".mode-switcher",
    ".mode-btn",
    ".chip-btn",
    ".canvas-tabs",
    ".canvas-tab",
    ".nav-",
    "nav ",
    "[role=\"tab\"]",
    "[role=\"tablist\"]",
    ".toolbar",
    ".tab-",
)

CHROME_DEVTOOLS_EVALUATE_SCRIPT = """() => {
  const getPx = (el, prop) => parseFloat(window.getComputedStyle(el)[prop] || '0') || 0;
  const isVis = (el) => {
    const r = el.getBoundingClientRect();
    const s = window.getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity || '1') > 0;
  };
  const h1 = document.querySelector('h1'), h2 = document.querySelector('h2'), h3 = document.querySelector('h3');
  const h1Px = h1 ? getPx(h1, 'fontSize') : 0;
  const h2Px = h2 ? getPx(h2, 'fontSize') : 0;
  const h3Px = h3 ? getPx(h3, 'fontSize') : 0;
  const bodyPx = getPx(document.body, 'fontSize');
  const hierarchyMonotonic = (!h1 || !h2 || h1Px > h2Px) && (!h2 || bodyPx <= h2Px);

  const crampedMenus = [];
  document.querySelectorAll('nav, [role="tablist"], .mode-switcher, .canvas-tabs').forEach((navEl, idx) => {
    if (!isVis(navEl)) return;
    const gapPx = getPx(navEl, 'gap') || getPx(navEl, 'columnGap');
    const items = Array.from(navEl.querySelectorAll('button, a, [role="tab"]')).filter(isVis);
    if (gapPx > 0 && gapPx < 6) {
      crampedMenus.push(`nav#${navEl.id || idx}: gap=${gapPx}px (< 6px)`);
    }
    if (items.length > 6) {
      crampedMenus.push(`nav#${navEl.id || idx}: ${items.length} itens acumulados na mesma barra (> 6)`);
    }
    items.forEach((btn) => {
      const fz = getPx(btn, 'fontSize');
      const r = btn.getBoundingClientRect();
      if (fz < 13) crampedMenus.push(`${btn.tagName.toLowerCase()}#${btn.id || btn.textContent.trim().slice(0, 18)}: fontSize=${fz}px (< 13px)`);
      if (btn.scrollWidth > btn.clientWidth + 2) crampedMenus.push(`${btn.tagName.toLowerCase()}#${btn.id || btn.textContent.trim().slice(0, 18)}: scrollWidth(${btn.scrollWidth}) > clientWidth(${btn.clientWidth})`);
      if (r.height < 40) crampedMenus.push(`${btn.tagName.toLowerCase()}#${btn.id || btn.textContent.trim().slice(0, 18)}: height=${Math.round(r.height)}px (< 40px)`);
    });
  });

  const visibleNavs = Array.from(document.querySelectorAll('nav')).filter(isVis).length;
  const allTabs = document.querySelectorAll('[role="tab"]').length;
  const visibleInputs = Array.from(document.querySelectorAll('textarea, input[type="text"], input[type="search"], input:not([type])')).filter(isVis).length;

  return {
    pageMetadata: {
      title: document.title,
      hasViewportMeta: Boolean(document.querySelector('meta[name="viewport"]')),
      hasDescriptionMeta: Boolean(document.querySelector('meta[name="description"]')),
      theme: document.documentElement.getAttribute('data-theme') || 'default',
    },
    visualHierarchy: { h1Px, h2Px, h3Px, bodyPx, hierarchyMonotonic },
    organizationSprawl: { visibleNavs, allTabs, visibleInputs },
    crampedMenus,
    passed: hierarchyMonotonic && crampedMenus.length === 0 && visibleNavs <= 3 && allTabs <= 4 && visibleInputs <= 2,
  };
}"""


@dataclass
class UnifiedVisualOrgReport:
    """Relatório consolidado dos detectores de organização, hierarquia visual e menus."""

    nav_landmarks_count: int = 0
    primary_tabs_count: int = 0
    nested_subtab_calls: int = 0
    concurrent_text_inputs: int = 0
    inline_micro_font_count: int = 0
    tiny_font_declarations: List[str] = field(default_factory=list)
    cramped_menu_violations: List[str] = field(default_factory=list)
    sprawl_and_org_violations: List[str] = field(default_factory=list)
    hierarchy_violations: List[str] = field(default_factory=list)
    graph_node_violations: List[str] = field(default_factory=list)
    org_penalty_points: int = 0
    hierarchy_menu_penalty_points: int = 0
    graph_penalty_points: int = 0


def _inspect_css_blocks_for_menus_and_fonts(
    combined: str,
    tiny_fonts: List[str],
    cramped_menus: List[str],
) -> None:
    """Inspeciona blocos CSS em busca de menus compactados (gap < 6px, font < 13px) e micro-fontes."""
    for match in CSS_BLOCK_RE.finditer(combined):
        selector = " ".join(match.group(1).strip().split())
        body = match.group(2)
        if not selector or selector.startswith("@"):
            continue
        sel_low = selector.lower()
        is_menu_sel = any(tok in sel_low for tok in MENU_SELECTOR_TOKENS)

        for fz_m in FONT_SIZE_DECL_RE.finditer(body):
            px_val = float(fz_m.group(1))
            if px_val < 12.0:
                tiny_fonts.append(f"{selector} {{ font-size: {px_val:g}px (< 12px) }}")
            elif is_menu_sel and px_val < 13.0:
                cramped_menus.append(
                    f"Menu/Botão com tipografia comprimida em '{selector}': font-size: {px_val:g}px (< 13px)"
                )

        if is_menu_sel:
            for gap_m in GAP_DECL_RE.finditer(body):
                gap_val = float(gap_m.group(1))
                if gap_val < 6.0:
                    cramped_menus.append(
                        f"Barra de navegação compactada em '{selector}': gap: {gap_val:g}px (< 6px)"
                    )


def _inspect_inline_styles_and_templates(
    combined: str,
    report: UnifiedVisualOrgReport,
) -> None:
    """Detecta poluição de micro-fontes inline, botões de menu espremidos e excesso de abas/inputs."""
    inline_fz = [float(m.group(1)) for m in INLINE_FONT_SIZE_PX_RE.finditer(combined)]
    micro_inline = [px for px in inline_fz if px <= 13.0]
    report.inline_micro_font_count = len(micro_inline)

    if len(micro_inline) > 4:
        report.hierarchy_violations.append(
            f"Poluição tipográfica inline: {len(micro_inline)} elementos com style='font-size: 11px..13px' hardcoded achatando a hierarquia visual"
        )

    for min_m in MIN_BLOCK_DECL_RE.finditer(combined):
        val = float(min_m.group(1))
        if val < 40.0:
            report.cramped_menu_violations.append(
                f"Alvo interativo espremido: min-block-size/min-height de {val:g}px (< 40px/44px)"
            )

    for pad_m in PADDING_COMPACT_RE.finditer(combined):
        report.cramped_menu_violations.append(
            f"Padding de botão/pílula excessivamente compactado: padding: {pad_m.group(1)}px {pad_m.group(2)}px"
        )

    for nav_tag in NAV_TAG_RE.findall(combined):
        gap_m = GAP_DECL_RE.search(nav_tag)
        if gap_m and float(gap_m.group(1)) < 6.0:
            report.cramped_menu_violations.append(
                f"<nav> com espaçamento inline espremido (gap: {gap_m.group(1)}px < 6px)"
            )


def _inspect_sprawl_and_graph_nodes(combined: str, report: UnifiedVisualOrgReport) -> None:
    """Audita proliferação de abas, sub-abas aninhadas, excesso de <nav>, inputs e nós de grafo."""
    report.nav_landmarks_count = len(NAV_TAG_RE.findall(combined))
    role_tabs = len(ROLE_TAB_RE.findall(combined))
    unique_tab_targets = len(set(PRIMARY_TAB_CALL_RE.findall(combined)))
    report.primary_tabs_count = max(role_tabs, unique_tab_targets)
    report.nested_subtab_calls = len(SUBTAB_CALL_RE.findall(combined))
    report.concurrent_text_inputs = len(TEXT_INPUT_RE.findall(combined))

    if report.nav_landmarks_count > 3:
        report.sprawl_and_org_violations.append(
            f"Excesso de barras <nav> ({report.nav_landmarks_count} detectadas > limite de 3 Camadas: Global, Local e Breadcrumbs)"
        )
    if report.primary_tabs_count > 4:
        report.sprawl_and_org_violations.append(
            f"Proliferação de abas primárias ({report.primary_tabs_count} abas > limite de 4): consolide nos slots existentes"
        )
    if report.primary_tabs_count > 0 and report.nested_subtab_calls > 0:
        report.sprawl_and_org_violations.append(
            f"Sub-abas/filtros aninhados dentro de abas ({report.nested_subtab_calls} chamadas de sub-view): proibido criar abas dentro de abas"
        )
    if report.concurrent_text_inputs > 3:
        report.sprawl_and_org_violations.append(
            f"Múltiplos campos de entrada/busca/chat competindo na mesma interface ({report.concurrent_text_inputs} inputs > 3): unifique em 1 Command Bar/Composer"
        )

    if HARDCODED_NODE_PASS_RE.search(combined):
        report.graph_node_violations.append(
            "Nó do grafo com badge '[PASS]' hardcoded no template sem validação real (Placebo Visual)"
        )
    badge_count = len(METRIC_BADGE_OCCURRENCE_RE.findall(combined))
    if badge_count >= 3 and "fs-node-box" in combined:
        report.graph_node_violations.append(
            f"Superlotação visual no nó do grafo ({badge_count} metric-badges espremidos dentro do mesmo card de nó)"
        )


def analyze_visual_hierarchy_and_organization(combined_source: str) -> UnifiedVisualOrgReport:
    """Executa a análise estática profunda de organização, hierarquia visual, menus e grafos."""
    report = UnifiedVisualOrgReport()
    _inspect_css_blocks_for_menus_and_fonts(
        combined_source,
        report.tiny_font_declarations,
        report.cramped_menu_violations,
    )
    _inspect_inline_styles_and_templates(combined_source, report)
    _inspect_sprawl_and_graph_nodes(combined_source, report)

    if report.tiny_font_declarations:
        report.hierarchy_violations.extend(report.tiny_font_declarations[:5])

    if report.sprawl_and_org_violations:
        report.org_penalty_points = min(20, len(report.sprawl_and_org_violations) * 7)
    if report.cramped_menu_violations or report.hierarchy_violations:
        total_hm = len(report.cramped_menu_violations) + len(report.hierarchy_violations)
        report.hierarchy_menu_penalty_points = min(20, total_hm * 6)
    if report.graph_node_violations:
        report.graph_penalty_points = min(15, len(report.graph_node_violations) * 8)

    return report


def probe_live_url_metadata(live_url: str, timeout_sec: float = 5.0) -> Dict[str, Any]:
    """Inspeciona o HTML/CSS servido ao vivo em `live_url` e avalia metadados, hierarquia e menus."""
    if not live_url.startswith(("http://", "https://")):
        return {"reachable": False, "error": "URL deve iniciar com http:// ou https://"}
    try:
        req = urllib.request.Request(live_url, headers={"User-Agent": "ComplexZero-NavXFunc-Probe/3.0"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            status_code = resp.status
    except Exception as exc:  # noqa: BLE001
        return {"reachable": False, "url": live_url, "error": str(exc)}

    org_rep = analyze_visual_hierarchy_and_organization(html)
    has_title = bool(re.search(r"<title>[^<]+</title>", html, re.IGNORECASE))
    has_viewport = bool(re.search(r"<meta[^>]+name=['\"]viewport['\"]", html, re.IGNORECASE))
    return {
        "reachable": True,
        "url": live_url,
        "http_status": status_code,
        "has_title": has_title,
        "has_viewport_meta": has_viewport,
        "live_dom_analysis": asdict(org_rep),
    }


def main() -> int:
    """CLI auxiliar para exportar o script Chrome DevTools MCP ou sondar uma URL ao vivo."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Sonda Visual, Hierárquica e CDP (complex-zero + nav-x-func)")
    parser.add_argument("--dump-cdp-script", action="store_true", help="Imprime o script JS para evaluate_script do Chrome DevTools MCP")
    parser.add_argument("--live-url", type=str, default="", help="URL ao vivo para sondagem de HTML/CSS renderizado")
    args = parser.parse_args()

    if args.dump_cdp_script:
        sys.stdout.write(CHROME_DEVTOOLS_EVALUATE_SCRIPT + "\n")
        return 0
    if args.live_url:
        sys.stdout.write(json.dumps(probe_live_url_metadata(args.live_url), indent=2, ensure_ascii=False) + "\n")
        return 0
    sys.stdout.write(json.dumps({"status": "READY", "module": "visual_hierarchy_and_cdp_probe"}, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
