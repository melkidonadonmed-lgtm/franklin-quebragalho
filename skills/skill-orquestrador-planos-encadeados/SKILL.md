---
name: skill-orquestrador-planos-encadeados
description: >-
  Orquestrador executivo de planos encadeados e modulares. Recebe planos decompostos em fases numeradas, mapeia as dependências entre skills especialistas, gerencia o estado compartilhado sem poluição de contexto, governa a aderência do estilo visual ao propósito do projeto (espaçamento, contraste, tipografia e camadas sem paleta fixa) e dispara a execução sequencial com validação de discrepâncias a cada transição.
license: MIT
metadata:
  version: "2.0.0"
  author: "LoopPlanner & Melki"
  category: "Orquestração, Workflows e Execução Multiagente"
  updated_at: "2026-10-19"
  tags:
    - "orquestrador"
    - "planos-encadeados"
    - "workflow"
    - "estilo-por-proposito"
    - "multiagente"
version: 2.0.0
updated_at: 2026-10-19
author: LoopPlanner & Melki
category: Orquestração, Workflows e Execução Multiagente
---

# SKILL: Orquestração e Execução de Planos Encadeados (`skill-orquestrador-planos-encadeados` v2.0.0)

## 1. Nome da Skill
`skill-orquestrador-planos-encadeados` (Orquestrador e Coordenador Executivo de Planos Modulares Encadeados com Portão de Estilo por Propósito).

---

## 2. Descrição
Esta skill atua como o motor de orquestração e roteamento executivo para planos de trabalho decompostos em etapas, módulos e cadeias de dependência. Sua responsabilidade central é receber planos estruturados, verificar os pré-requisitos de cada fase, manter a memória de trabalho enxuta (isolando payloads intermediários para mitigar *context rot*) e acionar cada skill especialista no momento exato em que seus insumos estiverem validados. Adicionalmente, quando o plano envolve entregas visuais/frontend, aplica a governança de **Preferências de Estilo e Arquitetura Visual por Propósito** ([`../_template/references/preferencias_estilo_e_temas.md`](../_template/references/preferencias_estilo_e_temas.md)), garantindo que o tema se encaixe no objetivo do projeto sem impor paletas fixas repetitivas.

---

## 3. Gatilhos de Ativação

### Quando Usar
- Quando o usuário ou uma skill de nível superior fornecer um plano de ação estruturado em etapas (ex.: Fase 0, Fase 1, Fase 2...).
- Em solicitações de execução que envolvem mais de duas ferramentas ou skills trabalhando em conjunto de forma sequencial ou ramificada.
- Quando for necessário coordenar a transição entre planejamento, arquitetura, código e auditoria mantendo o estado isolado e validado.

### Quando NÃO Usar
- Para tarefas simples de comando único ou script isolado que não demandam transição de fases.
- Para auditar ou refatorar o catálogo de habilidades (utilize `skill-auditor-refatorador-skills`).
- Para executar ações de alto risco destrutivo sem aprovação do usuário (Human-in-the-Loop).

---

## 4. Entradas Esperadas
- `structured_plan` (obrigatório): O plano de trabalho estruturado contendo título, objetivo final e fases numeradas com: Objetivo específico, Skill/Agente responsável, Insumos necessários (`inputs`), Entregáveis esperados (`outputs`) e Regras de aceite.
- `context_state` (opcional): Variáveis de contexto iniciais e restrições de negócio fornecidas pelo usuário.
- `execution_policy` (opcional): `autonomous` (padrão) ou `step_by_step`.
- `design_preferences_gate` (opcional): Habilitação do portão de validação visual por propósito para fases geradoras de UI/relatórios (`true` por padrão).

---

## 5. Governança de Estilo por Propósito e Arquitetura Visual nos Planos Encadeados

Em todas as fases que gerem interfaces, dashboards ou relatórios HTML/PDF, o orquestrador verifica os 4 módulos de qualidade visual (consulte [`../_template/references/preferencias_estilo_e_temas.md`](../_template/references/preferencias_estilo_e_temas.md)):

### 5.1. Módulo de Tema e Atmosfera pelo Propósito do Projeto (Sem Paleta Fixa)
- **Propagação Semântica Contextual:** O orquestrador propaga no payload de transição (`references/schema_transicao_contexto.json`) o propósito do projeto (*Conversão/SaaS*, *Editorial*, *FinTech*, *IA Nativa/AETHER*, *MedTech* ou *DevTools/Terminal IBM*) e a atmosfera selecionada:
  * *Ad Lucem* (Claro Editorial/Técnico: `--bg-canvas: #F3F3F5` / `#F6F6F4`, `--bg-surface: #FFFFFF`, `--bg-contrast-card: #18181C`).
  * *Cinza Monolítico* (`--bg-canvas: #57545d`, `--bg-surface: #49464f`, menus `#8e8999` com tinta escura `--nav-ink: #16151A`).
  * *Preto Terminal IBM (`Ex Umbris`)* (`--bg-canvas: #070709`, `--bg-surface: #101014`, acoplado à tipografia `IBM Plex Sans` + `IBM Plex Mono`).
  * *AETHER 2027* (Espaço perceptual `oklch()` e contraste APCA).
