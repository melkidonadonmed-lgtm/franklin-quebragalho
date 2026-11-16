# Root Cause Analysis (RCA) Taxonomy & Anomaly Classification

This reference specifies the analytical taxonomy applied by `gap-analyzer-auditor` to dissect failures across AI workflows and software pipelines.

---

## 1. Epistemic Classification of Evidence

Before drawing diagnostic conclusions, tag every evidence item explicitly:

| Marker | Definition | Acceptance Criterion |
| :--- | :--- | :--- |
| **`[FACT]`** | Explicit documentary evidence | Verbatim entry in logs, source code, HTTP response, disk file state, or terminal output. |
| **`[INFERENCE]`** | Causal analytical deduction | Logical link connecting observed facts to system failure mechanics. |
| **`[GAP]`** | Missing critical evidence | Uncertainty point where logs were truncated, omitted, or lack inputs to confirm root cause. |

---

## 2. The 4 Root Cause Vectors

### Vector 1: Context / Injection Failure (Prompt & Data)
- **Symptoms**: Missing parameters, entity hallucination, malformed output schemas, multi-turn context drift, or prompt injection attempts.
- **Typical Root Cause**: Unisolated external inputs lacking XML boundaries, overloaded prompts (`> 5` rules/node), or permissive schemas missing `extra="forbid"` / `.strict()`.

### Vector 2: Tooling / MCP Protocol Failure (Tools & Connectors)
- **Symptoms**: External API `4xx`/`5xx` errors, request timeouts, malformed JSON-RPC payloads, or schema type mismatches.
- **Typical Root Cause**: Drift from `MCP Spec 2026-07-28`, stdout pollution in STDIO servers, or missing retry/backoff handling on transient errors.

### Vector 3: Architecture Bottleneck (Execution Graph & Performance)
- **Symptoms**: Infinite orchestration loops, redundant recursive tool calls, token budget exhaustion, parallel write collisions, or blocking synchronous I/O.
- **Typical Root Cause**: Circular dependencies between graph nodes, shared `target_files` across `[P]` workers, or missing `max_iterations` / `timeoutMs` caps.

### Vector 4: Security & Reliability Risk (Zero-Trust & Safety)
- **Symptoms**: Unconfirmed destructive commands (`rm -rf`, `DROP TABLE`), plaintext credentials in logs/code, or unsandboxed code execution.
- **Typical Root Cause**: Missing Human-in-the-Loop (`[HITL BLOCK]`) checkpoint or bypassed `BeforeToolCallback` input sanitization.

---

## 3. Severity & Verdict Matrix

- **`CRITICAL`**: Blocking failure causing task failure, irreversible data loss, or severe security vulnerability. Halts execution immediately.
- **`WARNING`**: Secondary-stage failure, degraded partial recovery, or latent schema mismatch.
- **`SUBOPTIMAL`**: Pipeline succeeded with measurable inefficiency (excessive token burn, high latency, or unnecessary complexity).
- **`COMPLIANT` / `CONVERGED`**: Audited workflow or Spec-to-Code state matches all requirements with zero gaps.
