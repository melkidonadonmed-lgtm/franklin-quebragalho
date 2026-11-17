# Deterministic Audit Criteria — `html-pdf-converter` (`v1.2.0`)

Falsifiable boolean rules (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for executive Markdown/HTML to PDF conversion:

---

- **`[PASS]` Criterion 01 (Physical Existence & Non-Zero Byte Size):** The generated `.pdf` exists on disk (`Test-Path -LiteralPath`) and has verified `Length > 0` bytes after rendering.
- **`[FAIL: EMPTY_OR_MISSING_PDF]` Criterion 01:** Output PDF file is missing or corrupted with `0` bytes.
- **`[UNVERIFIED]` Criterion 01:** Local browser binary (`msedge.exe` / `chrome.exe`) is unavailable in the runtime environment.

- **`[PASS]` Criterion 02 (Print Page-Break Shielding):** Injected print CSS defines `@page { size: A4; }` plus `page-break-inside: avoid; break-inside: avoid;` on `table`, `pre`, and `blockquote`, and `break-after: avoid` on headings.
- **`[FAIL: TABLE_SPLIT_ACROSS_PDF_PAGES]` Criterion 02:** Print stylesheet lacks page-break shielding, allowing rows inside tables or code blocks to split mid-element.

- **`[PASS]` Criterion 03 (Local-First Headless Execution Without Cloud APIs):** Uses strictly local Windows binaries (`msedge.exe --headless --print-to-pdf` or `chrome.exe`) via `scripts/md-to-pdf.ps1` without transmitting documents to external APIs.
- **`[FAIL: EXTERNAL_API_DATA_LEAK]` Criterion 03:** Attempting to upload local document contents to an external web conversion service.

- **`[PASS]` Criterion 04 (Original Source Preservation):** The input `.md` or `.html` file remains unmodified after PDF generation, and both files are reported with clickable `file:///` links.
- **`[FAIL: SOURCE_FILE_DELETED_OR_OVERWRITTEN]` Criterion 04:** Deleting or destructively overwriting the input file after conversion.
