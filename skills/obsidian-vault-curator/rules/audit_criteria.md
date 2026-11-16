# Deterministic Audit Criteria — `obsidian-vault-curator` (`v1.3.0`)

Falsifiable boolean rules (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) under Module **M5 (Obsidian Vault `C:\Users\melki\dev\notes` & MemPalace)**:

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
