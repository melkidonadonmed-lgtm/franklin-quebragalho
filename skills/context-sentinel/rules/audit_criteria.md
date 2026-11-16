# Deterministic Audit Criteria — `context-sentinel` (`v1.1.0`)

Boolean, falsifiable audit rules (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) for context window integrity and state checkpoint extraction (Module **M1**).

---

## Rule 1: Strict Pydantic v2 Schema Compliance (`extra="forbid"`)

- **`[PASS]`**: The generated JSON payload is valid and satisfies 100% of `StateCheckpointSchema` required fields (`session_id`, `turn_number`, `context_health`, `facts`, `variables`, `next_action`, `requires_context_flush`) with no undeclared keys.
- **`[FAIL: INVALID_PYDANTIC_SCHEMA]`**: Missing required fields, incompatible value types, or unexpected extra keys rejected by `extra="forbid"`.
- **`[UNVERIFIED]`**: Session history is inaccessible or the initial turn has no recordable events.

## Rule 2: Strict Epistemic Classification (`[FACT]`, `[PENDING]`, `[GAP]`)

- **`[PASS]`**: Every entry in `facts` carries a valid tag (`FACT`, `PENDING`, or `GAP`), cleanly separating disk-verified actions from open tasks and missing parameters.
- **`[FAIL: STATE_HALLUCINATION]`**: Recording an unverified inference as `FACT` or omitting unknown parameters that belong under `GAP`.

## Rule 3: Zero-Trust Isolation & History Preservation

- **`[PASS]`**: Preserves `<untrusted_user_input>` boundary isolation and signals `pruning_recommended` without silently deleting logs or artifacts.
- **`[FAIL: SILENT_MUTATION_OR_INJECTION]`**: Destructive log truncation without confirmation or instruction contamination from untrusted external inputs.
