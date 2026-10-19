# Guia de Tokens Clínicos, Tipografia Tabular e Impressão A4 (`design-interface-medica-minimalista` v2.2.0)

Referência técnica de Tier 3 para interfaces clínicas, prontuários eletrônicos (PEP), calculadoras médicas e receituários sob o contrato **`DESIGN.md v4.5-soft`** (Módulos **M3** e **M7**).

---

## 1. Presets Tonais Clínicos (`DESIGN.md v4.5-soft` — Zero Cobalto)

| Preset Clínico | `--surface-canvas` (60%) | `--surface-raised` (30%) | `--surface-inset` | `--accent-point` (10%) | Uso Clínico Recomendado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`slate` (Diurno Padrão)** | `#F1F4F8` | `#F1F4F8` (`.ui-card-soft` 135°) | `#E5E9F0` | `#0284C7` (*Cerulean Sapphire*) | Prontuário ambulatorial, calculadoras e prescrição hospitalar |
| **`sapphire` (Leitura Longa)** | `#F5F4EE` | `#FAF9F5` (`.ui-card-soft` 135°) | `#EAE8DF` | `#1E6091` (*Ocean Sapphire*) | Evolução clínica extensa, anamnese e revisão de prontuários |
| **`moss` (Conforto Cirúrgico)** | `#F4F3EC` | `#F9F8F3` (`.ui-card-soft` 135°) | `#E6E5DC` | `#174930` (*Forest Moss*) | Farmácia clínica, checagem de aprazamento e protocolos |
| **`obsidian` (Plantão Noturno)** | `#12151B` | `#181D26` ($L_{\text{card}} > L_{\text{canvas}}$) | `#0D1015` | `#38BDF8` (*Mineral Ice*) | UTI, emergência e plantão noturno com baixa luminância ambiente |

> **Banimento Estrito (`AUDIT-VIS-01`)**: Proibido `#0044FF`, `#0057FF`, `#233DFF`, `#1D4ED8`, `backdrop-filter: blur()`, bordas duras `1px` (`border-slate-200`) e qualquer emoji em componentes clínicos.

---

## 2. Tipografia Tabular e Blindagem de Unidades Médicas

```css
/* Precisão numérica obrigatória para doses, exames laboratoriais e escores */
.clinical-metric,
.dosage-value,
.lab-result-table td {
  font-family: 'JetBrains Mono', monospace;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
}

/* Blindagem Anti-Squish para botões de conduta e badges de unidades (mg/dL, mL/min, mcg/kg/min) */
.clinical-action-btn,
.unit-badge-soft {
  min-height: 44px;
  flex-shrink: 0;
  white-space: nowrap;
}
```

---

## 3. Folha de Estilo de Impressão Clínica A4 (`@media print`)

Receituários, sumários de alta e prescrições devem colapsar a navegação e remover sombras neumórficas na impressão física/PDF para máxima nitidez em impressoras térmicas ou laser monocromáticas:

```css
@media print {
  @page {
    size: A4 portrait;
    margin: 15mm 18mm;
  }

  body,
  .ui-card-soft {
    background: #FFFFFF !important;
    color: #0F172A !important;
    box-shadow: none !important;
  }

  aside,
  nav,
  #sidebar-active-tracker,
  .no-print {
    display: none !important;
  }

  .prescription-block {
    break-inside: avoid;
    page-break-inside: avoid;
    padding: 8mm 0;
  }
}
```

---

## 4. Segurança Clínica e Delegação Determinística (`M7`)

1. **Zero Cálculo de Dose por LLM**: Toda fórmula médica (ex.: Cockcroft-Gault, CKD-EPI, Parkland, infusão em `mL/h`) deve residir em função pura tipada com testes unitários determinísticos ou na tool `agy_deterministic_calc_suite`.
2. **Faixas Fisiológicas Explícitas**: Inputs numéricos (`surface-inset`) devem validar limites fisiológicos plausíveis (ex.: Peso `0.5–350 kg`, Creatinina `0.1–25 mg/dL`) exibindo erro semântico `role="alert" aria-live="assertive"` fora da faixa.
