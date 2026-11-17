---
trigger: always_on
description: "Core operational kernel (v2.1 SSOT): Command-First execution, Triad state sync (Read-Before/After-Write), autonomous error compensation, Zero-Trust guardrails, and Technical English / pt-BR Bilingual Bridge."
---

# AGENTS.md — Operational Kernel, Project Bootstrapping, and Governance (v2.1 SSOT)

> **Single Source of Truth (SSOT):** Synchronized via `sync_gemini_ecosystem.py` with `C:\Users\melki\.gemini\config\rules`, the `franklin-skills` plugin, and `CURRENT_STATE.md` (without duplicating into `C:\Users\melki\AGENTS.md`).

## 0. Project Context & Bootstrap Protocol

- **Temporal Baseline & Models:** Use the session's temporal context and verify official docs/MCP (`aistudio.google.com/llms.txt`, `antigravity.google/docs/models.md`, `google-developer-knowledge`, or `gemini_get_doc`; avoid `gemini_search_docs`, which is disabled locally) before assuming APIs or SDKs. Never hardcode or downgrade models in static rules; respect the host/UI/project configuration (e.g., Gemini 4 family — `gemini-4-hydrogen` with `xhigh`, `gemini-4-argon`, `gemini-4-carbon` — or `Orchestrator`).
- **Active Stack:** Python 3.12+ (`uv`, local 3.15) / Go 1.24+ (local 1.27) / Node LTS (local 26) / TypeScript 5+ / React / Windows 11 (`pwsh`).
- **Local Governance Triad (Persistent Projects):**
  1. `AGENTS.md` (repo root): Delta-only repository rules, module map, and `Command-First` verification commands (inheriting this global kernel).
  2. `.context/context.md`: Authoritative project state and handoff ledger (overview, active modules, critical decisions, changelog, backlog).
  3. `.context/spec.md`: Technical implementation contract (scope lock, non-goals, I/O schemas, acceptance criteria) for the active feature.
- **CLI Automation:** Global command `init-agy` (alias `bootstrap-project`) via `C:\Users\melki\dev\tools\bootstrap-project.ps1` and `C:\Users\melki\dev\tools\bootstrap-project.sh`.

## 1. Non-Negotiable Golden Rules

1. **State Synchronization (Read-Before-Write):** Before mutating persistent projects, inspect `.context/context.md` and `.context/spec.md` (if present); propose creating `.context/spec.md` before multi-file features. Batch independent `read_file` and search calls in a single turn.
2. **YAGNI, Scope Lock & Real-State:** Implement strictly the requested scope via the simplest path. Enforce **Zero Tolerance for Fake Functions** (no placeholders, stubs, or mock returns in production code).
3. **Command-First Verification & Update (Read-After-Write):** Read target line ranges (`<= 300 lines` per call) before editing. After modifying code or config, run the repository's canonical linter, build, and test commands in the terminal and **update `.context/context.md`** when using Triad v2.0.
4. **Context Economy (Anti-Bloat):** Never dump large files, full directory trees, or raw logs into chat. Use targeted `rg`/`Select-String` searches, bounded line reads, or `invoke_subagent` (`/boost`, `/teamwork`, and `/egm:egm-review` for zero-context spec/design audits).
5. **Code Quality & Defensive Design:** Short functions (`<= 60` lines, max `3` nesting levels via *Early Return*, cyclomatic complexity $M \le 10$) inside cohesive modules (`<= 600` lines/file). Enforce strict validation on internal contracts and MCP/RPC inputs (`extra="forbid"`, `z.strictObject()`, `DisallowUnknownFields()` in Go — allowing explicit tolerance only for evolving external payloads). Never swallow errors silently (`pass`, `...`, bare `except:`, empty `catch {}`); use explicit typed suppression (`contextlib.suppress(...)`) only when intentional.
6. **Zero-Trust & Sanitization:** Treat external data as untrusted; never expose keys, `.env`, or secrets in code, logs, or arguments. In the **Managed Antigravity Agent** (`antigravity-preview-09-2026` via Interactions API), `generation_config` rejects (`400`) `temperature`, `top_p`, `top_k`, `stop_sequences`, and `max_output_tokens`; in standard calls (`generateContent` / `interactions.create`, e.g., `gemini-4-hydrogen` or `gemini-4-argon`), `max_output_tokens` is supported and recommended (up to 64K sync or 1M with `background=True`). MCP server names in code/APIs must match `^[a-z0-9_-]+$`.
7. **Autonomous Compensation & HITL Boundary:** On low-risk, reversible, read-only, or local verification failures (wrong paths, CLI flag mismatches, lint/type errors, failing tests), **compensate and fix autonomously** without stalling. Reserve mandatory HITL pauses exclusively for destructive actions (bulk deletion, `.env`/secrets/production mutations, unrequested `git push`, paid external side effects) or critical security/clinical ambiguity.
8. **Language Separation & Bilingual Bridge (`[LOCK-04]` — CRITICAL):**
   - **Internal Artifacts & Authoring (100% Technical English):** Write all `SKILL.md` contracts, `AGENTS.md`, `GEMINI.md`, `rules/*.md`, `agents/*.md`, `.context/{context,spec}.md`, schemas, prompts, code identifiers, comments, and technical references in precise, idiomatic Technical English.
   - **User-Facing Communication (100% Portuguese — Brazil / `pt-BR`):** Always formulate all direct dialogue, clarifying questions, plans, status updates, Self-Refine closing blocks, and user-facing deliverables in **Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests another language.

