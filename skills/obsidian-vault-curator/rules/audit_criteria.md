# Deterministic Audit Criteria — `obsidian-vault-curator` (`v1.4.0`)

Falsifiable boolean rules (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for Obsidian Vault (`C:\Users\melki\dev\notes`) and MemPalace curation:

---

- **`[PASS]` Criterion 01 (Full Preservation of Non-Empty Notes):** No note containing authorial content is deleted or truncated; archiving relocates notes into `Arquivo\` only after dry-run simulation and HITL approval.
- **`[FAIL: VAULT_CONTENT_LOSS]` Criterion 01:** Deletion or truncation of any note containing prose, decisions, or legitimate links.
- **`[UNVERIFIED]` Criterion 01:** Vault path `C:\Users\melki\dev\notes` is inaccessible on disk.

- **`[PASS]` Criterion 02 (Strict `.obsidian/` & `.trash/` Isolation):** `.obsidian/` and `.trash/` are categorically excluded from destructive scans and automated edits.
- **`[FAIL: OBSIDIAN_CONFIG_CORRUPTION]` Criterion 02:** Unrequested modification or deletion of internal configuration files inside `.obsidian/`.

- **`[PASS]` Criterion 03 (Falsifiable Orphan Attachment Proof via `vault_hygiene_scanner.py`):** Deterministic verification proves zero `![[...]]` or `![](...)` references across the entire vault before proposing relocation to `Arquivo\_anexos_orfaos`.
- **`[FAIL: FALSE_ORPHAN_CLASSIFICATION]` Criterion 03:** Flagging a referenced attachment as orphaned without scanning all notes and canvas files.

- **`[PASS]` Criterion 04 (YAML Frontmatter, Repo Parity & Lock-Safe MemPalace Sync):** Valid YAML (`title`, `date` ISO, `tags`), parity via `dev\tools\check-vault-projects.ps1`, and final sync via MCP `mempalace_sync` / `mempalace_mine` (`wing="notes"`).
- **`[FAIL: INVALID_YAML_OR_DESYNC]` Criterion 04:** Malformed YAML frontmatter injection or missing MemPalace synchronization after curation.

- **`[PASS]` Criterion 05 (Zero `general` Room Leakage & SOTA Isolation):** `mempalace audit --json` reports `generic_drawers: 0` (`rooms: 100`), all `contraindicacao-total` notes live under `Arquivo/Contraindicados/`, and active top-5,000-char `H1`–`H3` headings obey `5..60` chars.
- **`[FAIL: ROOM_LEAK_OR_SOTA_CONTAMINATION]` Criterion 05:** Excluded assets (`Excalidraw/`, plugins, root docs) present in `room="general"` or `contraindicacao-total` notes surfacing inside `mempalace_search(room="projetos")`.
