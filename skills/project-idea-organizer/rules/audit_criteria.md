# Deterministic Audit & Rejection Criteria (`project-idea-organizer` v1.3.0)

Every run is verified against real disk state and proportional scope using three deterministic markers:

- `[PASS]`: Requirement verified against real files on disk, active manifests, and proportional scope.
- `[FAIL]`: Violation of right-sizing rules, `README.md`-vs-disk parity, secret safety, or unconfirmed root mutation.
- `[UNVERIFIED]`: Cannot be verified due to missing filesystem access or pending user response during discovery.

---

### Rule 1: Dynamic Routing & Smart *"I Don't Know"* Fallback (Mode 1)

- **Criterion**: When refining an idea (`ideation_to_v1`), did the skill ask `1–3` focused questions, propose a minimal runnable vertical slice (`Input -> Real Logic -> Verifiable Output + 1 Test`) if the user answered *"I don't know"*, defer extras to `Deferred (Post-MVP)`, and offer dated `v1.0.0` confirmation (`YYYY-MM-DD`)?
- **Test**:
  - Stalled when user answered *"I don't know"* without proposing a runnable vertical slice -> `[FAIL: FALLBACK_UNKNOWN_OMITTED]`
  - Missing dated version metadata (`YYYY-MM-DD`) when locking `v1.0.0` -> `[FAIL: VERSION_METADATA_MISSING]`
  - Minimal runnable slice proposed with right-sized layout and HITL confirmation -> `[PASS]`

---

### Rule 2: Right-Sized Structure, Preserved Imports & `README.md` 1:1 Disk Parity (Mode 2)

- **Criterion**: Did the skill match the layout to actual scale (flat `1–4` files for micro/CLI without empty sublayers; Triad v2.1 root `AGENTS.md` + `.context/{context,spec}.md` via `bootstrap-project.ps1` only when `>= 5` source files or non-trivial service), preserve working package imports, and ensure `README.md` matches disk 1:1?
- **Test**:
  - Created empty subfolders (`< 2` files), `src/api`+`src/domain`+`src/contracts` for a simple script/CLI, unrequested `DESIGN.md`/`tools.json`, legacy `.agents/AGENTS.md`, or broke working imports -> `[FAIL: SPECULATIVE_FOLDER_BLOAT]`
  - `README.md` cites files, scripts, or folders absent from disk without marking them as roadmap -> `[FAIL: README_OUT_OF_SYNC_VS_DISK]`
  - Delivered hollow/placebo MVP modules lacking basic logic or security -> `[FAIL: PLACEBO_OR_INSECURE_MVP]`
  - Persistent repo (`>= 5` files) missing Triad v2.1 governance docs -> `[FAIL: KEY_GOVERNANCE_DOCS_INCOMPLETE]`
  - Proportional layout, functional code, preserved imports, and 1:1 `README.md` verified (or Triad optional on `1–4` file micro-repos) -> `[PASS]`

---

### Rule 3: Conditional Protocol Contract Organization (`MCP`, `FastAPI`, `RPC`)

- **Criterion**: When the target project actually exposes `MCP`, `FastAPI`, or `JSON-RPC 2.0` interfaces in manifests/source, were only the active contracts organized with strict schemas (`extra="forbid"` / `.strict()`)?
- **Test**:
  - Project has no MCP/HTTP/RPC surface and none were fabricated -> `[PASS: N/A_NO_PROTOCOL_SURFACE]`
  - Active MCP/FastAPI/RPC contracts scattered or missing strict schemas -> `[FAIL: UNORGANIZED_CONTRACTS]`
  - Active contracts cleanly typed and organized -> `[PASS]`

---

### Rule 4: Security (`.env` / `.gitignore`), Remote Check & Dry-Run Root Hygiene

- **Criterion**: Did the skill verify `.env` protection in `.gitignore`, inspect `git remote -v`, and preview root cleanup (`Dry-Run`) before moving or deleting any files?
- **Test**:
  - Deleted or moved root files without explicit user approval -> `[FAIL: DESTRUCTIVE_ROOT_CLEANUP]`
  - Real `.env` secrets exposed in docs or missing `.gitignore` protection -> `[FAIL: SECRET_EXPOSURE_OR_MISSING_GITIGNORE]`
  - Safe dry-run preview presented, `.env`/`.gitignore` verified, and git remote status reported -> `[PASS]`

---

### Rule 5: Conditional Mermaid Flowchart & `.context/context.md` Synchronization

- **Criterion**: When `>= 3` runtime components interact, was a valid Mermaid diagram produced, and on persistent Triad repos (`>= 5` files) was `.context/context.md` updated?
- **Test**:
  - Micro/CLI utility (`1–4` files, linear flow, Triad optional) omitted gratuitous diagram/context files -> `[PASS: N/A_LINEAR_MICRO_REPO]`
  - Multi-component workflow shipped without Mermaid diagram or `.context/context.md` left stale on a Triad repo -> `[FAIL: MISSING_FLOWCHART_OR_STALE_CONTEXT]`
  - Conditional Mermaid diagram and `.context/context.md` verified -> `[PASS]`
