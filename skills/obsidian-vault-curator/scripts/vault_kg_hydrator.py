#!/usr/bin/env python3
"""
vault_kg_hydrator.py
Deterministic Obsidian + Franklin ecosystem Knowledge Graph hydrator for
MemPalace SQLite (`knowledge_graph.sqlite3`) using WAL mode and scoped upserts.
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

ADAPTER_NAME = "vault_kg_hydrator_v1"
DEFAULT_VAULT_DIR = Path(r"C:\Users\melki\dev\notes")
DEFAULT_KG_DB = Path(r"C:\Users\melki\.config\mempalace\palace\knowledge_graph.sqlite3")
DEFAULT_REPO_DIR = Path(r"C:\Users\melki\dev\repos\franklin-quebragalho")

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
CODE_SPAN_RE = re.compile(r"```[\s\S]*?```|`[^`\n]+`")
IGNORED_WIKILINK_TARGETS = {"wikilinks", "wikilink", "nome da nota", "projeto", "nota"}

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

INDEXES_DDL = (
    "CREATE INDEX IF NOT EXISTS idx_triples_subject ON triples(subject)",
    "CREATE INDEX IF NOT EXISTS idx_triples_object ON triples(object)",
    "CREATE INDEX IF NOT EXISTS idx_triples_predicate ON triples(predicate)",
    "CREATE INDEX IF NOT EXISTS idx_triples_valid ON triples(valid_from, valid_to)",
)

EntityTuple = Tuple[str, str, str, str]
TripleTuple = Tuple[str, str, str, str, str]


def _slug_id(prefix: str, name: str) -> str:
    """Build a deterministic readable entity identifier."""
    clean = re.sub(r"[^a-zA-Z0-9_\-]+", "_", name.strip().lower()).strip("_")
    if not clean:
        clean = hashlib.sha256(name.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}:{clean[:64]}"


def _triple_id(subject: str, predicate: str, obj: str) -> str:
    """Compute a short deterministic SHA-256 primary key for a triple."""
    digest = hashlib.sha256(f"{subject}|{predicate}|{obj}".encode("utf-8")).hexdigest()[:20]
    return f"trp:{digest}"


def _classify_note_room(rel_parts: Tuple[str, ...]) -> str:
    """Classify the semantic node type from the top-level vault folder."""
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


def _is_private_note(md_text: str) -> bool:
    """Return True when YAML frontmatter or tags mark a note as private/PHI."""
    if not md_text.startswith("---"):
        return False
    lines = md_text.splitlines()
    end_idx = next((i for i in range(1, min(40, len(lines))) if lines[i].strip() == "---"), 0)
    if end_idx == 0:
        return False
    fm_block = "\n".join(lines[1:end_idx]).lower()
    if re.search(r"^\s*(private|phi)\s*:\s*[\"']?true[\"']?\s*$", fm_block, re.MULTILINE):
        return True
    tags_match = re.findall(r"(?:tags\s*:.*|^\s*-\s+.*)", fm_block, re.MULTILINE)
    joined = " ".join(tags_match)
    return any(tok in joined for tok in ("private", "phi", "confidencial"))


def _extract_note_links(
    md_path: Path,
    content: str,
    ent_id: str,
    note_name: str,
    room_name: str,
    entities: Dict[str, EntityTuple],
    triples: List[TripleTuple],
) -> None:
    """Extract [[Wikilinks]] from Markdown prose and register graph nodes and edges."""
    clean_content = CODE_SPAN_RE.sub("", content)
    seen_targets: Set[str] = set()
    for match in WIKILINK_RE.finditer(clean_content):
        target_name = match.group(1).strip().split("/")[-1]
        if (
            not target_name
            or target_name.lower() in IGNORED_WIKILINK_TARGETS
            or target_name.startswith("<")
            or target_name == note_name
            or target_name in seen_targets
        ):
            continue
        seen_targets.add(target_name)
        target_id = _slug_id("note", target_name)
        if target_id not in entities:
            props = json.dumps(
                {"referenced_from": note_name, "managed_by": ADAPTER_NAME},
                ensure_ascii=False,
            )
            entities[target_id] = (target_id, target_name, "referenced_note", props)
        triples.append((ent_id, "WIKILINKS_TO", target_id, room_name, str(md_path)))


def _collect_vault_entities_and_triples(
    vault_dir: Path,
) -> Tuple[List[EntityTuple], List[TripleTuple]]:
    """Scan non-archived, non-private Obsidian notes for entities and wikilinks."""
    entities: Dict[str, EntityTuple] = {}
    triples: List[TripleTuple] = []
    if not vault_dir.exists():
        return [], []

    for md_path in sorted(vault_dir.rglob("*.md")):
        rel = md_path.relative_to(vault_dir)
        if any(part.startswith(".") or part == "Arquivo" for part in rel.parts):
            continue
        try:
            content = md_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"[WARN] Failed reading {md_path}: {exc}", file=sys.stderr)
            continue
        if _is_private_note(content):
            continue
        note_name = md_path.stem
        ent_id = _slug_id("note", note_name)
        room_name = rel.parts[0] if len(rel.parts) > 1 else "root"
        props = json.dumps(
            {"path": str(md_path), "room": room_name, "managed_by": ADAPTER_NAME},
            ensure_ascii=False,
        )
        entities[ent_id] = (ent_id, note_name, _classify_note_room(rel.parts), props)
        _extract_note_links(md_path, content, ent_id, note_name, room_name, entities, triples)
    return list(entities.values()), triples


def _collect_ecosystem_entities_and_triples(
    repo_dir: Path,
) -> Tuple[List[EntityTuple], List[TripleTuple]]:
    """Extract canonical skills and declarative subagents from the Franklin repository."""
    hub_id = "repo:franklin_quebragalho"
    skill_entities: List[EntityTuple] = []
    agent_entities: List[EntityTuple] = []
    triples: List[TripleTuple] = []

    skills_dir = repo_dir / "skills"
    if skills_dir.exists():
        for s_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()):
            s_id = _slug_id("skill", s_dir.name)
            props = json.dumps(
                {"directory": s_dir.name, "has_scripts": (s_dir / "scripts").is_dir(), "managed_by": ADAPTER_NAME},
                ensure_ascii=False,
            )
            skill_entities.append((s_id, s_dir.name, "canonical_skill", props))
            triples.append((hub_id, "PROVIDES_SKILL", s_id, "franklin-skills", str(s_dir / "SKILL.md")))

    agents_dir = repo_dir / "agents"
    if agents_dir.exists():
        for a_file in sorted(agents_dir.glob("*.md")):
            a_id = _slug_id("subagent", a_file.stem)
            props = json.dumps({"contract": a_file.name, "managed_by": ADAPTER_NAME}, ensure_ascii=False)
            agent_entities.append((a_id, a_file.stem, "specialist_subagent", props))
            triples.append((hub_id, "ORCHESTRATES_SUBAGENT", a_id, "franklin-agents", str(a_file)))

    hub_props = json.dumps(
        {
            "path": str(repo_dir),
            "skills": len(skill_entities),
            "subagents": len(agent_entities),
            "managed_by": ADAPTER_NAME,
        },
        ensure_ascii=False,
    )
    hub_entity: EntityTuple = (hub_id, "franklin-quebragalho", "canonical_repository", hub_props)
    return [hub_entity, *skill_entities, *agent_entities], triples


def _init_kg_schema(cur: sqlite3.Cursor) -> None:
    """Initialize WAL mode, busy timeout, tables, and MemPalace KG indexes."""
    cur.execute("PRAGMA journal_mode=WAL")
    cur.execute("PRAGMA busy_timeout=10000")
    cur.execute(ENTITIES_DDL)
    cur.execute(TRIPLES_DDL)
    for ddl in INDEXES_DDL:
        cur.execute(ddl)


def _collect_prev_hydrator_ids(cur: sqlite3.Cursor) -> Set[str]:
    """Collect existing hydrator-managed entity IDs prior to scoped refresh."""
    rows = cur.execute(
        """SELECT id FROM entities
           WHERE json_extract(properties, '$.managed_by') = ?
              OR id LIKE 'note:%'
              OR id LIKE 'skill:%'
              OR id LIKE 'subagent:%'
              OR id = 'repo:franklin_quebragalho'""",
        (ADAPTER_NAME,),
    ).fetchall()
    return {str(row[0]) for row in rows}


def _upsert_and_prune_kg(
    cur: sqlite3.Cursor,
    all_entities: Dict[str, EntityTuple],
    all_triples: List[TripleTuple],
    now_iso: str,
) -> None:
    """Replace hydrator-scoped triples and upsert entities without clobbering external facts."""
    prev_ids = _collect_prev_hydrator_ids(cur)
    cur.execute("DELETE FROM triples WHERE adapter_name = ?", (ADAPTER_NAME,))
    cur.executemany(
        """INSERT INTO entities (id, name, type, properties, created_at)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(id) DO UPDATE SET
               name = excluded.name,
               type = excluded.type,
               properties = excluded.properties""",
        [(eid, name, etype, props, now_iso) for eid, name, etype, props in all_entities.values()],
    )
    cur.executemany(
        """INSERT OR REPLACE INTO triples
           (id, subject, predicate, object, valid_from, confidence, source_closet, source_file, adapter_name, extracted_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            (_triple_id(s, p, o), s, p, o, now_iso, 1.0, closet, sfile, ADAPTER_NAME, now_iso)
            for s, p, o, closet, sfile in all_triples
        ],
    )
    stale_ids = sorted(prev_ids - set(all_entities.keys()))
    if stale_ids:
        cur.executemany(
            """DELETE FROM entities
               WHERE id = ?
                 AND id NOT IN (SELECT subject FROM triples UNION SELECT object FROM triples)""",
            [(eid,) for eid in stale_ids],
        )


