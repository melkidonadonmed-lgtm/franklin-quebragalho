# Matriz de Referência: Acessibilidade WCAG 2.1 AA, Tokens em 3 Camadas (`OKLCH`), Física da Luz, Nitidez GPU e Estados Real-State (`frontend-testing-auditor` v5.0.0)

Documento de referência técnica para inspeção determinística via `scripts/audit_tactile_ui.py` e suítes `jest-axe` / `Playwright` alinhado aos **9 Eixos da SSOT**.

---

## 1. Rubrica de Pesos e Aprovação (`Score >= 90.0`)

$$\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$$

| Pilar | Código | Peso | Limiar Mínimo | Indicadores Verificados |
| :--- | :---: | :---: | :---: | :--- |
| **Nitidez GPU, Nav Adaptável, Acessibilidade & Tabular** | `AUDIT-A11Y-01/02` | `35%` | `85.0` | Contraste WCAG AA $\ge 4.5:1$, `antialiased` + `font-synthesis: none`, zero `scale()` fracionário em textos, `:focus-visible`, Único DOM Nav Adaptável (`env(safe-area-inset-bottom)` $\leftrightarrow$ Sidebar `240px`), Breadcrumbs (`<ol role="list">` + `::before` silencioso + `aria-current="page"` $\ge 3:1$), Ordem DOM = Visual, `tabular-nums`, `any-pointer: coarse` (`48x48px`), `transition-behavior: allow-discrete` separado e `prefers-reduced-motion`. |
| **Engenharia Real-State & Estados (FSM)** | `AUDIT-STATE-01/02` | `30%` | `85.0` | Atributos executáveis `data-state` (`idle`, `loading`, `error`, `empty`, `pressed`), `data-variant` (`elevated`, `outlined`, `subtle`), `aria-busy`, `role="status"`, `role="alert"`, zero comment-gaming e zero placebos. |
| **Tokens 3 Camadas (`OKLCH`), Espaçamento & Sombras** | `AUDIT-VIS-01` | `20%` | `85.0` | Famílias `--bg-canvas`/`--surface-canvas` (`oklch()`, `light-dark()`), escala de espaçamento `4px/8px` (`--space-*`) + semânticos (`--space-card-padding`, `--space-grid-gap`), raios concêntricos ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$), `subgrid` + `:has(> img)`, luz zenital (`inset 0 1px 0 0`), sombras multi-camadas (`--shadow-elevation-1/2/3`), zero emojis. |
| **Segurança Anti-XSS** | `AUDIT-SEC-01` | `15%` | `100.0` | Zero `eval()`, zero `dangerouslySetInnerHTML` sem `DOMPurify.sanitize()` (exceto script estático anti-FOUC de `data-theme`). |

---

## 2. Template de Teste Automatizado (`SurfaceCard.test.tsx`)

```tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { SurfaceCard } from './SurfaceCard';

expect.extend(toHaveNoViolations);

describe('Deterministic UI Audit (9 Axes): <SurfaceCard />', () => {
  it('[AUDIT-A11Y-01] deve passar no motor Axe-Core com 0 violações WCAG 2.1 AA', async () => {
    const { container } = render(
      <SurfaceCard title="Receita Recorrente" eyebrow="FINTECH" variant="elevated">
        <p className="tabular-metric">R$ 128.450,00</p>
      </SurfaceCard>
    );
    expect(await axe(container)).toHaveNoViolations();
  });

  it('[AUDIT-STATE-01/02] deve transitar entre loading, error e pressed na máquina de estados', () => {
    const { rerender } = render(<SurfaceCard title="Telemetria" isLoading={true}><span>OK</span></SurfaceCard>);
    expect(screen.getByRole('status')).toHaveAttribute('aria-busy', 'true');
    rerender(<SurfaceCard title="Telemetria" isLoading={false} error="Timeout"><span>OK</span></SurfaceCard>);
    expect(screen.getByRole('alert')).toHaveTextContent('Timeout');
    rerender(<SurfaceCard title="Telemetria" isLoading={false} error={null}><span>Estável</span></SurfaceCard>);
    const card = screen.getByRole('article', { name: 'Telemetria' });
    fireEvent.mouseDown(card);
    expect(card).toHaveAttribute('data-state', 'pressed');
    fireEvent.mouseUp(card);
    expect(card).toHaveAttribute('data-state', 'idle');
  });

  it('[AUDIT-SEC-01] deve escapar strings maliciosas prevenindo XSS', () => {
    const xssPayload = '<img src=x onerror="alert(1)" />';
    render(<SurfaceCard title="Input Seguro"><p>{xssPayload}</p></SurfaceCard>);
    expect(screen.getByText(xssPayload)).toBeInTheDocument();
  });
});
```
