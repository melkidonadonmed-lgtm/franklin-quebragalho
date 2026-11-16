# Deterministic Audit Criteria — `plan-uiux` (`v1.2.0`)

Objective and falsifiable criteria (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for REA-backed UI/UX audits and Before/After mutation planning.

---

- **`[PASS]`**: Static/runtime evidence gathered via `analyze_javascript_application` / `inspect_go_binary` (or `inspect_web_page` + `capture_web_screenshot`) and filtered through `inspect_analysis_view(detail="summary")` without loading raw minified bundles.
- **`[PASS]`**: `OKLCH` color tokens enforce the `60-30-10` ratio, `[LOCK-02]` 3-layer shadows (`--shadow-elevation-1..3` + `--catch-light`), `@container` isolated from `subgrid`, concentric radii, and `48x48px` touch targets under `any-pointer: coarse`.
- **`[FAIL]`**: Missing epistemic separation (`[OBSERVED FACT]`, `[TECHNICAL INFERENCE]`, `[UNCERTAINTY / GAP]`) or omission of concrete `Before vs. After` code mutation blocks.
- **`[FAIL]`**: Preserving flat 1-layer drop shadows, decorative UI emojis in controls, pure `#000000`, duplicate `<nav>` trees, or missing `:focus-visible` indicators.
- **`[UNVERIFIED]`**: Target compiled artifact, JS bundle, Go binary, or live URL is inaccessible to REA inspection.
