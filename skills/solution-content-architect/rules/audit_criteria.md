# Deterministic Audit & Rejection Criteria (`solution-content-architect` v2.6.0)

Run this gate silently on Direct Execution deliveries; emit explicit `[PASS]`, `[FAIL]`, or `[UNVERIFIED]` markers visibly when an audit or architectural fork blueprint is requested:

- `[PASS]`: Requirement verified against real input data, codebase context, or consulted documentation anchors.
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

### Rule 2: Media Prompt Completeness (`M5` & `M6` — Explicit Requests Only)

- **Criterion**: Were image or video generation prompts explicitly requested and produced?
- **Test**: Is the final generation prompt written in English and complete with all **8 Visual Pillars** for images, or **1 dominant action + 1 camera move** with temporal progression for video?
- **Result**:
  - Complete English prompt with all required pillars (or N/A) -> `[PASS]`
  - Non-English generation prompt or missing required visual pillars -> `[FAIL: Incomplete visual prompt pillars]`

---

### Rule 3: Clinical & Prescribing Integrity (`M7` — Explicit Requests Only)

- **Criterion**: Does the technical request explicitly involve clinical, medical, or pharmacological guidance?
- **Test**: Does the deliverable enforce PII/PHI anonymization, the 4-step causal chain, all **6 prescribing pillars**, guideline Institution + Year, and an explicit educational disclaimer?
- **Result**:
  - All clinical pillars, anonymization, and disclaimers present (or N/A) -> `[PASS]`
  - Missing dose, route, duration, anonymization, or disclaimer -> `[FAIL: Missing mandatory clinical field]`

---

### Rule 4: Defensive Typing & Scoped Runtime Guardrails (`M1`)

- **Criterion**: Does the generated artifact include executable code or agent specifications?
- **Test**: Does the code include strict type hints/schemas (`extra="forbid"` / `.strict()` / Go structs), module size bounds (`<= 600` lines), actionable error handling, non-interactive `argparse` flags *when building CLI tools*, and `max_steps`/`deadline_seconds` caps *when building agent or retry loops*?
- **Result**:
  - Full typing, defensive error handling, and scoped runtime guards verified -> `[PASS]`
  - Untyped code, silent exception swallowing, or unbounded agent/retry loops -> `[FAIL: Missing defensive typing or guardrails]`

---

### Rule 5: Blocking `[GAP]` Question Cap

- **Criterion**: Did missing constraints trigger blocking clarification?
- **Test**: Number of strategic clarifying questions asked.
- **Result**:
  - Between 1 and 3 high-impact strategic questions (`<= 3`) paired with a minimal working skeleton -> `[PASS]`
  - More than 3 questions or stalling without a working draft -> `[FAIL: Clarification question cap exceeded]`

---

### Rule 6: Prohibition of Synthetic Audits

- **Criterion**: Did the deliverable avoid fabricated "100% compliant" badges, fake hashes, or unmeasured percentage scores?
- **Test**: Only factual, falsifiable checks and real CLI verification results are reported.
- **Result**:
  - Objective checks with `[PASS]`/`[FAIL]`/`[UNVERIFIED]` markers -> `[PASS]`
  - Invented badges, arbitrary percentages, or simulated test outputs -> `[FAIL: Synthetic audit detected]`

---

### Rule 7: Proportionality & Zero Dead Abstractions

- **Criterion**: Does every introduced module, class, interface, wrapper, or dependency directly serve an active caller or requested behavior?
- **Test**: Check for single-implementation interfaces, pass-through wrappers, speculative `AbstractFactory` layers, unused folders, or unrequested external packages when stdlib suffices.
- **Result**:
  - Minimal working solution with zero unused wrappers or speculative layers -> `[PASS]`
  - Speculative or single-use dead abstraction detected -> `[FAIL: Speculative or single-use dead abstraction detected]`
