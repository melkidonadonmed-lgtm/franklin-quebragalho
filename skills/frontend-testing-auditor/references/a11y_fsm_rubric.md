# Matriz de Referência: Acessibilidade WCAG 2.1 AA, FSM e Tokens (`frontend-testing-auditor`)

Documento de referência técnica para inspeção determinística via `scripts/audit_tactile_ui.py` e suítes `jest-axe` / `Playwright`.

---

## 1. Rubrica de Pesos e Aprovação (`Score >= 90.0`)

$$\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$$

| Pilar | Código | Peso | Limiar Mínimo | Indicadores Verificados |
| :--- | :---: | :---: | :---: | :--- |
| **Acessibilidade & Tabular** | `AUDIT-A11Y-01/02` | `35%` | `85.0` | Contraste $\ge 4.5:1$ ($\ge 7.0:1$ títulos), `:focus-visible`, `tabular-nums`, `prefers-reduced-motion`. |
| **Máquina de Estados (FSM)** | `AUDIT-STATE-01/02` | `30%` | `85.0` | Atributos `data-state` (`idle`, `loading`, `error`, `empty`, `success`), `aria-busy`, `role="status"`, `role="alert"`. |
| **Tokens Semânticos & Camadas** | `AUDIT-VIS-01` | `20%` | `85.0` | Família `--bg-canvas` / `--bg-surface` / `--ink-primary`, elevação `--shadow-sculpted`, zero componentes órfãos. |
| **Segurança Anti-XSS** | `AUDIT-SEC-01` | `15%` | `100.0` | Zero `eval()`, zero `dangerouslySetInnerHTML` sem `DOMPurify.sanitize()`. |
