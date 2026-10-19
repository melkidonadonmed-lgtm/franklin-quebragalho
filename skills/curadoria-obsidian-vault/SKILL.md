---
name: curadoria-obsidian-vault
description: >-
  Audita e higieniza estruturalmente o cofre do Obsidian (C:\Users\melki\dev\notes\), validando frontmatter YAML, links bidirecionais [[Wikilinks]], paridade de projetos ativos com dev\repos, deteccao de anexos orfaos e sincronizacao com MemPalace (wing: notes) sem perda de dados.
license: MIT
metadata:
  version: "1.2.0"
  author: "VaultMaster & Melki"
  category: "Gestão de Conhecimento e PKM"
  updated_at: "2026-10-19"
  tags:
    - "obsidian"
    - "wikilinks"
    - "frontmatter"
    - "mempalace"
    - "hybrid-search"
    - "anexos-orfaos"
version: 1.2.0
updated_at: 2026-10-19
author: VaultMaster & Melki
category: Gestão de Conhecimento e PKM
---

# 1. NOME DA SKILL
`curadoria-obsidian-vault` (Auditoria Estrutural, Higienização de Metadados, Paridade de Projetos e Integridade de Links no Cofre Obsidian `C:\Users\melki\dev\notes\`).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "audite a integridade do meu Obsidian", "verifique links quebrados no cofre", "limpe anexos órfãos em dev/notes", "padronize as tags e frontmatter das notas", "confira a paridade entre projetos e notas".
- Notas soltas acumularem-se na pasta `Inbox/` ou na raiz de `C:\Users\melki\dev\notes\`.
- Houver suspeita de imagens ou PDFs sem referência cruzada nas notas do cofre.
- Complementarmente à skill global `obsidian-vault` (que gerencia leitura/escrita cotidiana por módulos), quando o foco for auditoria determinística de saúde do cofre.

### Quando NÃO Usar
- Para consulta rápida de notas médicas, registro de decisões ou leitura modular cotidiana do cofre (utilize a skill `obsidian-vault`).
- Para manipulação de instaladores ou faxina em Downloads/Desktop do Windows (utilize `manutencao-disco-windows`).
- Para modificação da pasta interna de configuração do Obsidian (`.obsidian/`).
- Para exclusão definitiva de notas ou ideias anotadas.

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `vault_path` (opcional): Caminho do cofre do Obsidian (padrão canônico desta máquina: `C:\Users\melki\dev\notes\`).
- `audit_type` (opcional): `completa`, `anexos_orfaos`, `links_quebrados`, `frontmatter`, `projetos_repos`. Padrão: `completa`.
- `orphan_quarantine_folder` (opcional): Subpasta para onde mover anexos não referenciados (padrão: `Arquivo/_anexos_orfaos`).
- **Pré-requisito**: Acesso local a `C:\Users\melki\dev\notes\` e CLI `mempalace` disponível no ambiente.

---

## 4. DIRETRIZES DE INTEGRIDADE DO CONHECIMENTO (PKM + MEMPALACE)

A curadoria de `C:\Users\melki\dev\notes\` obedece aos seguintes pilares:

### 4.1. Preservação Absoluta de Conteúdo Intelectual e Sigilo
- NUNCA apagar uma nota que contenha conteúdo autoral; notas históricas recebem `type: historico` ou seguem para `Arquivo/`.
- NUNCA permitir senhas, tokens de API ou dados identificáveis de pacientes (PII/PHI) nas notas do cofre.

### 4.2. Estrutura Canônica de Pastas do Cofre (Nomes Simples Sem Números/Emojis)
```text
C:\Users\melki\dev\notes\
├── Inbox/             # Capturas rápidas e ideias brutas a triar
├── Diário/            # Notas diárias e registros cronológicos
├── Medicina/          # Condutas clínicas, resumos, protocolos e plantões
├── Pessoal/           # Gestão pessoal, finanças e rotinas TDAH
├── Projetos/          # Ativos/ (espelha dev\repos\<Projeto>) e Fora da Máquina/
├── Interesses/        # Estudos de IA, MCP, automações e leituras
├── Modelos/           # Templates padronizados (ex: Template - Projeto Dev.md)
├── Arquivo/           # Notas históricas e anexos em quarentena
└── Memória/           # Decisões.md, Ambiente Dev (PC atual).md, Preferências
```

### 4.3. Padronização de Frontmatter YAML
Toda nota estruturada deve possuir metadados válidos em UTF-8 sem BOM:
```yaml
---
title: Nome da Nota
date: YYYY-MM-DD
tags:
  - categoria/subcategoria
---
```
Para notas em `Projetos/Ativos/<Projeto>.md`, exigir também `type: projeto`, `status`, `repo: repos/<Projeto>`, `github` e `stack`.

### 4.4. Integridade de Links Bidirecionais, Paridade de Projetos e MemPalace
- Varredura de `[[Wikilinks]]` apontando para notas inexistentes.
- Conferência de paridade `dev\repos\` ↔ `notes\Projetos\Ativos\` via `pwsh C:\Users\melki\dev\tools\check-vault-projects.ps1`.
- Reindexação semântica ao concluir alterações: `mempalace mine "C:\Users\melki\dev\notes"`.

---

## 5. PROCESSO PASSO A PASSO (EXECUÇÃO DE CURADORIA)

### Passo 1: Varredura Determinística (`vault_hygiene_scanner.py`) e Paridade de Projetos
Disparar o scanner determinístico reconstruído do `obsidian-mind` (detecta *Active Drift*, *Open Loops* $\ge 14$ dias, notas monolíticas $>25\text{KB}$, pressão em `Inbox/`, `[[Wikilinks]]` quebrados, guarda *Never-Expose* Case-Insensitive Windows e gera `report_key` SHA-256 anti-nagging):
```powershell
uv run python skills/curadoria-obsidian-vault/scripts/vault_hygiene_scanner.py --json
pwsh "C:\Users\melki\dev\tools\check-vault-projects.ps1"
```

### Passo 2: Detecção de Anexos Órfãos
1. Coletar arquivos de mídia/PDF dentro do cofre.
2. Verificar ocorrência do nome de cada anexo em `![[arquivo]]` ou `![](arquivo)` nas notas `.md`.
3. Anexos sem correspondência são listados como órfãos para realocação segura em `Arquivo/_anexos_orfaos/`.

### Passo 3: Auditoria de Links, Frontmatter e Monólitos (>25KB)
Identificar notas sem cabeçalho YAML (`title`, `date`, `tags`), `[[Wikilinks]]` órfãos e notas monolíticas que pedem *split* (nunca *trim*).

### Passo 4: Relatório, Realocação Segura, Índice Seccional Híbrido e Sincronização MemPalace
Apresentar o diagnóstico determinístico (`[PASS]` / `[FAIL]`) com `report_key` canônico, aplicar correções aprovadas, atualizar o índice incremental de seções (`vault_palace_search.py`) e executar `mempalace mine`:
```powershell
uv run python skills/curadoria-obsidian-vault/scripts/vault_palace_search.py --query "preferencias" --room memoria --rebuild
mempalace mine "C:\Users\melki\dev\notes"
```

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill entrega:
1. **Quadro de Saúde do Cofre (`C:\Users\melki\dev\notes\`):**
   - Total de notas ativas por sala (`Inbox`, `Projetos`, `Memória`, `Medicina`, etc.) e status de `check-vault-projects.ps1`.
2. **Relatório de Anexos Órfãos e Links Quebrados:**
   - Lista de arquivos sem vínculos e `[[Wikilinks]]` pendentes de resolução.
3. **Resumo de Triagem de `Inbox/`:**
   - Sugestão de encaminhamento de notas brutas para as salas canônicas.
4. **Status de Sincronização MemPalace:**
   - Resultado da execução de `mempalace mine "C:\Users\melki\dev\notes"`.

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA modificar arquivos da pasta `.obsidian/` (configurações de plugins, temas ou workspaces).
- NUNCA deletar notas ou anexos permanentemente; mover anexos órfãos para `Arquivo/_anexos_orfaos/`.
- Não alterar nomes de notas sem atualizar simultaneamente os `[[Wikilinks]]` correspondentes.
