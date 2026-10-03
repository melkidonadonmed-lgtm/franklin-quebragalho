---
name: skill-auditor-refatorador-skills
description: >-
  Subagente auditor e refatorador de habilidades. Inspeciona o catalogo de skills em busca de schemas incompletos, descricoes imprecisas, monólitos e discrepâncias com as preferências de design tátil e paleta mineral do desenvolvedor, propondo desacoplamento em cadeias modulares e atualizando os arquivos SKILL.md com changelogs detalhados.
version: 1.1.0
updated_at: 2026-10-03
author: Arquiteto de Conteudo e Solucoes & Melki
category: Governanca, Metaprompting e Arquitetura de Agentes
---

# SKILL: Auditoria Arquitetural e Refatoração de Skills (`skill-auditor-refatorador-skills`)

## 1. Nome da Skill
`skill-auditor-refatorador-skills` (Auditor Arquitetural, Refatorador Modular, Validador de Preferências e Atualizador de Habilidades).

---

## 2. Descrição
Esta skill instancia um subagente analítico de alta precisão dedicado a auditar a saúde estrutural, contratual, semântica e visual de catálogos de habilidades em ecossistemas de agentes autônomos. Ela identifica ausências de formatos obrigatórios, descrições vagas que prejudicam a descoberta (*progressive discovery*), redundâncias entre prompts e funções monolíticas que devem ser desacopladas em sub-skills independentes — como isolar o motor de planejamento da geração de diagramas Mermaid, mantendo a permissão contratual de invocação sob demanda. Adicionalmente, ela audita a conformidade de cada skill com os 4 módulos canônicos de design tátil e preferências perenes do desenvolvedor (paleta de cores mineral, anti-cobalto, anti-glassmorphism, opções de arquétipos e detecção determinística de discrepâncias). Ao concluir o diagnóstico, o subagente compila os novos artefatos, atualiza as skills auditadas, ajusta a skill de encadeamento e atualiza a si mesma, gerando um histórico de alterações (diff/changelog) com todas as modificações realizadas.

---

## 3. Gatilhos de Ativação

### Quando Usar
Esta skill **DEVE** ser acionada nas seguintes condições:
- Solicitações explícitas como: "audite minhas skills", "verifique quais skills estão faltando descrição, formato ou módulos de design", "separe esta skill monolítica em módulos encadeados", "audite se as skills respeitam minhas preferências de UI e paleta mineral".
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

## 5. Diretrizes Canônicas de Design e Preferências Melki na Auditoria de Skills

Ao auditar e refatorar qualquer skill do catálogo, o auditor valida a presença e a conformidade dos 4 módulos canônicos:

### 5.1. Módulo de Paleta de Cores na Auditoria de Skills
- **Verificação de Cores Minerais:** Garantir que skills que geram código visual, páginas, componentes ou relatórios HTML utilizem a paleta canônica (Canvas Ardósia Grafite `#0B101B`, Cartões Elevados `#162033`, Fundo Claro `#FDFEE9`/`#EEF2F6`, Acentos Petroleum Blue `#2B4C7E`, Slate Navy `#203657`, Ouro Champanhe `#D4AF37`).
- **Verificação Anti-Cobalto:** Assegurar que a skill auditada proíba terminantemente o uso de azul cobalto puro (`#0044FF`, `#233DFF`, `#1D4ED8`) ou cores fluorescentes que agridam a vista.

### 5.2. Módulo de Design Tátil e Qualidade Estrutural das Skills
- **Verificação de Relevo Físico & Anti-Glassmorphism:** A skill auditada deve banir vidros translúcidos difusos (`backdrop-filter: blur`), gradientes plásticos reflexivos e caixas neon.
- **Verificação da Regra de Ouro (Cards Lighter than Canvas):** Exigir que interfaces escuras possuam cartões visivelmente mais claros que o canvas de fundo (`L_card > L_canvas`).
- **Verificação de Sombras Multicamadas e Rim Light:** Exigir sombra física dupla (contato + projeção difusa) e micro-chanfro de luz zenital (`border-top: 1px solid rgba(255, 255, 255, 0.14)`).
- **Verificação de Resiliência Anti-Squish:** Checar se tags e botões utilizam `flex-shrink: 0;` e `white-space: nowrap;`.

