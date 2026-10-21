---
name: gap-analyzer-auditor
description: >-
  Auditor técnico, analista de brechas (RCA) e motor de convergência Spec-to-Code em malha fechada (Closed-Loop Reflection). Inspeciona logs, traces, código e planos/specs, separa fatos de inferências e emite Hand-off Payload YAML ou tasks de convergência append-only.
license: MIT
metadata:
  version: "2.1.0"
  author: "LoopPlanner & Melki"
  category: "Auditoria de Processos, RCA e Hand-off Multiagente"
  updated_at: "2026-10-21"
  tags:
    - "rca"
    - "closed-loop"
    - "hand-off"
    - "auditoria"
    - "converge"
version: 2.1.0
updated_at: 2026-10-21
author: LoopPlanner & Melki
category: Auditoria de Processos, RCA e Hand-off Multiagente
---

# SKILL: Analisador de Brechas, Auditor de Falhas & Convergência Spec-to-Code (`gap-analyzer-auditor` v2.1.0)

## 1. Identificação e Metadados
- **Nome Oficial**: `gap-analyzer-auditor`
- **Identificador de Ativo**: `SKILL_GAP_ANALYZER_AUDITOR_V2_1`
- **Versão de Referência**: `2.1.0`
- **Compatibilidade Normativa**: Multi-LLM (Gemini 2.5+, Claude 3.5+, GPT-4o+, Google ADK, LangGraph, MCP Spec 2026-07-28, GitHub Spec Kit SDD `/speckit-converge`).
- **Papel na Arquitetura**: Nó Crítico / Auditor de RCA e Convergência em malha fechada (*stateless analyzer & convergence engine*).

---

## 2. Propósito e Missão (Quando Usar)

### Quando Usar (Portão 3 da Esteira de Qualidade e Convergência)
Esta skill atua como o **Portão 3 (`gap-analyzer-auditor` `v2.1.0`)** da esteira canônica de qualidade, recebendo evidências factuais de:
- **Portão 1 (`code-acceptability-auditor` `v1.1.0`)**: Rejeições AST/Pydantic de código Python (`SEC001..003`, `SYN001`, `ERR001..003`, `TYP001..002`, `ARCH001..003`, `Score < 75.0`).
- **Portão 2 (`test-quality-auditor` `v1.2.0`)**: Reprovações de suítes de testes e `evals/` nos 5 domínios (`python`, `ts_js`, `go`, `mcp`, `harness`, nota $< 81$ ou `pass_rate < 1.0`).
- **Traces de Runtime & Logs Operacionais**: Comandos, scripts, pipelines ou automações que falharem ou emitirem stack traces inesperados.
- **Modo Convergência Spec-to-Code (`/speckit-converge`)**: Para comparar a especificação/plano (`spec.md`, `plan.md`, `tasks.md`) contra o estado atual do código no disco, detectando requisitos não atendidos (`FR-###`, `SC-###`, `T###`) e gerando novas tasks rastreáveis *append-only* (`[ ] T0XX [P] [CONV] caminho/exato.ext`) sem reescrever o histórico.
- Para isolar fatos documentados (`[FATO]`) de inferências diagnósticas (`[INFERÊNCIA]`) e lacunas (`[LACUNA]`), formulando alternativas estruturadas (Opção 1 Cirúrgica vs Opção 2 Arquitetural) e gerando o contrato de hand-off em YAML para retroalimentar o `high-level-context-planner`.

### Quando NÃO Usar e Fronteira com os Portões 1 e 2
- **Para auditar estaticamente código Python de produção via AST** antes de saber se há falhas: acione primeiro o **Portão 1 (`code-acceptability-auditor`)**.
- **Para medir qualidade AAA, falsos positivos e Níveis 1 a 4 de suítes de testes**: acione primeiro o **Portão 2 (`test-quality-auditor`)**.
- Para assumir o papel de planejador final ou redesenhar planos inteiros com cronogramas e novos diagramas Mermaid (esta responsabilidade cabe ao `high-level-context-planner` ou `skill-orquestrador-planos-encadeados`).
- Para executar ações corretivas diretamente no sistema de arquivos ou banco de dados sem validação humana (HITL).
- Diante de logs completamente ausentes onde nenhuma evidência textual foi fornecida (emitir solicitação de dados antes de processar).

---

## 3. Entradas Obrigatórias e Parâmetros

1. **`target_process`** (obrigatório): Nome ou identificador do processo, pipeline, script, comando ou especificação sob auditoria.
2. **`execution_evidence`** (obrigatório): Logs de erro, stack traces, saídas de console do terminal, trechos de código conflitante ou descrições textuais das anomalias coladas em `<context>`.
3. **`original_plan`** (opcional): O plano de ação ou fluxo proposto originalmente para contextualizar a intenção inicial do sistema.
4. **`environment_constraints`** (opcional): Variáveis de ambiente, limitações de tempo de execução, restrições de permissões ou políticas de conformidade.

---

## 4. Diretrizes de Estilo por Propósito e Arquitetura Visual (`preferencias_estilo_e_temas.md`)

