# AGENTS.md — Repository Delta & Topology (`franklin-quebragalho` v2.1) — Franklin Quebra-Galho

> **Global Kernel Inheritance:** Universal Golden Rules (1–8), `Managed Antigravity Agent` API constraints, Bilingual Bridge (`[LOCK-04]`: Technical English internals / **Portuguese (`pt-BR`)** user dialogue), and the Self-Refine Closing Block are enforced globally via [`rules/quality-efficiency-guidelines.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/rules/quality-efficiency-guidelines.md) (`always_on`).

## 0. PROJECT CONTEXT & COMMANDS

- **Project:** `franklin-quebragalho` (**Franklin Quebra-Galho** — Incubator of **21 Canonical Skills**, **5 Declarative Subagents**, **FastMCP Server (`server.py`)**, and **A2A v1.0 JWS Bridge**; UI/UX suite federated in [`shredded-shape`](file:///c:/Users/melki/dev/repos/shredded-shape); Goldfish review via official `egm` plugin).
- **Active Stack:** Python 3.12+ (local 3.15, `uv` / `pyproject.toml`, `FastMCP`, `Pydantic v2`, `a2a-sdk`) + TypeScript 5+ / Node LTS (`google-drive-index-app`, `templates/universal-app`) + Go 1.24+ (standalone ADK/MCP services) + Windows 11 (`pwsh`).
- **Executable Commands (`Command-First`):**
  - **Unit Tests & MCP Contracts:** `uv run pytest -q`
  - **Deterministic Catalog Validator (`21/21` skills):** `uv run python scripts/validate_skills.py --strict --ecosystem`
  - **Project Structural & AST Audit:** `uv run python skills/system-project-auditor/scripts/project_structure_and_code_auditor.py --self-test`
  - **AST Quality Audit (`Quality Score >= 75`):** `uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --file server.py`
  - **Ecosystem Synchronization (`~/.gemini`, `rules/`, `.agents/`, `.context/` & `memories/audit_report.json`):** `uv run python scripts/sync_gemini_ecosystem.py`
- **Canonical Triad & SSOT Docs:** [`.context/context.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/context.md) | [`.context/spec.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/spec.md) | [`CURRENT_STATE.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CURRENT_STATE.md) | [`MY_AGENTS.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_AGENTS.md) | [`MY_SKILLS.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md) | [`Preferências de Trabalho com Agentes.md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md)

## 1. DOMAIN PERSONAS (8 Specialists) & DECLARATIVE SUBAGENTS (`5` Local + `4` UI Federated)

| Persona | Real Scope of Action | Core Skills (`skills/` + `shredded-shape`) | Activation Trigger |
| :--- | :--- | :--- | :--- |
| **`Franklin-Main`** | Master Orchestrator, 3-in-1 Auditor, MVP Architecture, Android & 3D Physics | `system-project-auditor`, `solution-content-architect`, `android-agy-projects`, `project-idea-organizer`, `code-quality-audit-3d-physics`, `context-sentinel`, `refine-prompt` | Direct execution, MVP diagnostics/planning, functional islands & `SGA`, Android, 3D physics, and context governance. |
| **`UI-Architect`** | UI Architecture, Optical Physics & Actor-Critic QA (Federated in `../shredded-shape`) | `ui-frontend-analyst`, `ui-brand-ux-planner`, `ui-clean-worker`, `ui-quality-judge`, `complex-zero`, `clinical-minimalist-ui` | DevTools inventory, AI Slop, brand/style archetypes, Stitch/Figma/Fonts/3D, Light 3-layer shadows, Dark rim light, and WCAG 2.2 OKLCH Judge. |
| **`SkillCraft`** | Deterministic AST Quality, 5-Module Test Suites, MCP/A2A Servers & Android REA | `code-acceptability-auditor`, `test-quality-auditor`, `agent-server-auditor`, `re-a-ndroid` | AST gate (`>= 75/100`), test suites (`Pass@k`), MCP `2026-07-28` / A2A JWS compliance, and APK reverse engineering. |
| **`LoopPlanner`** | Non-Linear Cognitive Planning, DAG Graphs (Kahn) & Closed-Loop RCA | `high-level-context-planner`, `chained-plan-orchestrator`, `gap-analyzer-auditor` | Phase 0 decomposition (`<= 5` rules/node), parallel DAG waves, and root-cause analysis (`[FACT]`/`[INFERENCE]`/`[GAP]`). |
| **`DriveMaster`** | Google Drive (`G:\Meu Drive`) Cleanup & Taxonomy | `gdrive-cleanup-auditor`, `gdrive-taxonomy-organizer` | Scans for `>100MB` files, SHA-256 duplicates, and ISO (`YYYY-MM-DD`) organization. |
| **`FileOpsLocal`** | Local Windows 11 (`pwsh`) Disk Maintenance | `windows-disk-maintenance` | Triage of `Downloads`/`Desktop` and `C:\Users\melki\dev\` hygiene. |
| **`VaultMaster`** | Obsidian Vault Curation & MemPalace Maintenance | `obsidian-vault-curator` | Bulk YAML frontmatter, `[[Wikilinks]]`, orphan attachment sweeps, and `wing: notes` sync. |
| **`DocMaker`** | Technical Markdown Authoring, Mermaid Flows & PDF Export | `technical-markdown-writer`, `html-pdf-converter`, `flow-filetree-organizer` | Technical notes, decision records, file trees, and headless Edge PDF export. |

### Declarative Subagents (`agents/*.md` via `invoke_subagent` or `franklin_execute_dag`)

1. **Federated UI Actor-Critic Pipeline (`../shredded-shape/plans/ui_actor_critic_dag.json` via `invoke_subagent` or `franklin_execute_dag("ui")`)**:
   - **Stage 0**: [`ui-analyst`](file:///c:/Users/melki/dev/repos/shredded-shape/agents/ui-analyst.md) (DevTools inventory, AI Slop & `Before vs. After` nav)
   - **Stage 1**: [`ui-planner`](file:///c:/Users/melki/dev/repos/shredded-shape/agents/ui-planner.md) (Brand, 7 styles, Stitch/Figma/Fonts/3D, `DESIGN.md` & DAG `<= 5` rules/node)
   - **Stage 2**: [`ui-worker`](file:///c:/Users/melki/dev/repos/shredded-shape/agents/ui-worker.md) (Clean Light/Dark ReAct implementation + RAW SHA-256)
   - **Stage 3 (Judge)**: [`ui-judge`](file:///c:/Users/melki/dev/repos/shredded-shape/agents/ui-judge.md) (Read-Only WCAG 2.2 OKLCH `FNR < 0.001` & Self-Refine loop)
2. **Local Governance, Memory & Operations (`5` Subagents in `agents/*.md` + `[Plugin: egm]` Goldfish Review)**:
   - [`intent-hitl-mediator`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/intent-hitl-mediator.md) (Pydantic Triage + HITL Gate + GCP Labels)
   - [`read-after-write-verifier`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/read-after-write-verifier.md) (Post-mutation Physical Verification & Fan-In)
   - [`vault-memory-retriever`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/vault-memory-retriever.md) (Hybrid Obsidian Vault + MemPalace retrieval `~35ms`)
   - [`adk-go-operator`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/adk-go-operator.md) (On-demand `adk-go-mcp` operator)
   - [`dev-workspace-publisher`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/agents/dev-workspace-publisher.md) (Bootstrap, anti-secret scan, and GitHub publish under HITL)
   - **`[Plugin: egm]` (`egm-synthesizer` / `/egm:egm-review` / `/egm:egm-review-loop`)**: Zero-Context Goldfish spec/design reviews and drift checks.

## 2. REPOSITORY ARCHITECTURAL LOCKS (Project-Learned Rules)

- **`[LOCK-01]` 3-in-1 Fusion in `system-project-auditor` (`v6.0.0`):** Forbidden to recreate `skills/antigravity-project-auditor/`, `skills/nav-x-func/`, or `skills/auditoria-projetos-sistema/`; legacy names remain strictly as aliases in `shared/catalog_service.py`.
- **`[LOCK-02]` Federated `60-30-10` `OKLCH` & 3-Layer Optics:** UI audits and templates follow [`../shredded-shape/rules/frontend-9-axes-guidelines.md`](file:///c:/Users/melki/dev/repos/shredded-shape/rules/frontend-9-axes-guidelines.md).
- **`[LOCK-03]` Mandatory Ecosystem Sync (`~/.gemini` & Canonical `.context/`):** Every edit to `skills/`, `agents/`, `rules/`, `AGENTS.md`, `.context/{context,spec}.md`, or `CURRENT_STATE.md` requires running `uv run python scripts/sync_gemini_ecosystem.py` (never recreate root `SPEC.md`/`CONTEXT.md` or `.agents/AGENTS.md` mirrors).
- **`[LOCK-04]` Retired `audit-skills-antigravity`:** All deterministic skill/ecosystem checks live in `scripts/validate_skills.py --strict --ecosystem` and `shared/catalog_service.py`.