def hydrate_knowledge_graph(
    vault_dir: Path = DEFAULT_VAULT_DIR,
    repo_dir: Path = DEFAULT_REPO_DIR,
    kg_db_path: Path = DEFAULT_KG_DB,
) -> Dict[str, int | str]:
    """Hydrate entities and triples from Obsidian and Franklin into MemPalace SQLite."""
    kg_db_path.parent.mkdir(parents=True, exist_ok=True)
    v_entities, v_triples = _collect_vault_entities_and_triples(vault_dir)
    e_entities, e_triples = _collect_ecosystem_entities_and_triples(repo_dir)
    all_entities = {ent[0]: ent for ent in (v_entities + e_entities)}
    all_triples = v_triples + e_triples
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    conn = sqlite3.connect(str(kg_db_path), timeout=10.0)
    try:
        cur = conn.cursor()
        _init_kg_schema(cur)
        _upsert_and_prune_kg(cur, all_entities, all_triples, now_iso)
        conn.commit()
        total_entities = int(cur.execute("SELECT COUNT(*) FROM entities").fetchone()[0])
        total_triples = int(cur.execute("SELECT COUNT(*) FROM triples").fetchone()[0])
    finally:
        conn.close()

    return {
        "status": "HYDRATED",
        "database": str(kg_db_path),
        "entities_upserted": len(all_entities),
        "triples_upserted": len(all_triples),
        "total_entities": total_entities,
        "total_triples": total_triples,
    }


