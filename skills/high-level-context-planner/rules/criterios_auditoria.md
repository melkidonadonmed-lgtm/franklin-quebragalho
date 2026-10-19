# CRITÉRIOS DE AUDITORIA E REJEIÇÃO DETERMINÍSTICA (`high-level-context-planner` v2.1.0)

Este documento estabelece as regras de conformidade e critérios de corte falsificáveis para validação dos planos emitidos pela skill `high-level-context-planner`. Toda verificação emite obrigatoriamente um dos três marcadores padronizados:
- `[PASS]`: Requisito comprovado e verificado contra âncoras documentais reais.
- `[FAIL]`: Requisito violado com motivo específico demonstrado.
- `[UNVERIFIED]`: Não verificável por ausência de insumos no briefing inicial.

---

### Regra 1: Presença Mandatória da Fase 0
- **Critério**: O plano de ação estruturado contém a Fase 0 dedicada a alinhamento, pré-requisitos, variáveis de ambiente e validação de schemas?
- **Teste**: A primeira etapa declarada é formalmente a Fase 0 antes de qualquer código ou ação operária?
- **Resultado**:
  - Se contiver a Fase 0 explicitada -> `[PASS]`
  - Se iniciar diretamente na implementação pulando a Fase 0 -> `[FAIL: Ausência mandatória da Fase 0]`

---

### Regra 2: Decomposição Falsificável, Notação `[ID] [P?] [US#]` e Critérios Go/No-Go
- **Critério**: Todas as fases possuem tasks no formato `[ID] [P?] [US#] caminho/exato.ext` e critérios objetivos de aceite e bloqueio?
- **Teste**: As tasks paralelizadas (`[P]`) tocam arquivos distintos sem conflito de escrita e as condições Go/No-Go baseiam-se em estados falsificáveis (exit codes, schemas, arquivos)?
- **Resultado**:
  - Se todas as fases possuírem tasks estruturadas e condições Go/No-Go determinísticas -> `[PASS]`
  - Se contiver critérios vagos ou paralelismo conflitante no mesmo arquivo -> `[FAIL: Tasks sem caminho exato ou critérios Go/No-Go subjetivos]`

---

### Regra 3: Diagramação Mermaid Sintaticamente Válida
- **Critério**: O plano contém diagrama Mermaid renderizável sem erros de parser CommonMark?
- **Teste**: Utiliza `flowchart TD` ou `LR`, com rótulos de nós entre aspas e sem tags HTML brutas?
- **Resultado**:
  - Se o bloco Mermaid for sintaticamente correto e limpo -> `[PASS]`
  - Se contiver caracteres quebrados, nós sem aspas ou tipo de diagrama inválido -> `[FAIL: Sintaxe Mermaid corrompida]`

---

### Regra 4: Consumo Integral do Hand-Off Payload e Convergência *Append-Only*
- **Critério**: Diante de uma entrada contendo o payload YAML do `gap-analyzer-auditor`, o novo plano incorporou todos os ajustes solicitados em modo *Append-Only*?
- **Teste**: O plano v2.0 reflete as ações (`REFATORAR`, `INSERIR_GUARDRAIL`, `REMOVER_DEPENDENCIA`, `ADICIONAR_RETRY`, `BLOQUEIO_HITL` ou `APPEND_CONVERGENCE_TASKS`) anexando a seção de Convergência sem apagar ou renumerar tasks concluídas?
- **Resultado**:
  - Se todas as mitigações forem anexadas sem destruir histórico -> `[PASS]`
  - Se ignorar qualquer ajuste do payload ou reescrever tasks concluídas -> `[FAIL: Violação de hand-off ou reescrita destrutiva de histórico]`

---

### Regra 5: Estimativas de Esforço e Alocação de Responsáveis
- **Critério**: Cada fase possui skill/agente executor definido e nível de esforço relativo classificado?
- **Teste**: Há atribuição explícita de quem executa e se o esforço é Baixo, Médio ou Alto?
- **Resultado**:
  - Se todas as fases possuírem responsável e esforço tipado -> `[PASS]`
  - Se houver fases sem responsável atribuído -> `[FAIL: Fase órfã sem executor definido]`

---

### Regra 6: Delimitação Estrita de Papel e Tabela `Complexity Tracking` (YAGNI)
- **Critério**: O agente manteve sua atuação restrita ao planejamento e incluiu a tabela `Complexity Tracking` justificando eventuais abstrações extras?
- **Teste**: O plano não executou mutações diretas no disco e documentou violações YAGNI (ou declarou zero violações)?
- **Resultado**:
  - Se formulou a esteira com `Complexity Tracking` e delegou para as skills operárias -> `[PASS]`
  - Se executou mutações destrutivas ou omitiu justificativa de complexidade -> `[FAIL: Violação de separação de papéis ou over-engineering não justificado]`

---

### Regra 7: Aderência à Arquitetura Visual por Propósito (`preferencias_estilo_e_temas.md`)
- **Critério**: Fases que envolvem interfaces de usuário respeitam a atmosfera alinhada ao propósito do projeto?
- **Teste**: Seleção de atmosfera (*Ad Lucem*, *Cinza Monolítico `#57545d` + `#8e8999`*, *Preto Terminal IBM `Ex Umbris`* ou *AETHER 2027*), banimento de azul cobalto puro (`#0044FF`) e Design Atômico em 5 camadas?
- **Resultado**:
  - Se incorporar os guardrails visuais orientados ao propósito -> `[PASS]`
  - Se planejar paleta fixa repetitiva, componentes neon ou caixas-pretas -> `[FAIL: Inconformidade com arquitetura visual por propósito]`

