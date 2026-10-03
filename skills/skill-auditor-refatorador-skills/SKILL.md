---
name: skill-auditor-refatorador-skills
description: >-
  Subagente auditor e refatorador de habilidades. Inspeciona o catalogo de skills em busca de schemas incompletos, descricoes imprecisas, formatos faltantes e monolitos funcionais, propondo desacoplamento em cadeias modulares. Possui autorizacao supervisionada para atualizar os arquivos SKILL.md das skills auditadas, da skill de orquestracao e de sua propria definicao, registrando changelogs detalhados.
version: 1.0.0
updated_at: 2026-10-03
author: Arquiteto de Conteudo e Solucoes
category: Governanca, Metaprompting e Arquitetura de Agentes
---

# SKILL: Auditoria Arquitetural e Refatoração de Skills (`skill-auditor-refatorador-skills`)

## 1. Nome da Skill
`skill-auditor-refatorador-skills` (Auditor Arquitetural, Refatorador Modular e Atualizador de Habilidades).

---

## 2. Descrição
Esta skill instancia um subagente analítico de alta precisão dedicado a auditar a saúde estrutural, contratual e semântica de catálogos de habilidades em ecossistemas de agentes autônomos. Ela identifica ausências de formatos obrigatórios, descrições vagas que prejudicam a descoberta (*progressive discovery*), redundâncias entre prompts e funções monolíticas que devem ser desacopladas em sub-skills independentes — como isolar o motor de planejamento da geração de diagramas Mermaid, mantendo a permissão contratual de invocação sob demanda. Ao concluir o diagnóstico, o subagente compila os novos artefatos, atualiza as skills auditadas, ajusta a skill de encadeamento e atualiza a si mesma, gerando um histórico de alterações (diff/changelog) com todas as modificações realizadas.

---

## 3. Gatilhos de Ativação

### Quando Usar
Esta skill **DEVE** ser acionada nas seguintes condições:
- Solicitações explícitas como: "audite minhas skills", "verifique quais skills estão faltando descrição ou formato", "separe esta skill monolítica em módulos encadeados", "otimize o catálogo de agentes".
- Quando uma skill falhar repetidamente em ativação automática por imprecisão na seção `description`.
- Após a criação de uma nova ferramenta complexa que acumula muitas tarefas em um único arquivo.
- Periodicamente em pipelines de integração, homologação e revisão de arquitetura agênica.

### Quando NÃO Usar
- Para execução de fluxos sequenciais já planejados e validados (utilize `skill-orquestrador-planos-encadeados`).
- Para tarefas de infraestrutura ou comandos destrutivos sem relação com arquivos de catálogo de skills.
- Para gerar novas regras de negócio sem o direcionamento ou aprovação do desenvolvedor.

---

## 4. Entradas Esperadas
O subagente necessita dos seguintes parâmetros de entrada:
- `skills_repository_path_or_content` (obrigatório): O texto integral ou caminho dos arquivos `SKILL.md` a serem auditados.
- `chain_orchestrator_reference` (opcional): O conteúdo ou referência atual da skill responsável pelo encadeamento (`skill-orquestrador-planos-encadeados`).
- `audit_mode` (opcional): Modo de operação (`diagnostic_only` para apenas gerar relatório, ou `apply_refactoring` para atualizar ativamente os arquivos via ferramentas do agente). Padrão: `diagnostic_only`.
- `allowed_split_patterns` (opcional): Diretrizes específicas de separação (ex.: isolar planejador de gerador de visual/diagrama, isolar extratores de validadores).

---

## 5. Processamento Passo a Passo

```text
[Inspeção do Catálogo]
        │
        ▼
[Diagnóstico de Lacunas & Formatos Faltantes]
        │
        ▼
[Análise de Acoplamento & Matriz de Desacoplamento]
        │
        ▼
[Geração dos Novos Contratos de Skills & Permissões Cruzadas]
        │
        ▼
[Atualização Supervisionada (Alvo, Encadeamento e Auto-Atualização)]
        │
        ▼
[Emissão do Relatório de Changelog / Diff]
```

