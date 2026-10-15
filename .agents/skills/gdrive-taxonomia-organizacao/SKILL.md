---
name: gdrive-taxonomia-organizacao
description: >-
  Estrutura e categoriza arquivos e pastas no Google Drive (G:\Meu Drive), aplicando a taxonomia canonica numerada real da maquina, padronizacao de nomes com datas ISO (YYYY-MM-DD), higienizacao de caracteres especiais e organizacao tematica sem perdas.
license: MIT
metadata:
  version: "1.1.0"
  author: "DriveMaster & Melki"
  category: "Gestão Cloud e Taxonomia Documental"
  updated_at: "2026-10-14"
  tags:
    - "google-drive"
    - "taxonomia"
    - "datas-iso"
    - "organizacao"
version: 1.1.0
updated_at: 2026-10-14
author: DriveMaster & Melki
category: Gestão Cloud e Taxonomia Documental
---

# 1. NOME DA SKILL
`gdrive-taxonomia-organizacao` (Taxonomia Estruturada, Nomenclatura Canônica ISO e Classificação Temática em `G:\Meu Drive\`).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "organize as pastas do meu Google Drive", "arrume os arquivos soltos na raiz do Drive", "padronize os nomes de arquivos com datas no Drive", "classifique documentos nas pastas numeradas do Drive".
- A raiz de `G:\Meu Drive\` tiver arquivos dispersos sem categorização semântica.
- For necessário renomear lotes de arquivos para formato uniforme (`YYYY-MM-DD_Nome_Sem_Espaco_Duplo.ext`).

### Quando NÃO Usar
- Para varredura de arquivos pesados (>100MB) ou quarentena de descarte de duplicatas por SHA-256 (utilize `gdrive-auditoria-limpeza`).
- Para organização de notas locais no cofre Obsidian em `C:\Users\melki\dev\notes\` (utilize `obsidian-vault` ou `curadoria-obsidian-vault`).
- Para manipulação de arquivos locais em `Downloads`/`Desktop`/`dev` do Windows (utilize `manutencao-disco-windows`).

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `target_folder` (opcional): Pasta do Google Drive a ser organizada (padrão: `G:\Meu Drive\`).
- `taxonomy_profile` (opcional): Perfil de taxonomia (`padrao_melki`). Padrão: `padrao_melki`.
- `apply_iso_dates` (opcional, booleano): Se deve renomear arquivos inserindo a data de modificação/criação no padrão ISO `YYYY-MM-DD_`. Padrão: `false` (solicitar confirmação).
- **Pré-requisito**: Google Drive montado em `G:\Meu Drive\`. **Atenção PowerShell**: Use `-LiteralPath` ao manipular pastas com colchetes como `[01]Projetos`.

---

## 4. TAXONOMIA CANÔNICA DO GOOGLE DRIVE (ESTRUTURA REAL NESTA MÁQUINA)

O ecossistema em `G:\Meu Drive\` segue a árvore temática numerada real desta máquina:

```text
G:\Meu Drive\
├── [01]Projetos/                    # Projetos específicos (ex: 01. App de anatomia, 08_Projeto_App_Scoreboard)
├── 01_Modelos_Rapidos/              # Modelos ágeis de receituários, atestados e condutas
├── 02_Protocolos_e_Medicamentos/    # Guias farmacológicos, protocolos clínicos e posologias
├── 03_Medicina_Faculdade/           # Materiais acadêmicos, aulas, slides e referências médicas
├── 04_Workspace_e_Banco_de_Dados/   # Aplicativos, acervos, briefings, cadernos Colab e AppSheets
├── 05_Banco_dados_apoio_backup/     # Backups estruturados e bases de dados de apoio
├── 07_Gemini_Gems/                  # System prompts, Gems e personas customizadas
├── 09_ui_web_kits/                  # Kits de UI, referências de Design System e dossiês de skills
├── 10_Pessoal/                      # Documentos pessoais, certidões, contratos e financeiro
├── 11_Salvo_do_Chrome/              # Capturas, PDFs e páginas salvas do navegador
├── 12_MCP_Servers/                  # Backups e referências de servidores MCP
├── 15_chaves_api/                   # Referências de chaves em Google Docs (PROIBIDO copiar para repos/notas)
├── 16_Documentos_comp_SUS/          # Formulários e planilhas oficiais do SUS (APAC, LME, SISREG, GAL, SISCAN)
├── 99_Arquivo_Historico/            # Itens históricos congelados de anos/versões anteriores
└── Franklin_Skills_Docs_2026/       # Dossiê legível e comparativo das skills do Franklin Quebra-Galho
```

### 4.1. Regras de Nomenclatura Canônica
1. **Datas ISO no Prefixo:** Documentos com data relevante devem adotar `YYYY-MM-DD_Assunto_Descritivo.ext`.
2. **Higienização de Caracteres:**
   * Substituição de espaços múltiplos por espaço único ou underline (`_`).
   * Eliminação de caracteres problemáticos em nomes de arquivos (`#`, `%`, `&`, `{`, `}`, `\`, `<`, `>`, `*`, `?`, `/`, `$`, `!`, `'`, `"`, `:`, `@`).
3. **Preservação de Extensão:** Nunca alterar a extensão original do arquivo.

---

## 5. PROCESSO PASSO A PASSO (EXECUÇÃO DE TAXONOMIA)

### Passo 1: Mapeamento de Itens Soltos
Listar todos os arquivos soltos na raiz de `G:\Meu Drive\` sem alterar nada:
```powershell
Get-ChildItem -LiteralPath "G:\Meu Drive\" -File | Select-Object Name, Length, Extension, LastWriteTime
```

### Passo 2: Associação com a Taxonomia Real da Máquina
Classificar cada arquivo em sua respectiva pasta temática existente:
- Formulários/fichas do SUS (APAC, LME, GAL, SISCAN, SISREG) ➔ `16_Documentos_comp_SUS/`
- Aulas médicas, slides (`.gslides`) e resumos de faculdade ➔ `03_Medicina_Faculdade/`
- Protocolos clínicos e medicamentos ➔ `02_Protocolos_e_Medicamentos/`
- Prompts, especificações de agentes e Gems ➔ `07_Gemini_Gems/` ou `04_Workspace_e_Banco_de_Dados/`
- Kits de interface, design tokens e dossiês de UI ➔ `09_ui_web_kits/`
- Documentos pessoais, laudos próprios e comprovantes ➔ `10_Pessoal/`
- Arquivos históricos e backups encerrados ➔ `99_Arquivo_Historico/`

### Passo 3: Apresentação da Simulação (Dry-Run)
Exibir ao usuário a matriz de movimentação: `Arquivo Atual ➔ Destino Canônico`.

### Passo 4: Execução com Verificação (`-LiteralPath`)
Aplicar a movimentação utilizando `-LiteralPath` para evitar expansão indevida de colchetes no PowerShell:
```powershell
$destino = "G:\Meu Drive\03_Medicina_Faculdade"
if (!(Test-Path -LiteralPath $destino)) { New-Item -ItemType Directory -Path $destino -Force }
Move-Item -LiteralPath "G:\Meu Drive\Tuberculose Novo modificado.gslides" -Destination $destino -WhatIf
```

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill entrega:
1. **Mapa da Estrutura Canônica:**
   - Visualização das pastas reais de `G:\Meu Drive\` com a contagem de arquivos alocados.
2. **Tabela de Arquivos Classificados:**
   - Origem ➔ Destino e nome normalizado.
3. **Resumo de Higienização de Nomes:**
   - Quantidade de nomes corrigidos (espaços múltiplos removidos, datas ISO inseridas).
4. **Links de Acesso Local:**
   - Links com esquema `file:///` para verificação direta no Explorer.

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA ler, expor ou copiar conteúdos de `15_chaves_api` para repositórios Git ou notas do Obsidian.
- NUNCA mover arquivos compartilhados com links ativos sem avisar o usuário sobre o impacto na hierarquia.
- NUNCA mesclar ou renomear `G:\Outros computadores` (backups de PCs anteriores de julho, agosto e setembro de 2026).
