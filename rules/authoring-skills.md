---
trigger: glob
globs: "**/SKILL.md, **/evals/evals.json"
description: "Load when creating, refactoring, auditing, or validating Agent Skills (SKILL.md frontmatter, Progressive Disclosure L1-L3, references/, scripts/, evals/evals.json, skills.json, validate_skills.py, or migrating legacy .agents/workflows/*.md). Do NOT load when merely activating or running an existing skill."
---

# Official Guidelines for Authoring Agent Skills (Antigravity / agentskills.io)

1. **Discovery & Canonical Locations:**
   - Workspace: `.agents/skills/<skill-name>/SKILL.md` (or `_agents/skills/`); always author skills instead of legacy `.agents/workflows/*.md` (deprecated in Antigravity 2.12+).
   - Global/Plugin: `~/.gemini/config/skills/<skill-name>/SKILL.md` or `plugins/<plugin>/skills/<skill-name>/SKILL.md` (use `skills.json` `entries`/`inherits` only for non-standard directories, avoiding duplication of globally active skills).

2. **Language Separation & Bilingual Bridge (MANDATORY):**
   - **Internal Logic (100% Technical English):** Write every `SKILL.md` (YAML frontmatter + Markdown body), `rules/audit_criteria.md`, and `references/*.md` in concise, standardized Technical English.
   - **User Interaction (100% Portuguese — Brazil / `pt-BR`):** Every `SKILL.md` MUST include `## 6. User Communication Rule` requiring all user-facing conversation, status reports, and deliverables to be communicated in **Portuguese (`pt-BR`)**, unless the user explicitly asks otherwise.

3. **Strict YAML Frontmatter (L1 — Semantic Discovery):**
   - Required fields: **`name`** (`^[a-z0-9]+(-[a-z0-9]+)*$`, `<= 64` chars, **identical to folder slug**) and **`description`** (`1-1024` chars, ideally `<= 420`, imperative 3rd-person Technical English stating **WHAT** it does, **WHEN** to use it, and explicit negative exclusion `"Do not use for ... (use <other-skill> instead)."`).
   - Wrap `description` in double quotes (`"..."`) or folded block (`>-`) whenever `: ` appears to prevent PyYAML parsing errors.
   - Optional fields: `compatibility`, `license`, and `metadata:` (`version` SemVer `X.Y.Z`, `updated_at`, `author`, `category`, `tags` with bilingual EN + PT-BR trigger keywords). **Never duplicate** `version`, `updated_at`, or `allowed-tools` at the top level when `metadata:` is present (`validate_skills.py --strict` rejects orphan top-level keys).

4. **3-Tier Progressive Disclosure & Self-Containment (L1 -> L2 -> L3):**
   - **L2 (`SKILL.md`):** Keep body concise (`<= 1,000` tokens, `< 100` lines, hard cap `< 500` lines) with defaults instead of ambiguous menus, concrete **Gotchas & Edge Cases**, and these 6 canonical sections:
     1. `## 1. Overview & Scope` (`When to Use` / `When NOT to Use`)
     2. `## 2. Inputs & Prerequisites`
     3. `## 3. Step-by-Step Procedure`
     4. `## 4. Gotchas & Edge Cases`
     5. `## 5. Output Schema & Validation Criteria`
     6. `## 6. User Communication Rule`
   - **L3 (`references/`, `scripts/`, `rules/`, `evals/`):** Offload heavy matrices, schemas, and checklists to `references/*.md` and deterministic code to `scripts/`. Use **one-level relative paths only** (`references/guide.md`, `scripts/run.py`, `rules/audit_criteria.md`) — parent escapes (`../` or `../../`) are strictly forbidden.
   - **Third-Party Skills (`npx skills`, Orca, external plugins):** Treat as strictly **read-only**; update only via their upstream installer.

5. **Evals & Deterministic Validation Gates:**
   - Include `evals/evals.json` (`{"skill_name": "...", "evals": [...]}`) containing at least 2 positive (`"should_trigger": true`) and 2 near-miss negative (`"should_trigger": false`) cases alongside functional assertions.
   - Validate physically before completing: `uv run python scripts/validate_skills.py --strict --ecosystem` (must exit `0` with zero broken links, zero `../` escapes, and zero Jaccard trigger collisions).
