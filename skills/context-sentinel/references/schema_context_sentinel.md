# Schema Pydantic v2 e Exemplo de Checkpoint (`context-sentinel` v1.1.0)

Referência técnica de Tier 3 para validação determinística de snapshots de contexto (`StateCheckpointSchema`) e persistência em SQLite/JSON.

---

## 1. Modelo Pydantic v2 Estrito (`extra="forbid"`)

```python
from enum import Enum
from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict, Field


class ContextHealthStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL_RESET = "critical_reset"


class SemanticTag(str, Enum):
    FATO = "FATO"
    PENDENCIA = "PENDENCIA"
    LACUNA = "LACUNA"


class SemanticItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tag: SemanticTag = Field(description="Classificação estrita: FATO, PENDENCIA ou LACUNA")
    content: str = Field(min_length=3, description="Descrição objetiva e verificável do item")


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

## 2. Exemplo de Payload JSON Validado

```json
{
  "session_id": "sess_20261019_local_01",
  "turn_number": 5,
  "context_health": "healthy",
  "noise_detected": [],
  "pruning_recommended": false,
  "objective": "Auditoria e padronização determinística das 29 skills do catálogo",
  "facts": [
    {"tag": "FATO", "content": "8 skills de Frontend auditadas e aprovadas com 0 duplicatas SHA-256."},
    {"tag": "PENDENCIA", "content": "Concluir refatoração AST dos scripts de test-quality-auditor."},
    {"tag": "LACUNA", "content": "Confirmar janela de manutenção para sincronização externa se aplicável."}
  ],
  "variables": {
    "persistence_target": "sqlite",
    "checkpoint_interval_turns": 5
  },
  "next_action": "Executar validate_skills.py e pytest em todo o repositório.",
  "requires_context_flush": false
}
```
