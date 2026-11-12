---
name: frontend-code-architect
description: "Implementa e refatora interfaces web React Next.js Tailwind consumindo o contrato DESIGN.md com estados finitos FSM, OKLCH e @container. Use para construir UI; não use só para criar o DESIGN.md."
version: "7.0.0"
updated_at: "2026-11-12"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "write_file", "edit_file", "run_command", "call_mcp_tool"]
metadata:
  version: "7.0.0"
  updated_at: "2026-11-12"
  author: "UI-Architect & Melki"
  category: "Frontend Engineering, OKLCH Design System, Container Queries, 3-Tier Project Architecture & Real-State"
  tags: ["frontend-architect", "oklch", "container-queries", "logical-properties", "feature-driven-spa", "app-router-pwa", "real-state-engineering"]
---
# Frontend Code Architect (`frontend-code-architect` v7.0.0 — 9 Eixos, OKLCH, `@container`, 3 Níveis de Complexidade & Real-State)

## 1. Objetivo, Gatilhos e Quando Usar

Esta Skill governa a implementação e refatoração de interfaces web seguindo os **9 Eixos + Matriz de Decisão** da Fonte Única de Verdade (SSOT) em [`../../rules/diretrizes-frontend-9-eixos.md`](../../rules/diretrizes-frontend-9-eixos.md), [`../design-md/SKILL.md`](../design-md/SKILL.md) e [`references/tactile_elevation_and_shadows.md`](references/tactile_elevation_and_shadows.md).

### Quando NÃO Usar (Exceções, Limites e Guardrails)

- **Reutilização de Layouts Pré-Moldados ou Cores Gritantes:** Proibido copiar a estética de outros projetos por inércia, usar preto puro (`#000000`) que cause *OLED smearing* no modo escuro, ou aplicar cores neon/saturadas para contraste artificial.
- **Borrão de GPU em Textos, Colapso de Margem Descontrolado ou Sombras Lavadas:** Proibido `scale()` fracionário em textos ou `translate(-50%, -50%)` em dimensões ímpares; proibido deixar margens internas vazarem sem `display: flow-root` ou `gap` no pai; proibido usar sombra simples de camada única (`0 4px 12px rgba(0,0,0,0.4)`).
- **Funções Falsas (Placebos), Quebra da Ordem de `Tab`, Emojis ou Emissão Longa:** Proibido `setTimeout` placebo, `alert('Em breve')`, `flex-direction: row-reverse` / `order` arbitrário em navegação, emojis na UI, imagens Base64 `> 50 KB` ou emissões `> 300 linhas` (`~15 KB`) por chamada.

---

## 1.5. Entradas e Pré-requisitos

- `target_path` (obrigatório): Arquivo standalone (`.html`) ou diretório raiz do projeto.
- `complexity_tier` (opcional, auto-detectado): `tier_1_static` (Landing Page / `@layer` / Standalone), `tier_2_spa_feature` (SPA Modular Orientada a Domínio) ou `tier_3_fullstack_pwa` (App Router com `(grupos)` + `_components` + PWA).
- `design_contract` (opcional): Caminho do `DESIGN.md` na raiz do projeto.
- `spatial_archetype` (opcional): Um dos 6 Arquétipos Espaciais canônicos.

---

## 2. Fluxo Operacional nos 4 Módulos de Engenharia (Eixos 1 a 9)

### Módulo 1: Seleção Proporcional do Modelo Arquitetural por Nível de Complexidade (Eixo 9)

Preserve integralmente qualquer referência enviada pelo usuário, escolha nomes semânticos ao domínio real do projeto (sem forçar nomes fixos de componentes) e selecione a estrutura proporcional ao escopo (`<= 300 linhas` por arquivo):

1. **Nível 1 — Baixa Complexidade (Landing Page, Hub Estático ou Artefato Standalone):**
   - Para arquivo único (`.html` `<= 150 KB`) ou template embarcado em servidor (Go/Python), mantenha a estrutura enxuta sem criar pastas artificiais.
   - Para site estático multi-arquivo, utilize **Zero-Runtime CSS** com `@layer reset, tokens, base, layouts, components, utilities;`.
2. **Nível 2 — Média Complexidade (SPA Modular Orientada a Domínio — Feature-Driven):**
   - Aplique *Feature-Driven Architecture* com colocalização (`Componente.tsx`, `.module.css`, `.test.tsx`, `.types.ts` na mesma pasta):

     ```text
     src/
     ├── app/                     # Providers globais e roteamento da aplicação
     ├── styles/                  # tokens.css (3 camadas OKLCH + sombras) e globals.css (@layer)
     ├── components/
     │   ├── ui/                  # Primitivos agnósticos de negócio (Button, Card, Dialog, Input)
     │   └── layout/              # Macrolayouts (AppShell, Header, Sidebar)
     ├── features/                # Módulos de negócio isolados (<dominio>/{api,components,hooks,types})
     └── types/ & utils/          # Contratos TypeScript estritos (zero any) e utilitários puros
     ```

3. **Nível 3 — Alta Complexidade (Plataforma Fullstack, App Router & PWA):**
   - Utilize **Grupos de Rotas** (ex.: `(marketing)/` e `(workspace)/`) para isolar Macrolayouts sem afetar a URL, e **Pastas Privadas** `_components/` colocadas ao lado das rotas para componentes exclusivos daquela página.
   - Configure `manifest.ts`, `Viewport` API (`colorScheme: 'light dark'`) e script síncrono anti-FOUC no `<head>` quando houver troca dinâmica de tema.

