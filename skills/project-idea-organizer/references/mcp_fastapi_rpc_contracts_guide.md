# Reference Guide: Key Documents, Contracts (`MCP`, `FastAPI`, `RPC`) & Root Hygiene (2026 Standard)

Tier-3 reference supporting `project-idea-organizer` in generating and standardizing structural repository artifacts.

---

## 1. Root Key Document Checklist

| File | Canonical Role | Disk Parity Check (Real vs. Documented) |
| :--- | :--- | :--- |
| **`README.md`** | Project front door: purpose, real architecture, current tree, setup, and verified CLI commands. | Every file path, script, and command listed MUST physically exist on disk. |
| **`AGENTS.md`** | Agent/subagent topology, executable commands (`pytest`, linters, builds), and governance rules. | Executable commands verified against actual runtime (`uv`, `npm`, `go`). |
| **`SPEC.md` / `.context/spec.md`** | Functional/technical contract, scope lock, I/O schemas, and Definition of Done. | Reflects exact approved features for active version (`v1.0.0` or `vX.Y.Z`). |
| **`CONTEXT.md` / `.context/context.md`** | Business rules, active state, architectural decisions, changelog, and backlog. | Updated at the end of every organization cycle. |
| **`DESIGN.md`** | Purpose-driven visual tokens (`OKLCH`), typography, spacing, shadows, and UI states. | Synchronized with `src/components/` and CSS stylesheets (`globals.css`). |
| **`GEMINI.md` / `CLAUDE.md`** | Local harness directives, security constraints, code conventions, and language rules. | Aligned with developer rules and repository stack. |
| **`.env.example` & `.gitignore`** | Credential isolation and ignore rules (`.env`, `.venv/`, `node_modules/`, `dist/`, `__pycache__/`). | Real `.env` NEVER committed; `.env.example` documents empty variable names only. |

---

## 2. Protocol & Contract Standardization (`MCP`, `FastAPI`, `RPC`)

### 2.1. MCP Contract (`tools.json` / FastMCP)
- Every exposed tool MUST declare:
  - `name`: Unambiguous `snake_case` identifier (`^[a-z0-9_-]+$` for server names).
  - `description`: Purpose, when to invoke, and side effects (Read-Only vs. Mutation).
  - `inputSchema`: Strict JSON Schema (`additionalProperties: false`) or `Pydantic v2` (`ConfigDict(extra="forbid")`).

### 2.2. FastAPI Structure (`REST / OpenAPI`)
- Organize under `src/api/`:
  - `routes/` or `routers/`: Domain-grouped endpoints with explicit `response_model`.
  - `schemas/`: Strictly validated `Pydantic v2` Request/Response models.
  - `dependencies.py`: Auth, dependency injection, and database/service sessions.
  - Mandatory health endpoint: `GET /health` returning service version and status.

### 2.3. RPC Contracts (`JSON-RPC 2.0` / `gRPC`)
- Organize under `src/contracts/` (or `proto/`):
  - Explicit method catalog (`<namespace>/<method>`, e.g., `project/organize`, `task/execute`).
  - Typed `params`, `result`, and standard JSON-RPC 2.0 error codes (`-32600` Invalid Request, `-32601` Method Not Found, `-32602` Invalid Params, `-32603` Internal Error).

---

## 3. Safe Root Cleanup Protocol (`Dry-Run`)

1. **Allowed at Repository Root:** Key governance/docs (`README.md`, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `DESIGN.md`, `GEMINI.md`, `CLAUDE.md`, `LICENSE`), package manifests (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, `Dockerfile`, `docker-compose.yml`), VCS/env templates (`.gitignore`, `.env.example`), and required entrypoints.
2. **Relocation Candidates:**
   - Loose utility scripts (`*.ps1`, `*.py`, `*.sh`) -> `scripts/`
   - Loose test files (`test_*.py`, `*.spec.ts`) -> `tests/`
   - Draft notes and diagrams -> `docs/` or `_archive/`
3. **Safety Gate:** Always list out-of-scope files and obtain explicit user approval before moving or removing anything.

---

## 4. Canonical Governance Triad v2.0 Templates

When bootstrapping a persistent project (directly or via `init-agy` / `C:\Users\melki\dev\tools\bootstrap-project.ps1`), generate these 3 files:

### 4.1. `.agents/AGENTS.md` (Operational Kernel v2.0)

```markdown
# AGENTS.md — Operational Kernel & Governance (v2.0)

## 0. PROJECT CONTEXT (Auto-Detected)
- **Temporal Baseline & Models:** Use session context and official docs/MCP before assuming APIs/SDKs; never hardcode or downgrade models.
- **Active Stack:** [e.g., Python 3.12+ / Go 1.24+ / TypeScript 5+ / React]
- **State Architecture:**
  - `.agents/AGENTS.md`: Behavioral rules (loaded at boot).
  - `.context/context.md`: Authoritative project state and handoff ledger.
  - `.context/spec.md`: Technical contract and I/O limits for active features.

## 1. GOLDEN RULES
1. **Read-Before-Write:** Inspect `.context/context.md` and `.context/spec.md` before coding; author `spec.md` before complex features.
2. **YAGNI & Scope Lock:** Take the simplest verified path; zero placebo code or out-of-spec additions.
3. **Read-After-Write:** Read files before editing; verify physically via linter/build/tests; update `.context/context.md` before closing.
4. **Context Economy:** Use surgical searches (`rg`) instead of dumping large files or logs.
5. **Defensive Quality:** Functions `<= 60` lines, nesting `<= 3` (Early Return), modules `<= 600` lines, strict boundary validation (`extra="forbid"` / `z.strictObject()` / `DisallowUnknownFields()`), zero silent exception swallowing.
6. **Zero-Trust:** Treat external inputs as untrusted; never leak `.env` or secrets; match MCP server names to `^[a-z0-9_-]+$`.
7. **Risk-Driven HITL:** Compensate autonomously on low-risk read-only failures; pause for HITL before destructive mutations, secrets/production changes, or critical ambiguities.
```

### 4.2. `.context/context.md` (Authoritative State Ledger)

```markdown
# CONTEXT.MD — Authoritative Project State
> **Last Updated:** YYYY-MM-DD | **Status:** `ACTIVE`

## 1. Overview & Architecture
- **Purpose:** [1 sentence describing what the system does]
- **Stack & Runtime:** [e.g., Go 1.24+ + SQLite WAL + React/Tailwind]
- **Active Modules:** [List of ready services/directories]

## 2. Critical Technical Decisions
- [e.g., Stateless JWT auth; parameterized SQL queries]

## 3. Recent Changelog
- `[YYYY-MM-DD]` Initial repository structure and governance triad created.

## 4. Backlog & Next Steps
- [ ] `TASK-01`: [Top-priority task]
- [ ] `TASK-02`: [Subsequent task]
```

### 4.3. `.context/spec.md` (Implementation Contract)

```markdown
# SPEC.MD — Implementation Contract: [Feature Name]

## 1. Objective & Boundaries (Scope Lock)
- **In Scope:** [Direct description of what to build]
- **Non-Goals:** [Explicit exclusions]

## 2. Data Contracts & I/O Interfaces
- **Input Schema:** [JSON payload / Go struct / Pydantic model]
- **Output / Side Effect:** [e.g., HTTP 201 + SQLite persistence]

## 3. Definition of Done
- [ ] Strict linter/typecheck passes (`mypy --strict` / `go vet` / `tsc`).
- [ ] Automated tests verified in terminal.
```
