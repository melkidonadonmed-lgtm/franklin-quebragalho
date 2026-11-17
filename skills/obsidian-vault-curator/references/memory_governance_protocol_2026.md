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

- **Mandatory Metadata**: Every note under `Memória/` and `Projetos/` must include YAML frontmatter with `title`, `date: YYYY-MM-DD`, `status: ativo | arquivado | desatualizado`, and `tags`.
- **Soft Delete Invalidation**:
  - Superseded notes receive `type: historico` or `type: arquivo` and `status: desatualizado` or `status: arquivado`.
  - The JIT search engine (`scripts/vault_palace_search.py`) automatically demotes notes with `type in ("historico", "arquivo")` or `status in ("desatualizado", "obsoleto", "arquivado")` to the `"arquivo"` room (`0.55x`–`0.60x` multiplier instead of `1.35x`–`1.40x`).
- **SQLite Graph Hygiene (`scripts/vault_kg_hydrator.py`)**:
  - Ignore `[[Wikilinks]]` inside code blocks/inline code and generic placeholders (`wikilinks`, `nome da nota`, `projeto`).
  - Purge stale triples (`DELETE FROM triples; DELETE FROM entities;`) before rehydrating the 4 `knowledge_graph.sqlite3` mirrors.
- **Lock-Safe Windows Synchronization**:
  - When `mempalace-mcp.exe` is active in the session, use MCP tools `mempalace_mine(source="C:\\Users\\melki\\dev\\notes", wing="notes")`, `mempalace_sync(apply=true, project_dir="C:\\Users\\melki\\dev\\notes", wing="notes")`, and `mempalace_delete_drawer` rather than spawning a competing CLI `mempalace mine` subprocess.

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
