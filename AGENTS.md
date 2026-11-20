# AGENTS.md — Repository Delta & Topology (`franklin-quebragalho` v2.1) — Franklin Quebra-Galho

> **Global Kernel Inheritance:** Universal Golden Rules (1–8), `Managed Antigravity Agent` API constraints, Bilingual Bridge (`[LOCK-04]`: Technical English internals / **Portuguese (`pt-BR`)** user dialogue), and the Self-Refine Closing Block are enforced globally via [`rules/quality-efficiency-guidelines.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/rules/quality-efficiency-guidelines.md) (`always_on`).

## 0. PROJECT CONTEXT & COMMANDS

- **Project:** `franklin-quebragalho` (**Franklin Quebra-Galho** — Incubator of **21 Canonical Skills**, **5 Local Declarative Subagents**, **FastMCP Server (`server.py`)**, and **A2A v1.0 JWS Bridge**; **7 UI/UX skills + 4 Actor-Critic subagents** federated in [`shredded-shape`](file:///c:/Users/melki/dev/repos/shredded-shape); Goldfish review via official `egm` plugin).
- **Active Stack:** Python 3.12+ (local 3.15, `uv` / `pyproject.toml`, `FastMCP`, `Pydantic v2`, `a2a-sdk`) + TypeScript 5+ / Node LTS (`google-drive-index-app`, `templates/universal-app`) + Go 1.24+ (ADK/MCP interop) + Windows 11 (`pwsh`).
- **Executable Commands (`Command-First`):**
  - **Unit Tests & MCP Contracts:** `uv run pytest -q`
  - **Deterministic Catalog Validator (`21/21` skills):** `uv run python scripts/validate_skills.py --strict --ecosystem`
  - **Project Structural & AST Audit:** `uv run python skills/system-project-auditor/scripts/project_structure_and_code_auditor.py --self-test`
  - **AST Quality Audit (`Quality Score >= 75`):** `uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --file server.py`
  - **Ecosystem Synchronization (`~/.gemini`, `rules/`, `.agents/`, `.context/` & `memories/audit_report.json`):** `uv run python scripts/sync_gemini_ecosystem.py`
- **Canonical Triad (SSOT):** [`.context/context.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/context.md) | [`.context/spec.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/spec.md) | [`Preferências de Trabalho com Agentes.md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md)

## 1. FUNCTIONAL DOMAINS (`6`) & DECLARATIVE SUBAGENTS (`5` Local + `4` UI Federated)

| Domain | Real Scope of Action | Core Skills (`skills/` + `shredded-shape`) | Activation Trigger |
| :--- | :--- | :--- | :--- |
| **`core-engineering`** | 3-in-1 Project Auditor, MVP Architecture, Android, 3D Physics & Prompts | `system-project-auditor`, `solution-content-architect`, `android-agy-projects`, `project-idea-organizer`, `code-quality-audit-3d-physics`, `context-sentinel`, `refine-prompt` | Direct execution, MVP/SGA diagnostics, Android, 3D physics, prompt entropy, and context governance. |
| **`ui-suite`** | UI Architecture, Optical Physics, Stitch Bridge & Actor-Critic QA (Federated in `../shredded-shape`) | `ui-frontend-analyst`, `ui-brand-ux-planner`, `ui-clean-worker`, `ui-quality-judge`, `clinical-minimalist-ui`, `complex-zero`, `stitch-canvas` | DevTools inventory, AI Slop, 5-Plane `OKLCH`, Stitch Canvas bridge, Light/Dark craft, and 3-Axis WCAG 2.2 Judge. |
| **`quality-engineering`** | Deterministic AST Quality, 5-Module Test Suites, MCP/A2A Servers & Android REA | `code-acceptability-auditor`, `test-quality-auditor`, `agent-server-auditor`, `re-a-ndroid` | AST gate (`>= 75/100`), test suites (`Pass@k`), MCP `2026-07-28` / A2A JWS compliance, and APK reverse engineering. |
| **`planning-orchestration`** | Non-Linear Cognitive Planning, DAG Graphs (Kahn) & Closed-Loop RCA | `high-level-context-planner`, `chained-plan-orchestrator`, `gap-analyzer-auditor` | Phase 0 decomposition (`<= 5` rules/node), parallel DAG waves, and root-cause analysis (`[FACT]`/`[INFERENCE]`/`[GAP]`). |
| **`knowledge-docs`** | Obsidian Vault Curation, Technical Markdown, Mermaid Flows & PDF Export | `obsidian-vault-curator`, `technical-markdown-writer`, `html-pdf-converter`, `flow-filetree-organizer` | Bulk vault hygiene (`wing: notes`), technical reports, file trees, and headless Edge PDF export. |
| **`workspace-ops`** | Google Drive (`G:\Meu Drive`) & Windows 11 (`pwsh`) Disk Hygiene | `gdrive-cleanup-auditor`, `gdrive-taxonomy-organizer`, `windows-disk-maintenance` | Heavy/duplicate quarantine, ISO (`YYYY-MM-DD`) Drive taxonomy, and `Downloads`/`Desktop` triage (`-WhatIf`). |

