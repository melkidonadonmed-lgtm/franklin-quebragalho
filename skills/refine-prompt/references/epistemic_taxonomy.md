# Epistemic Premise Taxonomy & Feasibility Auditing (2026 Standard)

This reference defines the epistemic classification framework, temporal grounding, and anti-hallucination feasibility gate used by `refine-prompt`.

---

## 1. Temporal Grounding & Active Documentation Verification

- **Session Temporal Baseline**: Ground volatile APIs, protocol specifications (`MCP 2026-07-28`, `Pydantic v2`, `TypeScript 5+`, `Go 1.24+`), and model capabilities in the session's active temporal context.
- **Official Source Verification Protocol**:
  - Never guess non-existent SDK methods, deprecated model names, or unverified protocol parameters.
  - Consult primary official documentation (`google-developer-knowledge`, `gemini_get_doc`, or official specification docs) before endorsing technical parameters in a refined prompt.

---

## 2. Three-Tier Epistemic Classification

When transforming a raw prompt or idea into a hardened specification, every premise MUST be classified into one of three deterministic levels:

### 2.1. `[FACT]`
- **Definition**: Data explicitly provided in the user input or directly verified in consulted primary documentation/files.
- **Handling**: Treated as an immutable operational truth. Must not be altered or softened.
- **Example**: "The user specified PostgreSQL 16 hosted on Cloud SQL."

### 2.2. `[INFERENCE]`
- **Definition**: Low-risk senior engineering assumption adopted autonomously to resolve minor gaps (style, conventions, linter defaults, file layout).
- **Handling**: Documented explicitly in the Methodological Note (`Module 1`) or scope header (`Module 2`) without interrupting execution.
- **Example**: "Since no Python formatter/typechecker was specified, assume Ruff and strict MyPy (`strict = true`)."

### 2.3. `[GAP]`
- **Definition**: Critical missing parameter whose autonomous assumption poses high operational risk (clinical dosing, destructive production mutations, financial transfers, or security credentials).
- **Handling**: Blocks immediate final execution in `Module 1` and activates **`Module 3` (Socratic Interview)** with at most 3 surgical A/B questions.
- **Example**: "The user requested an automated cleanup script for production files without defining the root directory or retention cutoff."

---

## 3. Feasibility Verdict Protocol

Before refining or expanding a prompt, evaluate physical, mathematical, autoregressive, regulatory, and security feasibility:

```text
               [Raw Prompt / Idea Evaluation]
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
         [Feasible]                 [Infeasible / Flawed]
              │                             │
    [Proceed to Epistemic         [Emit Immediate [VERDICT]
     Typing & Module 1/2/3]        + Root Cause + Viable Alternative]
```

### Rejection Verdict Criteria

1. **Physical, Mathematical, or Autoregressive Impossibility**: Demands contradicting computational limits, thermodynamics, or autoregressive generation mechanics (such as silent `Self-Refine` without native `<thinking>` tokens or a preliminary `"_pre_flight_check"` field).
2. **Flagrantly Suboptimal Architecture**: Unbounded loops without `max_steps`, severe context bloat, or architectural coupling guaranteeing failure.
3. **Critical Security Vulnerability**: Plaintext secrets, unsandboxed remote execution, missing HITL on destructive commands, or privacy regulation violations (`LGPD`, `HIPAA`, `GDPR`).

### Mandatory Rejection Format

```markdown
[VERDICT: INFEASIBLE/FLAWED/SUBOPTIMAL]
- **Root Cause**: [Detailed technical explanation of why the current design fails]
- **Recommended Alternative**: [Viable modern architecture grounded in 2026 standards]
```
