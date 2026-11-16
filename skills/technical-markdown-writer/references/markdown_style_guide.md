# Canonical Markdown Style Guide (Obsidian & Antigravity)

Formatting and syntax guidelines for structured technical authoring:

1. **Canonical YAML Frontmatter:**
   - Always use lowercase field keys (`title`, `date`, `tags`, `author`, `status`).
   - Format all dates strictly in ISO `YYYY-MM-DD`.

2. **Blank-Line Law:**
   - Always place an empty line before and after headings, bullet/numbered lists, Markdown tables, blockquotes/GitHub alerts, and code fences.
   - Never nest GitHub alert blocks (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) or place them back-to-back without separating prose or spacing.

3. **Fenced Code Blocks:**
   - Always declare a language identifier on opening fences (`powershell`, `python`, `go`, `typescript`, `json`, `yaml`, `mermaid`, `text`).
   - Use four backticks (```` ```` ````) whenever wrapping Markdown examples that contain triple-backtick code fences.

4. **Links & References:**
   - For local OS file paths, always use the `file:///` scheme with forward slashes (`/`).
   - For internal Obsidian note links, use descriptive Wikilink labels (`[[NoteName|Display Text]]`).

5. **Heading Hierarchy:**
   - Reserve Heading 1 (`#`) exclusively for the document title.
   - Use Heading 2 (`##`) for primary sections and Heading 3 (`###`) for subsections.
