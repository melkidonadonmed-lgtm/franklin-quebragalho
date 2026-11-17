# Deterministic Audit Criteria — `gdrive-taxonomy-organizer` (`v1.2.0`)

Falsifiable boolean rules (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for Google Drive (`G:\Meu Drive`) taxonomy and ISO date naming:

---

- **`[PASS]` Criterion 01 (Adherence to Real Numbered Taxonomy):** Files are routed strictly into existing numbered buckets under `G:\Meu Drive\` (`[01]Projetos`, `01_Modelos_Rapidos`, `02_Protocolos_e_Medicamentos`, `03_Medicina_Faculdade`, `04_Workspace_e_Banco_de_Dados`, `05_Banco_dados_apoio_backup`, `07_Gemini_Gems`, `09_ui_web_kits`, `10_Pessoal`, `11_Salvo_do_Chrome`, `12_MCP_Servers`, `16_Documentos_comp_SUS`, `99_Arquivo_Historico`, `Franklin_Skills_Docs_2026`).
- **`[FAIL: INVENTED_PARALLEL_FOLDER]` Criterion 01:** Creating redundant parallel root folders in `G:\Meu Drive\` instead of using the existing canonical tree.
- **`[UNVERIFIED]` Criterion 01:** Drive `G:\Meu Drive\` is unmounted or inaccessible.

- **`[PASS]` Criterion 02 (ISO `YYYY-MM-DD` Date Standardization):** Renamed files strictly adopt `YYYY-MM-DD` dates with clean underscores/separators.
- **`[FAIL: AMBIGUOUS_DATE_FORMAT]` Criterion 02:** Using ambiguous regional date formats (`DD-MM-YY`, `MM/DD/YYYY`).

- **`[PASS]` Criterion 03 (Character Sanitization, `-LiteralPath` & Dry-Run):** Sanitized filenames exclude illegal characters, PowerShell uses `-LiteralPath` (handling `[01]Projetos` brackets safely), and batch moves/renames preview with `-WhatIf` first.
- **`[FAIL: UNESCAPED_PATH_OR_NO_DRYRUN]` Criterion 03:** Passing unescaped `-Path` to bracketed directories or running batch moves/renames without a dry-run preview.

- **`[PASS]` Criterion 04 (Extension Preservation & `15_chaves_api` Secrecy):** Original file extensions remain intact during renaming, and `15_chaves_api` is never read, exposed, or copied into repositories.
- **`[FAIL: EXTENSION_CORRUPTED_OR_SECRET_EXPOSED]` Criterion 04:** Altering/stripping a file extension or accessing/leaking credentials inside `15_chaves_api`.
