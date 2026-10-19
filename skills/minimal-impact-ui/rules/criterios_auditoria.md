# Critérios Determinísticos de Auditoria — `minimal-impact-ui` (`v1.0.0`)

Esta matriz define as regras falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar interfaces e páginas HTML/CSS/JS construídas sob o padrão **Ex Umbris Ad Lucem + WinUI 3 Gallery (`minimal-impact-ui`)**.

---

## Módulo M1: Sistema de 3 Temas e Proporção Cromática 98/2

- **`[RULE-MIU-01]` Suporte Ao Vivo aos 3 Temas Oficiais (`gray`, `light`, `dark`) + `localStorage`**:
  - **`[PASS]`**: O documento define os blocos `:root, [data-theme="light"]` (`#F3F3F5`), `[data-theme="gray"]` (`#57545d` canvas, `#49464f` card, `#635f6a` elevado, `#232127` contraste) e `[data-theme="dark"]` (`#070709` + títulos em `IBM Plex Mono`), com função `setThemeMode()` persistindo em `localStorage`.
  - **`[FAIL]`**: Ausência do tema Cinza sobre Cinza (`#57545d`) ou acoplamento a uma única paleta estática sem alternância funcional.
- **`[RULE-MIU-02]` Isolamento de Acento (Regra dos 2% — Von Restorff) e 4 Presets Calibrados**:
  - **`[PASS]`**: 98% da interface mantém superfícies neutras/acromáticas e aplica `--punctual-accent` (`#e13535`, `#35acd8`, `#10B981` ou `#D97706`) apenas no ponto focal, com `--punctual-btn-ink` escuro (`#091318` / `#062016`) para Azul/Verde e branco (`#FFFFFF`) para Carmim/Âmbar.
  - **`[FAIL]`**: Uso simultâneo de múltiplos acentos coloridos competindo na mesma dobra ou texto branco ilegível sobre botão `#35acd8` / `#10B981`.

## Módulo M2: Nitidez Tipográfica Absoluta e Contraste de Menus

- **`[RULE-MIU-03]` Zero Letras Vermelhas Embaçadas ou Serifa Fina sobre Cinza/Escuro**:
  - **`[PASS]`**: Nenhum texto solto usa `color: #e13535` diretamente sobre `#57545d`, `#49464f` ou `#070709`. Destaques em títulos usam `.highlight-surgical` / `.font-serif-editorial` (`font-weight: 600` + sublinhado `2px` em `--punctual-accent`), e badges/tags usam `.accent-text` (`--punctual-text: #FFFFFF` no cinza/escuro e `#991B1B` no claro + fundo `--punctual-soft` + `border-left: 2.5px solid var(--punctual-accent)`).
  - **`[FAIL]`**: Presença de letras vermelhas puras sem fundo/borda sobre superfície cinza/escura (contraste `2.1:1`) ou fonte serifada fina borrada.
- **`[RULE-MIU-04]` Barra de Navegação em Pílula (`#8e8999`) com Tinta Escura Nítida (`#16151A`)**:
  - **`[PASS]`**: No tema `gray`, `.nav-shell` utiliza `--nav-shell-bg: #8e8999` com `--nav-ink: #16151A` e item ativo invertido (`--nav-active-bg: #1E1C22`, `--nav-active-ink: #F5F4F8`).
  - **`[FAIL]`**: Texto branco ou cinza claro lavado sobre barra `#8e8999`.

## Módulo M3: Arquétipos de Página, 28 Efeitos WinUI 3, Camadas e A4 Print

- **`[RULE-MIU-05]` Sombra Esculpida em 3 Camadas + `1px` Rim Light e Alternância de Contraste**:
  - **`[PASS]`**: Cards principais aplicam `--shadow-sculpted` (umbra + penumbra + difusão + `inset 0 1px 0 0 var(--rim-light)`), alternam `.surface-card` e `.surface-contrast` e utilizam `font-variant-numeric: tabular-nums` em dados numéricos.
  - **`[FAIL]`**: Sombras duras de 1 camada sem Rim Light ou ausência de `tabular-nums` em tabelas/métricas.
- **`[RULE-MIU-06]` Cinemática Física (`Quint Out` / `Spring`), Acessibilidade FSM e `@media print` A4**:
  - **`[PASS]`**: Transições utilizam `cubic-bezier(0.16, 1, 0.3, 1)` ou `cubic-bezier(0.34, 1.56, 0.64, 1)`, incluem `@media (prefers-reduced-motion: reduce)`, `@media print` A4 limpo e atingem `Readiness Score >= 90.0` em `audit_tactile_ui.py`.
  - **`[FAIL]`**: Uso de `alert()` nativo, ausência de `@media print` ou `Readiness Score < 90.0`.
  - **`[UNVERIFIED]`**: Quando o arquivo HTML/CSS alvo ainda não foi gerado ou fornecido para inspeção estática.
