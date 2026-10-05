---
name: organizar-gdrive
description: >-
  Use esta skill sempre que o usuário solicitar organização, varredura, limpeza, triagem ou classificação de pastas e arquivos no Google Drive (unidade G:\Meu Drive ou via MCP google-drive).
license: MIT
metadata:
  version: "1.0.0"
  author: "DriveMaster & Melki"
  category: "Gestão Cloud e Armazenamento Google Drive"
  updated_at: "2026-10-04"
  tags:
    - "google-drive"
    - "mcp-drive"
    - "classificacao"
    - "arquivos"
version: 1.0.0
updated_at: 2026-10-04
author: DriveMaster & Melki
category: Gestão Cloud e Armazenamento Google Drive
---

# Organizar Google Drive ☁️

Procedimento estruturado para inspeção, auditoria, triagem e categorização de pastas e arquivos no Google Drive.

---

## 🎯 Quando Usar
- O usuário pede para organizar ou higienizar arquivos no Google Drive.
- A raiz de `G:\Meu Drive` possui arquivos soltos sem categoria.
- O usuário quer encontrar arquivos duplicados, pesados ou antigos para arquivamento.
- Criação de estruturas de pastas padronizadas no Google Drive.

---

## 🚫 Limites, Exceções e Quando NÃO Usar
- ⚠️ **NUNCA** execute exclusão permanente no Google Drive (`Remove-Item -Recurse -Force`).
- Não utilize para operações em discos locais fora do Google Drive.
- Caso o usuário deseje descartar arquivos, mova-os para uma subpasta `_Quarentena_Descarte/` com aviso explícito.

---

## 📥 Entradas Obrigatórias e Pré-requisitos
1. **Caminho Alvo no Google Drive**: Ex.: `G:\Meu Drive\` ou pasta específica.
2. **Critério de Organização**: Por data, extensão, tipo documental ou taxonomia temática.
3. **Pré-requisito**: Google Drive montado em `G:\Meu Drive` ou MCP `google-drive` ativo.

---

## 🧭 Formas de Acesso ao Google Drive

1. **Unidade Montada no Windows (`G:\Meu Drive`)**:
   - Ideal para operações rápidas em lote via PowerShell (`Get-ChildItem`, `Move-Item`, `Test-Path`).
2. **MCP Server `google-drive`**:
   - Ideal para buscas semânticas, listagem de arquivos recentes na nuvem (`call_mcp_tool` com `ServerName: "google-drive"` e ferramentas `search_files`, `list_recent_files`, `get_file_metadata`).

---

## 📋 Passo a Passo de Execução

### 1. Diagnóstico e Varredura Inicial
Identifique os itens soltos no diretório alvo sem alterar nada:
```powershell
# Listar itens soltos na raiz ou pasta alvo
Get-ChildItem -Path "G:\Meu Drive\" -File | Select-Object Name, Length, LastWriteTime | Sort-Object LastWriteTime -Descending
```

### 2. Taxonomia Padronizada Recomendada
Proponha ou aplique a estrutura padrão:
```text
G:\Meu Drive\
├── 01_Projetos/             # Projetos ativos e repositórios
├── 02_Documentos_Pessoais/  # Contratos, identificações, certidões
├── 03_Estudos_Cursos/       # Materiais de estudo, PDFs, cursos
├── 04_Financeiro/           # Recibos, comprovantes, faturas
├── 05_Trabalho/             # Demandas profissionais e relatórios
└── 99_Arquivo/              # Itens arquivados e congelados
```

### 3. Simulação Obrigatória (Dry-Run)
Antes de mover qualquer arquivo, apresente uma tabela detalhada com:
- Nome atual do arquivo.
- Pasta de destino proposta.
- Novo nome sugerido (se for padronizar data: `YYYY-MM-DD_Nome.ext`).

### 4. Execução Segura
Após a validação:
```powershell
# Cria a pasta de destino caso não exista
if (-not (Test-Path $pastaDestino)) {
    New-Item -ItemType Directory -Path $pastaDestino -Force
}
# Move o arquivo preservando atributos
Move-Item -Path $origem -Destination $pastaDestino
```

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
1. Tabela de Simulação (Dry-Run) antes da execução física.
2. Relatório de Movimentação com contagem de arquivos processados.
3. Links clicáveis de conferência (`file:///G:/Meu Drive/...`).
