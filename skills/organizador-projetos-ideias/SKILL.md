---
name: organizador-projetos-ideias
description: "Organiza ideias do zero com perguntas guiadas e sugestão de MVP ou reestrutura README.md fiel ao disco e contratos MCP tools.json. Use para estruturar repositórios; não use para limpeza de SO."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, TypeScript 5+, Go 1.24+"
metadata:
  version: "1.2.0"
  updated_at: "2026-11-13"
  author: "Melki & Franklin-Main"
  category: "Project Architecture, Idea Refinement & Repository Hygiene"
  tags: ["organizador-projetos", "refinamento-ideias", "mvp-funcional", "benchmark-repos", "mcp-fastapi-rpc", "higiene-repositorio"]
---
# SKILL: `organizador-projetos-ideias` (`v1.2.0`) — Ideação, Estrutura Ideal e MVP Seguro

## 1. Propósito e Gatilhos (Quando Usar)

Arquiteto de Produto e Repositórios com dois modos complementares:
1. **Modo 1 (`ideation_to_v1`):** Converte uma ideia bruta em **MVP funcional e seguro (`v1.0.0`)** com perguntas guiadas (incluindo gestão de ambiguidade para *"não sei"*), benchmark de referência, árvore modular e código inicial real (zero placebo).
2. **Modo 2 (`project_organizer_sync`):** Mapeia estrutura atual, extrai intenção real, desenha a **Estrutura Ideal** (preenchendo módulos faltantes com segurança), sincroniza Tríade (`AGENTS.md`, `.context/context.md`, `.context/spec.md`, `DESIGN.md`, `README.md` 1:1) e contratos (`MCP tools.json`, `FastAPI`, `JSON-RPC 2.0`).

## 2. Entradas e Parâmetros

- **Modo 1 (`ideation_to_v1`):** Diretório vazio ou ideação; recebe rascunho da ideia, objetivo e respostas (1–3 perguntas por rodada).
- **Modo 2 (`project_organizer_sync`):** Repositório existente (`project_root`), manifestos (`pyproject.toml`, `package.json`, `go.mod`), código e histórico Git.

## 3. Processamento e Fluxo Passo a Passo

- **Modo 1 (`ideation_to_v1`):**
  1. **Triagem (1–3 perguntas)** resolvendo ambiguidade e definindo problema, resultado e recorte v1.
  2. **Protocolo *"Não sei"*:** Proponha o pacote mínimo com validação estrita e variáveis protegidas (nunca casca vazia).
  3. **Benchmark & Árvore:** Compare repositórios de referência na mesma stack e explique o papel de cada pasta/arquivo.
  4. **Bootstrap (`v1.0.0` sob confirmação HITL):** Crie Tríade `.agents/AGENTS.md` / `.context/{context,spec}.md`, `.gitignore`, `.env.example` e código base seguro.
- **Modo 2 (`project_organizer_sync`):**
  1. **Mapeamento & Precedência:** Inspecione árvore e manifestos; esclareça até 3 `[LACUNA]`s de arquitetura antes de reorganizar.
  2. **Benchmark & Estrutura Ideal:** Defina árvore destino sem quebrar imports.
  3. **Pré-Preenchimento & Mermaid:** Gere módulos com `Pydantic v2 extra="forbid"` / `Zod .strict()` / Go structs e diagrama `flowchart TD` com rótulos entre aspas.
  4. **Sincronia Docs & Contratos:** Aplique [`references/guia_contratos_mcp_fastapi_rpc_e_documentos.md`](references/guia_contratos_mcp_fastapi_rpc_e_documentos.md); se houver Gemini API ou WS/JSON-RPC, consulte `google-developer-knowledge`/`gemini_get_doc` (não use `gemini_search_docs`, desabilitada) e a skill `agent-server-auditor`.
  5. **Higiene Segura (`Dry-Run`):** Liste órfãos na raiz e realoque somente após confirmação humana.

## 4. Saídas e Entregáveis

Emita os 4 blocos canônicos (Metadados + Análise MVP, Diagrama Mermaid, Mapeamento Atual vs. Estrutura Ideal comentada e Próximo Passo HITL) conforme [`references/organizador_output_template.md`](references/organizador_output_template.md).

## 5. Limites, Exceções e Guardrails (Quando NÃO Usar)

- **Proibido MVP Oco, Vazamento ou Limpeza sem `Dry-Run`** ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)): zero funções `TODO`/placebo, zero segredos de `.env` em docs, zero remoção de raiz sem aprovação.
- **Fronteira:** Para auditoria `0–100`, AST e DOM live `@eX`, use [`../auditoria-projetos-sistema/SKILL.md`](../auditoria-projetos-sistema/SKILL.md); para diagramar apenas Markdown/PDF sem reorganizar código, use `organizador-fluxo-arvore-arquivos`.
