# Franklin Quebra-Galho

> **Master Orchestrator & Canonical Catalog for Daily Automation and Software Engineering**

**Franklin Quebra-Galho** (`franklin-quebragalho`) combines **21 Canonical Skills** (Technical English internals + Portuguese `pt-BR` Bilingual Bridge), **5 Local Declarative Subagents** (plus **7 Federated UI Skills & 4 Actor-Critic Subagents** in [`shredded-shape`](file:///C:/Users/melki/dev/repos/shredded-shape) and the official **`egm`** plugin), versioned governance rules ([`rules/`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/rules/quality-efficiency-guidelines.md)), Triad v2.1 state ([`.context/context.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/context.md)), and the **Franklin Skills MCP Server** ([`server.py`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/server.py)).

---

## Quick Skill Catalog (21 Canonical Skills)

| Skill | Version | Domain | Primary Purpose | Link |
| :--- | :---: | :--- | :--- | :--- |
| **`agent-server-auditor`** | `v1.2.1` | `quality-engineering` | Polyglot agent/MCP `2026-07-28` auditor, A2A `v1.0` JWS cards, WebSockets/JSON-RPC 2.0, `max_steps` guards, and `memories/audit_report.json`. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/agent-server-auditor/SKILL.md) |
| **`android-agy-projects`** | `v2.1.0` | `core-engineering` | Android MVP scaffolding (Kotlin 2.4+, AGP 9.x Built-in Kotlin, KSP2, Compose BOM, Navigation 3), 5-axis CoT RCA, and R8 Full Mode. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/android-agy-projects/SKILL.md) |
| **`chained-plan-orchestrator`** | `v3.0.0` | `planning-orchestration` | Executive DAG compiler for parallel Kahn waves (`dag_chain_validator.py`) with `[P]` collision detection and `<= 5`-rule Context Fork isolation. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/chained-plan-orchestrator/SKILL.md) |
| **`code-acceptability-auditor`** | `v1.1.1` | `quality-engineering` | Gate 1 static AST/Pydantic auditor for Python (`13` rules incl. `STUB001`), Quality Gate (`>= 75/100`), and Trigger Matrix ($F_1=1.0$). | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-acceptability-auditor/SKILL.md) |
| **`code-quality-audit-3d-physics`** | `v1.0.0` | `core-engineering` | Three-wave 3D Physics & WebGL auditor (`Three.js`, `Babylon.js`, shaders, collisions, Pass@10, and $S_{\text{norm}}$ observer). | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/SKILL.md) |
| **`context-sentinel`** | `v1.1.0` | `core-engineering` | Multi-turn context-window integrity auditing, context-rot mitigation, and structured session snapshots (`[FACT]`, `[PENDING]`, `[GAP]`). | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/context-sentinel/SKILL.md) |
| **`flow-filetree-organizer`** | `v1.2.0` | `knowledge-docs` | Converts raw ideas into Mermaid flowcharts, ASCII directory trees, and execution plans with MD/PDF export. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/flow-filetree-organizer/SKILL.md) |
| **`gap-analyzer-auditor`** | `v2.2.0` | `planning-orchestration` | Gate 3 4-vector RCA auditor, `[FACT]`/`[INFERENCE]`/`[GAP]` segregation, and YAML hand-off emission. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gap-analyzer-auditor/SKILL.md) |
| **`gdrive-cleanup-auditor`** | `v1.2.0` | `workspace-ops` | Scans Google Drive (`G:\Meu Drive`) for heavy files (`>100MB`), SHA-256 duplicates, and safe quarantine staging. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-cleanup-auditor/SKILL.md) |
| **`gdrive-taxonomy-organizer`** | `v1.2.0` | `workspace-ops` | Canonical numbered Google Drive taxonomy, ISO (`YYYY-MM-DD`) naming, and document triage. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-taxonomy-organizer/SKILL.md) |
| **`high-level-context-planner`** | `v3.0.0` | `planning-orchestration` | Non-linear cognitive planner (`cognitive_plan_builder.py`), mandatory Phase 0, Complexity Wall guard (`<= 5` rules/node), and *append-only* convergence. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/high-level-context-planner/SKILL.md) |
| **`html-pdf-converter`** | `v1.2.0` | `knowledge-docs` | Deterministic Markdown/HTML to print-grade PDF converter via headless Edge/Chrome (`scripts/md-to-pdf.ps1`). | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/html-pdf-converter/SKILL.md) |
| **`obsidian-vault-curator`** | `v1.4.0` | `knowledge-docs` | Bulk Obsidian Vault curator (`C:\Users\melki\dev\notes\`): YAML/SOTA `veredito:`, `[[Wikilinks]]`, `vault_palace_search.py` `v2.2`, and MemPalace sync. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/obsidian-vault-curator/SKILL.md) |
| **`project-idea-organizer`** | `v1.3.0` | `core-engineering` | Right-sized vertical-slice MVP bootstrapping (`ideation_to_v1`) and Triad v2.1 / 1:1 disk-truth repo sync (`project_organizer_sync`). | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/project-idea-organizer/SKILL.md) |
| **`re-a-ndroid`** | `v2.2.0` | `quality-engineering` | Android APK reverse engineering & security audit via REA + ADB: DEX/`.so`, `v1–v3.1` signatures, CVEs, placebo detection, and 6 metrics. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/re-a-ndroid/SKILL.md) |
| **`refine-prompt`** | `v3.3.0` | `core-engineering` | Epistemic prompt auditing (`[FACT]`/`[INFERENCE]`/`[GAP]`), entropy modulation, and Zero-Trust XML prompt refinement. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/refine-prompt/SKILL.md) |
| **`solution-content-architect`** | `v2.6.1` | `core-engineering` | Right-sized technical architect delivering typed production code, OpenAPI/JSON-RPC contracts, SQL optimizations, and trade-off blueprints. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/solution-content-architect/SKILL.md) |
| **`system-project-auditor`** | `v6.1.0` | `core-engineering` | **Integrated 3-in-1 Stack-Adaptive Auditor** (`[LOCK-01]`): polyglot AST/tree parity, `SGA V1 vs V2`, conditional UI checks, and defect-driven fixes. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/system-project-auditor/SKILL.md) |
| **`technical-markdown-writer`** | `v1.3.0` | `knowledge-docs` | Executive reports, ADRs, engineering notes, and specs in Markdown compatible with `C:\Users\melki\dev\notes\Inbox\`. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/technical-markdown-writer/SKILL.md) |
| **`test-quality-auditor`** | `v1.3.1` | `quality-engineering` | Gate 2 modular test auditor across 5 domains (Python, TS/JS, Go, MCP, Harness) detecting Green Build Illusion + `perfkit_stats.py`. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/test-quality-auditor/SKILL.md) |
| **`windows-disk-maintenance`** | `v1.2.0` | `workspace-ops` | Triage of `Downloads`, `Desktop`, installer quarantine, and `C:\Users\melki\dev\` organization with `-WhatIf` dry-run. | [SKILL.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/windows-disk-maintenance/SKILL.md) |

---

> **Federated UI/UX Plugin (`shredded-shape`):** Frontend analysis, branding, Stitch Canvas bridge, implementation, and 3-Axis WCAG 2.2 gatekeeping live in [`shredded-shape`](file:///C:/Users/melki/dev/repos/shredded-shape) (**7 skills:** `ui-frontend-analyst`, `ui-brand-ux-planner`, `ui-clean-worker`, `ui-quality-judge`, `clinical-minimalist-ui`, `complex-zero`, `stitch-canvas`; **4 subagents:** `ui-analyst`, `ui-planner`, `ui-worker`, `ui-judge`) and remain federated into `franklin-skills` MCP discovery.

## Quick Commands

- **Run MCP Server Locally**: `uv run python server.py`
- **Run Full Test Suite**: `uv run pytest -q`
- **Validate All Canonical Skills (`21/21`)**: `uv run python scripts/validate_skills.py --strict --ecosystem`
- **Audit Physical Project Structure & AST**: `uv run python skills/system-project-auditor/scripts/project_structure_and_code_auditor.py --self-test`
- **Sync Catalog, Rules, Subagents & Global Plugin**: `uv run python scripts/sync_gemini_ecosystem.py`
- **Read Authoritative Project State**: [`.context/context.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/context.md)
- **Read Design & Engineering Preferences SSOT**: [Preferências de Trabalho com Agentes.md](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md)
