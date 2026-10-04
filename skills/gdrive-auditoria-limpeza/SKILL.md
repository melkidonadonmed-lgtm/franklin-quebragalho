---
name: gdrive-auditoria-limpeza
description: >-
  Audita e higieniza a unidade Google Drive (G:\Meu Drive e MCP), detectando arquivos pesados (>100MB), duplicatas por hash e nome, pastas vazias orfas e executando simulacao segura de descarte com quarentena preventiva (Dry-run).
version: 1.0.0
updated_at: 2026-10-04
author: DriveMaster & Melki
category: Gestao Cloud e Higienizacao de Armazenamento
---

# 1. NOME DA SKILL
`gdrive-auditoria-limpeza` (Auditoria de Armazenamento, Detecção de Duplicatas e Quarentena Segura no Google Drive).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "audite o espaço do meu Google Drive", "encontre arquivos pesados no Drive", "remova duplicados do Drive", "limpe arquivos temporários ou desnecessários no Drive".
- O volume do Google Drive estiver próximo do limite de cota de armazenamento.
- For necessário fazer uma triagem de arquivos zips órfãos, instaladores esquecidos ou cópias repetidas na unidade `G:\Meu Drive`.
- Antes de grandes reestruturações de pastas no Drive, para eliminar entulho previamente.

### Quando NÃO Usar
- Para definir novas estruturas de pastas temáticas ou padronizar nomes com datas ISO (utilize `gdrive-taxonomia-organizacao`).
- Para executar exclusões permanentes e destrutivas (`Remove-Item -Force` definitivo sem confirmação explícita).
- Para operações em pastas do disco local fora do Google Drive (utilize `manutencao-disco-windows`).

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `target_drive_path` (opcional): Diretório alvo no Google Drive (padrão: `G:\Meu Drive`).
- `size_threshold_mb` (opcional): Limiar de tamanho em MB para qualificar como arquivo pesado (padrão: `100`).
- `duplicate_detection_mode` (opcional): `name_and_size` (rápido) ou `hash_sha256` (rigoroso). Padrão: `name_and_size`.
- `quarantine_folder_name` (opcional): Nome da pasta de quarentena preventiva (padrão: `_Quarentena_Descarte`).
- **Pré-requisito**: Google Drive montado em `G:\Meu Drive` ou MCP `google-drive` ativo.

---

## 4. DIRETRIZES DE SEGURANÇA E HIGIENIZAÇÃO (ZERO-LOSS)

Toda auditoria e limpeza no Google Drive segue o protocolo de preservação de dados:

### 4.1. Princípio da Quarentena Preventiva (Sem Exclusão Direta)
- ⚠️ **PROIBIÇÃO DE EXCLUSÃO DEFINITIVA:** É proibido executar comandos como `Remove-Item -Recurse -Force` diretamente em arquivos do Drive.
- Qualquer item indicado para descarte deve ser **movido** para uma subpasta `_Quarentena_Descarte/` com carimbo de data ISO (`_Quarentena_Descarte/YYYY-MM-DD/`).
- O descarte definitivo na lixeira do Google Drive é exclusivo do usuário ou mediante aprovação humana expressa (Human-in-the-Loop).

### 4.2. Detecção de Duplicatas Determinística
1. **Fase 1 (Triagem Rápida):** Agrupamento por tamanho exato em bytes (`Length`) e extensão.
2. **Fase 2 (Confirmação por Hash SHA256):** Para arquivos suspeitos com mesmo tamanho, cálculo do hash criptográfico via PowerShell (`Get-FileHash -Algorithm SHA256`). Apenas itens com hash idêntico são marcados como duplicatas reais.

### 4.3. Rastreamento de Arquivos Pesados e Resíduos
- Varredura de instaladores esquecidos (`.exe`, `.msi`, `.iso`, `.dmg`).
- Varredura de arquivos compactados redundantes (`.zip`, `.rar`, `.7z`, `.tar.gz`).
- Localização de diretórios vazios sem nenhum arquivo interno.

---

## 5. PROCESSO PASSO A PASSO (EXECUÇÃO DEFENSIVA)

```text
[1. Varredura Não-Destrutiva de Armazenamento]
                     │
                     ▼
[2. Detecção de Itens Pesados & Duplicados por Hash]
                     │
                     ▼
[3. Geração do Relatório de Simulação (Dry-Run)]
                     │
                     ▼
[4. Aprovação HITL / Movimentação para Quarentena]
```

### Passo 1: Varredura de Armazenamento
Executar levantamento estatístico no PowerShell 7:
```powershell
# Levantar os 20 maiores arquivos da unidade
Get-ChildItem -Path "G:\Meu Drive" -File -Recurse -ErrorAction SilentlyContinue |
    Sort-Object Length -Descending |
    Select-Object -First 20 Name, @{Name="Tamanho_MB"; Expression={[math]::Round($_.Length / 1MB, 2)}}, FullName
```

### Passo 2: Detecção de Duplicatas Reais
```powershell
# Agrupar arquivos com mesmo tamanho para cálculo de hash
$candidatos = Get-ChildItem -Path "G:\Meu Drive\pasta-alvo" -File -Recurse -ErrorAction SilentlyContinue |
    Group-Object Length | Where-Object { $_.Count -gt 1 }
```

### Passo 3: Geração de Relatório de Simulação (Dry-Run)
Apresentar uma tabela determinística contendo os itens candidatos a quarentena com tamanho total recuperável.

### Passo 4: Movimentação para Quarentena
Após a confirmação do usuário, mover os arquivos duplicados/pesados para a pasta segura:
```powershell
$quarentena = "G:\Meu Drive\_Quarentena_Descarte\$(Get-Date -Format 'yyyy-MM-dd')"
if (!(Test-Path $quarentena)) { New-Item -ItemType Directory -Path $quarentena -Force }
Move-Item -Path "G:\Meu Drive\arquivo-duplicado.zip" -Destination $quarentena -WhatIf
```

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill entrega:
1. **Resumo Executivo de Ocupação:**
   - Total de espaço inspecionado e volume ocupado por arquivos grandes.
2. **Tabela de Arquivos Pesados (> 100MB):**
   - Nome, tamanho em MB, extensão e caminho completo.
3. **Matriz Determinística de Duplicatas Identificadas:**
   - Arquivo original vs. Cópia duplicada, tamanho e hash SHA-256 idêntico.
4. **Plano de Simulação de Quarentena (Dry-Run):**
   - Lista exata de arquivos que serão movidos para `_Quarentena_Descarte/` e confirmação antes de mover.

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA executar `Remove-Item` definitivo na unidade `G:\`.
- Se a unidade `G:\` não estiver conectada (porta Google Drive Desktop fechada), emitir `[FAIL: GDRIVE_NAO_MONTADO]` e sugerir abrir o Google Drive for Desktop ou acionar o MCP `google-drive`.
- Não mover arquivos de sistema do Drive (`desktop.ini`, `.tmp.drivedownload`).
