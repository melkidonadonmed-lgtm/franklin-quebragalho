---
name: gdrive-taxonomy-organizer
description: "Organize and classify Google Drive (G:\\Meu Drive) files into canonical numbered folders (01_*..99_*) and standardize filenames with ISO YYYY-MM-DD prefixes. Use for Drive folder taxonomy and naming; do NOT use for >100MB or SHA-256 duplicate cleanup (gdrive-cleanup-auditor), Obsidian vault curation, local Windows disk maintenance, or Mermaid file trees."
compatibility: "Windows 11, pwsh 7+, Google Drive for Desktop or workspace-mcp"
metadata:
  author: "Franklin"
  version: "1.2.0"
  updated_at: "2026-11-16"
  category: "Cloud Storage & Document Taxonomy"
  tags: ["google-drive", "gdrive", "drive", "taxonomia", "taxonomy", "organizacao", "organizar", "categorizar", "estruturar", "pastas", "numerada", "iso", "yyyy-mm-dd", "padronizacao"]
---

# Google Drive Numbered Taxonomy & ISO Dates (`gdrive-taxonomy-organizer`)

## 1. Overview & Scope

Classify loose files in `G:\Meu Drive\` into canonical numbered folders defined in [`references/default_drive_taxonomy.json`](references/default_drive_taxonomy.json) and standardize batch filenames to `YYYY-MM-DD_Descriptive_Subject.ext` while preserving extensions and removing illegal characters.

- **When NOT to Use**: `> 100 MB` bloat scans or `SHA-256` duplicate quarantine (`gdrive-cleanup-auditor`), Obsidian vault curation (`obsidian-vault-curator`), local Windows disk maintenance (`windows-disk-maintenance`), or Mermaid file trees (`flow-filetree-organizer`).

## 2. Inputs & Prerequisites

- `target_folder` (optional): Default `G:\Meu Drive\`.
- `apply_iso_dates` (optional, boolean): Default `false` (requires explicit HITL confirmation before batch renaming).
- **Prerequisites**: Mounted `G:\Meu Drive\` (or read-only `workspace-mcp` / `gdrive`). Always pass `-LiteralPath` in PowerShell for bracketed folders like `[01]Projetos`.

## 3. Step-by-Step Procedure

1. **Inventory**: List files via `Get-ChildItem -LiteralPath "G:\Meu Drive\" -File | Select-Object Name, Length, Extension, LastWriteTime`.
2. **Canonical Classification**: Route files strictly into the buckets of [`references/default_drive_taxonomy.json`](references/default_drive_taxonomy.json) (`[01]Projetos`, `01_Modelos_Rapidos`..`16_Documentos_comp_SUS`, `99_Arquivo_Historico`, `Franklin_Skills_Docs_2026`), stripping forbidden characters and double spaces without altering extensions.
3. **Dry-Run & HITL Gate**: Present a `Current Path -> Canonical Destination` preview table and require explicit approval.
4. **Safe Relocation**: Execute moves with `Move-Item -LiteralPath $sourceFile -Destination $targetBucket -WhatIf` before confirmed execution.

## 4. Gotchas & Edge Cases

- **Bracket Glob Trap**: Passing `-Path` to `[01]Projetos` treats `[01]` as a wildcard range and fails silently; always use `-LiteralPath`.
- **Protected Locations**: Never read, move, or expose `15_chaves_api`; never touch `G:\Outros computadores`; never invent parallel root folders; warn before moving shared links.
- **Extension & Date Guard**: Keep original extensions and forbid ambiguous dates (`DD-MM-YY`, `MM/DD/YYYY`).

## 5. Output Schema & Validation Criteria

1. `Source -> Canonical Destination` table and normalized `YYYY-MM-DD` rename summary.
2. `[PASS]` / `[FAIL]` / `[UNVERIFIED]` verdict per [`rules/audit_criteria.md`](rules/audit_criteria.md) and `file:///` links.

## 6. User Communication Rule

All internal taxonomy rules, PowerShell commands, and validation criteria run in Technical English. **All user-facing dialogue, classification tables, HITL confirmations, and reports MUST be written in Portuguese — Brazil (`pt-BR`)**, unless the user explicitly requests otherwise.
