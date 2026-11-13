---
name: frontend-testing-auditor
description: "Audita qualidade de interfaces web via audit_tactile_ui.py verificando WAI-ARIA, zero emojis, zero bloat Base64, OKLCH e anti-XSS. Use para validar qualidade de UI; não use para implementar componentes."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "5.0.0"
  updated_at: "2026-11-13"
  author: "UI-Architect & Melki"
  category: "Frontend QA, Accessibility, OKLCH 3-Layer Tokens, Optical Physics & Deterministic Auditing"
  tags: ["frontend-testing", "oklch", "axe-core", "wcag-aa", "anti-borrao-gpu", "deterministic-audit"]
---

# Frontend Testing & Deterministic Auditor (`frontend-testing-auditor`)

## 1. Propósito e Gatilhos (Quando Usar)

Esteira **determinística** de testes (`jest-axe` / `Vitest` / `Playwright`) e inspeção estática AST/regex (`scripts/audit_tactile_ui.py`) alinhada aos **9 Eixos** ([`../../rules/diretrizes-frontend-9-eixos.md`](../../rules/diretrizes-frontend-9-eixos.md)) e [`../design-md/SKILL.md`](../design-md/SKILL.md):

- Validar tokens `OKLCH` em 3 camadas, sombras zenitais, `tabular-nums`, WAI-ARIA/WCAG 2.1 AA, FSM real, anti-orfandade, zero emojis/Base64 `> 50 KB` e anti-XSS.
- Criar suítes `*.test.tsx` / `*.spec.ts` com React Testing Library, Vitest/Jest, `jest-axe` e Playwright.

## 2. Entradas e Pré-requisitos

- **`target_path` (obrigatório):** Diretório `src/` (Níveis 2/3) ou arquivo `.html`/`.tsx`/`.css` (Nível 1).
- **`design_contract` (opcional):** Contrato `DESIGN.md` de referência.

## 3. Processamento nos 4 Pilares e Execução

Consulte detalhes em [`references/matriz_4_pilares_auditoria.md`](references/matriz_4_pilares_auditoria.md) e [`references/a11y_fsm_rubric.md`](references/a11y_fsm_rubric.md):

1. **`AUDIT-A11Y` (`35%`):** Zero violações `axe-core` / WCAG AA, nitidez GPU, `tabular-nums`, Ordem DOM = `Tab`, Bottom Bar $\leftrightarrow$ Sidebar Rail, `any-pointer: coarse` $\ge 48\text{px}$, `allow-discrete` e `prefers-reduced-motion`.
2. **`AUDIT-STATE` (`30%`):** FSM executável (`idle | loading | empty | error | pressed`), `data-state`/`aria-busy`/`role="status"`, zero placebos e anti-comment-gaming (`-25 pts`).
3. **`AUDIT-VIS-01` (`20%`):** Tokens 3 camadas (`oklch`/`light-dark`), luz zenital/3 sombras, anti-orfandade (`-25 pts`), zero emojis e zero Base64 `> 50 KB`.
4. **`AUDIT-SEC` (`15%`):** Anti-XSS (`DOMPurify.sanitize()`, zero `eval()`).

```powershell
uv run python skills/frontend-testing-auditor/scripts/audit_tactile_ui.py <caminho_do_projeto_ou_arquivo>
```

## 4. Saídas e Entregáveis

$$\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$$

- **Aceite (`PASS` — [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)):** $\text{Score} \ge 90.0$, $S_{\text{Tokens}} \ge 85.0$ e $S_{\text{FSM}} \ge 85.0$.

## 5. Exceções, Limites e Quando NÃO Usar

- **Backend Puro ou Scaffolding:** Não use para unit tests Python/Go/SQL sem DOM, nem para estruturar pastas iniciais (`frontend-code-architect`, `design-md`).
- **DOM Live / Snapshot Browser:** `audit_tactile_ui.py` é estático; para `take_snapshot`/DOM ao vivo via CDP/browser combine com `auditoria-projetos-sistema` ou `complex-zero`.
