---
name: frontend-testing-auditor
description: "Use this skill when auditing web UI quality with audit_tactile_ui.py, Jest, Axe-Core, or Playwright for WAI-ARIA, Real-State FSM, zero emojis, Base64 bloat, OKLCH, and anti-XSS. Do NOT use for implementing UI components or backend-only unit tests."
metadata:
  author: "Franklin"
  version: "5.0.0"
  updated_at: "2026-11-16"
  tags: ["frontend-testing-auditor", "audit_tactile_ui", "wai-aria", "axe-core", "wcag", "a11y", "acessibilidade", "oklch", "fsm", "xss", "anti-xss", "bloat-base64", "zero-emojis", "qualidade-interfaces"]
---

# `frontend-testing-auditor` — Deterministic Frontend QA & Gatekeeper

## 1. Overview & Scope

Deterministic QA pipeline pairing `jest-axe` / Vitest / Playwright test suites with [scripts/audit_tactile_ui.py](scripts/audit_tactile_ui.py), aligned with `rules/frontend-9-axes-guidelines.md` and `design-md`.

- **When NOT to Use:** Do not use for backend-only Python/Go/SQL unit tests without a DOM, scaffolding components (`frontend-code-architect`, `design-md`), or live CDP graph audits (`complex-zero` / `system-project-auditor`).

## 2. Inputs & Prerequisites

- **`target_path` (required):** `src/` folder (Tiers 2/3) or `.html`/`.tsx`/`.css` file (Tier 1).
- **`design_contract` (optional) & Gatekeeper:** `<project_root>/DESIGN.md` and [scripts/audit_tactile_ui.py](scripts/audit_tactile_ui.py) (`--target <path> --json`).

## 3. Step-by-Step Procedure

Consult [references/audit_4_pillars_matrix.md](references/audit_4_pillars_matrix.md) and [references/a11y_fsm_rubric.md](references/a11y_fsm_rubric.md):

1. **Run Zero-LLM Gatekeeper:** Execute `uv run python skills/frontend-testing-auditor/scripts/audit_tactile_ui.py --target "<target_path>" --json` (strips `//` and `/* */` comments prior to scanning).
2. **Pillar 1 — `AUDIT-A11Y` (`35%`):** Check 0 `axe-core`/WCAG AA violations, `:focus-visible`, `tabular-nums`, DOM = Tab order, adaptive Bottom Bar $\leftrightarrow$ Sidebar Rail, `any-pointer: coarse` $\ge 48\text{px}$, separate `transition-behavior: allow-discrete`, and `prefers-reduced-motion`.
3. **Pillar 2 — `AUDIT-STATE` (`30%`):** Verify executable FSM (`idle | loading | empty | error | pressed`) via `data-state`, `data-theme`, `data-variant`, `aria-busy`, `role="status"`/`"alert"`, rejecting placeholders and comment-gaming (`-25 pts`).
4. **Pillar 3 — `AUDIT-VIS-01` (`20%`):** Verify 3-layer `OKLCH`/`light-dark()` tokens, `[LOCK-02]` 3-level shadows (`--shadow-elevation-1..3`, `--catch-light`), zero orphan `SoftCard`/`SurfaceCard` (`-25 pts`), zero UI emojis, and zero Base64 `> 50 KB`.
5. **Pillar 4 — `AUDIT-SEC` (`15%`):** Enforce `DOMPurify.sanitize()` (except static `data-theme` FOUC script) and zero `eval()`, authoring RTL + `jest-axe` tests with adversarial XSS assertions.

## 4. Gotchas & Edge Cases

- **Defaults Over Menus:** Pass `--json` automatically and co-locate `*.test.tsx` suites next to components.
- **Anti-Gaming & Thresholds:** Reject comment-gaming (`// empty | loading | success | error`) and orphan cards; never pass if `s_tokens < 85.0` or `s_fsm < 85.0`.
- **Stop Criteria:** Stop with `verdict: "UNVERIFIED"` if no `.tsx`/`.jsx`/`.vue`/`.html`/`.css` files exist in `target_path`.

## 5. Output Schema & Validation Criteria

Compute $\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$. `Verdict: PASS` per [rules/audit_criteria.md](rules/audit_criteria.md) requires **`readiness_score >= 90.0`**, **`s_tokens >= 85.0`**, and **`s_fsm >= 85.0`**.

## 6. User Communication Rule

Always formulate all direct user-facing conversation, explanations, clarifying questions, status reports, and deliverables in Portuguese (Brazil / pt-BR), unless the user explicitly requests otherwise.
