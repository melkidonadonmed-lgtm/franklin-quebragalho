# Deterministic Audit & Rejection Criteria (`solution-content-architect` v2.5.0)

To prevent empty validations and fabricated compliance claims, every Mode D pre-delivery check MUST emit strictly one of these deterministic markers:

- `[PASS]`: Requirement verified against real input data, code, or consulted documentation anchors.
- `[FAIL]`: Requirement violated with an explicit, verifiable reason.
- `[UNVERIFIED]`: Cannot be verified due to missing inputs or reference context.

---

### Rule 1: Evidence Anchoring & Ban on Bibliographic Hallucination

- **Criterion**: When citing libraries, SDK methods, APIs, statistics, or architectural patterns, do all references exist in the target runtime or consulted documentation?
- **Test**: Are all APIs and dependencies verified against local manifests or official docs?
- **Result**:
  - Proven in input, codebase, or verified official docs -> `[PASS]`
  - Fabricated method, library, or unsupported statistic -> `[FAIL: Unverified or fabricated reference detected]`

---

### Rule 2: Media Prompt Completeness (`M5` & `M6`)

- **Criterion**: Were image or video generation prompts produced?
- **Test**: Is the final generation prompt written in English and complete with all **8 Visual Pillars** (Subject, Environment, Lighting, Composition, Style, Palette, Flags, Negative Constraints) for images, or **1 dominant action + 1 camera move** with temporal progression for video?
- **Result**:
  - Complete English prompt with all required pillars -> `[PASS]`
  - Non-English generation prompt or missing required visual pillars -> `[FAIL: Incomplete visual prompt pillars]`

---

### Rule 3: Clinical & Prescribing Integrity (`M7`)

- **Criterion**: Does the technical request involve clinical, medical, or pharmacological guidance?
- **Test**: Does the deliverable enforce PII/PHI anonymization, the 4-step causal chain, all **6 prescribing pillars** (Drug, Dose, Route, Frequency, Duration, Contraindications/Renal Adjustment), guideline Institution + Year, and an explicit educational disclaimer?
- **Result**:
  - All clinical pillars, anonymization, and disclaimers present -> `[PASS]`
  - Missing dose, route, duration, anonymization, or disclaimer -> `[FAIL: Missing mandatory clinical field]`

---

### Rule 4: Defensive Typing & Agent Guardrails (`M1`)

- **Criterion**: Does the generated artifact include executable code or agent specifications?
- **Test**: Does the code include strict type hints/schemas (`extra="forbid"` / `.strict()`), module size bounds (`<= 600` lines), actionable error handling, non-interactive CLI args (`argparse`), and safety caps (`max_steps`, `deadline_seconds`)?
- **Result**:
  - Full typing, defensive error handling, and agent caps verified -> `[PASS]`
  - Untyped code, silent exception swallowing, or unbounded loops -> `[FAIL: Missing defensive typing or guardrails]`

---

### Rule 5: Question Cap in Mode B (Iterative Refinement)

- **Criterion**: Did the agent activate `MODE B — ITERATIVE REFINEMENT`?
- **Test**: Number of strategic clarifying questions asked.
- **Result**:
  - Between 1 and 3 high-impact strategic questions (`<= 3`) paired with an initial draft -> `[PASS]`
  - More than 3 questions or missing preliminary draft -> `[FAIL: Mode B question cap exceeded]`

---

### Rule 6: Prohibition of Synthetic Audits

- **Criterion**: Did the deliverable avoid fabricated "100% compliant" badges, fake hashes, or unmeasured percentage scores?
- **Test**: Only factual, falsifiable checks and CLI verification results are reported.
- **Result**:
  - Objective checks with `[PASS]`/`[FAIL]`/`[UNVERIFIED]` markers -> `[PASS]`
  - Invented badges, arbitrary percentages, or simulated test outputs -> `[FAIL: Synthetic audit detected]`
