# Matriz de Referência: Acessibilidade WCAG 2.1 AA, Tokens em 3 Camadas (`OKLCH`), Física da Luz, Nitidez GPU e Estados Real-State (`frontend-testing-auditor` v5.0.0)

Documento de referência técnica para inspeção determinística via `scripts/audit_tactile_ui.py` e suítes `jest-axe` / `Playwright` alinhado aos **9 Eixos da SSOT**.

---

## 1. Rubrica de Pesos e Aprovação (`Score >= 90.0`)

$$\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$$

| Pilar | Código | Peso | Limiar Mínimo | Indicadores Verificados |
| :--- | :---: | :---: | :---: | :--- |
| **Nitidez GPU, Nav 3 Camadas, Acessibilidade & Tabular** | `AUDIT-A11Y-01/02` | `35%` | `85.0` | Contraste WCAG AA $\ge 4.5:1$, `antialiased` + `font-synthesis: none`, zero `scale()` fracionário em textos, `:focus-visible`, Breadcrumbs (`<ol role="list">` + `aria-current="page"`), Ordem DOM = Visual, `tabular-nums`, `prefers-reduced-motion`. |
| **Engenharia Real-State & Estados (FSM)** | `AUDIT-STATE-01/02` | `30%` | `85.0` | Atributos executáveis `data-state` (`idle`, `loading`, `error`, `empty`, `pressed`), `data-variant` (`elevated`, `outlined`, `subtle`), `aria-busy`, `role="status"`, `role="alert"`, zero comment-gaming e zero placebos. |
| **Tokens 3 Camadas (`OKLCH`) & Sombras 3 Níveis** | `AUDIT-VIS-01` | `20%` | `85.0` | Famílias `--bg-canvas`/`--bg-surface-1`/`--text-primary` ou `--surface-canvas`/`--surface-card`/`--ink-primary` (`oklch()`, `light-dark()`), luz zenital (`inset 0 1px 0 0`), sombras multi-camadas (`--shadow-elevation-1/2/3` ou `--elevation-1/2/3`), zero órfãos, zero emojis. |
| **Segurança Anti-XSS** | `AUDIT-SEC-01` | `15%` | `100.0` | Zero `eval()`, zero `dangerouslySetInnerHTML` sem `DOMPurify.sanitize()` (exceto script estático anti-FOUC de `data-theme`). |
