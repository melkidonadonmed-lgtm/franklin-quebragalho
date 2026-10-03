---
name: skill-orquestrador-planos-encadeados
description: >-
  Orquestrador executivo de planos encadeados e modulares. Recebe planos decompostos em fases numeradas, mapeia as dependencias entre skills especialistas, gerencia o estado compartilhado sem poluicao de contexto, governa a aderência ao design tátil e paleta mineral do desenvolvedor e dispara a execucao sequencial com validacao de discrepancias a cada transicao.
version: 1.1.0
updated_at: 2026-10-03
author: Arquiteto de Conteudo e Solucoes & Melki
category: Orquestracao, Workflows e Execucao Multiagente
---

# SKILL: Orquestração e Execução de Planos Encadeados (`skill-orquestrador-planos-encadeados`)

## 1. Nome da Skill
`skill-orquestrador-planos-encadeados` (Orquestrador e Coordenador Executivo de Planos Modulares Encadeados com Portão de Preferências Táteis).

---

## 2. Descrição
Esta skill atua como o motor de orquestração e roteamento executivo para planos de trabalho decompostos em etapas, módulos e cadeias de dependência. Sua responsabilidade central é receber planos estruturados, verificar os pré-requisitos de cada fase, manter a memória de trabalho enxuta (isolando payloads intermediários para mitigar *context rot*) e acionar cada skill especialista no momento exato em que seus insumos estiverem validados. Ela suporta chamadas condicionais — permitindo que uma skill planejadora decida se e quando a skill de diagramação visual deve ser acionada — e assegura que nenhuma etapa subsequente seja inicializada sem a satisfação integral dos critérios de aceite da etapa anterior. Adicionalmente, ela incorpora os 4 módulos canônicos de governança de design tátil e preferências perenes do desenvolvedor (paleta de cores mineral, anti-cobalto, anti-glassmorphism, opções de arquétipos e matriz de discrepâncias), atuando como guardiã da qualidade visual e arquitetural em toda a esteira de execução.

---

## 3. Gatilhos de Ativação

### Quando Usar
Esta skill **DEVE** ser acionada nas seguintes circunstâncias:
- Quando o usuário ou uma skill de nível superior fornecer um plano de ação estruturado em etapas (ex.: Fase 0, Fase 1, Fase 2...).
- Em solicitações de execução que envolvem mais de duas ferramentas ou skills trabalhando em conjunto de forma sequencial ou ramificada.
- Quando for necessário auditar a conformidade de planos multiagente com as preferências do Melki (paleta mineral e ergonomia tátil).
- Comandos diretos como: "execute o plano encadeado", "orquestre estas skills para resolver o projeto", "coordene a execução do plano modular garantindo minhas preferências de design".

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
- `design_preferences_gate` (opcional): Habilitação do portão de validação tátil para fases geradoras de UI/relatórios. Padrão: `true`.

---

## 5. Governança Canônica de Design e Preferências Melki nos Planos Encadeados

Em todas as transições de fase e consolidações de entregáveis, o orquestrador aplica os 4 módulos canônicos:

### 5.1. Módulo de Governança de Paleta de Cores nos Fluxos
- **Propagação de Tokens Minerais:** O orquestrador injeta no payload de transição (`references/schema_transicao_contexto.json`) os tokens cromáticos canônicos:
  * Canvas Ardósia Grafite (`#0B101B`), Superfície Elevada (`#162033`), Fundo Claro (`#FDFEE9`/`#EEF2F6`).
  * Acentos autorizados: Petroleum Blue (`#2B4C7E`), Slate Navy (`#203657`), Ouro Champanhe (`#D4AF37`), Sage Clínico (`#2D6A4F`).
- **Intercepção Anti-Cobalto:** Bloqueio imediato de qualquer entregável intermediário que utilize azul cobalto ofuscante (`#0044FF`, `#233DFF`, `#1D4ED8`) ou neons fluorescentes.

### 5.2. Módulo de Design Tátil para Artefatos e Painéis do Fluxo
- **Qualidade Visual dos Entregáveis da Cadeia:** Todo artefato visual, painel de monitoramento, dashboard ou mockup gerado pelas skills do fluxo deve:
  * Respeitar a Regra de Ouro da profundidade no dark mode (`L_card > L_canvas`).
  * Conter sombras físicas multicamadas (contato + projeção difusa) e rim light zenital mineral.
  * Banir categoricamente vidros translúcidos com blur excessivo (`backdrop-filter: blur`) e elementos neon reflexivos.
  * Conter classes de proteção anti-squish em botões e badges (`flex-shrink: 0; white-space: nowrap;`).

### 5.3. Módulo de Opções das Preferências na Tomada de Decisão do Fluxo
- **Pontos de Decisão com `ask_question`:** Em bifurcações de rota técnica ou visual, o orquestrador aciona a ferramenta `ask_question` oferecendo opções pré-configuradas baseadas nos 5 arquétipos canônicos do Melki (*Tactile Matte Minimalist*, *Phantom Obsidian 4K*, *Luxury Deep Blue*, *Gilded Navy Heritage*, *Polar Sand Light*).
- **Adoção do Padrão shadcn/ui:** Garantir que quando a esteira demandar novas bibliotecas de UI, priorize componentes de código aberto "copy-paste" (shadcn/ui, Radix UI, Lucide Icons, Tailwind UI) em vez de pacotes opacos monolíticos.

