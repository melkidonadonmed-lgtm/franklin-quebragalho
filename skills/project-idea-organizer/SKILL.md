---
name: project-idea-organizer
description: "Bootstrap raw ideas into right-sized runnable v1.0.0 MVPs or sync repositories across Triad v2.1 docs, 1:1 disk-accurate README.md, active MCP/FastAPI/RPC contracts, and dry-run root hygiene. Use when starting an idea or aligning repo structure. Do NOT use for 0-100 AST audits (system-project-auditor), single-module coding (solution-content-architect), or Mermaid trees (flow-filetree-organizer)."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
metadata:
  author: "Franklin"
  version: "1.3.0"
  updated_at: "2026-11-17"
  category: "Project Architecture & Repository Hygiene"
  tags: ["project-idea-organizer", "ideia", "ideias", "mvp", "sincronizar", "organizar", "organizador", "estruturar", "do-zero", "bootstrap", "scaffold", "readme", "contratos", "mcp", "fastapi", "rpc", "dry-run"]
---

# `project-idea-organizer` (`v1.3.0`) — Right-Sized Idea-to-MVP & Repo Sync

## 1. Overview & Scope

Structures raw ideas into runnable, right-sized `v1.0.0` MVPs (`ideation_to_v1`) or aligns existing repositories with disk-accurate `README.md`, Triad v2.1 docs, active protocol contracts, and Dry-Run root hygiene (`project_organizer_sync`).

### When NOT to Use
- **0–100 AST/Live-DOM MVP Audits:** Use `system-project-auditor` (read-only audits).
- **Single-Module Feature Coding:** Use `solution-content-architect`.
- **Standalone Mermaid Flows or OS Disk Cleanup:** Use `flow-filetree-organizer`, `windows-disk-maintenance`, or `gdrive-cleanup-auditor`.

## 2. Inputs & Prerequisites

- **Mode 1 (`ideation_to_v1`):** Target folder or idea draft, core goal, and `1–3` round replies.
- **Mode 2 (`project_organizer_sync`):** `project_root`, manifests (`pyproject.toml`, `package.json`, `go.mod`), real source imports, and `git remote -v`.

## 3. Step-by-Step Procedure

Consult [`mcp_fastapi_rpc_contracts_guide.md`](references/mcp_fastapi_rpc_contracts_guide.md) and [`organizer_output_template.md`](references/organizer_output_template.md):

1. **Step 0 — Scale & Archetype Right-Sizing Gate:**
   - **Micro / Script / CLI (`1–4` source files, no network/MCP boundary):** Use a flat vertical slice (`<app>.py`, `tests/test_<app>.py`, `README.md`, manifest, `.gitignore`). Triad `.context/` is optional; **never** create `src/api/`, `src/domain/`, `src/contracts/`, `DESIGN.md`, or `tools.json`.
   - **Single Service / Web App / MCP Server (`5–20` source files):** Follow stack-native layout (`server.py` + `shared/` or `src/<pkg>/`), initialize Triad v2.1 via `pwsh -NoProfile -File C:\Users\melki\dev\tools\bootstrap-project.ps1 -TargetDir <path>`, add contracts *only* for the protocol active in manifests (`FastMCP` *or* `FastAPI` *or* `JSON-RPC`), and add `DESIGN.md` *only* when UI files exist.
   - **Multi-Domain Platform (`> 20` source files or multi-protocol):** Explicit domain/contract packages + Triad v2.1 + Mermaid component diagram (`>= 3` interacting components).
   - **Hard Invariant:** Never create a subdirectory for fewer than `2` real files, and never add unrequested protocol layers.
2. **Mode 1 (`ideation_to_v1`):** Ask `1–3` high-impact questions (on *"I don't know"*, propose the smallest runnable vertical slice: `Input -> Real Logic -> Verifiable Output + 1 Test`), defer non-core ideas to `Deferred (Post-MVP)` instead of creating empty stubs, and confirm under HITL before writing `v1.0.0` files.
3. **Mode 2 (`project_organizer_sync` + ReAct RAW):** Inspect manifests and imports first; **preserve working package paths and imports** (never reshuffle functional code into an abstract template); sync `README.md` 1:1 with disk; preview stray root moves via **Dry-Run HITL**; verify all written Triad/README paths via `Read-After-Write`.

## 4. Gotchas & Edge Cases

- **Zero Empty Layers or Broken Imports:** Ban empty `TODO`/stub folders, speculative `tools.json`/`src/api/` bloat, and renaming imported packages without fixing callers.
- **Secrets & Mandatory Dry-Run:** Never expose `.env` values, keep `.env` in `.gitignore`, and never move/delete root files without explicit user approval.

## 5. Output Schema & Validation Criteria

Deliver the applicable sections in [`organizer_output_template.md`](references/organizer_output_template.md) (omitting Mermaid when `< 3` components interact), validated with `[PASS]`/`[FAIL]`/`[UNVERIFIED]` against [`rules/audit_criteria.md`](rules/audit_criteria.md).

## 6. User Communication Rule

All internal governance docs (`AGENTS.md`, `.context/spec.md`, `.context/context.md`), schemas, and contracts stay in Technical English; **all user-facing questions, *"I don't know"* MVP proposals, dry-run root previews, and Self-Refine summaries MUST be delivered in Portuguese (Brazil / `pt-BR`)**, unless explicitly requested otherwise.