### 5.3. Módulo de Opções das Preferências do Desenvolvedor na Refatoração
- **Consulta Estruturada via `ask_question`:** Garantir que a skill ofereça alternativas configuráveis de decisão estética ou técnica ao usuário em vez de adotar caminhos unilaterais arbitrários.
- **Arquétipos Aprovados:** Assegurar suporte aos 5 arquétipos canônicos (*Tactile Matte Minimalist*, *Phantom Obsidian 4K*, *Luxury Deep Blue*, *Gilded Navy Heritage*, *Polar Sand Light*).
- **Supply Chain e Padrão shadcn/ui:** Validar se a skill prioriza componentes de código aberto "copy-paste" desacoplados (shadcn/ui, Radix UI, Lucide Icons, Tailwind UI) em vez de pacotes fechados proprietários.

### 5.4. Módulo de Detecção e Matriz de Discrepâncias com as Preferências
- O auditor confronta o conteúdo das skills contra as preferências de governança perene do Nível 0 (`~/.gemini/memory/global_state.md`), gerando status determinísticos:
  * `[DISC-PALETA]` `[PASS / FAIL]`: Presença de azul cobalto ou cores ácidas fluorescentes.
  * `[DISC-TATIL]` `[PASS / FAIL]`: Ausência de relevo físico, cartões escuros demais ou glassmorphism indevido.
  * `[DISC-OPCOES]` `[PASS / FAIL]`: Ausência de alternativas estruturadas (`ask_question`) em bifurcações.
  * `[DISC-SUPPLY]` `[PASS / FAIL]`: Adoção de dependências opacas caixa-preta sem controle do código.

---

## 6. Processamento Passo a Passo

```text
[Inspeção do Catálogo de Skills]
               │
               ▼
[Diagnóstico de Lacunas, Formatos & Preferências de Design]
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
[Emissão do Relatório de Auditoria, Discrepâncias e Changelog]
```

### Passo 1: Inspeção e Validação de Contrato Estático & Preferências
1. Verificar a presença e formato do frontmatter YAML (`name`, `description`, `version`, `updated_at`).
2. Avaliar se o campo `description` contém: o que a skill faz, quando ativa e gatilhos negativos (quando NÃO ativar), respeitando o limite máximo de 1024 caracteres.
3. Checar a presença das seções essenciais do corpo: Objetivo, Gatilhos, Entradas Mínimas, Módulos de Design e Preferências, Processamento Passo a Passo, Saídas Estruturadas e Exceções/Limites.
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
   - Inserir os blocos dos 4 módulos de design e preferências com comentários explicativos.
   - Utilizar as ferramentas de edição de arquivo do agente para gravar as alterações.
   - Garantir o espelhamento consistente entre `.agents/skills/`, `skills/` e o plugin global.

### Passo 5: Emissão do Relatório de Auditoria, Discrepâncias e Changelog
Compilar o registro histórico de mudanças separando claramente o que foi alterado em cada componente, com comprovação factual de execução no terminal (`python scripts/validate_skills.py`).

---

## 7. Saídas Estruturadas
A saída final deve ser um relatório estruturado em Markdown contendo:

1. **Quadro Resumo de Auditoria:** Tabela contendo Nome da Skill, Status Anterior, Problemas Encontrados (descrição vaga, falta de formato, acoplamento indevido, discrepância com preferências) e Status Após Refatoração.
2. **Matriz de Discrepâncias com as Preferências do Melki:** Relatório detalhado dos 4 módulos avaliados para cada skill auditada (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).
3. **Especificação das Novas Skills Desacopladas:** Código integral dos arquivos `SKILL.md` criados ou refatorados.
4. **Atualizações Aplicadas na Skill de Encadeamento:** Trecho exato das rotas e dependências adicionadas.
5. **Auto-Atualização do Auditor:** Parâmetros atualizados na própria skill de auditoria para suportar novos padrões identificados.
6. **Changelog / Histórico de Implementação (Diff):**
   - Data e Versão.
   - Lista discriminada de campos adicionados, removidos e isolados.
   - Justificativa arquitetural de cada mudança.

---

## 8. Exceções e Limites (O que esta Skill NÃO cobre)
- Não executa chamadas externas a serviços reais que não possuam tool ou credencial configurada no runtime.
- Não deleta permanentemente nenhuma skill antiga sem gerar o backup e a versão arquivada no changelog.
- Não altera regras de negócio fundamentais sem explicitação prévia no relatório.
- Não contorna limites de políticas de segurança (Human-in-the-Loop) para ações destrutivas fora do escopo do catálogo.
