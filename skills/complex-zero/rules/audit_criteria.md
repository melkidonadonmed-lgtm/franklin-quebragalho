# Deterministic Audit Criteria — `complex-zero` (`v3.1.0`) integrated with `system-project-auditor`

Objective and falsifiable criteria (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for empirical ReAct auditing (Visual Screenshot + Chrome DevTools MCP/CDP DOM Probe + Static AST), semantic domain-tab governance (blocking duplicate tabs, sprawl over messy primary tabs, nested sub-tabs, and exposed backend plumbing tabs), monotonic visual hierarchy, menu decompression, and complex UI engineering (`@xyflow/react`, `150ms` `WebSocket` batching, `OKLCH`, `[LOCK-02]` 3-layer shadows, `@container`, and Next.js 15+ App Router).

---

## 1. Axis 1: Semantic Interactivity, Focus Flow, Fitts' Law & Menu Decompression (`25 pts` — `[AUDIT-CZ-01]`)

- **`[PASS]`**: Interactive controls use native HTML elements (`<button>`, `<a>`, `<input>`, `<nav>`), preserve DOM Order = Visual Order, apply LVHA link states, declare `:focus-visible`, honor `@media (prefers-reduced-motion: reduce)`, enforce visible touch targets `>= 44x44px` (`>= 48x48px` under `@media (any-pointer: coarse)`), and **keep menus/tabs/buttons decompressed (`font-size >= 13px`, `gap >= 6px`, `padding >= 8px 12px`, `scrollWidth <= clientWidth`)**.
- **`[FAIL]`** (`CRAMPED_MENU_OR_FITTS_VIOLATION`): Cramped menus/buttons with `font-size < 13px`, `<nav>`/`.mode-switcher` bars with `gap < 6px`, targets with `min-block-size < 40px` or `padding: 4px 8px` (`-15 pts`), `<div onClick>` without `role`/`tabIndex` (`-5 pts`), or global focus suppression (`outline: none` without `:focus-visible`, `-10 pts`).
- **`[UNVERIFIED]`**: No interactive controls present in the evaluated scope.

## 2. Axis 2: Domain-Tab Cohesion, Visual Hierarchy, `@container` & `OKLCH` (`25 pts` — `[AUDIT-CZ-02]`)

- **`[PASS]`**: Respects the **3-Layer Navigation ceiling (`<= 3` `<nav>` tags)**, allows primary tabs (`role="tab"`) to separate distinct domains only when the **primary tab is clean**, guarantees **zero duplicate-function/duplicate-label tabs**, **zero internal backend plumbing tabs** (`sql_raw`, `db_pool`, `worker_queue`, etc.), **zero nested sub-tabs inside tabs**, **1 single Chat Composer/Command Bar**, monotonic typographic hierarchy ($H_1 > H_2 > H_3 > \text{Body} \ge 14\text{px} > \text{Caption} \ge 12\text{px}$), zero inline `style="font-size: 11px/12px"` clutter, `@container` (`container-type: inline-size`), `oklch()` tokens ($L = 0.16 \to 0.22 \to 0.27$) with `[LOCK-02]` 3-layer shadows, and `tabular-nums`.
- **`[FAIL]`** (`DUPLICATE_TAB_BACKEND_LEAK_OR_HIERARCHY_VIOLATION`): Duplicate tabs, adding extra tabs without cleaning the primary tab, exposing backend internals in tabs, nested sub-tabs, or `> 3` `<nav>` blocks (`-15 pts`), competing chat inputs (`-15 pts`), flattened visual hierarchy from inline `11px/12px` micro-fonts (`-15 pts`), missing `@container`/`oklch()` (`-10 pts`), or hardcoded contrast flags (`oklchContrastValid: true`, `-15 pts`).

## 3. Axis 3: Real-Time Reactive Graph (`@xyflow/react`), Clean Nodes & Anti-Fake AST (`25 pts` — `[AUDIT-CZ-03]`)

- **`[PASS]`**: Uses the modern `@xyflow/react` package (or an isolated 2D canvas with viewport `>= 520px`), `WebSocket` + `chokidar` with `150ms` batching (`BATCH_UPDATE`), `1:1` parity between graph nodes and physical files on disk (`fs.existsSync` confined against Path Traversal), zero empty functions (`{}`), zero stubs (`console.log`/`alert`), zero UI emojis, **zero statically hardcoded `'[PASS]'` strings inside nodes**, and **at most 2 compact badges per node** (delegating extended telemetry to the lateral inspector panel).
- **`[FAIL]`** (`GHOST_NODE_PLACEBO_OR_OVERSTUFFING`): Ghost nodes pointing to nonexistent files (`-15 pts`), empty handlers/stubs (`-15 pts`), faked `Math.random()` telemetry (`-15 pts`), hardcoded `'[PASS]'` node badges (`-15 pts`), or overcrowded `.metric-badge` elements crammed inside node cards (`-8 to -15 pts`).

## 4. Axis 4: Chrome DevTools Visual Inspection (Screenshot + DOM Probe) & Next.js 15+ Async (`25 pts` — `[AUDIT-CZ-04]`)

- **`[PASS]`**: Executes the Chrome DevTools MCP protocol (`take_screenshot` + `take_snapshot` + `evaluate_script` via `--dump-cdp-script`) verifying monotonic visual hierarchy and zero cramped menus in the rendered DOM, complete page metadata (`<title>`, `<meta name="viewport">`, `<meta name="description">`), and in Next.js 15+ App Router routes, `params: Promise<{ slug: string }>` consumed via `await params` or `React.use(params)`.
- **`[FAIL]`** (`LIVE_DOM_OR_SYNC_PARAMS_VIOLATION`): Runtime DOM/metadata probe failure (`-10 to -15 pts`) or legacy synchronous access to `params.slug` / `searchParams` without `await` or `use()` in Next.js 15+ (`-15 pts`).
