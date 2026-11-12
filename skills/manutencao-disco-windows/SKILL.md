---
name: manutencao-disco-windows
description: "Executa manutenção de arquivos locais no Windows 11 (Downloads, Desktop e dev/) isolando instaladores antigos e resíduos temporários. Use para higiene de disco local; não use para Google Drive."
version: "1.2.0"
updated_at: "2026-11-12"
compatibility: "Windows 11, pwsh 7+, Python 3.12+"
allowed-tools: ["read_file", "run_command"]
metadata:
  version: "1.2.0"
  updated_at: "2026-11-12"
  author: "FileOpsLocal & Melki"
  category: "Sistema Operacional e Automação Local"
  tags: ["windows-11", "powershell", "downloads", "disco", "dev-workspace"]
---
# Manutenção de Disco Local no Windows 11 (`manutencao-disco-windows`)

## 1. Propósito e Gatilhos de Ativação (Quando Usar)

- Triagem de arquivos soltos em `C:\Users\melki\Downloads` e na Área de Trabalho (`Desktop`).
- Auditoria de higiene de `C:\Users\melki\dev\` (experimentos avulsos em `sandbox/`, caches órfãos e paridade `repos/` <-> `notes/Projetos/Ativos/`).

### Quando NÃO Usar

- Curadoria do cofre Obsidian em `C:\Users\melki\dev\notes\` (use `curadoria-obsidian-vault`).
- Organização ou limpeza do Google Drive `G:\Meu Drive` (use `gdrive-taxonomia-organizacao` ou `gdrive-auditoria-limpeza`).
- Modificação de diretórios protegidos do sistema (`C:\Windows`, `C:\Program Files`).

---

## 2. Entradas Esperadas e Pré-requisitos

- `target_area` (opcional): `downloads` (padrão), `desktop`, `dev` ou `all`.
- `days_threshold` (opcional): Idade mínima em dias para quarentena de instaladores/resíduos (padrão `30`, conforme [`references/politica_retencao_local.json`](references/politica_retencao_local.json)).
- `clean_heavy_caches` (opcional, booleano): Padrão `false` (exige aprovação HITL).
- **Pré-requisito**: PowerShell 7 (`pwsh`) no Windows 11.

---

## 3. Fluxo de Execução Defensiva (Passo a Passo)

1. **Topologia Real de `C:\Users\melki\dev\`**:
   - `repos\` (repositórios Git ativos), `sandbox\node\` e `sandbox\python\` (experimentos descartáveis), `tools\` (scripts utilitários), `notes\` (Obsidian Vault) e `references\templates\`.
   - Proibido rodar `npm install` ou `pip install` soltos na raiz `C:\Users\melki\` ou `C:\Users\melki\dev\`.
2. **Diagnóstico Não-Destrutivo (`-LiteralPath`)**:

   ```powershell
   Get-ChildItem -LiteralPath "C:\Users\melki\Downloads" -File |
       Group-Object Extension |
       Select-Object Name, Count, @{N="Tamanho_MB";E={[math]::Round(($_.Group | Measure-Object Length -Sum).Sum / 1MB, 2)}} |
       Sort-Object Count -Descending
   ```

3. **Simulação (`Dry-Run` / `-WhatIf`) e Verificação de Locks**: Exibir tabela `Origem -> Destino` antes de mover e respeitar os launchers protegidos em [`references/politica_retencao_local.json`](references/politica_retencao_local.json).
4. **Movimentação Segura Sem Glob Bug**:

   ```powershell
   $destInstaladores = "C:\Users\melki\Downloads\_Instaladores"
   if (!(Test-Path -LiteralPath $destInstaladores)) { New-Item -ItemType Directory -Path $destInstaladores -Force }
   Get-ChildItem -LiteralPath "C:\Users\melki\Downloads" -File |
       Where-Object { $_.Extension -in '.exe', '.msi', '.iso', '.msix' } |
       ForEach-Object { Move-Item -LiteralPath $_.FullName -Destination $destInstaladores -WhatIf }
   ```

---

## 4. Saídas e Entregáveis

1. Quadro estatístico de ocupação, tabela de itens realocados e status `[PASS]` / `[FAIL]` segundo [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).
2. Resultado da paridade `dev\repos\` <-> `dev\notes\Projetos\Ativos\` e links `file:///`.

---

## 5. Guardrails e Limites

- **Proibido** executar `Remove-Item -Recurse -Force` sem aprovação humana expressa (HITL).
- **Proibido** remover repositórios em `dev\repos\` sem confirmar `git status` limpo, `git push` atualizado e migração da nota para `notes\Projetos\Fora da Máquina\` (`status: fora-da-maquina`).
- **Proibido** mover ou renomear atalhos/launchers ativos na Área de Trabalho sem solicitação explícita.
