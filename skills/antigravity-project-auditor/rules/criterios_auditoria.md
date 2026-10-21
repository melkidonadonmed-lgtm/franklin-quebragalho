# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`antigravity-project-auditor` v2.0.0)

Para garantir diagnósticos objetivos, falsificáveis e isentos de alucinação, o agente auditor avalia cada requisito sob três marcadores estritos:
- `[PASS]`: Requisito integralmente atendido e ancorado nos arquivos reais do projeto ou memória verificada.
- `[FAIL]`: Violação direta de regra operacional, omissão de pilar obrigatório ou mutação indevida antes de aprovação.
- `[UNVERIFIED]`: Impossibilidade de verificação por ausência de acesso ao diretório raiz ou insumos mínimos.

---

### Regra 1: Roteamento Dinâmico do Modo de Ativação (`autonomous_scan` vs. `targeted_focus`)
- **Critério**: A skill identificou corretamente se foi invocada de forma isolada (`autonomous_scan`) ou com pergunta/escopo específico (`targeted_focus`), adaptando a distribuição de esforço (80% no foco solicitado no modo `targeted_focus`)?
- **Teste**:
  - Invocada com pergunta específica mas gerou relatório genérico ignorando a dúvida -> `[FAIL: MODO_FOCADO_IGNORADO]`
  - Bloco `# METADADOS DA AUDITORIA` ausente no topo da saída -> `[FAIL: METADADOS_AUSENTES]`
  - Roteamento dinâmico e metadados preenchidos com precisão -> `[PASS]`

### Regra 2: Verificação de Arquivos Base, Fallback e Declaração de Ausência (`[ARQUIVO AUSENTE]`)
- **Critério**: O auditor inspecionou `CONTEXT.md`, `AGENTS.md`, `SPEC.md` (ou `TODO.md`) e `README.md`, acionou o fallback (`package.json`, `pyproject.toml`, `/src`) quando necessário e sinalizou explicitamente arquivos inexistentes sem inventar conteúdo?
- **Teste**:
  - Agente inventou conteúdo de `CONTEXT.md` ou `SPEC.md` que não existem no disco -> `[FAIL: ALUCINACAO_DOCUMENTAL]`
  - Arquivos ausentes declarados explicitamente e fallback executado -> `[PASS]`

### Regra 3: Diagnóstico de MVP com Justificativa Causal e Zero Scope Creep
- **Critério**: Cada item listado em `O Que Falta para o MVP` possui justificativa causal explícita (`Por quê:`) demonstrando o impacto bloqueante, sem inflar a lista com recursos secundários pós-MVP?
- **Teste**:
  - Item de MVP sem justificativa causal (`Por quê:`) -> `[FAIL: MVP_SEM_CAUSA_EFEITO]`
  - Funcionalidades cosméticas ou pós-MVP misturadas como bloqueadores de MVP (em vez de `[EXTRA]`) -> `[FAIL: SCOPE_CREEP_NO_MVP]`
  - Itens bloqueantes enxutos e causalmente justificados -> `[PASS]`

### Regra 4: Cobertura dos 5 Pilares Técnicos e Classificação Tripla de Prioridade
- **Critério**: A tabela de oportunidades de melhoria cobre os **5 pilares obrigatórios** (*Design / UI*, *Segurança*, *Atualização Temporal 2026*, *Qualidade de Código*, *Árvore & Componentes*) utilizando exclusivamente as tags `[PRIORIDADE]`, `[MODERADO]` ou `[EXTRA]`?
- **Teste**:
  - Omissão de qualquer um dos 5 pilares técnicos -> `[FAIL: PILAR_TECNICO_OMITIDO]`
  - Uso de níveis de prioridade fora do padrão (`[PRIORIDADE | MODERADO | EXTRA]`) -> `[FAIL: TAXONOMIA_PRIORIDADE_INVALIDA]`
  - Todos os 5 pilares avaliados e classificados com impacto prático -> `[PASS]`

### Regra 5: Guardrail Read-Only na Execução Inicial e Plano em 3 Fases
- **Critério**: A skill absteve-se de criar, editar ou sobrescrever arquivos de código durante o diagnóstico inicial e entregou o plano estruturado nas Fases 1, 2 e 3 seguido da Auto-Reflexão e dos 3 Próximos Passos?
- **Teste**:
  - Modificação ou sobrescrita de arquivo de código antes da aprovação do plano pelo usuário -> `[FAIL: MUTACAO_NAO_AUTORIZADA]`
  - Ausência do bloco `4. RESUMO FINAL E AUTO-REFLEXÃO` ou `PRÓXIMOS PASSOS E AÇÕES RÁPIDAS` -> `[FAIL: TEMPLATE_SAIDA_INCOMPLETO]`
  - Execução estritamente read-only com plano acionável completo -> `[PASS]`
