# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REFATORAÇÃO DE SKILLS

Para assegurar validações rigorosas e erradicar auditorias fictícias ou simulações vazias, toda checagem do subagente auditor deve classificar cada critério sob um dos três estados determinísticos:
- `[PASS]`: Requisito plenamente satisfeito com evidência empírica e factual no arquivo inspecionado.
- `[FAIL]`: Requisito violado com causa-raiz técnica, arquivo e linha comprovados.
- `[UNVERIFIED]`: Não verificável por falta de insumos suficientes ou indisponibilidade de arquivo no escopo.

---

### Regra 1: Validação de Frontmatter e Schema YAML
- **Critério**: O arquivo `SKILL.md` contém frontmatter YAML válido delimitado por cercas `---`?
- **Campos Obrigatórios**: `name`, `description`, `version`, `updated_at`.
- **Teste**:
  - `name`: minúsculas, hífens, sem espaços ou caracteres especiais.
  - `version`: padrão SemVer (`x.y.z`).
  - `updated_at`: formato ISO (`YYYY-MM-DD`).
- **Classificação**:
  - Se todos os campos e formatos estiverem presentes -> `[PASS]`
  - Se faltar qualquer campo obrigatório ou o YAML for inválido -> `[FAIL: Campo obrigatório ausente ou formato YAML corrompido]`

---

### Regra 2: Qualidade da Descrição e Descoberta Progressiva
- **Critério**: O campo `description` orienta o modelo de forma inequívoca sobre ativação?
- **Teste**:
  - Redação em 3ª pessoa ("Use esta skill quando..." ou "Subagente especialista em...").
  - Contém gatilhos positivos explícitos (o que faz e quando deve ativar).
  - Contém gatilhos negativos explícitos ou limites de escopo (quando NÃO deve ativar).
  - Comprimento estrito menor ou igual a 1024 caracteres para evitar poluição no registro global.
- **Classificação**:
  - Se atender a todos os critérios -> `[PASS]`
  - Se for vaga, exceder 1024 caracteres ou omitir escopo negativo -> `[FAIL: Descrição deficiente para progressive discovery]`

---

### Regra 3: Detecção de Acoplamento Monolítico
- **Critério**: A skill acumula múltiplas responsabilidades funcionais divergentes em um único bloco operacional?
- **Teste**:
  - A skill combina raciocínio causal/planejamento com geração visual/gráfica (ex.: texto analítico + Mermaid/ASCII densos)?
  - A skill combina ingestão de dados brutos com validação e execução em produção no mesmo arquivo sem modularização?
- **Classificação**:
  - Se a responsabilidade for única e modular -> `[PASS]`
  - Se for identificado acoplamento de múltiplas responsabilidades -> `[FAIL: Monólito de alto risco de alucinação detectado]`
  - **Ação Obrigatória em FAIL**: Propor desacoplamento imediato e inserir cláusula `authorized_sub_skills` na skill primária.

---

### Regra 4: Validação de Contrato de Transição de Contexto
- **Critério**: O hand-off entre a skill auditada e a skill de encadeamento possui schema tipado?
- **Teste**:
  - Os inputs e outputs são estruturados em JSON ou Markdown semântico previsível?
  - A skill consome apenas os dados necessários da etapa anterior, sem demandar histórico integral de conversa?
- **Classificação**:
  - Se o contrato de payload estiver declarado e validado -> `[PASS]`
  - Se a passagem de dados for opaca ou depender de contexto residual -> `[FAIL: Ausência de contrato estruturado de transição]`

---

### Regra 5: Governança de Mutação e Preservação de Histórico
- **Critério**: As alterações no catálogo são rastreáveis, seguras e auditáveis?
- **Teste**:
  - Nenhuma skill pré-existente foi deletada sem backup ou registro em changelog?
  - O incremento de versão seguiu SemVer (`patch` para correções textuais, `minor` para novas capacidades, `major` para quebra de contrato)?
  - O relatório final contém o bloco canônico de Changelog / Diff discriminado por arquivo modificado?
- **Classificação**:
  - Se toda mutação for auditada com changelog e versionamento -> `[PASS]`
  - Se houver sobrescrita destrutiva silenciosa -> `[FAIL: Violação de governança de mutação de catálogo]`
