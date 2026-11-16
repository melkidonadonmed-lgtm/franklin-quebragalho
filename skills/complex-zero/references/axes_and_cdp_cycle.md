# The 4 Axes, Pre-Flight & ReAct/CDP Cycle — `complex-zero`

Extended reference consumed by [`../SKILL.md`](../SKILL.md), paired with [`react_devtools_and_xyflow_patterns.md`](react_devtools_and_xyflow_patterns.md) and `skills/agent-server-auditor/references/audit-websocket-jsonrpc.md`.

## 5 Blocked Structural Failures

1. **No Pseudo-ReAct (Real Chrome DevTools):** Requires `take_screenshot` + `take_snapshot` + `evaluate_script` (`getComputedStyle` and `getBoundingClientRect`) whenever an active `live_url` exists.
2. **Semantic Tab Governance (`Domain-Tab Separation` vs. `Anti-Duplicate-Tab`):** Primary tabs (`role="tab"`) may separate distinct domains, but strictly forbid: (a) duplicate-function tabs, (b) new tabs added while the primary tab remains messy, (c) exposing internal backend plumbing as tabs, and (d) nested sub-tabs (`switchSubview` inside `switchTab`) or `> 3` `<nav>` blocks.
3. **Monotonic Hierarchy (`Anti-Flat-Hierarchy`):** Blocks inline `style="font-size: 11px|12px"`; enforces $H_1 > H_2 > H_3 > \text{Body} \ge 14\text{px} > \text{Caption} \ge 12\text{px}$.
4. **Legible Menus (`Anti-Cramped-Menu`):** Blocks `font-size < 13px`, `gap < 6px`, `min-block-size < 40px`, or `scrollWidth > clientWidth`.
5. **Anti-Fake AST & Next.js 15+:** Blocks *Ghost Nodes*, `() => {}` handlers, `Math.random()` telemetry, hardcoded `'[PASS]'` tags, `> 2` metric badges per node card, and synchronous `params.slug` reads.

## Scoring Matrix (`25 pts` per Axis)

| Axis | Deterministic Criteria | Primary Penalty |
| :--- | :--- | :--- |
| **1. Interactivity, Fitts, INP & Menus (`25 pts`)** | Native elements, `:focus-visible`, `@media (any-pointer: coarse)` $\ge 48\text{px}$, `prefers-reduced-motion`, separate `transition-behavior: allow-discrete`, `content-visibility: auto`, menus `>= 13px`/`gap >= 6px`/`min-block-size >= 44px`. | `-15 pts` cramped menu; `-10 pts` missing `:focus-visible`. |
| **2. Tab Cohesion, Hierarchy & `OKLCH` (`25 pts`)** | `<= 3 <nav>`, zero duplicate/backend/sub-tabs, 1 Composer, monotonic type scale, `@container`, `oklch()`, and `[LOCK-02]` 3-layer shadows. | `-15 pts` invalid tabs or `<nav> > 3`; `-15 pts` inline micro-fonts. |
| **3. Real-State Graph & Anti-Fake AST (`25 pts`)** | Zero `{}` stubs/`Math.random()`/`'[PASS]'`; `@xyflow/react` 1:1 parity with disk, `150ms` batching, and `<= 2` badges/node. | `-15 pts` per placebo, node overstuffing, or *Ghost Node*. |
| **4. DevTools Probe & Next.js 15+ Routes (`25 pts`)** | `<title>`, `<meta name="viewport">`, `evaluate_script` probe, and `params: Promise<{ slug: string }>` via `await`/`use()`. | `-15 pts` DOM failure or sync `params.slug` access. |
