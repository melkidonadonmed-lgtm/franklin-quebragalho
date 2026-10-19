---
name: context-sentinel
description: >-
  Audita a integridade da janela de contexto em conversas multi-turn e pipelines multiagente. A cada ciclo de turnos ou sob demanda, extrai o estado estruturado da sessão com validação determinística Pydantic/JSON (classificando [FATO], [PENDENCIA] e [LACUNA]) para persistência em SQLite ou JSON local.
license: MIT
metadata:
  version: "1.1.0"
  author: "Franklin-Main & Melki"
  category: "Auditoria e Integridade de Janela de Contexto"
  updated_at: "2026-10-19"
  tags:
    - "context-rot"
    - "sqlite"
    - "snapshots"
    - "pydantic"
version: 1.1.0
updated_at: 2026-10-19
author: Franklin-Main & Melki
category: Auditoria e Integridade de Janela de Contexto
---

# Context Sentinel & Automated State Checkpointer (`context-sentinel` v1.1.0)

Skill especializada em auditoria de integridade da janela de contexto, mitigação de degradação semântica (*context rot* / *lost in the middle*) e extração determinística de snapshots de estado (`StateCheckpointSchema`) para persistência local em `.context/` ou SQLite.

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Sessões longas de conversação ou desenvolvimento com mais de 5 turnos consecutivos.
- Pipelines de múltiplos subagentes onde o estado compartilhado precisa ser transferido sem ruído.
- Quando o consumo estimado da janela de contexto ultrapassar 60% do orçamento de tokens.
- Solicitações explícitas como: "faça um checkpoint", "salve o estado atual da sessão", "audite a janela de contexto".

### Quando NÃO Usar (Fronteira Estrita)
- Tarefas pontuais e atômicas de 1 único turno (ex.: consulta rápida de sintaxe).
- Para auditar ou refatorar prompts iniciais de usuário (use `refine-prompt`).
- Para curadoria de notas permanentes no cofre Obsidian `dev/notes` (use `curadoria-obsidian-vault`).

---

## ⚙️ Pré-requisitos e Entradas
1. **Histórico da Sessão / Turnos Atuais**: Sequência de passos executados, arquivos tocados e decisões tomadas.
2. **Alvo de Persistência**: `.context/CURRENT_STATE.md`, `.context/SESSION_LOG.md`, `state_checkpoint.json` ou SQLite local (`checkpoints.db`).

---

## 📋 Fluxo Operacional Passo a Passo

### 1. Auditoria de Context Engineering (Métrica & Ruído)
- Calcule a densidade de informação da sessão e identifique blocos redundantes (schemas repetidos, outputs truncados ou chamadas duplicadas).
- Verifique se os delimitadores XML (`<context>`, `<untrusted_user_input>`) mantiveram seu isolamento contra *prompt injection*.
- Avalie se há necessidade de poda (*context pruning* / `/compact`) de turnos antigos.

### 2. Deduplicação e Classificação Epistêmica Estrita
Varra o histórico desde o último checkpoint e classifique cada item estritamente como:
- **`[FATO]`**: Decisões confirmadas, arquivos gravados ou comandos executados com retorno verificado no disco.
- **`[PENDENCIA]`**: Tarefas planejadas pendentes de execução nas próximas etapas.
- **`[LACUNA]`**: Parâmetros indispensáveis ausentes que exigem entrada do usuário ou inspeção adicional.

### 3. Validação Tipada com Pydantic v2 (`extra="forbid"`)
Valide o snapshot contra o contrato `StateCheckpointSchema` detalhado em [`references/schema_context_sentinel.md`](references/schema_context_sentinel.md) antes de gravar o checkpoint.

---

## 📤 Saídas e Entregáveis
1. **Payload JSON Determinístico (`StateCheckpointSchema`)**: Contendo `session_id`, `turn_number`, `context_health` (`healthy` | `warning` | `critical_reset`), `facts` (`[FATO]`, `[PENDENCIA]`, `[LACUNA]`), `variables`, `next_action` e `requires_context_flush`.
2. **Veredito de Conformidade**: Validação explícita das regras de [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md) (`[PASS]` / `[FAIL]` / `[UNVERIFIED]`).

---

## 🔒 Diretrizes de Segurança e Resiliência
- **Sem Mutação Destrutiva Silenciosa**: A skill sinaliza `pruning_recommended = true`, mas nunca apaga artefatos ou logs sem confirmação.
- **Zero Alucinação de Variáveis**: Qualquer parâmetro não comprovado no histórico deve ser registrado como `[LACUNA]`.
