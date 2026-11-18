---
name: technical-markdown-writer
description: "Author executive reports, technical notes, ADRs, roadmaps, and installation guides in Markdown (GFM) using GitHub alert callouts, the Blank-Line Law, and Google Style Guides. Use for structured technical writing; do NOT use for PDF rendering/export (html-pdf-converter), bulk Obsidian vault curation (obsidian-vault-curator), or Mermaid directory tree mapping (flow-filetree-organizer)."
compatibility: "Antigravity 2.0, CommonMark/GFM, Obsidian"
allowed-tools: read_file write_file edit_file run_command
metadata:
  author: "Franklin"
  version: "1.3.0"
  updated_at: "2026-11-16"
  category: "Technical Documentation & Structured Authoring"
  tags: "markdown, gfm, relatorio, relatorios, ata, atas, notas, tecnicas, adr, documentacao, alerta, google-styleguides, blank-line-law"
---

# Structured Technical Markdown Authoring (`technical-markdown-writer`)

## 1. Overview & Scope

Author executive reports, technical notes, ADRs, roadmaps, and installation guides in GitHub-Flavored Markdown (GFM) aligned with Google Style Guides, using lowercase YAML frontmatter, GitHub alerts, and typed code fences prior to optional PDF export.

- **When NOT to Use**: PDF rendering/export (`html-pdf-converter`), bulk Obsidian vault curation (`obsidian-vault-curator`), Mermaid app flowcharts or directory trees (`flow-filetree-organizer`), or auditing skill contracts (`agent-server-auditor`).

## 2. Inputs & Prerequisites

- `topic_or_draft` (required): Subject, raw notes, ADR context, or code artifact to document.
- `document_type` (optional): `technical_note` (default), `executive_report`, `adr_decision`, `roadmap`, `installation_guide`.
- `output_path` (optional): Destination `.md` path (e.g., `C:\Users\melki\dev\notes\Inbox\` or repository `docs\`).

## 3. Step-by-Step Procedure

1. **Frontmatter & Layout**: Follow [`references/markdown_style_guide.md`](references/markdown_style_guide.md). Start Obsidian/archive files with lowercase YAML (`title`, `date: YYYY-MM-DD`, `author`, `tags`, `status`) and clear sections (Summary, Context, Technical Spec, Next Steps).
2. **GFM & Blank-Line Law Shielding**:
   - **Blank-Line Law**: Keep one blank line before and after headings, lists, tables, blockquotes, alerts, and code fences.
   - **Canonical Alerts**: Use `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, or `> [!CAUTION]` without nesting or raw HTML `<div class="alert">`.
   - **Escaping & Typed Fences**: Escape table pipes (`\|`) and literal `$` (`\$`), wrap nested triple backticks in quadruple backticks, and declare fence languages (`python`, `go`, `typescript`, `json`, `powershell`, `mermaid`, `yaml`).
3. **ReAct Persistence & RAW Verification**: Write UTF-8 Markdown via `write_file`, use `file:///` forward-slash links, and re-read the saved file (`Read-After-Write`) to confirm valid YAML frontmatter, Blank-Line Law spacing, and `[PASS]` against [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 4. Gotchas & Edge Cases

- **Zero Fabrication**: Label unproven metrics or unconfirmed decisions `[UNVERIFIED]`; never invent data.
- **Parser & Zero-Trust XSS Guardrail**: Quote Mermaid labels with parentheses/brackets (`id["Label (Info)"]`); never embed raw `<script>` tags or real secrets.
- **No Binary Coupling**: Do not run headless PDF rendering here; hand off `.md` files to `html-pdf-converter`.

## 5. Output Schema & Validation Criteria

1. UTF-8 `.md` file saved on disk and validated `[PASS]` / `[FAIL]` / `[UNVERIFIED]` against [`rules/audit_criteria.md`](rules/audit_criteria.md).
2. Concise section summary with a clickable `file:///` link to the saved document.

## 6. User Communication Rule

All internal style guides, escaping rules, and validation criteria run in Technical English. **All user-facing dialogue, summaries, and authored end-user documents (unless English is explicitly requested) MUST be written in Portuguese — Brazil (`pt-BR`)**.
