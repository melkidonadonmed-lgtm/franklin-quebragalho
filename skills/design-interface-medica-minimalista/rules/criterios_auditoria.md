# Critérios Determinísticos de Auditoria — `design-interface-medica-minimalista` (`v4.0.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar interfaces clínicas, prontuários eletrônicos (PEP), calculadoras médicas e folhas vetoriais A4.

---

## 1. Superfícies Clínicas por Propósito, Iluminação Zenital e Semântica de Alerta (`[DISC-PALETA]` / `AUDIT-VIS-01`)

- **`[PASS]`**: Adapta os tokens `--surface-canvas`, `--surface-sunken`, `--surface-card`, `--surface-elevated` e `--surface-glass` ao contexto assistencial (Consultório Diurno ou Plantão Noturno), aplica incidência de luz zenital (`--catch-light`) e sombras multi-camadas em 3 níveis (`--elevation-1..3`), contraste WCAG AAA em dados vitais, destaque acromático em ações primárias e restringe indicadores semânticos (alergias/alertas críticos) a micro-dots (`6px`), linhas de acento (`2px`) ou badges sutis com texto neutro de alto contraste.
- **`[FAIL: CONTRASTE_OU_SEMANTICA_CLINICA_VIOLADA]`**: Falta de contraste em sinais vitais/doses, texto colorido de baixo contraste sobre fundo médio, sombras simples borradas de camada única ou poluição cromática incompatível com ambiente médico.
- **`[UNVERIFIED]`**: Arquivos de estilo/componentes da interface clínica não fornecidos ou inacessíveis.

## 2. Nitidez Tipográfica Anti-Borrão, Zero Emojis, Unidades Inquebráveis e Folha Vetorial A4 (`[DISC-TATIL]`)

- **`[PASS]`**: Aplica travas `antialiased` + `font-synthesis: none`, zero `scale()` fracionário em contêineres de texto, zero caracteres emoji (uso exclusivo de ícones vetoriais Lucide `stroke-width="1.5"` a `"1.75"`), alvos $\ge 44\times44\text{px}$ com blindagem `anti-squish` (`flex-shrink: 0; white-space: nowrap` preservando `mg/dL`, `mL/min`, `mEq/L`), doses/exames em `IBM Plex Mono` / `JetBrains Mono` com `font-variant-numeric: tabular-nums` e folha `@media print` 100% CSS Grid vetorial + SVG (`210mm × 297mm`) sem sombras nem sidebars na impressão.
- **`[FAIL: EMOJI_OU_DESALINHAMENTO_CLINICO]`**: Presença de qualquer emoji em botões/badges, uso de `scale()` fracionário em texto, quebra de linha em unidades médicas, ausência de `tabular-nums` em tabelas numéricas ou falta de `@media print` vetorial em telas de prescrição/receituário.

## 3. Delegação Determinística de Cálculos e Engenharia Real-State (`[DISC-OPCOES]` & `AUDIT-STATE-01`)

- **`[PASS]`**: Fórmulas médicas (clearance renal, infusão, correção eletrolítica) são executadas por funções determinísticas tipadas e testadas (ou `agy_deterministic_calc_suite`), inputs validam faixas fisiológicas com alerta semântico `role="alert" aria-live="assertive"`, zero componentes placebo e o projeto atinge `Verdict: PASS` (`Readiness >= 90.0`) no `scripts/audit_tactile_ui.py`.
- **`[FAIL: RISCO_CLINICO_OU_SEM_FSM]`**: Cálculo de doses delegado a inferência livre de LLM, controles placebo sem efeito real, ausência de validação de limites fisiológicos ou reprovação no `audit_tactile_ui.py`.
