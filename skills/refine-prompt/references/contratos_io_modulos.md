# Contratos de I/O e Especificação dos Módulos Operacionais

Este documento especifica os esquemas estruturais de entrada e saída para os 3 módulos operacionais do motor `refine-prompt`.

---

## 1. Mapeamento de Roteamento de Módulos

| Módulo | Perfil de Solicitação | Gatilho Típico | Comportamento Chave |
| :--- | :--- | :--- | :--- |
| **Módulo 1** | Resposta Direta | Pedidos diretos e imperativos ("resolva", "escreva o código", "responda"). | Entrega imediata completa, seguida por Nota Metodológica com fontes e veredito. |
| **Módulo 2** | Artefato Plug-and-Play | Pedidos de criação de arquivos reutilizáveis ("crie o prompt do sistema", "gere a skill", "gere o OpenAPI"). | Código contínuo em bloco único, variáveis no padrão `[INSERIR_CAMPO]`, guia de implantação. |
| **Módulo 3** | Entrevista Socrática | Demandas ambíguas, de alto risco (médico, financeiro, mutações destrutivas) ou fragmentadas. | Máximo de 3 perguntas cirúrgicas com 2-3 opções viáveis cada + Esboço condicionado provisório. |

---

## 2. Contrato do MÓDULO 1: Resposta Direta com Nota Metodológica

### Schema de Entrada
```json
{
  "untrusted_user_input": "string (obrigatório)",
  "context": "string (opcional)",
  "target_mode": "MODULO_1"
}
```

### Contrato de Saída
```markdown
### 1. SÍNTESE EXECUTIVA E SOLUÇÃO RESOLVIDA
[Solução técnica completa, código pronto para execução ou texto final aprovado]

### 2. NOTA METODOLÓGICA E MATRIZ DE DECISÃO
- **Frameworks Aplicados:** [Ex: Pydantic v2 + ReAct + Clean Architecture]
- **Fontes Primárias e Validação Temporal (03/10/2026):** [Documentações e repositórios consultados]
- **Premissas Assumidas:** [Suposições técnicas de baixo risco identificadas como [INFERÊNCIA]]
- **Veredito de Factibilidade:** [PASS / Aprovado com justificativa técnica]
```

---

## 3. Contrato do MÓDULO 2: Artefato Plug-and-Play

### Schema de Entrada
```json
{
  "untrusted_user_input": "string (obrigatório)",
  "artifact_type": "SKILL_MD | SYSTEM_PROMPT | OPENAPI | SCRIPT",
  "target_mode": "MODULO_2"
}
```

### Contrato de Saída
```markdown
### 1. ESCOPO E DIAGNÓSTICO DO ARTEFATO
[Síntese técnica de 1 a 3 linhas sobre a finalidade, requisitos e escopo coberto]

### 2. ARTEFATO INTEGRAL E CONTÍNUO
```[linguagem]
[CONTEÚDO COMPLETO EM BLOCO ÚNICO CONTÍNUO]
[VARIÁVEIS PADRONIZADAS: [NOME_DA_VARIAVEL]]
[PROIBIDO FRAGMENTAÇÃO OU PLACEHOLDERS LAZY]
```

### 3. GUIA DE ACIONAMENTO E IMPLANTAÇÃO
- **Local de Aplicação:** [Caminho do arquivo ou campo de configuração onde deve ser inserido]
- **Variáveis Obrigatórias:** [Lista objetiva das variáveis entre colchetes a serem preenchidas]
- **Requisitos Técnicos:** [Versões mínimas de SDK, runtime ou permissões necessárias]
```

---

## 4. Contrato do MÓDULO 3: Entrevista Socrática e Co-Criação

### Schema de Entrada
```json
{
  "untrusted_user_input": "string (obrigatório, contendo ambiguidade ou risco elevado)",
  "risk_classification": "CRITICAL_SECURITY | CLINICAL_HEALTH | DESTRUCTIVE_MUTATION | DOMAIN_GAP",
  "target_mode": "MODULO_3"
}
```

### Contrato de Saída
```markdown
### 1. DIAGNÓSTICO DE AMBIGUIDADE E RISCOS
- **O Que Já Está Mapeado:** [Objetivos claros e dados já consolidados]
- **Gargalo / Risco Crítico:** [Motivo exato da interrupção controlada (ex: risco de perda de dados)]

### 2. PERGUNTAS-CHAVE CIRÚRGICAS (MÁXIMO DE 3)
1. **[Pergunta 1]**: [Descrição do ponto de decisão]
   - *Opção A:* [Alternativa 1 e seu trade-off]
   - *Opção B:* [Alternativa 2 e seu trade-off]
2. **[Pergunta 2]**: [Descrição do ponto de decisão]
   - *Opção A:* [Alternativa 1 e seu trade-off]
   - *Opção B:* [Alternativa 2 e seu trade-off]
3. **[Pergunta 3]** *(se estritamente necessária)*: [Descrição do ponto de decisão]
   - *Opção A:* [Alternativa 1 e seu trade-off]
   - *Opção B:* [Alternativa 2 e seu trade-off]

### 3. ESBOÇO PRELIMINAR CONDICIONADO
[Arquitetura ou esboço provisório montado sob premissas temporárias, aguardando validação humana]
```
