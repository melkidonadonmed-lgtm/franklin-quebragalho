# Reference Matrix: WCAG 2.1 AA Accessibility, 3-Layer `OKLCH` Tokens, Light Physics, GPU Sharpness & Real-State FSM (`frontend-testing-auditor` v5.0.0)

Technical reference for deterministic auditing via `scripts/audit_tactile_ui.py` and `jest-axe` / Playwright suites aligned with the **9-Axis SSOT**.

---

## 1. Weighting Rubric & Passing Gate (`Readiness Score >= 90.0`)

$$\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$$

| Pillar | Rule Code | Weight | Min Threshold | Verified Indicators |
| :--- | :---: | :---: | :---: | :--- |
| **GPU Sharpness, Adaptive Nav, A11y & Tabular** | `AUDIT-A11Y-01/02` | `35%` | `85.0` | WCAG AA contrast $\ge 4.5:1$, `antialiased` + `font-synthesis: none`, zero fractional `scale()` on text, `:focus-visible`, Single-DOM Adaptive Nav (`env(safe-area-inset-bottom)` $\leftrightarrow$ `240px` Sidebar), Breadcrumbs (`<ol role="list">` + silent `::before` + `aria-current="page"` $\ge 3:1$), DOM = Visual order, `tabular-nums`, `any-pointer: coarse` (`48x48px`), separate `transition-behavior: allow-discrete`, and `prefers-reduced-motion`. |
| **Real-State Engineering & FSM** | `AUDIT-STATE-01/02` | `30%` | `85.0` | Executable attributes `data-state` (`idle`, `loading`, `error`, `empty`, `pressed`), `data-variant` (`elevated`, `outlined`, `subtle`), `aria-busy`, `role="status"`, `role="alert"`, zero comment-gaming, and zero placebos. |
| **3-Layer `OKLCH` Tokens, Spacing & Shadows** | `AUDIT-VIS-01` | `20%` | `85.0` | Families `--bg-canvas`/`--surface-canvas` (`oklch()`, `light-dark()`), `4px/8px` spacing scale (`--space-*`) + semantic intent (`--space-card-padding`, `--space-grid-gap`), concentric radii ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$), `subgrid` + `:has(> img)`, zenith light (`inset 0 1px 0 0`), multi-layer shadows (`--shadow-elevation-1/2/3`), zero UI emojis. |
| **Anti-XSS Security** | `AUDIT-SEC-01` | `15%` | `100.0` | Zero `eval()`, zero `dangerouslySetInnerHTML` without `DOMPurify.sanitize()` (except static anti-FOUC `data-theme` script). |

---

## 2. Automated Test Suite Template (`SurfaceCard.test.tsx`)

```tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { SurfaceCard } from './SurfaceCard';

expect.extend(toHaveNoViolations);

describe('Deterministic UI Audit (9 Axes): <SurfaceCard />', () => {
  it('[AUDIT-A11Y-01] passes Axe-Core with 0 WCAG 2.1 AA violations', async () => {
    const { container } = render(
      <SurfaceCard title="Recurring Revenue" eyebrow="FINTECH" variant="elevated">
        <p className="tabular-metric">$128,450.00</p>
      </SurfaceCard>
    );
    expect(await axe(container)).toHaveNoViolations();
  });

  it('[AUDIT-STATE-01/02] transitions across loading, error, and pressed FSM states', () => {
    const { rerender } = render(<SurfaceCard title="Telemetry" isLoading={true}><span>OK</span></SurfaceCard>);
    expect(screen.getByRole('status')).toHaveAttribute('aria-busy', 'true');
    rerender(<SurfaceCard title="Telemetry" isLoading={false} error="Timeout"><span>OK</span></SurfaceCard>);
    expect(screen.getByRole('alert')).toHaveTextContent('Timeout');
    rerender(<SurfaceCard title="Telemetry" isLoading={false} error={null}><span>Healthy</span></SurfaceCard>);
    const card = screen.getByRole('article', { name: 'Telemetry' });
    fireEvent.mouseDown(card);
    expect(card).toHaveAttribute('data-state', 'pressed');
    fireEvent.mouseUp(card);
    expect(card).toHaveAttribute('data-state', 'idle');
  });

  it('[AUDIT-SEC-01] escapes malicious strings preventing XSS injection', () => {
    const xssPayload = '<img src=x onerror="alert(1)" />';
    render(<SurfaceCard title="Safe Input"><p>{xssPayload}</p></SurfaceCard>);
    expect(screen.getByText(xssPayload)).toBeInTheDocument();
  });
});
```
