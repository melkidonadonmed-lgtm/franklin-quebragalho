---
name: frontend-code-architect
description: "Implementa e refatora interfaces web React Next.js Tailwind consumindo o contrato DESIGN.md com estados finitos FSM, OKLCH e @container. Use para construir UI; não use só para criar o DESIGN.md."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "7.0.0"
  updated_at: "2026-11-13"
  author: "UI-Architect & Melki"
  category: "Frontend Engineering, OKLCH Design System, Container Queries, 3-Tier Project Architecture & Real-State"
  tags: ["frontend-architect", "oklch", "container-queries", "logical-properties", "feature-driven-spa", "app-router-pwa", "real-state-engineering"]
---

# Frontend Code Architect (`frontend-code-architect`)

## 1. Objetivo, Gatilhos e Quando Usar

Governa implementação e refatoração de interfaces web alinhadas aos **9 Eixos + Matriz de Decisão** da SSOT [`../../rules/diretrizes-frontend-9-eixos.md`](../../rules/diretrizes-frontend-9-eixos.md), consumindo o contrato [`../design-md/SKILL.md`](../design-md/SKILL.md) com tokens `OKLCH`, propriedades lógicas, `@container`, estados finitos (FSM) e interatividade Real-State.

## 2. Entradas e Pré-requisitos

- **`target_path` (obrigatório):** Arquivo standalone (`.html`) ou diretório raiz do projeto.
- **`complexity_tier` (opcional, auto-detectado):** `tier_1_static` (Landing / `@layer` / Standalone), `tier_2_spa_feature` (SPA Feature-Driven) ou `tier_3_fullstack_pwa` (App Router com `(grupos)` + `_components` + PWA).
- **`design_contract` (opcional):** Caminho do `DESIGN.md` na raiz do projeto.
- **`spatial_archetype` (opcional):** Um dos 6 Arquétipos Espaciais canônicos.

## 3. Processamento e Fluxo Operacional (4 Módulos / 9 Eixos)

Consulte as especificações completas em [`references/arquitetura_4_modulos_e_eixos.md`](references/arquitetura_4_modulos_e_eixos.md), [`references/canonical_templates.md`](references/canonical_templates.md), [`references/layout_grid_cards_and_navigation.md`](references/layout_grid_cards_and_navigation.md) e [`references/tactile_elevation_and_shadows.md`](references/tactile_elevation_and_shadows.md):

1. **Módulo 1 — Arquitetura Proporcional (`tier_1` a `tier_3`, Eixo 9):** Selecionar entre standalone/`@layer` (`<= 150 KB`), SPA *Feature-Driven* (`src/{app,styles,components/{ui,layout},features/<dominio>}`) ou App Router PWA com `(grupos)` e `_components/`.
2. **Módulo 2 — Box Lógico, Tipografia & Tokens OKLCH (Eixos 1–5):** Aplicar `border-box`, propriedades lógicas, `display: flow-root`/`gap`, `clamp()`, `65ch`, nitidez GPU, tokens em 3 camadas (`--primitive-*`, `--bg-canvas`/`--surface-card`, componente) com `OKLCH`/`light-dark()`, Dark Mode $L = 0.16 \to 0.22 \to 0.27$ + Glow e sombras em 3 camadas (Umbra + Penumbra + Catch-Light).
3. **Módulo 3 — Macro/Microlayout (`@container`), `subgrid` & 4 Variantes de Cards (Eixos 6–7):** Estruturar CSS Grid RAM (`minmax(min(100%, 280px), 1fr)`), `@container` separado de `subgrid`, variantes `elevated`/`outlined`/`subtle`/`interactive`, `cubic-bezier(0.22, 1, 0.36, 1)`, `any-pointer: coarse` (`48x48px`), `content-visibility: auto` e `@media (display-mode: standalone)`.
4. **Módulo 4 — Navegação Adaptável Único DOM & Real-State (Eixo 8):** Bottom Bar (`env(safe-area-inset-bottom)`) $\leftrightarrow$ Sidebar Rail (`240px`), navegação local e Breadcrumbs (`>= 3` níveis), Ordem DOM = Ordem Visual e estados reais (`idle`, `loading`, `empty`, `error`, `pressed`). Consulte [`../design-md/references/spacing_tokens_and_stitch_hierarchy.md`](../design-md/references/spacing_tokens_and_stitch_hierarchy.md).

## 4. Saídas, Entregáveis e Orquestração (`Topologia 3+1`)

- **Entregáveis ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)):** Código real estruturado em `tier_1..3` com tokens OKLCH em 3 camadas, `@container`, 4 variantes de cards, navegação contextual e emissões `<= 300 linhas` por chamada.
- **Persona Coordenadora:** `UI-Architect` (`ui-shell-navigator` $\to$ `ui-controls-data` + `ui-motion-interaction` $\to$ `ui-deterministic-observer`).

## 5. Exceções, Limites e Quando NÃO Usar

- **Design Tokens sem Implementação:** Não use apenas para redigir `DESIGN.md` (use `design-md`).
- **Estética Genérica ou Contraste Nocivo:** Proibido copiar layouts por inércia, preto puro (`#000000`) ou cores neon artificiais.
- **Borrão GPU, Colapso ou Sombra Lavada:** Proibido `scale()` fracionário em texto, margens vazando sem `flow-root`/`gap` e sombra simples de camada única.
- **Placebos e Quebra de Tab:** Proibido `setTimeout` placebo, `alert('Em breve')`, `row-reverse`/`order` quebrando `Tab`, emojis na UI e Base64 `> 50 KB`.
