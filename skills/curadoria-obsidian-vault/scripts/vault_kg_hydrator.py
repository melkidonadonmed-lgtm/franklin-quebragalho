#!/usr/bin/env python3
"""
vault_kg_hydrator.py
Sincronizador determinístico do Grafo de Conhecimento (MemPalace SQLite `knowledge_graph.sqlite3`)
a partir das notas ativas do Cofre Obsidian (`Memória/`, `Projetos/`, `Medicina/`), `[[Wikilinks]]`,
27 Skills canônicas e 5 Subagentes do ecossistema Franklin Quebra-Galho.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_VAULT_DIR = Path(r"C:\Users\melki\dev\notes")
DEFAULT_KG_DB = Path(r"C:\Users\melki\.mempalace\knowledge_graph.sqlite3")
SECONDARY_KG_DBS = (
    Path(r"C:\Users\melki\.config\mempalace\knowledge_graph.sqlite3"),
    Path(r"C:\Users\melki\.config\mempalace\palace\knowledge_graph.sqlite3"),
    Path(r"C:\Users\melki\.mempalace\palace\knowledge_graph.sqlite3"),
)
DEFAULT_REPO_DIR = Path(r"C:\Users\melki\dev\repos\franklin-quebragalho")

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

ENTITIES_DDL = """CREATE TABLE IF NOT EXISTS entities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT DEFAULT 'unknown',
    properties TEXT DEFAULT '{}',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)"""

TRIPLES_DDL = """CREATE TABLE IF NOT EXISTS triples (
    id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object TEXT NOT NULL,
    valid_from TEXT,
    valid_to TEXT,
    confidence REAL DEFAULT 1.0,
    source_closet TEXT,
    source_file TEXT,
    source_drawer_id TEXT,
    adapter_name TEXT,
    extracted_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject) REFERENCES entities(id),
    FOREIGN KEY (object) REFERENCES entities(id)
)"""


def _slug_id(prefix: str, name: str) -> str:
    """Gera um ID determinístico legível para uma entidade do grafo."""
    clean = re.sub(r"[^a-zA-Z0-9_\-]+", "_", name.strip().lower()).strip("_")
    if not clean:
        clean = hashlib.sha256(name.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}:{clean[:64]}"


def _triple_id(subject: str, predicate: str, obj: str) -> str:
    """Gera chave primária SHA-256 curta para uma tripla (subject, predicate, object)."""
    digest = hashlib.sha256(f"{subject}|{predicate}|{obj}".encode("utf-8")).hexdigest()[:20]
    return f"trp:{digest}"


def _classify_note_room(rel_parts: Tuple[str, ...]) -> str:
    """Classifica o tipo semântico da nota com base na pasta raiz no cofre."""
    if not rel_parts:
        return "vault_root_note"
    mapping = {
        "Memória": "memory_note",
        "Projetos": "project_note",
        "Medicina": "clinical_note",
        "Agentes & Skills": "agent_doc_note",
        "Modelos": "template_note",
    }
    return mapping.get(rel_parts[0], "vault_note")


def _extract_note_links(
    md_path: Path,
    ent_id: str,
    note_name: str,
    room_name: str,
    entities: Dict[str, Tuple[str, str, str, str]],
    triples: List[Tuple[str, str, str, str, str]],
) -> None:
    """Extrai [[Wikilinks]] de uma nota Markdown e registra nós e arestas."""
    try:
        content = md_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        _ = exc
        return

    seen_targets: Set[str] = set()
    for match in WIKILINK_RE.finditer(content):
        target_name = match.group(1).strip().split("/")[-1]
        if not target_name or target_name == note_name or target_name in seen_targets:
            continue
        seen_targets.add(target_name)
        target_id = _slug_id("note", target_name)
        if target_id not in entities:
            props = json.dumps({"referenced_from": note_name}, ensure_ascii=False)
            entities[target_id] = (target_id, target_name, "referenced_note", props)
        triples.append((ent_id, "WIKILINKS_TO", target_id, room_name, str(md_path)))


def _collect_vault_entities_and_triples(
    vault_dir: Path,
) -> Tuple[List[Tuple[str, str, str, str]], List[Tuple[str, str, str, str, str]]]:
    """Varre notas ativas do Obsidian e extrai entidades e triplas de [[Wikilinks]]."""
    entities: Dict[str, Tuple[str, str, str, str]] = {}
    triples: List[Tuple[str, str, str, str, str]] = []
    if not vault_dir.exists():
        return [], []

    for md_path in sorted(vault_dir.rglob("*.md")):
        rel = md_path.relative_to(vault_dir)
        if any(part.startswith(".") or part == "Arquivo" for part in rel.parts):
            continue
        note_name = md_path.stem
        ent_id = _slug_id("note", note_name)
        room_name = rel.parts[0] if len(rel.parts) > 1 else "root"
        props = json.dumps({"path": str(md_path), "room": room_name}, ensure_ascii=False)
        entities[ent_id] = (ent_id, note_name, _classify_note_room(rel.parts), props)
        _extract_note_links(md_path, ent_id, note_name, room_name, entities, triples)
    return list(entities.values()), triples


def _collect_ecosystem_entities_and_triples(
    repo_dir: Path,
) -> Tuple[List[Tuple[str, str, str, str]], List[Tuple[str, str, str, str, str]]]:
    """Extrai entidades e relações das 27 Skills canônicas e 5 Subagentes do Franklin."""
    hub_id = "repo:franklin_quebragalho"
    entities: List[Tuple[str, str, str, str]] = [(
        hub_id,
        "franklin-quebragalho",
        "canonical_repository",
        json.dumps({"path": str(repo_dir), "skills": 29, "subagents": 9}, ensure_ascii=False),
    )]
    triples: List[Tuple[str, str, str, str, str]] = []

    skills_dir = repo_dir / "skills"
    if skills_dir.exists():
        for s_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()):
            s_id = _slug_id("skill", s_dir.name)
            props = json.dumps({"directory": s_dir.name, "has_scripts": (s_dir / "scripts").is_dir()}, ensure_ascii=False)
            entities.append((s_id, s_dir.name, "canonical_skill", props))
            triples.append((hub_id, "PROVIDES_SKILL", s_id, "franklin-skills", str(s_dir / "SKILL.md")))

    agents_dir = repo_dir / "agents"
    if agents_dir.exists():
        for a_file in sorted(agents_dir.glob("*.md")):
            a_id = _slug_id("subagent", a_file.stem)
            entities.append((a_id, a_file.stem, "specialist_subagent", json.dumps({"contract": a_file.name}, ensure_ascii=False)))
            triples.append((hub_id, "ORCHESTRATES_SUBAGENT", a_id, "franklin-agents", str(a_file)))

    return entities, triples


def hydrate_knowledge_graph(
    vault_dir: Path = DEFAULT_VAULT_DIR,
    repo_dir: Path = DEFAULT_REPO_DIR,
    kg_db_path: Path = DEFAULT_KG_DB,
) -> Dict[str, int | str]:
    """Popula idempotentemente as tabelas `entities` e `triples` do MemPalace SQLite."""
    kg_db_path.parent.mkdir(parents=True, exist_ok=True)
    v_entities, v_triples = _collect_vault_entities_and_triples(vault_dir)
    e_entities, e_triples = _collect_ecosystem_entities_and_triples(repo_dir)
    all_entities = {ent[0]: ent for ent in (v_entities + e_entities)}
    all_triples = v_triples + e_triples
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    conn = sqlite3.connect(str(kg_db_path))
    try:
        cur = conn.cursor()
        cur.execute(ENTITIES_DDL)
        cur.execute(TRIPLES_DDL)
        cur.executemany(
            "INSERT OR REPLACE INTO entities (id, name, type, properties, created_at) VALUES (?, ?, ?, ?, ?)",
            [(eid, name, etype, props, now_iso) for eid, name, etype, props in all_entities.values()],
        )
        cur.executemany(
            "INSERT OR REPLACE INTO triples (id, subject, predicate, object, valid_from, confidence, source_closet, source_file, adapter_name, extracted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(_triple_id(s, p, o), s, p, o, now_iso, 1.0, closet, sfile, "vault_kg_hydrator_v1", now_iso) for s, p, o, closet, sfile in all_triples],
        )
        conn.commit()
        total_entities = int(cur.execute("SELECT COUNT(*) FROM entities").fetchone()[0])
        total_triples = int(cur.execute("SELECT COUNT(*) FROM triples").fetchone()[0])
    finally:
        conn.close()

    if kg_db_path == DEFAULT_KG_DB:
        import shutil

        for mirror_db in SECONDARY_KG_DBS:
            try:
                mirror_db.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(kg_db_path, mirror_db)
            except OSError as exc:
                _ = exc

    return {
        "status": "HYDRATED",
        "database": str(kg_db_path),
        "entities_upserted": len(all_entities),
        "triples_upserted": len(all_triples),
        "total_entities": total_entities,
        "total_triples": total_triples,
    }


def _run_self_test() -> int:
    """Executa autoteste determinístico em banco SQLite temporário."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        v_dir = tmp_path / "notes" / "Memória"
        v_dir.mkdir(parents=True)
        (v_dir / "Decisões.md").write_text("Link para [[Ambiente Dev (PC atual)]].", encoding="utf-8")
        res = hydrate_knowledge_graph(vault_dir=tmp_path / "notes", repo_dir=DEFAULT_REPO_DIR, kg_db_path=tmp_path / "kg.sqlite3")
        assert int(res["total_entities"]) >= 2, f"Entidades insuficientes: {res}"
        assert int(res["total_triples"]) >= 1, f"Triplas insuficientes: {res}"
    print(json.dumps({"self_test": "PASS", "verified": True}, ensure_ascii=False))
    return 0


def main() -> int:
    """Ponto de entrada CLI."""
    parser = argparse.ArgumentParser(description="Hidrata o Grafo de Conhecimento SQLite do MemPalace.")
    parser.add_argument("--self-test", action="store_true", help="Executa autoteste isolado.")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    print(json.dumps(hydrate_knowledge_graph(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
