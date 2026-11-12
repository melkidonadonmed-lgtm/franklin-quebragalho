---
name: curadoria-obsidian-vault
description: "Audita e higieniza o cofre do Obsidian validando frontmatter YAML, links bidirecionais Wikilinks e sincronia com MemPalace wing notes. Use para curadoria do vault; não use para Google Drive."
version: "1.3.0"
updated_at: "2026-11-12"
compatibility: "Windows 11, Python 3.12+, pwsh 7+, MemPalace MCP"
allowed-tools: ["read_file", "write_file", "edit_file", "run_command", "call_mcp_tool"]
metadata:
  version: "1.3.0"
  updated_at: "2026-11-12"
  author: "VaultMaster & Melki"
  category: "Gestão de Conhecimento e PKM"
  tags: ["obsidian", "wikilinks", "frontmatter", "mempalace", "hybrid-search", "anexos-orfaos"]
---
# Curadoria e Governança do Obsidian Vault (`curadoria-obsidian-vault`)

## 1. Propósito e Gatilhos de Ativação (Quando Usar)

- Auditar a integridade estrutural de `C:\Users\melki\dev\notes\`: `[[Wikilinks]]` quebrados, frontmatter YAML ausente, notas monolíticas (`> 25 KB`), pressão em `Inbox/` e anexos órfãos.
- Conferir paridade entre repositórios locais (`dev\repos\`) e notas de projeto (`notes\Projetos\Ativos\`) e sincronizar com MemPalace (`wing: notes`).

### Quando NÃO Usar

- Leitura/escrita rápida cotidiana de uma nota específica (use `obsidian-vault`).
- Higienização de `Downloads`/`Desktop`/`dev` (use `manutencao-disco-windows`) ou Google Drive (`gdrive-auditoria-limpeza`).

---

## 2. Entradas Esperadas e Pré-requisitos

- `vault_path` (opcional): Padrão `C:\Users\melki\dev\notes\`, conforme topologia em [`references/estrutura_vault_padrao.json`](references/estrutura_vault_padrao.json).
- `audit_type` (opcional): `completa` (padrão), `anexos_orfaos`, `links_quebrados`, `frontmatter`, `projetos_repos`.
- `orphan_quarantine_folder` (opcional): Padrão `Arquivo/_anexos_orfaos`.
- **Pré-requisito**: Acesso a `C:\Users\melki\dev\notes\` e índice unificado MemPalace (`~/.config/mempalace`).

---

## 3. Fluxo de Execução (Passo a Passo)

1. **Varredura Determinística e Paridade de Projetos**:

   ```powershell
   $env:PYTHONUTF8 = "1"
   uv run python skills/curadoria-obsidian-vault/scripts/vault_hygiene_scanner.py --json
   pwsh "C:\Users\melki\dev\tools\check-vault-projects.ps1"
   ```

2. **Auditoria de Frontmatter, Links e Anexos Órfãos**:
   - Exigir `title`, `date: YYYY-MM-DD` e `tags` em notas estruturadas (e `type: projeto`, `status`, `repo`, `github`, `stack` em `Projetos/Ativos/`).
   - Identificar anexos sem referência `![[...]]` ou `![](...)` em todo o cofre e propor quarentena em `Arquivo/_anexos_orfaos/` (Dry-Run).
   - Aplicar regras de invalidação temporal (`status: arquivado` / *split* `< 25 KB`) conforme [`references/protocolo_governanca_memoria_2026.md`](references/protocolo_governanca_memoria_2026.md).
3. **Reindexação Seccional, Grafo SQLite e MemPalace (Sem Lock Concorrente)**:
   - Atualizar índice seccional (`scripts/vault_palace_search.py --rebuild`) e grafo (`scripts/vault_kg_hydrator.py`).
   - Quando o servidor MCP `mempalace` estiver ativo na sessão, acionar `mempalace_sync` / `mempalace_mine` via `call_mcp_tool` (`wing="notes"`) em vez de subprocesso concorrente.

---

## 4. Saídas e Entregáveis

1. Quadro de saúde por sala (`Inbox`, `Projetos`, `Memória`, `Medicina`, `Arquivo`) e status `[PASS]` / `[FAIL]` segundo [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).
2. Lista de `[[Wikilinks]]` quebrados, notas sem YAML e anexos órfãos candidatos a quarentena.
3. Status de paridade `check-vault-projects.ps1` e sincronização MemPalace (`wing: notes`).

---

## 5. Guardrails e Limites

- **Proibido** modificar `.obsidian/` ou `.trash/`.
- **Proibido** apagar ou truncar notas autorais; arquivar em `Arquivo/` após aprovação HITL e nunca persistir PII/PHI ou segredos de API.
- **Proibido** renomear notas sem atualizar simultaneamente os `[[Wikilinks]]` bidirecionais.
