# Minhas Skills (MY SKILLS)

> **Manifesto, Catálogo de Ciclo de Vida e Histórico de Versões de Skills**

Este repositório é a incubadora central de skills do **Franklin Quebra-Galho**. Cada skill encapsula um procedimento, automação ou runbook especializado que o agente pode carregar sob demanda (*progressive disclosure*).

---

## 🚦 Tabela de Ciclo de Vida das Skills

| Ícone | Status | Descrição |
| :---: | :--- | :--- |
| 💡 | **Ideia** | Rascunho de conceito ou necessidade levantada no dia a dia. |
| 🧪 | **Em Teste** | Implementada em `.agents/skills/<nome>/`, passando por cenários de teste reais. |
| ✅ | **Validada** | Fluxo testado com sucesso, documentação completa e tratamento de erros ok. |
| 🚀 | **Produção** | Skill consolidada, estável e ativada rotineiramente pelo orquestrador. |

---

## 📦 Catálogo de Skills do Workspace

| Skill | Versão | Status | Descrição Curta | Localização |
| :--- | :---: | :---: | :--- | :--- |
| **`organizar-gdrive`** | `v1.0.0` | 🧪 Em Teste | Varredura, categorização, higienização e organização de arquivos no Google Drive (`G:\Meu Drive` e MCP). | [.agents/skills/organizar-gdrive/](file:///c:/Users/melki/Documents/antigravity/wonderful-franklin/.agents/skills/organizar-gdrive/SKILL.md) |
| **`organizar-local`** | `v1.0.0` | 🧪 Em Teste | Rotinas de organização em pastas locais do Windows 11 (Downloads, Desktop, dev, Obsidian) via PowerShell. | [.agents/skills/organizar-local/](file:///c:/Users/melki/Documents/antigravity/wonderful-franklin/.agents/skills/organizar-local/SKILL.md) |
| **`gerar-docs-pdf`** | `v1.0.0` | 🧪 Em Teste | Criação de documentos Markdown formatados e conversão automatizada para PDF de alta fidelidade visual. | [.agents/skills/gerar-docs-pdf/](file:///c:/Users/melki/Documents/antigravity/wonderful-franklin/.agents/skills/gerar-docs-pdf/SKILL.md) |
| **`organizador-fluxo-arvore-arquivos`** | `v1.0.0` | 🧪 Em Teste | Converte ideias brutas em fluxos visuais Mermaid, árvores de arquivos comentadas e planos de execução enxutos. | [.agents/skills/organizador-fluxo-arvore-arquivos/](file:///c:/Users/melki/Documents/antigravity/wonderful-franklin/.agents/skills/organizador-fluxo-arvore-arquivos/SKILL.md) |
| **`evoluir-skills`** | `v1.0.0` | ✅ Validada | Protocolo de engenharia de skills: como conceber, codificar `SKILL.md`, testar, versionar e refinar. | [.agents/skills/evoluir-skills/](file:///c:/Users/melki/Documents/antigravity/wonderful-franklin/.agents/skills/evoluir-skills/SKILL.md) |
| **`_template`** | `v1.0.0` | 🚀 Produção | Modelo base oficial para criação imediata de novas skills do Antigravity. | [.agents/skills/_template/](file:///c:/Users/melki/Documents/antigravity/wonderful-franklin/.agents/skills/_template/SKILL.md) |

---

## 📜 Histórico de Versões e Contexto (Changelog)

### [2026-09-27] - Inclusão da Skill `organizador-fluxo-arvore-arquivos` (v1.0.0)
- **Nova Habilidade Registrada**: Adicionada a skill `organizador-fluxo-arvore-arquivos` para traduzir ideias de software e processos em diagramas Mermaid intuitivos e árvores ASCII comentadas de arquivos, com controle de versão semântico e preservação integral do pedido original.

### [2026-09-27] - Inicialização do Laboratório de Skills (v1.0.0)
- **Criação do Framework**: Estruturação inicial do workspace `franklin-quebra-galho`.
- **Skill `_template`**: Criado modelo com frontmatter oficial YAML (`name`, `description`) e subpastas recomendadas (`scripts/`, `references/`).
- **Skill `organizar-gdrive`**: Adicionado fluxo de inspeção no `G:\Meu Drive` com regras de dry-run e integração MCP `google-drive`.
- **Skill `organizar-local`**: Definidas rotinas de triagem para pastas Windows (`Downloads`, `Desktop`, `dev/`) usando cmdlets nativos do PowerShell.
- **Skill `gerar-docs-pdf`**: Desenvolvido fluxo de criação de notas compatíveis com Obsidian e script de conversão de Markdown para PDF via Edge/Chrome headless.
- **Skill `evoluir-skills`**: Documentado o procedimento de melhoria contínua de skills com histórico de evolução e métricas de ativação.

---

## 🛠️ Como Criar e Testar uma Nova Skill

1. **Duplique o Template**:
   Copie a pasta `.agents/skills/_template/` para `.agents/skills/<sua-nova-skill>/`.
2. **Defina o Frontmatter**:
   - `name`: Nome em minúsculas separado por hífens (ex.: `limpar-cache-dev`).
   - `description`: Descreva em terceira pessoa **o que** a skill faz e **quando** deve ser ativada.
3. **Adicione os Passos e Scripts**:
   - Mantenha o `SKILL.md` conciso (progressivo).
   - Coloque comandos pesados ou scripts em `scripts/`.
4. **Teste a Ativação**:
   - Faça uma pergunta de teste simulando a intenção do usuário e confirme se o agente ativa a skill.
5. **Registre no Manifesto**:
   - Adicione a linha correspondente na tabela acima e adicione uma entrada de changelog no histórico.
