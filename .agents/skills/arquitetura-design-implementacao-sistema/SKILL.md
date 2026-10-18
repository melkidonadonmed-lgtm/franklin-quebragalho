---
name: arquitetura-design-implementacao-sistema
description: >-
  Executa diagnóstico severo de MVP, arquitetura de navegabilidade comentada,
  aglomeração funcional por ilhas (Island UI/UX), especificação tipográfica linear,
  auditoria anti-hardcode e plano de implementação modular com score determinístico
  e histórico comparativo V1 vs V2 em HTML com metadados.
license: MIT
metadata:
  version: "2.0.0"
  author: "Franklin-Main & Melki"
  category: "Arquitetura, UI/UX Estrutural e Qualidade de Código"
  updated_at: "2026-10-15"
  tags:
    - "navegabilidade"
    - "arquitetura-em-ilhas"
    - "auditoria-mvp"
    - "zero-hardcode"
    - "tipografia-linear"
    - "score-deterministico"
version: 2.0.0
updated_at: 2026-10-15
author: Franklin-Main & Melki
category: Arquitetura, UI/UX Estrutural e Qualidade de Código
---

# Skill: Arquitetura, Navegabilidade, Ilhas Funcionais e Implementação de Sistemas (`v2.0.0`)

## Gatilhos de Ativação
- Solicitações para arquitetar softwares, plataformas web ou aplicativos focando em navegabilidade, intuitividade e modularidade.
- Pedidos de diagnóstico arquitetural severo de MVPs, refatoração de código acoplado/hardcoded ou organização de interfaces em ilhas funcionais (*Functional Island Architecture*).
- Demandas de modo de resolução (`V1 -> V2`) exigindo diagrama de fluxo comentado, score determinístico auditável (`SGA`) e relatório comparativo em HTML com metadados.

## Quando NÃO Usar
- Para definição exclusiva de paletas de cores ou temas puramente cosméticos (delegar ao arquivo `DESIGN.md` ou à skill `consultor-design-tatil-frontend`).
- Para auditoria isolada de árvore Git ou `.gitignore` sem escopo de arquitetura de software (delegar à skill `auditoria-projetos-sistema`).
- Para aplicar mutações destrutivas em banco de dados de produção sem validação humana explícita (*Human-in-the-Loop*).

## Entradas Obrigatórias
1. **Objetivo Central e Dor Real:** O problema exato que o sistema resolve (sem jargões de marketing).
2. **Perfis de Acesso e Contexto de Uso:** Quem opera o sistema, sob qual pressão cognitiva/tempo e com quais permissões.
3. **Proposta de Escopo (Candidato a MVP) ou Código/Fluxo Atual (V1):** Funcionalidades pretendidas ou artefato existente para diagnóstico e refatoração.

---

## Módulos Funcionais e Regras de Engenharia (v2.0.0)

Toda arquitetura concebida ou auditada por esta skill é governada por 5 módulos técnicos independentes de cor (evitando *lost in the middle* por poluição cosmética):

### Módulo 1: Navegabilidade, Grafo Comentado e Intuitividade Cognitiva
- **Regra dos 3 Cliques e Zero Becos sem Saída (Dead-Ends):** Nenhuma ação de valor primário pode exigir mais de 3 transições de estado a partir do Dashboard. Todo nó do fluxo deve possuir rota de retorno clara ou conclusão explícita.
- **Diagnóstico Comentado com Diagrama de Navegabilidade:** Todo mapa Mermaid deve vir acompanhado de comentários técnicos nó a nó explicando: (a) gatilho de entrada, (b) validação de estado e (c) motivo da transição.
- **Ergonomia Cognitiva (Padrão TDAH-Friendly):** Obrigatoriedade de barra de comando/busca global unificada (`Ctrl+K` / `Cmd+K`), ausência total de bloqueios nativos de thread (`alert()`, `confirm()`), feedback cinestésico imediato (`active:scale-95`) e previsibilidade espacial.
- **Cobertura Estrita dos 4 Estados de UI:** Toda tela ou ilha assíncrona deve especificar formalmente os estados `Empty`, `Loading`, `Success` e `Error`.

