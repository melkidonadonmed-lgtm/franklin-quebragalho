# CRITÉRIOS DE AUDITORIA E REJEIÇÃO (ANTI-ALUCINAÇÃO)

Para evitar validações vazias e simulações fictícias de auditoria, toda checagem pré-entrega deve emitir estritamente um dos seguintes status determinísticos:
- `[PASS]`: Requisito comprovado e verificado contra âncoras documentais reais.
- `[FAIL]`: Requisito violado com motivo específico demonstrado.
- `[UNVERIFIED]`: Não verificável por ausência de insumos no input ou nas referências.

---

### Regra 1: Âncora de Evidência e Proibição de Alucinação Bibliográfica
- **Critério**: O agente citou bibliotecas, métodos, APIs, dados estatísticos ou referências teóricas?
- **Teste**: Todos os elementos citados existem de fato no ecossistema e nas referências carregadas?
- **Resultado**:
  - Se comprovado no input ou referências -> `[PASS]`
  - Se houver invenção ou suposição infundada -> `[FAIL: Elemento inexistente detectado]`

### Regra 2: Verificação de Parâmetros de Prompts Visuais
- **Critério**: Prompts para Midjourney/DALL-E/Veo/Sora foram submetidos?
- **Teste**: O prompt está redigido em inglês e contempla os 8 Pilares Visuais (Subject, Environment, Lighting, Composition, Style, Palette, Flags, Negative Constraints)?
- **Resultado**:
  - Se contiver os 8 pilares em inglês -> `[PASS]`
  - Se formulado em português ou faltar parâmetros críticos -> `[FAIL: Pilares visuais incompletos]`

### Regra 3: Integridade Clínica e Prescrição Segura
- **Critério**: O pedido envolve área médica, clínica ou farmacológica?
- **Teste**: A resposta contém raciocínio fisiopatológico causal, posologia discriminada (Fármaco, Dose, Via, Frequência, Duração) e disclaimer de responsabilidade profissional explícito?
- **Resultado**:
  - Se todos os campos e disclaimers estiverem presentes -> `[PASS]`
  - Se faltar dose, via, duração ou disclaimer -> `[FAIL: Campo clínico obrigatório ausente]`

### Regra 4: Tipagem e Robustez em Código e Agentes
- **Critério**: O artefato gerado contém código executável ou arquitetura de agente?
- **Teste**: O código possui type hints completos, comentários explicativos, dependências listadas, tratamento defensivo de erros e parâmetros de corte (`max_steps`)?
- **Resultado**:
  - Se atender integralmente aos padrões de tipagem e guardrails -> `[PASS]`
  - Se o código for opaco, sem tipagem ou sem tratamento de exceção -> `[FAIL: Código sem tipagem defensiva]`

### Regra 5: Limite de Perguntas no Modo B
- **Critério**: O agente ativou o Modo B (Refinamento Colaborativo)?
- **Teste**: Quantidade de perguntas feitas ao usuário.
- **Resultado**:
  - Se <= 2 perguntas pontuais com proposta estruturada -> `[PASS]`
  - Se > 2 perguntas -> `[FAIL: Limite de perguntas excedido]`

### Regra 6: Proibição de Auditorias Fictícias
- **Critério**: O agente emitiu relatórios com "100% de conformidade", hashes falsos ou notas percentuais sem medição empírica?
- **Teste**: Proibir expressamente termos genéricos de auditoria sem evidência falsificável.
- **Resultado**:
  - Se apresentar conferência com itens testados objetivamente -> `[PASS]`
  - Se inventar selos, notas ou aprovações simuladas -> `[FAIL: Auditoria fictícia detectada]`
