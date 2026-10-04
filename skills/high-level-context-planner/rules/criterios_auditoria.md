# CRITÉRIOS DE AUDITORIA E REJEIÇÃO DETERMINÍSTICA (`high-level-context-planner` v2.0.0)

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

### Regra 2: Decomposição Falsificável e Critérios Go/No-Go
- **Critério**: Todas as fases possuem critérios objetivos de aceite e bloqueio?
- **Teste**: As condições Go e No-Go baseiam-se em estados falsificáveis (exit codes, schemas, arquivos) e possuem rota de contingência?
- **Resultado**:
  - Se todas as fases possuírem condições Go/No-Go determinísticas -> `[PASS]`
  - Se contiver critérios vagos ("verificar se funciona", "validar tudo") -> `[FAIL: Critérios Go/No-Go subjetivos ou ausentes]`

---

### Regra 3: Diagramação Mermaid Sintaticamente Válida
- **Critério**: O plano contém diagrama Mermaid renderizável sem erros de parser CommonMark?
- **Teste**: Utiliza `flowchart TD` ou `LR`, com rótulos de nós entre aspas e sem tags HTML brutas?
- **Resultado**:
  - Se o bloco Mermaid for sintaticamente correto e limpo -> `[PASS]`
  - Se contiver caracteres quebrados, nós sem aspas ou tipo de diagrama inválido -> `[FAIL: Sintaxe Mermaid corrompida]`

---

### Regra 4: Consumo Integral do Hand-Off Payload no Replanning
- **Critério**: Diante de uma entrada contendo o payload YAML do `gap-analyzer-auditor`, o novo plano incorporou todos os ajustes solicitados?
- **Teste**: O plano v2.0 reflete as ações `REFATORAR`, `INSERIR_GUARDRAIL`, `REMOVER_DEPENDENCIA`, `ADICIONAR_RETRY` ou `BLOQUEIO_HITL` e registra o `incident_id`?
- **Resultado**:
  - Se todas as mitigações do payload forem absorvidas no plano e no diagrama -> `[PASS]`
  - Se ignorar qualquer ajuste mandatório do payload -> `[FAIL: Descumprimento das diretrizes de hand-off]`

---

### Regra 5: Estimativas de Esforço e Alocação de Responsáveis
- **Critério**: Cada fase possui skill/agente executor definido e nível de esforço relativo classificado?
- **Teste**: Há atribuição explícita de quem executa e se o esforço é Baixo, Médio ou Alto?
- **Resultado**:
  - Se todas as fases possuírem responsável e esforço tipado -> `[PASS]`
  - Se houver fases sem responsável atribuído -> `[FAIL: Fase órfã sem executor definido]`

---

### Regra 6: Delimitação Estrita de Papel (Planejamento vs Execução)
- **Critério**: O agente manteve sua atuação restrita à arquitetura, orquestração e planejamento?
- **Teste**: O plano não executou mutações diretas no disco nem rodou comandos sem a esteira apropriada?
- **Resultado**:
  - Se formulou a esteira e delegou para as skills operárias -> `[PASS]`
  - Se executou mutações destrutivas diretamente durante o turno de planejamento -> `[FAIL: Violação de separação entre planejamento e execução]`

---

### Regra 7: Aderência ao Design System Tátil e Paleta Mineral
- **Critério**: Fases que envolvem interfaces de usuário respeitam o design tátil Melki?
- **Teste**: Banimento explícito de azul cobalto puro (`#0044FF`), especificação de cartões elevados e componentes modulares (shadcn/ui)?
- **Resultado**:
  - Se incorporar os guardrails visuais minerais -> `[PASS]`
  - Se planejar componentes neon ou bibliotecas opacas caixa-preta -> `[FAIL: Inconformidade com preferências visuais]`
