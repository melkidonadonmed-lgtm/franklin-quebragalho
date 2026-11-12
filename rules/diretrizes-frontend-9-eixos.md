---
trigger: glob
globs: "**/*.css, **/*.scss, **/*.html, **/*.tsx, **/*.jsx, **/*.vue, **/DESIGN.md, **/elevationRenderer.ts"
description: "Ativa os 9 Eixos do SSOT para Frontend, UI/UX, CSS e DESIGN.md (Regra 60-30-10 em OKLCH, 3 níveis de sombra, anti-borrão GPU, @container e Real-State)."
---

# Diretrizes de Composição Visual, UI/UX, Regra 60-30-10 OKLCH e Sombras em 3 Camadas (9 Eixos do SSOT)

1. Consulte a skill `design-md`, `auditoria-projetos-sistema` (`v6.0.0`) ou [`Preferências de Trabalho com Agentes.md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md).
2. **Proporção Cromática `60-30-10` e Cores Perceptuais `OKLCH`:**
   - **60% Superfície Dominante:** `--surface-canvas` (alias legado `--bg-canvas`) em `oklch()` com `light-dark()` (no Dark Mode: $L = 0.16$, zero `#000000` puro).
   - **30% Estrutura Secundária:** `--surface-sunken` ($L = 0.13$ Dark), `--surface-card` ($L = 0.22$ Dark) e `--surface-elevated` ($L = 0.27$ Dark) com pares explícitos `light-dark()`.
   - **10% Acento Cirúrgico:** `--brand-primary` calibrado via `color-mix(in oklab, ...)` e `oklch(from ...)` restrito a CTAs primários, `:focus-visible` e indicadores de `6px`/`2px` (zero cores neon).
3. **Física da Luz Zenital (90°–120°) e Sombras Multi-Camadas em 3 Níveis (`--shadow-elevation-1..3` + `--shadow-inset`):**
   - Proibido usar sombra simples borrada ou pipeline de 2 passagens `rgba(0,0,0)` chapado.
   - Combine sempre **3 camadas ópticas**: (1) **Umbra de Contato** (oclusão curta), (2) **Penumbra Difusa com `spread` negativo** e (3) **Borda Especular Zenital Superior (`Top Catch-Light` `inset 0 1px 0 0`) + Anel Perimetral `1px`**.
4. **Box Lógico, Tipografia Fluida e Navegação Semântica em 3 Camadas:**
   - Use `box-sizing: border-box`, propriedades lógicas (`inline-size`, `padding-inline`, `gap`, `display: flow-root`), tipografia `clamp()` (`65ch`, `antialiased`, `font-synthesis: none`, `tabular-nums`, zero `scale()` fracionário em texto e **zero emojis na UI**).
   - Estruture Macrolayouts (`@media` nos 6 Arquétipos) + Microlayouts (`@container`), 4 variantes de cards e **Navegação em 3 Camadas** (`<= 3 <nav>`, menus descompactados `>= 13px`, Breadcrumbs `<ol role="list">` + `aria-current="page"` condicional para hierarquias `>= 3` níveis com Ordem DOM = Ordem Visual; abas novas permitidas para separar domínios distintos, proibidas abas com função duplicada, abas criadas sem sanear a principal ou vazamento de componentes internos de backend em abas).
