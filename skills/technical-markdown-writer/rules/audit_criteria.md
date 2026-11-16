# Deterministic Audit Criteria — `technical-markdown-writer` (`v1.3.0`)

Falsifiable boolean rules (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) under Module **M5 (Technical Markdown Documentation & Layout Shielding)**:

---

- **`[PASS]` Criterion 01 (Blank-Line Law):** Mandatory blank lines appear before and after every heading, table, GitHub alert (`> [!NOTE]`), list, and fenced code block.
- **`[FAIL: MARKDOWN_BLOCK_COLLISION]` Criterion 01:** Structural elements placed directly adjacent without blank lines, breaking CommonMark/GFM rendering.
- **`[UNVERIFIED]` Criterion 01:** Target document was not written to disk or remains an unpersisted verbal draft.

- **`[PASS]` Criterion 02 (Valid YAML Frontmatter & Obsidian Compatibility):** Document opens with a valid `---` YAML block containing `title` (or `aliases`), ISO `date` (`YYYY-MM-DD`), and `tags` with zero YAML parse errors.
- **`[FAIL: INVALID_FRONTMATTER]` Criterion 02:** Missing frontmatter where required or malformed YAML metadata keys/values.

- **`[PASS]` Criterion 03 (Special Character Escaping & Safe Mermaid Syntax):** Literal pipes (`\|`) in table cells and angle brackets (`\<`, `\>`) are escaped, literal `$` is escaped (`\$` or inline code), and Mermaid nodes with special characters use double quotes.
- **`[FAIL: PARSER_BREAKAGE]` Criterion 03:** Unescaped `<`, `>`, `|`, or `$` corrupting Markdown tables, KaTeX math blocks, or Mermaid diagrams.

- **`[PASS]` Criterion 04 (Strict Separation — Authoring vs. PDF Export):** Scope remains strictly on `.md` authoring with clickable `file:///` links, delegating binary PDF export to `html-pdf-converter` when requested.
- **`[FAIL: BINARY_EXPORT_COUPLING]` Criterion 04:** Attempting binary PDF conversion outside the approved headless browser pipeline.
