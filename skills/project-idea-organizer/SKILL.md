---
name: project-idea-organizer
description: "Structure raw ideas into secure v1.0.0 MVPs via guided discovery or reorganize existing repositories by syncing Triad governance docs, disk-accurate README.md, and MCP/FastAPI/RPC contracts with dry-run root hygiene. Use when bootstrapping an idea or aligning repo structure. Do NOT use for OS disk cleanup, 0-100 AST scoring, or standalone Mermaid diagrams."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
metadata:
  author: "Franklin"
  version: "1.2.0"
  updated_at: "2026-11-16"
  category: "Project Architecture & Repository Hygiene"
  tags: ["project-idea-organizer", "ideia", "ideias", "mvp", "sincronizar", "organizar", "organizador", "readme", "contratos", "mcp", "fastapi", "rpc", "dry-run"]
---

# `project-idea-organizer` (`v1.2.0`) — Idea-to-MVP & Repo Sync

## 1. Overview & Scope

Product and repository architect with two complementary modes:
1. **Mode 1 (`ideation_to_v1`):** Converts a raw concept into a **secure `v1.0.0` MVP** via `1–3` guided questions (with *"I don't know"* fallback), benchmarking, modular tree, and working starter code.
2. **Mode 2 (`project_organizer_sync`):** Maps current repo state, designs an **Ideal Structure**, aligns Triad v2.0 docs (`AGENTS.md`, `.context/context.md`, `.context/spec.md`, `DESIGN.md`, `README.md` 1:1 with disk), and organizes `MCP` / `FastAPI` / `JSON-RPC 2.0` contracts.

### When NOT to Use
- **0–100 AST/Live-DOM MVP Audits:** Use `system-project-auditor`.
- **Visual Flowcharts & Trees Only:** Use `flow-filetree-organizer`.
- **OS Disk / Drive Cleanup:** Use `windows-disk-maintenance` or `gdrive-cleanup-auditor`.

## 2. Inputs & Prerequisites

- **Mode 1 (`ideation_to_v1`):** Empty directory or idea draft, target objective, and `1–3` round replies.
- **Mode 2 (`project_organizer_sync`):** `project_root`, manifests (`pyproject.toml`, `package.json`, `go.mod`), source tree, and `git remote -v`.

## 3. Step-by-Step Procedure

Consult [`mcp_fastapi_rpc_contracts_guide.md`](references/mcp_fastapi_rpc_contracts_guide.md) and [`organizer_output_template.md`](references/organizer_output_template.md):

- **Mode 1 (`ideation_to_v1`):** Ask `1–3` triage questions (on *"I don't know"*, propose a minimal typed MVP + safe defaults), benchmark the stack, explain folders, and bootstrap Triad v2.0 + `.gitignore` + `.env.example` + starter code under HITL.
- **Mode 2 (`project_organizer_sync`):** Inspect actual tree/manifests, clarify up to 3 `[GAP]`s if intent is ambiguous, propose Ideal Structure without breaking imports, pre-fill `Pydantic v2 extra="forbid"` / `Zod .strict()` / Go structs, draw Mermaid `flowchart TD`, sync `README.md` 1:1 with disk and contracts (checking `google-developer-knowledge`/`gemini_get_doc` and `agent-server-auditor` rules), and run **Dry-Run** root cleanup.

## 4. Gotchas & Edge Cases

- **Zero Hollow MVPs or Secret Leaks:** Ban empty `TODO`/placebo stubs; never expose `.env` secrets in docs; ensure `.gitignore` ignores `.env`.
- **Mandatory Dry-Run:** Never move/delete root files without user confirmation.

## 5. Output Schema & Validation Criteria

Deliver the 4 sections in [`organizer_output_template.md`](references/organizer_output_template.md) (Metadata & MVP Analysis, Mermaid Diagram, Current vs. Ideal Tree, HITL Next Step), validated with `[PASS]`/`[FAIL]`/`[UNVERIFIED]` against [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

All internal governance docs (`AGENTS.md`, `.context/spec.md`, `.context/context.md`), code schemas, and contracts MUST stay in Technical English; however, **all user-facing questions, *"I don't know"* MVP proposals, dry-run root previews, and Self-Refine summaries MUST be communicated in Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.
