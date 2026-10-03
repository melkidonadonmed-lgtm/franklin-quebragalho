---
name: context-sentinel
description: >-
  Audita a integridade da janela de contexto em conversas multi-turn e pipelines multiagente. A cada ciclo de turnos ou sob demanda, extrai o estado estruturado da sessão com validação determinística Pydantic/JSON (classificando [FATO], [PENDENCIA] e [LACUNA]) para persistência em SQLite ou JSON local.
version: 1.0.0
updated_at: 2026-09-30
---

# Context Sentinel & Automated State Checkpointer 🛡️

Skill especializada em auditoria de integridade da janela de contexto, mitigação de degradação semântica (*context rot* / *lost in the middle*) e extração determinística de snapshots de estado para persistência local.

---

## 🎯 Quando Usar
- Sessões longas de conversação ou desenvolvimento com mais de 5 turnos.
- Pipelines de múltiplos subagentes onde o contexto precisa ser compartilhado sem ruídos.
- Quando o consumo estimado da janela de contexto ultrapassar 60% do limite do modelo.
- Solicitações explícitas como: "faça um checkpoint", "salve o estado atual", "audite a memória da sessão".

---

## 🚫 Quando NÃO Usar
- Tarefas pontuais e atômicas de 1 único turno (ex: consulta rápida de sintaxe).
- Operações de escrita em banco de dados de produção sem confirmação de schema.

---

## ⚙️ Pré-requisitos e Dependências
- Python 3.10+ com biblioteca `pydantic >= 2.0` (para validação tipada de esquemas).
- Banco SQLite local (`checkpoints.db`) ou arquivo JSON de histórico (`state_checkpoint.json`).

---

## 📋 Passo a Passo de Execução (Divulgação Progressiva)

### 1. Auditoria de Context Engineering (Métrica & Ruído)
- Calcule a densidade de informação da sessão e identifique blocos redundantes (schemas repetidos, tool calls idênticas consecutivas).
- Verifique se os delimitadores XML (`<context>`, `<untrusted_user_input>`) mantiveram seu isolamento.
- Avalie se há necessidade de poda (*context pruning*) de turnos antigos.

### 2. Deduplicação e Classificação Semântica de Fatos
Varra o histórico desde o último checkpoint e extraia:
- `[FATO]`: Decisões confirmadas, irreversíveis ou comandos executados com sucesso comprovado.
- `[PENDENCIA]`: Tarefas planejadas pendentes de execução.
- `[LACUNA]`: Parâmetros indispensáveis ausentes que exigem entrada do usuário ou consulta.

### 3. Validação Tipada com Pydantic v2
Valide a estrutura antes de emitir o payload:

```python
from enum import Enum
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ContextHealthStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL_RESET = "critical_reset"


class SemanticItem(BaseModel):
    tag: str = Field(description="Classificação: FATO, PENDENCIA ou LACUNA")
    content: str = Field(description="Descrição objetiva do item")


class StateCheckpointSchema(BaseModel):
    session_id: str
    turn_number: int
    context_health: ContextHealthStatus
    noise_detected: List[str] = Field(default_factory=list)
    pruning_recommended: bool
    objective: str
    facts: List[SemanticItem]
    variables: Dict[str, Any]
    next_action: str
---

## 📤 Saídas e Entregáveis (Modelo de Saída)

Payload JSON determinístico validado com schema Pydantic v2:

```json
{
  "session_id": "sess_20260930_local_01",
  "turn_number": 5,
  "context_health": "healthy",
  "noise_detected": [],
  "pruning_recommended": false,
  "objective": "Auditoria, higienização e promoção de ativos de IA",
  "facts": [
    {"tag": "FATO", "content": "126 arquivos organizados em 9 pastas canônicas no Google Drive."},
    {"tag": "FATO", "content": "Bancada Workspace Studio implantada em dev/sandbox/index.html."},
    {"tag": "PENDENCIA", "content": "Conectar o middleware ContextSentinel ao loop do epic-volta."}
  ],
  "variables": {
    "persistence_target": "sqlite",
    "checkpoint_interval_turns": 5
  },
  "next_action": "Instanciar tabela de checkpoints no SQLite local.",
  "requires_context_flush": false
}
```

---

## 🔒 Diretrizes de Segurança e Resiliência
- **Sem mutação silenciosa:** A skill sinaliza `pruning_recommended = True`, mas não descarta o histórico sem ordem do orquestrador.
- **Zero Alucinação de Variáveis:** Parâmetros não informados são marcados como `[LACUNA]`.
