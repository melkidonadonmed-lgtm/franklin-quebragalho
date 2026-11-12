---
name: gdrive-taxonomia-organizacao
description: "Estrutura e categoriza pastas no Google Drive aplicando taxonomia canônica numerada e padronização de datas ISO YYYY-MM-DD. Use para organizar taxonomia no Drive; não use para exclusão de duplicatas."
version: "1.2.0"
updated_at: "2026-11-12"
compatibility: "Windows 11, pwsh 7+, Google Drive Desktop ou workspace-mcp"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "1.2.0"
  updated_at: "2026-11-12"
  author: "DriveMaster & Melki"
  category: "Gestão Cloud e Taxonomia Documental"
  tags: ["google-drive", "taxonomia", "datas-iso", "organizacao"]
---
# Taxonomia Numerada e Datas ISO no Google Drive (`gdrive-taxonomia-organizacao`)

## 1. Propósito e Gatilhos de Ativação (Quando Usar)

- Classificar arquivos soltos na raiz de `G:\Meu Drive\` dentro das pastas numeradas reais da máquina definidas em [`references/taxonomia_padrao.json`](references/taxonomia_padrao.json).
- Padronizar lotes de nomes no formato `YYYY-MM-DD_Assunto_Descritivo.ext` preservando a extensão original.

### Quando NÃO Usar

- Varredura de arquivos `> 100 MB` ou quarentena de duplicatas por `SHA-256` (use `gdrive-auditoria-limpeza`).
- Notas do Obsidian Vault (`curadoria-obsidian-vault`) ou disco local (`manutencao-disco-windows`).

---

## 2. Entradas Esperadas e Pré-requisitos

- `target_folder` (opcional): Padrão `G:\Meu Drive\`.
- `apply_iso_dates` (opcional, booleano): Padrão `false` (exige confirmação HITL antes de renomear em lote).
- **Pré-requisito**: `G:\Meu Drive\` montado (ou consulta via `workspace-mcp` / skill `gdrive`). No PowerShell, usar sempre `-LiteralPath` por causa de colchetes como `[01]Projetos`.

---

## 3. Fluxo de Execução (Passo a Passo)

1. **Mapeamento Não-Destrutivo**:

   ```powershell
   Get-ChildItem -LiteralPath "G:\Meu Drive\" -File | Select-Object Name, Length, Extension, LastWriteTime
   ```

2. **Classificação contra a Taxonomia Canônica ([`references/taxonomia_padrao.json`](references/taxonomia_padrao.json))**:
   - `[01]Projetos`, `01_Modelos_Rapidos`, `02_Protocolos_e_Medicamentos`, `03_Medicina_Faculdade`, `04_Workspace_e_Banco_de_Dados`, `05_Banco_dados_apoio_backup`, `07_Gemini_Gems`, `09_ui_web_kits`, `10_Pessoal`, `11_Salvo_do_Chrome`, `12_MCP_Servers`, `16_Documentos_comp_SUS`, `99_Arquivo_Historico` e `Franklin_Skills_Docs_2026`.
   - Higienizar espaços duplos e caracteres ilegais sem alterar a extensão.
3. **Simulação (`Dry-Run` / `-WhatIf`) e Aprovação HITL**: Exibir matriz `Arquivo Atual -> Destino Canônico` antes de mover.
4. **Execução Segura com `-LiteralPath`**:

   ```powershell
   $destino = "G:\Meu Drive\03_Medicina_Faculdade"
   Move-Item -LiteralPath $arquivoOrigem -Destination $destino -WhatIf
   ```

---

## 4. Saídas e Entregáveis

1. Tabela `Origem -> Destino Canônico` e resumo de nomes normalizados (`YYYY-MM-DD`).
2. Veredito `[PASS]` / `[FAIL]` segundo [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md) e links `file:///`.

---

## 5. Guardrails e Limites

- **Proibido** ler, mover ou expor `15_chaves_api` em repositórios Git ou notas do Obsidian.
- **Proibido** criar pastas paralelas fora da árvore canônica sem autorização humana ou alterar `G:\Outros computadores`.
- Avisar explicitamente antes de mover arquivos compartilhados com links ativos.
