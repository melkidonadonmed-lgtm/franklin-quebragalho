# Critérios Determinísticos de Auditoria — `design-interface-medica-minimalista` (`v2.2.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar interfaces clínicas, prontuários eletrônicos (PEP), calculadoras médicas e receituários sob o contrato **`DESIGN.md v4.5-soft`** (Módulos **M3** e **M7**).

---

## 1. Paleta Clínica Tonal 60-30-10 e Iluminação 135° (`[DISC-PALETA]` / `AUDIT-VIS-01`)
- **`[PASS]`**: Aplica a hierarquia tonal 60-30-10 com `--surface-canvas` (`#F1F4F8` em Slate ou `#F5F4EE` em Warm Ivory; `#12151B` no Plantão Noturno com $L_{\text{card}} > L_{\text{canvas}}$), elevação dupla a 135° (`.ui-card-soft`), inputs em cavidade `--surface-inset` (`#E5E9F0`) e `--accent-point` em **Cerulean Sapphire** (`#0284C7`), **Ocean Sapphire** (`#1E6091`) ou **Clinical Emerald** (`#059669`).
- **`[FAIL: COBALTO_OU_BORDA_DURA_CLINICA]`**: Presença de azul cobalto/neon (`#0044FF`, `#0057FF`, `#233DFF`, `#1D4ED8`), `backdrop-filter: blur()` ou bordas duras de `1px` (`border-slate-200`) em cards clínicos.
- **`[UNVERIFIED]`**: Arquivos de estilo/componentes da interface clínica não fornecidos ou inacessíveis.

## 2. Ergonomia Tátil, Zero Emojis, Tipografia Tabular e Impressão A4 (`[DISC-TATIL]`)
- **`[PASS]`**: Zero caracteres emoji na interface (uso exclusivo de ícones vetoriais Lucide `stroke-width="1.5"` a `"1.75"`), alvos de toque $\ge 44\times44\text{px}$ com blindagem `anti-squish` (`flex-shrink: 0; white-space: nowrap` preservando unidades como `mg/dL`, `mL/min`, `mEq/L`), doses/exames em `JetBrains Mono` com `font-variant-numeric: tabular-nums` e folha `@media print` calibrada para papel A4 sem sombras nem sidebars.
- **`[FAIL: EMOJI_OU_DESALINHAMENTO_CLINICO]`**: Presença de qualquer emoji em botões/badges, quebra de linha em unidades médicas, ausência de `tabular-nums` em tabelas numéricas ou falta de `@media print` em telas de prescrição/receituário.

## 3. Delegação Determinística de Cálculos e Máquina de Estados FSM (`[DISC-OPCOES]` & `[DISC-SUPPLY]`)
- **`[PASS]`**: Fórmulas médicas (clearance renal, infusão, correção eletrolítica) são executadas por funções determinísticas tipadas e testadas (ou `agy_deterministic_calc_suite`), inputs validam faixas fisiológicas com alerta semântico `role="alert" aria-live="assertive"`, e o projeto atinge `Verdict: PASS` (`Readiness >= 90.0`) no `scripts/audit_tactile_ui.py`.
- **`[FAIL: RISCO_CLINICO_OU_SEM_FSM]`**: Cálculo de doses delegado a inferência livre de LLM, ausência de validação de limites fisiológicos ou reprovação no `audit_tactile_ui.py`.