### Módulo 2: Aglomeração de Funções por Ilha (Functional Island Architecture)
- **Coesão Funcional por Ilha:** Funções que manipulam o mesmo domínio ou intenção imediata do usuário devem ser agrupadas em "Ilhas Funcionais" autocontidas (cards/painéis independentes). É proibido espalhar botões da mesma tarefa em extremidades opostas da tela.
- **Isolamento de Estado e Desacoplamento Data/Render:** Cada ilha gerencia seu estado efêmero de apresentação, enquanto os dados de negócio residem de forma autoritativa no servidor/store central. Ferramentas de busca/mutação de dados (*data tools*) devem ser estritamente separadas da camada de renderização da UI (*render tools*).
- **Blindagem Estrutural (Anti-Squish):** Botões de ação, badges e controles dentro das ilhas devem impor `flex-shrink: 0` e `white-space: nowrap` para impedir quebras verticais ou esmagamento em layouts responsivos.
- **Hierarquia de Profundidade Estrutural (`DESIGN.md v4.5-soft`):** Uso de iluminação direcional dupla a 135° (`.ui-card-soft`) e cavidades escavadas (`surface-inset`) para delimitar ilhas sem bordas duras de `1px` e sem depender de blur pesado (proibido glassmorphism difuso e azul cobalto).
- **Orquestração Multiagente de UI (`Topologia 3+1`):** Para decomposição em 3 ondas paralelas (*Shell/Navigator*, *Controls/Data*, *Motion/Interaction* e *Deterministic Observer*), consulte [`references/taxonomia_subagentes_ui_6_camadas.md`](references/taxonomia_subagentes_ui_6_camadas.md) e [`plans/ui_composition_dag.json`](../../plans/ui_composition_dag.json).

### Módulo 3: Crítica Severa de MVP (Rigor Técnico Superior)
- **Filtro Implacável de Escopo (Anti-Bloat):** O agente deve atuar como um Tech Lead severo. Toda funcionalidade proposta para o MVP que não contribua diretamente para validar a hipótese central de valor na Semana 1 deve ser classificada como `[CORTE OBRIGATÓRIO - FASE 2]` com justificativa técnica.
- **Proibição de "Vibe Coding" Frágil:** Rejeitar arquiteturas baseadas em mocks estáticos fingindo funcionamento, rotas sem tratamento de erro ou fluxos sem validação de schema (exigir Zod, Pydantic ou JSON Schema estrito).

### Módulo 4: Qualidade de Código, Modularidade por Função e Zero Hardcode
- **Tolerância Zero a Hardcode:** É proibido chumbar strings de configuração, URLs, limites numéricos ("magic numbers"), regras de negócio ou credenciais dentro de componentes de UI. Tudo deve ser extraído para constantes tipadas, variáveis de ambiente ou dicionários de configuração.
- **Modularidade por Função Única (SRP):** Cada módulo ou arquivo deve ter uma única responsabilidade clara (ex: `calculators/`, `validators/`, `adapters/`, `ui-islands/`).
- **Ecossistema Open-Source Auditável (Copy-Paste Pattern):** Priorizar componentes modulares abertos sem caixa-preta (`shadcn/ui`, Radix Primitives, Lucide Icons), garantindo controle total sobre o DOM e acessibilidade.

### Módulo 5: Tipografia Linear e Combinada (Fluid & Harmonious Typography)
- **Escala Tipográfica Linear/Fluida:** Tamanhos de fonte e espaçamentos devem seguir progressão matemática contínua usando `clamp(min, val_fluido, max)` com base em grid estrito de `4px` / `8px`, evitando saltos bruscos entre mobile e desktop.
- **Pareamento Semântico em 3 Camadas (Combinando):**
  1. **Display / Títulos de Ilha:** Fonte geométrica ou humanista de alto impacto (`font-weight: 600-700`, `letter-spacing: -0.02em`, `line-height: 1.15`).
  2. **Corpo / Leitura Contínua:** Sans-serif de alta legibilidade (`font-size: clamp(0.95rem, 1vw, 1.05rem)`, `line-height: 1.6`, largura máxima de linha de `65ch`).
  3. **Dados Técnicos / Métricas / Badges:** Fonte Monospace alinhada (`font-variant-numeric: tabular-nums`) para garantir que números e tabelas nunca desalinhem horizontalmente.

