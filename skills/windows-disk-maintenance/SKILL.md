---
name: windows-disk-maintenance
description: "Maintain local Windows 11 files across Downloads, Desktop, and C:\\Users\\melki\\dev\\ by triaging old installers and temporary clutter with PowerShell -WhatIf dry-runs. Use for local disk hygiene; do NOT use for Google Drive (G:\\Meu Drive), Obsidian vault curation (obsidian-vault-curator), or protected Windows OS directories."
compatibility: "Windows 11, pwsh 7+, Python 3.12+"
metadata:
  author: "Franklin"
  version: "1.2.0"
  updated_at: "2026-11-16"
  category: "Local OS & Disk Maintenance"
  tags: ["windows", "windows-11", "powershell", "pwsh", "downloads", "desktop", "disco", "manutencao", "locais", "instaladores", "temporarios", "residuos", "dev-workspace", "whatif"]
---

# Windows 11 Local Disk Maintenance (`windows-disk-maintenance`)

## 1. Overview & Scope

Triage loose files in `C:\Users\melki\Downloads` and `Desktop` using [`references/local_retention_policy.json`](references/local_retention_policy.json), and audit `C:\Users\melki\dev\` hygiene (routing scratch code to `sandbox/`, checking stale caches, and verifying `repos/` <-> `notes/Projetos/Ativos/` parity).

- **When NOT to Use**: Google Drive (`G:\Meu Drive`) cleanup or taxonomy (`gdrive-cleanup-auditor`, `gdrive-taxonomy-organizer`), Obsidian vault curation (`obsidian-vault-curator`), or OS system paths (`C:\Windows`, `C:\Program Files`).

## 2. Inputs & Prerequisites

- `target_area` (optional): `downloads` (default), `desktop`, `dev`, or `all`.
- `days_threshold` (optional): Minimum age in days for stale installers/clutter (default `30`, per [`references/local_retention_policy.json`](references/local_retention_policy.json)).
- `clean_heavy_caches` (optional, boolean): Default `false` (requires explicit HITL approval).
- **Prerequisites**: Windows 11 with PowerShell 7 (`pwsh`).

## 3. Step-by-Step Procedure

1. **Enforce `dev\` Topology**: Preserve `repos\`, `sandbox\node\`, `sandbox\python\`, `tools\`, `notes\`, and `references\`. Never run `npm install` or `pip install` loose in `C:\Users\melki\` or `C:\Users\melki\dev\`.
2. **Non-Destructive Diagnostics (`-LiteralPath`)**: Group `Downloads` and `Desktop` files by extension via `Get-ChildItem -LiteralPath ... -File | Group-Object Extension` and compute total MB.
3. **Dry-Run (`-WhatIf`), Lock Checks & Shielding**: Check open process locks on `.exe`/`.msi` binaries, skip protected Desktop launchers listed in [`references/local_retention_policy.json`](references/local_retention_policy.json) (e.g., `Cockpit-Melki.html`, `FrontCraft-Studio.cmd`), and display a `Source -> Destination` table.
4. **Safe Relocation**: Route stale installers (`.exe`, `.msi`, `.iso`, `.msix`) to `C:\Users\melki\Downloads\_Instaladores` (and documents/media to policy buckets) using `Move-Item -LiteralPath ... -WhatIf` before HITL execution.

## 4. Gotchas & Edge Cases

- **Zero Unapproved Deletion**: Never run `Remove-Item -Recurse -Force` without explicit HITL confirmation.
- **Git Repo Safety**: Never delete `dev\repos\` folders without clean `git status`, current `git push`, and migrating the note to `notes\Projetos\Fora da Máquina\` (`status: fora-da-maquina`).
- **Special Paths & Locks**: Always pass `-LiteralPath` (never `-Path`) and catch open-file lock errors cleanly.

## 5. Output Schema & Validation Criteria

1. Disk occupancy breakdown, relocation table, `dev\repos\` <-> `notes\Projetos\Ativos\` parity, and `file:///` links.
2. `[PASS]` / `[FAIL]` / `[UNVERIFIED]` verdict per [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

All internal retention rules, PowerShell commands, and audit verdicts run in Technical English. **All user-facing dialogue, triage tables, HITL prompts, and summaries MUST be written in Portuguese — Brazil (`pt-BR`)**, unless the user explicitly requests otherwise.
