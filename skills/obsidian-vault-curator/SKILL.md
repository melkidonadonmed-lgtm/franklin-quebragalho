---
name: obsidian-vault-curator
description: "Audit and curate the Obsidian vault (C:\\Users\\melki\\dev\\notes) for broken Wikilinks, YAML frontmatter repair, orphaned attachments, repo parity, and MemPalace batch indexing (wing notes). Use for bulk vault hygiene; do NOT use for quick single-note CRUD (obsidian-vault), authoring docs from scratch (technical-markdown-writer), or Windows/Drive disk cleanup."
compatibility: "Windows 11, Python 3.12+, pwsh 7+, MemPalace MCP"
metadata:
  author: "Franklin"
  version: "1.3.0"
  updated_at: "2026-11-16"
  category: "Knowledge Management & Obsidian PKM"
  tags: ["obsidian", "vault", "cofre", "wikilinks", "frontmatter", "yaml", "mempalace", "curadoria", "higienizar", "anexos-orfaos", "notes", "bidirecionais", "hybrid-search"]
---

# Obsidian Vault Curation & Governance (`obsidian-vault-curator`)

## 1. Overview & Scope

Audit bulk structural hygiene of `C:\Users\melki\dev\notes\`: broken `[[Wikilinks]]`, missing YAML frontmatter, monoliths (`> 25 KB`), `Inbox/` pressure, orphaned attachments, repo parity (`dev\repos\` <-> `notes\Projetos\Ativos\`), and MemPalace batch sync (`wing: notes`).

- **When NOT to Use**: Quick single-note CRUD/recall (`obsidian-vault`), authoring new docs (`technical-markdown-writer`), Windows local cleanup (`windows-disk-maintenance`), or Google Drive cleanup (`gdrive-cleanup-auditor`).

## 2. Inputs & Prerequisites

- `vault_path` (optional): Default `C:\Users\melki\dev\notes\`, per [`references/default_vault_structure.json`](references/default_vault_structure.json).
- `audit_type` (optional): `full` (default), `orphaned_attachments`, `broken_links`, `frontmatter`, `repo_parity`.
- `orphan_quarantine_folder` (optional): Default `Arquivo/_anexos_orfaos`.
- **Prerequisites**: Access to `C:\Users\melki\dev\notes\` and MemPalace index (`~/.config/mempalace`).

## 3. Step-by-Step Procedure

1. **Hygiene Scan & Parity**: Set `$env:PYTHONUTF8 = "1"`, run [`scripts/vault_hygiene_scanner.py`](scripts/vault_hygiene_scanner.py) (`--json`), and execute `pwsh "C:\Users\melki\dev\tools\check-vault-projects.ps1"`. Use [`scripts/text_sanitizer_and_chunker.py`](scripts/text_sanitizer_and_chunker.py) for chunking.
2. **Frontmatter, Links & Orphans**: Require `title`, `date: YYYY-MM-DD`, and `tags` (plus `type`, `status`, `repo`, `github`, `stack` in `Projetos/Ativos/`). Prove zero `![[...]]` / `![](...)` links before proposing dry-run quarantine to `Arquivo/_anexos_orfaos/`. Apply temporal invalidation (`< 25 KB` split) per [`references/memory_governance_protocol_2026.md`](references/memory_governance_protocol_2026.md).
3. **Reindex & MemPalace Sync**: Rebuild index via [`scripts/vault_palace_search.py`](scripts/vault_palace_search.py) (`--rebuild-index`) and hydrate SQLite via [`scripts/vault_kg_hydrator.py`](scripts/vault_kg_hydrator.py). Call MCP `mempalace_sync` / `mempalace_mine` (`wing="notes"`) instead of a concurrent CLI subprocess.

## 4. Gotchas & Edge Cases

- **Protected Config**: Never touch `.obsidian/` or `.trash/`.
- **Zero Content Loss**: Never delete or truncate authorial notes; archive to `Arquivo/` only with HITL approval, never store PII/PHI or secrets, and update `[[Wikilinks]]` whenever renaming notes.
- **SQLite Lock Contention**: Export `PYTHONUTF8=1` and avoid CLI `mempalace mine` while `mempalace-mcp` holds SQLite locks.

## 5. Output Schema & Validation Criteria

1. Room health summary (`Inbox`, `Projetos`, `Memória`, `Medicina`, `Arquivo`) with `[PASS]` / `[FAIL]` / `[UNVERIFIED]` verdicts per [`rules/audit_criteria.md`](rules/audit_criteria.md).
2. Broken `[[Wikilinks]]`, missing YAML notes, orphan candidates, parity status, and MemPalace sync confirmation.

## 6. User Communication Rule

Internal scripts, schemas, and audit rules execute in Technical English. **All user-facing dialogue, audit tables, quarantine proposals, and questions MUST be written in Portuguese — Brazil (`pt-BR`)**, unless the user explicitly requests otherwise.