### 5.4. Módulo de Portão de Qualidade e Matriz de Discrepâncias
- Na conclusão de cada fase que gere artefatos de interface ou documentação de arquitetura, o orquestrador executa o portão de qualidade com marcadores determinísticos:
  * `[DISC-PALETA]` `[PASS / FAIL]`: Cores minerais sem cobalto neon.
  * `[DISC-RELEVO]` `[PASS / FAIL]`: Cartões elevados com sombras multicamadas e rim light.
  * `[DISC-RESILIENCIA]` `[PASS / FAIL]`: Botões e badges protegidos com anti-squish.
  * `[DISC-SUPPLY]` `[PASS / FAIL]`: Stack modular alinhada com as preferências do Melki.
- Se qualquer item for reprovado (`[FAIL]`), a transição para a próxima fase é pausada para 1 ciclo de auto-correção.

---

## 6. Processamento Passo a Passo

```text
[Recepção do Plano Estruturado]
               │
               ▼
[Fase 0: Validação de Pré-requisitos & Schemas de Design]
               │
               ▼
┌───► [Ciclo de Execução por Fase com Injeção de Contexto] ◄───┐
│                      │                                       │
│                      ▼                                       │
│        [Disparo da Skill Designada]                          │
│                      │                                       │
│                      ▼                                       │
│        [Portão de Qualidade & Matriz de Discrepâncias]       │
│                      │                                       │
└──── [Aprovado] ──────┴── [Discrepância] ─────────────────────► [Auto-Correção / Fallback]
               │
               ▼
[Consolidação Final, Matriz de Preferências & Entrega Integrada]
```

### Passo 1: Fase 0 — Validação Estrutural do Plano e Catálogo
1. Analisar o plano recebido e verificar se há:
   - Ambiguidade crítica ou ausência de insumos essenciais.
   - Referência a skills inexistentes no catálogo registrado.
   - Loops circulares de dependência (ex.: Fase A depende de B que depende de A).
2. Consultar os critérios em `rules/criterios_auditoria.md` e validar se os parâmetros de design tátil foram incluídos.

### Passo 2: Isolamento de Contexto e Montagem do Payload de Transição
1. Para cada fase ativa:
   - Extrair exclusivamente os dados necessários para aquela etapa específica.
   - NUNCA injetar o histórico bruto inteiro na skill operária para evitar poluição de contexto (*context rot*).
   - Envelopar os dados sob o formato de transição estruturado com injeção dos tokens de design e paleta mineral definidos em `references/schema_transicao_contexto.json`:
     ```json
     {
       "phase_id": "fase_1",
       "target_skill": "skill-nome",
       "input_payload": { },
       "context_constraints": [ "tactile_matte", "anti_cobalt", "cards_lighter_than_canvas" ]
     }
     ```

### Passo 3: Execução Condicional e Invocação de Sub-Skills
1. Se uma skill de planejamento indicar a necessidade de um artefato complementar (ex.: fluxograma ou mockup visual), verificar se a permissão contratual de invocação (`authorized_sub_skills`) está ativa.
2. Fazer o despacho da tarefa para a sub-skill autorizada, receber o retorno validado e reanexá-lo ao pacote de entrega da fase antes de prosseguir.

### Passo 4: Verificação de Critérios de Aceite e Matriz de Discrepâncias (Quality Gate)
1. Conferir se a saída produzida pela skill atende aos requisitos declarados no plano e passa na Matriz de Discrepâncias do Módulo 5.4.
2. Atualizar o estado da execução:
   - `FASE_CONCLUIDA`: Avança para a próxima fase numerada.
   - `FALHA_RECUPERAVEL`: Dispara 1 ciclo de auto-correção enviando o feedback de discrepância para a skill responsável.
   - `BLOQUEIO_CRITICO`: Suspende a execução e aciona `ask_question` para alinhamento com o usuário (HITL).

### Passo 5: Consolidação do Produto Final Integrado
Reunir os entregáveis gerados em cada fase em um único documento coerente e executivo, acompanhado do relatório de rastreabilidade e da matriz de conformidade com as preferências do Melki.

---

## 7. Saídas Estruturadas
O orquestrador entrega:

1. **Painel de Rastreabilidade do Fluxo:**
   - Tabela com: Fase | Skill Acionada | Insumos | Status de Execução | Tempo/Esforço Estimado.
2. **Matriz Consolidada de Discrepâncias com as Preferências:**
   - Tabela determinística com os status de aceite de design e qualidade (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).
3. **Entregável Integrado:** O compilado final dos produtos gerados em estrita conformidade com o formato solicitado pelo usuário.
4. **Registro de Transições e Hand-offs:** Descrição concisa dos dados transferidos entre cada elo da cadeia.

---

## 8. Exceções e Limites (O que esta Skill NÃO cobre)
- Não executa ações de risco crítico (deletar bases, publicar dados sensíveis, transações financeiras) sem autorização humana explícita no ponto de parada (Human-in-the-Loop).
- Não continua a execução se o resultado de uma fase antecedente for inválido e violar o contrato de entrada da fase subsequente.
- Não aceita entregáveis que violem o banimento estrito de azul cobalto puro ou empreguem vidros difusos que quebrem a consistência tátil.
- Não assume suposições probabilísticas sobre dados factuais ausentes; nestes casos, marca a fase como pendente (`[UNVERIFIED]`).
