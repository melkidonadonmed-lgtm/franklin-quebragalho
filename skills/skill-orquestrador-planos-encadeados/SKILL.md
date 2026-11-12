---
name: skill-orquestrador-planos-encadeados
description: "Orquestrador executivo de planos encadeados DAG mapeando dependências entre skills especialistas e executando ondas sequenciais com Context Fork. Use para orquestrar planos DAG; não use para turno único."
version: "3.0.0"
updated_at: "2026-11-12"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "3.0.0"
  updated_at: "2026-11-12"
  author: "LoopPlanner & Melki"
  category: "Orquestração DAG, Compilação de Ondas, Context Fork & Transição de Estado"
  tags: ["orquestrador", "planos-encadeados", "dag", "kahn", "context-fork", "multiagente"]
---

# SKILL: Compilador e Orquestrador Executivo de Planos Encadeados e Grafos DAG (`skill-orquestrador-planos-encadeados` v3.0.0)

## 1. Objetivo, Papel na Arquitetura e Quando Usar (Gatilhos)

Enquanto o `high-level-context-planner` diagnostica a intenção e projeta o grafo cognitivo não-linear, esta skill atua como o **Motor Executivo de Compilação Topológica (Kahn), Isolamento de Contexto (*Context Fork*) e Roteamento de Estado** entre skills e subagentes.

Sua função real e determinística é:

1. **Compilar Planos em Ondas Paralelas (`Wave 1..Wave N` via Algoritmo de Kahn):** Detectar ciclos de dependência e agrupar etapas independentes que podem rodar simultaneamente via `invoke_subagent` ou `franklin_execute_dag`.
2. **Prevenir Colisões de Escrita em Paralelo (`[P]` Anti-Collision Gate):** Impedir que dois subagentes ou tasks na mesma onda editem o mesmo arquivo (`target_files`) simultaneamente.
3. **Blindar a Memória de Trabalho (*Context Fork* & Teto $\le 5$ Regras):** Montar envelopes enxutos (`ContextTransitionPayload`) injetando apenas os dados necessários para o nó ativo e até 5 regras operacionais (Camadas L2/L3), eliminando o *context rot* do histórico bruto.
4. **Executar Transições Não-Lineares (`ramo_fallback`), Verificação *Read-After-Write* e Portões HITL.**

### Quando Usar

- Para compilar e executar um plano emitido pelo `high-level-context-planner` (`grafo_execucao` ou `phases`) ou um arquivo `plans/*.json` (`DAGExecutionPlan`).
- Quando uma demanda aciona 2 ou mais skills/subagentes encadeados (ex.: Auditoria AST $\rightarrow$ Testes $\rightarrow$ RCA $\rightarrow$ Convergência, ou Topologia `3+1` de UI) exigindo isolamento de chaves de estado (`isolated_state_keys`).
- Para validar deterministicamente via `scripts/dag_chain_validator.py` se um plano possui ciclos, colisões de escrita ou excesso de contexto antes do disparo.

### Quando NÃO Usar (Limites e Exclusões)

- Para tarefas simples de turno único ou script isolado que não exigem encadeamento entre skills.
- Para conceber o planejamento inicial ou selecionar frameworks cognitivos a partir de uma ideia crua (utilize primeiro `high-level-context-planner`).
- Para executar mutações destrutivas sem passar pelo portão de aprovação humana (`BLOCKED_HITL` / `franklin_harness_checkpoint`).

---

## 2. Entradas e Parâmetros Esperados

- **`structured_plan` / `grafo_execucao`** (obrigatório): Plano em formato `CognitiveAdaptivePlan` (`grafo_execucao`), `DAGExecutionPlan` (`tasks`) ou fases numeradas (`phases`).
- **`execution_mode`** (opcional): `native_subagents` (`invoke_subagent` em ondas), `franklin_dag` (`franklin_execute_dag`) ou `step_by_step`.
- **`max_retries`** (opcional): Limite de tentativas de auto-correção por nó antes de desviar para `ramo_fallback` ou acionar `gap-analyzer-auditor` (padrão: `1`).

---

## 3. Processamento e Arquitetura de Execução em 5 Estágios

```mermaid
flowchart TD
    A["Entrada: Grafo de Execução (JSON) ou Plano Multifásico"] --> B["Estágio 1: Compilação Topológica de Kahn (scripts/dag_chain_validator.py)"]
    B -->|Ciclo, Lacuna ou Colisão| B1["[FAIL] Bloqueio Imediato na Fase 0"]
    B -->|Grafo Válido| C["Estágio 2: Agrupamento em Ondas Paralelas (Wave 0 -> Wave 1 -> Wave 2)"]
    C --> D["Estágio 3: Montagem do Envelope Context Fork (<= 5 regras, isolated_state_key)"]
    D --> E{"Estágio 4: Despacho e Avaliação do Nó"}
    E -->|Go (Critério Aprovado)| F["Estágio 5: Verificação Read-After-Write e Avanço"]
    E -->|No-Go Recuperável| G["Acionar ramo_fallback Não-Linear ou 1 Ciclo Self-Refine"]
    E -->|Risco Destrutivo| H["[BLOCKED_HITL] Suspender no Harness (franklin_harness_checkpoint)"]
```

### Estágio 1: Validação Topológica (Kahn), Gestão de Ambiguidade e Colisão de Escrita

