---
name: frontend-testing-auditor
description: >-
  Gatekeeper determinístico de testes e qualidade frontend (scripts/audit_tactile_ui.py + Jest/Vitest + Axe-Core) para auditar arquitetura visual por propósito, contraste (WCAG AA/AAA), tipografia tabular (tabular-nums), camadas esculpidas, componentes órfãos, estados finitos FSM e anti-XSS. Não use para scaffolding (use frontend-code-architect).
version: "3.0.0"
license: MIT
compatibility: "Jest, Vitest, React Testing Library, Playwright, @axe-core/playwright, jest-axe, Python 3.11+"
metadata:
  author: "FrontCraftMaster & Melki"
  version: "3.0.0"
  category: "Frontend QA, Accessibility, Purpose-Driven Style & Deterministic Auditing"
  updated_at: "2026-10-19"
  tags:
    - "frontend-testing"
    - "axe-core"
    - "wcag-aa"
    - "estilo-por-proposito"
    - "deterministic-audit"
updated_at: 2026-10-19
author: FrontCraftMaster & Melki
category: Frontend QA, Accessibility, Purpose-Driven Style & Deterministic Auditing
authorized_sub_skills:
  - name: minimal-impact-ui
    role: "Referência Ex Umbris + WinUI 3 Gallery (atlas_ex_umbris_winui.html, 3 temas, 6 arquétipos e 28 efeitos)"
  - name: frontend-code-architect
    role: "Correção estrutural de componentes que reprovarem nos testes determinísticos"
  - name: design-md
    role: "Validação cruzada de tokens e estilo contra o contrato DESIGN.md"
---

# 🛡️ Frontend Testing & Deterministic Auditor (`frontend-testing-auditor` v3.0.0)

## 1. OBJETIVO E DIRETRIZES DE ATIVAÇÃO

Esta Skill fornece uma esteira **determinística** de testes automatizados e auditoria estática para interfaces web modernas. Ela substitui avaliações subjetivas por **métricas verificáveis** de acessibilidade (Axe-Core / WCAG 2.1 AA), máquina de estados finitos (`idle`, `loading`, `error`, `pressed`), **adequação de estilo, contraste, nitidez tipográfica, espaçamento e camadas ao propósito do projeto** (`AUDIT-VIS-01`, alinhado a [`../minimal-impact-ui/SKILL.md`](../minimal-impact-ui/SKILL.md) e [`../minimal-impact-ui/references/atlas_ex_umbris_winui.html`](../minimal-impact-ui/references/atlas_ex_umbris_winui.html)) e segurança anti-XSS (`AUDIT-SEC-01`).

### ✅ Gatilhos Positivos (Quando Usar):
- Auditoria de componentes React/TypeScript, Vue ou HTML/CSS após geração pelo `frontend-code-architect` ou `minimal-impact-ui`.
- Validação determinística via [`scripts/audit_tactile_ui.py`](scripts/audit_tactile_ui.py) de tokens semânticos (`--bg-canvas`, `--bg-surface`, `--ink-primary`), camadas esculpidas (`--shadow-sculpted` + `--rim-light`), alinhamento numérico (`tabular-nums`), estados FSM e ausência de componentes órfãos.
- Criação de suítes de testes `*.test.tsx` ou `*.spec.ts` com **React Testing Library**, **Vitest/Jest**, **jest-axe** e **Playwright**.

### ❌ Quando NÃO Usar (Limites e Exceções):
- Testes unitários de backend puro (Python/Go/SQL) sem DOM ou interface visual.
- Para criar a estrutura inicial de pastas do zero (use `frontend-code-architect` ou `minimal-impact-ui`).

---

## 📥 Entradas e Pré-requisitos
- `target_path`: Caminho do diretório ou arquivo frontend a ser auditado por `scripts/audit_tactile_ui.py` e `jest-axe`.

---

## 2. FLUXO DE EXECUÇÃO — MATRIZ DE AUDITORIA DETERMINÍSTICA (4 PILARES)

### Pilar 1: Acessibilidade, Contraste, Nitidez Tipográfica, Foco & Alinhamento Tabular (`AUDIT-A11Y` — 35%)
- **`[AUDIT-A11Y-01]` Zero Violações Axe-Core, Nitidez & Contraste:** Nenhum componente pode falhar nas regras WCAG 2.1 AA ($\ge 4.5:1$ para texto normal; $\ge 7.0:1$ para títulos/métricas críticas; tinta escura `#16151A` em menus `#8e8999`; texto escuro `#091318`/`#062016` em botões Azul `#35acd8`/Verde `#10B981`; zero letras vermelhas puras `#e13535` embaçadas sobre cinza `#57545d` — usar `.accent-text` ou `.highlight-surgical`).
- **`[AUDIT-A11Y-02]` Navegabilidade por Teclado, `tabular-nums` & Proteção Vestibular:** Todo elemento interativo deve ser alcançável via `Tab` (`:focus-visible`), exibir números dinâmicos com `font-variant-numeric: tabular-nums` e respeitar `@media (prefers-reduced-motion: reduce)`.

