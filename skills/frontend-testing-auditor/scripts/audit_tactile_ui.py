#!/usr/bin/env python3
"""
audit_tactile_ui.py (v4.5.0-soft)
Motor Determinístico Zero-LLM de Auditoria de Frontend Tátil & Minimalist Impact (DESIGN.md v4.5-soft).

Executa 4 suítes determinísticas sobre repositórios React/Next.js/Vue/HTML/CSS:
  - AUDIT-VIS-01  (20%): Fidelidade Tonal 135°, adoção real de .ui-card-soft / <SoftCard /> nas views,
                         banimento de Azul Cobalto/Neon, Glassmorphism (backdrop-blur), gradientes IA,
                         excesso de bordas duras 1px, micro-tipografia (10px/11px) e emojis em controles.
  - AUDIT-STATE-01(30%): Determinismo de Estados Finitos (FSM: idle/loading/error/pressed) SEM comment-gaming
                         + verificação física de #sidebar-active-tracker.
  - AUDIT-A11Y-01 (35%): Semântica WCAG 2.1 AA, foco sem neon, aria-live, tabular-nums e reduced-motion.
  - AUDIT-SEC-01  (15%): Prevenção XSS (banimento de dangerouslySetInnerHTML sem DOMPurify e eval).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

IGNORE_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", ".venv", "venv",
    "coverage", "__pycache__", ".pytest_cache", "tests", "__tests__", "test",
}
NON_PRIMITIVE_EXCLUDES = {
    "SoftCard.tsx", "BentoStudioCard.tsx", "BentoGridShell.tsx", "main.tsx", "index.tsx",
}
TACTILE_PRIMITIVES = (
    "SoftCard", "BentoStudioCard", "ui-card-soft", "ui-btn-tactile", "surface-inset", "surface-raised",
)
CANONICAL_TOKENS = (
    "--surface-canvas", "--surface-inset", "--surface-raised", "--accent-point", "--ease-spring",
)

COBALT_HEX_RE = re.compile(r"#(?:0044ff|0057ff|233dff|1d4ed8|2563eb|3b82f6|00ff66|ff00ff)\b", re.IGNORECASE)
COBALT_TW_RE = re.compile(r"\b(?:bg|text|border|ring|from|to|via)-(?:blue|indigo|violet|purple|fuchsia)-(?:400|500|600|700)\b")
GLASS_RE = re.compile(r"(?:backdrop-filter\s*:\s*blur|backdrop-blur(?:-[a-z0-9]+)?\b)", re.IGNORECASE)
HARD_BORDER_TW_RE = re.compile(r"\bborder-(?:slate|gray|zinc|neutral|amber|sky|emerald|red|blue|indigo)-(?:200|300|400|500|600|700|800)(?:/\d+)?\b")
GENERIC_GRADIENT_RE = re.compile(r"\bbg-gradient-to-(?:t|tr|r|br|b|bl|l|tl)\b")
MICRO_TEXT_RE = re.compile(r"\btext-\[(?:9|10|11)px\]")
EMOJI_UI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
COMMENT_SINGLE_RE = re.compile(r"//.*?$", re.MULTILINE)
COMMENT_MULTI_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def strip_code_comments(source: str) -> str:
    """Remove comentários // e /* */ para impedir comment-gaming de FSM e tokens."""
    return COMMENT_SINGLE_RE.sub("", COMMENT_MULTI_RE.sub("", source))


def collect_frontend_files(target_dir: Path) -> Tuple[List[Path], List[Path], List[Path]]:
    """Retorna (view_files, style_files, all_ui_files) ignorando diretórios de build/testes."""
    view_files: List[Path] = []
    style_files: List[Path] = []
    for p in target_dir.rglob("*"):
        if not p.is_file() or any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.name.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx")):
            continue
        suffix = p.suffix.lower()
        if suffix in {".tsx", ".jsx", ".vue", ".html"}:
            view_files.append(p)
        elif suffix in {".css", ".scss"}:
            style_files.append(p)
    return view_files, style_files, view_files + style_files