1. Antes de iniciar qualquer execução, valide o grafo na Fase 0 usando `scripts/dag_chain_validator.py`:
   - **Gestão de Ambiguidade (`[LACUNA]` Zero no Disparo):** Planos contendo marcadores `[LACUNA]` em aberto ou ambiguidade não esclarecida retornam ao `high-level-context-planner` / usuário para clarificação antes de compilar ondas.
   - **Detecção de Ciclos (DAG):** Calcula o grau de entrada (`in_degree`) de cada nó. Se `visited_nodes < total_nodes`, aborta com `[FAIL: CYCLE_DETECTED]`.
   - **Guarda Anti-Colisão de Arquivos (`target_files`):** Verifica se dois nós alocados na mesma onda paralela (`Wave K`) declaram interseção em `target_files`. Se houver colisão, serializa os nós em ondas distintas ou bloqueia com `[FAIL: PARALLEL_FILE_COLLISION]`.
   - **Validação de Catálogo:** Confirma que todas as `responsible_skill` / `target_skill` existem no catálogo do workspace.

### Estágio 2: Isolamento de Contexto (*Context Fork*) e Envelope de Transição

Para evitar degradação de atenção (*context rot*) e respeitar a Parede de Complexidade ($\le 5$ regras por nó), o orquestrador **nunca repassa o histórico bruto da conversa** para os subagentes. Ele instancia o contrato `ContextTransitionPayload` formalizado em [`references/schema_transicao_contexto.json`](references/schema_transicao_contexto.json) (`phase_id`, `wave_index`, `sequence_index`, `target_skill`, `cognitive_pattern`, `isolated_state_key`, `input_payload`, `active_rules <= 5`, `target_files`, `expected_outputs`, `acceptance_criteria`, `fallback_branch` e `status`).

### Estágio 3: Despacho Paralelo (*Fan-Out*) e Consolidação (*Fan-In*)

- **Modo Subagentes Nativos (`invoke_subagent`)**: Dispara todos os nós da mesma onda (`Wave K`) em paralelo, gravando o retorno de cada subagente em sua respectiva chave isolada (`isolated_state_key`) para impedir sobrescrita concorrente.
- **Modo Motor DAG (`franklin_execute_dag`)**: Despacha o plano JSON para o orquestrador determinístico (`shared/execution_orchestrator.py`) com controle de `run_id`, `--resume` e `idempotency_key`.

### Estágio 4: Roteamento Não-Linear (`fallback_branch`), Retry e Portão HITL

- **`COMPLETED` (Condição Go atendida)**: O entregável passa na verificação *Read-After-Write* e libera os nós dependentes na onda seguinte.
- **`RETRYING` / `FALLBACK_ROUTED` (Falha Recuperável)**: Se o entregável violar o critério de aceite, o orquestrador executa até `max_retries = 1` enviando a discrepância exata ou desvia o fluxo para o nó declarado em `fallback_branch` (`ramo_fallback`).
- **`BLOCKED_HITL` (Mutação Crítica)**: Se o nó for do tipo `hitl_gate` ou envolver ação destrutiva, aciona `franklin_harness_guard` / `franklin_harness_checkpoint` e aguarda aprovação humana explícita.
- **`FAILED` (Falha Irrecuperável)**: Emite os logs de execução para o `gap-analyzer-auditor` realizar RCA e convergência *Append-Only*.

---

## 4. Automação Determinística (`scripts/dag_chain_validator.py`)

Utilize o script determinístico da skill para validar grafos, compilar ondas paralelas de Kahn, checar colisões de escrita e gerar os envelopes de transição:

```powershell
# Auto-teste determinístico (Kahn, detecção de ciclo, colisão de arquivos [P] e teto <= 5 regras)
uv run python skills/skill-orquestrador-planos-encadeados/scripts/dag_chain_validator.py --self-test

# Compilar um plano JSON (do high-level-context-planner ou plans/*.json) em Ondas Paralelas
uv run python skills/skill-orquestrador-planos-encadeados/scripts/dag_chain_validator.py --plan plans/distributed_agent_mediation_dag.json
```

---

## 5. Saídas e Entregáveis Estruturados

Toda execução ou compilação emitida por esta skill entrega:

1. **Mapa de Ondas Topológicas (Kahn Waves)**: Lista ordenada de ondas (`Wave 0`, `Wave 1`...) mostrando quais nós rodam em paralelo e quais chaves `isolated_state_key` recebem cada saída.
2. **Painel de Rastreabilidade e Transição de Estado**: `Onda | Nó / Fase | Skill / Subagente | Padrão Cognitivo | Regras Ativas (<=5) | Status ([PASS]/[FAIL]/BLOCKED_HITL)`.
3. **Veredito *Read-After-Write* Consolidado (`post_condition_verified: true/false`)**.

---

## 6. Exceções, Limites e Restrições Negativas (Guardrails)

Valide cada onda contra [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md):

- ❌ **Proibição de Injetar Histórico Bruto (*Context Rot*)**: Nenhum envelope `ContextTransitionPayload` pode repassar a transcrição inteira da sessão; envie apenas `input_payload` + `active_rules` ($\le 5$).
- ❌ **Proibição de Executar Grafo com Ciclo ou Colisão de Arquivo**: Se `dag_chain_validator.py` acusar ciclo (`CYCLE_DETECTED`) ou disputa de escrita no mesmo arquivo na mesma onda (`PARALLEL_FILE_COLLISION`), o disparo é bloqueado na Fase 0.
- ❌ **Proibição de Bypassar o Portão HITL**: Nós com `hitl_gate` ou risco crítico nunca podem avançar automaticamente sem `approval_token` válido.