### Pilar 2: Máquina de Estados Finitos Executável (`AUDIT-STATE` — 30%)
- **`[AUDIT-STATE-01]` Estados Finitos (`idle | loading | error | pressed`):** O componente deve expor atributos executáveis (`data-state`, `data-theme`, `aria-busy="true"`, `role="status"` / `role="alert"`).
- **`[AUDIT-STATE-02]` Anti-Comment-Gaming:** Comentários estáticos simulando estados (`// idle | loading | error`) são removidos antes da análise e penalizados em `-25 pts`.

### Pilar 3: Tokens Semânticos por Propósito, Camadas Esculpidas & Anti-Orfandade (`AUDIT-VIS-01` — 20%)
- **`[AUDIT-VIS-01]` Conformidade Arquitetural & Camadas:**
  1. Aceita qualquer família semântica alinhada ao propósito do projeto (*Ex Umbris Ad Lucem / `minimal-impact-ui`*: `--bg-canvas`, `--bg-surface`, `--ink-primary`; *AETHER 2027*: `--surface-canvas`, `--surface-primary`, `--ink-primary`; ou *Studio v4.5*: `--surface-canvas`, `--surface-raised`, `--text-primary`).
  2. Verifica a presença de **elevação em camadas esculpidas** (`--shadow-sculpted`, `--rim-light`, `.sculpted-card`, `.terrixa-card`, `.bento-card` ou `.ui-card-soft`) e alternância rítmica (`.surface-contrast`).
  3. **Detecção de Componentes Órfãos (`-25 pts`):** Reprova automaticamente projetos que criam `SurfaceCard.tsx` ou `SoftCard.tsx` em `src/components/ui/` mas não os importam nas views reais.

### Pilar 4: Segurança Frontend & Sanitização (`AUDIT-SEC` — 15%)
- **`[AUDIT-SEC-01]` Prevenção de XSS:** Proibido `dangerouslySetInnerHTML` sem `DOMPurify.sanitize()` ou uso de `eval()`.

---

## 3. TEMPLATE DE TESTE AUTOMATIZADO (`SurfaceCard.test.tsx`)

```tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { SurfaceCard } from './SurfaceCard';

expect.extend(toHaveNoViolations);

describe('Deterministic UI Audit: <SurfaceCard />', () => {
  it('[AUDIT-A11Y-01] deve passar no motor Axe-Core com 0 violações WCAG 2.1 AA', async () => {
    const { container } = render(
      <SurfaceCard title="Receita Recorrente" eyebrow="FINTECH">
        <p className="tabular-metric">R$ 128.450,00</p>
      </SurfaceCard>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('[AUDIT-VIS-01] deve aplicar classe sculpted-card e variante de superfície', () => {
    render(
      <SurfaceCard title=" Bloco de Destaque" variant="contrast">
        <span>Conteúdo</span>
      </SurfaceCard>
    );
    const card = screen.getByRole('article', { name: /Bloco de Destaque/i });
    expect(card).toHaveClass('sculpted-card');
    expect(card).toHaveAttribute('data-variant', 'contrast');
  });

  it('[AUDIT-STATE-01/02] deve transitar entre loading, error e pressed na máquina de estados', () => {
    const { rerender } = render(
      <SurfaceCard title="Telemetria" isLoading={true}>
        <span>OK</span>
      </SurfaceCard>
    );
    expect(screen.getByRole('status')).toHaveAttribute('aria-busy', 'true');

    rerender(
      <SurfaceCard title="Telemetria" isLoading={false} error="Timeout de conexão">
        <span>OK</span>
      </SurfaceCard>
    );
    expect(screen.getByRole('alert')).toHaveTextContent('Timeout de conexão');

    rerender(
      <SurfaceCard title="Telemetria" isLoading={false} error={null}>
        <span>Estável</span>
      </SurfaceCard>
    );
    const card = screen.getByRole('article', { name: 'Telemetria' });
    fireEvent.mouseDown(card);
    expect(card).toHaveAttribute('data-state', 'pressed');
    fireEvent.mouseUp(card);
    expect(card).toHaveAttribute('data-state', 'idle');
  });

  it('[AUDIT-SEC-01] deve escapar strings maliciosas prevenindo XSS', () => {
    const xssPayload = '<img src=x onerror="alert(1)" />';
    render(
      <SurfaceCard title="Input Seguro">
        <p>{xssPayload}</p>
      </SurfaceCard>
    );
    expect(screen.getByText(xssPayload)).toBeInTheDocument();
  });
});
```

---

## 4. SAÍDAS E ENTREGÁVEIS — RUBRICA MATEMÁTICA DE APROVAÇÃO (SCORE 0 A 100)

Execute o auditor determinístico:
```powershell
uv run python skills/frontend-testing-auditor/scripts/audit_tactile_ui.py <caminho_do_projeto_ou_arquivo>
```

$$\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$$

- **Critério de Aceite (`PASS`):** $\text{Score} \ge 90.0$, $S_{\text{Tokens}} \ge 85.0$ e $S_{\text{FSM}} \ge 85.0$.
