#!/usr/bin/env python3
"""
complex_zero_ast_auditor.py
Auditor determinístico unificado Zero-LLM da fusão `complex-zero` (v3.0.0) <-> `nav-x-func` (v6.0.0).
Avalia os 4 Eixos (25 pts cada = 100 pts) + Ponte SGA/TIF (`nav-x-func`) + Sonda Visual/DOM Chrome DevTools:
  - Eixo 1 (25 pts): Interatividade semântica, :focus-visible, pointer: coarse (>=48px), reduced-motion e Descompactação de Menus (font >= 13px, gap >= 6px, min-block-size >= 40px).
  - Eixo 2 (25 pts): Organização Macro/Micro (`@container`), Tokens OKLCH, Hierarquia Visual Monotônica (zero poluição de micro-fontes 11px/12px inline) e Anti-Proliferação de Abas/Navs (reuso de slots existentes).
  - Eixo 3 (25 pts): Grafo `@xyflow/react`, AST anti-fake (corpos vazios {}, console.log stubs, Math.random(), Ghost Nodes e zero '[PASS]' hardcoded / superlotação de badges nos nós).
  - Eixo 4 (25 pts): Next.js 15+ App Router async params/searchParams (`Promise<...>`) + Inspeção Live Chrome DevTools / Metadados DOM (`--live-url` / `--dump-cdp-script`).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from visual_hierarchy_and_cdp_probe import (  # noqa: E402
    CHROME_DEVTOOLS_EVALUATE_SCRIPT,
    UnifiedVisualOrgReport,
    analyze_visual_hierarchy_and_organization,
    probe_live_url_metadata,
)

FRONTEND_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".css", ".html"}
IGNORED_DIRS = {
    "node_modules", ".next", ".venv", "venv", ".git",
    "dist", "build", "__pycache__", ".pytest_cache",
}

EMPTY_ARROW_OR_FN_RE = re.compile(
    r"(?:=>\s*\{\s*\}|function\s+[a-zA-Z0-9_]*\s*\([^)]*\)\s*\{\s*\})"
)
CONSOLE_ONLY_BODY_RE = re.compile(r"=>\s*\{\s*console\.log\([^}]*\)\s*;?\s*\}")
FAKE_TELEMETRY_RANDOM_RE = re.compile(
    r"(?:fps|cpu|latency|memory|metric)[a-zA-Z0-9_]*\s*:\s*[^,\n]*Math\.random\(\)",
    re.IGNORECASE,
)
HARDCODED_OKLCH_VALID_RE = re.compile(r"oklchContrastValid\s*:\s*true\b")
DIV_ONCLICK_NO_ROLE_RE = re.compile(r"<div\b(?![^>]*\brole=)[^>]*\bonClick=", re.IGNORECASE)
OUTLINE_NONE_RE = re.compile(r"outline\s*:\s*(?:none|0)\b")
FOCUS_VISIBLE_RE = re.compile(r":focus-visible\b")
POINTER_COARSE_RE = re.compile(r"any-pointer\s*:\s*coarse|pointer\s*:\s*coarse")
REDUCED_MOTION_RE = re.compile(r"prefers-reduced-motion\s*:\s*reduce")
CONTAINER_QUERY_RE = re.compile(r"@container\b|container-type\s*:\s*inline-size")
OKLCH_RE = re.compile(r"oklch\(")
TABULAR_NUMS_RE = re.compile(r"tabular-nums")
LEGACY_REACTFLOW_IMPORT_RE = re.compile(r"from\s+['\"]reactflow['\"]")
SYNC_NEXT15_PARAMS_RE = re.compile(
    r"export\s+default\s+function\s+\w+\s*\(\s*\{\s*params\s*\}\s*:\s*\{\s*params\s*:\s*\{\s*\w+\s*:\s*string"
)
ASYNC_NEXT15_PARAMS_RE = re.compile(r"Promise<\s*\{[^}]*\}\s*>")


def _strip_comments(text: str) -> str:
    """Remove comentários de linha e bloco para evitar falsos positivos/gaming."""
    no_block = re.sub(r"/\*[\s\S]*?\*/", "", text)
    return re.sub(r"//[^\n]*", "", no_block)


def _evaluate_axis_1_interactivity_and_menus(
    combined: str,
    has_css: bool,
    org_rep: UnifiedVisualOrgReport,
    findings: List[Dict[str, Any]],
) -> int:
    """Calcula o Eixo 1 (25 pts): Semântica, Foco, Lei de Fitts e Descompactação de Menus."""
    score = 25
    div_clicks = len(DIV_ONCLICK_NO_ROLE_RE.findall(combined))
    if div_clicks > 0:
        penalty = min(10, div_clicks * 5)
        score -= penalty
        findings.append({
            "axis": 1, "severity": "WARN", "rule": "SEMANTIC_BUTTON",
            "detail": f"{div_clicks} <div onClick> sem role explícito (-{penalty} pts)",
        })

    if OUTLINE_NONE_RE.search(combined) and not FOCUS_VISIBLE_RE.search(combined):
        score -= 10
        findings.append({
            "axis": 1, "severity": "CRITICAL", "rule": "FOCUS_VISIBLE_MISSING",
            "detail": "outline: none detectado sem regra :focus-visible (-10 pts)",
        })

    if has_css and not POINTER_COARSE_RE.search(combined):
        score -= 5
        findings.append({
            "axis": 1, "severity": "WARN", "rule": "FITTS_COARSE_POINTER",
            "detail": "Ausência de @media (any-pointer: coarse) para alvos >= 48x48px (-5 pts)",
        })

    if has_css and not REDUCED_MOTION_RE.search(combined):
        score -= 5
        findings.append({
            "axis": 1, "severity": "WARN", "rule": "VESTIBULAR_SAFETY",
            "detail": "Ausência de @media (prefers-reduced-motion: reduce) (-5 pts)",
        })

    if org_rep.cramped_menu_violations:
        pen = min(15, len(org_rep.cramped_menu_violations) * 5)
        score -= pen
        findings.append({
            "axis": 1, "severity": "CRITICAL", "rule": "CRAMPED_MENU_OR_BAD_TYPOGRAPHY",
            "detail": f"{len(org_rep.cramped_menu_violations)} violação(ões) de menu compactado/tipografia espremida (-{pen} pts): {org_rep.cramped_menu_violations[0]}",
            "examples": org_rep.cramped_menu_violations[:5],
        })
    return max(0, score)


def _evaluate_axis_2_organization_hierarchy_oklch(
    combined: str,
    has_css: bool,
    org_rep: UnifiedVisualOrgReport,
    findings: List[Dict[str, Any]],
) -> int:
    """Calcula o Eixo 2 (25 pts): Organização nav-x-func, Reuso Anti-Abas, Hierarquia Visual, @container e OKLCH."""
    score = 25
    if has_css and not CONTAINER_QUERY_RE.search(combined):
        score -= 10
        findings.append({
            "axis": 2, "severity": "CRITICAL", "rule": "MICRO_CONTAINER_QUERY",
            "detail": "Ausência de container-type: inline-size / @container (-10 pts)",
        })

    if has_css and not OKLCH_RE.search(combined):
        score -= 10
        findings.append({
            "axis": 2, "severity": "WARN", "rule": "OKLCH_COLOR_SPACE",
            "detail": "Tokens perceptuais oklch() não detectados (-10 pts)",
        })

    if not TABULAR_NUMS_RE.search(combined):
        score -= 5
        findings.append({
            "axis": 2, "severity": "WARN", "rule": "TABULAR_NUMS_METRICS",
            "detail": "Ausência de tabular-nums para estabilidade de telemetria (-5 pts)",
        })

    if HARDCODED_OKLCH_VALID_RE.search(combined):
        score -= 15
        findings.append({
            "axis": 2, "severity": "CRITICAL", "rule": "PLACEBO_CONTRAST_CHECK",
            "detail": "oklchContrastValid: true hardcoded sem cálculo real (-15 pts)",
        })

    if org_rep.sprawl_and_org_violations:
        pen = min(15, len(org_rep.sprawl_and_org_violations) * 6)
        score -= pen
        findings.append({
            "axis": 2, "severity": "CRITICAL", "rule": "TAB_AND_NAV_SPRAWL_NO_SLOT_REUSE",
            "detail": f"Desorganização estrutural / criação de abas extras sem reuso in-place (-{pen} pts): {'; '.join(org_rep.sprawl_and_org_violations)}",
        })

    if org_rep.hierarchy_violations:
        pen = min(15, len(org_rep.hierarchy_violations) * 5)
        score -= pen
        findings.append({
            "axis": 2, "severity": "CRITICAL", "rule": "VISUAL_HIERARCHY_FLATNESS",
            "detail": f"Quebra de hierarquia visual / micro-fontes inline (-{pen} pts): {org_rep.hierarchy_violations[0]}",
            "examples": org_rep.hierarchy_violations[:5],
        })
    return max(0, score)


def _evaluate_axis_3_graph_and_ast(
    combined: str,
    sources: Dict[str, str],
    root_dir: Path | None,
    org_rep: UnifiedVisualOrgReport,
    findings: List[Dict[str, Any]],
) -> int:
    """Calcula o Eixo 3 (25 pts): Grafo @xyflow/react, Telemetria Real, Nós Limpos e AST Anti-Fake."""
    score = 25
    if LEGACY_REACTFLOW_IMPORT_RE.search(combined):
        score -= 10
        findings.append({
            "axis": 3, "severity": "WARN", "rule": "XYFLOW_MODERN_PACKAGE",
            "detail": "Import legado 'reactflow' detectado; use '@xyflow/react' (-10 pts)",
        })

    empty_fns = len(EMPTY_ARROW_OR_FN_RE.findall(combined))
    console_stubs = len(CONSOLE_ONLY_BODY_RE.findall(combined))
    if empty_fns > 0 or console_stubs > 0:
        score -= 15
        findings.append({
            "axis": 3, "severity": "CRITICAL", "rule": "AST_FAKE_FUNCTION_STUB",
            "detail": f"Detectados {empty_fns} corpos vazios {{}} e {console_stubs} stubs console.log (-15 pts)",
        })

    if FAKE_TELEMETRY_RANDOM_RE.search(combined):
        score -= 15
        findings.append({
            "axis": 3, "severity": "CRITICAL", "rule": "FAKE_TELEMETRY_MATH_RANDOM",
            "detail": "Telemetria simulada com Math.random() detectada (-15 pts)",
        })

    if org_rep.graph_node_violations:
        pen = min(15, len(org_rep.graph_node_violations) * 8)
        score -= pen
        findings.append({
            "axis": 3, "severity": "CRITICAL", "rule": "GRAPH_NODE_PLACEBO_OR_OVERSTUFFING",
            "detail": f"Poluição ou placebo visual nos nós do grafo (-{pen} pts): {'; '.join(org_rep.graph_node_violations)}",
        })

    if root_dir is not None:
        for rel_path in sources:
            candidate = (root_dir / rel_path).resolve()
            if not candidate.exists():
                score -= 15
                findings.append({
                    "axis": 3, "severity": "CRITICAL", "rule": "GHOST_NODE_DISK_MISMATCH",
                    "detail": f"Nó fantasma sem arquivo físico: {rel_path} (-15 pts)",
                })
    return max(0, score)


def _bridge_nav_x_func_score(root_dir: Path | None) -> Dict[str, Any]:
    """Aciona o motor `deterministic_scorer.py` da skill unificada `auditoria-projetos-sistema` para consolidar SGA + TIF."""
    if root_dir is None or not root_dir.exists():
        return {"bridged": False}
    nav_script_dir = SCRIPT_DIR.parent.parent / "auditoria-projetos-sistema" / "scripts"
    if not (nav_script_dir / "deterministic_scorer.py").exists():
        return {"bridged": False}
    if str(nav_script_dir) not in sys.path:
        sys.path.insert(0, str(nav_script_dir))
    try:
        import deterministic_scorer as nav_scorer  # type: ignore

        ev, diag = nav_scorer.scan_project_tree(root_dir)
        rep = nav_scorer.calculate_architecture_score(ev, "COMPLEX_ZERO_NAVXFUNC_FUSION")
        return {
            "bridged": True,
            "sga_global_score": rep.sga_global_score,
            "ine_navigation": rep.ine_navigation,
            "ici_island_cohesion": rep.ici_island_cohesion,
            "ipc_code_purity": rep.ipc_code_purity,
            "irm_mvp_rigor": rep.irm_mvp_rigor,
            "icte_typography_structure": rep.icte_typography_structure,
            "tif_verdict": rep.tif_verdict,
            "verdict": rep.verdict,
            "diagnostics": diag,
        }
    except Exception as exc:  # noqa: BLE001
        return {"bridged": False, "error": str(exc)}


def audit_source_bundle(
    sources: Dict[str, str],
    root_dir: Path | None = None,
    live_url: str = "",
) -> Dict[str, Any]:
    """Calcula a pontuação determinística nos 4 Eixos (0 a 100) + Organização/Hierarquia + Ponte nav-x-func."""
    combined_raw = "\n".join(sources.values())
    combined = _strip_comments(combined_raw)
    has_css = any(k.endswith(".css") or "<style>" in v for k, v in sources.items())
    findings: List[Dict[str, Any]] = []

    org_rep = analyze_visual_hierarchy_and_organization(combined)
    s1 = _evaluate_axis_1_interactivity_and_menus(combined, has_css, org_rep, findings)
    s2 = _evaluate_axis_2_organization_hierarchy_oklch(combined, has_css, org_rep, findings)
    s3 = _evaluate_axis_3_graph_and_ast(combined, sources, root_dir, org_rep, findings)

    s4 = 25
    if SYNC_NEXT15_PARAMS_RE.search(combined) and not ASYNC_NEXT15_PARAMS_RE.search(combined):
        s4 -= 15
        findings.append({
            "axis": 4, "severity": "CRITICAL", "rule": "NEXTJS15_SYNC_PARAMS",
            "detail": "Acesso síncrono legado a params sem Promise<{...}> no Next.js 15+ (-15 pts)",
        })

    live_probe_result: Dict[str, Any] = {"executed": False}
    if live_url.strip():
        live_probe_result = probe_live_url_metadata(live_url.strip())
        live_probe_result["executed"] = True
        if not live_probe_result.get("reachable"):
            s4 = max(0, s4 - 10)
            findings.append({
                "axis": 4, "severity": "WARN", "rule": "LIVE_URL_UNREACHABLE",
                "detail": f"URL ao vivo inacessível para print/DOM probe ({live_url}): {live_probe_result.get('error')}",
            })

    total = s1 + s2 + s3 + s4
    verdict = "[PASS]" if total >= 90 else ("[WARN]" if total >= 75 else "[FAIL]")

    return {
        "skill": "complex-zero+nav-x-func",
        "version": "3.0.0",
        "verdict": verdict,
        "total_score": total,
        "axes": {
            "eixo_1_interatividade_fitts": s1,
            "eixo_2_macro_micro_oklch": s2,
            "eixo_3_xyflow_ast_antifake": s3,
            "eixo_4_nextjs15_async_params": s4,
        },
        "visual_organization_and_hierarchy": asdict(org_rep),
        "nav_x_func_bridge": _bridge_nav_x_func_score(root_dir),
        "live_browser_probe": live_probe_result,
        "chrome_devtools_mcp_protocol": {
            "mandatory_steps": [
                "1. navigate_page / list_pages (abrir URL real no Chrome DevTools MCP)",
                "2. take_screenshot (capturar print visual real para detectar menus espremidos, colisão de layout e bagunça de abas)",
                "3. take_snapshot (inspecionar árvore de acessibilidade, metadados e landmarks)",
                "4. evaluate_script (executar sonda JS de getComputedStyle + getBoundingClientRect via --dump-cdp-script)",
            ]
        },
        "files_analyzed": len(sources),
        "findings": findings,
    }


def _collect_target_files(target: Path) -> Dict[str, str]:
    """Lê os arquivos elegíveis de um diretório ou arquivo único."""
    if target.is_file():
        return {target.name: target.read_text(encoding="utf-8", errors="replace")}
    bundle: Dict[str, str] = {}
    for p in sorted(target.rglob("*")):
        if not p.is_file() or any(part in IGNORED_DIRS for part in p.parts):
            continue
        is_go_ui = p.suffix.lower() == ".go" and p.name.startswith("mcp_apps_ui_")
        if p.suffix.lower() in FRONTEND_EXTENSIONS or is_go_ui:
            rel = str(p.relative_to(target)).replace("\\", "/")
            bundle[rel] = p.read_text(encoding="utf-8", errors="replace")
    return bundle


def run_self_test() -> int:
    """Executa autoteste validando aprovação de UI limpa (>=90) vs. reprovação de menus compactados/abas/placebos (<50)."""
    healthy_bundle = {
        "styles.css": """
            .card-wrapper { container-type: inline-size; }
            @container (min-width: 380px) { .card { background: oklch(0.22 0.02 260); font-variant-numeric: tabular-nums; } }
            .mode-switcher { display: flex; gap: 10px; padding: 8px; }
            .mode-btn, .chip-btn { font-size: 14px; min-block-size: 44px; padding: 10px 16px; }
            .btn:focus-visible { outline: 2px solid oklch(0.68 0.17 237); }
            @media (any-pointer: coarse) { .btn { min-width: 48px; min-height: 48px; } }
            @media (prefers-reduced-motion: reduce) { .btn { transition: none; } }
        """,
        "page.tsx": """
            import { ReactFlow } from '@xyflow/react';
            export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
              const { slug } = await params;
              return <main><nav aria-label="Principal"><button className="mode-btn">{slug}</button></nav></main>;
            }
        """,
    }
    res_ok = audit_source_bundle(healthy_bundle)
    assert res_ok["verdict"] == "[PASS]" and res_ok["total_score"] == 100, f"Falha no caso saudável: {res_ok}"

    broken_bundle = {
        "bad.css": """
            .btn:focus { outline: none; }
            .mode-switcher { gap: 4px; }
            .chip-btn { font-size: 12px; padding: 4px 8px; min-block-size: 36px; }
            .canvas-tab-sub { font-size: 11px; }
        """,
        "bad.tsx": """
            import ReactFlow from 'reactflow';
            const ghostHandler = () => {};
            const fakeMetrics = { fps: Math.floor(58 + Math.random() * 3), oklchContrastValid: true };
            export default function Page({ params }: { params: { slug: string } }) {
              return (
                <div onClick={ghostHandler}>
                  <nav style="gap:4px"><button style="font-size:11px">A</button></nav>
                  <nav><button style="font-size:12px">B</button></nav>
                  <nav><button style="font-size:12px">C</button></nav>
                  <nav><button style="font-size:12px">D</button></nav>
                  <button role="tab" onClick={() => switchCanvasTab('1')} style="font-size:11px">T1</button>
                  <button onClick={() => switchNodesSubview('sub1')} style="font-size:11px">[DIR] [PASS]</button>
                  {params.slug}
                </div>
              );
            }
        """,
    }
    res_bad = audit_source_bundle(broken_bundle)
    assert res_bad["verdict"] == "[FAIL]" and res_bad["total_score"] < 40, f"Falha na detecção de placebos/menus: {res_bad}"
    print(json.dumps({
        "status": "[PASS]",
        "healthy_score": res_ok["total_score"],
        "broken_score": res_bad["total_score"],
        "broken_findings_count": len(res_bad["findings"]),
    }, ensure_ascii=False))
    return 0


def main() -> int:
    """Ponto de entrada CLI do auditor unificado complex-zero v3.0.0 + nav-x-func v6.0.0."""
    parser = argparse.ArgumentParser(description="Auditor Unificado complex-zero v3.0.0 + nav-x-func v6.0.0")
    parser.add_argument("--target", type=str, default="", help="Caminho do arquivo ou diretório a auditar")
    parser.add_argument("--live-url", type=str, default="", help="URL ao vivo para sondagem de HTML/CSS renderizado")
    parser.add_argument("--dump-cdp-script", action="store_true", help="Exporta script JS para evaluate_script do Chrome DevTools MCP")
    parser.add_argument("--self-test", action="store_true", help="Executa a suíte interna de autoteste")
    args = parser.parse_args()

    if args.dump_cdp_script:
        print(CHROME_DEVTOOLS_EVALUATE_SCRIPT)
        return 0
    if args.self_test:
        return run_self_test()
    if not args.target.strip():
        print(json.dumps({"error": "Forneça --target <path>, --dump-cdp-script ou --self-test"}, ensure_ascii=False))
        return 1

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(json.dumps({"error": f"Caminho não encontrado: {target_path}"}, ensure_ascii=False))
        return 1

    sources = _collect_target_files(target_path)
    root_dir = target_path if target_path.is_dir() else target_path.parent
    report = audit_source_bundle(sources, root_dir=root_dir, live_url=args.live_url)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["total_score"] >= 75 else 1


if __name__ == "__main__":
    sys.exit(main())
