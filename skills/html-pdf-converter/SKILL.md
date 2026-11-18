---
name: html-pdf-converter
description: "Convert Markdown and HTML reports into A4 PDF files via headless Microsoft Edge or Chrome with print CSS. Use when exporting existing documents to PDF; do NOT use for authoring content from scratch (technical-markdown-writer) or bulk Obsidian vault curation (obsidian-vault-curator)."
compatibility: "Windows 11, pwsh 7+, Microsoft Edge or Google Chrome Headless"
allowed-tools: read_file write_file edit_file run_command
metadata:
  author: "Franklin"
  version: "1.2.0"
  updated_at: "2026-11-16"
  category: "Document Publishing & PDF Conversion"
  tags: "pdf, html, md-to-pdf, converter, conversao, export, edge, chrome, headless, imprimir, impressao, print-css, a4"
---

# Markdown/HTML to PDF Conversion Pipeline (`html-pdf-converter`)

## 1. Overview & Scope

Convert existing Markdown (`.md`) or HTML (`.html`) documents into print-ready A4 PDFs using local headless Microsoft Edge (`msedge.exe`) or Chrome (`chrome.exe`), styled with [`references/print_theme.css`](references/print_theme.css) and orchestrated via [`scripts/md-to-pdf.ps1`](scripts/md-to-pdf.ps1). Typically runs as the final export step after `technical-markdown-writer` or `flow-filetree-organizer`.

- **When NOT to Use**: Authoring new content or drafting technical notes from scratch (`technical-markdown-writer`), bulk Obsidian vault curation (`obsidian-vault-curator`), or notes meant to remain Markdown-only in the vault.

## 2. Inputs & Prerequisites

- `input_file_path` (required): Absolute path to the existing `.md` or `.html` input file.
- `output_pdf_path` (optional): Target `.pdf` output path (defaults to same directory and base filename).
- `page_orientation` (optional): `portrait` (default) or `landscape` (recommended for tables wider than 8 columns).
- **Prerequisites**: Local `msedge.exe` or `chrome.exe` installed on Windows 11 with PowerShell 7 (`pwsh`).

## 3. Step-by-Step Procedure

1. **Validate Input Path**: Confirm existence via `Test-Path -LiteralPath $inputFilePath`.
2. **HTML Wrapper & Print CSS Shielding**: For `.md` sources, invoke [`scripts/md-to-pdf.ps1`](scripts/md-to-pdf.ps1) (`pwsh -File skills/html-pdf-converter/scripts/md-to-pdf.ps1 -InputFile "<input.md>" -OutputFile "<output.pdf>"`) or apply [`references/print_theme.css`](references/print_theme.css) (`@page { size: A4; margin: 18mm 20mm 20mm 20mm; }`, `break-inside: avoid` on `table`, `pre`, `blockquote`, and `break-after: avoid` on `h1..h6`).
3. **Local Headless Rendering**: Invoke `msedge.exe` (or `chrome.exe`) with `--headless --disable-gpu --run-all-compositor-stages-before-draw --no-pdf-header-footer --print-to-pdf="$outputPdfPath" "$tempHtmlUri"`.
4. **Physical Verification (`Read-After-Write`)**: Verify `(Get-Item -LiteralPath $outputPdfPath).Length -gt 0`, remove temporary `.tmp.html` files (unless `-KeepHtml` is set), and keep the original input file intact.

## 4. Gotchas & Edge Cases

- **Local-First Privacy Guardrail:** Never upload untrusted local documents to external cloud PDF APIs, and never require Pandoc or `wkhtmltopdf` when local Edge/Chrome headless is available.
- **Source File Protection**: Never delete or overwrite the source `.md` or `.html` file.
- **Spaces & Brackets in Paths**: Always use `-LiteralPath` in PowerShell and convert local paths into `file:///` URIs with forward slashes before passing to Chromium.

## 5. Output Schema & Validation Criteria

1. Deterministic `[PASS]` / `[FAIL]` / `[UNVERIFIED]` verdict per [`rules/audit_criteria.md`](rules/audit_criteria.md).
2. Final PDF file size in KB, applied page orientation (`portrait` | `landscape`), and clickable `file:///` links to both the generated PDF and preserved source file.

## 6. User Communication Rule

All internal print CSS rules, PowerShell invocations, and browser flags execute in Technical English. **All user-facing dialogue, export status reports, and clickable file links MUST be written in Portuguese — Brazil (`pt-BR`)**, unless the user explicitly requests otherwise.
