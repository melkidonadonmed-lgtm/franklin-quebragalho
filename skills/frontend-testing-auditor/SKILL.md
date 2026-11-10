---
name: frontend-testing-auditor
description: "Audita qualidade de interfaces web via audit_tactile_ui.py verificando WAI-ARIA, zero emojis, zero bloat Base64, OKLCH e anti-XSS. Use para validar qualidade de UI; não use para implementar componentes."
version: "5.0.0"
updated_at: "2026-10-27"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "5.0.0"
  updated_at: "2026-10-27"
  author: "UI-Architect & Melki"
  category: "Frontend QA, Accessibility, OKLCH 3-Layer Tokens, Optical Physics & Deterministic Auditing"
  tags: ["frontend-testing", "oklch", "axe-core", "wcag-aa", "anti-borrao-gpu", "deterministic-audit"]
---
# Frontend Testing & Deterministic Auditor (`frontend-testing-auditor` v5.0.0 — 9 Eixos, OKLCH, `@container`, Breadcrumbs & FSM)

## 1. Objetivo e Diretrizes de Ativação

Esta Skill fornece a esteira **determinística** de testes automatizados e auditoria estática para interfaces web modernas, alinhada aos **9 Eixos + Matriz de Complexidade** da Fonte Única de Verdade (SSOT) em [`Preferências de Trabalho com Agentes.md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Prefer%C3%AAncias%20de%20Trabalho%20com%20Agentes.md) e [`../design-md/SKILL.md`](../design-md/SKILL.md). Substitui avaliações subjetivas por **métricas verificáveis** de acessibilidade e Navegação em 3 Camadas (Axe-Core / WCAG 2.1 AA / Breadcrumbs), nitidez anti-borrão de GPU, tokens em 3 camadas (`OKLCH`) e sombras multi-camadas (`AUDIT-VIS-01`), estados funcionais reais (`AUDIT-STATE-01`) e segurança anti-XSS (`AUDIT-SEC-01`).

### Gatilhos Positivos (Quando Usar)

- Auditoria de componentes React/TypeScript, Next.js App Router, Vue ou HTML/CSS standalone após geração ou refatoração.
- Validação determinística via [`scripts/audit_tactile_ui.py`](scripts/audit_tactile_ui.py) de tokens semânticos em 3 camadas (`--bg-canvas`/`--surface-canvas`, `--bg-surface-1`/`--surface-card`, `--bg-surface-2`/`--surface-sunken`/`--surface-elevated`, `--surface-glass`, `--text-primary`/`--ink-primary`, `oklch()`, `light-dark()`, `color-mix()`), camadas de elevação (`--shadow-elevation-1/2/3`, `--elevation-1/2/3`, `--shadow-inset`, `--catch-light`), alinhamento numérico (`tabular-nums`), estados executáveis e ausência de componentes órfãos.
- Criação de suítes de testes `*.test.tsx` ou `*.spec.ts` com **React Testing Library**, **Vitest/Jest**, **jest-axe** e **Playwright**.

### Quando NÃO Usar (Limites e Exceções)

- Testes unitários de backend puro (Python/Go/SQL) sem DOM ou interface visual.
- Para criar a estrutura inicial de pastas do zero (use `frontend-code-architect` ou `design-md`).

---

## 1.5. Entradas e Pré-requisitos

- `target_path` (obrigatório): Caminho do diretório frontend (`src/` nos Níveis 2/3) ou arquivo standalone (`.html`, `.tsx`, `.css` no Nível 1).
- `design_contract` (opcional): Contrato `DESIGN.md` de referência.

---

## 2. Fluxo de Execução — Matriz de Auditoria Determinística (4 Pilares / 9 Eixos)

### Pilar 1: Acessibilidade, Navegação em 3 Camadas, Nitidez Anti-Borrão GPU & Alinhamento Tabular (`AUDIT-A11Y` — 35%)

- **`[AUDIT-A11Y-01]` Zero Violações Axe-Core, Nitidez Tipográfica & Contraste Neutro:** Nenhum componente pode falhar nas regras WCAG 2.1 AA ($\ge 4.5:1$). Exige travas `antialiased`, `optimizeLegibility` e `font-synthesis: none` em `html, body`, escala `clamp()`, `max-inline-size: 65ch`, `text-wrap: balance/pretty`, proíbe `scale()` fracionário em contêineres de texto e proíbe texto colorido de baixo contraste sobre fundo cinza médio.
- **`[AUDIT-A11Y-02]` Navegação Contextual, Teclado, `tabular-nums` & Proteção Vestibular:** Todo elemento interativo deve ser alcançável via `Tab` (`:focus-visible`) mantendo **Ordem do DOM = Ordem Visual** (zero `flex-direction: row-reverse` em `<nav>`), múltiplos `<nav>` com `aria-label` único (Breadcrumbs `<ol role="list">` exigidos apenas quando houver hierarquia de rotas $\ge 3$ níveis), números com `font-variant-numeric: tabular-nums`, alvos `@media (any-pointer: coarse)` $\ge 48\text{px}$ e `@media (prefers-reduced-motion: reduce)`.

### Pilar 2: Engenharia Real-State & Máquina de Estados Executável (`AUDIT-STATE` — 30%)

- **`[AUDIT-STATE-01]` Estados Finitos Reais (`idle | loading/active | empty | error | pressed`):** O componente deve expor atributos semânticos/executáveis (`data-state`, `data-theme`, `aria-busy="true"`, `role="status"` / `role="alert"`) e controles funcionais reais (proibido `setTimeout` placebo ou `alert('Em breve')`). Nomes de componentes e classes CSS são livres e devem refletir o domínio do projeto (não é obrigatório usar nomes fixos como `SurfaceCard` ou `.sculpted-card`).
- **`[AUDIT-STATE-02]` Anti-Comment-Gaming:** Comentários estáticos simulando estados (`// idle | loading | error`) são removidos antes da análise e penalizados em `-25 pts`.

### Pilar 3: Tokens em 3 Camadas (`OKLCH`), Sombras Multi-Camadas, `@container`, 4 Cards & Anti-Orfandade (`AUDIT-VIS-01` — 20%)

- **`[AUDIT-VIS-01]` Conformidade Óptica, Box Lógico & Camadas:**
  1. Verifica o uso de famílias semânticas de superfície e tinta (`--bg-canvas`/`--bg-surface-1`/`--text-primary` ou `--surface-canvas`/`--surface-card`/`--ink-primary` em `oklch()` / `light-dark()`) e estrutura de pastas compatível com os **3 Níveis de Complexidade** (Nível 1 `@layer`/standalone, Nível 2 `src/features/` + `src/components/ui/`, Nível 3 `src/app/(marketing)` + `(workspace)` + `_components`).
  2. Verifica a presença de **iluminação zenital** (`inset 0 1px 0 0` / `--catch-light`), **sombras multi-camadas em 3 níveis** (Umbra + Penumbra com `spread` negativo via `--shadow-elevation-1/2/3` ou `--elevation-1/2/3`) e cavidade (`--shadow-inset` / `--sunken-recess`).
  3. **Detecção de Componentes Órfãos (`-25 pts`), Zero Emojis (`AUDIT-VIS-EMOJI`) e Zero Bloat Base64 (`AUDIT-VIS-BLOAT`):** Reprova automaticamente componentes (`Card.tsx`, `SurfaceCard.tsx`, `SoftCard.tsx`) criados em `src/components/ui/` mas não importados nas views/features, emojis na interface e ativos Base64 `> 50 KB`.

### Pilar 4: Segurança Frontend & Sanitização (`AUDIT-SEC` — 15%)

- **`[AUDIT-SEC-01]` Prevenção de XSS:** Proibido `dangerouslySetInnerHTML` sem `DOMPurify.sanitize()` (exceto o script estático síncrono anti-FOUC no `<head>` que apenas lê `localStorage` e aplica `document.documentElement.setAttribute('data-theme', saved)`) ou uso de `eval()`.

---

## 3. Template de Teste Automatizado (`SurfaceCard.test.tsx`)

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
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('[AUDIT-VIS-01] deve aplicar classe sculpted-card e as 4 variantes de Card', () => {
    render(
      <SurfaceCard title="Bloco de Destaque" variant="outlined" interactive={true}>
        <span>Conteúdo</span>
      </SurfaceCard>
    );
    const card = screen.getByRole('article', { name: /Bloco de Destaque/i });
    expect(card).toHaveClass('sculpted-card');
    expect(card).toHaveAttribute('data-variant', 'outlined');
    expect(card).toHaveAttribute('data-interactive', 'true');
  });

  it('[AUDIT-STATE-01/02] deve transitar entre loading, error, empty e pressed na máquina de estados', () => {
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

## 4. Saídas e Entregáveis — Rubrica Matemática de Aprovação (Score 0 a 100)

Execute o auditor determinístico:
```powershell
uv run python skills/frontend-testing-auditor/scripts/audit_tactile_ui.py <caminho_do_projeto_ou_arquivo>
```

$$\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$$

- **Critério de Aceite (`PASS`):** $\text{Score} \ge 90.0$, $S_{\text{Tokens}} \ge 85.0$ e $S_{\text{FSM}} \ge 85.0$.
