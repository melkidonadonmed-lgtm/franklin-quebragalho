---
name: manutencao-disco-windows
description: >-
  Executa manutencao, triagem e higienizacao de pastas locais no Windows 11 (Downloads, Desktop, C:\Users\melki\dev\), isolando instaladores antigos, limpando residuos temporarios, organizando experimentos em dev\sandbox\ e sincronizando status de repositorios em dev\repos\ com simulacao preventiva.
license: MIT
metadata:
  version: "1.1.0"
  author: "FileOpsLocal & Melki"
  category: "Sistema Operacional e Automação Local"
  updated_at: "2026-10-14"
  tags:
    - "windows-11"
    - "powershell"
    - "downloads"
    - "disco"
    - "dev-workspace"
version: 1.1.0
updated_at: 2026-10-14
author: FileOpsLocal & Melki
category: Sistema Operacional e Automação Local
---

# 1. NOME DA SKILL
`manutencao-disco-windows` (Manutenção de Armazenamento Local, Triagem de Downloads, Higienização do Desktop e Governança de `C:\Users\melki\dev\`).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "limpe a pasta Downloads", "organize minha Área de Trabalho / Desktop", "audite as pastas em dev/", "encontre instaladores pesados no meu PC", "faxina nas pastas locais".
- O diretório `Downloads` acumular mais de 30 arquivos soltos.
- O Desktop do Windows estiver poluído com arquivos soltos.
- For necessário organizar experimentos soltos para `C:\Users\melki\dev\sandbox\` ou conferir a higiene de `C:\Users\melki\dev\repos\`.

### Quando NÃO Usar
- Para organização de notas intelectuais ou curadoria do cofre Obsidian em `C:\Users\melki\dev\notes\` (utilize `obsidian-vault` ou `curadoria-obsidian-vault`).
- Para organização de arquivos no Google Drive (utilize `gdrive-taxonomia-organizacao` ou `gdrive-auditoria-limpeza`).
- Para modificação de pastas protegidas do sistema Windows (`C:\Windows`, `C:\Program Files`).

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `target_area` (opcional): Área de foco (`downloads`, `desktop`, `dev`, `all`). Padrão: `downloads`.
- `days_threshold` (opcional): Idade mínima em dias para qualificar arquivos antigos para arquivamento (padrão: `30`).
- `clean_heavy_caches` (opcional, booleano): Se deve auditar pastas `node_modules/` ou `.venv/` órfãs fora de projetos ativos. Padrão: `false` (solicitar confirmação).
- **Pré-requisito**: PowerShell 7 (`pwsh`) no Windows 11.

---

## 4. DIRETRIZES DE MANUTENÇÃO E REGRAS DE ISOLAMENTO

A higienização opera sobre áreas estratégicas desta máquina:

### 4.1. Pasta Downloads (`C:\Users\melki\Downloads`)
- **Triagem por Tipo:**
  * **Instaladores:** `.exe`, `.msi`, `.iso`, `.msix` ➔ Mover para `_Instaladores/` ou sugerir quarentena se idade > 30 dias.
  * **Documentos:** `.pdf`, `.docx`, `.xlsx`, `.csv` ➔ Agrupar em `_Documentos_Recebidos/` ou sugerir envio para `G:\Meu Drive\`.
  * **Mídias e Imagens:** `.png`, `.jpg`, `.mp4`, `.webp` ➔ Agrupar em `_Midia/`.
  * **Scripts e Experimentos Avulsos:**
    - Node/JS/TS (`.js`, `.ts`) ➔ Mover para `C:\Users\melki\dev\sandbox\node\`.
    - Python (`.py`) ➔ Mover para `C:\Users\melki\dev\sandbox\python\`.
    - Utilitários PowerShell recorrentes (`.ps1`) ➔ Mover para `C:\Users\melki\dev\tools\`.

### 4.2. Área de Trabalho / Desktop (`C:\Users\melki\OneDrive\Área de Trabalho` / `C:\Users\melki\Desktop`)
- **Preservação de Launchers:** NUNCA remover atalhos vitais (`.lnk`, `.cmd` ou índices HTML em uso pelo usuário).
- **Remoção de Resíduos:** Mover capturas de tela e rascunhos avulsos para pastas de triagem após Dry-Run.

### 4.3. Estrutura Canônica de Desenvolvimento (`C:\Users\melki\dev\`)
- **Topologia Oficial da Máquina:**
  * `C:\Users\melki\dev\repos\` — Repositórios Git ativos (1 por pasta, com nota correspondente em `dev\notes\Projetos\Ativos\<Projeto>.md`).
  * `C:\Users\melki\dev\sandbox\node\` e `C:\Users\melki\dev\sandbox\python\` — Experimentos descartáveis.
  * `C:\Users\melki\dev\skills\` — Agent skills locais reutilizáveis.
  * `C:\Users\melki\dev\tools\` — Scripts utilitários pessoais (ex.: `check-vault-projects.ps1`).
  * `C:\Users\melki\dev\notes\` — Cofre do Obsidian sincronizado com MemPalace (`wing: notes`).
  * `C:\Users\melki\dev\references\templates\` — Templates de documentação para novos repositórios.
- **Invariante de Higiene:** Proibido rodar `npm install` ou `pip install` soltos em `C:\Users\melki\` ou na raiz `C:\Users\melki\dev\`. Quando um repositório for removido da máquina após `git push`, sua nota deve ser movida de `notes\Projetos\Ativos\` para `notes\Projetos\Fora da Máquina\` com `status: fora-da-maquina`.

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

### Passo 2: Geração de Proposta de Movimentação (Dry-Run / WhatIf)
Montar tabela clara com origem, destino e economia esperada antes de qualquer mutação.

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
   - Total de arquivos triados e espaço liberado/organizado.
2. **Tabela de Itens Realocados:**
   - Origem ➔ Destino por categoria funcional.
3. **Auditoria de Higiene `C:\Users\melki\dev\`:**
   - Verificação de dependências soltas e paridade `dev\repos\` ↔ `dev\notes\Projetos\Ativos\`.
4. **Links de Verificação Local:**
   - Links com esquema `file:///` para abertura direta no Windows Explorer.

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA executar `Remove-Item -Recurse -Force` em pastas de usuário sem confirmação interativa explícita.
- NUNCA deletar repositórios em `dev\repos\` sem antes confirmar `git status` limpo, `git push` em dia e autorização HITL.
- NUNCA alterar atalhos ou launchers ativos na Área de Trabalho sem solicitação.
