# Deterministic Audit & Rejection Criteria (`project-idea-organizer` v1.2.0)

To ensure both greenfield ideation (`ideation_to_v1`) and repository restructuring (`project_organizer_sync`) remain auditable and grounded in actual disk state, every run is verified using three deterministic markers:

- `[PASS]`: Requirement verified against real files on disk and contracts.
- `[FAIL]`: Violation of operational rules, `README.md`-vs-disk mismatch, or unconfirmed root cleanup.
- `[UNVERIFIED]`: Cannot be verified due to missing filesystem access or pending user response during ideation.

---

### Rule 1: Dynamic Routing & Smart *"I Don't Know"* Fallback (Mode 1)

- **Criterion**: When refining an idea (`ideation_to_v1`), did the skill investigate intent, ask for desired features, provide a concrete MVP proposal if the user answered *"I don't know"*, ask whether to modify features, and offer dated `v1.0.0` creation (`YYYY-MM-DD`)?
- **Test**:
  - Stalled when user answered *"I don't know"* without proposing an MVP -> `[FAIL: FALLBACK_UNKNOWN_OMITTED]`
  - Missing dated version metadata (`YYYY-MM-DD`) when locking `v1.0.0` -> `[FAIL: VERSION_METADATA_MISSING]`
  - Clear MVP proposed with folder design and `v1.0.0` confirmation prompt -> `[PASS]`

---

### Rule 2: Holistic Analysis, Pre-Filled Ideal Structure & `README.md` 1:1 Disk Parity (Mode 2)

- **Criterion**: During `project_organizer_sync`, did the skill map actual disk state, compare reference patterns, explain each file's role, pre-fill working secure starter code, align Triad governance docs (`AGENTS.md`, `.context/spec.md`, `.context/context.md`), and verify 1:1 `README.md` parity?
- **Test**:
  - `README.md` cites files, scripts, or folders absent from disk without marking them as roadmap -> `[FAIL: README_OUT_OF_SYNC_VS_DISK]`
  - Delivered hollow/placebo MVP modules lacking basic logic or security -> `[FAIL: PLACEBO_OR_INSECURE_MVP]`
  - Missing Triad governance documents -> `[FAIL: KEY_GOVERNANCE_DOCS_INCOMPLETE]`
  - Ideal structure explained, functional starter code provided, and `README.md` 1:1 with disk -> `[PASS]`

---

### Rule 3: Component & Protocol Contract Organization (`MCP`, `FastAPI`, `RPC`)

- **Criterion**: Did the skill audit and organize applicable communication contracts (`tools.json` / FastMCP, FastAPI routers/schemas, JSON-RPC 2.0 methods) using strict 2026 typing?
- **Test**:
  - Scattered or undocumented RPC/MCP/FastAPI contracts left unorganized -> `[FAIL: UNORGANIZED_CONTRACTS]`
  - Contracts structured with explicit methods and strict schemas -> `[PASS]`

---

### Rule 4: Security (`.env` / `.gitignore`), Remote Check & Dry-Run Root Hygiene

- **Criterion**: Did the skill verify `.env` vs. `.gitignore`, inspect `git remote -v`, and preview root cleanup (`Dry-Run`) before moving or deleting any files?
- **Test**:
  - Deleted or moved root files without explicit user approval -> `[FAIL: DESTRUCTIVE_ROOT_CLEANUP]`
  - Real `.env` secrets exposed in docs or missing `.gitignore` validation -> `[FAIL: SECRET_EXPOSURE_OR_MISSING_GITIGNORE]`
  - Safe dry-run root preview presented, `.env`/`.gitignore` verified, and git remote status reported -> `[PASS]`

---

### Rule 5: Valid Mermaid Flowchart & Context State Synchronization

- **Criterion**: When operational workflows exist, did the skill generate a valid Mermaid diagram (double-quoted labels with special characters) and update `.context/context.md` / `CONTEXT.md`?
- **Test**:
  - Clear operational workflow shipped without a Mermaid flowchart -> `[FAIL: MISSING_FLOWCHART_DIAGRAM]`
  - Project context file left stale after restructuring -> `[FAIL: CONTEXT_MEMORY_STALE]`
  - Valid Mermaid flowchart and synchronized context state -> `[PASS]`
