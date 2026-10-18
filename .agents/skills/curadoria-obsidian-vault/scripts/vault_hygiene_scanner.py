"""
vault_hygiene_scanner.py
Scanner determinístico de saúde, deriva ativa (Active Drift) e segurança Zero-Trust
para o cofre Obsidian (C:\\Users\\melki\\dev\\notes\\), incorporando algoritmos
reconstruídos do breferrari/obsidian-mind (v8.3):

1. Active Drift & Open Loops (>14 dias, completed-in-active, inbox pressure, monolith >25KB)
2. Canonical Report Hash (strip volatile fields sizeKb/ageDays/oldestDays para zero nagging)
3. Windows Case-Insensitive Never-Expose & Private Frontmatter Guard (proteção PHI/PII)
4. Wikilinks & Frontmatter Integrity Validator
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Mapping, Set

DEFAULT_VAULT = Path(r"C:\Users\melki\dev\notes")
MONOLITH_BYTES = 25_000
AGENTS_MD_FLAG_BYTES = 23_000
OPEN_LOOP_DAYS = 14
OPEN_LOOP_CAP = 8
VOLATILE_KEYS: FrozenSet[str] = frozenset({"sizeKb", "ageDays", "oldestDays"})
ARCHIVABLE_STATUS: FrozenSet[str] = frozenset({"concluido", "arquivado", "completed", "archived", "done"})
SKIP_DIRS: FrozenSet[str] = frozenset({".obsidian", ".git", "node_modules", ".trash", "Modelos"})
OPEN_LOOP_PHRASE_RX = re.compile(r"\b(waiting on|watch for|aguardando|pendente de)\b", re.IGNORECASE)
ACTION_HEADING_RX = re.compile(r"^##+\s+(pend[êe]ncias|pr[óo]ximos passos|action items|what to watch)", re.IGNORECASE)
WIKILINK_RX = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


@dataclass
class VaultHygieneReport:
    """Relatório estruturado de higiene do cofre Obsidian com hash canônico anti-nagging."""

    vault_path: str
    total_notes: int = 0
    completed_in_active: List[str] = field(default_factory=list)
    oversized_notes: List[Dict[str, Any]] = field(default_factory=list)
    open_loops: List[Dict[str, Any]] = field(default_factory=list)
    inbox_pressure: Dict[str, int] = field(default_factory=dict)
    missing_frontmatter: List[str] = field(default_factory=list)
    broken_wikilinks: List[Dict[str, str]] = field(default_factory=list)
    withheld_private_notes: List[str] = field(default_factory=list)
    report_key: str = ""
    one_line_summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def parse_frontmatter(md_text: str) -> Dict[str, str]:
    """Extrai pares simples chave: valor do frontmatter YAML sem dependências externas."""
    m = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", md_text)
    if not m:
        return {}
    out: Dict[str, str] = {}
    for line in m.group(1).splitlines():
        kv = re.match(r"^([A-Za-z_][\w\-]*):\s*(.*)$", line)
        if kv:
            out[kv.group(1).lower()] = kv.group(2).strip().strip("\"'")
    return out


def is_never_exposed(rel_path: str, fm: Mapping[str, str], never_expose: Set[str]) -> bool:
    """Guarda Case-Insensitive (Windows NTFS) e bloqueio de tags/campos private/phi."""
    norm_name = Path(rel_path.replace("\\", "/")).name.lower()
    if any(entry.lower() == norm_name for entry in never_expose):
        return True
    if fm.get("private", "").lower() == "true" or fm.get("phi", "").lower() == "true":
        return True
    tags_raw = fm.get("tags", "").lower()
    return "private" in tags_raw or "phi" in tags_raw or " confidencial" in tags_raw


def count_open_loops(content: str) -> int:
    """Conta checkboxes abertos (- [ ]) em seções de pendências ou frases explícitas de espera."""
    in_action = False
    count = 0
    for line in content.splitlines():
        if line.startswith("##"):
            in_action = bool(ACTION_HEADING_RX.match(line.strip()))
            continue
        if in_action and re.match(r"^\s*-\s*\[\s\]", line):
            count += 1
        elif OPEN_LOOP_PHRASE_RX.search(line):
            count += 1
    return count


def _strip_volatile(obj: Any) -> Any:
    """Remove chaves voláteis (sizeKb, ageDays, oldestDays) e ordena listas para hash estável."""
    if isinstance(obj, dict):
        return {
            k: _strip_volatile(v)
            for k, v in sorted(obj.items())
            if k not in VOLATILE_KEYS and k not in ("report_key", "one_line_summary")
        }
    if isinstance(obj, list):
        cleaned = [_strip_volatile(x) for x in obj]
        return sorted(cleaned, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    return obj


def compute_report_key(report_dict: Mapping[str, Any]) -> str:
    """Gera hash SHA-256 canônico ignorando variações de tamanho/idade (#252 anti-nagging)."""
    canonical = json.dumps(_strip_volatile(dict(report_dict)), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def _collect_markdown_files(vault: Path) -> List[Path]:
    """Lista todas as notas .md do cofre ignorando diretórios de infraestrutura."""
    files: List[Path] = []
    if not vault.is_dir():
        return files
    for p in sorted(vault.rglob("*.md")):
        rel_parts = p.relative_to(vault).parts
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel_parts):
            continue
        files.append(p)
    return files


def _inspect_note(
    p: Path,
    vault: Path,
    now_s: float,
    known_stems: Set[str],
    never_expose: Set[str],
    report: VaultHygieneReport,
) -> None:
    """Analisa uma nota individual e popula os coletores do VaultHygieneReport."""
    rel = str(p.relative_to(vault)).replace("\\", "/")
    try:
        raw = p.read_text(encoding="utf-8", errors="replace")
        stat = p.stat()
    except OSError:
        return

    fm = parse_frontmatter(raw)
    if is_never_exposed(rel, fm, never_expose):
        report.withheld_private_notes.append(rel)
        return

    if not fm.get("title") and not fm.get("date"):
        report.missing_frontmatter.append(rel)

    if rel.startswith("Projetos/Ativos/") and fm.get("status", "").lower() in ARCHIVABLE_STATUS:
        report.completed_in_active.append(rel)

    if "Arquivo/" not in rel and stat.st_size > MONOLITH_BYTES:
        report.oversized_notes.append({"path": rel, "sizeKb": round(stat.st_size / 1000, 1)})

    age_days = int((now_s - stat.st_mtime) // 86_400)
    if "Arquivo/" not in rel and not p.name.upper().startswith("README") and age_days >= OPEN_LOOP_DAYS:
        loops = count_open_loops(raw)
        if loops > 0 and len(report.open_loops) < OPEN_LOOP_CAP:
            report.open_loops.append({"path": rel, "ageDays": age_days, "openItems": loops})

    # Ignora blocos de código cercados e código inline antes de extrair [[Wikilinks]]
    prose_only = re.sub(r"```[\s\S]*?```|`[^`\n]+`", "", raw)
    for match in WIKILINK_RX.findall(prose_only):
        target = match.strip().split("/")[-1].lower()
        if (
            target
            and not target.endswith((".png", ".jpg", ".pdf", ".webp"))
            and target not in known_stems
            and target not in {"wikilinks", "nota", "projeto"}
        ):
            report.broken_wikilinks.append({"source": rel, "target": match.strip()})


def scan_vault_hygiene(
    vault_path: Path = DEFAULT_VAULT,
    never_expose: Set[str] | None = None,
) -> VaultHygieneReport:
    """Executa varredura completa de saúde e deriva ativa no cofre Obsidian."""
    vault = Path(vault_path)
    never = never_expose or {"SOUL.md", "SECRETS.md"}
    md_files = _collect_markdown_files(vault)
    known_stems = {p.stem.lower() for p in md_files}
    now_s = time.time()

    report = VaultHygieneReport(vault_path=str(vault), total_notes=len(md_files))
    for p in md_files:
        _inspect_note(p, vault, now_s, known_stems, never, report)

    inbox_dir = vault / "Inbox"
    if inbox_dir.is_dir():
        inbox_notes = [
            f for f in inbox_dir.glob("*.md")
            if f.is_file() and not f.name.upper().startswith("README")
        ]
        if inbox_notes:
            oldest = max(int((now_s - f.stat().st_mtime) // 86_400) for f in inbox_notes)
            report.inbox_pressure = {"count": len(inbox_notes), "oldestDays": oldest}

    report.report_key = compute_report_key(report.to_dict())
    report.one_line_summary = (
        f"obsidian-mind: vault check [{report.report_key[:8]}] -> "
        f"{report.total_notes} notes | {len(report.oversized_notes)} monoliths (>25KB) | "
        f"{len(report.open_loops)} stale open-loops | {len(report.broken_wikilinks)} broken links"
    )
    return report


def _run_self_test() -> int:
    """Executa autoteste determinístico em memória/tmp."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "Projetos" / "Ativos").mkdir(parents=True)
        note_a = root / "Projetos" / "Ativos" / "Demo.md"
        note_a.write_text(
            "---\ntitle: Demo\ndate: 2026-10-01\nstatus: concluido\n---\n## Pendências\n- [ ] Test [[Inexistente]]\n",
            encoding="utf-8",
        )
        rep1 = scan_vault_hygiene(root)
        assert "Projetos/Ativos/Demo.md" in rep1.completed_in_active
        assert len(rep1.broken_wikilinks) == 1
        # Valida invariante report_key ignorando campos voláteis
        d1 = rep1.to_dict()
        d2 = dict(d1, oversized_notes=[{"path": "x.md", "sizeKb": 30.1}])
        d3 = dict(d1, oversized_notes=[{"path": "x.md", "sizeKb": 99.9}])
        assert compute_report_key(d2) == compute_report_key(d3)
    print("[PASS] vault_hygiene_scanner self-test succeeded.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Obsidian Vault Hygiene & Active Drift Scanner")
    parser.add_argument("--vault", type=str, default=str(DEFAULT_VAULT), help="Caminho do cofre Obsidian")
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    parser.add_argument("--self-test", action="store_true", help="Executa autoteste determinístico")
    args = parser.parse_args()

    if args.self_test:
        return _run_self_test()

    rep = scan_vault_hygiene(Path(args.vault))
    if args.json:
        print(json.dumps(rep.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(rep.one_line_summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