def _seed_external_kg_fact(db_path: Path) -> None:
    """Seed an unadapted MCP-style entity and triple to verify non-destructive hydration."""
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        _init_kg_schema(cur)
        cur.execute(
            "INSERT INTO entities (id, name, type, properties) VALUES (?, ?, ?, ?)",
            ("ext:manual", "ManualFact", "manual", '{"origin":"mcp"}'),
        )
        cur.execute(
            "INSERT INTO entities (id, name, type, properties) VALUES (?, ?, ?, ?)",
            ("ext:target", "TargetVal", "manual", '{"origin":"mcp"}'),
        )
        cur.execute(
            """INSERT INTO triples (id, subject, predicate, object, valid_from, adapter_name)
               VALUES (?, ?, ?, ?, ?, NULL)""",
            ("trp:manual_1", "ext:manual", "USES_MODEL", "ext:target", "2026-11-18T00:00:00Z"),
        )
        conn.commit()
    finally:
        conn.close()


def _verify_self_test_assertions(db_path: Path, expected_skills: int, expected_agents: int) -> None:
    """Assert isolation, private exclusion, external triple survival, and stale pruning."""
    conn = sqlite3.connect(str(db_path))
    try:
        ext_trp = conn.execute("SELECT COUNT(*) FROM triples WHERE id = 'trp:manual_1' AND adapter_name IS NULL").fetchone()[0]
        assert ext_trp == 1, "External NULL-adapter triple was lost during hydration"
        ext_ent = conn.execute("SELECT COUNT(*) FROM entities WHERE id = 'ext:manual'").fetchone()[0]
        assert ext_ent == 1, "External entity ext:manual was deleted"
        iso_ent = conn.execute("SELECT COUNT(*) FROM entities WHERE id = 'note:isolada'").fetchone()[0]
        assert iso_ent == 1, "Zero-wikilink active note note:isolada was wrongly pruned"
        rem_ent = conn.execute("SELECT COUNT(*) FROM entities WHERE id = 'note:removida'").fetchone()[0]
        assert rem_ent == 0, "Deleted note note:removida was not pruned on second hydration"
        priv_ent = conn.execute("SELECT COUNT(*) FROM entities WHERE id = 'note:privada'").fetchone()[0]
        assert priv_ent == 0, "Private note note:privada leaked into KG"
        hub_raw = conn.execute("SELECT properties FROM entities WHERE id = 'repo:franklin_quebragalho'").fetchone()[0]
        hub_props = json.loads(hub_raw)
        assert hub_props["skills"] == expected_skills and hub_props["subagents"] == expected_agents, hub_props
    finally:
        conn.close()


