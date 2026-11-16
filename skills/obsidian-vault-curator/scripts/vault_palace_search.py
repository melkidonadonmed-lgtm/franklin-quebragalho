#!/usr/bin/env python3
"""
vault_palace_search.py
Motor híbrido de busca rápida (< 25ms) e indexação incremental por seções para o Cofre Obsidian
(C:\\Users\\melki\\dev\\notes) + MemPalace SQLite/ChromaDB (wing: notes).
Combina índice incremental de seções Markdown com Min-Chunk Merge (< 160B), Max-Chunk Split (> 1.800 chars),
cabeçalho contextual [ID | Project | Room | Heading], priorização de salas ativas sobre Arquivo/,
expansão de grafo 1-hop [[Wikilinks]] e Reciprocal Rank Fusion (RRF) direto via SQLite FTS5 (mode=ro).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_VAULT = Path(r"C:\Users\melki\dev\notes")
MEMPALACE_CONFIG_DIR = Path.home() / ".config" / "mempalace"
CACHE_PATH = MEMPALACE_CONFIG_DIR / "vault_sections_index.json"
CHROMA_DB_PATH = MEMPALACE_CONFIG_DIR / "palace" / "chroma.sqlite3"
MIN_CHUNK_BYTES = 160
MAX_CHUNK_CHARS = 1800
INDEX_SCHEMA_VERSION = "2.1"

SKIP_DIRS = {".obsidian", ".git", "node_modules", ".trash"}
WIKILINK_RX = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
CANONICAL_ID_RX = re.compile(r"\[((?:PRJ|SYS)-\d{3}[A-Z]?)\s*\|\s*([a-z0-9\-]+)\]", re.IGNORECASE)

FOLDER_TO_ROOM: Dict[str, str] = {
    "memória": "memoria", "memoria": "memoria", "projetos": "projetos",
    "medicina": "medicina", "pessoal": "pessoal", "interesses": "interesses",
    "diário": "diario", "diario": "diario", "inbox": "inbox",
    "arquivo": "arquivo", "modelos": "templates",
}

ROOM_PRIORITY: Dict[str, float] = {
    "memoria": 1.40, "projetos": 1.35, "medicina": 1.35, "pessoal": 1.25,
    "interesses": 1.20, "diario": 1.15, "inbox": 1.10, "arquivo": 0.55, "templates": 0.50,
}

INTENT_ROOM_HINTS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("memoria", ("decisao", "decisoes", "preferencia", "ambiente", "pc", "dossie", "qualidade", "regra", "auditoria")),
    ("projetos", ("repo", "repositorio", "skill", "mcp", "adk", "deploy", "franklin", "epic", "mytts", "pcm", "gostylo")),
    ("medicina", ("medicina", "clinica", "soap", "dose", "bulario", "plantao", "exame", "semiologia")),
    ("pessoal", ("financa", "conta", "tdah", "sono", "rotina", "habito")),
)


@dataclass(frozen=True)
class SectionHit:
    source_id: str
    file_uri: str
    room: str
    title: str
    heading: str
    line_range: List[int]
    byte_range: List[int]
    score: float
    tags: List[str] = field(default_factory=list)
    wikilinks: List[str] = field(default_factory=list)
    snippet: str = ""


@dataclass(frozen=True)
class SearchResponse:
    query: str
    mode: str
    room_filter: str
    inferred_rooms: List[str]
    elapsed_ms: float
    total_sections_indexed: int
    hits: List[SectionHit]
    graph_neighbors: List[Dict[str, str]]


def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def _slugify(text: str) -> str:
    normed = _norm(text)
    return re.sub(r"[^a-z0-9]+", "-", normed).strip("-") or "note"


def _parse_frontmatter(md_text: str) -> Tuple[Dict[str, str], List[str], int]:
    """Extrai metadados simples, tags e linha final do frontmatter YAML."""
    if not md_text.startswith("---"):
        return {}, [], 1
    lines = md_text.splitlines()
    end_idx = next((i for i in range(1, min(40, len(lines))) if lines[i].strip() == "---"), 0)
    if end_idx == 0:
        return {}, [], 1
    meta: Dict[str, str] = {}
    for line in lines[1:end_idx]:
        if ":" in line and not line.strip().startswith("-"):
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip().strip("\"'")
    tags = re.findall(r"[A-Za-z0-9_\-/À-ÿ]+", meta.get("tags", ""))
    for line in lines[1:end_idx]:
        if line.strip().startswith("- "):
            tags.append(line.strip()[2:].strip().strip("\"'"))
    return meta, sorted(set(tags)), end_idx + 2


def _is_private_note(meta: Mapping[str, str], tags: Sequence[str]) -> bool:
    if meta.get("private", "").lower() == "true" or meta.get("phi", "").lower() == "true":
        return True
    joined_tags = " ".join(tags).lower()
    return any(tok in joined_tags for tok in ("private", "phi", "confidencial"))


def _resolve_canonical_header(rel_id: str, room: str, title: str, heading: str, body_txt: str) -> Tuple[str, str]:
    """Resolve ID canônico e projeto a partir de marcadores [PRJ-XXX | slug] ou caminho da nota."""
    match = CANONICAL_ID_RX.search(body_txt) or CANONICAL_ID_RX.search(heading)
    if match:
        cid, proj_slug = match.group(1).upper(), match.group(2).lower()
    else:
        proj_slug = _slugify(Path(rel_id).stem if room == "projetos" else title)
        short_hash = hashlib.sha1(f"{rel_id}:{heading}".encode("utf-8")).hexdigest()[:4].upper()
        prefix = "PRJ" if room == "projetos" else ("MEM" if room == "memoria" else "SEC")
        cid = f"{prefix}-{short_hash}"
    header = f"[{cid} | {proj_slug} | {room} | {heading}]"
    return cid, header


def _extract_raw_heading_blocks(lines: List[str], body_start_line: int, title: str) -> List[Dict[str, Any]]:
    """Extrai blocos brutos delimitados por headings Markdown (#, ##, ###)."""
    raw_blocks: List[Dict[str, Any]] = []
    cur_heading = title
    cur_start_line = body_start_line
    cur_byte_start = sum(len(ln.encode("utf-8")) for ln in lines[: max(0, body_start_line - 1)])
    cur_buf: List[str] = []

    for idx in range(max(0, body_start_line - 1), len(lines)):
        line = lines[idx]
        if line.startswith(("# ", "## ", "### ")) and cur_buf:
            raw_text = "".join(cur_buf)
            byte_len = len(raw_text.encode("utf-8"))
            if raw_text.strip():
                raw_blocks.append({
                    "heading": cur_heading,
                    "text": raw_text,
                    "l_start": cur_start_line,
                    "l_end": idx,
                    "b_start": cur_byte_start,
                    "b_end": cur_byte_start + byte_len,
                })
            cur_heading = line.lstrip("#").strip() or title
            cur_start_line = idx + 1
            cur_byte_start += byte_len
            cur_buf = [line]
        else:
            cur_buf.append(line)

    if cur_buf and "".join(cur_buf).strip():
        raw_text = "".join(cur_buf)
        byte_len = len(raw_text.encode("utf-8"))
        raw_blocks.append({
            "heading": cur_heading,
            "text": raw_text,
            "l_start": cur_start_line,
            "l_end": len(lines),
            "b_start": cur_byte_start,
            "b_end": cur_byte_start + byte_len,
        })
    return raw_blocks


def _merge_small_blocks(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Funde blocos menores que MIN_CHUNK_BYTES (160B) com o bloco adjacente (Min-Chunk Merge)."""
    if len(blocks) <= 1:
        return blocks
    merged: List[Dict[str, Any]] = []
    carry: Dict[str, Any] | None = None
    for blk in blocks:
        if carry is not None:
            combined_heading = f"{carry['heading']} — {blk['heading']}" if carry["heading"] != blk["heading"] else blk["heading"]
            blk = {
                "heading": combined_heading,
                "text": carry["text"] + blk["text"],
                "l_start": carry["l_start"],
                "l_end": blk["l_end"],
                "b_start": carry["b_start"],
                "b_end": blk["b_end"],
            }
            carry = None
        if len(blk["text"].strip().encode("utf-8")) < MIN_CHUNK_BYTES:
            carry = blk
        else:
            merged.append(blk)

    if carry is not None:
        if merged:
            prev = merged[-1]
            merged[-1] = {
                "heading": prev["heading"],
                "text": prev["text"] + carry["text"],
                "l_start": prev["l_start"],
                "l_end": carry["l_end"],
                "b_start": prev["b_start"],
                "b_end": carry["b_end"],
            }
        else:
            merged.append(carry)
    return merged


def _split_oversized_block(blk: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Divide blocos maiores que MAX_CHUNK_CHARS (1.800 chars) respeitando quebras de linha."""
    text = blk["text"]
    if len(text.strip()) <= MAX_CHUNK_CHARS:
        return [blk]
    blk_lines = text.splitlines(keepends=True)
    sub_blocks: List[Dict[str, Any]] = []
    cur_lines: List[str] = []
    cur_chars = 0
    sub_l_start = blk["l_start"]
    sub_b_start = blk["b_start"]

    for idx, ln in enumerate(blk_lines):
        is_para_break = not ln.strip() or ln.lstrip().startswith(("- ", "* ", "1.", "|"))
        if cur_chars + len(ln) > MAX_CHUNK_CHARS and cur_lines and (is_para_break or cur_chars >= MAX_CHUNK_CHARS // 2):
            sub_txt = "".join(cur_lines)
            b_len = len(sub_txt.encode("utf-8"))
            sub_blocks.append({
                "heading": blk["heading"],
                "text": sub_txt,
                "l_start": sub_l_start,
                "l_end": blk["l_start"] + idx - 1,
                "b_start": sub_b_start,
                "b_end": sub_b_start + b_len,
            })
            sub_l_start = blk["l_start"] + idx
            sub_b_start += b_len
            cur_lines = [ln]
            cur_chars = len(ln)
        else:
            cur_lines.append(ln)
            cur_chars += len(ln)

    if cur_lines and "".join(cur_lines).strip():
        sub_txt = "".join(cur_lines)
        if sub_blocks and len(sub_txt.strip().encode("utf-8")) < MIN_CHUNK_BYTES:
            prev = sub_blocks[-1]
            sub_blocks[-1] = {
                "heading": prev["heading"],
                "text": prev["text"] + sub_txt,
                "l_start": prev["l_start"],
                "l_end": blk["l_end"],
                "b_start": prev["b_start"],
                "b_end": blk["b_end"],
            }
        else:
            sub_blocks.append({
                "heading": blk["heading"],
                "text": sub_txt,
                "l_start": sub_l_start,
                "l_end": blk["l_end"],
                "b_start": sub_b_start,
                "b_end": blk["b_end"],
            })

    total = len(sub_blocks)
    if total > 1:
        for i, sb in enumerate(sub_blocks, start=1):
            sb["heading"] = f"{sb['heading']} ({i}/{total})"
    return sub_blocks


def _split_markdown_sections(rel_id: str, abs_path: Path, room: str, md_text: str) -> List[Dict[str, Any]]:
    meta, tags, body_start_line = _parse_frontmatter(md_text)
    if _is_private_note(meta, tags):
        return []
    if (
        meta.get("type", "").lower() in ("historico", "arquivo")
        or meta.get("status", "").lower() in ("desatualizado", "obsoleto", "arquivado")
    ):
        room = "arquivo"
    title = meta.get("title") or abs_path.stem
    lines = md_text.splitlines(keepends=True)
    raw_blocks = _extract_raw_heading_blocks(lines, body_start_line, title)
    merged_blocks = _merge_small_blocks(raw_blocks)

    sections: List[Dict[str, Any]] = []
    for blk in merged_blocks:
        for sub in _split_oversized_block(blk):
            body_txt = sub["text"].strip()
            if body_txt:
                sections.append(_build_sec_dict(
                    rel_id, room, title, sub["heading"], tags, body_txt,
                    sub["l_start"], sub["l_end"], sub["b_start"], sub["b_end"],
                ))
    return sections


def _build_sec_dict(
    rel_id: str, room: str, title: str, heading: str, tags: List[str],
    body_txt: str, l_start: int, l_end: int, b_start: int, b_end: int,
) -> Dict[str, Any]:
    links = sorted({m.strip() for m in WIKILINK_RX.findall(body_txt) if m.strip()})
    cid, header = _resolve_canonical_header(rel_id, room, title, heading, body_txt)
    enriched_snippet = f"{header}\n{body_txt}"
    if len(enriched_snippet.encode("utf-8")) < MIN_CHUNK_BYTES:
        enriched_snippet = f"{enriched_snippet}\n[Fonte: {rel_id} | Título: {title} | Tags: {', '.join(tags) or room}]"
    return {
        "source_id": rel_id,
        "canonical_id": cid,
        "room": room,
        "title": title,
        "heading": heading,
        "tags": tags,
        "wikilinks": links,
        "line_range": [max(1, l_start), max(l_start, l_end)],
        "byte_range": [b_start, b_end],
        "snippet": enriched_snippet,
        "norm_cache": [
            _norm(title),
            _norm(heading),
            _norm(" ".join(tags)),
            _norm(" ".join(links)),
            _norm(enriched_snippet),
        ],
    }


def _resolve_room_for_rel(rel_id: str) -> str:
    first_part = rel_id.split("/", 1)[0].lower()
    return FOLDER_TO_ROOM.get(first_part, "projetos")


def _scan_dir_single(cur_dir: str, vault_str: str, stack: List[str], out: List[Tuple[str, str, os.stat_result]]) -> None:
    try:
        with os.scandir(cur_dir) as it:
            for entry in it:
                if entry.is_dir(follow_symlinks=False) and entry.name not in SKIP_DIRS:
                    stack.append(entry.path)
                elif entry.is_file(follow_symlinks=False) and entry.name.endswith(".md"):
                    rel_id = entry.path[len(vault_str) + 1 :].replace("\\", "/")
                    out.append((rel_id, entry.path, entry.stat(follow_symlinks=False)))
    except OSError:
        return


def _scan_markdown_entries(vault_str: str) -> List[Tuple[str, str, os.stat_result]]:
    stack = [vault_str]
    entries_found: List[Tuple[str, str, os.stat_result]] = []
    while stack:
        _scan_dir_single(stack.pop(), vault_str, stack, entries_found)
    return sorted(entries_found, key=lambda x: x[0])


def load_or_update_index(vault_path: Path, force_rebuild: bool = False) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """Carrega ou atualiza incrementalmente o índice de seções em ~/.config/mempalace (< 5ms se inalterado)."""
    cached_files: Dict[str, Any] = {}
    if not force_rebuild and CACHE_PATH.exists():
        try:
            raw = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            if isinstance(raw, dict) and raw.get("schema_version") == INDEX_SCHEMA_VERSION:
                cached_files = raw.get("files", {})
        except (OSError, json.JSONDecodeError):
            cached_files = {}

    new_files: Dict[str, Any] = {}
    note_map: Dict[str, str] = {}
    dirty = force_rebuild or not cached_files
    for rel_id, full_str, st in _scan_markdown_entries(str(vault_path)):
        stem = os.path.basename(full_str)[:-3]
        note_map[_norm(stem)] = rel_id
        sig = f"{st.st_mtime_ns}:{st.st_size}"
        prev = cached_files.get(rel_id)
        if prev and prev.get("sig") == sig:
            new_files[rel_id] = prev
            continue
        dirty = True
        md_file = Path(full_str)
        room = _resolve_room_for_rel(rel_id)
        text = md_file.read_text(encoding="utf-8", errors="replace")
        new_files[rel_id] = {"sig": sig, "sections": _split_markdown_sections(rel_id, md_file, room, text)}

    if dirty or len(new_files) != len(cached_files):
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema_version": INDEX_SCHEMA_VERSION, "files": new_files}
        CACHE_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    all_sections = [sec for item in new_files.values() for sec in item.get("sections", [])]
    return all_sections, note_map


def _infer_rooms(norm_terms: Sequence[str], explicit_room: str) -> List[str]:
    if explicit_room and explicit_room != "all":
        return [explicit_room.lower()]
    inferred = [r for r, kws in INTENT_ROOM_HINTS if any(any(k in t or t in k for k in kws) for t in norm_terms)]
    return inferred or ["memoria", "projetos"]


def _score_section(
    sec: Mapping[str, Any], norm_q: str, terms: Sequence[str], explicit_room: str, inferred_rooms: Sequence[str]
) -> float:
    sec_room = str(sec.get("room", ""))
    if explicit_room and explicit_room != "all" and sec_room != explicit_room:
        return 0.0
    nc = sec.get("norm_cache")
    if isinstance(nc, list) and len(nc) == 5:
        title_n, head_n, tags_n, links_n, body_n = nc[0], nc[1], nc[2], nc[3], nc[4]
    else:
        title_n = _norm(str(sec.get("title", "")))
        head_n = _norm(str(sec.get("heading", "")))
        tags_n = _norm(" ".join(sec.get("tags", [])))
        links_n = _norm(" ".join(sec.get("wikilinks", [])))
        body_n = _norm(str(sec.get("snippet", "")))

    raw_score = 4.0 if norm_q in head_n or norm_q in title_n else (2.0 if norm_q in body_n else 0.0)
    matched_terms = 0
    for t in terms:
        t_hit = (
            (3.5 if t in title_n else 0.0)
            + (2.5 if t in head_n else 0.0)
            + (2.0 if t in tags_n else 0.0)
            + (1.5 if t in links_n else 0.0)
            + (1.0 if t in body_n else 0.0)
        )
        if t_hit > 0:
            matched_terms += 1
            raw_score += t_hit
    if raw_score == 0.0:
        return 0.0
    coverage_boost = 1.0 + (0.25 * (matched_terms / max(1, len(terms))))
    room_mult = 1.0 if explicit_room else ROOM_PRIORITY.get(sec_room, 1.0)
    intent_mult = 1.25 if (not explicit_room and sec_room in inferred_rooms) else 1.0
    return round(raw_score * coverage_boost * room_mult * intent_mult, 3)


def _query_chroma_fts_direct(terms: Sequence[str], room: str, limit: int) -> Dict[str, float]:
    """Consulta diretamente a tabela FTS5 do ChromaDB em SQLite (mode=ro, < 5ms) com filtro pré-HNSW."""
    if not CHROMA_DB_PATH.exists() or not terms:
        return {}
    fts_expr = " OR ".join(f'"{t}"' for t in terms[:8] if t.isalnum() or "-" in t)
    if not fts_expr:
        return {}
    room_clause = (
        "HAVING MAX(CASE WHEN m.key = 'room' THEN m.string_value END) = ?"
        if (room and room != "all")
        else "HAVING COALESCE(MAX(CASE WHEN m.key = 'room' THEN m.string_value END), '') != 'arquivo'"
    )
    sql = f"""
    WITH fts_hits AS (
        SELECT rowid, bm25(embedding_fulltext_search) AS rank_score
        FROM embedding_fulltext_search
        WHERE embedding_fulltext_search MATCH ?
        ORDER BY rank_score
        LIMIT ?
    )
    SELECT MAX(CASE WHEN m.key = 'source_file' THEN m.string_value END) AS source_file,
           fts_hits.rank_score
    FROM fts_hits
    JOIN embedding_metadata m ON m.id = fts_hits.rowid
    GROUP BY fts_hits.rowid
    {room_clause}
    ORDER BY fts_hits.rank_score
    """
    params: Tuple[Any, ...] = (fts_expr, max(20, limit * 5), room) if (room and room != "all") else (fts_expr, max(20, limit * 5))
    stem_ranks: Dict[str, float] = {}
    try:
        with sqlite3.connect(f"file:{CHROMA_DB_PATH.as_posix()}?mode=ro", uri=True, timeout=1.5) as conn:
            rows = conn.execute(sql, params).fetchall()
        for rank_idx, (src_file, _) in enumerate(rows, start=1):
            if src_file:
                stem_n = _norm(Path(str(src_file)).stem)
                if stem_n and stem_n not in stem_ranks:
                    stem_ranks[stem_n] = 60.0 / (60.0 + rank_idx) * 5.0
    except sqlite3.Error:
        return {}
    return stem_ranks


def _apply_mempalace_rrf(
    scored: List[Tuple[float, Dict[str, Any]]], terms: Sequence[str], room: str, limit: int
) -> List[Tuple[float, Dict[str, Any]]]:
    """Combina o ranking de seções com o ranking FTS5/vetorial do ChromaDB via RRF (k=60) sem subprocesso."""
    stem_bonuses = _query_chroma_fts_direct(terms, room, limit)
    fused: List[Tuple[float, Dict[str, Any]]] = []
    for rank, (base_sc, sec) in enumerate(scored, start=1):
        rrf_bonus = 10.0 / (60.0 + rank)
        stem_n = _norm(Path(str(sec["source_id"])).stem)
        rrf_bonus += stem_bonuses.get(stem_n, 0.0)
        fused.append((round(base_sc + rrf_bonus, 3), sec))
    fused.sort(key=lambda x: x[0], reverse=True)
    return fused


def search_vault_and_palace(
    query: str,
    vault_path: Path = DEFAULT_VAULT,
    room: str = "",
    mode: str = "fast",
    limit: int = 5,
    force_rebuild: bool = False,
) -> SearchResponse:
    t0 = time.perf_counter()
    sections, note_map = load_or_update_index(vault_path, force_rebuild=force_rebuild)
    norm_q = _norm(query.strip())
    terms = [t for t in re.findall(r"[a-z0-9_\-]{2,}", norm_q) if t not in {"de", "do", "da", "em", "no", "na", "para", "com", "que"}]
    clean_room = _norm(room.strip())
    inferred = _infer_rooms(terms, clean_room)

    scored = [
        (sc, sec)
        for sec in sections
        if (sc := _score_section(sec, norm_q, terms, clean_room, inferred)) > 0.0
    ]
    scored.sort(key=lambda x: x[0], reverse=True)
    if mode.lower() == "hybrid" and scored:
        scored = _apply_mempalace_rrf(scored[: max(15, limit * 3)], terms, clean_room, limit)

    top_hits: List[SectionHit] = []
    neighbors: Dict[str, str] = {}
    for sc, sec in scored[:limit]:
        abs_uri = f"file:///{(vault_path / sec['source_id']).as_posix()}#L{sec['line_range'][0]}-L{sec['line_range'][1]}"
        top_hits.append(SectionHit(
            source_id=sec["source_id"], file_uri=abs_uri, room=sec["room"],
            title=sec["title"], heading=sec["heading"],
            line_range=sec["line_range"], byte_range=sec["byte_range"],
            score=sc, tags=sec["tags"], wikilinks=sec["wikilinks"], snippet=sec["snippet"],
        ))
        for wl in sec.get("wikilinks", []):
            target_rel = note_map.get(_norm(wl))
            if target_rel and target_rel != sec["source_id"]:
                neighbors[wl] = f"file:///{(vault_path / target_rel).as_posix()}"

    elapsed = round((time.perf_counter() - t0) * 1000.0, 2)
    return SearchResponse(
        query=query, mode=mode, room_filter=clean_room or "auto",
        inferred_rooms=inferred, elapsed_ms=elapsed,
        total_sections_indexed=len(sections), hits=top_hits,
        graph_neighbors=[{"wikilink": k, "uri": v} for k, v in list(neighbors.items())[:8]],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Busca Híbrida Rápida no Cofre Obsidian + MemPalace")
    parser.add_argument("--query", "-q", type=str, default="", help="Consulta de busca")
    parser.add_argument("--room", "-r", type=str, default="", help="Sala (memoria, projetos, medicina, pessoal, arquivo)")
    parser.add_argument("--mode", "-m", choices=("fast", "hybrid"), default="fast", help="fast (<15ms) ou hybrid (RRF + SQLite FTS5)")
    parser.add_argument("--limit", "-n", type=int, default=5, help="Número máximo de resultados")
    parser.add_argument("--vault", type=str, default=str(DEFAULT_VAULT), help="Caminho do cofre Obsidian")
    parser.add_argument("--rebuild-index", action="store_true", help="Reconstruir cache de seções")
    parser.add_argument("--json", action="store_true", help="Saída em JSON estruturado")
    parser.add_argument("--self-test", action="store_true", help="Executar auto-teste determinístico")
    args = parser.parse_args()

    q = args.query or ("qualidade de código ISO 25010" if args.self_test else "")
    if not q:
        parser.print_help()
        return 0

    resp = search_vault_and_palace(
        query=q, vault_path=Path(args.vault), room=args.room,
        mode=args.mode, limit=args.limit, force_rebuild=args.rebuild_index,
    )
    if args.json:
        print(json.dumps(asdict(resp), indent=2, ensure_ascii=False))
        return 0

    print(f"=== VAULT+PALACE SEARCH ({resp.mode.upper()} | {resp.elapsed_ms} ms | {resp.total_sections_indexed} seções) ===")
    for idx, h in enumerate(resp.hits, start=1):
        print(f"{idx}. [{h.room}] {h.title} :: {h.heading} (score={h.score}) -> {h.file_uri}")
        lines = h.snippet.splitlines()
        preview = lines[1] if len(lines) > 1 else (lines[0] if lines else "")
        print(f"   ↳ {preview[:140]}")
    if resp.graph_neighbors:
        links_str = ", ".join(f"[[{g['wikilink']}]]" for g in resp.graph_neighbors)
        print(f"🔗 Grafo 1-Hop: {links_str}")
    return 0 if (not args.self_test or len(resp.hits) > 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
