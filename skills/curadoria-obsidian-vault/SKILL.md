---
name: curadoria-obsidian-vault
description: >-
  Audita e gerencia o cofre Obsidian Vault (C:\Users\melki\Documents\Obsidian Vault\), validando frontmatter YAML, links bidirecionais [[Wikilinks]], consistencia de tags, deteccao de anexos orfaos e organizacao de pastas de conhecimento sem perda de dados.
version: 1.0.0
updated_at: 2026-10-04
author: VaultMaster & Melki
category: Gestao de Conhecimento e PKM
---

# 1. NOME DA SKILL
`curadoria-obsidian-vault` (Curadoria Estrutural, Higienização de Metadados e Integridade de Conhecimento no Obsidian Vault).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "organize meu Obsidian", "verifique links quebrados no vault", "limpe anexos órfãos no Obsidian", "padronize as tags e frontmatter das notas", "faça a curadoria do meu cofre".
- Notas soltas acumularem-se na pasta `00_Inbox/` ou na raiz do vault.
- Houver suspeita de imagens ou PDFs na pasta de anexos que não são mais referenciados por nenhuma nota.
- Antes de exportar relatórios ou notas técnicas para documentação de projetos.

### Quando NÃO Usar
- Para manipulação de arquivos executáveis ou faxina em Downloads do Windows (utilize `manutencao-disco-windows`).
- Para modificação da pasta interna de plugins e temas do Obsidian (`.obsidian/`).
- Para exclusão definitiva de notas ou ideias anotadas.

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `vault_path` (opcional): Caminho do Obsidian Vault (padrão: `C:\Users\melki\Documents\Obsidian Vault\`).
- `audit_type` (opcional): `completa`, `anexos_orfaos`, `links_quebrados`, `frontmatter`. Padrão: `completa`.
- `orphan_quarantine_folder` (opcional): Subpasta para onde mover anexos não referenciados (padrão: `_anexos_orfaos`).
- **Pré-requisito**: Acesso local ao diretório do cofre no Windows 11.

---

## 4. DIRETRIZES DE INTEGRIDADE DO CONHECIMENTO (PKM)

A curadoria do Obsidian Vault obedece aos seguintes pilares:

### 4.1. Preservação Absoluta de Conteúdo Intelectual
- NUNCA apagar uma nota que contenha texto gerado pelo usuário.
- Notas em branco (0 bytes ou apenas espaços) podem ser sugeridas para exclusão apenas mediante relatório prévio.

### 4.2. Estrutura Canônica de Pastas do Vault (Padrão PARA / Melki)
```text
C:\Users\melki\Documents\Obsidian Vault\
├── 00_Inbox/          # Notas rápidas, capturas e ideias brutas a triar
├── 01_Projetos/       # Notas de projetos ativos com entregáveis definidos
├── 02_Areas/          # Áreas de responsabilidade contínua (Saúde, Finanças, Dev)
├── 03_Recursos/       # Materiais de referência, artigos, resumos e manuais
├── 04_Arquivo/        # Notas de projetos concluídos ou históricos
└── _anexos/           # Imagens, prints, PDFs embutidos em notas
```

### 4.3. Padronização de Frontmatter YAML
Toda nota estruturada deve possuir metadados válidos:
```yaml
---
title: Nome da Nota
date: YYYY-MM-DD
tags:
  - categoria/subcategoria
aliases:
  - Sinônimo de Busca
---
```

### 4.4. Integridade de Links Bidirecionais e Anexos
- Varredura de `[[Wikilinks]]` apontando para notas inexistentes.
- Rastreamento de arquivos em `_anexos/` que não aparecem em nenhuma ocorrência de `![[arquivo]]` ou `![](arquivo)` em todas as notas do cofre.

---

## 5. PROCESSO PASSO A PASSO (EXECUÇÃO DE CURADORIA)

### Passo 1: Leitura da Árvore de Notas
Mapear todos os arquivos `.md` e seus respectivos metadados:
```powershell
$vault = "C:\Users\melki\Documents\Obsidian Vault"
$notas = Get-ChildItem -Path $vault -Filter *.md -Recurse | Where-Object { $_.FullName -notmatch '\\\.obsidian\\' }
```

### Passo 2: Detecção de Anexos Órfãos
1. Coletar a lista de todos os anexos em `_anexos/`.
2. Verificar ocorrência do nome de cada anexo dentro do texto de todas as notas `.md`.
3. Anexos sem nenhuma correspondência são marcados como órfãos.

### Passo 3: Auditoria de Links e Frontmatter
Identificar notas sem cabeçalho YAML e notas com links quebrados.

### Passo 4: Apresentação do Relatório e Realocação Segura
Apresentar o diagnóstico determinístico. Ao mover anexos órfãos, transferi-los para `_anexos_orfaos/` com WhatIf.

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill entrega:
1. **Quadro de Saúde do Cofre (Vault Health):**
   - Total de notas ativas, anexos e notas na pasta `00_Inbox/`.
2. **Relatório de Anexos Órfãos:**
   - Lista de imagens/PDFs sem vínculos em nenhuma nota e economia de espaço.
3. **Diagnóstico de Links Quebrados:**
   - Nome da nota de origem e o link que aponta para destino inexistente.
4. **Resumo de Triagem de Inbox:**
   - Sugestão de encaminhamento de notas brutas para `01_Projetos` ou `02_Areas`.

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA modificar arquivos da pasta `.obsidian/` (configurações de plugins, temas ou workspaces).
- NUNCA deletar anexos órfãos permanentemente; movê-los para `_anexos_orfaos/`.
- Não alterar links existentes sem atualizar simultaneamente o arquivo de destino para evitar links quebrados em cascata.
