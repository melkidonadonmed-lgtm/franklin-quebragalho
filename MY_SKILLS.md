# My Skills (MY SKILLS)

> **Manifesto, Lifecycle Catalog, and Skill Version Registry**

This repository is the canonical skill catalog for **Franklin Quebra-Galho**. For UI architecture preferences, visual physics, and the **9-Axis + Complexity Matrix SSOT**, consult [`Preferências de Trabalho com Agentes.md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md) and the architectural locks in [`CURRENT_STATE.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CURRENT_STATE.md).

---

## Skill Lifecycle Table

| Status | Description |
| :--- | :--- |
| **Idea** | Initial concept draft or operational workflow need identified in daily work. |
| **Testing** | Implemented in `skills/<slug>/`, undergoing real scenario and eval validation. |
| **Validated** | Workflow verified end-to-end with complete Tier-1/2/3 docs and error handling. |
| **Production** | Consolidated, stable skill routinely dispatched by the orchestrator. |

---

### Workspace Skill Catalog (21 Canonical Skills)

| Skill | Version | Status | Short Description | Location |
| :--- | :---: | :---: | :--- | :--- |
| **`agent-server-auditor`** | `v1.2.0` | Production | Polyglot (`Go`, `TypeScript`, `Python`, `Kotlin`) auditor for AI agents, MCP servers (`2026-07-28`, `STDIO` hygiene), WebSockets/JSON-RPC 2.0 ([`references/audit-websocket-jsonrpc.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/agent-server-auditor/references/audit-websocket-jsonrpc.md)), Gemini 4 / Decisions API / `v1beta`, A2A nodes (`v1.0`, JWS `agent-card.json`), `max_steps` bounds, and `memories/audit_report.json`. | [skills/agent-server-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/agent-server-auditor/SKILL.md) |
| **`android-agy-projects`** | `v2.1.0` | Production | Android specialist module for MVP architecture (Kotlin 2.4+, AGP 9.x Built-in Kotlin, KSP2, Compose BOM, Navigation 3), 5-axis CoT RCA (ANR, memory leaks, *Phase Deferral*, *Strong Skipping Mode*), and R8 Full Mode / Baseline Profiles. | [skills/android-agy-projects/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/android-agy-projects/SKILL.md) |
| **`chained-plan-orchestrator`** | `v3.0.0` | Production | Executive DAG compiler and orchestrator for parallel execution waves (Kahn via `scripts/dag_chain_validator.py`), `[P]` file-collision detector, *Context Fork* isolation ($\le 5$ rules/node), and `fallback_branch` / HITL routing. | [skills/chained-plan-orchestrator/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/chained-plan-orchestrator/SKILL.md) |
| **`code-acceptability-auditor`** | `v1.1.0` | Production | Gate 1 static AST and Pydantic v2 auditor for Python code (`13` rules including `STUB001` against `eval`/`exec`, `shell=True`, missing type hints, functions `> 60` lines), Quality Gate (`>= 75/100`), and Trigger Matrix ($F_1 = 1.0$). | [skills/code-acceptability-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-acceptability-auditor/SKILL.md) |
| **`code-quality-audit-3d-physics`** | `v1.0.0` | Production | Three-wave 3D physics and WebGL graphics auditor (`Three.js`, `Babylon.js`, shaders, collisions, AST Py/JS sanitization, Pass@10 tests, and $S_{\text{norm}}$ deterministic observer). | [skills/code-quality-audit-3d-physics/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/SKILL.md) |
| **`context-sentinel`** | `v1.1.0` | Production | Multi-turn context-window integrity auditor mitigating context rot and emitting structured deterministic session snapshots (`[FACT]`, `[PENDING]`, `[GAP]`) in SQLite or JSON. | [skills/context-sentinel/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/context-sentinel/SKILL.md) |
| **`flow-filetree-organizer`** | `v1.2.0` | Production | Converts raw ideas and domain systems into Mermaid architecture diagrams, ASCII file trees, and execution plans with direct Markdown or PDF export. | [skills/flow-filetree-organizer/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/flow-filetree-organizer/SKILL.md) |
| **`gap-analyzer-auditor`** | `v2.2.0` | Production | Gate 3 gap and RCA analyst executing 4-vector failure inspection over logs/traces, separating `[FACT]`/`[INFERENCE]`/`[GAP]` and emitting *append-only* Spec-to-Code YAML hand-off payloads. | [skills/gap-analyzer-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gap-analyzer-auditor/SKILL.md) |
| **`gdrive-cleanup-auditor`** | `v1.2.0` | Production | Scans Google Drive (`G:\Meu Drive`) for heavy files (`>100MB`), SHA-256 duplicates, and orphaned roots with non-destructive quarantine staging (`_Quarentena_Descarte\YYYY-MM-DD`). | [skills/gdrive-cleanup-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-cleanup-auditor/SKILL.md) |
| **`gdrive-taxonomy-organizer`** | `v1.2.0` | Production | Applies the canonical numbered Google Drive taxonomy (`01_*`..`99_*`), ISO date prefixes (`YYYY-MM-DD`), and document triage with dry-run previews. | [skills/gdrive-taxonomy-organizer/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/gdrive-taxonomy-organizer/SKILL.md) |
| **`high-level-context-planner`** | `v3.0.0` | Production | Non-linear cognitive planner (`scripts/cognitive_plan_builder.py`): 4-quadrant intent triage, structured reasoning (`CoT`/`ToT`/`ReAct`/`Self-Refine`), Complexity Wall guard ($\le 5$ rules/node), mandatory Phase 0, and *append-only* convergence. | [skills/high-level-context-planner/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/high-level-context-planner/SKILL.md) |
| **`html-pdf-converter`** | `v1.2.0` | Production | Deterministic Markdown and HTML to professional PDF converter using headless Edge/Chrome (`scripts/md-to-pdf.ps1`) and calibrated `@page` print CSS. | [skills/html-pdf-converter/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/html-pdf-converter/SKILL.md) |
| **`obsidian-vault-curator`** | `v1.3.0` | Production | Bulk curator for the Obsidian Vault (`C:\Users\melki\dev\notes\`): repairs YAML frontmatter, broken `[[Wikilinks]]`, canonical tags, and orphaned attachments with zero data loss. | [skills/obsidian-vault-curator/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/obsidian-vault-curator/SKILL.md) |
| **`project-idea-organizer`** | `v1.3.0` | Production | Right-sized zero-to-one vertical-slice MVP organizer (`ideation_to_v1`) via `1–3` questions + *"I don't know"* fallback, and disk-truth Triad v2.1 repository sync (`project_organizer_sync`) without empty folder bloat. | [skills/project-idea-organizer/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/project-idea-organizer/SKILL.md) |
| **`re-a-ndroid`** | `v2.2.0` | Production | Deep Android APK reverse-engineering and security auditor using REA, ADB, CoT, ReAct, and Self-Refine: DEX/`.so` decompilation, `v1–v3.1` signatures, placebo detection, route latency, `48dp` targets, and 6 formal metrics. | [skills/re-a-ndroid/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/re-a-ndroid/SKILL.md) |
| **`refine-prompt`** | `v3.3.0` | Production | Isolated epistemic prompt auditor (`[VERDICT]`, `[FACT]`/`[INFERENCE]`/`[GAP]`), Socratic entropy modulation, and Zero-Trust XML prompt refactoring aligned with OWASP LLM Top 10. | [skills/refine-prompt/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/refine-prompt/SKILL.md) |
| **`solution-content-architect`** | `v2.6.0` | Production | Right-sized technical architect delivering direct typed production code, OpenAPI/JSON-RPC contracts, SQL optimizations, and simpler-baseline trade-off blueprints with zero dead abstractions. | [skills/solution-content-architect/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/solution-content-architect/SKILL.md) |
| **`system-project-auditor`** | `v6.1.0` | Production | **Integrated 3-in-1 Stack-Adaptive Auditor** (`[LOCK-01]`): polyglot AST & physical tree inspection (`scripts/project_structure_and_code_auditor.py`), adaptive Backend/CLI vs. UI `SGA V1 vs V2` (`scripts/deterministic_scorer.py`), conditional 9-Axis `OKLCH` / `agent-browser` DOM checks, and defect-driven remediation. | [skills/system-project-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/system-project-auditor/SKILL.md) |
| **`technical-markdown-writer`** | `v1.3.0` | Production | Technical writer producing executive reports, ADRs, engineering specs, and roadmaps in Markdown with Obsidian YAML frontmatter and strict Blank-Line Law formatting. | [skills/technical-markdown-writer/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/technical-markdown-writer/SKILL.md) |
| **`test-quality-auditor`** | `v1.3.0` | Production | Gate 2 modular test-suite auditor across 5 domains (Python, TypeScript, Go, MCP `JSON-RPC 2.0`, and Harness HITL/Evals) detecting Green Build Illusion and emitting `grading.json` + `perfkit_stats.py`. | [skills/test-quality-auditor/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/test-quality-auditor/SKILL.md) |
| **`windows-disk-maintenance`** | `v1.2.0` | Production | Windows 11 local disk hygiene (`pwsh`): `Downloads` and `Desktop` triage, installer quarantine, and `C:\Users\melki\dev\` workspace categorization with `-WhatIf` safety. | [skills/windows-disk-maintenance/](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/windows-disk-maintenance/SKILL.md) |

---

### Federated UI/UX Suite (`../shredded-shape` — 6 Skills)

All UI/UX analysis, branding, implementation, and visual verification skills were separated into the sibling plugin repository [`shredded-shape`](file:///C:/Users/melki/dev/repos/shredded-shape) and remain discoverable via `franklin-skills` federation:

- **4 Actor-Critic Pipeline Skills:** `ui-frontend-analyst` (`Stage 0`), `ui-brand-ux-planner` (`Stage 1`), `ui-clean-worker` (`Stage 2`), `ui-quality-judge` (`Stage 3`)
- **2 Domain Packs:** `clinical-minimalist-ui`, `complex-zero`
- **4 Declarative UI Subagents & DAG:** `ui-analyst`, `ui-planner`, `ui-worker`, `ui-judge` orchestrated via `../shredded-shape/plans/ui_actor_critic_dag.json`

## Recent Version History (Changelog)

### `[2026-11-16]` — Phase 35: UI/UX Decoupling into `shredded-shape` (`28 -> 21` Canonical Skills, `6 + 4` Federated UI Suite)

- Extracted the 7 legacy UI skills into [`shredded-shape`](file:///C:/Users/melki/dev/repos/shredded-shape) (6 Actor-Critic & domain skills + 4 declarative UI subagents), keeping 21 canonical non-UI skills in `skills/`.

### `[2026-11-16]` — Phase 34: Bilingual Standardization (`agentskills.io` + Antigravity 2.0), Retirement of `audit-skills-antigravity` (`29 -> 28` Canonical Skills), and `pt-BR` Bridge

- **Internal Artifacts in Technical English + Bilingual Bridge (`pt-BR` User Layer):** Retired `audit-skills-antigravity` (deterministic checks merged into `scripts/validate_skills.py` and `shared/catalog_service.py`), renamed the 12 Portuguese skill directories and `rules/{quality-efficiency-guidelines,frontend-9-axes-guidelines}.md` to English slugs while keeping all legacy aliases in `shared/catalog_service.py`, standardized all 28 `SKILL.md` contracts (`<= 1,000` tokens, explicit `When NOT to Use`, `Gotchas & Edge Cases`, bilingual `metadata.tags`, zero `../` link escapes, `evals/evals.json` `+2/-2`), updated all 10 `agents/*.md` subagents with native Antigravity 2.0 `tools:`, and standardized the 17 owned satellite skills (`adk-go-mcp/skills`, 9 owned in `~/.agents/skills`, `mytts`).

### `[2026-11-13]` — Gemini 4 (`hydrogen`/`argon`/`carbon`), `Orchestrator`, Decisions API, `googleapis` SDKs (`v1`/`v1beta` + `kotlin-genai`) & Zero-Drift

- **Gemini 4 & `googleapis` Baseline:** Updated rules, `AGENTS.md`, `agent-server-auditor`, and `references/official_sources.json` for `gemini-4-hydrogen` (`xhigh`), `gemini-4-argon`, `gemini-4-carbon`, Decisions API (`gemini-decision-1`), `antigravity-preview-09-2026`, `google-genai>=3.3.0`, `@google/genai>=3.3.0`, `v1` vs `v1beta` breaking change, and retired `gemini_search_docs`.

### `[2026-11-03]` — Phase 30: 3-in-1 Fusion (`system-project-auditor` `v6.0.0`), `rules/` + `CURRENT_STATE.md`, and 3-Layer Shadow Physics

- Merged `antigravity-project-auditor` and `nav-x-func` into `system-project-auditor` (`v6.0.0`, `[LOCK-01]`), added `CURRENT_STATE.md` (`[LOCK-01..03]`), and enforced `OKLCH` + 3-layer shadows (`[LOCK-02]`).
