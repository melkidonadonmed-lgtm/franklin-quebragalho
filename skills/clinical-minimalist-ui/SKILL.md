---
name: clinical-minimalist-ui
description: "Use this skill when designing or building clinical interfaces, electronic health records (EHR/PEP), A4 vector print sheets (.sus-grid), and medical calculators. Do NOT use for generic SaaS, e-commerce, or non-clinical dashboards."
metadata:
  author: "Franklin"
  version: "5.0.0"
  updated_at: "2026-11-16"
  tags: ["clinical-minimalist-ui", "clinical-ui", "medtech", "ehr", "pep", "prontuario-eletronico", "interfaces-clinicas", "receituarios-laudos", "sus-grid", "a4", "calculadoras-medicas", "oklch", "tabular-nums"]
---

# `clinical-minimalist-ui` — Clinical Interfaces & Vector A4 Print Architecture

## 1. Overview & Scope

Ergonomic and patient-safety UI architecture aligned with `rules/frontend-9-axes-guidelines.md` and `design-md` for EHR/PEP screens, prescriptions, ICU monitoring, deterministic medical calculators (`SOFA`, `CHA2DS2-VASc`, `CKD-EPI`), and 100% vector CSS Grid + SVG `@media print` A4 sheets (`210mm × 297mm` `.sus-grid`).

- **When NOT to Use:** Do not use for generic SaaS, fintech, crypto, e-commerce, or gaming UIs (`design-md`, `frontend-code-architect`, or `system-project-auditor`).

## 2. Inputs & Prerequisites

- **`clinical_context` (required) & `target_stack` (optional):** `outpatient_ehr` | `icu_night_shift` | `dosing_calculator` | `a4_prescription_sheet`; React/TS + Tailwind v4/CSS Variables or standalone HTML5/CSS3.
- **Deterministic Math Mandate:** Delegate dosing, infusion, and clearance math to typed deterministic functions or `agy_deterministic_calc_suite` — never free-form LLM output.

## 3. Step-by-Step Procedure

Consult [references/clinical_polarities_architecture.md](references/clinical_polarities_architecture.md) and [references/clinical_a4_tokens_guide.md](references/clinical_a4_tokens_guide.md):

1. **Clinical `OKLCH` Polarities & `[LOCK-02]` Elevation:** Apply `clinical-day` (`--surface-canvas` `L=0.97` to `--surface-card` `L=1.00`, WCAG AAA $\ge 14:1$) or `clinical-night` (`0.16 -> 0.21 -> 0.26`, zero `#000000`), 3-level shadows (`--shadow-elevation-1..3` + `--catch-light`), `--shadow-inset-sunken`, achromatic CTAs, 4 card variants, and contained alerts (`6px` dot / `2px` border + `--ink-primary`).
2. **Logical Box, GPU Sharpness & Unbreakable Units:** Enforce logical CSS, `antialiased`, `font-synthesis: none`, zero fractional `scale()` on text, **zero emojis** (Lucide `stroke-width: 1.5..1.75` only), `tabular-nums`, and `anti-squish` (`white-space: nowrap; flex-shrink: 0`) on units (`mg/dL`, `mL/min/1.73m²`, `mEq/L`) with `>= 44x44px` targets.
3. **Archetypes, `@container` & A4 `.sus-grid`:** Use *Workbench Split-View* or *Command Center* with `@container`, 3-layer nav, physiological range alerts (`role="alert" aria-live="assertive"`), and `@media print` stripping `.no-print`/`nav`/`aside` and shadows.

## 4. Gotchas & Edge Cases

- **Defaults Over Menus:** Infer `clinical_context` directly (ICU defaults to `clinical-night`; prescriptions default to `clinical-day` + A4 `@media print`).
- **Patient-Safety Stop Criteria:** Halt if deterministic formulas or physiological bounds are missing; never emit low-contrast colored alert text, UI emojis, or flat 1-layer shadows.

## 5. Output Schema & Validation Criteria

Deliver typed clinical components (`.tsx`/`.html`) with Real-State FSM, deterministic dosing helpers, and vector `@media print` A4 CSS validated against [rules/audit_criteria.md](rules/audit_criteria.md) and `frontend-testing-auditor` (`audit_tactile_ui.py` `Readiness >= 90.0`).

## 6. User Communication Rule

Always formulate all direct user-facing conversation, explanations, clarifying questions, status reports, and deliverables in Portuguese (Brazil / pt-BR), unless the user explicitly requests otherwise.