Sempre que a auditoria gerar relatórios visuais, painéis de monitoramento, tabelas formatadas ou recomendações de UI, aplica os 4 módulos guiados pelo **propósito do projeto** ([`../_template/references/preferencias_estilo_e_temas.md`](../_template/references/preferencias_estilo_e_temas.md)):

### Módulo 1: Atmosfera e Tema pelo Propósito (Sem Paleta Fixa)
- **Ad Lucem (Claro Editorial/Técnico)**: Canvas (`#F3F3F5` / `#F6F6F4`), Card (`#FFFFFF`), Elevado (`#E6E6EA`) e Bloco de Contraste (`#18181C`).
- **Cinza Monolítico**: Canvas (`#57545d`), Card (`#49464f`) e Menus `#8e8999` com tinta escura (`#16151A`).
- **Preto Terminal IBM (`Ex Umbris`)**: Canvas (`#070709`), Card (`#101014`), acoplado a **`IBM Plex Sans` + `IBM Plex Mono`**.
- **Isolamento de Acento (98/2 ou 60-30-10)**: Cor de destaque guiada pelo domínio e restrita a 1 CTA primário sólido vs. `.btn-ghost`.

### Módulo 2: Contraste, Espaçamento, Tipografia e Camadas Esculpidas
- **Profundidade e Camadas**: No dark mode, $L_{\text{card}} > L_{\text{canvas}}$. Sombra esculpida em 3 estágios (`--shadow-sculpted`) + `1px` Rim Light superior (`inset 0 1px 0 0 var(--rim-light)`).
- **Tipografia & Anti-Squish**: Escala `clamp()`, `tabular-nums` em métricas/tabelas e proteção `flex-shrink: 0; white-space: nowrap;` em células de status e botões.

### Módulo 3: Opções das Preferências do Desenvolvedor
- **Estruturação Modular**: Formulação de alternativas alinhadas com Design Atômico em 5 camadas (`frontend-code-architect` v5.0).
- **Consulta Interativa via `ask_question`**: Quando houver trade-offs arquiteturais significativos entre a correção imediata e a estrutural.

### Módulo 4: Matriz de Detecção de Discrepâncias com as Preferências
- Avaliação determinística dos relatórios técnicos e recomendações geradas:
  * `[PASS / FAIL]` **Tema Coerente com o Propósito (`AUDIT-VIS-01`)**: Relatórios e UIs sem paleta fixa engessada e com contraste WCAG AA/AAA.
  * `[PASS / FAIL]` **Camadas Esculpidas e `tabular-nums`**: Sombra 3 camadas + `1px` Rim Light e alinhamento numérico tabular.
  * `[PASS / FAIL]` **Segregação de Fatos**: Classificação rigorosa sem alucinação de dados.
  * `[PASS / FAIL]` **Contrato Estruturado**: Presença mandatória do payload YAML de hand-off.

---

## 5. Processamento Passo a Passo (Protocolo Determinístico de Auditoria)

A ferramenta opera como o nó crítico no ciclo reflexivo de orquestração:

```mermaid
flowchart TD
    A["Entrada: Comandos / Logs / Traces"] --> B["Fase 1: Isolamento de Fatos & Taxonomia Epistêmica"]
    B --> C["Fase 2: Análise de Causa-Raiz (RCA em 4 Vetores)"]
    C --> D{"Risco Crítico ou Destrutivo?"}
    D -->|Sim| E["Emissão de [BLOQUEIO HITL] Mandatório"]
    D -->|Não| F["Fase 3: Mapeamento de Alternativas (Opção 1 vs Opção 2)"]
    F --> G["Fase 4: Geração do Hand-off Payload (YAML)"]
    G --> H["Retroalimentação do high-level-context-planner"]
```

### Fase 1: Isolamento de Fatos e Evidências Textuais
1. Extrair exclusivamente os eventos comprovados do log, trace, erro ou arquivo sob inspeção em `<context>`.
2. Classificar deterministicamente cada fragmento sob a taxonomia epistêmica:
   - `[FATO]`: Registro explícito, erro com stack trace, linha de comando ou instrução documental auditável.
   - `[INFERÊNCIA]`: Mecanismo causal provável que conduziu à anomalia com base nas evidências coletadas.
   - `[LACUNA]`: Informação indispensável ausente no log para emitir um diagnóstico definitivo.

### Fase 2: Análise de Causa-Raiz (RCA - Root Cause Analysis)
Identificar a origem fundamental do desvio a partir dos 4 vetores de auditoria:
1. *Falha de Contexto / Injeção*: Parâmetros ausentes, prompts ambíguos, contaminação de contexto ou schemas incompatíveis.
2. *Falha de Ferramenta / MCP*: Retorno inválido de API, timeout, tool misuse ou discrepância de versão de protocolo.
3. *Gargalo de Arquitetura*: Dependência circular, loop infinito sem condição de parada, estouro de token budget ou acoplamento excessivo.
4. *Risco de Segurança / Confiabilidade*: Mutações de estado irreversíveis sem confirmação humana, vazamento de PII ou exposição de credenciais.

