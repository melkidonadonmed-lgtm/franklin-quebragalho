---
name: organizar-local
description: >-
  Use esta skill para gerenciar, triar, catalogar e organizar pastas e arquivos no computador local (Windows 11), incluindo Downloads, Área de Trabalho, pasta dev e Obsidian Vault.
---

# Organizar Pastas Locais (Windows 11) 💻

Procedimento operacional para triagem, higienização e organização de diretórios locais utilizando PowerShell 7 nativo.

---

## 🎯 Quando Usar
- Limpeza e classificação da pasta `Downloads` ou `Desktop`.
- Triagem de projetos e repositórios em `C:\Users\melki\dev\`.
- Organização de notas e anexos soltos no **Obsidian Vault** (`C:\Users\melki\Documents\Obsidian Vault\`).
- Identificação de arquivos pesados que consom espaço em disco.

---

## 📍 Diretórios de Referência
- **Downloads**: `C:\Users\melki\Downloads`
- **Área de Trabalho**: `C:\Users\melki\OneDrive\Área de Trabalho` (ou `C:\Users\melki\Desktop`)
- **Projetos Dev**: `C:\Users\melki\dev\`
- **Obsidian Vault**: `C:\Users\melki\Documents\Obsidian Vault\`

---

## 📋 Passo a Passo de Execução

### 1. Levantamento de Arquivos por Tipo e Idade
Exemplo de diagnóstico na pasta Downloads:
```powershell
$path = "C:\Users\melki\Downloads"
Get-ChildItem -Path $path -File | Group-Object Extension | Select-Object Name, Count | Sort-Object Count -Descending
```

### 2. Regras de Categorização por Extensão
| Categoria | Extensões | Destino Típico |
| :--- | :--- | :--- |
| **Instaladores** | `.exe`, `.msi`, `.iso` | `_Instaladores/` ou Quarentena |
| **Documentos** | `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.csv` | `_Documentos/` ou `G:\Meu Drive\` |
| **Imagens/Mídia**| `.png`, `.jpg`, `.jpeg`, `.gif`, `.mp4`, `.zip` | `_Midia/` / `_Arquivos_Comprimidos/` |
| **Código/Scripts**| `.py`, `.js`, `.ts`, `.json`, `.sql`, `.ps1` | `C:\Users\melki\dev\scratch\` |

### 3. Simulação Obrigatória (Dry-Run com WhatIf)
Antes de mover, mostre os primeiros 10-20 itens a serem processados:
```powershell
Get-ChildItem -Path "C:\Users\melki\Downloads" -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Select-Object Name, LastWriteTime, Length
```

### 4. Movimentação Segura em Lote
```powershell
$destino = "C:\Users\melki\Downloads\_Arquivo_Antigos"
if (-not (Test-Path $destino)) { New-Item -ItemType Directory -Path $destino -Force }

Get-ChildItem -Path "C:\Users\melki\Downloads" -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | ForEach-Object {
    Move-Item -Path $_.FullName -Destination $destino -Verbose
}
```

### 5. Boas Práticas para o Obsidian Vault
- No Obsidian, arquivos `.md` devem seguir links bidirecionais `[[Nota]]`.
- Anexos (PDFs, imagens) devem ser mantidos na pasta designada de anexos (geralmente `_attachments/` ou `Anexos/`).
- Não modifique a pasta oculta `.obsidian/` sem necessidade explícita.
