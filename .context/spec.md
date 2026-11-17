# SPEC.MD — Implementation Contract: Franklin Quebra-Galho (`franklin-quebragalho` v2.1)

> Referenced directly by [`AGENTS.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/AGENTS.md) and mirrored between [`.context/spec.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/.context/spec.md), [`SPEC.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/SPEC.md), and [`CURRENT_STATE.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CURRENT_STATE.md).

## 1. Objective and Boundaries (Scope Lock)
- **What to build:**
  1. **FastMCP Server (`server.py`) & Modular Domain (`shared/`):** Official MCP server (`franklin-skills` under protocol `2026-07-28` over `stdio`) exposing **13 tools**, **8 passive resources**, and **2 structured prompts**.
  2. **Master Catalog of 21 Agent Skills (`skills/`):** Three-tier *Progressive Disclosure* architecture (Tier 1 XML `<available_skills>`, Tier 2 Technical English `SKILL.md` `< 100` lines / `<= 1,000` tokens with `pt-BR` Bilingual Bridge, Tier 3 `scripts/`, `references/`, `rules/audit_criteria.md`, `evals/evals.json`) validated deterministically by `scripts/validate_skills.py` and `shared/trigger_eval_suite.py` ($F_1 = 1.0$), with federated alias routing into `../shredded-shape/skills/` for UI/UX workflows.
  3. **Agent2Agent Bus (`A2A v1.0` JWS) & Zero-Trust Harness² (`shared/a2a_bridge.py` + `shared/harness.py`):** Protobuf validation (`a2a.types.AgentCard`), RFC 8785 canonical signing (JCS) + HMAC-SHA256 JWS (`.well-known/agent-card.json`), `SemanticGuard`, HITL `CheckpointStore` (`.sessions/harness_checkpoints.json`), MCP idempotency, and recursive Harness² engine (`shared/harness2_engine.py` + `shared/harness2_tree.py`).
  4. **Mesh of 6 Declarative Subagents (`agents/*.md`), Federated `shredded-shape` UI Actor-Critic Plugin & SSOT Governance (`rules/*.md`):** `intent-hitl-mediator`, `read-after-write-verifier`, `review-squad`, `vault-memory-retriever`, `adk-go-operator`, `dev-workspace-publisher` (plus federated UI subagents `ui-analyst`, `ui-planner`, `ui-worker`, `ui-judge` in `../shredded-shape/agents/`), synchronized via `scripts/sync_gemini_ecosystem.py`.
- **Non-Goals (Forbidden):**
  - Forbidden to recreate legacy directories `antigravity-project-auditor`, `nav-x-func`, `auditoria-projetos-sistema` (consolidated into `skills/system-project-auditor/SKILL.md` `v6.0.0` under `[LOCK-01]`), or the retired `audit-skills-antigravity` skill (`[LOCK-04]`).
  - Forbidden to emit debug logs to `stdout` in `stdio` MCP servers, use symlinks/junctions instead of physical copies during skill sync, or include `../` parent path escapes in `SKILL.md` relative links.
  - Forbidden to exceed `600` lines in orchestration modules (`server.py`, `shared/*.py`) or weaken Zero-Trust/HITL validations in automated tests.

---

## 2. Data Contracts and Interfaces (I/O)

### 2.1 Modules and Technical Contracts

| Module / File | Responsibility and Contract |
| :--- | :--- |
| **`server.py`** | FastMCP (`stdio`) server exposing **13 tools**, **8 resources** (`skills://catalog`, `skills://catalog/xml`, `skills://manifest`, `skills://agents`, `skills://agent/{agent_name}`, `skills://skill/{skill_name}`, `skills://a2a/agent-card`, `skills://mcp-2026/spec`, `skills://harness/checkpoints`), and **2 prompts** (`activate_skill`, `tactile_frontend_audit`). |
| **`shared/catalog_service.py`** | Discovery, metadata indexing (including bilingual PT/EN tags), ranked search, 3-Tier progressive loading, backward-compatible and federated aliases (including UI aliases into `../shredded-shape/skills/`), and deterministic validation of the **21 Agent Skills**. |
| **`shared/compass_topology.py`** | Zero-LLM semantic compass (`franklin_smart_compass`), 5-layer Multi-Repo Topology, and catalog of 8 personas + 6 Franklin subagents + 4 federated `shredded-shape` UI subagents (`franklin_get_agents`). |
| **`shared/execution_orchestrator.py`** | Sandboxed script runner (`.py`, `.js`, `.ps1`, `.cmd`), DAG plan resolution/execution in `epic-volta`, and HITL/A2A orchestration. |
| **`shared/modular_orchestrator.py`** | 6-role orchestrator (`Intent`, `Planner`, `Worker`, `HITL Gate`, `Critic Loop`, `Reporter`) and `ProgressiveSkillRegistry`. |
| **`shared/harness.py` & `shared/harness2_engine.py` & `shared/harness2_tree.py`** | `SemanticGuard.sanitize_input`, `evaluate_action_risk` (`LOW`, `MEDIUM`, `CRITICAL`), HITL `CheckpointStore`, `execute_with_idempotency`, `IntentBoundTokenValidator`, and recursive Harness² engine. |
| **`shared/a2a_bridge.py`** | Validates `AgentCard` via Protobuf (`a2a.types.AgentCard`) enforcing kebab-case `id` and mandatory `tags` across all **21 Agent Skills**, signs with JCS (RFC 8785) + JWS (`HMAC-SHA256` via `FRANKLIN_A2A_SIGNING_SECRET`), and manages tasks (`FranklinA2ATaskManager`). |
| **`shared/mcp_2026_advisor.py`** | Implements `franklin_mcp_build_advisor` (Pattern A `<15` tools vs Pattern B *Search + Execute* `>=15` tools, `ui://` MCP Apps, and `.mcpb` v0.4 manifest). |
| **`shared/agent_spec_loader.py` & `shared/tools/frontmatter_parser.py`** | Deterministic parsers for declarative subagent contracts (`agents/*.md`) and YAML frontmatter with resilient zero-dependency fallback. |
| **`rules/quality-efficiency-guidelines.md` & `rules/authoring-*.md`** | Versioned project guidelines synchronized automatically with `~/.gemini/config/rules/` and `~/.gemini/config/plugins/` via `scripts/sync_gemini_ecosystem.py`. |
| **`plans/physics_code_audit_dag.json` & `plans/distributed_agent_mediation_dag.json`** | Executable DAG plans for the Kahn execution engine (`epic-volta`; UI Actor-Critic DAG federated in `../shredded-shape/plans/ui_actor_critic_dag.json`). |
| **`tests/test_*.py`** | Automated Level-4 contract, parity, trigger-precision ($F_1 = 1.0$), A2A JWS, and adversarial Zero-Trust pytest suites. |

