# Context Engineering, Audit & Memory Governance Protocol (2026)

> **Scope:** Canonical Tier 3 reference for `obsidian-vault-curator` and the symbiotic `Obsidian Vault` (`C:\Users\melki\dev\notes`) + `MemPalace` (`wing: notes`) + `Knowledge Graph SQLite` ecosystem.

---

## 1. Attention Dynamics & Preventing Token Dispersion

Transformer attention weights keys and queries via:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

When obsolete, verbose, or contradictory notes remain active inside high-priority rooms such as `memoria` (`1.40x`) or `projetos` (`1.35x`), the $\text{softmax}$ denominator accumulates spurious entries (**attention dispersion**), reducing probability mass allocated to system rules and active task parameters.

---

## 2. Strict 4-Layer Operational Memory Taxonomy

1. **Working Memory**:
   - Volatile active session state, immediate goals, and runtime variables (`temp:` invocation-scoped state).
   - Transient conversational noise must never be persisted into the vault.
2. **Semantic Memory**:
   - Durable facts, stable preferences, and active workspace topology: `Memória/Ambiente Dev (PC atual).md`, `Memória/Preferências de Trabalho com Agentes.md`, and `Projetos/Repositórios na Máquina.md`.
   - Updated **in-place** whenever runtime versions, repository/skill counts, or structural rules change.
3. **Episodic Memory**:
   - Chronological milestones and decision logs: `Memória/Decisões.md`, `Diário/AAAA-MM-DD.md`, and `hall_diary` drawers in MemPalace.
   - **Partition Ceiling (`< 25 KB`)**: Whenever `Memória/Decisões.md` exceeds `25 KB`, older entries before recent active decisions must move to `Arquivo/Decisões - Histórico Vol. N.md` (`type: arquivo`, `status: arquivado`).
4. **Procedural Memory**:
   - Deterministic routines, `AGENTS.md` / `SKILL.md` contracts, and validated scripts (`vault_palace_search.py`, `vault_kg_hydrator.py`, `vault_hygiene_scanner.py`, `sync-dev-workspace.ps1`).

---

## 3. Temporal Invalidation & Conflict Resolution

- **Mandatory Metadata & 4-Tier SOTA Ranking**: Every note under `Memória/` and `Projetos/` must include YAML frontmatter with `title`, `date: YYYY-MM-DD`, `status: ativo | arquivado | desatualizado`, and `tags`; architectural, idea, example, and triaged notes also carry `veredito: recomendado | casos-especificos | nao-recomendado | contraindicacao-total`, `funcao:`, and `#sota/<tier>`.
- **Dual-Engine Invalidation (`vault_palace_search.py` v2.2 + Upstream MemPalace)**:
  - Superseded notes receive `type: historico` or `type: arquivo` and `status: desatualizado` or `status: arquivado`.
  - `scripts/vault_palace_search.py` (`INDEX_SCHEMA_VERSION = "2.2"`) applies `VEREDITO_PRIORITY` (`recomendado 1.10x`, `casos-especificos 1.00x`, `nao-recomendado 0.75x -> arquivo`, `contraindicacao-total 0.50x -> arquivo`) alongside `type`/`status` demotion (`0.55x`–`0.60x`).
  - Because upstream MemPalace `miner.py` `detect_room()` ignores YAML and classifies solely by folder path, `contraindicacao-total` notes MUST be physically isolated in `Arquivo/Contraindicados/` to keep `mempalace_search(room="projetos")` clean.
- **Closet-First Authoring (`MemPalace v3.12.0`)**:
  - Keep `H1`–`H3` headings within `5..60` characters inside the first `5,000` chars (`CLOSET_EXTRACT_WINDOW`) and place one `"15..150"`-char double-quoted verdict near the top so Closet extraction reaches up to `+0.40` `closet_boost`.
- **SQLite Graph Hygiene (`scripts/vault_kg_hydrator.py`)**:
  - Ignore `[[Wikilinks]]` inside code blocks/inline code and generic placeholders (`wikilinks`, `nome da nota`, `projeto`).
  - Invoke `vault_kg_hydrator.py` without `--vault` (only `[--self-test]` is accepted). It hydrates the unified `~/.config/mempalace/palace/knowledge_graph.sqlite3` via scoped replacement (`WHERE adapter_name = 'vault_kg_hydrator_v1'`), preserving MCP-authored temporal facts (`adapter_name IS NULL`).
  - Record architectural replacements/retirements atomically with MCP `mempalace_kg_supersede` and `mempalace_kg_invalidate` so point-in-time queries reflect historical boundaries (`expired_facts > 0`).
- **Lock-Safe Windows Synchronization & `exclude_patterns` Purge Trap**:
  - When `mempalace-mcp.exe` is active in the session, use MCP tools `mempalace_mine(source="C:\\Users\\melki\\dev\\notes", wing="notes")`, `mempalace_sync(apply=true, project_dir="C:\\Users\\melki\\dev\\notes", wing="notes")`, and `mempalace_delete_drawers` rather than spawning a competing CLI `mempalace mine` subprocess.
  - **Gotcha (`exclude_patterns`):** `mempalace_sync` only prunes deleted or `.gitignore`d files—it does NOT remove pre-existing drawers matching newly added `mempalace.yaml` `exclude_patterns`. Moreover, `mempalace_list_drawers` previews basename-only `source_file` (causing `mempalace_delete_by_source("<basename>")` to delete `0` rows). Always list `room="general"` with `mempalace_list_drawers(wing="notes", room="general", limit=100)`, delete leaked IDs in bulk with `mempalace_delete_drawers(drawer_ids=[...])`, and confirm `generic_drawers: 0` via `mempalace audit --json`.

---

## 4. Standardized Memory Audit Output Schema

When a structured memory governance audit report is requested, format the payload strictly as:

```json
{
  "general_analysis": {
    "total_entries_analyzed": 0,
    "consolidated_active_entries": 0,
    "invalidated_or_purged_entries": 0,
    "estimated_tokens_saved": 0
  },
  "optimized_memory_bank": [
    {
      "id": "MEM-001",
      "category": "semantic | episodic | procedural | working",
      "consolidated_fact": "Atomic, accurate, concise factual statement.",
      "scope": "user | project | task_specific",
      "status": "active | obsolete | purged",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
      "confidence": 0.95,
      "activation_triggers": ["tag1", "keyword", "task_condition"],
      "audit_reason": "Summary of curation action (consolidation, temporal invalidation, or purge)."
    }
  ],
  "retrieval_orchestrator_guidelines": {
    "max_memory_token_budget": 800,
    "min_relevance_score": 0.75,
    "purge_rules": "Criteria to prevent unnecessary retrieval in the active session."
  }
}
```