- **Isolamento de Acento (98/2 ou 60-30-10):** A cor de acento (`--punctual-accent`) é escolhida conforme o propósito do projeto e restrita a 1 único CTA primário sólido por dobra (contra ações secundárias `.btn-ghost`).

### 5.2. Módulo de Contraste, Espaçamento, Tipografia e Camadas Esculpidas
- **Qualidade Visual dos Entregáveis da Cadeia:**
  * Respeitar separação de luminância no dark mode ($L_{\text{card}} > L_{\text{canvas}}$) e tinta escura nítida em menus claros/`#8e8999`.
  * Conter sombra esculpida em 3 camadas (`--shadow-sculpted`: Umbra + Penumbra + Difusão) + `1px` Rim Light (`inset 0 1px 0 0 var(--rim-light)`).
  * Preservar $\ge 25\%$ de respiro no canvas, raios concêntricos, escala fluida `clamp()`, `tabular-nums` em métricas e proteção anti-squish (`flex-shrink: 0; white-space: nowrap;`, alvos $\ge 44\times44\text{px}$).

### 5.3. Módulo de Decisão Arquitetural
- Em bifurcações visuais ou arquiteturais ambíguas, o orquestrador pode acionar `ask_question` apresentando a recomendação alinhada ao propósito do projeto.
- Prioriza componentes modulares em **5 camadas de Design Atômico** (`frontend-code-architect` v5.0).

### 5.4. Módulo de Portão de Qualidade e Matriz de Discrepâncias
- Na conclusão de cada fase visual/arquitetural, valida:
  * `[DISC-PROPOSITO]` `[PASS / FAIL]`: Tema e acento coerentes com o objetivo do projeto e isolamento de 1 CTA primário.
  * `[DISC-CAMADAS]` `[PASS / FAIL]`: Sombra esculpida 3 estágios + `1px` Rim Light, contraste WCAG AA/AAA e espaçamento concêntrico.
  * `[DISC-RESILIENCIA]` `[PASS / FAIL]`: Tipografia `tabular-nums`, botões com anti-squish e estados FSM (`idle | loading | error | pressed`).
  * `[DISC-SUPPLY]` `[PASS / FAIL]`: Stack modular alinhada com as preferências do projeto.

---

## 6. Processamento Passo a Passo

### Passo 1: Fase 0 — Validação Estrutural do Plano e Catálogo
1. Analisar o plano recebido e verificar se há ambiguidade crítica, referência a skills inexistentes ou loops circulares de dependência (DAG).
2. Consultar os critérios em [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).

### Passo 2: Isolamento de Contexto e Montagem do Payload de Transição
1. Extrair exclusivamente os dados necessários para a etapa ativa (evitando *context rot*).
2. Envelopar os dados sob o formato de `references/schema_transicao_contexto.json`:
   ```json
   {
     "phase_id": "fase_1",
     "target_skill": "skill-nome",
     "input_payload": {},
     "context_constraints": ["purpose_driven_theme", "sculpted_layers_rim_light", "wcag_contrast_tabular_nums"]
   }
   ```

### Passo 3: Execução Condicional, Despacho DAG e Invocação de Sub-Skills
1. Se o plano estiver no formato `DAGExecutionPlan`, acione `franklin_execute_dag(plan_path_or_json)` para execução paralela em ondas via Kahn.
2. Despache sub-tarefas para skills autorizadas (`authorized_sub_skills`) e valide o retorno antes de avançar.

### Passo 4: Verificação de Critérios de Aceite (Quality Gate)
- `FASE_CONCLUIDA`: Avança para a próxima fase numerada.
- `FALHA_RECUPERAVEL`: Dispara 1 ciclo de auto-correção enviando o feedback de discrepância.
- `BLOQUEIO_CRITICO`: Suspende a execução e solicita alinhamento (HITL).

### Passo 5: Consolidação do Produto Final Integrado
Reunir os entregáveis gerados em cada fase em um documento executivo acompanhado do painel de rastreabilidade.

---

## 7. Saídas Estruturadas
1. **Painel de Rastreabilidade do Fluxo:** Fase | Skill Acionada | Insumos | Status de Execução.
2. **Matriz Consolidada de Conformidade:** Status `[PASS]`, `[FAIL]`, `[UNVERIFIED]`.
3. **Entregável Integrado e Registro de Transições.**
