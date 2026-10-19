# Critérios Determinísticos de Auditoria — `design-interface-medica-minimalista` (`v3.0.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar interfaces clínicas, prontuários eletrônicos (PEP), calculadoras médicas e receituários A4 (Módulos **M3** e **M7**).

---

## 1. Atmosfera Clínica por Propósito, Contraste e Semântica de Alerta (`[DISC-PALETA]` / `AUDIT-VIS-01`)
- **`[PASS]`**: Adapta a superfície ao contexto assistencial (Consultório Diurno `#F4F6F8`/`#FFFFFF` ou Plantão Noturno `#0B0E14`/`#121721` com $L_{\text{card}} > L_{\text{canvas}}$), aplica camadas esculpidas sutis (`--shadow-sculpted` + `1px` Rim Light), contraste WCAG AAA em dados vitais e restringe vermelho (`#DC2626`) exclusivamente a alertas críticos/alergias.
- **`[FAIL: CONTRASTE_OU_SEMANTICA_CLINICA_VIOLADA]`**: Falta de contraste em sinais vitais/doses, uso decorativo de vermelho de emergência ou poluição visual incompatível com ambiente médico.
- **`[UNVERIFIED]`**: Arquivos de estilo/componentes da interface clínica não fornecidos ou inacessíveis.

## 2. Ergonomia Clínica, Zero Emojis, Tipografia Tabular e Impressão A4 (`[DISC-TATIL]`)
- **`[PASS]`**: Zero caracteres emoji na interface (uso exclusivo de ícones vetoriais Lucide `stroke-width="1.5"` a `"1.75"`), alvos de toque $\ge 44\times44\text{px}$ com blindagem `anti-squish` (`flex-shrink: 0; white-space: nowrap` preservando unidades como `mg/dL`, `mL/min`, `mEq/L`), doses/exames em `IBM Plex Mono` / `JetBrains Mono` com `font-variant-numeric: tabular-nums` e folha `@media print` calibrada para papel A4 sem sombras nem sidebars.
- **`[FAIL: EMOJI_OU_DESALINHAMENTO_CLINICO]`**: Presença de qualquer emoji em botões/badges, quebra de linha em unidades médicas, ausência de `tabular-nums` em tabelas numéricas ou falta de `@media print` em telas de prescrição/receituário.

## 3. Delegação Determinística de Cálculos e Máquina de Estados FSM (`[DISC-OPCOES]` & `[DISC-SUPPLY]`)
- **`[PASS]`**: Fórmulas médicas (clearance renal, infusão, correção eletrolítica) são executadas por funções determinísticas tipadas e testadas (ou `agy_deterministic_calc_suite`), inputs validam faixas fisiológicas com alerta semântico `role="alert" aria-live="assertive"`, e o projeto atinge `Verdict: PASS` (`Readiness >= 90.0`) no `scripts/audit_tactile_ui.py`.
- **`[FAIL: RISCO_CLINICO_OU_SEM_FSM]`**: Cálculo de doses delegado a inferência livre de LLM, ausência de validação de limites fisiológicos ou reprovação no `audit_tactile_ui.py`.