def _check_tactile_adoption(all_views_clean: Dict[Path, str], findings: List[str]) -> Tuple[float, int, int]:
    """Verifica adoção real de <SoftCard /> / .ui-card-soft nas views não primitivas."""
    non_primitive = [f for f in all_views_clean if f.name not in NON_PRIMITIVE_EXCLUDES]
    adopted = [
        f.name for f in non_primitive
        if any(tok in all_views_clean[f] for tok in TACTILE_PRIMITIVES)
    ]
    penalty = 0.0
    if non_primitive and (len(adopted) / len(non_primitive)) < 0.5:
        ratio = len(adopted) / len(non_primitive)
        penalty = 25.0
        findings.append(
            f"[FAIL: ORPHAN-SOFTCARD] Adoção real de primitivos táteis nas views é "
            f"{len(adopted)}/{len(non_primitive)} ({ratio:.0%}). <SoftCard /> / .ui-card-soft "
            f"não podem ser placebo órfão (-25 pts)"
        )
    return penalty, len(adopted), len(non_primitive)


def _check_visual_prohibitions(
    combined_all: str, combined_views: str, findings: List[str]
) -> Tuple[float, Dict[str, int]]:
    """Avalia proibições visuais: cobalto, glassmorphism, bordas 1px, gradientes, micro-texto e emojis."""
    penalty = 0.0
    cobalt_hex = COBALT_HEX_RE.findall(combined_all)
    cobalt_tw = COBALT_TW_RE.findall(combined_views)
    if cobalt_hex or cobalt_tw:
        penalty += 20.0
        findings.append(
            f"[FAIL: ANTI-COBALT] Detectado azul cobalto/neon proibido: "
            f"hex={set(cobalt_hex)} tw={set(cobalt_tw[:5])} (-20 pts)"
        )

    glass_hits = GLASS_RE.findall(combined_all)
    if glass_hits:
        p_glass = min(20.0, len(glass_hits) * 5.0)
        penalty += p_glass
        findings.append(f"[FAIL: ANTI-GLASSMORPHISM] Detectadas {len(glass_hits)} ocorrências de backdrop-blur / blur() (-{p_glass:.0f} pts)")

    hard_borders = HARD_BORDER_TW_RE.findall(combined_views)
    if len(hard_borders) > 6:
        p_border = min(20.0, (len(hard_borders) - 6) * 0.5)
        penalty += p_border
        findings.append(f"[FAIL: HARD-BORDERS-1PX] Detectadas {len(hard_borders)} classes de borda 1px genérica (limite = 6) (-{p_border:.1f} pts)")

    gradients = GENERIC_GRADIENT_RE.findall(combined_views)
    if gradients:
        p_grad = min(15.0, len(gradients) * 5.0)
        penalty += p_grad
        findings.append(f"[FAIL: GENERIC-AI-GRADIENT] Detectados {len(gradients)} gradientes lineares Tailwind (bg-gradient-to-*) (-{p_grad:.0f} pts)")

    micro_hits = MICRO_TEXT_RE.findall(combined_views)
    if micro_hits:
        p_micro = min(15.0, len(micro_hits) * 1.5)
        penalty += p_micro
        findings.append(f"[FAIL: MICRO-TYPOGRAPHY] Detectadas {len(micro_hits)} ocorrências de micro-fonte (text-[10px]/text-[11px]) (-{p_micro:.1f} pts)")

    emoji_hits = EMOJI_UI_RE.findall(combined_views)
    if emoji_hits:
        p_emoji = min(10.0, len(emoji_hits) * 2.0)
        penalty += p_emoji
        findings.append(f"[FAIL: EMOJI-IN-UI] Detectados {len(emoji_hits)} emojis em templates de UI (-{p_emoji:.0f} pts)")

    counts = {
        "hard_borders_1px_count": len(hard_borders),
        "glassmorphism_blur_count": len(glass_hits),
        "micro_text_10_11px_count": len(micro_hits),
        "generic_gradients_count": len(gradients),
        "emoji_in_ui_count": len(emoji_hits),
    }
    return penalty, counts


