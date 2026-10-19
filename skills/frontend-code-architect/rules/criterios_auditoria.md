# Critérios Determinísticos de Auditoria — `frontend-code-architect` (`v4.1.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar o scaffolding estrutural em Design Atômico e os templates base sob `DESIGN.md v4.5-soft` (Módulo **M3**).

---

## 1. Particionamento em 5 Camadas de Design Atômico (`[AUDIT-ARCH-01]`)
- **`[PASS]`**: Estrutura modular `src/` dividida em `components/ui/` (Átomos), `components/bento/` (Moléculas/Organismos), `components/layout/` (Templates/Shell), `config/` (`tokens.ts` + `DESIGN.md`), `styles/` (`globals.css` + `theme.css`), `types/` (`index.ts`) e `views/`, com todos os arquivos $\le 300$ linhas.
- **`[FAIL: MONOLITO_FRONTEND]`**: Componentes monolíticos na raiz, arquivos $> 300$ linhas ou ausência de separação nas 5 camadas atômicas.
- **`[UNVERIFIED]`**: Diretório `src/` ainda não inicializado no caminho informado.

## 2. Paridade de Tokens Tonais 60-30-10 e Iluminação 135° (`[AUDIT-ARCH-02]`)
- **`[PASS]`**: `src/styles/globals.css` e `src/config/tokens.ts` implementam `--surface-canvas: #F1F4F8`, `--surface-inset: #E5E9F0`, `--surface-raised: #F1F4F8`, `--surface-contrast: #1E293B` e `--accent-point: #0284C7` (*Cerulean Sapphire*), com sombras duplas a 135° e `@media (prefers-reduced-motion: reduce)`.
- **`[FAIL: DIVERGENCIA_DE_TOKENS]`**: Presença de `backdrop-filter: blur()`, bordas duras de `1px`, azul cobalto (`#0044FF`, `#0057FF`, `#1D4ED8`, `#233DFF`) ou ausência de `--ease-spring`.

## 3. Adoção Real de `<SoftCard />` e Tracker Deslizante (`[AUDIT-ARCH-03]`)
- **`[PASS]`**: `<SoftCard />` (`src/components/ui/SoftCard.tsx`) é importado e instanciado em $\ge 50\%$ das views não-primitivas, e a Tactile Companion Sidebar implementa `#sidebar-active-tracker` como elemento posicional deslizante em `surface-inset`.
- **`[FAIL: PLACEBO_ORFAO_OU_TRACKER_FAKE]`**: `<SoftCard />` criado mas órfão (views usando `<div className="border-slate-800">`) ou `#sidebar-active-tracker` aplicado como `id` condicional estático dentro de `.map()`.

## 4. Tipagem TypeScript Estrita e Estados Finitos FSM (`[AUDIT-ARCH-04]`)
- **`[PASS]`**: Contratos TypeScript estritos (zero `any`), alvos interativos $\ge 44\times44\text{px}$ com `flex-shrink: 0; white-space: nowrap`, números com `tabular-nums` e suporte executável aos estados FSM (`Idle`, `Loading` com `aria-busy="true"`, `Error` com `role="alert"` e `Pressed`).
- **`[FAIL: TIPAGEM_FRACA_OU_SEM_FSM]`**: Uso de `any`, ausência de estados WAI-ARIA executáveis ou uso de emojis em controles.
