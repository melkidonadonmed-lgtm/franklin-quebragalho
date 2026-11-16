# Deterministic Audit Criteria — `windows-disk-maintenance` (`v1.2.0`)

Falsifiable boolean rules (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) under Module **M4 (Local Windows 11 / PowerShell Operations)**:

---

- **`[PASS]` Criterion 01 (Launcher & Cockpit Preservation):** Essential Desktop launchers (`Cockpit-Melki.html`, `FrontCraft-Studio.html`, `FrontCraft-Studio.cmd`, `Antigravity-Painel-Controle.cmd`, active `.lnk` shortcuts) remain untouched.
- **`[FAIL: LAUNCHER_AFFECTED]` Criterion 01:** Attempting to move, rename, or delete protected Desktop launcher files.
- **`[UNVERIFIED]` Criterion 01:** `Desktop` or `Downloads` directory is inaccessible in the current session.

- **`[PASS]` Criterion 02 (Mandatory `-WhatIf` Dry-Run & `-LiteralPath`):** Batch moves in `Downloads` or `Desktop` display a `-WhatIf` preview table and pass `-LiteralPath` to safely handle brackets `[]` and spaces.
- **`[FAIL: MUTATION_WITHOUT_DRYRUN]` Criterion 02:** Running bulk transfers without prior dry-run simulation or passing unsafe `-Path` globs on special-character paths.

- **`[PASS]` Criterion 03 (Non-Destructive `C:\Users\melki\dev\` Hygiene):** Scratch experiments move to `dev\sandbox\`, and no repository in `dev\repos\` is deleted (`Remove-Item -Recurse -Force`) without HITL approval, clean `git status`, and vault migration to `notes\Projetos\Fora da Máquina\`.
- **`[FAIL: DESTRUCTIVE_DELETION]` Criterion 03:** Executing permanent deletion without explicit human approval.

- **`[PASS]` Criterion 04 (Defensive Process Lock Verification):** Checks whether `.exe`/`.msi` binaries or target folders are locked by active processes before relocation.
- **`[FAIL: IGNORED_FILE_LOCK]` Criterion 04:** Unhandled failure triggered by attempting to move an open, process-locked file.
