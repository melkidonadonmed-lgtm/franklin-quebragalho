# 5 Technical Pillars Matrix (2026 Standard), 60-30-10 OKLCH & Project Orchestration

Level 3 reference for `system-project-auditor` (`v6.0.0` — canonical fusion of `system-project-auditor`, legacy `antigravity-project-auditor`, and `nav-x-func`), detailing evaluation criteria and boundaries with `project-idea-organizer` and `android-agy-projects`.

---

## 1. Canonical Ecosystem Flow for Projects + Android Module (2026)

| Step | Canonical Skill | Mode / Scope | Exact Responsibility (Zero Overlap) |
| :---: | :--- | :--- | :--- |
| **1** | **`project-idea-organizer`** | `Mode 1: ideation_to_v1` \| `Mode 2: project_organizer_sync` | **Conception & Active Hygiene:** Guided MVP scoping from scratch (`ideation_to_v1`) or 1:1 creation/sync of key governance docs (`README.md` matching disk, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `CURRENT_STATE.md`, `DESIGN.md`), contracts (`MCP`/`FastAPI`/`RPC`), and root cleanup. |
| **2** | **`system-project-auditor`** | `Mode 1: mvp_and_plan` \| `Mode 2: deep_code_and_nav_audit` \| `Mode 3: live_dom_inspection` | **Unified Project, Real-Code, Navigation & UI Audit (0–100 pts + SGA/TIF):** Runs `project_structure_and_code_auditor.py`, `deterministic_scorer.py`, and `frontiercode_maintainability_guardrail.py`; diagnoses MVP blockers (`Why:`), reconciles `README.md`/`SPEC.md` vs. real code, audits 3-Layer Navigation (`X activates Y`), `60-30-10 OKLCH`, and DOM via `agent-browser` (`@eX`). |
| **2B** | **`android-agy-projects`** | `GREEN \| COT \| AUDIT` | **Android Specialist Module:** 2026 Android MVP creation (`libs.versions.toml`, AGP 9.x Built-in Kotlin, KSP2 `2.3.12`, Compose BOM `2026.09.00`, Navigation 3), 5-axis RCA (ANR, Memory Leaks, Phase Deferral, Strong Skipping Mode), and R8 Full Mode / Baseline Profiles audit. |

---

## 2. 2026 Reference Criteria Across the 5 Mandatory Pillars

| Pillar | 2026 Technical Reference (`[PRIORITY]` if violated on critical path) |
| :--- | :--- |
| **1. Design, UI/UX, `60-30-10` Rule & `OKLCH` Colors** | Project-driven identity (`design-md` SSOT): **60-30-10 Color Ratio** (`60%` dominant `--bg-canvas`/`--surface-canvas`, `30%` secondary `--bg-surface-1`/`--surface-card` and `--bg-surface-2`/`--surface-elevated`, `10%` surgical `--brand-primary` or achromatic contrast), **Perceptual `OKLCH`** (`oklch(L C H / alpha)`, `light-dark()`, `color-mix(in oklab, ...)`), Dark Mode without `#000000` ($L = 0.16 \to 0.22 \to 0.27$), **Zenith Lighting (90°–120° with `inset 0 1px 0 0`)**, **3-Level Multi-Layer Shadows** (`--shadow-elevation-1..3`: Umbra + negative-spread Penumbra + Specular Rim), **6 Spatial Archetypes** + `@container`, **3-Layer Navigation** (`<= 3 <nav>`, menus `>= 13px`, `X activates Y`), GPU anti-blur locks (`antialiased`, `font-synthesis: none`, zero fractional `scale()` on text), `tabular-nums`, WCAG 2.1 AA ($\ge 4.5:1$), targets $\ge 44\times44\text{px}$, and Real-State engineering (zero placebos). |
| **2. Security (AppSec & AI)** | Secrets exclusively in `.env` (clean `.env.example` + strict `.gitignore`), boundary schema validation (`Pydantic v2` `extra="forbid"`, `Zod`), anti-XSS sanitization (`DOMPurify`), and Zero-Trust isolation against Prompt Injection in tools and agents. |
| **3. Temporal Baseline** | Active runtimes & SDKs grounded in session context and official docs/MCP: Python `3.12+` (`uv`), `google-genai>=3.3.0`, `@google/genai>=3.3.0`, `google.golang.org/genai>=1.77.0` (Gemini 4 family — `gemini-4-hydrogen` with `xhigh`, `gemini-4-argon`, `gemini-4-carbon`, Decisions `gemini-decision-1`, Live `gemini-3.8-live`), `google-adk>=2.14.1` / `adk-go>=2.7.1`, `FastMCP` / MCP Spec `2026-07-28`, `a2a-sdk` `1.0+` (JCS/JWS), TS `5+` / Node LTS, Go `1.24+`. Conditional lookup via `google-developer-knowledge` / `gemini_get_doc` (`aistudio.google.com/llms.txt`; never invoke disabled doc-search aliases) and `audit-websocket-jsonrpc.md` when applicable. |
| **4. Real-Code AST Quality** | Mandatory source-code inspection (`project_structure_and_code_auditor.py` + `frontiercode_maintainability_guardrail.py`): cohesive modularity (functions $\le 60$ lines, McCabe $M \le 10$), strict typing (zero `any`, `dataclass(frozen=True)` / `BaseModel`), ban on bare `except:` or placebo stubs (`pass`, `onClick={() => {}}`), and zero orphan files. |
| **5. Physical Tree, Navigation & Components** | Clean root (only manifests and core docs `README.md`, `AGENTS.md`, `.context/spec.md`, `.context/context.md`, `CURRENT_STATE.md`), versioned `rules/` folder, clear `src/`, `scripts/`, `tests/` separation, and UI tab governance (allowed for distinct domains; banned for duplicate functions, nested sub-tabs, or backend-internal modules). |
