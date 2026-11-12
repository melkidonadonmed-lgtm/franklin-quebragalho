---
name: redator-tecnico-markdown
description: "Redige relatórios executivos, notas técnicas e atas de decisão em Markdown com caixas de alerta GitHub e Google Style Guides. Use para documentação técnica; não use apenas para converter HTML em PDF."
version: "1.3.0"
updated_at: "2026-11-12"
compatibility: "Antigravity 2.0, CommonMark/GFM, Obsidian"
allowed-tools: ["read_file", "write_file", "edit_file", "call_mcp_tool"]
metadata:
  version: "1.3.0"
  updated_at: "2026-11-12"
  author: "DocMaker & Melki"
  category: "Documentação Técnica e Redação Estruturada"
  tags: ["markdown", "obsidian", "google-styleguides", "documentacao"]
---
# Redação Técnica Estruturada em Markdown (`redator-tecnico-markdown`)

## 1. Propósito e Gatilhos de Ativação (Quando Usar)

- Redigir relatórios executivos, notas técnicas, ADRs (atas de decisão de arquitetura), guias de instalação e notas para o Obsidian em Markdown (GFM).
- Padronizar rascunhos técnicos com frontmatter YAML, alertas GitHub e blocos de código alinhados aos Google Style Guides antes de eventual exportação PDF.

### Quando NÃO Usar

- Apenas para converter Markdown/HTML existente em PDF (use `conversor-html-pdf`).
- Para mapear especificamente fluxogramas de ideias e árvores comentadas de diretórios (use `organizador-fluxo-arvore-arquivos`).
- Para auditar contratos de skills do Antigravity (use `audit-skills-antigravity`).

---

## 2. Entradas Esperadas e Pré-requisitos

- `topic_or_draft` (obrigatório): Tema, rascunho, ata ou código a documentar.
- `document_type` (opcional): `nota_tecnica` (padrão), `relatorio_executivo`, `adr_decisao`, `roadmap`, `guia_instalacao`.
- `output_path` (opcional): Caminho `.md` de destino (`C:\Users\melki\dev\notes\Inbox\` ou `docs\` do repositório).

---

## 3. Diretrizes e Fluxo de Execução (Passo a Passo)

1. **Estrutura e Frontmatter YAML ([`references/guia_estilo_markdown.md`](references/guia_estilo_markdown.md))**:
   - Iniciar com YAML válido (`title`, `date: YYYY-MM-DD`, `author`, `tags`, `status`) quando destinado ao Obsidian ou acervo documental.
   - Organizar em Sumário Executivo, Diagnóstico/Contexto, Especificação Técnica e Próximos Passos.
2. **Blindagem CommonMark/GFM e Google Style Guides**:
   - **Lei da Linha em Branco**: Linha vazia obrigatória antes e depois de títulos, listas, tabelas, blocos `>` e cercas de código.
   - **Alertas Canônicos**: Usar `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]` ou `> [!CAUTION]` sem aninhamento.
   - **Escape Seguro**: Escapar `\|` em células de tabela, `\$` literal em prosa e usar 4 crases (```` ```` ````) ao envolver blocos que já contenham crases triplas.
   - **Código Tipado**: Declarar sempre a linguagem na cerca (`python`, `go`, `typescript`, `json`, `powershell`, `mermaid`, `yaml`).
3. **Gravação Física (`write_file` / `edit_file`)**: Persistir em UTF-8 e conferir contra [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).

---

## 4. Saídas e Entregáveis

1. Arquivo `.md` gravado e validado segundo [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).
2. Resumo conciso das seções redigidas e link clicável `file:///`.

---

## 5. Guardrails e Limites

- **Zero Invenção Factual**: Rotular dados não comprovados como `[UNVERIFIED]`; nunca fabricar métricas ou decisões não tomadas.
- **Zero XSS/Segredos**: Proibido embutir `<script>` não sanitizado ou credenciais reais em exemplos de código.
- Para exportação binária em `.pdf`, delegar para `conversor-html-pdf`.
