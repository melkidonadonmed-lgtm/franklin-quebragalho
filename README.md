# Franklin Quebra-Galho

> **Master Orchestrator & Canonical Catalog for Daily Automation and Software Engineering**

**Franklin Quebra-Galho** (`franklin-quebragalho`) is Melki's central productivity and engineering agent ecosystem, combining **21 Canonical Skills** (Technical English internals + Portuguese `pt-BR` Bilingual Bridge), **6 Local Declarative Subagents** (plus **4 Federated UI Subagents** in [`shredded-shape`](file:///C:/Users/melki/dev/repos/shredded-shape)), versioned governance rules ([`rules/`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/rules/quality-efficiency-guidelines.md)), architectural locks ([`CURRENT_STATE.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CURRENT_STATE.md)), and the **Franklin Skills MCP Server** ([`server.py`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/server.py)).

---

## Quick Skill Catalog (21 Canonical Skills)

| Skill | Version | Status | Primary Purpose | Link |
| :--- | :---: | :---: | :--- | :--- |
| **`agent-server-auditor`** | `v1.2.0` | Production | Polyglot (Go, TS, Py, Kotlin) agent/MCP `2026-07-28` auditor, A2A `v1.0` JWS cards, WebSockets/JSON-RPC 2.0, `max_steps` guards, and `memories/audit_report.json`. | [skills/agent-server-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/agent-server-auditor/SKILL.md) |
| **`android-agy-projects`** | `v2.1.0` | Production | Android specialist: MVP scaffolding (Kotlin 2.4+, AGP 9.x Built-in Kotlin, KSP2, Compose BOM, Navigation 3), 5-axis CoT RCA, and R8 Full Mode / Baseline Profiles. | [skills/android-agy-projects/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/android-agy-projects/SKILL.md) |
| **`chained-plan-orchestrator`** | `v3.0.0` | Production | Executive DAG compiler and orchestrator for parallel waves (Kahn via `dag_chain_validator.py`) with `[P]` collision detection and shared-state isolation. | [skills/chained-plan-orchestrator/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/chained-plan-orchestrator/SKILL.md) |
| **`code-acceptability-auditor`** | `v1.1.0` | Production | Gate 1 static AST/Pydantic auditor for Python code (`12` rules), Quality Gate (`>= 75/100`), and Trigger Matrix ($F_1=1.0$). | [skills/code-acceptability-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-acceptability-auditor/SKILL.md) |
| **`code-quality-audit-3d-physics`** | `v1.0.0` | Production | Three-wave code and 3D Physics audit (`Three.js`, `Babylon.js`, shaders, collisions, Pass@10, and $S_{\text{norm}}$ observer). | [skills/code-quality-audit-3d-physics/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/SKILL.md) |
| **`context-sentinel`** | `v1.1.0` | Production | Multi-turn context-window integrity auditing, context-rot mitigation, and deterministic structured session snapshots (`[FACT]`, `[PENDING]`, `[GAP]`). | [skills/context-sentinel/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/context-sentinel/SKILL.md) |
| **`flow-filetree-organizer`** | `v1.2.0` | Production | Converts raw ideas into Mermaid diagrams, ASCII file trees, and execution plans with direct MD/PDF export. | [skills/flow-filetree-organizer/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/flow-filetree-organizer/SKILL.md) |
| **`gap-analyzer-auditor`** | `v2.2.0` | Production | Gate 3 4-vector RCA auditor, `[FACT]`/`[INFERENCE]`/`[GAP]` segregation, and YAML hand-off emission. | [skills/gap-analyzer-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gap-analyzer-auditor/SKILL.md) |
| **`gdrive-cleanup-auditor`** | `v1.2.0` | Production | Scans Google Drive (`G:\Meu Drive`) for heavy files (`>100MB`), SHA-256 duplicates, and safe quarantine staging. | [skills/gdrive-cleanup-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-cleanup-auditor/SKILL.md) |
| **`gdrive-taxonomy-organizer`** | `v1.2.0` | Production | Canonical numbered Google Drive taxonomy, ISO (`YYYY-MM-DD`) naming, and document triage. | [skills/gdrive-taxonomy-organizer/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-taxonomy-organizer/SKILL.md) |
| **`high-level-context-planner`** | `v3.0.0` | Production | Non-linear cognitive planner (`cognitive_plan_builder.py`), mandatory Phase 0, parallelizable tasks, Complexity Wall guard, and *append-only* convergence. | [skills/high-level-context-planner/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/high-level-context-planner/SKILL.md) |
| **`html-pdf-converter`** | `v1.2.0` | Production | Deterministic Markdown/HTML to print-grade PDF converter via headless Edge/Chrome (`scripts/md-to-pdf.ps1`). | [skills/html-pdf-converter/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/html-pdf-converter/SKILL.md) |
| **`obsidian-vault-curator`** | `v1.3.0` | Production | Bulk curation of the Obsidian Vault (`C:\Users\melki\dev\notes\`): YAML frontmatter repair, `[[Wikilinks]]`, and orphaned attachments. | [skills/obsidian-vault-curator/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/obsidian-vault-curator/SKILL.md) |
| **`project-idea-organizer`** | `v1.2.0` | Production | Zero-to-one idea organizer (`ideation_to_v1`) and disk-truth repository organizer (`project_organizer_sync`). | [skills/project-idea-organizer/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/project-idea-organizer/SKILL.md) |
| **`re-a-ndroid`** | `v2.2.0` | Production | Full Android APK reverse engineering and audit via REA + ADB: DEX/`.so` decompilation, `v1–v3.1` signatures, CVEs, placebo functions, route latency, `48dp` accessibility, and 6 formal metrics. | [skills/re-a-ndroid/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/re-a-ndroid/SKILL.md) |
| **`refine-prompt`** | `v3.3.0` | Production | Feasibility auditing, epistemic tagging (`[FACT]`/`[INFERENCE]`/`[GAP]`), entropy modulation, and Zero-Trust XML prompt refinement. | [skills/refine-prompt/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/refine-prompt/SKILL.md) |
| **`solution-content-architect`** | `v2.5.0` | Production | Autonomous 4-mode technical architect (Modes A, B, C, D), comparative ToT, enterprise prompts, typed code, and roadmaps. | [skills/solution-content-architect/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/solution-content-architect/SKILL.md) |
| **`system-project-auditor`** | `v6.0.0` | Production | **Integrated 3-in-1 Auditor** (`[LOCK-01]`): real AST/tree inspection (`project_structure_and_code_auditor.py`), 3-Layer Navigation & Functional Islands (`deterministic_scorer.py` `SGA V1 vs V2`), 9-Axis SSOT (`OKLCH`, 3-level shadows, `@container`, 4 Cards), `agent-browser` DOM check, and 3-Phase Evolution Plan. | [skills/system-project-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/system-project-auditor/SKILL.md) |
| **`technical-markdown-writer`** | `v1.3.0` | Production | Technical writing of executive reports, engineering notes, and specs in Markdown compatible with `C:\Users\melki\dev\notes\Inbox\`. | [skills/technical-markdown-writer/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/technical-markdown-writer/SKILL.md) |
| **`test-quality-auditor`** | `v1.3.0` | Production | Gate 2 modular test auditor across 5 domains (Python, TS/JS, Go, MCP, and Harness) detecting Green Build Illusion + `perfkit_stats.py`. | [skills/test-quality-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/test-quality-auditor/SKILL.md) |
| **`windows-disk-maintenance`** | `v1.2.0` | Production | Triage of `Downloads`, `Desktop`, installer quarantine, and `C:\Users\melki\dev\` organization with `-WhatIf` dry-run. | [skills/windows-disk-maintenance/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/windows-disk-maintenance/SKILL.md) |

---

> **Federated UI/UX Plugin:** Frontend analysis, branding, implementation, and visual gatekeeping live in [`shredded-shape`](file:///C:/Users/melki/dev/repos/shredded-shape) (6 skills: `ui-frontend-analyst`, `ui-brand-ux-planner`, `ui-clean-worker`, `ui-quality-judge`, `clinical-minimalist-ui`, `complex-zero`; 4 subagents: `ui-analyst`, `ui-planner`, `ui-worker`, `ui-judge`) and remain federated into `franklin-skills` MCP discovery.

## Quick Commands

- **Run MCP Server Locally**: `uv run python server.py`
- **Run Full Test Suite**: `uv run pytest -q`
- **Validate All Canonical Skills (`21/21`)**: `uv run python scripts/validate_skills.py --strict --ecosystem`
- **Audit Physical Project Structure & AST**: `uv run python skills/system-project-auditor/scripts/project_structure_and_code_auditor.py --self-test`
- **Sync Catalog, Rules, Subagents & Global Plugin**: `uv run python scripts/sync_gemini_ecosystem.py`
- **Read Current State & Architectural Locks**: [CURRENT_STATE.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CURRENT_STATE.md)
- **Read Design & Engineering Preferences SSOT**: [Preferências de Trabalho com Agentes.md](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md)
