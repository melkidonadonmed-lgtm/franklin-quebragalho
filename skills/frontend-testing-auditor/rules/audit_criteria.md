# Deterministic Audit Criteria — `frontend-testing-auditor` (`v5.0.0`)

Objective and falsifiable criteria (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for the deterministic frontend testing gatekeeper (`scripts/audit_tactile_ui.py` + Jest/Vitest + Axe-Core) under the **9-Axis SSOT** (`rules/frontend-9-axes-guidelines.md`).

---

## 1. Zero-LLM Execution of `scripts/audit_tactile_ui.py` (`[AUDIT-GATE-01]`)

- **`[PASS]`**: `scripts/audit_tactile_ui.py` executes with zero external network dependencies, strips comments (`//` and `/* */`) before static inspection, and enforces `readiness_score >= 90.0`, `s_tokens >= 85.0`, and `s_fsm >= 85.0` to emit `Verdict: PASS`.
- **`[FAIL]`** (`SIMULATED_AUDIT`): Reporting a subjective visual verdict without executing `audit_tactile_ui.py`, or passing code with `readiness_score < 90.0`.
- **`[UNVERIFIED]`**: No `.tsx`, `.jsx`, `.vue`, `.html`, or `.css` files found inside the target directory.

## 2. 4-Pillar Deterministic Coverage & Weighted Rubric (`[AUDIT-GATE-02]`)

- **`[PASS]`**: Computes exactly $\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$ covering:
  - `AUDIT-A11Y-01/02` (`35%`): 0 `jest-axe` WCAG 2.1 AA violations, `:focus-visible`, `aria-live`, conditional Breadcrumbs (`role="list"` + `aria-current="page"` in hierarchies $\ge 3$ levels), `tabular-nums`, `antialiased` + `font-synthesis: none`, and `prefers-reduced-motion`.
  - `AUDIT-STATE-01/02` (`30%`): Executable finite state machine (`data-state`, `data-theme`, `data-variant`, `aria-busy`, `role="alert"` / `role="status"`).
  - `AUDIT-VIS-01` (`20%`): 3-layer semantic token families (`--bg-canvas`/`--bg-surface-1`/`--text-primary` or `--surface-canvas`/`--surface-card`/`--ink-primary` in `oklch()` / `light-dark()`), `[LOCK-02]` zenithal light and 3-level multi-layer shadows (`--shadow-elevation-1/2/3`, `--elevation-1/2/3`, `--shadow-inset`, `--catch-light`), zero emojis, zero Base64 `> 50 KB`, and zero orphan components in `src/components/ui/`.
  - `AUDIT-SEC-01` (`15%`): Rejects unsanitized `dangerouslySetInnerHTML` without `DOMPurify` (sole exception: static synchronous anti-FOUC `data-theme` script) and all `eval()` calls.
- **`[FAIL]`** (`INCOMPLETE_SUITE`): Omitting any of the 4 weighted dimensions or lacking adversarial anti-XSS test assertions.

## 3. Anti-Placebo & Anti-Comment-Gaming Detection (`[AUDIT-GATE-03]`)

- **`[PASS]`**: Automatically penalizes (`-25 pts`) comment-gaming stubs like `// empty | loading | success | error` and unconsumed `SoftCard.tsx`/`SurfaceCard.tsx` components orphaned in `src/components/ui/` (`-25 pts`).
- **`[FAIL]`** (`FALSE_POSITIVE_GAMING`): Accepting static comments as proof of finite state machine execution.
