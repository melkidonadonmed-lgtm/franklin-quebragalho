# Deterministic Audit Criteria — `clinical-minimalist-ui` (`v5.0.0`)

Objective and falsifiable criteria (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for auditing clinical UIs, Electronic Health Records (EHR/PEP), medical calculators, and vector A4 print sheets.

---

## 1. Purpose-Driven Clinical Surfaces, Zenithal Lighting & Alert Semantics (`[DISC-PALETA]` / `AUDIT-VIS-01`)

- **`[PASS]`**: Adapts `--surface-canvas`, `--surface-sunken`, `--surface-card`, `--surface-elevated`, and `--surface-glass` to the care setting (`clinical-day` or `clinical-night`), applies `[LOCK-02]` zenith lighting (`--catch-light`) and 3-level multi-layer shadows (`--shadow-elevation-1..3` / `--elevation-1..3`), enforces WCAG AAA contrast on vital signs, keeps primary actions achromatic, and restricts critical allergy/alert accents to `6px` micro-dots, `2px` accent rules, or subtle tinted badges paired with high-contrast neutral text (`--ink-primary`).
- **`[FAIL]`** (`CLINICAL_CONTRAST_OR_SEMANTIC_VIOLATION`): Insufficient contrast on vital signs or dosages, blurry colored text over mid-gray backgrounds, flat single-pass shadows, or distracting neon/decorative color noise unfit for medical environments.
- **`[UNVERIFIED]`**: Clinical UI stylesheets or component files were not provided or are inaccessible on disk.

## 2. Anti-Blur Typography, Zero Emojis, Unbreakable Units & Vector A4 Sheet (`[DISC-TATIL]`)

- **`[PASS]`**: Applies `antialiased` + `font-synthesis: none`, zero fractional `scale()` on text containers, zero emoji characters (exclusively Lucide vector icons `stroke-width="1.5"` to `"1.75"`), `>= 44x44px` interactive targets with `anti-squish` shielding (`flex-shrink: 0; white-space: nowrap` protecting `mg/dL`, `mL/min`, `mEq/L`), doses/labs in `IBM Plex Mono` / `JetBrains Mono` with `font-variant-numeric: tabular-nums`, and a 100% vector CSS Grid + SVG `@media print` A4 sheet (`210mm × 297mm` `.sus-grid`) with shadows and sidebars removed during print.
- **`[FAIL]`** (`CLINICAL_EMOJI_OR_MISALIGNMENT`): Any emoji inside buttons/badges, fractional `scale()` on text, line-wrapping across medical measurement units, missing `tabular-nums` on numeric tables, or missing vector `@media print` rules on prescription/report screens.

## 3. Deterministic Calculation Delegation & Real-State Engineering (`[DISC-OPCOES]` & `AUDIT-STATE-01`)

- **`[PASS]`**: Medical formulas (renal clearance, infusion rates, electrolyte correction) run inside typed, tested deterministic functions (or `agy_deterministic_calc_suite`), inputs validate physiological bounds with `role="alert" aria-live="assertive"`, zero placebo controls exist, and the project achieves `Verdict: PASS` (`readiness_score >= 90.0`) via `skills/frontend-testing-auditor/scripts/audit_tactile_ui.py`.
- **`[FAIL]`** (`CLINICAL_RISK_OR_MISSING_FSM`): Dosing math delegated to free-form LLM generation, non-functional placebo controls, absent physiological range guardrails, or failure in `audit_tactile_ui.py`.
