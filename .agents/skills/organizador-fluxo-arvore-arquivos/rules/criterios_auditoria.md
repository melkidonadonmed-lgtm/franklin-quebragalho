# CRITÉRIOS DE AUDITORIA E REJEIÇÃO (ORGANIZADOR DE FLUXO E ÁRVORE)

Para evitar validações vazias e saídas truncadas, cada entrega gerada por esta skill deve ser conferida contra os seguintes critérios determinísticos:

---

### Regra 1: Preservação Fiel do Pedido Original
- **Critério**: O campo `Pedido original :` contém o texto literal enviado pelo usuário sem alterações?
- **Teste**: Comparar texto contido nas aspas com o prompt do usuário.
- **Resultado**:
  - Se for cópia 100% fiel -> `[PASS]`
  - Se houve reescrita, resumo ou alteração do prompt -> `[FAIL: Pedido original modificado]`

### Regra 2: Isolamento Estrito do MVP (Regra Anti-Inchaço)
- **Critério**: O fluxo principal contém apenas ações vitais para a ideia central?
- **Teste**: Todos os recursos extras, melhorias de segurança ou refinamentos secundários estão segregados em `### 5. Sugestões Opcionais`?
- **Resultado**:
  - Se o escopo central for enxuto e melhorias estiverem segregadas -> `[PASS]`
  - Se o fluxo central inflar a proposta original -> `[FAIL: Escopo inflado sem segregação]`

### Regra 3: Validade de Sintaxe Mermaid
- **Critério**: O bloco Mermaid está devidamente cercado por ```mermaid e utiliza nós descritivos simples (ex: `A[Início] --> B[Ação]`)?
- **Teste**: Ausência de caracteres ilegais em labels não escapados e ausência de jargões técnicos opacos.
- **Resultado**:
  - Se o diagrama for visualmente intuitivo e sintaticamente válido -> `[PASS]`
  - Se houver sintaxe quebrada ou rótulos ilegíveis -> `[FAIL: Sintaxe Mermaid inválida]`

### Regra 4: Árvore ASCII com Comentários Explicativos
- **Critério**: A árvore de arquivos possui anotações explicativas em cada linha mapeada?
- **Teste**: Verificar presença de comentários `# [função do arquivo]` em cada nó da árvore.
- **Resultado**:
  - Se todos os arquivos possuírem responsabilidades declaradas -> `[PASS]`
  - Se houver arquivos sem explicação de propósito -> `[FAIL: Arquivos sem comentário funcional]`

### Regra 5: Disponibilização da Opção de Exportação Direta (MD/PDF)
- **Critério**: A seção `### 6. Opção de Exportação (Arquivo Único / PDF)` está presente ao final da resposta?
- **Teste**: Verificar se a oferta de salvar em arquivo único `.md` ou gerar `.pdf` via `scripts/md-to-pdf.ps1` foi apresentada ou executada.
- **Resultado**:
  - Se a opção ou o link gerado estiver presente -> `[PASS]`
  - Se omitida a opção de exportação -> `[FAIL: Opção de exportação ausente]`
