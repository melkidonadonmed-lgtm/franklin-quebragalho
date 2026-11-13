---
name: design-interface-medica-minimalista
description: "Arquitetura para interfaces clínicas, prontuários eletrônicos PEP, receituários e laudos A4 .sus-grid e calculadoras médicas. Use para sistemas de saúde; não use para SaaS genérico."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "5.0.0"
  updated_at: "2026-11-13"
  author: "Melki"
  category: "Design System Clínico, MedTech & Impressão Vetorial A4"
  tags: ["medtech-ui", "clinical-design", "prontuario-eletronico", "a4-print", "tabular-nums"]
---

# Design de Interface Médica Minimalista (`design-interface-medica-minimalista`)

## 1. Propósito e Gatilhos (Quando Usar)

Diretrizes visuais, ergonômicas e de segurança assistencial para sistemas de saúde sob os **9 Eixos** e contrato [`../design-md/SKILL.md`](../design-md/SKILL.md):

- Criar ou refatorar telas de Prontuário Eletrônico (PEP), prescrição, evolução clínica, triagem e calculadoras médicas (`SOFA`, `CHA2DS2-VASc`, `CKD-EPI`).
- Projetar folhas vetoriais de impressão (`@media print` / A4 `210mm × 297mm` `.sus-grid`) com **100% CSS Grid vetorial e SVG** para receituários, APAC/LME, atestados e laudos.

## 2. Entradas e Pré-requisitos

- **`clinical_context` (obrigatório):** `ambulatorio_pep`, `uti_plantao_noturno`, `calculadora_doses` ou `receituario_a4`.
- **`target_stack` (opcional):** React + TypeScript + Tailwind v4/CSS Variables ou HTML5/CSS3 standalone.

## 3. Fluxo Arquitetural Clínico (9 Eixos)

Consulte tokens e snippets completos em [`references/arquitetura_polaridades_clinicas.md`](references/arquitetura_polaridades_clinicas.md) e [`references/guia_tokens_clinicos_a4.md`](references/guia_tokens_clinicos_a4.md):

1. **Polaridades `OKLCH` & Elevação:** `clinical-day` (`0.97 -> 1.00`, contraste AAA $\ge 14:1$) vs. `clinical-night` UTI (`0.16 -> 0.21 -> 0.26`, zero `#000000`), luz zenital em 3 níveis + `--shadow-inset-sunken`, destaque acromático e 4 variantes de cards.
2. **Box Lógico, Nitidez & Dados Clínicos:** Propriedades lógicas, zero `scale()` fracionário, **zero emojis** (apenas **Lucide**), `tabular-nums` em sinais vitais/doses/CID-10 e unidades críticas (`mg/dL`, `mL/min/1.73m²`) com `white-space: nowrap; flex-shrink: 0` + alvos $\ge 44\text{px}$.
3. **Layouts, `@container` & Folha A4 `.sus-grid`:** *Workbench Split-View* ou *Command Center* com `@container`, navegação em 3 camadas e `@media print` removendo `.no-print`/`nav`/`aside` e sombras.

## 4. Saídas e Entregáveis

Componentes clínicos tipados (`.tsx`/`.html`) com estado real, CSS `@media print` A4 vetorial e auditoria via [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md) e `frontend-testing-auditor`.

## 5. Exceções, Limites e Quando NÃO Usar

- **SaaS Genérico / E-commerce / Jogos:** Fora da área de saúde, use `design-md`, `frontend-code-architect` ou `auditoria-projetos-sistema`.
- **Cálculos Clínicos em Produção:** Nunca delegue cálculo de doses, infusões ou escores a inferência livre do LLM; use função determinística tipada ou `agy_deterministic_calc_suite`.