### Declarative Subagents (`agents/*.md` via `invoke_subagent` or `franklin_execute_dag`)

1. **Federated UI 4-Stage Actor-Critic Pipeline (`../shredded-shape/plans/ui_actor_critic_dag.json` via `franklin_execute_dag("ui")`):**
   - **Stage 0**: [`ui-analyst`](file:///c:/Users/melki/dev/repos/shredded-shape/agents/ui-analyst.md) (Read-Only CoT DevTools/Slop & 7-Section CLAREZA)
   - **Stage 1**: [`ui-planner`](file:///c:/Users/melki/dev/repos/shredded-shape/agents/ui-planner.md) (Read-Only ToT `DESIGN.md`, 5-Plane `OKLCH`, 7 styles, bounded DAG `<= 5` rules/node)
   - **Stage 2**: [`ui-worker`](file:///c:/Users/melki/dev/repos/shredded-shape/agents/ui-worker.md) (ReAct Light/Dark implementation + RAW SHA-256)
   - **Stage 3**: [`ui-judge`](file:///c:/Users/melki/dev/repos/shredded-shape/agents/ui-judge.md) (Read-Only Double-Pass 3-Axis WCAG 2.2 OKLab `FNR < 0.001` & Self-Refine loop)
2. **Local Governance, Memory & Operations (`5` Subagents in `agents/*.md` + `[Plugin: egm]` Goldfish Review):**
   - [`intent-hitl-mediator`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/intent-hitl-mediator.md) (Pydantic Triage + HITL Gate + GCP Labels)
   - [`read-after-write-verifier`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/read-after-write-verifier.md) (Post-mutation Physical Verification & Fan-In)
   - [`vault-memory-retriever`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/vault-memory-retriever.md) (Hybrid Obsidian Vault + MemPalace retrieval `~35ms`)
   - [`adk-go-operator`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/adk-go-operator.md) (On-demand `adk-go-mcp` operator)
   - [`dev-workspace-publisher`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/dev-workspace-publisher.md) (Bootstrap, anti-secret scan, and GitHub publish under HITL)
   - **`[Plugin: egm]` (`egm-synthesizer` / `/egm:egm-review`)**: Zero-Context Goldfish spec/design reviews.

## 2. REPOSITORY ARCHITECTURAL LOCKS

- **`[LOCK-01]` 3-in-1 Fusion in `system-project-auditor` (`v6.1.0`):** Forbidden to recreate `skills/antigravity-project-auditor/`, `skills/nav-x-func/`, or `skills/auditoria-projetos-sistema/`; legacy names remain routing aliases in `shared/_catalog_scoring.py`.
- **`[LOCK-02]` Federated UI Optics SSOT:** All `OKLCH 60-30-10`, Dark Mode elevation planes, shadow physics, `44/48px` targets, and WCAG 2.2 rules live exclusively in [`../shredded-shape/rules/frontend-9-axes-guidelines.md`](file:///c:/Users/melki/dev/repos/shredded-shape/rules/frontend-9-axes-guidelines.md) (never duplicate literal UI physics here).
- **`[LOCK-03]` Pure Triad v2.1 & Ecosystem Sync:** Maintain ONLY `AGENTS.md`, `.context/context.md`, and `.context/spec.md` (never recreate `CURRENT_STATE.md`, `MY_SKILLS.md`, `MY_AGENTS.md`, root `CONTEXT.md`/`SPEC.md`, or `.agents/AGENTS.md`). Run `uv run python scripts/sync_gemini_ecosystem.py` after editing `skills/`, `agents/`, `rules/`, or Triad docs.
- **`[LOCK-04]` Retired `audit-skills-antigravity` & Bilingual Bridge:** All deterministic skill/ecosystem checks live in `scripts/validate_skills.py --strict --ecosystem` and `shared/catalog_service.py`; internals stay Technical English (`<= 1,000` L2 tokens, `<= 420c` L1 desc) and user dialogue stays `pt-BR`.