### 2.2 Catalog of 13 MCP Tools (`franklin-skills` • Protocol `2026-07-28`)
1. `franklin_skills_list` (`readOnlyHint=True`) — Lists all **21 Agent Skills** in Markdown, JSON, or Tier-1 XML (`<available_skills>`).
2. `franklin_skills_get` (`readOnlyHint=True`) — Loads `SKILL.md` contracts (Tier 2: `contract` / `activate`) and on-demand resources (`resource:<path>`, `rules`, `references`, `evals`, `scripts`, `all` in Tier 3) with path-traversal protection.
3. `franklin_skills_search` (`readOnlyHint=True`) — Ranked intent/domain/tag search with negative-clause penalty (`Do NOT use for` / `não use para`).
4. `franklin_skills_validate` (`readOnlyHint=True`) — Audits YAML frontmatter, kebab-case slugs, required English sections, `<500` line budget, and relative link safety across the **21 Agent Skills**.
5. `franklin_get_agents` (`readOnlyHint=True`) — Returns the 8 personas (`MY_AGENTS.md`), Multi-Repo Topology (`ecosystem`), and 10 declarative subagents (`agents/*.md`).
6. `franklin_smart_compass` (`readOnlyHint=True`) — Zero-LLM deterministic compass recommending the exact skill, persona, script, and DAG plan for a user intent.
7. `franklin_run_skill_script` (`readOnlyHint=False`, `idempotency_key`) — Executes auxiliary skill scripts with directory confinement, cross-project `target_dir` support, and Zero-Trust guardrails.
8. `franklin_execute_dag` (`readOnlyHint=False`, `idempotency_key`) — Validates or dispatches DAG plans (`ui`, `physics`, `mediation`) integrated with the SQLite WAL Kahn engine.
9. `franklin_harness_guard` (`readOnlyHint=False`) — Evaluates operational risk (`LOW`/`MEDIUM`/`CRITICAL`) and sanitizes inputs against Prompt Injection and XSS.
10. `franklin_harness_checkpoint` (`readOnlyHint=False`, `idempotency_key`) — Creates, queries, approves, or rejects Human-in-the-Loop checkpoints and dispatches Harness² actions (`validate_tree`, `evolve`, `record_experience`).
11. `franklin_a2a_agent_card` (`readOnlyHint=True`) — Generates and cryptographically verifies Franklin's A2A v1.0 `AgentCard` (`.well-known/agent-card.json`).
12. `franklin_a2a_dispatch_task` (`readOnlyHint=False`, `idempotency_key`) — Dispatches, queries, resumes, or cancels A2A v1.0 tasks with Zero-Trust and HITL enforcement.
13. `franklin_mcp_build_advisor` (`readOnlyHint=True`) — MCP Spec `2026-07-28` architectural advisor (`build-with-agent-skills`).

---

## 3. Acceptance and Exit Criteria (Definition of Done)
- [x] Pass 100% of the deterministic Pytest suite (`uv run pytest -q`).
- [x] Validate 100% of the **21 Canonical Skills** (`uv run python scripts/validate_skills.py --strict --ecosystem` — `21/21 PASS`, Top-1 trigger precision $F_1 = 1.0$).
- [x] Pass deterministic AST and structural auditors (`uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --file server.py` with `Score >= 75/100` and `uv run python skills/system-project-auditor/scripts/project_structure_and_code_auditor.py --self-test` with `[PASS]`).
- [x] Synchronize global and local ecosystems with zero drift (`uv run python scripts/sync_gemini_ecosystem.py` returning `"status": "SYNCHRONIZED"` and `memories/audit_report.json` with `100.0/100 APPROVED`).
