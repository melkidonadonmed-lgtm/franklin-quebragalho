# Critérios Determinísticos de Auditoria — `frontend-code-architect` (`v5.0.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar a arquitetura modular em Design Atômico e os templates de estilo adaptados ao propósito do projeto (Módulo **M3**).

---

## 1. Particionamento em 5 Camadas de Design Atômico (`[AUDIT-ARCH-01]`)
- **`[PASS]`**: Estrutura modular `src/` dividida em `components/ui/` (Átomos), `components/bento/` (Moléculas/Organismos), `components/layout/` (Templates/Shell), `config/` (`tokens.ts` + `DESIGN.md`), `styles/` (`globals.css` + `theme.css`), `types/` (`index.ts`) e `views/`, com todos os arquivos $\le 300$ linhas.
- **`[FAIL: MONOLITO_FRONTEND]`**: Componentes monolíticos na raiz, arquivos $> 300$ linhas ou ausência de separação nas 5 camadas atômicas.
- **`[UNVERIFIED]`**: Diretório `src/` ainda não inicializado no caminho informado.

## 2. Alinhamento do Tema ao Propósito, Camadas Esculpidas e Contraste (`[AUDIT-ARCH-02]`)
- **`[PASS]`**: `src/styles/globals.css` e `src/config/tokens.ts` implementam superfícies semânticas (`--bg-canvas`, `--bg-surface`, `--bg-elevated`, `--bg-contrast-card`), 4 níveis de tinta (`--ink-primary..subtle`), tinta escura nítida em menus claros/`#8e8999` (`--nav-ink`), sombra esculpida em 3 camadas + `1px` Rim Light (`--shadow-sculpted`), acoplamento `IBM Plex` quando em tema Preto Terminal (`Ex Umbris`) e `@media (prefers-reduced-motion: reduce)`.
- **`[FAIL: TEMA_DESALINHADO_OU_CONTRASTE_RUIM]`**: Aplicação de paleta fixa sem relação com o propósito do projeto, texto branco lavado em menus claros/cinzas ou ausência de camadas de elevação.

## 3. Adoção Real de Componentes nas Views e Isolamento de CTA (`[AUDIT-ARCH-03]`)
- **`[PASS]`**: Os componentes criados em `src/components/ui/` (`SurfaceCard` / `SoftCard`, botões `.btn-primary-intent` e `.btn-ghost`) são efetivamente importados nas views reais (zero componentes órfãos), mantendo 1 único CTA primário sólido por dobra (proporção 98/2 ou 60-30-10).
- **`[FAIL: COMPONENTE_ORFAO_OU_POLUICAO_CTA]`**: Componentes criados em `ui/` mas nunca importados nas views, ou múltiplos CTAs primários coloridos competindo na mesma vista.

## 4. Tipagem TypeScript Estrita, `tabular-nums` e Estados Finitos FSM (`[AUDIT-ARCH-04]`)
- **`[PASS]`**: Contratos TypeScript estritos (zero `any`), alvos interativos $\ge 44\times44\text{px}$ com `flex-shrink: 0; white-space: nowrap`, números com `font-variant-numeric: tabular-nums` e suporte executável aos estados FSM (`idle`, `loading` com `aria-busy="true"`, `error` com `role="alert"` e `pressed`).
- **`[FAIL: TIPAGEM_FRACA_OU_SEM_FSM]`**: Uso de `any`, ausência de estados WAI-ARIA executáveis ou ausência de `tabular-nums` em KPIs/tabelas.
