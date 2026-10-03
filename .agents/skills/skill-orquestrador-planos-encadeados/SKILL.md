---
name: skill-orquestrador-planos-encadeados
description: >-
  Orquestrador executivo de planos encadeados e modulares. Recebe planos decompostos em fases numeradas, mapeia as dependencias entre skills especialistas, gerencia o estado compartilhado sem poluicao de contexto e dispara a execucao sequencial ou sob demanda, com validacao de saida a cada transicao.
version: 1.0.0
updated_at: 2026-10-03
author: Arquiteto de Conteudo e Solucoes
category: Orquestracao, Workflows e Execucao Multiagente
---

# SKILL: Orquestração e Execução de Planos Encadeados (`skill-orquestrador-planos-encadeados`)

## 1. Nome da Skill
`skill-orquestrador-planos-encadeados` (Orquestrador e Coordenador Executivo de Planos Modulares Encadeados).

---

## 2. Descrição
Esta skill atua como o motor de orquestração e roteamento executivo para planos de trabalho decompostos em etapas, módulos e cadeias de dependência. Sua responsabilidade central é receber planos estruturados, verificar os pré-requisitos de cada fase, manter a memória de trabalho enxuta (isolando payloads intermediários para mitigar *context rot*) e acionar cada skill especialista no momento exato em que seus insumos estiverem validados. Ela suporta chamadas condicionais — permitindo que uma skill planejadora decida se e quando a skill de diagramação visual deve ser acionada — e assegura que nenhuma etapa subsequente seja inicializada sem a satisfação integral dos critérios de aceite da etapa anterior.

---

## 3. Gatilhos de Ativação

### Quando Usar
Esta skill **DEVE** ser acionada nas seguintes circunstâncias:
- Quando o usuário ou uma skill de nível superior fornecer um plano de ação estruturado em etapas (ex.: Fase 0, Fase 1, Fase 2...).
- Em solicitações de execução que envolvem mais de duas ferramentas ou skills trabalhando em conjunto de forma sequencial ou ramificada.
- Comandos diretos como: "execute o plano encadeado", "orquestre estas skills para resolver o projeto", "coordene a execução do plano modular".

### Quando NÃO Usar
- Para tarefas simples de comando único ou script isolado que não demandam transição de fases.
- Para auditar ou refatorar o catálogo de habilidades (utilize `skill-auditor-refatorador-skills`).
- Para executar ações de alto risco destrutivo sem aprovação do usuário (Human-in-the-Loop).

---

## 4. Entradas Esperadas
- `structured_plan` (obrigatório): O plano de trabalho estruturado contendo:
  * Título e objetivo final do fluxo.
  * Fases numeradas com: Objetivo específico, Skill/Agente responsável, Insumos necessários (inputs), Entregáveis esperados (outputs), Regras de aceite e Nível de esforço.
- `context_state` (opcional): Variáveis de contexto iniciais e restrições de negócio fornecidas pelo usuário.
- `execution_policy` (opcional): Política de execução (`autonomous` para rodar ponta a ponta sem interrupções em ações seguras; ou `step_by_step` para solicitar confirmação ao fim de cada fase). Padrão: `autonomous`.

---

## 5. Processamento Passo a Passo

```text
[Recepção do Plano Estruturado]
              │
              ▼
[Fase 0: Validação de Pré-requisitos & Schemas]
              │
              ▼
┌───► [Ciclo de Execução por Fase] ◄───┐
│                     │                │
│                     ▼                │
│       [Disparo da Skill Designada]   │
│                     │                │
│                     ▼                │
│       [Inspeção de Saída & Critérios]│
│                     │                │
└──── [Sucesso] ──────┴── [Falha] ─────► [Fallback / Ajuste]
              │
              ▼
[Consolidação Final & Entrega Estruturada]
```

### Passo 1: Fase 0 — Validação Estrutural do Plano e Catálogo
1. Analisar o plano recebido e verificar se há:
   - Ambiguidade crítica ou ausência de insumos essenciais.
   - Referência a skills inexistentes no catálogo registrado.
   - Loops circulares de dependência (ex.: Fase A depende de B que depende de A).
2. Consultar os critérios em `rules/criterios_auditoria.md`. Se qualquer incoerência for identificada, a execução é pausada imediatamente e um alerta determinístico é emitido.

### Passo 2: Isolamento de Contexto e Montagem do Payload de Transição
1. Para cada fase ativa:
   - Extrair exclusivamente os dados necessários para aquela etapa específica.
   - NUNCA injetar o histórico bruto inteiro na skill operária para evitar poluição de contexto (*context rot*).
   - Envelopar os dados sob o formato de transição estruturado definido em `references/schema_transicao_contexto.json`:
     ```json
     {
       "phase_id": "fase_1",
       "target_skill": "skill-nome",
       "input_payload": { },
       "context_constraints": [ ]
     }
     ```

### Passo 3: Execução Condicional e Invocação de Sub-Skills
1. Se uma skill de planejamento indicar a necessidade de um artefato complementar (ex.: necessidade de fluxograma de processos), verificar se a permissão contratual de invocação (`authorized_sub_skills`) está ativa.
2. Fazer o despacho da tarefa para a sub-skill autorizada (`skill-diagramador-visual`), receber o retorno validado e reanexá-lo ao pacote de entrega da fase antes de prosseguir.

### Passo 4: Verificação de Critérios de Aceite e Marcadores de Parada
1. Conferir se a saída produzida pela skill atende aos requisitos declarados no plano.
2. Atualizar o estado da execução:
   - `FASE_CONCLUIDA`: Avança para a próxima fase numerada.
   - `FALHA_RECUPERAVEL`: Dispara 1 ciclo de auto-correção enviando o feedback de erro para a skill responsável.
   - `BLOQUEIO_CRITICO`: Suspende a execução e aguarda intervenção humana (HITL).

### Passo 5: Consolidação do Produto Final
Reunir os entregáveis gerados em cada fase em um único documento coerente e executivo, sem duplicar instruções internas ou logs operacionais de bastidores.

---

## 6. Saídas Estruturadas
O orquestrador entrega:

1. **Painel de Rastreabilidade do Fluxo:**
   - Tabela com: Fase | Skill Acionada | Insumos | Status de Execução | Tempo/Esforço Estimado.
2. **Entregável Integrado:** O compilado final dos produtos gerados em estrita conformidade com o formato solicitado pelo usuário.
3. **Registro de Transições e Hand-offs:** Descrição concisa dos dados transferidos entre cada elo da cadeia.

---

## 7. Exceções e Limites (O que esta Skill NÃO cobre)
- Não executa ações de risco crítico (deletar bases, publicar dados sensíveis, transações financeiras) sem autorização humana explícita no ponto de parada (Human-in-the-Loop).
- Não continua a execução se o resultado de uma fase antecedente for inválido e violar o contrato de entrada da fase subsequente.
- Não assume suposições probabilísticas sobre dados factuais ausentes; nestes casos, marca a fase como pendente (`[UNVERIFIED]`).
