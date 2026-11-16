# 4-Step Architecture & Operational Modules — `refine-prompt`

Complete processing flow consumed by [`SKILL.md`](../SKILL.md), complementing [`zero_trust_owasp_guidelines.md`](zero_trust_owasp_guidelines.md), [`epistemic_taxonomy.md`](epistemic_taxonomy.md), [`fluidity_and_low_entropy_engineering.md`](fluidity_and_low_entropy_engineering.md), [`modules_io_contracts.md`](modules_io_contracts.md), and [`master_system_prompt.md`](master_system_prompt.md).

## Epistemic & Entropy Audit Flowchart

```text
[Input in <untrusted_user_input>]
                 │
                 ▼
[Step 1: Zero-Trust Sanitization & Feasibility Verdict (2026)]
                 │
     ┌───────────┴───────────┐
     ▼                       ▼
[Feasible]          [Infeasible / Flawed] ──► [Emit [VERDICT] + Root Cause + Alternative]
     │
     ▼
[Step 2: Epistemic Classification ([FACT], [INFERENCE], [GAP]) + Entropy Regime]
     │
     ▼
[Step 3: Execute Module (1 / 2 / 3) + Fluidity / Low-Entropy Engineering]
     │
     ▼
[Step 4: Deterministic Gate (rules/audit_criteria.md & prompt_entropy_auditor.py)]
```

## Output Modules (`modules_io_contracts.md`)

- **Module 1 (Direct Resolution):** `1. EXECUTIVE SYNTHESIS & RESOLVED SOLUTION` + `2. METHODOLOGICAL NOTE & DECISION MATRIX`.
- **Module 2 (Plug-and-Play Artifact):** `1. ARTIFACT SCOPE & DIAGNOSTICS` + `2. COMPLETE CONTINUOUS ARTIFACT` (single uninterrupted block with `[VARIABLE_NAME]` placeholders) + `3. DEPLOYMENT & TRIGGER GUIDE`.
- **Module 3 (Socratic Interview):** `1. AMBIGUITY & RISK DIAGNOSTICS` + `2. SURGICAL KEY QUESTIONS (MAX 3 WITH A/B OPTIONS)` + `3. CONDITIONAL PRELIMINARY DRAFT`.

## Entropy Regimes

- **`COGNITIVE_FLUID`:** Open human interaction (*Why-First*, adaptive prose/table/list routing, zero forced mechanical templates).
- **`LOW_ENTROPY_CONTRACT`:** Repetitive operational routines and machine boundaries (strict contract, `[NOT PROVIDED: field]` / `missing_required_fields` escape tokens, and preliminary `"_pre_flight_check"` field before JSON output).
