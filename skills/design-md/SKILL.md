---
name: design-md
description: "Cria ou atualiza o contrato DESIGN.md na raiz do projeto definindo tokens semânticos OKLCH, escala tipográfica modular, espaçamento e camadas. Use para criar o DESIGN.md; não use para projetos sem UI."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "8.2.0"
  updated_at: "2026-11-13"
  author: "UI-Architect & Melki"
  category: "Guia de Princípios de Design System Frontend (OKLCH), Física Óptica de Sombras e Arquitetura Espacial"
  tags: ["design-md", "frontend-design-md", "principios-de-design", "oklch", "sombras-multi-camadas", "container-queries", "starting-style", "aom-acessibilidade"]
---
# `design-md` (`v8.2.0`) — Contrato `DESIGN.md` Contextual (Zero Copia-e-Cola)

Guia de princípios visuais para sintetizar `<project_root>/DESIGN.md` sob medida a partir de [`references/design_md_5_pilares_detalhados.md`](references/design_md_5_pilares_detalhados.md), [`references/design_system_composition_reference.md`](references/design_system_composition_reference.md), [`references/spacing_tokens_and_stitch_hierarchy.md`](references/spacing_tokens_and_stitch_hierarchy.md), [`../../rules/diretrizes-frontend-9-eixos.md`](../../rules/diretrizes-frontend-9-eixos.md) e [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).

> **Regra de Ouro:** O `DESIGN.md` **NÃO é despejo de componentes**; derive decisões contextuais do propósito, público e stack real do projeto.

## 1. Quando Usar, Entradas e Limites (Quando NÃO Usar)

- **Gatilhos & Entradas:** Contexto do produto, público-alvo, stack frontend e arquivos (`README.md`, CSS/tokens) para criar/atualizar o `DESIGN.md` antes de codificar telas.
- **Quando NÃO Usar:** Projetos backend/CLI sem UI; docs de arquitetura (`SPEC.md` / `arquiteto-conteudo-solucoes`), `CONTEXT.md` ou `AGENTS.md`. Nunca copie adendos irrelevantes (ex.: Canvas Infinito em app clínico/landing page).

## 2. Processamento / Fluxo — Os 5 Pilares de `DESIGN.md`

1. **Filosofia & Identidade:** Justifique matiz ($H$), croma ($C$) e tipografia pelo domínio; garanta *Hero Funcional* e informação via bordas/`tabular-nums`.
2. **Arquitetura Espacial:** Separe Macrolayout (`@media`, Grid RAM, 1 Arquétipo Espacial) de Microlayout (`@container` fora de `subgrid`), tokens `--space-*` + Gestalt, Raios Concêntricos e tipografia fluida (`clamp()`, `60ch–65ch`, `antialiased`, `font-synthesis: none`).
3. **Cores `OKLCH` (60-30-10):** 60% Canvas / 30% Superfícies / 10% Destaque; eleve luminosidade $L$ no Dark Mode (`0.14 -> 0.26`, zero `#000000`) e derive hover/estados com `light-dark()`, `color-mix()` e RCS (`oklch(from ...)`).
4. **Física Óptica de Sombras (3–4 Camadas):** Umbra + Penumbra (`spread` negativo `-1px..-8px`) + Catch-Light (`inset 0 1px 0 0`); escolha `box-shadow` vs `text-shadow` vs `filter: drop-shadow()` e apenas os modos pertinentes (Glass, Tactile Inset, Dark Glow, `<dialog>` + `@starting-style`).
5. **Interatividade, AOM & `@layer`:** Ordem DOM = Visual, `:focus-visible`, Lei de Fitts (`>= 48x48px`, `gap >= 8px` em `any-pointer: coarse`), `prefers-reduced-motion`, `@layer` sem `!important` e árvore proporcional (Níveis 1/2/3).

## 3. Saídas / Entregáveis & Orquestração (`Topologia 3+1`)

Gere `<project_root>/DESIGN.md` cobrindo: (1) Propósito Visual e Hero Funcional, (2) Tokens 3 Camadas `OKLCH`, (3) Sombras Multi-Camadas e Modos selecionados, (4) Arquitetura Espacial + Tipografia, (5) Regras AOM + `@layer` filtradas de `references/`. Coordenação: `UI-Architect` + `ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer`.