---

## Motor de Cálculos Determinísticos (Zero Números Vazios / Zero Placebo)

É terminantemente proibido atribuir notas subjetivas ou inventadas. Todo diagnóstico deve calcular o **Score Global de Arquitetura (SGA de 0 a 100)** usando as 5 equações determinísticas abaixo (implementadas em [`modules/deterministic_scorer.py`](modules/deterministic_scorer.py) e [`scripts/deterministic_scorer.py`](scripts/deterministic_scorer.py)) a partir das contagens reais extraídas do projeto/especificação:

1. **Índice de Navegabilidade e Estados (INE - Peso 25%):**
   - `Taxa_Rotas_Validas = (Total_Nos - Nos_Orfaos_Ou_DeadEnds) / max(1, Total_Nos)`
   - `Taxa_Estados_UI = Telas_Com_4_Estados_Mapeados / max(1, Total_Telas)`
   - `Penalidade_Cliques = max(0, (Profundidade_Maxima_Cliques - 3) * 15)`
   - `INE = max(0, ((Taxa_Rotas_Validas * 0.5 + Taxa_Estados_UI * 0.5) * 100) - Penalidade_Cliques)`

2. **Índice de Coesão em Ilhas (ICI - Peso 20%):**
   - `ICI = (Funcoes_Agrupadas_Em_Ilhas_Com_SRP / max(1, Total_Funcoes_Mapeadas)) * 100`
   - Se uma ilha misturar mais de 2 domínios distintos ou ultrapassar 7 elementos interativos primários sem sub-agrupamento, ela é contada como `0` (falha de sobrecarga cognitiva).

3. **Índice de Pureza de Código e Zero Hardcode (IPC - Peso 25%):**
   - `IPC = max(0, 100 - (Ocorrencias_Hardcode * 12) - (Funcoes_Acopladas_Data_UI * 15))`
   - Qualquer valor mágico, string de regra fixa na view ou chamada de banco/API direta dentro do componente visual deduz pontos imediatamente.

4. **Rigor de Enxugamento de MVP (IRM - Peso 15%):**
   - `IRM = (Features_Essenciais_Com_Contrato_Verificavel / max(1, Total_Features_Mantidas_No_MVP)) * 100`
   - Deduzir `20 pontos` para cada feature cosmética/secundária que não foi cortada da Fase 1.

5. **Conformidade Tipográfica e Estrutural (ICTE - Peso 15%):**
   - Soma binária auditável (20 pontos cada item cumprido):
     1. Uso de escala fluida `clamp()` definida.
     2. Pareamento de 3 camadas (Display + Body + Monospace `tabular-nums`).
     3. Respeito ao limite de `65ch` para texto corrido e ritmo vertical (`line-height`).
     4. Blindagem `anti-squish` (`flex-shrink: 0; white-space: nowrap`) em botões/tags.
     5. Presença de atalho global `Ctrl+K` sem `alert()` nativo.

- **Fórmula Final do Score Global (SGA):**
  `SGA = (INE * 0.25) + (ICI * 0.20) + (IPC * 0.25) + (IRM * 0.15) + (ICTE * 0.15)`

---

## Fluxo Operacional Passo a Passo

### Passo 1: Crítica Severa de Intenção e Corte de MVP
- Disseque o pedido do usuário. Identifique excessos de escopo, premissas frágeis e potenciais pontos de hardcode.
- Apresente a crítica severa antes de desenhar a solução, separando o que entra no **MVP Enxuto (Fase 1)** do que vai para o **Backlog (Fase 2)**.