### Módulo 2: Box Model Lógico, Anti-Colapso de Margem, Tipografia Fluida e OKLCH (Eixos 1 a 5)

1. **Box Model e Propriedades Lógicas (Eixo 1):**
   - Aplique `box-sizing: border-box` globalmente e use propriedades lógicas (`inline-size`, `block-size`, `padding-inline`, `padding-block`, `margin-inline`, `margin-block`, `border-inline-start`).
   - Previna colapso de margem com `display: flow-root` nos wrappers de seção, `gap` nos contêineres Flexbox/Grid e `.prose > * + * { margin-block-start: var(--flow-space, 1.25em); }` em textos ricos.
2. **Tipografia Fluida e Nitidez GPU (Eixo 2):**
   - Aplique `antialiased`, `grayscale`, `optimizeLegibility`, `font-optical-sizing: auto` e `font-synthesis: none` em `html, body`.
   - Use escala fluida `clamp()` (`--step--1` a `--step-3`), `max-inline-size: 65ch` em `p, li` (`text-wrap: pretty`, `line-height: 1.6`), `text-wrap: balance` em `h1`–`h4` (`line-height: 1.18`, `letter-spacing: -0.02em`) e `font-variant-numeric: tabular-nums` em métricas.
3. **Tokens em 3 Camadas `OKLCH`, `light-dark()`, `color-mix()`, RCS e Sombras (Eixos 3, 4 e 5):**
   - Implemente Primitivos (`--primitive-*`, `--space-*`, `--radius-*`), Semânticos (`--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--bg-surface-2`/`--surface-elevated`/`--surface-sunken`, `--surface-glass`, `--text-primary`/`--ink-primary`, `--text-secondary`/`--ink-secondary`, `--border-subtle`) e Componente.
   - No modo escuro, eleve a luminosidade $L$ progressivamente (`0.16` Fundo $\to$ `0.22` Card $\to$ `0.27` Modal).
   - Use `box-shadow` em camadas (Umbra + Penumbra com `spread` negativo + Catch-Light `inset 0 1px 0 0` e `--shadow-inset`), `filter: drop-shadow()` em SVGs/PNGs vazados, `isolation: isolate` em blend modes e gradientes `linear-gradient(in oklch longer hue ...)`.

### Módulo 3: Macrolayouts (`@media`), Microlayouts (`@container`), PWAs e 4 Variantes de Cards (Eixos 6 e 7)

1. **Macrolayout vs. Microlayout & 6 Arquétipos Espaciais:**
   - Estruture a página com CSS Grid RAM (`repeat(auto-fit, minmax(min(100%, 320px), 1fr))`) e o Arquétipo Espacial do domínio (*Split-View*, *Bento 12 col*, *Command Center*, *Editorial*, *HUD Espacial* ou *Folha Vetorial A4 `@media print`*).
   - Em componentes autônomos, declare `container-type: inline-size; container-name: card;` e adapte com `@container card (min-width: 420px)`.
   - Em PWAs (`@media (display-mode: standalone), (display-mode: minimal-ui)`), oculte `.install-pwa-banner` e aplique `user-select: none` em `nav, button, .app-header`.
2. **Repertório das 4 Variantes de Cards (Uso Contextual):** Utilize as variantes `elevated`, `outlined`, `subtle` (filled) e `interactive` conforme a necessidade de hierarquia da tela (sem obrigar as 4 na mesma vista), com transições `cubic-bezier(0.22, 1, 0.36, 1)`, `@media (prefers-reduced-motion: reduce)` e `@media (any-pointer: coarse)` (`min-block-size: 48px`).

### Módulo 4: Arquitetura de Navegação Contextual e Engenharia Real-State (Eixo 8)

- Adapte as camadas de navegação ao escopo real da tela: **Global** (`<nav aria-label="Principal">`), **Local/In-Page** quando houver seções ou filtros contextuais (`<nav aria-label="Filtros da seção">`) e **Estrutural/Breadcrumbs** (`<nav aria-label="Caminho de navegação"><ol role="list">` + `aria-current="page"`) **apenas quando houver hierarquia profunda de rotas/documentos ($\ge 3$ níveis)** — evitando breadcrumbs artificiais em landing pages, modais ou apps de vista única. Mantenha Ordem DOM = Ordem Visual e 100% de lógica funcional real nos controles (`idle`, `loading`, `empty`, `error`, `pressed`).

---

## 3. Templates Base Canônicos (`references/`)

- **CSS OKLCH em 3 Camadas, Sombras, `@container` e Breadcrumbs (`src/styles/globals.css`):** Consulte [`references/canonical_templates.md`](references/canonical_templates.md) e [`references/tactile_elevation_and_shadows.md`](references/tactile_elevation_and_shadows.md).
- **Componente Polimórfico de Superfície (`src/components/ui/SurfaceCard.tsx`):** Consulte [`references/canonical_templates.md`](references/canonical_templates.md).

## 4. Saídas, Entregáveis e Orquestração (`Topologia 3+1`)

- **Entregáveis ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)):** Projeto estruturado em Nível 1 (`@layer`/standalone), Nível 2 (SPA Feature-Driven) ou Nível 3 (Fullstack App Router/PWA) com tokens OKLCH em 3 camadas, `@container`, 4 variantes contextuais de cards, navegação contextual e estado real executável (`<= 300 linhas`/chamada).
- **Persona Coordenadora:** `UI-Architect` (`ui-shell-navigator` $\to$ `ui-controls-data` + `ui-motion-interaction` $\to$ `ui-deterministic-observer`).