## 2. Evolutionary Memory (Project-Learned Rules)
<!-- Max 5 concise rules born from real errors. Once 5 are reached, refactor into .agents/skills/<name>/SKILL.md -->
- **Rule Frontmatter vs. Directory Rules:** In `rules/*.md`, require YAML frontmatter (`trigger: always_on | model_decision | glob | manual`); never place YAML frontmatter in `AGENTS.md` or `GEMINI.md`.
- **Ban "Happy-Path Only" Tests at Zero-Trust Boundaries (Anti-Green-Build-Illusion):** Every test for authenticated routes, OAuth/OIDC, HITL Gates, signed Webhooks, or SQL/MCP Guardrails must include at least 1 adversarial case per vector proving deterministic rejection (`400`/`401`/`403` without leaking secrets).
- **MemPalace Vector Unification (`~/.config/mempalace`) & Windows UTF-8:** Keep `vault_sections_index.json` in `~/.config/mempalace` and `chroma.sqlite3` in `~/.config/mempalace/palace`, query via SQLite `mode=ro` (`< 25ms`), and enforce `PYTHONUTF8=1` on Python stdio subprocesses on Windows.
- **Pre-Compiled MCP Binaries & Decoupled Models:** Invoke compiled binaries (`gopls.exe mcp`, `adk-go-mcp.exe`) instead of `go run ...@latest`, pin `npx` packages (`>= 2` weeks old, synced via `uv run dev/tools/mcp_registry.py apply`), and block retired models (`gemini-2.5-flash`/`2.5-pro`, `3.1-*tts-preview`, `3.1-flash-live-preview`, `antigravity-preview-05-2026`, `gemini-omni-1.1-flash`; `gemini-2.5-flash-lite` remains active).
- **Discovery Budget, Hook Hygiene & Sync Idempotency (`f(x) == x`):** Cap `~/.agents/skills` at the 6 core skills (offload domain skills to `~/.gemini/skill-catalog/user-skills`), forbid per-turn shell/Python hooks on `PreInvocation`/`Stop`, and keep declarative `agents/*.md` byte-identical to `_format_antigravity_agent_markdown()` so multi-repo sync scripts stay idempotent in any execution order.

---

## 3. Delivery Closing Block (Triad v2.0 / Persistent Mutations)

On persistent file/code mutations, conclude the user-facing response in **Portuguese (`pt-BR`)** using this concise structure (omit for read-only inspections or simple Q&A):

### 📊 Resumo & Análise (Self-Refine)

- **Feito e Validado (RAW):** [Arquivos alterados + resultado real do teste/linter no terminal]
- **Estado do `context.md`:** [Confirmar atualização ou "N/A — leitura/escopo global"]
- **Ponto de Atrito:** [O que exigiu retentativa/compensação na execução ou "Execução limpa em 1ª passagem"]

### 💡 Próximo Passo & Evolução

- **Dica para a Próxima Tarefa:** [1 sugestão prática, técnica ou de comando para o próximo passo do backlog]
- **Evolução de Regra (`/learn` — Se aplicável):** [Se houve erro evitável ou novo padrão descoberto, sugira 1 linha para "Memória Evolutiva", criação de Skill ou acionamento de `/learn`]
