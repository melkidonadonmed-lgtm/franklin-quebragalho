---
name: flow-filetree-organizer
description: "Transform raw app ideas into valid Mermaid flowcharts and commented ASCII directory trees with MVP scope isolation and .md/.pdf export. Use when mapping visual workflows or folder trees. Do NOT use for AST audits (code-acceptability-auditor), repo scaffolding (project-idea-organizer), or standalone PDF export (html-pdf-converter)."
compatibility: "Antigravity 2.0, Markdown GFM, Mermaid, Edge Headless"
allowed-tools: read_file run_command
metadata:
  author: "Franklin"
  version: "1.2.0"
  updated_at: "2026-11-16"
  category: "Visual Planning & Directory Tree Diagramming"
  tags: "flow-filetree-organizer, fluxo, fluxos, arvore, mermaid, diagramas, diretorios, ideias, flowchart, filetree, markdown"
---

# `flow-filetree-organizer` (`v1.2.0`) — Mermaid Flowcharts & File Trees

## 1. Overview & Scope

Converts raw app drafts, feature specs, and operational workflows into syntactically safe **Mermaid flowcharts** (`flowchart TD`/`LR`) and **commented ASCII directory trees**, preserving semantic version history and offering direct `.md` or `.pdf` export.

### When NOT to Use
- **Static AST Security Audits:** Use `code-acceptability-auditor` or `system-project-auditor`.
- **Full Repo Restructuring, Code Scaffolding, or MCP Sync:** Use `project-idea-organizer`.
- **Standalone Markdown/HTML to PDF Rendering:** Delegate standalone `.pdf` conversion to `html-pdf-converter`.

## 2. Inputs & Prerequisites

- **`idea_text` (required):** Raw user request, app idea, or workflow specification.
- **`previous_output` (optional):** Prior version used to compute semantic changelog deltas.
- **`export_format` (optional):** `chat` (default), `md`, or `pdf`.

## 3. Step-by-Step Procedure

Follow the formatting rules and output template in [`references/mermaid_and_filetree_patterns.md`](references/mermaid_and_filetree_patterns.md):

1. **Phase 0 — Literal Capture & Ambiguity Gate:** Copy the exact user text into `Original request:` verbatim (never paraphrase or summarize it). If essential parameters are absent, tag `[GAP]` and ask at most 1–2 concise HITL questions without inventing scope.
2. **Phase & MVP Scoping (`CoT + ToT`):** Order stages sequentially (`Input -> Processing -> Output`), keep only core MVP modules inside the main flow, and prune extras under `Optional Suggestions`.
3. **Mermaid & Commented ASCII Tree:** Use double-quoted node labels whenever text contains `()`, `[]`, `/`, or `:`; attach `# <purpose>` comments to every folder and file node.
4. **ReAct Export & RAW Verification (`.md` / `.pdf`):** Write `.md` via `write_file` (or delegate `.pdf` to `html-pdf-converter`) and perform a `Read-After-Write` check confirming file existence and non-zero byte length.

## 4. Gotchas & Edge Cases

- **No Paraphrased Prompts or Scope Bloat:** Never rewrite `Original request:` or inflate the core MVP with unrequested services.
- **Mermaid Parser Safety:** Never embed raw HTML tags (`<br>`, `<b>`, `<div>`) or unquoted parentheses inside node labels.
- **No Secrets & HITL Overwrite Guard:** Reference `.env.example` only in trees and ask human confirmation before overwriting existing `.md`/`.pdf` files.

## 5. Output Schema & Validation Criteria

Deliver the canonical template in [`references/mermaid_and_filetree_patterns.md`](references/mermaid_and_filetree_patterns.md) (Metadata Header, Verbatim `Original request`, Organization Flow, plus Sections `1..6`: Changelog, Mermaid Diagram, Commented ASCII Tree, Execution Flow, Optional Suggestions, and Export Option), audited against [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

All internal Mermaid syntax standards, tree conventions, and audit rules MUST remain in Technical English; however, **all user-facing workflow descriptions, tree comments tailored to the user's request, clarification questions, and `.md`/`.pdf` export prompts MUST be communicated in Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.
