---
name: manutencao-disco-windows
description: >-
  Executa manutencao, triagem e higienizacao de pastas locais no Windows 11 (Downloads, Desktop, dev), isolando instaladores antigos, limpando residuos temporarios e arquivando projetos inativos em dev com simulacao preventiva.
version: 1.0.0
updated_at: 2026-10-04
author: FileOpsLocal & Melki
category: Sistema Operacional e Automacao Local
---

# 1. NOME DA SKILL
`manutencao-disco-windows` (Manutenção de Armazenamento Local, Triagem de Downloads, Higienização do Desktop e Arquivamento em Dev).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "limpe a pasta Downloads", "organize minha Área de Trabalho / Desktop", "arquive projetos antigos em dev/", "encontre instaladores pesados no meu PC", "faxina nas pastas locais".
- O diretório `Downloads` acumular mais de 30 arquivos soltos.
- O Desktop do Windows estiver poluído com arquivos soltos sem atalhos dedicados.
- For necessário liberar espaço em disco eliminando caches ou isolando repositórios inativos em `dev/_arquivo/`.

### Quando NÃO Usar
- Para organização de notas intelectuais ou curadoria de conhecimento (utilize `curadoria-obsidian-vault`).
- Para organização de arquivos na nuvem do Google Drive (utilize `gdrive-taxonomia-organizacao` ou `gdrive-auditoria-limpeza`).
- Para modificação de pastas protegidas do sistema Windows (`C:\Windows`, `C:\Program Files`).

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `target_area` (opcional): Área de foco (`downloads`, `desktop`, `dev`, `all`). Padrão: `downloads`.
- `days_threshold` (opcional): Idade mínima em dias para qualificar arquivos antigos para arquivamento (padrão: `30`).
- `clean_heavy_caches` (opcional, booleano): Se deve auditar e sugerir limpeza de pastas `node_modules/` ou `.venv/` em projetos arquivados. Padrão: `false` (solicitar confirmação).
- **Pré-requisito**: PowerShell 7 (`pwsh`) no Windows 11.

---

## 4. DIRETRIZES DE MANUTENÇÃO E REGRAS DE ISOLAMENTO

A higienização opera sobre áreas estratégicas do Windows 11:

### 4.1. Pasta Downloads (`C:\Users\melki\Downloads`)
- **Triagem por Tipo:**
  * **Instaladores:** `.exe`, `.msi`, `.iso`, `.zip` de programas ➔ Mover para `_Instaladores/` ou sugerir quarentena se idade > 30 dias.
  * **Documentos:** `.pdf`, `.docx`, `.xlsx`, `.csv` ➔ Agrupar em `_Documentos_Recebidos/` ou sugerir subir para o Google Drive.
  * **Mídias e Imagens:** `.png`, `.jpg`, `.mp4` ➔ Agrupar em `_Midia/`.
  * **Scripts e Código:** `.py`, `.js`, `.json`, `.sql`, `.ps1` ➔ Mover para `C:\Users\melki\dev\scratch\`.

### 4.2. Área de Trabalho / Desktop (`C:\Users\melki\OneDrive\Área de Trabalho`)
- **Preservação de Launchers:** NUNCA remover atalhos vitais (`Cockpit-Melki.html`, `FrontCraft-Studio.cmd`, `.lnk` de ferramentas).
- **Remoção de Resíduos:** Mover arquivos avulsos (capturas de tela, notas `.txt` temporárias) para pastas de triagem.

### 4.3. Pasta de Desenvolvimento (`C:\Users\melki\dev\`)
- **Arquivamento Inativo:** Projetos sem commits ou alterações há mais de 90 dias são candidatos a serem movidos para `C:\Users\melki\dev\_arquivo/`.
- **Limpeza de Caches de Dependências:** Identificar pastas `node_modules` e `.venv` dentro de projetos arquivados que consom gigabytes sem necessidade.

---

## 5. PROCESSO PASSO A PASSO (EXECUÇÃO DEFENSIVA)

### Passo 1: Diagnóstico Não-Destrutivo
Mapear a quantidade de arquivos e extensões no alvo:
```powershell
$path = "C:\Users\melki\Downloads"
Get-ChildItem -Path $path -File |
    Group-Object Extension |
    Select-Object Name, Count, @{Name="Tamanho_MB"; Expression={[math]::Round(($_.Group | Measure-Object Length -Sum).Sum / 1MB, 2)}} |
    Sort-Object Count -Descending
```

### Passo 2: Geração de Proposta de Movimentação (WhatIf)
Montar tabela clara com origem, destino e economia esperada.

### Passo 3: Execução Segura com Salvaguarda
Executar as movimentações garantindo a criação prévia dos diretórios de destino:
```powershell
$destInstaladores = "C:\Users\melki\Downloads\_Instaladores"
if (!(Test-Path $destInstaladores)) { New-Item -ItemType Directory -Path $destInstaladores -Force }
Get-ChildItem -Path "C:\Users\melki\Downloads" -File -Include *.exe, *.msi |
    Move-Item -Destination $destInstaladores -WhatIf
```

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill entrega:
1. **Quadro Estatístico de Ocupação:**
   - Total de arquivos triados e espaço liberado.
2. **Tabela de Itens Realocados:**
   - Origem ➔ Destino por categoria funcional.
3. **Alerta de Resíduos Pesados:**
   - Lista de instaladores ou pastas `node_modules` candidatas a descarte mediante aprovação explícita.
4. **Links de Verificação Local:**
   - Links com esquema `file:///` para abertura no Windows Explorer.

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA executar `Remove-Item -Recurse -Force` em pastas de usuário sem confirmação interativa.
- NUNCA deletar projetos em `dev/`; apenas arquivar para `dev/_arquivo/`.
- NUNCA alterar atalhos do Cockpit Melki ou launchers `.cmd` na Área de Trabalho.
