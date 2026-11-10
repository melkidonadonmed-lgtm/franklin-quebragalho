# Critérios Determinísticos de Auditoria — `frontend-code-architect` (`v7.0.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar a implementação de código frontend conforme os **9 Eixos da SSOT** (`Preferências de Trabalho com Agentes.md`).

---

## 1. Modularidade (`<= 300 linhas`), Preservação de Referência e 3 Níveis de Complexidade (`[AUDIT-ARCH-01]`)

- **`[PASS]`**: Respeita o limite de `<= 300 linhas` (`~15 KB`) por chamada/arquivo e preserva referências do usuário. Estrutura o projeto proporcionalmente ao escopo: **Nível 1** (`.html` standalone `<= 150 KB` ou CSS nativo com `@layer tokens, reset, layouts, components, utilities;`), **Nível 2** (SPA Feature-Driven com `src/components/{ui,layout}` e `src/features/<dominio>/` ou Design Atômico) ou **Nível 3** (Fullstack App Router com `(marketing)` / `(workspace)`, `_components` privados, `Viewport` API e script anti-FOUC).
- **`[FAIL: MONOLITO_OU_DESCARTE_DE_REFERENCIA]`**: Arquivos `> 300 linhas`, substituição de referência funcional por template genérico ou inclusão de bitmaps Base64 `> 50 KB`.
- **`[UNVERIFIED]`**: Caminho alvo ainda não inicializado no disco.

## 2. Box Model Lógico, Anti-Colapso de Margem, Tokens em 3 Camadas (`OKLCH`) e Sombras (`[AUDIT-ARCH-02]`)

- **`[PASS]`**: Aplica `box-sizing: border-box`, propriedades lógicas (`inline-size`, `padding-inline`, `margin-block`), contenção BFC (`display: flow-root`, `gap` no pai e `.prose > * + *`), tokens em **3 camadas** (*Primitivos*, *Semânticos* `--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--text-primary`/`--ink-primary` com `oklch()`, `light-dark()`, `color-mix()` e RCS `from`, e *Componente*), elevação progressiva de $L$ no Modo Escuro (`0.16 -> 0.22 -> 0.27`), sombras multi-camadas (`--shadow-elevation-1..3` / `--elevation-1..3`, `--shadow-inset`, `drop-shadow()`) e `isolation: isolate` em blend modes.
- **`[FAIL: POLUICAO_CROMATICA_OU_SOMBRA_LAVADA]`**: Uso de cores neon/saturadas para destaque, preto puro `#000000` causando *smearing*, sombras borradas de camada única ou vazamento de margem vertical por falta de `flow-root`/`gap`.

## 3. Tipografia Fluida Anti-Borrão GPU, `@container`, 4 Cards e Navegação em 3 Camadas (`[AUDIT-ARCH-03]`)

- **`[PASS]`**: Aplica `antialiased`, `grayscale`, `optimizeLegibility`, `font-optical-sizing: auto` e `font-synthesis: none` em `html, body`; escala fluida `clamp()`, `max-inline-size: 65ch`, `text-wrap: balance/pretty` e `font-variant-numeric: tabular-nums`; separa Macrolayout (`@media`, Grid RAM) de Microlayout (`@container`); implementa as **4 Variantes de Cards** (`elevated`, `outlined`, `subtle`, `interactive`), as **3 Camadas de Navegação** (*Global*, *Local/In-Page*, *Breadcrumbs* `<ol role="list">` + `aria-current="page"`, Ordem DOM = Ordem Visual), zero emojis, `@media (prefers-reduced-motion: reduce)` e `@media (pointer: coarse)` ($\ge 44\text{px}$).
- **`[FAIL: BORRAO_GPU_EMOJI_OU_ORDEM_TAB_QUEBRADA]`**: Uso de `scale()` fracionário em textos, `flex-direction: row-reverse` em navegação, ausência de `font-synthesis: none` ou presença de emojis.

## 4. Engenharia Real-State (Zero Placebos), Zero Órfãos e Tipagem Estrita (`[AUDIT-ARCH-04]`)

- **`[PASS]`**: Contratos TypeScript/ES6+ estritos (zero `any`), consumo real de todos os componentes criados nas views (zero órfãos), e 100% dos controles (busca, filtro, cálculo, persistência e estados `idle`, `active`/`loading`, `empty`, `error`, `pressed`) com lógica funcional real (zero `setTimeout` placebo ou `alert('Em breve')`).
- **`[FAIL: PLACEBO_OU_COMPONENTE_ORFAO]`**: Presença de funções falsas/placebos, controles sem efeito sobre os dados ou componentes órfãos em `src/components/ui/`.