def audit_tokens_and_visuals(
    target_dir: Path, view_files: List[Path], style_files: List[Path]
) -> Dict[str, Any]:
    """AUDIT-VIS-01: Camadas tonais 135°, adoção real de SoftCard e proibição de IA genérica."""
    del target_dir
    score = 100.0
    findings: List[str] = []

    all_css = "\n".join(strip_code_comments(f.read_text(encoding="utf-8", errors="ignore")) for f in style_files)
    all_views_clean = {f: strip_code_comments(f.read_text(encoding="utf-8", errors="ignore")) for f in view_files}
    combined_views = "\n".join(all_views_clean.values())
    combined_all = all_css + "\n" + combined_views

    missing_tokens = [t for t in CANONICAL_TOKENS if t not in combined_all]
    if missing_tokens:
        p_tok = min(25.0, len(missing_tokens) * 5.0)
        score -= p_tok
        findings.append(f"[FAIL: TOKENS-V4.5] Tokens canônicos ausentes no CSS/HTML: {', '.join(missing_tokens)} (-{p_tok:.0f} pts)")

    p_adopt, adopted_cnt, total_non_prim = _check_tactile_adoption(all_views_clean, findings)
    p_prohib, counts = _check_visual_prohibitions(combined_all, combined_views, findings)
    score -= (p_adopt + p_prohib)
    counts["tactile_views_adopted"] = adopted_cnt
    counts["total_non_primitive_views"] = total_non_prim

    return {"score": round(max(0.0, score), 2), "metrics": counts, "findings": findings}


def audit_fsm_and_tracker(view_files: List[Path], style_files: List[Path]) -> Dict[str, Any]:
    """AUDIT-STATE-01: Verifica FSM real (sem comentários) e #sidebar-active-tracker deslizante."""
    score = 100.0
    findings: List[str] = []
    raw_views = "\n".join(f.read_text(encoding="utf-8", errors="ignore") for f in view_files)
    clean_views = strip_code_comments(raw_views)
    clean_css = "\n".join(strip_code_comments(f.read_text(encoding="utf-8", errors="ignore")) for f in style_files)
    combined_clean = clean_views + "\n" + clean_css

    if re.search(r"//.*?\bempty\s*\|\s*loading\s*\|\s*success\s*\|\s*error\b", raw_views, re.IGNORECASE):
        score -= 25.0
        findings.append("[FAIL: FSM-COMMENT-GAMING] Detectado comentário artificial '// empty | loading | success | error' (-25 pts)")

    has_data_state = bool(re.search(r"data-state\s*=|UIState|status\s*===\s*['\"](?:loading|error|idle)['\"]", clean_views))
    if not has_data_state:
        score -= 20.0
        findings.append("[FAIL: FSM-DATA-STATE] Views não implementam máquina de estados finitos executável (data-state / status) (-20 pts)")

    has_aria_busy = "aria-busy" in clean_views
    has_role_alert = 'role="alert"' in clean_views or "role='alert'" in clean_views
    if not has_aria_busy or not has_role_alert:
        score -= 15.0
        findings.append("[FAIL: FSM-ARIA-STATES] Ausência de aria-busy (Loading) ou role='alert' (Error) no JSX/HTML executável (-15 pts)")

    if "sidebar-active-tracker" in combined_clean:
        if re.search(r"id\s*=\s*\{\s*isActive\s*\?\s*['\"]sidebar-active-tracker['\"]", clean_views):
            score -= 20.0
            findings.append("[FAIL: FAKE-SIDEBAR-TRACKER] #sidebar-active-tracker aplicado como id condicional estático em vez de elemento deslizante (-20 pts)")
    else:
        score -= 15.0
        findings.append("[FAIL: MISSING-SIDEBAR-TRACKER] #sidebar-active-tracker ausente na Tactile Companion Sidebar (-15 pts)")

    return {"score": round(max(0.0, score), 2), "findings": findings}


def audit_a11y_and_ergonomics(view_files: List[Path], style_files: List[Path]) -> Dict[str, Any]:
    """AUDIT-A11Y-01: Acessibilidade WCAG 2.1 AA, anti-squish, tabular-nums e reduced-motion."""
    score = 100.0
    findings: List[str] = []
    clean_all = "\n".join(strip_code_comments(f.read_text(encoding="utf-8", errors="ignore")) for f in (view_files + style_files))
    checks = [
        ("prefers-reduced-motion", 20.0, "Ausência de @media (prefers-reduced-motion: reduce)"),
        ("tabular-nums", 15.0, "Ausência de font-variant-numeric: tabular-nums para dados numéricos"),
        ("focus-visible", 20.0, "Ausência de anel de foco acessível :focus-visible"),
        ("aria-live", 15.0, "Ausência de região aria-live ('polite' / 'assertive')"),
    ]
    for token, penalty, msg in checks:
        if token not in clean_all:
            score -= penalty
            findings.append(f"[FAIL: A11Y-{token.upper()}] {msg} (-{penalty:.0f} pts)")
    return {"score": round(max(0.0, score), 2), "findings": findings}


