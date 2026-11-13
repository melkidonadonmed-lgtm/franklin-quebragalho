---
name: gdrive-auditoria-limpeza
description: "Audita e higieniza Google Drive detectando arquivos pesados >100MB, duplicatas por hash e pastas vazias órfãs com Dry-run. Use para limpeza de arquivos duplicados no Drive; não use para disco local."
compatibility: "Windows 11, pwsh 7+, Google Drive Desktop ou workspace-mcp"
metadata:
  version: "1.2.0"
  updated_at: "2026-11-13"
  author: "DriveMaster & Melki"
  category: "Gestão Cloud e Higienização de Armazenamento"
  tags: ["google-drive", "limpeza", "sha256", "dry-run"]
---
# Auditoria de Armazenamento e Quarentena no Google Drive (`gdrive-auditoria-limpeza`)

## 1. Propósito e Gatilhos de Ativação (Quando Usar)

- Detectar arquivos pesados (`> 100 MB`), instaladores/compactados esquecidos (conforme [`references/extensoes_residuos.json`](references/extensoes_residuos.json)), pastas vazias e duplicatas confirmadas por `SHA-256` em `G:\Meu Drive`.
- Preparar plano de quarentena reversível antes de reestruturações taxonômicas.

### Quando NÃO Usar

- Para classificar arquivos nas pastas temáticas ou aplicar prefixos ISO `YYYY-MM-DD` (use `gdrive-taxonomia-organizacao`).
- Para higiene de `Downloads`, `Desktop` ou `C:\Users\melki\dev\` (use `manutencao-disco-windows`).

---

## 2. Entradas Esperadas e Pré-requisitos

- `target_drive_path` (opcional): Padrão `G:\Meu Drive`.
- `size_threshold_mb` (opcional): Padrão `100`.
- `quarantine_folder_name` (opcional): Padrão `_Quarentena_Descarte`.
- **Pré-requisito**: Unidade `G:\Meu Drive` montada (Google Drive for Desktop) ou `workspace-mcp` / skill `gdrive` ativa.

---

## 3. Fluxo de Execução Defensiva (Passo a Passo)

1. **Varredura Não-Destrutiva (`-LiteralPath`)**:

   ```powershell
   Get-ChildItem -LiteralPath "G:\Meu Drive" -File -Recurse -ErrorAction SilentlyContinue |
       Where-Object { $_.FullName -notmatch '15_chaves_api' } |
       Sort-Object Length -Descending |
       Select-Object -First 20 Name, @{N="Tamanho_MB";E={[math]::Round($_.Length / 1MB, 2)}}, FullName
   ```

2. **Confirmação de Duplicatas por Tamanho + `SHA-256`**:
   - Fase 1: Agrupar candidatos com mesmo `Length` em bytes.
   - Fase 2: Confirmar identidade real com `Get-FileHash -LiteralPath $file -Algorithm SHA256` (nunca marcar duplicata apenas pelo nome).
3. **Plano de Simulação (`Dry-Run` / `-WhatIf`)**: Apresentar tabela de impacto com espaço recuperável e aguardar aprovação HITL.
4. **Movimentação para Quarentena Datada**:

   ```powershell
   $quarentena = "G:\Meu Drive\_Quarentena_Descarte\$(Get-Date -Format 'yyyy-MM-dd')"
   if (!(Test-Path -LiteralPath $quarentena)) { New-Item -ItemType Directory -Path $quarentena -Force }
   Move-Item -LiteralPath $itemDuplicado -Destination $quarentena -WhatIf
   ```

---

## 4. Saídas e Entregáveis

1. Resumo de ocupação, tabela de itens `> 100 MB` e matriz de duplicatas com hash `SHA-256`.
2. Plano `Dry-Run` e veredito `[PASS]` / `[FAIL]` segundo [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).

---

## 5. Guardrails e Limites

- **Proibido** executar `Remove-Item` definitivo em `G:\`; todo descarte segue para `_Quarentena_Descarte\YYYY-MM-DD\`.
- **Proibido** inspecionar/expor `15_chaves_api` ou mover metadados de sincronização (`desktop.ini`, `.tmp.drivedownload`, `.gdoc`, `.gsheet`).
- Se `G:\Meu Drive` estiver desmontado, emitir `[FAIL: GDRIVE_NAO_MONTADO]` e orientar montagem ou consulta somente-leitura via `workspace-mcp` (`drive_list_files`).
