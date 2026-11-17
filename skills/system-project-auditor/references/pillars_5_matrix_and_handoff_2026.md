# 5 Technical Pillars Matrix (2026 Standard), Conditional `OKLCH` & Project Orchestration (`v6.1.0`)

Level 3 reference for `system-project-auditor` (`v6.1.0` — canonical fusion of `system-project-auditor`, legacy `antigravity-project-auditor`, and `nav-x-func`), detailing evaluation criteria and boundaries with `project-idea-organizer` and `android-agy-projects`.

---

## 1. Canonical Ecosystem Flow for Projects + Android Module (2026)

| Step | Canonical Skill | Mode / Scope | Exact Responsibility (Zero Overlap) |
| :---: | :--- | :--- | :--- |
| **1** | **`project-idea-organizer`** (`v1.3.0`) | `Mode 1: ideation_to_v1` \| `Mode 2: project_organizer_sync` | **Right-Sized Conception & Active Hygiene:** Guided runnable vertical-slice MVPs (`ideation_to_v1`) or 1:1 creation/sync of governance docs (`README.md` matching disk, root `AGENTS.md`, `.context/spec.md`, `.context/context.md`, `DESIGN.md` only if UI), active protocol contracts (`MCP`/`FastAPI`/`RPC`), and dry-run root cleanup. |
| **2** | **`system-project-auditor`** (`v6.1.0`) | `Mode 1: mvp_and_plan` \| `Mode 2: deep_code_and_nav_audit` \| `Mode 3: live_dom_inspection` | **Read-Only Stack-Adaptive Audit (`0–100 pts` + `SGA`/`TIF`):** Runs `project_structure_and_code_auditor.py`, `deterministic_scorer.py`, and (when `.py` files exist) `frontiercode_maintainability_guardrail.py`; diagnoses causal MVP blockers, reconciles `README.md`/`.context/spec.md` vs. real code, and activates UI/OKLCH/`@eX` checks *only* when `has_ui_layer == True`. |
| **2B** | **`android-agy-projects`** | `GREEN \| COT \| AUDIT` | **Android Specialist Module:** 2026 Android MVP creation (`libs.versions.toml`, AGP 9.x Built-in Kotlin, KSP2 `2.3.12`, Compose BOM `2026.09.00`, Navigation 3), 5-axis CoT RCA (ANR, Memory Leaks, Phase Deferral, Strong Skipping Mode), and R8 Full Mode / Baseline Profiles audit. |

---

## 2. 2026 Reference Criteria Across the 5 Mandatory Pillars

| Pillar | 2026 Technical Reference (`[PRIORITY]` if violated on critical path) |
| :--- | :--- |
| **1. Design, UI/UX, `60-30-10` Rule & `OKLCH` *(UI Targets Only — `[PASS: N/A_BACKEND_ONLY]` on Headless/CLI/Backend)* ** | Project-driven identity (`ui-brand-ux-planner` / `DESIGN.md` SSOT): **60-30-10 Color Ratio** (`60%` `--surface-canvas`, `30%` `--surface-card`/`--surface-elevated`, `10%` surgical `--brand-primary`), **Perceptual `OKLCH`** (`oklch(L C H / alpha)`, `light-dark()`, Dark Mode without `#000000` $L = 0.16 \to 0.22 \to 0.27$), **Zenith Lighting (90°–120° with `inset 0 1px 0 0`)**, **3-Level Multi-Layer Shadows**, **6 Spatial Archetypes** + `@container`, **3-Layer Navigation**, GPU anti-blur locks, `tabular-nums`, WCAG 2.2 AA ($\ge 4.5:1$), targets $\ge 48\times48\text{px}$, and Real-State engineering. |
| **2. Security (AppSec & AI)** | Secrets exclusively in `.env` (clean `.env.example` when env vars exist + strict `.gitignore`), boundary schema validation (`Pydantic v2` `extra="forbid"`, `Zod .strict()`, Go `DisallowUnknownFields()`), anti-XSS sanitization, and Zero-Trust isolation against Prompt Injection in tools and agents. |
| **3. Temporal Baseline** | Active runtimes & SDKs grounded in session context and official docs/MCP: Python `3.12+` (`uv`), `google-genai>=3.3.0`, `@google/genai>=3.3.0`, `google.golang.org/genai>=1.77.0` (Gemini 4 family — `gemini-4-hydrogen`, `gemini-4-argon`, `gemini-4-carbon`, Decisions `gemini-decision-1`, Live `gemini-3.8-live`), `google-adk>=2.14.1` / `adk-go>=2.7.1`, `FastMCP` / MCP Spec `2026-07-28`, `a2a-sdk` `1.0+` (JCS/JWS), TS `5+` / Node LTS, Go `1.24+`. Conditional lookup via `google-developer-knowledge` / `gemini_get_doc` (`aistudio.google.com/llms.txt`). |
| **4. Real-Code AST Quality** | Mandatory source-code inspection (`project_structure_and_code_auditor.py` + `deterministic_scorer.py`): cohesive modularity (functions $\le 60$ lines, McCabe $M \le 10$), strict typing, ban on bare `except:` or placebo stubs (`pass`, `...`, `onClick={() => {}}`), and zero orphan files across Python, TS/JS, and Go packages. |
| **5. Physical Tree, Navigation & Components** | Clean root (`README.md`, `AGENTS.md`, `.context/spec.md`, `.context/context.md` — advisory on `1–4` file micro-repos; `CURRENT_STATE.md` / `rules/` for skill catalogs), right-sized package separation without empty speculative layers, and UI tab governance when `has_ui_layer == True`. |
