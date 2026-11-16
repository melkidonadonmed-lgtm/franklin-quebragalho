# REA UI/UX Stages & Detailed Criteria — `plan-uiux`

Reference for the 4 REA stages and optical standards consumed by [`../SKILL.md`](../SKILL.md), complementing [`mutation_patterns.md`](mutation_patterns.md).

## 4-Stage REA UI/UX Workflow

```text
[1. REA EXTRACTION]         ──► Run analyze_javascript_application / inspect_go_binary
              │
              ▼
[2. SUMMARY VIEW]           ──► Filter graphs via inspect_analysis_view (detail: summary)
              │
              ▼
[3. BENCHMARK & CLAREZA]    ──► Cross-check evidence against OKLCH, 60-30-10 & A11y rules
              │
              ▼
[4. MUTATION PROPOSAL]      ──► Emit structured plan with Before vs. After code blocks
```

## Verified Technical Standards

1. **REA Collection:** `analyze_javascript_application` / `inspect_go_binary` -> `parent_evidence_id` -> `inspect_analysis_view(kind="javascript-routes" | "javascript-facts" | "api-surface", detail="summary")`, augmenting live web targets with `inspect_web_page`, `capture_web_screenshot`, and `compare_web_screenshots` (isolating `_meta.provenance.untrusted_content == true`).
2. **Colors & `60-30-10` (`OKLCH`):** `oklch(L C H)` allocated across 60% Canvas, 30% Structural Surfaces, and 10% Focal Accents.
3. **`[LOCK-02]` 3-Layer Physical Elevation & Dark Mode:** Contact Umbra + negative-spread Penumbra + Zenithal Catch-Light (`--shadow-elevation-1..3` / `--shadow-elevation-low/medium/high`) with progressive lightness $L$ (`0.16 -> 0.22 -> 0.27`).
4. **Responsiveness, Cards & Navigation:** `@container` isolated from `subgrid`, `--space-*` / `--space-card-padding` / `--space-grid-gap`, concentric radii $R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$, `flex-wrap: balance`, `clamp()` ($\max \le 2.5\times \min$), `max-inline-size: 60ch–65ch`, `tabular-nums`, Single-DOM Nav (`env(safe-area-inset-bottom)` $\leftrightarrow$ `240px` Sidebar Rail), and `48x48px` targets under `any-pointer: coarse`.
