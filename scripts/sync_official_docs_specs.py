#!/usr/bin/env python3
"""
sync_official_docs_specs.py — Sentinel de Atualização de Documentação Oficial (Stdlib Puro)

Consulta fontes oficiais do Google Antigravity, AgentSkills, MCP, ADK, Gemini API e JSON-RPC 2.0,
valida invariantes críticas contra a cache local (official_specs_lock.json) e emite proposta
auditável em .context/docs-drift-proposal.md sob detecção de drift — nunca sobrescrevendo regras
ou skills silenciosamente (HITL obrigatório).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES_PATH = ROOT_DIR / "references" / "official_sources.json"


def resolve_default_lock_path() -> Path:
    """Resolve o caminho canônico do lockfile respeitando FRANKLIN_SPECS_LOCK_PATH."""
    env_override = os.environ.get("FRANKLIN_SPECS_LOCK_PATH", "").strip()
    if env_override:
        return Path(env_override)
    return Path.home() / ".gemini" / "config" / "specs-cache" / "official_specs_lock.json"


def _validate_https_url(url: str) -> str:
    """Garante esquema HTTPS estrito e host válido (Zero-Trust anti-SSRF local)."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"URL inválida ou não HTTPS rejeitada: {url!r}")
    return url


def default_fetcher(url: str, timeout: float = 10.0) -> str:
    """Baixa conteúdo textual de endpoint HTTPS oficial via stdlib urllib."""
    safe_url = _validate_https_url(url)
    req = urllib.request.Request(safe_url, headers={"User-Agent": "FranklinDocsWatcher/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def _load_source_text(
    src: Dict[str, Any],
    home_dir: Path,
    fetcher: Callable[[str], str],
) -> tuple[str | None, str]:
    """Lê fonte remota (HTTPS) ou arquivo builtin local retornando (texto, status_erro)."""
    kind = str(src.get("kind", "remote"))
    if kind == "local_home":
        rel = str(src.get("home_rel_path", "")).strip()
        if not rel or ".." in Path(rel).parts:
            return None, "INVALID_LOCAL_PATH"
        target = home_dir / rel
        if not target.is_file():
            return None, "SKIPPED_LOCAL_MISSING"
        return target.read_text(encoding="utf-8", errors="ignore"), ""

    if kind == "remote":
        url = str(src.get("url", "")).strip()
        try:
            _validate_https_url(url)
            return fetcher(url), ""
        except (ValueError, urllib.error.URLError, TimeoutError, OSError) as exc:
            return None, f"FETCH_ERROR: {exc}"

    return None, f"UNSUPPORTED_KIND: {kind}"


def _evaluate_source(
    src: Dict[str, Any],
    prev_entries: Dict[str, Any],
    home_dir: Path,
    fetcher: Callable[[str], str],
) -> tuple[Dict[str, Any], Dict[str, Any] | None]:
    """Avalia hash SHA-256 e invariantes de uma fonte, retornando (resultado, nova_entrada_lock)."""
    src_id = str(src["id"])
    text, err = _load_source_text(src, home_dir, fetcher)
    if text is None:
        return {
            "id": src_id,
            "kind": src.get("kind", "remote"),
            "status": "SKIPPED" if err == "SKIPPED_LOCAL_MISSING" else "FETCH_ERROR",
            "error": err,
            "target_rules": src.get("target_rules", []),
        }, None

    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    missing = [inv for inv in src.get("required_invariants", []) if inv not in text]
    prev_hash = str((prev_entries.get(src_id) or {}).get("sha256", ""))

    if missing:
        status = "INVARIANT_MISSING"
    elif not prev_hash:
        status = "NEW"
    elif prev_hash != digest:
        status = "HASH_DRIFT"
    else:
        status = "UNCHANGED"

    lock_entry = {
        "sha256": digest,
        "bytes": len(text.encode("utf-8")),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "url": src.get("url", ""),
        "home_rel_path": src.get("home_rel_path", ""),
        "missing_invariants": missing,
    }
    return {
        "id": src_id,
        "title": src.get("title", src_id),
        "kind": src.get("kind", "remote"),
        "status": status,
        "sha256": digest,
        "previous_sha256": prev_hash,
        "missing_invariants": missing,
        "target_rules": src.get("target_rules", []),
    }, lock_entry


def _write_json_atomic(path: Path, payload: Dict[str, Any]) -> None:
    """Grava JSON de forma atômica via arquivo temporário e os.replace()."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp_name, path)
    except (OSError, TypeError, ValueError):
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise


def _build_drift_proposal_md(results: List[Dict[str, Any]]) -> str:
    """Gera relatório Markdown HITL para revisão de drift sem auto-editar rules/."""
    ts = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Proposta de Atualização de Regras (Docs Drift Sentinel)",
        "",
        f"- **Gerado em (UTC):** `{ts}`",
        "- **Ação exigida (HITL):** Revisar fontes divergentes e atualizar regras afetadas manualmente ou via PR.",
        "",
        "| Fonte ID | Status | Faltando Invariantes | Regras Impactadas |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for item in results:
        if item["status"] not in ("HASH_DRIFT", "INVARIANT_MISSING"):
            continue
        missing = ", ".join(f"`{m}`" for m in item.get("missing_invariants", [])) or "nenhuma"
        rules = ", ".join(f"`{r}`" for r in item.get("target_rules", [])) or "N/A"
        lines.append(f"| `{item['id']}` | `{item['status']}` | {missing} | {rules} |")
    lines.append("")
    return "\n".join(lines)


def run_sync(
    *,
    sources_path: Path = DEFAULT_SOURCES_PATH,
    lock_path: Path | None = None,
    workspace_dir: Path = ROOT_DIR,
    home_dir: Path | None = None,
    check: bool = False,
    sync_cache: bool = False,
    propose: bool = False,
    fetcher: Callable[[str], str] | None = None,
) -> Dict[str, Any]:
    """Executa auditoria/sincronia das fontes oficiais e retorna resumo estruturado."""
    active_fetcher = fetcher or default_fetcher
    resolved_lock = lock_path or resolve_default_lock_path()
    resolved_home = home_dir or Path.home()
    config = json.loads(sources_path.read_text(encoding="utf-8"))

    prev_lock: Dict[str, Any] = {}
    if resolved_lock.is_file():
        prev_lock = json.loads(resolved_lock.read_text(encoding="utf-8"))
    prev_entries: Dict[str, Any] = dict(prev_lock.get("sources") or {})

    results: List[Dict[str, Any]] = []
    next_entries: Dict[str, Any] = dict(prev_entries)
    for src in config.get("sources", []):
        res, entry = _evaluate_source(src, prev_entries, resolved_home, active_fetcher)
        results.append(res)
        if entry is not None:
            next_entries[res["id"]] = entry

    if sync_cache or (not resolved_lock.is_file() and not check):
        _write_json_atomic(
            resolved_lock,
            {
                "schema_version": config.get("schema_version", "1.0.0"),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "sources": next_entries,
            },
        )

    drift_items = [r for r in results if r["status"] in ("HASH_DRIFT", "INVARIANT_MISSING")]
    proposal_written: str | None = None
    if propose and drift_items:
        prop_path = workspace_dir / ".context" / "docs-drift-proposal.md"
        prop_path.parent.mkdir(parents=True, exist_ok=True)
        prop_path.write_text(_build_drift_proposal_md(results), encoding="utf-8")
        proposal_written = str(prop_path)

    return {
        "lock_file": str(resolved_lock),
        "total": len(results),
        "unchanged": sum(1 for r in results if r["status"] == "UNCHANGED"),
        "new": sum(1 for r in results if r["status"] == "NEW"),
        "drift": [r["id"] for r in results if r["status"] == "HASH_DRIFT"],
        "invariant_missing": [r["id"] for r in results if r["status"] == "INVARIANT_MISSING"],
        "fetch_errors": [r["id"] for r in results if r["status"] == "FETCH_ERROR"],
        "skipped": [r["id"] for r in results if r["status"] == "SKIPPED"],
        "proposal_path": proposal_written,
        "results": results,
    }


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    """Analisa argumentos CLI sem aceitar mutações silenciosas."""
    parser = argparse.ArgumentParser(description="Franklin Official Docs Drift Sentinel")
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES_PATH)
    parser.add_argument("--lock-file", type=Path, default=None)
    parser.add_argument("--workspace", type=Path, default=ROOT_DIR)
    parser.add_argument("--check", action="store_true", help="Verifica hash e invariantes vs cache.")
    parser.add_argument("--sync-cache", action="store_true", help="Atualiza official_specs_lock.json.")
    parser.add_argument("--propose", action="store_true", help="Gera .context/docs-drift-proposal.md em drift.")
    parser.add_argument("--fail-on-drift", action="store_true", help="Retorna exit 2 em drift/invariante.")
    parser.add_argument("--json", action="store_true", help="Emite relatório completo em JSON.")
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    """Ponto de entrada CLI com degradação graciosa em modo offline."""
    args = _parse_args(argv)
    if not (args.check or args.sync_cache or args.propose):
        args.check = True

    summary = run_sync(
        sources_path=args.sources,
        lock_path=args.lock_file,
        workspace_dir=args.workspace,
        check=args.check,
        sync_cache=args.sync_cache,
        propose=args.propose,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(
            f"[DocsWatcher] total={summary['total']} unchanged={summary['unchanged']} "
            f"new={summary['new']} drift={len(summary['drift'])} "
            f"invariant_missing={len(summary['invariant_missing'])} "
            f"fetch_errors={len(summary['fetch_errors'])} skipped={len(summary['skipped'])}"
        )
        if summary["proposal_path"]:
            print(f"[DocsWatcher] Proposta HITL gerada em {summary['proposal_path']}")

    if args.fail_on_drift and (summary["drift"] or summary["invariant_missing"]):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
