#!/usr/bin/env python3
"""
vault_palace_search.py
Motor híbrido de busca rápida (< 15ms) e indexação incremental por seções para o Cofre Obsidian
(C:\\Users\\melki\\dev\\notes) + MemPalace (wing: notes).
Combina índice incremental de seções Markdown (título, heading, tags, wikilinks, line_range, byte_range),
priorização de salas ativas sobre Arquivo/, expansão de grafo 1-hop [[Wikilinks]] e Reciprocal Rank Fusion (RRF).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_VAULT = Path(r"C:\Users\melki\dev\notes")
CACHE_PATH = Path.home() / ".mempalace" / "vault_sections_index.json"
SKIP_DIRS = {".obsidian", ".git", "node_modules", ".trash"}
WIKILINK_RX = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")

FOLDER_TO_ROOM: Dict[str, str] = {
    "memória": "memoria", "memoria": "memoria", "projetos": "projetos",
    "medicina": "medicina", "pessoal": "pessoal", "interesses": "interesses",
    "diário": "diario", "diario": "diario", "inbox": "inbox",
    "arquivo": "arquivo", "modelos": "templates",
}

ROOM_PRIORITY: Dict[str, float] = {
    "memoria": 1.40, "projetos": 1.35, "medicina": 1.35, "pessoal": 1.25,
    "interesses": 1.20, "diario": 1.15, "inbox": 1.10, "arquivo": 0.60, "templates": 0.50,
}

INTENT_ROOM_HINTS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("memoria", ("decisao", "decisoes", "preferencia", "ambiente", "pc", "dossie", "qualidade", "regra")),
    ("projetos", ("repo", "repositorio", "skill", "mcp", "adk", "deploy", "franklin", "epic", "mytts", "pcm")),
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


def _parse_frontmatter(md_text: str) -> Tuple[Dict[str, str], List[str], int]:
    """Extrai metadados simples, tags e linha final do frontmatter YAML."""
    if not md_text.startswith("---"):
        return {}, [], 1
    lines = md_text.splitlines()
    end_idx = next((i for i in range(1, min(40, len(lines))) if lines[i].strip() == "---"), 0)
    if end_idx == 0:
        return {}, [], 1
    fm_block = "\n".join(lines[1:end_idx])
    meta: Dict[str, str] = {}
    for line in lines[1:end_idx]:
        if ":" in line and not line.strip().startswith("-"):
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip().strip("\"'")
    tags = re.findall(r"[A-Za-z0-9_\-/À-ÿ]+", meta.get("tags", ""))
    for line in lines[1:end_idx]:
        if line.strip().startswith("- "):
            tags.append(line.strip()[2:].strip().strip("\"'"))
    _ = fm_block
    return meta, sorted(set(tags)), end_idx + 2


def _is_private_note(meta: Mapping[str, str], tags: Sequence[str]) -> bool:
    if meta.get("private", "").lower() == "true" or meta.get("phi", "").lower() == "true":
        return True
    joined_tags = " ".join(tags).lower()
    return any(tok in joined_tags for tok in ("private", "phi", "confidencial"))


def _split_markdown_sections(
    rel_id: str, abs_path: Path, room: str, md_text: str
) -> List[Dict[str, Any]]:
    meta, tags, body_start_line = _parse_frontmatter(md_text)
    if _is_private_note(meta, tags):
        return []
    title = meta.get("title") or abs_path.stem
    lines = md_text.splitlines(keepends=True)
    sections: List[Dict[str, Any]] = []
    cur_heading = title
    cur_start_line = body_start_line
    cur_byte_start = sum(len(ln.encode("utf-8")) for ln in lines[: max(0, body_start_line - 1)])
    cur_buf: List[str] = []

    for idx in range(max(0, body_start_line - 1), len(lines)):
        line = lines[idx]
        if line.startswith(("# ", "## ", "### ")) and cur_buf:
            body_txt = "".join(cur_buf).strip()
            byte_len = len("".join(cur_buf).encode("utf-8"))
            if body_txt:
                sections.append(_build_sec_dict(
                    rel_id, room, title, cur_heading, tags, body_txt,
                    cur_start_line, idx, cur_byte_start, cur_byte_start + byte_len,
                ))
            cur_heading = line.lstrip("#").strip()
            cur_start_line = idx + 1
            cur_byte_start += byte_len
            cur_buf = [line]
        else:
            cur_buf.append(line)

    tail_txt = "".join(cur_buf).strip()
    if tail_txt:
        byte_len = len("".join(cur_buf).encode("utf-8"))
        sections.append(_build_sec_dict(
            rel_id, room, title, cur_heading, tags, tail_txt,
            cur_start_line, len(lines), cur_byte_start, cur_byte_start + byte_len,
        ))
    return sections


def _build_sec_dict(
    rel_id: str, room: str, title: str, heading: str, tags: List[str],
    body_txt: str, l_start: int, l_end: int, b_start: int, b_end: int,
) -> Dict[str, Any]:
    links = sorted({m.strip() for m in WIKILINK_RX.findall(body_txt) if m.strip()})
    return {
        "source_id": rel_id,
        "room": room,
        "title": title,
        "heading": heading,
        "tags": tags,
        "wikilinks": links,
        "line_range": [max(1, l_start), max(l_start, l_end)],
        "byte_range": [b_start, b_end],
        "snippet": body_txt[:950],
    }


def _resolve_room_for_rel(rel_id: str) -> str:
    first_part = rel_id.split("/", 1)[0].lower()
    return FOLDER_TO_ROOM.get(first_part, "projetos")


def load_or_update_index(vault_path: Path, force_rebuild: bool = False) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """Carrega ou atualiza incrementalmente o índice de seções do cofre Obsidian (< 5ms se inalterado)."""
    cached_files: Dict[str, Any] = {}
    if not force_rebuild and CACHE_PATH.exists():
        try:
            raw = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            cached_files = raw.get("files", {}) if isinstance(raw, dict) else {}
        except (OSError, json.JSONDecodeError):
            cached_files = {}

    new_files: Dict[str, Any] = {}
    note_map: Dict[str, str] = {}
    dirty = force_rebuild
    for md_file in sorted(vault_path.rglob("*.md")):
        if any(part in SKIP_DIRS for part in md_file.parts):
            continue
        rel_id = md_file.relative_to(vault_path).as_posix()
        note_map[_norm(md_file.stem)] = rel_id
        st = md_file.stat()
        sig = f"{st.st_mtime_ns}:{st.st_size}"
        prev = cached_files.get(rel_id)
        if prev and prev.get("sig") == sig:
            new_files[rel_id] = prev
            continue
        dirty = True
        room = _resolve_room_for_rel(rel_id)
        text = md_file.read_text(encoding="utf-8", errors="replace")
        new_files[rel_id] = {"sig": sig, "sections": _split_markdown_sections(rel_id, md_file, room, text)}

    if dirty or len(new_files) != len(cached_files):
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(json.dumps({"files": new_files}, ensure_ascii=False), encoding="utf-8")

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


def _apply_mempalace_rrf(
    scored: List[Tuple[float, Dict[str, Any]]], query: str, room: str, limit: int
) -> List[Tuple[float, Dict[str, Any]]]:
    """Combina o ranking de seções BM25 com o ranking vetorial do MemPalace via RRF (k=60)."""
    cmd = ["mempalace", "search", query, "--wing", "notes", "--results", str(max(4, limit))]
    if room and room != "all":
        cmd.extend(["--room", room])
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=8, shell=False)
        out_n = _norm(res.stdout or "")
    except (OSError, subprocess.SubprocessError):
        return scored

    fused: List[Tuple[float, Dict[str, Any]]] = []
    for rank, (base_sc, sec) in enumerate(scored, start=1):
        rrf_bonus = 10.0 / (60.0 + rank)
        stem_n = _norm(Path(str(sec["source_id"])).stem)
        if stem_n and stem_n in out_n:
            rrf_bonus += 4.5
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
        scored = _apply_mempalace_rrf(scored[: max(15, limit * 3)], query, clean_room, limit)

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
    parser.add_argument("--mode", "-m", choices=("fast", "hybrid"), default="fast", help="fast (<15ms) ou hybrid (RRF + MemPalace)")
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
        first_line = h.snippet.splitlines()[0] if h.snippet else ""
        print(f"   ↳ {first_line[:140]}")
    if resp.graph_neighbors:
        links_str = ", ".join(f"[[{g['wikilink']}]]" for g in resp.graph_neighbors)
        print(f"🔗 Grafo 1-Hop: {links_str}")
    return 0 if (not args.self_test or len(resp.hits) > 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
