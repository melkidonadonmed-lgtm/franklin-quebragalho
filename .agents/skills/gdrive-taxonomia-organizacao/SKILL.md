---
name: gdrive-taxonomia-organizacao
description: >-
  Estrutura e categoriza arquivos e pastas no Google Drive (G:\Meu Drive e MCP), aplicando taxonomia canonica numerada, padronizacao de nomes com datas ISO (YYYY-MM-DD), higienizacao de caracteres especiais e organizacao tematica sem perdas.
version: 1.0.0
updated_at: 2026-10-04
author: DriveMaster & Melki
category: Gestao Cloud e Taxonomia Documental
---

# 1. NOME DA SKILL
`gdrive-taxonomia-organizacao` (Taxonomia Estruturada, Nomenclatura Canônica ISO e Classificação Temática no Google Drive).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "organize as pastas do meu Google Drive", "arrume os arquivos soltos na raiz do Drive", "padronize os nomes de arquivos com datas no Drive", "crie a estrutura canônica de pastas no Drive".
- A raiz de `G:\Meu Drive\` tiver arquivos dispersos sem categorização semântica.
- For necessário renomear lotes de arquivos para formato uniforme (`YYYY-MM-DD_Nome_Sem_Espaco_Duplo.ext`).
- Criação e manutenção das pastas mestras numeradas de primeiro nível.

### Quando NÃO Usar
- Para varredura de arquivos pesados ou quarentena de descarte de duplicatas (utilize `gdrive-auditoria-limpeza`).
- Para organização de notas locais no Obsidian Vault (utilize `curadoria-obsidian-vault`).
- Para manipulação de arquivos locais em Downloads/Desktop do Windows (utilize `manutencao-disco-windows`).

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `target_folder` (opcional): Pasta do Google Drive a ser organizada (padrão: `G:\Meu Drive\`).
- `taxonomy_profile` (opcional): Perfil de taxonomia (`padrao_melki`, `academico`, `corporativo`). Padrão: `padrao_melki`.
- `apply_iso_dates` (opcional, booleano): Se deve renomear arquivos inserindo a data de modificação/criação no padrão ISO `YYYY-MM-DD_`. Padrão: `false` (solicitar confirmação).
- **Pré-requisito**: Google Drive montado em `G:\Meu Drive\` ou MCP `google-drive` ativo.

---

## 4. TAXONOMIA CANÔNICA DO GOOGLE DRIVE (PADRÃO MELKI)

Todo o ecossistema do Google Drive deve seguir a árvore numerada de primeiro nível:

```text
G:\Meu Drive\
├── 01_Projetos/               # Repositórios, especificações, código e deploys
├── 02_Documentos_Pessoais/    # Identificações, certidões, contratos e saúde
├── 03_Estudos_Cursos/         # Livros, PDFs técnicos, artigos e anotações
├── 04_Financeiro_Fiscal/      # Notas fiscais, comprovantes, extratos e IRPF
├── 05_Midias_Assets/          # Imagens, vídeos, gravações, logotipos e design kits
└── 99_Arquivo_Historico/      # Itens inativos de anos anteriores (ex.: 2024/, 2025/)
```

### 4.1. Regras de Nomenclatura Canônica
1. **Datas ISO no Prefixo:** Documentos com data relevante devem adotar `YYYY-MM-DD_Assunto_Descritivo.ext`.
2. **Higienização de Caracteres:**
   * Substituição de espaços múltiplos por espaço único ou underline (`_`).
   * Eliminação de caracteres que causam problemas de sincronização no Windows/Mac (`#`, `%`, `&`, `{`, `}`, `\`, `<`, `>`, `*`, `?`, `/`, `$`, `!`, `'`, `"`, `:`, `@`).
3. **Preservação de Extensão:** Nunca alterar a extensão original do arquivo.

---

## 5. PROCESSO PASSO A PASSO (EXECUÇÃO DE TAXONOMIA)

### Passo 1: Mapeamento de Itens Soltos
Listar todos os arquivos e diretórios que estão fora da taxonomia padrão:
```powershell
Get-ChildItem -Path "G:\Meu Drive\" -File | Select-Object Name, Length, Extension
```

### Passo 2: Associação com a Taxonomia
Classificar cada arquivo em seu respectivo bucket temático com base na extensão e no nome:
- PDFs de boletos/impostos ➔ `04_Financeiro_Fiscal/`
- Manuais técnicos / E-books ➔ `03_Estudos_Cursos/`
- Contratos / Registros ➔ `02_Documentos_Pessoais/`
- Arquivos de código / Zips de projetos ➔ `01_Projetos/`

### Passo 3: Apresentação da Simulação (Dry-Run)
Exibir ao usuário a matriz de movimentação: `Arquivo Atual ➔ Destino Canônico`.

### Passo 4: Execução com Verificação
Aplicar a movimentação garantindo que o diretório de destino exista:
```powershell
$destino = "G:\Meu Drive\04_Financeiro_Fiscal"
if (!(Test-Path $destino)) { New-Item -ItemType Directory -Path $destino -Force }
Move-Item -Path "G:\Meu Drive\comprovante_pagamento.pdf" -Destination $destino -WhatIf
```

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill entrega:
1. **Mapa da Estrutura Canônica:**
   - Visualização da árvore de pastas com a contagem de arquivos alocados.
2. **Tabela de Arquivos Classificados:**
   - Origem ➔ Destino e nome normalizado.
3. **Resumo de Higienização de Nomes:**
   - Quantidade de nomes corrigidos (espaços múltiplos removidos, datas ISO inseridas).
4. **Links de Acesso Local:**
   - Links com esquema `file:///` para verificação direta no Explorer.

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA mover arquivos compartilhados com links ativos sem avisar o usuário sobre o risco de alterar a hierarquia visível para terceiros.
- NUNCA mesclar ou renomear pastas mestras do sistema do Google Drive (`Computadores`, `Compartilhados comigo`).
- Não tocar em repositórios Git clonados dentro do Drive sem verificar status de branch limpa.
