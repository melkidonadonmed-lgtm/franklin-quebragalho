---
name: template-skill
description: >-
  Modelo padrao oficial para criacao de novas skills no Antigravity e no workspace Franklin Quebra-Galho, estruturado sob divulgacao progressiva, regras deterministicas e cenarios de avaliacao real.
version: 1.1.0
updated_at: 2026-09-27
---

# Template de Skill (Padrao 2026)

Breve paragrafo explicando o objetivo principal desta habilidade e o contexto em que ela resolve problemas para o usuario com confiabilidade e sem alucinacao.

---

## 🎯 Quando Usar
- Liste gatilhos e cenarios especificos em que o modelo ou o usuario deve acionar esta skill.
- Cenario A: Quando o usuario pedir para executar a tarefa X.
- Cenario B: Quando for detectado o padrao Y.

---

## 🚫 Quando NAO Usar
- Cenario de exclusao A (quando outra skill for mais apropriada).
- Cenario de exclusao B (quando a tarefa demandar acoes fora do escopo autorizado).

---

## ⚙️ Pre-requisitos e Dependencias
- Ferramentas ou comandos necessarios (ex.: PowerShell 7, MCP Server especifico).
- Permissoes ou arquivos de configuracao que devem existir antes da execucao.

---

## 📋 Passo a Passo de Execucao (Divulgacao Progressiva)

### 1. Coleta de Informacoes e Validacao Determinística
- Verifique o ambiente e os parametros antes de agir.
- Consulte `rules/criterios_auditoria.md` para aplicar validacoes booleanas (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).
- Exemplo de comando seguro em PowerShell:
  ```powershell
  Test-Path "caminho\alvo"
  ```

### 2. Simulacao (Dry-run / Preview)
- Sempre que houver movimentacao de arquivos, delecoes temporarias ou modificacoes em lote, apresente um resumo ao usuario antes de aplicar.

### 3. Execucao Principal
- Descreva os comandos ou procedimentos de forma modular e defensiva.
- Trate erros e declare limites de passos (`max_steps`) caso utilize ferramentas repetitivas.

### 4. Verificacao e Fechamento
- Valide os resultados gerados sem inventar estatisticas.
- Registre o encerramento com auto-reflexao ou conferencias de regras.

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
- Formato obrigatório da resposta final (tabelas, blocos de código tipados ou links `file:///`).
- Checklist determinístico de verificação pós-execução (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).

---

## 📁 Estrutura Recomendada da Pasta da Skill
```text
.agents/skills/<nome-da-skill>/
├── SKILL.md            # Instrucoes nucleares (este arquivo)
├── references/         # Opcional: Manuais ou dados factuais imutaveis sob demanda
├── rules/              # Opcional: Criterios deterministicos de auditoria/rejeicao
├── scripts/            # Opcional: Scripts auxiliares PowerShell / Node
└── evals/              # Opcional: Cenarios de teste empiricos (evals.json)
```
