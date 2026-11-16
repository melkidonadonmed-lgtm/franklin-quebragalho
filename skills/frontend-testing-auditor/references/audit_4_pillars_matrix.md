# 4 Deterministic Audit Pillars Matrix — Frontend Testing Auditor

Technical specification of checks enforced by [`../SKILL.md`](../SKILL.md) and [`../scripts/audit_tactile_ui.py`](../scripts/audit_tactile_ui.py), aligned with `rules/frontend-9-axes-guidelines.md` and [`a11y_fsm_rubric.md`](a11y_fsm_rubric.md).

## Pillar 1: Accessibility, Navigation, GPU Sharpness & `tabular-nums` (`AUDIT-A11Y` — 35%)

- **`[AUDIT-A11Y-01]` Axe-Core, Typography & Contrast:** Zero WCAG 2.1 AA violations ($\ge 4.5:1$); requires `antialiased`, `optimizeLegibility`, and `font-synthesis: none` on `html, body`, fluid `clamp()`, `max-inline-size: 65ch`, `text-wrap: balance/pretty`, banning fractional `scale()` on text and low-contrast text over mid-gray surfaces.
- **`[AUDIT-A11Y-02]` Single-DOM Navigation, Keyboard & Motion:** Reachable via `Tab` (`:focus-visible`), **DOM Order = Visual Order** (zero `row-reverse` in `<nav>`), Bottom Bar (`env(safe-area-inset-bottom)`) $\leftrightarrow$ Sidebar Rail (`240px` `100dvh`), single `<nav aria-label>`, `aria-current="page"` ($\ge 3:1$), Breadcrumbs `<ol role="list">` + `::before` ($\ge 3$ levels), `tabular-nums`, `@media (any-pointer: coarse)` targets $\ge 48\text{px}$ (`touch-action: manipulation`), separate `transition-behavior: allow-discrete` after `transition`, `content-visibility: auto`, and `prefers-reduced-motion`.

## Pillar 2: Real-State Engineering & FSM (`AUDIT-STATE` — 30%)

- **`[AUDIT-STATE-01]` Real Finite States (`idle | loading/active | empty | error | pressed`):** Expose `data-state`, `data-theme`, `aria-busy="true"`, `role="status"`/`role="alert"`, and real working controls (zero `setTimeout` placebos or `alert('Coming soon')`). Component and class names remain domain-flexible.
- **`[AUDIT-STATE-02]` Anti-Comment-Gaming:** Static comments mimicking states (`// idle | loading | error`) are stripped and penalized (`-25 pts`).

## Pillar 3: 3-Layer `OKLCH` Tokens, Shadows & Anti-Orphan (`AUDIT-VIS-01` — 20%)

1. Semantic tokens (`--bg-canvas`/`--bg-surface-1`/`--text-primary` or `--surface-canvas`/`--surface-card`/`--ink-primary` in `oklch()`/`light-dark()`) and Tier 1–3 architecture (`@layer`, `src/features/`, App Router `(groups)`/`_components/`).
2. `[LOCK-02]` Zenith lighting (`inset 0 1px 0 0` / `--catch-light`), 3-level multi-layer shadows (`--shadow-elevation-1/2/3` or `--elevation-1/2/3`), and sunken recess (`--shadow-inset` / `--sunken-recess`).
3. **Anti-Orphan (`-25 pts`), Zero Emojis (`AUDIT-VIS-EMOJI`) & Zero Base64 Bloat (`AUDIT-VIS-BLOAT` > 50 KB):** Fails unimported `Card.tsx`/`SurfaceCard.tsx`/`SoftCard.tsx`, UI emojis, and oversized inline Base64 data URIs.

## Pillar 4: Frontend Security (`AUDIT-SEC` — 15%)

- **`[AUDIT-SEC-01]` Anti-XSS:** Forbids `dangerouslySetInnerHTML` without `DOMPurify.sanitize()` (sole exception: static synchronous anti-FOUC `<head>` script reading `localStorage` for `data-theme`) and forbids `eval()`.