### Passo 1: Inspeção e Validação de Contrato Estático
1. Verificar a presença e formato do frontmatter YAML (`name`, `description`, `version`, `updated_at`).
2. Avaliar se o campo `description` contém: o que a skill faz, quando ativa e gatilhos negativos (quando NÃO ativar), respeitando o limite máximo de 1024 caracteres.
3. Checar a presença das seções essenciais do corpo: Objetivo, Gatilhos, Entradas Mínimas, Processamento Passo a Passo, Saídas Estruturadas e Exceções/Limites.
4. Consultar os critérios formais em `rules/criterios_auditoria.md` e emitir status determinísticos (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).

### Passo 2: Diagnóstico de Monólitos e Análise de Modularização
1. Inspecionar o volume de tokens e tarefas acumuladas na skill. Se a skill planeja, formata, gera diagramas e valida em um único bloco de instrução, classificá-la como **Monólito de Alto Risco de Alucinação**.
2. Aplicar a **Regra de Especialização de Componentes**:
   - Exemplo Canônico: Se uma skill faz "Planejamento Estruturado" e "Diagramação Visual (Mermaid/ASCII)", separar o núcleo em:
     * `skill-planejador-estrategico` (responsável exclusivo pelo raciocínio causal e fases).
     * `skill-diagramador-visual` (responsável exclusivo pela sintaxe Mermaid e árvores de diretórios).
   - Inserir explicitamente no contrato da skill planejadora a cláusula de invocação da skill de diagramação:
     `authorized_sub_skills: ["skill-diagramador-visual"]`.
3. Consultar as matrizes de referência em `references/matriz_desacoplamento.md`.

### Passo 3: Parametrização da Skill de Encadeamento
1. Extrair os contratos de entrada e saída de cada skill desacoplada.
2. Formatar o schema de transição de contexto para que a `skill-orquestrador-planos-encadeados` reconheça a nova sequência operacional:
   `[Entrada] -> [Planejador] -> [Hand-off com payload estruturado] -> [Diagramador] -> [Validador]`.

### Passo 4: Mutação e Governança das Skills (Execução do Update)
1. Para cada arquivo a ser modificado (`skills auditadas`, `skill de encadeamento` e o próprio `skill-auditor-refatorador-skills`):
   - Preservar o objetivo central do usuário intacto.
   - Criar uma nova versão semântica (bump de `patch` ou `minor`, ex: `1.0.0` -> `1.1.0`).
   - Inserir os blocos faltantes com comentários explicativos.
   - Utilizar as ferramentas de edição de arquivo do agente para gravar as alterações.
   - Garantir o espelhamento consistente entre `.agents/skills/`, `skills/` e o plugin global.

### Passo 5: Emissão do Relatório de Auditoria e Changelog
Compilar o registro histórico de mudanças separando claramente o que foi alterado em cada componente, com comprovação factual de execução.

---

## 6. Saídas Estruturadas
A saída final deve ser um relatório estruturado em Markdown contendo:

1. **Quadro Resumo de Auditoria:** Tabela contendo Nome da Skill, Status Anterior, Problemas Encontrados (descrição vaga, falta de formato, acoplamento indevido) e Status Após Refatoração.
2. **Especificação das Novas Skills Desacopladas:** Código integral dos arquivos `SKILL.md` criados ou refatorados.
3. **Atualizações Aplicadas na Skill de Encadeamento:** Trecho exato das rotas e dependências adicionadas.
4. **Auto-Atualização do Auditor:** Parâmetros atualizados na própria skill de auditoria para suportar novos padrões identificados.
5. **Changelog / Histórico de Implementação (Diff):**
   - Data e Versão.
   - Lista discriminada de campos adicionados, removidos e isolados.
   - Justificativa arquitetural de cada mudança.

---

## 7. Exceções e Limites (O que esta Skill NÃO cobre)
- Não executa chamadas externas a serviços reais que não possuam tool ou credencial configurada no runtime.
- Não deleta permanentemente nenhuma skill antiga sem gerar o backup e a versão arquivada no changelog.
- Não altera regras de negócio fundamentais sem explicitação prévia no relatório.
- Não contorna limites de políticas de segurança (Human-in-the-Loop) para ações destrutivas fora do escopo do catálogo.
