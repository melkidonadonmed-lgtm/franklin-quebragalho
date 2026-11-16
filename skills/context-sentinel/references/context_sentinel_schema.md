# Pydantic v2 Schema and Checkpoint Example (`context-sentinel` v1.1.0)

Tier 3 technical reference for deterministic context snapshot validation (`StateCheckpointSchema`) and SQLite/JSON persistence.

---

## 1. Strict Pydantic v2 Model (`extra="forbid"`)

```python
from enum import Enum
from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict, Field


class ContextHealthStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL_RESET = "critical_reset"


class SemanticTag(str, Enum):
    FACT = "FACT"
    PENDING = "PENDING"
    GAP = "GAP"


class SemanticItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tag: SemanticTag = Field(description="Strict epistemic tag: FACT, PENDING, or GAP")
    content: str = Field(min_length=3, description="Objective, verifiable item description")


class StateCheckpointSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str
    turn_number: int = Field(ge=1)
    context_health: ContextHealthStatus
    noise_detected: List[str] = Field(default_factory=list)
    pruning_recommended: bool
    objective: str
    facts: List[SemanticItem]
    variables: Dict[str, Any] = Field(default_factory=dict)
    next_action: str
    requires_context_flush: bool = False
```

---

## 2. Validated JSON Payload Example

```json
{
  "session_id": "sess_20261116_local_01",
  "turn_number": 5,
  "context_health": "healthy",
  "noise_detected": [],
  "pruning_recommended": false,
  "objective": "Deterministic audit and Technical English standardization of canonical skills",
  "facts": [
    {"tag": "FACT", "content": "8 Frontend skills audited and verified with zero duplicate files."},
    {"tag": "PENDING", "content": "Complete AST verification of test-quality-auditor scripts."},
    {"tag": "GAP", "content": "Confirm maintenance window for external ecosystem sync if applicable."}
  ],
  "variables": {
    "persistence_target": "sqlite",
    "checkpoint_interval_turns": 5
  },
  "next_action": "Run validate_skills.py --strict and pytest across the repository.",
  "requires_context_flush": false
}
```