def audit_security_xss(view_files: List[Path]) -> Dict[str, Any]:
    """AUDIT-SEC-01: Prevenção XSS em templates de UI."""
    score = 100.0
    findings: List[str] = []
    clean_views = "\n".join(strip_code_comments(f.read_text(encoding="utf-8", errors="ignore")) for f in view_files)
    if "dangerouslySetInnerHTML" in clean_views and "DOMPurify" not in clean_views:
        score -= 50.0
        findings.append("[FAIL: SEC-XSS] Uso de dangerouslySetInnerHTML sem sanitização DOMPurify (-50 pts)")
    if re.search(r"\beval\s*\(", clean_views):
        score -= 50.0
        findings.append("[FAIL: SEC-EVAL] Uso de eval() detectado na camada de UI (-50 pts)")
    return {"score": round(max(0.0, score), 2), "findings": findings}


def run_audit(target_dir: Path) -> Dict[str, Any]:
    """Executa as 4 suítes determinísticas e consolida o Readiness Score."""
    view_files, style_files, all_files = collect_frontend_files(target_dir)
    if not all_files:
        return {
            "target": str(target_dir), "status": "NO_UI_FILES", "readiness_score": 0.0,
            "verdict": "FAIL", "error": "Nenhum arquivo .tsx, .jsx, .vue, .html ou .css encontrado.",
        }

    vis = audit_tokens_and_visuals(target_dir, view_files, style_files)
    fsm = audit_fsm_and_tracker(view_files, style_files)
    a11y = audit_a11y_and_ergonomics(view_files, style_files)
    sec = audit_security_xss(view_files)

    readiness = round((0.35 * a11y["score"]) + (0.30 * fsm["score"]) + (0.20 * vis["score"]) + (0.15 * sec["score"]), 2)
    verdict = "PASS" if (readiness >= 90.0 and vis["score"] >= 85.0 and fsm["score"] >= 85.0) else "FAIL"
    return {
        "target": str(target_dir),
        "files_scanned": {"views": len(view_files), "styles": len(style_files)},
        "scores": {
            "s_a11y_weight_35": a11y["score"], "s_fsm_weight_30": fsm["score"],
            "s_tokens_vis_weight_20": vis["score"], "s_sec_weight_15": sec["score"],
            "readiness_score": readiness,
        },
        "metrics": vis["metrics"],
        "verdict": verdict,
        "findings": vis["findings"] + fsm["findings"] + a11y["findings"] + sec["findings"],
    }


def _print_human_report(report: Dict[str, Any]) -> None:
    """Imprime o relatório legível para humanos no stdout."""
    print("=== AUDIT-TACTILE-UI (DESIGN.md v4.5-soft) ===")
    print(f"Alvo: {report['target']}")
    if "scores" not in report:
        print(f"[{report['verdict']}] {report.get('error')}")
        return
    s = report["scores"]
    print(
        f"Scores -> A11y(35%): {s['s_a11y_weight_35']} | FSM(30%): {s['s_fsm_weight_30']} "
        f"| Tokens/Vis(20%): {s['s_tokens_vis_weight_20']} | Sec(15%): {s['s_sec_weight_15']}"
    )
    print(f"Readiness Score Final: {s['readiness_score']} / 100.0 -> [{report['verdict']}]")
    print(f"Métricas Visuais: {json.dumps(report['metrics'], ensure_ascii=False)}")
    if report["findings"]:
        print("\nDiscrepâncias Detectadas:")
        for item in report["findings"]:
            print(f"  - {item}")
    else:
        print("\n[PASS] Zero discrepâncias táteis ou de FSM detectadas.")


def main() -> int:
    """Ponto de entrada CLI do auditor de UI tátil."""
    parser = argparse.ArgumentParser(description="Auditor determinístico de Frontend Tátil & Minimalist Impact (DESIGN.md v4.5-soft).")
    parser.add_argument("--target", type=str, required=True, help="Caminho do repositório ou diretório frontend a ser auditado.")
    parser.add_argument("--json", action="store_true", help="Emite resultado estritamente em JSON.")
    args = parser.parse_args()

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(json.dumps({"error": f"Caminho não encontrado: {target_path}"}), file=sys.stderr)
        return 1

    report = run_audit(target_path)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        _print_human_report(report)
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
