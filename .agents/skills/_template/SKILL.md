---
name: template-skill
description: >-
  Modelo padrão para criação de novas skills no Antigravity. Use este template como base ao criar uma nova habilidade ou procedimento para o Franklin Quebra-Galho.
---

# Template de Skill

Breve parágrafo explicando o objetivo principal desta habilidade e o contexto em que ela resolve problemas para o usuário.

---

## 🎯 Quando Usar
- Liste gatilhos e cenários específicos em que o modelo ou o usuário deve acionar esta skill.
- Cenário A: Quando o usuário pedir para executar a tarefa X.
- Cenário B: Quando for detectado o padrão Y.

---

## ⚙️ Pré-requisitos e Dependências
- Ferramentas ou comandos necessários (ex.: PowerShell 7, MCP Server específico).
- Permissões ou arquivos de configuração que devem existir.

---

## 📋 Passo a Passo de Execução

### 1. Coleta de Informações e Validação
- Verifique o ambiente e os parâmetros antes de agir.
- Exemplo de comando seguro:
  ```powershell
  Test-Path "caminho\alvo"
  ```

### 2. Simulação (Dry-run / Preview)
- Sempre que houver movimentação de arquivos ou modificação em lote, apresente um resumo ao usuário antes de aplicar.

### 3. Execução Principal
- Descreva os comandos ou procedimentos de forma clara e modular.

### 4. Verificação de Sucesso
- Como verificar se a tarefa foi concluída corretamente (ex.: checar tamanho do arquivo, verificar código de saída).

---

## 📁 Estrutura Recomendada da Pasta da Skill
```text
skills/<nome-da-skill>/
├── SKILL.md          # Instruções principais (este arquivo)
├── scripts/          # Scripts auxiliares PowerShell / Node
├── references/       # Manuais ou referências detalhadas
└── examples/         # Exemplos de entrada e saída
```