def _run_self_test() -> int:
    """Execute deterministic self-tests against an isolated temporary SQLite database."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        v_dir = tmp_path / "notes" / "Memória"
        v_dir.mkdir(parents=True)
        (v_dir / "Decisões.md").write_text("Link para [[Ambiente Dev]].", encoding="utf-8")
        (v_dir / "Isolada.md").write_text("Nota ativa sem links.", encoding="utf-8")
        (v_dir / "Privada.md").write_text("---\nprivate: true\n---\nSegredo [[Secreto]].", encoding="utf-8")
        removida = v_dir / "Removida.md"
        removida.write_text("Link temporário [[Decisões]].", encoding="utf-8")

        repo_dir = tmp_path / "repo"
        (repo_dir / "skills" / "alpha").mkdir(parents=True)
        (repo_dir / "skills" / "alpha" / "SKILL.md").write_text("# Alpha", encoding="utf-8")
        (repo_dir / "agents").mkdir(parents=True)
        (repo_dir / "agents" / "worker.md").write_text("# Worker", encoding="utf-8")

        db_path = tmp_path / "kg.sqlite3"
        _seed_external_kg_fact(db_path)
        hydrate_knowledge_graph(vault_dir=tmp_path / "notes", repo_dir=repo_dir, kg_db_path=db_path)
        removida.unlink()
        hydrate_knowledge_graph(vault_dir=tmp_path / "notes", repo_dir=repo_dir, kg_db_path=db_path)
        _verify_self_test_assertions(db_path, expected_skills=1, expected_agents=1)

    print(json.dumps({"self_test": "PASS", "verified": True}, ensure_ascii=False))
    return 0


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Hydrate MemPalace SQLite Knowledge Graph.")
    parser.add_argument("--self-test", action="store_true", help="Run isolated self-test suite.")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    print(json.dumps(hydrate_knowledge_graph(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
