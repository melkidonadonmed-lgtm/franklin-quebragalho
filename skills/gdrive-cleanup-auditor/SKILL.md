---
name: gdrive-cleanup-auditor
description: "Audit and clean up Google Drive (G:\\Meu Drive) by detecting heavy files >100MB, SHA-256 hash duplicates, residual archives, and orphan empty folders with non-destructive _Quarentena_Descarte dry-run. Use for Drive cleanup; do NOT use for numbered folder taxonomy or ISO dates (gdrive-taxonomy-organizer) or local Windows disk maintenance."
compatibility: "Windows 11, pwsh 7+, Google Drive for Desktop or workspace-mcp"
metadata:
  author: "Franklin"
  version: "1.2.0"
  updated_at: "2026-11-16"
  category: "Cloud Storage & Deduplication Auditing"
  tags: ["google-drive", "gdrive", "drive", "limpeza", "higienizar", "duplicatas", "duplicados", "hash", "sha256", "100mb", "orfas", "vazias", "quarentena", "dry-run"]
---

# Google Drive Storage Audit & Non-Destructive Quarantine (`gdrive-cleanup-auditor`)

## 1. Overview & Scope

Detect oversized files (`> 100 MB`), stale archives/installers defined in [`references/residual_extensions.json`](references/residual_extensions.json), empty orphan folders, and `SHA-256` confirmed duplicate files across `G:\Meu Drive`. Build a reversible dry-run quarantine plan (`_Quarentena_Descarte\YYYY-MM-DD\`) prior to taxonomic reorganization.

- **When NOT to Use**: Classifying files into numbered `01_*`..`99_*` buckets or applying `YYYY-MM-DD` naming conventions (`gdrive-taxonomy-organizer`), or cleaning local Windows `Downloads`, `Desktop`, and `C:\Users\melki\dev\` (`windows-disk-maintenance`).

## 2. Inputs & Prerequisites

- `target_drive_path` (optional): Default `G:\Meu Drive`.
- `size_threshold_mb` (optional): Default `100`.
- `quarantine_folder_name` (optional): Default `_Quarentena_Descarte`.
- **Prerequisites**: Mounted `G:\Meu Drive` via Google Drive for Desktop (or read-only fallback via `workspace-mcp` / `gdrive` skill).

## 3. Step-by-Step Procedure

1. **Non-Destructive Scan (`-LiteralPath`)**: Traverse `G:\Meu Drive` skipping `15_chaves_api`, rank largest items (`Length / 1MB`), flag extensions from [`references/residual_extensions.json`](references/residual_extensions.json), and list empty orphan directories.
2. **Two-Phase Duplicate Verification**:
   - **Phase 1**: Group candidate files sharing exact byte `Length`.
   - **Phase 2**: Confirm binary identity using `Get-FileHash -LiteralPath $file -Algorithm SHA256` (never classify duplicates by filename similarity alone).
3. **Dry-Run Impact Plan (`-WhatIf`) & HITL Gate**: Display a preview table of duplicate pairs, hashes, and reclaimable MB; await explicit human approval before moving items.
4. **Dated Quarantine Execution (`-LiteralPath`)**: Move approved items with `Move-Item -LiteralPath $dupItem -Destination "G:\Meu Drive\_Quarentena_Descarte\$(Get-Date -Format 'yyyy-MM-dd')"` (simulated via `-WhatIf` first).
5. **ReAct Post-Move Verification (`Read-After-Write`)**: Verify `Test-Path -LiteralPath $destPath` and matching byte `Length` inside `_Quarentena_Descarte\YYYY-MM-DD\` before reporting completion.

## 4. Gotchas & Edge Cases

- **Zero Permanent Deletion**: Never execute `Remove-Item` on `G:\`; all discards move reversibly into `_Quarentena_Descarte\YYYY-MM-DD\`.
- **Secrets & Sync Metadata Protection**: Never read, move, or expose `15_chaves_api`, and never touch Google Drive sync/stub files (`desktop.ini`, `.tmp.drivedownload`, `.gdoc`, `.gsheet`).
- **Unmounted Drive Fallback**: If `G:\Meu Drive` is unmounted, emit `[FAIL: GDRIVE_UNMOUNTED]` / `[UNVERIFIED]` and guide mounting or read-only inspection via `workspace-mcp` (`drive_list_files`).

## 5. Output Schema & Validation Criteria

1. Storage usage summary, oversized items table (`> 100 MB`), and `SHA-256` duplicate matrix.
2. Dry-run quarantine plan and `[PASS]` / `[FAIL]` / `[UNVERIFIED]` verdict per [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

All internal PowerShell diagnostics, hash checks, and audit criteria operate in Technical English. **All user-facing dialogue, impact tables, HITL approval prompts, and cleanup summaries MUST be written in Portuguese — Brazil (`pt-BR`)**, unless the user explicitly requests otherwise.
