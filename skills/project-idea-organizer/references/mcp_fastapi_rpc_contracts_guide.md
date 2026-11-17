# Reference Guide: Governance Docs, Conditional Contracts (`MCP`, `FastAPI`, `RPC`) & Root Hygiene (`v1.3.0`)

Tier-3 reference supporting `project-idea-organizer` in generating right-sized repository artifacts aligned with `[LOCK-03]`.

---

## 1. Key Document Checklist (Right-Sized by Scale)

| File | Canonical Role | Disk Parity Check (Real vs. Documented) |
| :--- | :--- | :--- |
| **`README.md`** | Project front door: purpose, real layout, setup, and verified CLI commands. | Every file path, script, and command listed MUST physically exist on disk. |
| **`AGENTS.md`** (*Root Delta-Only, `>= 5` files*) | Repo-specific rules, module map, and executable verification commands (`pytest`, linters, builds). | Inherits global kernel (`quality-efficiency-guidelines.md`); never mirror inside `.agents/AGENTS.md`. |
| **`.context/spec.md`** (*`>= 5` files or non-trivial MVP*) | Functional/technical contract, scope lock, I/O schemas, and Definition of Done. | Reflects exact active scope (`v1.0.0` or `vX.Y.Z`); never duplicate at root `SPEC.md`. |
| **`.context/context.md`** (*`>= 5` files*) | Live architectural decisions, active modules, changelog, and backlog. | Updated after reorganization; never duplicate at root `CONTEXT.md`. |
| **`DESIGN.md`** (*UI targets only*) | Purpose-driven visual tokens (`OKLCH`), typography, spacing, shadows, and UI states. | Omit on backend/CLI repos; when present, sync with active stylesheets/components. |
| **`.env.example` & `.gitignore`** | Credential isolation and ignore rules (`.env`, `.venv/`, `node_modules/`, `dist/`, `__pycache__/`). | Real `.env` NEVER committed; create `.env.example` only if environment variables exist. |

---

## 2. Strictly Conditional Protocol Contracts (`MCP`, `FastAPI`, `RPC`)

Create or organize **only** the contract matching the protocol present in the repository manifest or explicit user request—never scaffold unused protocol folders:

### 2.1. MCP Contract (Only for MCP Servers — `FastMCP` / `mcp`)
- Every exposed tool MUST declare `snake_case` `name`, `description` (purpose + side effects), and strict validation (`Pydantic v2 ConfigDict(extra="forbid")` or `additionalProperties: false` JSON Schema); server names match `^[a-z0-9_-]+$`.

### 2.2. FastAPI Structure (Only for HTTP REST Services — `fastapi`)
- Organize routers and strict `Pydantic v2` request/response schemas next to active endpoints (avoid empty `api/`/`domain/`/`contracts/` splits for single-file services), exposing `GET /health` when running as a service.

### 2.3. RPC Contracts (Only for `JSON-RPC 2.0` / `gRPC` Boundaries)
- Define explicit `<namespace>/<method>` catalogs, typed `params`/`result` payloads, and standard JSON-RPC 2.0 error codes (`-32600`..`-32603`).

---

## 3. Safe Root Cleanup Protocol (`Dry-Run`)

1. **Allowed at Repository Root:** Key governance/docs (`README.md`, `AGENTS.md`, `CURRENT_STATE.md`, `DESIGN.md` if UI, `LICENSE`), package manifests (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, `Dockerfile`, `docker-compose.yml`), VCS/env templates (`.gitignore`, `.env.example`), and flat micro-repo entrypoints (`1–4` files).
2. **Relocation Candidates (Only when moving `>= 2` stray files or keeping existing structure cleaner):**
   - Stray utility scripts (`*.ps1`, `*.py`, `*.sh`) -> `scripts/`
   - Loose test files (`test_*.py`, `*.spec.ts`) -> `tests/`
   - Draft notes and diagrams -> `docs/` or `_archive/`
3. **Safety Gate:** Never break working package imports; always preview moves in a Dry-Run table and obtain HITL confirmation before modifying disk files.

---

## 4. Canonical Triad v2.1 Bootstrap Protocol (`>= 5` Source Files or Multi-Module Repos)

Do **NOT** hand-copy obsolete v2.0 `.agents/AGENTS.md` boilerplate or duplicate global Golden Rules into child repositories (`[LOCK-03]`). Run the canonical bootstrap script and customize only repo-specific details:

```powershell
pwsh -NoProfile -File C:\Users\melki\dev\tools\bootstrap-project.ps1 -TargetDir <project_root>
```

After execution, verify all 3 generated files via Read-After-Write and tailor:
1. Root **`AGENTS.md`** (Delta-Only `v2.1`): fill exact `Project`, `Active Stack`, `Active Modules`, and `Command-First` test/linter commands.
2. **`.context/context.md`**: fill the 1-sentence `Purpose`, verified module paths, critical technical decisions, and active backlog.
3. **`.context/spec.md`**: lock `In-Scope`, `Non-Goals`, exact I/O schemas, and `Definition of Done`.
