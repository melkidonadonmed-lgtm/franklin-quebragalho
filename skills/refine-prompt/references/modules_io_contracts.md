# Module I/O Contracts & Operational Specifications

This document defines the structural input and output schemas for the three operational modules of `refine-prompt`.

---

## 1. Module Routing Matrix

| Module | Request Profile | Typical Trigger | Key Behavior |
| :--- | :--- | :--- | :--- |
| **Module 1** | Direct Resolution | Clear imperative requests ("audit", "fix", "refine this prompt"). | Immediate full delivery followed by a Methodological Note with sources and verdict. |
| **Module 2** | Plug-and-Play Artifact | Requests for reusable files ("generate system prompt", "build low-entropy extractor"). | Single continuous block, `[INSERT_FIELD]` placeholders, and deployment guide. |
| **Module 3** | Socratic Interview | Ambiguous, high-risk (clinical, financial, destructive), or underspecified requests. | At most 3 surgical questions with 2-3 viable options each + conditional draft. |

---

## 2. MODULE 1 Contract: Direct Resolution with Methodological Note

### Input Schema

```json
{
  "untrusted_user_input": "string (required)",
  "context": "string (optional)",
  "target_mode": "MODULE_1"
}
```

### Output Contract

```markdown
### 1. EXECUTIVE SYNTHESIS & RESOLVED SOLUTION
[Complete refined prompt, security audit, or resolved specification ready for immediate use]

### 2. METHODOLOGICAL NOTE & DECISION MATRIX
- **Applied Frameworks:** [e.g., Instruction Hierarchy + Zero-Trust XML + Entropy Modulation]
- **Primary Sources & Temporal Grounding (2026):** [Official docs and specs consulted]
- **Assumed Premises:** [Low-risk technical assumptions tagged as [INFERENCE]]
- **Feasibility Verdict:** [PASS / Approved with technical justification]
```

---

## 3. MODULE 2 Contract: Plug-and-Play Artifact

### Input Schema

```json
{
  "untrusted_user_input": "string (required)",
  "artifact_type": "SYSTEM_PROMPT | TASK_CONTRACT | JSON_EXTRACTOR | GUARDRAIL_BLOCK",
  "target_mode": "MODULE_2"
}
```

### Output Contract

```markdown
### 1. ARTIFACT SCOPE & DIAGNOSTICS
[1-to-3-line technical synthesis covering purpose, constraints, and covered scope]

### 2. COMPLETE CONTINUOUS ARTIFACT
```[language]
[FULL CONTENT IN ONE CONTINUOUS BLOCK]
[STANDARDIZED VARIABLES: [VARIABLE_NAME]]
[NO FRAGMENTATION OR LAZY PLACEHOLDERS]
```

### 3. DEPLOYMENT & TRIGGER GUIDE
- **Target Location:** [File path or runtime configuration field]
- **Required Variables:** [Concise list of bracketed placeholders to populate]
- **Technical Prerequisites:** [Minimum SDK versions, thinking mode, or permissions]
```

---

## 4. MODULE 3 Contract: Socratic Interview & Co-Creation

### Input Schema

```json
{
  "untrusted_user_input": "string (required, containing high risk or critical ambiguity)",
  "risk_classification": "CRITICAL_SECURITY | CLINICAL_HEALTH | DESTRUCTIVE_MUTATION | DOMAIN_GAP",
  "target_mode": "MODULE_3"
}
```

### Output Contract

```markdown
### 1. AMBIGUITY & RISK DIAGNOSTICS
- **Already Mapped:** [Clear objectives and confirmed facts tagged as [FACT]]
- **Critical Bottleneck / Risk:** [Exact reason for controlled pause, e.g., irreversible data loss]

### 2. SURGICAL KEY QUESTIONS (MAXIMUM 3)
1. **[Question 1]**: [Decision point description]
   - *Option A:* [Alternative 1 and trade-off]
   - *Option B:* [Alternative 2 and trade-off]
2. **[Question 2]**: [Decision point description]
   - *Option A:* [Alternative 1 and trade-off]
   - *Option B:* [Alternative 2 and trade-off]
3. **[Question 3]** *(only if strictly necessary)*: [Decision point description]
   - *Option A:* [Alternative 1 and trade-off]
   - *Option B:* [Alternative 2 and trade-off]

### 3. CONDITIONAL PRELIMINARY DRAFT
[Provisional prompt architecture built under temporary assumptions awaiting user confirmation]
```