### Passo 2: Mapeamento de Ilhas Funcionais e Tipografia Linear
- Agrupe as funcionalidades aprovadas em Ilhas Funcionais numeradas, definindo o contrato de entrada/saída de cada ilha (separando *data tools* de *render tools*).
- Defina a árvore de tokens tipográficos lineares (`clamp`) e pareamento de fontes em 3 camadas sem acoplamento de cores.

### Passo 3: Diagnóstico Comentado e Diagrama de Navegabilidade
- Construa o grafo Mermaid de navegabilidade mostrando todas as transições e atalhos (`Ctrl+K`).
- Abaixo do diagrama, forneça o **Diagnóstico Comentado Nó a Nó**, justificando a ergonomia do fluxo e provando a ausência de becos sem saída.

### Passo 4: Cálculo Determinístico de Métricas (Tabela Aberta)
- Execute `scripts/deterministic_scorer.py` (ou aplique as equações exatas sobre as contagens auditadas) e apresente a memória de cálculo completa das 5 fórmulas (`INE`, `ICI`, `IPC`, `IRM`, `ICTE`) mostrando numerador, denominador e penalidades aplicadas até chegar ao `SGA`.

### Passo 5: Modo de Resolução (Histórico V1 vs V2 em HTML com Metadados)
- **Gatilho Condicional:** Sempre que a skill for usada para corrigir, refatorar ou evoluir uma arquitetura/tela existente (Modo de Resolução), gere obrigatoriamente um arquivo **HTML5 autocontido** baseado em [`templates/resolution_diff_v1_v2.html`](templates/resolution_diff_v1_v2.html) contendo:
  1. `<head>` com `<meta>` tags de rastreabilidade (`skill-name`, `skill-version`, `resolution-mode`, `score-v1-baseline`, `score-v2-resolved`, `score-delta`, `audit-timestamp`).
  2. **Histórico Simples de Mudanças (Changelog Arquitetural V1 -> V2):** O que foi removido, o que foi isolado em ilhas e quais hardcodes foram eliminados.
  3. **Diagrama de Navegabilidade e Ilhas com Cores Semânticas de Diff:**
     - Vermelho (`#ef4444` / `#fef2f2`): Rota quebrada, hardcode ou excesso removido da V1.
     - Amarelo (`#f59e0b` / `#fffbeb`): Componente refatorado / desacoplado na transição V1 -> V2.
     - Verde (`#10b981` / `#ecfdf5`): Nova Ilha Funcional, validação determinística ou rota otimizada na V2.
  4. **Painel Comparativo de Scores Determinísticos (V1 vs V2):** Mostra a evolução matemática de cada módulo.

---

## Saídas e Entregáveis (Modelo de Saída)

Toda execução da skill deve entregar de forma estruturada:
1. **Matriz de Crítica Severa de MVP:** Tabela separando features aprovadas para a Fase 1 vs. features cortadas (`[CORTE OBRIGATÓRIO - FASE 2]`) com justificativa técnica.
2. **Especificação de Ilhas Funcionais e Tipografia Linear:** Contratos de dados vs. renderização por ilha, cobertura dos 4 estados (`Empty`, `Loading`, `Success`, `Error`) e tokens `clamp()` + `tabular-nums`.
3. **Grafo Mermaid de Navegabilidade + Diagnóstico Comentado Nó a Nó:** Comprovação da Regra dos 3 Cliques, atalho `Ctrl+K` e zero dead-ends.
4. **Memória de Cálculo Determinística (`SGA`):** Tabela com contagens brutas e resultados exatos de `INE`, `ICI`, `IPC`, `IRM`, `ICTE` e `SGA` (`0.00` a `100.00`).
5. **Artefato HTML de Resolução (`V1 -> V2`):** Gerado em modo de refatoração/resolução via `scripts/deterministic_scorer.py --html-out` ou template [`templates/resolution_diff_v1_v2.html`](templates/resolution_diff_v1_v2.html).
