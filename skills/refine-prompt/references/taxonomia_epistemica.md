# Taxonomia de Premissas Epistêmicas e Auditoria de Factibilidade (Padrão 2026)

Este documento define o framework de classificação epistêmica, ancoragem temporal e controle anti-alucinação utilizado pela skill `refine-prompt`.

---

## 1. Ancoragem Temporal e Base de Conhecimento

- **Data de Referência Fixa**: `2026-10-03`
- **Ponto de Corte de Conhecimento Interno**: Janeiro de 2025.
- **Protocolo de Busca Ativa em Fontes Primárias**:
  - Para qualquer informação posterior a janeiro de 2025, APIs voláteis, versões de bibliotecas (ex.: Pydantic v2, MyPy, TypeScript 5.x, MCP 2026-07-28), consensos científicos recentes ou dados de mercado, o agente **DEVE** realizar busca ativa em fontes primárias oficiais antes de emitir a resposta.
  - É proibido supor parâmetros de bibliotecas inexistentes ou versões fictícias de frameworks.

---

## 2. Taxonomia Epistêmica da Informação

Na conversão de uma ideia bruta em uma especificação executável, toda informação manipulada é categorizada em três níveis determinísticos:

### 2.1. `[FATO]`
- **Definição**: Dado explicitamente fornecido no prompt de entrada pelo usuário ou verificado diretamente em fonte primária consultada durante a execução.
- **Tratamento**: Considerado verdade operativa imutável. Não deve ser alterado ou relativizado.
- **Exemplo**: "O usuário informou que o banco de dados é PostgreSQL 16 hospedado no Cloud SQL."

### 2.2. `[INFERÊNCIA]`
- **Definição**: Premissa técnica sênior de baixo risco adotada autonomamente pelo agente para preencher lacunas de estilo, convenções de código, arquitetura ou organização de arquivos.
- **Tratamento**: Deve ser explicitada na Nota Metodológica (Módulo 1) ou na introdução do artefato (Módulo 2), permitindo que o usuário a ajuste se desejar, mas sem travar a execução com perguntas desnecessárias.
- **Exemplo**: "Como o usuário não especificou o linter para Python, assume-se Ruff e MyPy com tipagem estrita (`strict = true`)."

### 2.3. `[LACUNA]`
- **Definição**: Informação crítica ausente cujo preenchimento autônomo apresenta alto risco (ex: conduta médica vinculante, mutação irreversível de dados em produção, orçamento financeiro ou credencial de segurança).
- **Tratamento**: Impede a entrega direta no Módulo 1. Dispara o **Módulo 3 (Entrevista Socrática)** com no máximo 3 perguntas cirúrgicas e alternativas estruturadas.
- **Exemplo**: "O usuário pediu uma automação de exclusão de arquivos antigos, mas não delimitou o caminho raiz nem a idade de corte."

---

## 3. Protocolo do Veredito de Factibilidade

Antes de expandir uma ideia ou escrever código, o agente avalia se a demanda possui coerência física, matemática, regulatória e computacional:

```text
               [Avaliação da Ideia Bruta]
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
       [Factível]                   [Inviável / Falha]
            │                             │
    [Prossegue para               [Emissão Imediata do
    Classificação e               VEREDITO + Causa Raiz
    Módulos 1, 2 ou 3]            + Alternativa Superior]
```

### Critérios para Emissão do Veredito de Reprovação:
1. **Inviabilidade Física ou Matemática**: Ideias que violem leis da termodinâmica, complexidade computacional insolúvel em tempo polinomial sem aproximação, ou garantias matemáticas impossíveis (ex: quebra de criptografia pós-quântica em CPU convencional).
2. **Arquitetura Flagrantemente Subótima**: Propostas com gargalos insuperáveis de latência, custos proibitivos ou acoplamento que destrua a escalabilidade do sistema.
3. **Vulnerabilidade Crítica de Segurança**: Ideias que exponham credenciais em texto claro, dependam de execução de código remoto inseguro sem sandbox ou violem normas de privacidade (LGPD, HIPAA, GDPR).

### Formato Obrigatório de Reprovação:
```markdown
[VEREDITO: INVIÁVEL/FALHO/SUBÓTIMO]
- **Causa Raiz**: [Explicação técnica detalhada do porquê a abordagem falha]
- **Alternativa Recomendada**: [Solução moderna, viável e superior com base no estado da arte em 03/10/2026]
```