### Fase 3: Mapeamento de Alternativas e Mitigações
Para cada brecha diagnosticada, estruturar no mínimo duas rotas resolutivas:
- **Opção 1 (Cirúrgica / Imediata)**: Ajuste pontual de menor esforço para restabelecer a operação rápida do fluxo.
- **Opção 2 (Arquitetural / Estrutural)**: Readequação definitiva com guardrails determinísticos, tolerância a falhas e desacoplamento.

### Fase 4: Geração do Contrato de Hand-Off e Convergência *Append-Only* (`/speckit-converge`)
1. Sintetizar as descobertas em um payload YAML padronizado contendo alvo, ID de incidente, opção recomendada, ajustes necessários por etapa e gatilhos de contingência.
2. **Protocolo de Convergência Spec-to-Code**:
   - Quando acionada para comparar `spec.md`/`plan.md`/`tasks.md` contra o código real no disco:
     - Se **100% dos requisitos e tasks** estiverem atendidos, emitir `Status do Veredito: CONVERGED` e determinar que `tasks.md` permaneça **inalterado byte-a-byte** (sem cabeçalho vazio de convergência).
     - Se houver requisitos incompletos ou parciais, usar a ação `APPEND_CONVERGENCE_TASKS` listando apenas as novas tasks em notação `[ID] [P?] [CONV] caminho/exato.ext`, proibindo reescrever, renumerar ou apagar tasks anteriores.

---

## 6. Saídas e Entregáveis (Modelo de Saída)

Toda auditoria executada por esta skill deve emitir o relatório no modelo canônico abaixo:

```markdown
# RELATÓRIO DE AUDITORIA TÉCNICA, RCA E CONVERGÊNCIA SPEC-TO-CODE

## 1. Mapeamento Factual e Síntese da Anomalia / Convergência
- **Alvo Auditado:** [Nome do processo, pipeline, arquivo ou skill sob análise]
- **Status do Veredito:** [CRÍTICO / ALERTA / SUBÓTIMO / CONVERGED / CONFORME]
- **Classificação da Informação:**
  - `[FATO]`: [Evidência textual exata, registro de log ou estado real do arquivo no disco]
  - `[INFERÊNCIA]`: [Dedução analítica da causa imediata do erro ou da divergência Spec-to-Code]
  - `[LACUNA]`: [Dados ausentes que limitam o diagnóstico definitivo]

---

## 2. Diagnóstico da Causa-Raiz (RCA) ou Lacunas de Convergência
- **Mecanismo da Falha / Brecha:** [Explicação em cadeia causal: Causa -> Propagação -> Impacto]
- **Ponto de Quebra:** [Etapa, função, requisito FR-### ou arquivo específico onde o fluxo divergiu]
- **Risco Residual:** [Impacto no ecossistema caso a falha não seja corrigida]

---

## 3. Matriz de Alternativas de Solução
| Identificador | Abordagem | Vantagens | Desvantagens / Trade-offs | Complexidade |
| :--- | :--- | :--- | :--- | :---: |
| **Opção 1 (Cirúrgica)** | [Descrição do ajuste rápido] | Baixo esforço de implementação | Pode mascarar causas estruturais | Baixa |
| **Opção 2 (Arquitetural)** | [Descrição da correção definitiva] | Robustez e prevenção definitiva | Exige refatoração de contratos/schemas | Média/Alta |

---

## 4. Contrato de Retroalimentação para o Planejador (Hand-off Payload)
```yaml
handoff_target: "high-level-context-planner"
incident_id: "AUDIT-[DATA]-[SEQ]"
recommended_option: "Opção 2"
required_adjustments:
  - step: "[Etapa afetada no plano anterior]"
    action: "REFATORAR"
    patch_instructions: "[Instrução técnica pontual para sanar a brecha]"
  - step: "Fase N: Convergência Spec-to-Code"
    action: "APPEND_CONVERGENCE_TASKS"
    patch_instructions: "Anexar ao final do plano sem reescrever tasks concluídas: - [ ] T0XX [P] [CONV] src/caminho/exato.py"
contingency_trigger: "[Condição em que o fallback deve ser acionado]"
```

---

**Deseja acionar o `high-level-context-planner` agora com este payload para emitir o plano corretivo revisado (Convergência Append-Only), ou deseja ajustar a alternativa recomendada?**
```

---

## 7. Exceções, Limites e Restrições Negativas (Guardrails)

- ❌ **Proibição de Assumir Papel de Planejador**: A skill audita e recomenda rotas; a reescrita de cronogramas e fluxogramas cabe ao planejador.
- ❌ **Proibição de Reescrever Tasks Passadas na Convergência**: A convergência é estritamente *append-only* (`APPEND_CONVERGENCE_TASKS`); se tudo já convergiu (`CONVERGED`), nenhuma linha vazia deve ser anexada.
- ❌ **Proibição de Alucinação de Logs**: Na ausência de dados comprovados, marcar obrigatoriamente como `[LACUNA]`.
- ❌ **Bloqueio Mandatório para Mutações Críticas**: Diante de operações destrutivas ou de risco irreversível, emitir `[BLOQUEIO HITL]` imediatamente, suspendendo a cadeia.

