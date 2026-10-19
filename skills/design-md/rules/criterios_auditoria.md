# Critérios Determinísticos de Auditoria — `design-md` (`v5.0.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar a geração e atualização do contrato arquitetural `DESIGN.md` guiado pelo propósito do projeto (Módulo **M3**).

---

## 1. Alinhamento ao Propósito do Projeto e Tokens Semânticos (`[AUDIT-DESIGN-01]`)
- **`[PASS]`**: O arquivo `DESIGN.md` na raiz do projeto explicita o `project_purpose`, seleciona uma atmosfera coerente com o domínio (*Ad Lucem*, *Cinza Monolítico `#57545d` + Menus `#8e8999`*, *Preto Terminal IBM `Ex Umbris`*, *AETHER 2027* ou paleta própria fundamentada) e declara as camadas de superfície (`--bg-canvas`, `--bg-surface`, `--bg-elevated`, `--bg-contrast-card`) e 4 níveis de tinta (`--ink-primary..subtle`).
- **`[FAIL: TEMA_FIXO_SEM_PROPOSITO]`**: Aplicação mecânica de paleta fixa sem diagnosticar o propósito do projeto ou omissão das camadas de superfície e tinta.
- **`[UNVERIFIED]`**: Caminho raiz do projeto inacessível no disco.

## 2. Camadas Esculpidas, Rim Light e Espaçamento Concêntrico (`[AUDIT-DESIGN-02]`)
- **`[PASS]`**: Define sombra esculpida em 3 camadas (`--shadow-sculpted`: Umbra + Penumbra + Difusão) combinada com `1px` Rim Light (`inset 0 1px 0 0 var(--rim-light)`), respiro de canvas ($\ge 25\%$) e fórmula de raios concêntricos ($R_{\text{interno}} = R_{\text{externo}} - \text{Padding}$).
- **`[FAIL: CAMADAS_OU_ESPACAMENTO_AUSENTES]`**: Sombras borradas genéricas sem separação de camadas, falta de respiro ou ausência de diretrizes de espaçamento.

## 3. Contraste Perceptual, Isolamento de Acento e Legibilidade de Menus (`[AUDIT-DESIGN-03]`)
- **`[PASS]`**: Garante contraste WCAG 2.1 AA/AAA (APCA $L_c \ge 60/75$), tinta escura nítida sobre menus claros ou `#8e8999` (`--nav-ink`), e isolamento do acento pontual (proporção 98/2 ou 60-30-10 com 1 único CTA primário sólido vs. `.btn-ghost`).
- **`[FAIL: CONTRASTE_OU_POLUICAO_CROMATICA]`**: Texto branco sobre fundo claro/cinza médio, múltiplos CTAs primários competindo ou abuso de cores saturadas sem hierarquia.

## 4. Tipografia Fluida (`clamp()`), `tabular-nums` e Integração Atômica (`[AUDIT-DESIGN-04]`)
- **`[PASS]`**: Especifica escala fluida com `clamp()`, `font-variant-numeric: tabular-nums` para dados numéricos, acoplamento `IBM Plex Sans` + `IBM Plex Mono` quando o tema for Preto Terminal (`Ex Umbris`), e estrutura `src/` em 5 camadas atômicas com estados FSM (`idle | loading | error | pressed`).
- **`[FAIL: TIPOGRAFIA_OU_ARQUITETURA_INCOMPLETA]`**: Ausência de `tabular-nums`, falta de escala tipográfica ou omissão dos estados FSM.
