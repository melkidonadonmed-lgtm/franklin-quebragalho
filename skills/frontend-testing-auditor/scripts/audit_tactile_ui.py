#!/usr/bin/env python3
"""
Auditor Determinístico de Arquitetura Visual por Propósito, Contraste, Tipografia, Camadas & FSM (v3.0.0)
Calcula o Readiness Score ponderado (0 a 100):
  Score = 0.35 * S_A11y + 0.30 * S_FSM + 0.20 * S_Tokens + 0.15 * S_Sec
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

COMMENT_BLOCK_RE = re.compile(r"/\*[\s\S]*?\*/")
COMMENT_LINE_RE = re.compile(r"//.*$", re.MULTILINE)
GAMED_FSM_COMMENT_RE = re.compile(
    r"//\s*(?:empty|idle)\s*\|\s*loading\s*\|\s*(?:success|pressed)\s*\|\s*error",
    re.IGNORECASE,
)

EXECUTABLE_FSM_PATTERNS = (
    re.compile(r"data-state\s*="),
    re.compile(r"data-theme\s*="),
    re.compile(r"aria-busy\s*="),
    re.compile(r"aria-pressed\s*="),
    re.compile(r"aria-selected\s*="),
    re.compile(r'role\s*=\s*["\'](?:status|alert|tab)["\']'),
    re.compile(r"useState\s*<[^>]*?(?:idle|loading|error|pressed|UIState|ComponentFSMState)"),
    re.compile(r"['\"](?:idle|loading|error|pressed)['\"]"),
)

REQUIRED_ATOMIC_DIRS = (
    "src/components/ui",
    "src/components/bento",
    "src/components/layout",
    "src/config",
    "src/styles",
    "src/types",
)

SEMANTIC_TOKEN_FAMILIES: tuple[tuple[str, ...], ...] = (
    ("--bg-canvas", "--bg-surface", "--ink-primary"),
    ("--surface-canvas", "--surface-primary", "--ink-primary"),
    ("--surface-canvas", "--surface-raised", "--text-primary"),
)


@dataclass
class AuditFinding:
    rule_id: str
    severity: str
    file: str
    message: str


def strip_comments(source: str) -> str:
    """Remove comentários de bloco e de linha para evitar comment-gaming."""
    return COMMENT_LINE_RE.sub("", COMMENT_BLOCK_RE.sub("", source))


def collect_frontend_files(target: Path) -> list[Path]:
    """Coleta arquivos de código e estilo frontend ignorando node_modules e dist."""
    if target.is_file():
        return [target]
    ignored = {"node_modules", ".git", "dist", "build", ".next", "coverage", "__pycache__"}
    exts = {".tsx", ".ts", ".jsx", ".js", ".vue", ".html", ".css"}
    return sorted(
        p
        for p in target.rglob("*")
        if not any(part in ignored for part in p.parts)
        and p.is_file()
        and p.suffix.lower() in exts
    )


def _check_semantic_tokens(combined_text: str) -> bool:
    """Verifica se alguma família de tokens semânticos por propósito está presente."""
    return any(
        all(token in combined_text for token in family) for family in SEMANTIC_TOKEN_FAMILIES
    )


def _audit_tokens_and_layers(
    combined_text: str, files: list[Path], findings: list[AuditFinding]
) -> float:
    """Audita tokens semânticos, camadas esculpidas e componentes órfãos."""
    s_tokens = 100.0
    if not _check_semantic_tokens(combined_text):
        s_tokens -= 20.0
        findings.append(
            AuditFinding(
                "AUDIT-VIS-01",
                "MEDIUM",
                "global",
                "Tokens semânticos de superfície/tinta ausentes (--bg-canvas/--bg-surface/--ink-primary).",
            )
        )
    elevation_markers = (
        "--shadow-sculpted",
        "--rim-light",
        "--shadow-card",
        "--shadow-1",
        "sculpted-card",
        "ui-card-soft",
        "bento-card",
        "inset 0 1px 0",
    )
    if not any(m in combined_text for m in elevation_markers):
        s_tokens -= 15.0
        findings.append(
            AuditFinding(
                "AUDIT-VIS-01",
                "MEDIUM",
                "global",
                "Ausência de camadas de elevação esculpidas (--shadow-sculpted / --rim-light / cards).",
            )
        )
    for comp_name in ("SoftCard", "SurfaceCard"):
        comp_defs = [f for f in files if f.name == f"{comp_name}.tsx"]
        consumers = [
            f
            for f in files
            if f.name != f"{comp_name}.tsx"
            and f.suffix.lower() in {".tsx", ".jsx"}
            and comp_name in f.read_text(encoding="utf-8", errors="ignore")
        ]
        if comp_defs and not consumers:
            s_tokens -= 25.0
            findings.append(
                AuditFinding(
                    "AUDIT-VIS-01",
                    "CRITICAL",
                    comp_defs[0].name,
                    f"Componente <{comp_name} /> criado mas ÓRFÃO (não importado em nenhuma view).",
                )
            )
    return max(0.0, s_tokens)


def _audit_fsm(
    combined_text: str, combined_stripped: str, findings: list[AuditFinding]
) -> float:
    """Audita máquina de estados finitos executável (S_FSM)."""
    s_fsm = 100.0
    if GAMED_FSM_COMMENT_RE.search(combined_text):
        s_fsm -= 25.0
        findings.append(
            AuditFinding(
                "AUDIT-STATE-01",
                "HIGH",
                "global",
                "Comment-gaming detectado: comentário estático simulando estados FSM.",
            )
        )
    matched_fsm = sum(1 for pat in EXECUTABLE_FSM_PATTERNS if pat.search(combined_stripped))
    if matched_fsm == 0:
        s_fsm -= 40.0
        findings.append(
            AuditFinding(
                "AUDIT-STATE-01",
                "CRITICAL",
                "global",
                "Nenhum estado finito executável (data-state, data-theme, aria-busy, role=alert) encontrado.",
            )
        )
    elif matched_fsm < 2:
        s_fsm -= 15.0
    return max(0.0, s_fsm)


def _audit_a11y(combined_stripped: str, findings: list[AuditFinding]) -> float:
    """Audita acessibilidade WAI-ARIA, foco, alinhamento tabular e proteção vestibular (S_A11y)."""
    s_a11y = 100.0
    if "aria-" not in combined_stripped and "role=" not in combined_stripped:
        s_a11y -= 30.0
        findings.append(
            AuditFinding("AUDIT-A11Y-01", "HIGH", "global", "Ausência de atributos WAI-ARIA.")
        )
    if not any(k in combined_stripped for k in (":focus-visible", "tabIndex", "tabindex")):
        s_a11y -= 15.0
        findings.append(
            AuditFinding("AUDIT-A11Y-02", "MEDIUM", "global", "Anel :focus-visible/tabIndex ausente.")
        )
    if "tabular-nums" not in combined_stripped:
        s_a11y -= 10.0
        findings.append(
            AuditFinding("AUDIT-A11Y-02", "LOW", "global", "Alinhamento tabular-nums ausente.")
        )
    if "prefers-reduced-motion" not in combined_stripped:
        s_a11y -= 10.0
        findings.append(
            AuditFinding("AUDIT-A11Y-02", "LOW", "global", "Proteção prefers-reduced-motion ausente.")
        )
    return max(0.0, s_a11y)


def _audit_security(
    files: list[Path], target_path: Path, findings: list[AuditFinding]
) -> float:
    """Audita vetores XSS e eval() inseguro nos arquivos frontend."""
    s_sec = 100.0
    for fpath in files:
        stripped = strip_comments(fpath.read_text(encoding="utf-8", errors="ignore"))
        rel = str(fpath.relative_to(target_path)) if target_path.is_dir() else fpath.name
        if "dangerouslySetInnerHTML" in stripped and "DOMPurify" not in stripped:
            s_sec -= 40.0
            findings.append(
                AuditFinding("AUDIT-SEC-01", "CRITICAL", rel, "dangerouslySetInnerHTML sem DOMPurify.")
            )
        if re.search(r"\beval\s*\(", stripped):
            s_sec -= 40.0
            findings.append(
                AuditFinding("AUDIT-SEC-01", "CRITICAL", rel, "Uso inseguro de eval() detectado.")
            )
    return max(0.0, s_sec)


def run_audit(target_path: Path) -> dict[str, Any]:
    """Executa a auditoria determinística de estilo por propósito, contraste, camadas e FSM."""
    files = collect_frontend_files(target_path)
    findings: list[AuditFinding] = []
    missing_dirs = [
        req_dir
        for req_dir in REQUIRED_ATOMIC_DIRS
        if target_path.is_dir() and (target_path / "src").exists() and not (target_path / req_dir).exists()
    ]
    if not files:
        return {
            "target_path": str(target_path),
            "files_scanned": 0,
            "s_a11y": 0.0,
            "s_fsm": 0.0,
            "s_tokens": 0.0,
            "s_sec": 100.0,
            "readiness_score": 15.0,
            "scores": {"readiness_score": 15.0, "s_a11y": 0.0, "s_fsm": 0.0, "s_tokens": 0.0, "s_sec": 100.0},
            "verdict": "UNVERIFIED",
            "missing_atomic_dirs": missing_dirs,
            "findings": [],
        }

    combined_raw = "\n".join(f.read_text(encoding="utf-8", errors="ignore") for f in files)
    combined_stripped = strip_comments(combined_raw)
    s_tokens = round(_audit_tokens_and_layers(combined_raw, files, findings), 2)
    s_fsm = round(_audit_fsm(combined_raw, combined_stripped, findings), 2)
    s_a11y = round(_audit_a11y(combined_stripped, findings), 2)
    s_sec = round(_audit_security(files, target_path, findings), 2)
    readiness = round((0.35 * s_a11y) + (0.30 * s_fsm) + (0.20 * s_tokens) + (0.15 * s_sec), 2)
    verdict = "PASS" if (readiness >= 90.0 and s_tokens >= 85.0 and s_fsm >= 85.0) else "FAIL"
    return {
        "target_path": str(target_path),
        "files_scanned": len(files),
        "s_a11y": s_a11y,
        "s_fsm": s_fsm,
        "s_tokens": s_tokens,
        "s_sec": s_sec,
        "readiness_score": readiness,
        "scores": {
            "readiness_score": readiness,
            "s_a11y": s_a11y,
            "s_fsm": s_fsm,
            "s_tokens": s_tokens,
            "s_sec": s_sec,
        },
        "verdict": verdict,
        "missing_atomic_dirs": missing_dirs,
        "findings": [asdict(f) for f in findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Auditor Determinístico de Arquitetura Visual, Contraste, Camadas & FSM (v3.0.0)"
    )
    parser.add_argument("target", help="Caminho do diretório ou arquivo frontend")
    parser.add_argument("--json", action="store_true", help="Saída em formato JSON")
    args = parser.parse_args()
    target = Path(args.target).resolve()
    if not target.exists():
        print(f"Erro: caminho não encontrado: {target}", file=sys.stderr)
        return 2
    report = run_audit(target)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"=== FRONTEND VISUAL ARCHITECTURE & FSM AUDIT (v3.0.0): {report['verdict']} ===")
        print(f"Target: {report['target_path']} ({report['files_scanned']} arquivos escaneados)")
        print(
            f"Readiness Score: {report['readiness_score']}/100.0 "
            f"[A11y: {report['s_a11y']} | FSM: {report['s_fsm']} | Tokens/Layers: {report['s_tokens']} | Sec: {report['s_sec']}]"
        )
        for f in report["findings"]:
            print(f"  - [{f['severity']}] ({f['rule_id']}) {f['file']}: {f['message']}")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
