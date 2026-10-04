# Protocolo de Consumo de Hand-Off Payload e Replanejamento Contínuo

Este documento detalha o protocolo pelo qual o `high-level-context-planner` consome o payload YAML estruturado emitido pelo `gap-analyzer-auditor` e sintetiza o Plano de Ação Revisado (v2.0).

---

## 1. Mapeamento de Ações de Ajuste (Patch Actions)

Ao processar a lista `required_adjustments` do payload de auditoria, o planejador aplica as seguintes transformações determinísticas:

| Ação | Operação no Grafo do Plano | Efeito Prático na Fase |
| :--- | :--- | :--- |
| **`REFATORAR`** | Substituição de instrução ou contrato de dados | A fase existente tem seus inputs, ferramentas ou comandos modificados para sanar a causa-raiz apontada. |
| **`INSERIR_GUARDRAIL`** | Injeção de nova fase ou portão intermediário | É criada uma fase `Fase X.5` ou etapa de validação (ex: linter, verificação de schema, checagem de timeout) antes do avanço. |
| **`REMOVER_DEPENDENCIA`** | Quebra de acoplamento circular | Duas fases que dependiam mutuamente são desacopladas, utilizando um intermediário assíncrono ou fila de eventos. |
| **`ADICIONAR_RETRY`** | Configuração de resiliência | A fase afetada passa a conter política de retentativa com backoff exponencial e limite máximo de tentativas (`max_retries`). |
| **`BLOQUEIO_HITL`** | Portão de parada mandatória | A esteira automatizada é interrompida, inserindo um ponto de confirmação humana obrigatório via `ask_question`. |

---

## 2. Ciclo de Vida Semântico do Plano

```text
[Plano v1.0.0: Concepção Inicial]
                │
                ▼
[Execução / Pipeline / Simulação]
                │
       [Falha / Gargalo]
                │
                ▼
[gap-analyzer-auditor: Diagnóstico RCA & Hand-Off Payload]
                │
                ▼
[high-level-context-planner: Consumo de Patches]
                │
                ▼
[Plano v2.0.0: Versão Corrigida com Mitigações Integradas]
```

---

## 3. Estrutura do Registro de Mitigações

Todo plano emitido após um ciclo de auditoria deve conter a seção **5. Registro de Patches e Mitigações**, garantindo rastreabilidade total:
- Referência ao `incident_id` original (ex.: `AUDIT-2026-10-03-01`).
- Opção selecionada (`Opção 1 Cirúrgica` ou `Opção 2 Arquitetural`).
- Detalhamento de cada modificação aplicada no fluxo e no diagrama Mermaid.
