# Critérios Determinísticos de Auditoria — `design-md` (`v7.0.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar a geração e atualização do contrato arquitetural `DESIGN.md` alinhado aos **9 Eixos da SSOT** (`Preferências de Trabalho com Agentes.md`).

---

## 1. Box Model Lógico, Anti-Colapso de Margem e Identidade por Propósito (`[AUDIT-DESIGN-01]`)

- **`[PASS]`**: O arquivo `DESIGN.md` explicita o `project_purpose`, o `complexity_tier` (*Nível 1: `@layer` Estático*, *Nível 2: SPA Feature-Driven* ou *Nível 3: Fullstack App Router & PWA*), seleciona um dos **6 Arquétipos Canônicos de Layout** e define `box-sizing: border-box`, propriedades lógicas (`inline-size`, `block-size`, `padding-inline`, `margin-block`) e prevenção de colapso de margem (`display: flow-root`, `gap` no pai e `.prose > * + *`).
- **`[FAIL: TEMA_FIXO_OU_BOX_FISICO_LEGADO]`**: Reutilização mecânica de layout/paleta de outro projeto sem relação com o propósito, ou omissão das propriedades lógicas e contenção BFC.
- **`[UNVERIFIED]`**: Caminho raiz do projeto inacessível no disco.

## 2. Cores Perceptuais `OKLCH`, Temas Claro/Escuro e Tokens em 3 Camadas (`[AUDIT-DESIGN-02]`)

- **`[PASS]`**: Estrutura os tokens em **3 Camadas Hierárquicas** (*1. Primitivos*, *2. Semânticos/Alias* reativos via `oklch()`, `light-dark()`, `color-mix(in oklab, ...)` e Sintaxe de Cores Relativas RCS `from`, *3. Componente*), sincroniza `<meta name="color-scheme" content="light dark">` e `color-scheme: light dark`, e define elevação progressiva de luminosidade $L$ no Modo Escuro (`0.16 -> 0.22 -> 0.27`, evitando `#000000` puro).
- **`[FAIL: POLUICAO_CROMATICA_OU_SEM_3_CAMADAS]`**: Uso de cores neon/saturadas para contraste artificial, preto puro `#000000` causando *smearing* no escuro, ou ausência da separação entre tokens primitivos e semânticos (`--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--text-primary`/`--ink-primary`).

## 3. Sombras Multi-Camadas (3 Tipos), Luz Zenital e Nitidez Tipográfica Fluida (`[AUDIT-DESIGN-03]`)

- **`[PASS]`**: Especifica os 3 tipos de sombra (`box-shadow` com `inset` e `spread` negativo, `text-shadow`, `filter: drop-shadow()`), sombras realistas em 3 níveis (Umbra + Penumbra + Catch-Light `inset 0 1px 0 0` e `--shadow-inset`), `isolation: isolate` para blend modes, escala fluida `clamp()`, `max-inline-size: 65ch`, `text-wrap: balance/pretty`, travas `antialiased` + `font-synthesis: none`, zero `scale()` fracionário em textos e `font-variant-numeric: tabular-nums`.
- **`[FAIL: SOMBRA_LAVADA_OU_RISCO_BORRAO_GPU]`**: Sombra simples de camada única (`0 4px 12px rgba(0,0,0,0.4)`), ausência de `font-synthesis: none` ou omissão de `tabular-nums`.

## 4. Macro/Microlayout (`@container`), 4 Variantes de Cards, Navegação em 3 Camadas e Real-State (`[AUDIT-DESIGN-04]`)

- **`[PASS]`**: Distingue Macrolayout (`@media`, Grid RAM) de Microlayout (`@container`), define as **4 Variantes de Cards** (*Elevated*, *Outlined*, *Filled/Subtle*, *Interactive*), especifica as **3 Camadas de Navegação** (*Global*, *Local/In-Page*, *Breadcrumbs* `<ol role="list">` + `aria-current="page"`, Ordem DOM = Ordem Visual), curvas `cubic-bezier(0.22, 1, 0.36, 1)`, `@media (prefers-reduced-motion: reduce)`, `@media (pointer: coarse)` ($\ge 44\text{px}$), zero emojis e 100% Engenharia Real-State.
- **`[FAIL: EMOJI_PLACEBO_OU_NAVEGACAO_QUEBRADA]`**: Permissão de emojis na UI, `flex-direction: row-reverse` quebrando a ordem de `Tab`, ou omissão dos estados funcionais reais (`idle`, `active`, `empty`, `error`).
