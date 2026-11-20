# CONTEXT.MD — Authoritative Project State (`franklin-quebragalho` / Franklin Quebra-Galho)
> **Last Updated:** 2026-11-20 | **Status:** `ACTIVE`

## 1. Overview & Current Architecture

- **Purpose:** Central incubator of **21 Skills** (3-Tier *Progressive Disclosure* in Technical English + `pt-BR` Bilingual Bridge), **5 Local Declarative Subagents** (`agents/*.md`, plus **7 UI skills & 4 Actor-Critic subagents** federated in `shredded-shape`, and Zero-Context Goldfish review via the official `egm` plugin), **FastMCP Server (`server.py` — 13 Tools, 8 Resources, 2 Prompts)**, and **Agent2Agent Bridge (`A2A v1.0` + JWS signatures in `shared/a2a_bridge.py`)**.
- **Stack & Runtime:** Python 3.12+ (`uv` / `pyproject.toml`, `FastMCP`, `Pydantic v2`, `a2a-sdk` 1.2.2) + TypeScript 5+ / Node LTS (`google-drive-index-app`, `templates/universal-app`) + Go 1.24+ (`adk-go-mcp` interop) + Windows 11 (`pwsh`).
- **Active Modules:**
  - `"shared/"`: `catalog_service.py`, `_catalog_scoring.py`, `compass_topology.py`, `execution_orchestrator.py`, `modular_orchestrator.py`, `_progressive_registry.py`, `harness.py`, `_harness_idempotency.py`, `harness2_engine.py`, `harness2_tree.py`, `a2a_bridge.py`, `mcp_2026_advisor.py`, `trigger_eval_suite.py`, `agent_spec_loader.py`, `polymorphic_skill_envelope.py`, `tools/frontmatter_parser.py`.
  - `"skills/"`: **21 Canonical Skills** synced with `~/.gemini/config/plugins/franklin-skills/` (7 federated UI skills live in `../shredded-shape/skills/`).
  - `"agents/"`: **5 Local Subagents** (`intent-hitl-mediator`, `read-after-write-verifier`, `vault-memory-retriever`, `adk-go-operator`, `dev-workspace-publisher`).
  - `"rules/"`, `"plans/"`, `"references/"`, `"scripts/"`, `"templates/"`, `"tests/"`.

## 2. Critical Technical Decisions (Do Not Violate)

- **`[LOCK-01]` 3-in-1 Fusion in `system-project-auditor` (`v6.1.0`):** `antigravity-project-auditor` and `nav-x-func` remain strictly routing aliases in `shared/_catalog_scoring.py`.
- **`[LOCK-02]` Federated UI Optics SSOT:** All `OKLCH 60-30-10`, Dark elevation planes, shadow physics, `44/48px` targets, and WCAG 2.2 rules live exclusively in `../shredded-shape/rules/frontend-9-axes-guidelines.md`.
- **`[LOCK-03]` Pure Triad v2.1 & Global Memory Sync:** Keep ONLY `AGENTS.md`, `.context/context.md`, and `.context/spec.md` (no `CURRENT_STATE.md`, `MY_SKILLS.md`, `MY_AGENTS.md`, root `CONTEXT.md`/`SPEC.md`, or `.agents/AGENTS.md`). Run `uv run python scripts/sync_gemini_ecosystem.py` after any change to `skills/`, `agents/`, `rules/`, or Triad docs.
- **`[LOCK-04]` Technical English Internals + `pt-BR` Bridge:** Author all internal artifacts in Technical English (`<= 1,000` L2 tokens, `<= 420c` L1 desc, flat scalar `metadata:`) and deliver all user communication in **Portuguese (`pt-BR`)**. `audit-skills-antigravity` is retired (`scripts/validate_skills.py` + `shared/catalog_service.py`).
- **I/O Boundaries & Real-State:** Strict Pydantic `extra="forbid"`, `STDIO` stdout hygiene, native Antigravity 2.0 `tools:`, Zero Stubs (`STUB001`), and *Read-After-Write* verification.

## 3. Recent Changes (Changelog)

*(Historical phases `<= 2026-11-17` archived in [`.context/changelog_archive.md`](changelog_archive.md).)*

- `[2026-11-20]` **Cross-Repo Alignment (`shredded-shape` v1.6.0) & Radical Documentation/Reference Pruning:**
  - **DAG & Federation Parity:** Added `_strip_known_plan_metadata()` (`version`, `routing_modes`, `max_discovery_hops`) in `shared/execution_orchestrator.py` so `shredded-shape/plans/ui_actor_critic_dag.json` (`v1.6.0`) runs cleanly through `epic-volta`'s strict `DAGExecutionPlan(extra="forbid")`; registered `stitch-canvas` (`7` UI skills) across `shared/_catalog_scoring.py`, `shared/compass_topology.py`, `AGENTS.md`, `README.md`, and `tests/test_server.py`.
  - **Pure Triad & Virtual Persona Retirement:** Deleted redundant `CURRENT_STATE.md`, `MY_SKILLS.md`, `MY_AGENTS.md`, `.context/skills_budget_audit.json`, and stray `ms-azuretools.vscode-docker-2.0.0.vsix`; switched `skills://manifest` in `server.py` to live disk-rendered `skills_list_impl()`; replaced 8 virtual personas and 18 obsolete `3+1`/`onda*`/`wave*` aliases with 6 clean functional domains + real subagents; made `memories/audit_report.json` writes idempotent (timestamp-invariant) in `agent_server_auditor.py`; stopped copying `ui-*.md` into backend-only `adk-py-agents/.agents/agents/`.
  - **L3 Pruning & Contradiction Removal:** Eliminated opposite Dark Mode `L`/glow values in `system-project-auditor/references/`, consolidated `refine-prompt` (`6 -> 2` refs) and `agent-server-auditor` (`audit_websocket_jsonrpc.md`), trimmed `android_2026_versions_and_agp9_matrix.md` (`<= 140`L), compacted `test-quality-auditor` refs and 8 dense L1 descriptions (`<= 330c`), and archived old changelogs (`31.2 KB -> ~7 KB`).
- `[2026-11-20]` **SOTA 4-Tier Verdict Ranking & `/learn` Persistence (`vault_palace_search.py` v2.2, `obsidian-vault-curator` v1.4.0):**
  - Added native `veredito:` 4-tier SOTA multipliers (`recomendado 1.10x` .. `contraindicacao-total 0.50x -> arquivo`), expanded `SKIP_DIRS`, added unit + adversarial tests in `tests/test_vault_palace_search.py`, and persisted MemPalace `v3.12.0` Closet-First, `exclude_patterns` purge, and temporal KG invariants across `obsidian-vault-curator` (`v1.4.0`), `dev/notes/AGENTS.md`, and `~/.agents/skills/obsidian-vault`.
- `[2026-11-18]` **Single-DB KG Hydration & Wave 2 ADK Go v2 Parity (`21/21 APPROVED`):**
  - Scoped `vault_kg_hydrator.py` to unified `~/.config/mempalace/palace/knowledge_graph.sqlite3` preserving `adapter_name IS NULL` MCP facts; flattened `metadata.tags` to CSV scalars with top-level `allowed-tools` across all `21` skills; fixed Ruff `F/B/E9` defects; modularized all `> 600`L modules (`<= 600`L/file, `<= 60`L/fn); upgraded template/evals to `WCAG 2.2`.

## 4. Active Backlog
- [ ] Run periodic `scripts/sync_official_docs_specs.py` checks when Google publishes new Gemini / ADK releases.
- [ ] Clean legacy `3+1` / `WCAG 2.1` references in `epic-volta` and compact `PCM/.context/context.md` (`38 KB`) in a dedicated follow-up session.
