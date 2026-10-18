---
name: frontend-testing-auditor
description: >-
  Audita componentes e interfaces frontend com rigor técnico e matemático sob o paradigma Minimalist Impact e Soft UI (DESIGN.md v4.5-soft). Mede acessibilidade WCAG 2.1 AA (Axe-Core AUDIT-A11Y-01/02), fidelidade de camadas tonais e ausência de glassmorphism/cobalto/neon (AUDIT-VIS-01), determinismo de estados finitos FSM (AUDIT-STATE-01/02), sanitização XSS (AUDIT-SEC-01) e calcula o Score ponderado de prontidão (0-100).
version: "2.5.0"
license: MIT
compatibility: "React 18+, TypeScript 5+, Jest, Vitest, React Testing Library, Axe-Core, Tailwind CSS / Vanilla CSS"
metadata:
  author: "FrontCraftMaster & Melki"
  version: "2.5.0"
  category: "Auditoria de Testes Frontend, A11y e Soft UI"
  updated_at: "2026-10-18"
  tags:
    - "frontend-testing"
    - "axe-core"
    - "fsm"
    - "soft-ui-audit"
    - "minimalist-impact"
updated_at: 2026-10-18
author: FrontCraftMaster & Melki
category: Auditoria de Testes Frontend, A11y e Soft UI
authorized_sub_skills:
  - name: frontend-code-architect
    role: "Correção estrutural do componente em Design Atômico quando reprovado na auditoria"
  - name: design-md
    role: "Verificação do contrato canônico DESIGN.md v4.5-soft"
---

# 🛡️ SKILL: Auditor de Testes Frontend & UI de Alto Rigor Técnico (`frontend-testing-auditor` v2.5.0 — Soft Tactile & Minimalist Impact)

## 1. OBJETIVO E QUANDO USAR (GATILHOS DE ATIVAÇÃO)
Esta Skill substitui "testes por testes" (testes superficiais de renderização rasa) por uma esteira de auditoria determinística, matemática e estrutural adaptada para **Minimalist Impact & Neumorfismo Suave (*Soft UI* `v4.5-soft`)**. Cada teste gerado ou executado responde rigorosamente ao **O QUE**, **COMO** e **POR QUE** está sendo auditado.

### Quando Usar:
- Auditar ou criar suítes de testes (`Jest` / `Vitest` + `React Testing Library` + `jest-axe`) para componentes React, Next.js ou HTML/CSS.
- Verificar conformidade matemática com o `DESIGN.md v4.5-soft` (`AUDIT-VIS-01`: presença de `.ui-card-soft`, ausência de `backdrop-filter: blur`, ausência de azul cobalto `#0044FF`/`#0057FF` e ausência de neons).
- Validar transições determinísticas de Máquina de Estados Finita ($FSM = \{\text{Idle}, \text{Loading}, \text{Error}, \text{Pressed}\}$) e bloqueio de injeção XSS (`AUDIT-SEC-01`).

### 🚫 Quando NÃO Usar (Limites e Exceções):
- Para testes puramente de backend em Go ou Python sem DOM/UI (utilize `test-quality-auditor`).
- Para criar o layout visual inicial do zero antes de existir componente a ser testado (utilize `frontend-code-architect`).

### As 5 Dimensões Invioláveis da Auditoria:
1. **Contrato & Tipagem Estrita (Zero-Trust Props):** Garante que o componente rejeite propriedades malformadas, respeite generics de TypeScript e previna vazamentos de tipo.
2. **Acessibilidade WCAG 2.1 AA (Axe-Core & DOM Semântico — `AUDIT-A11Y-01/02`):** Calcula contraste luminoso real ($C \ge 4.5:1$ para corpo de texto, $7:1$ para títulos), mapeia árvore de acessibilidade (ARIA Roles) e valida navegação por teclado sem anéis neon.
3. **Integridade de Camadas Tonais & Elevação Tactile (`AUDIT-VIS-01`):** Audita a presença de variáveis CSS de superfície (`--surface-canvas`, `--surface-raised`, `--surface-inset`), ausência de bordas duras de 1px, ausência de glassmorphism (`backdrop-filter: blur`), ausência de azul cobalto (`#0044FF`, `#0057FF`, `#1D4ED8`) e presença de sombras difusas duplas a 135°.
4. **Determinismo de Estados Finitos (`AUDIT-STATE-01/02`) & Resiliência:** Modela o componente como uma Máquina de Estados Finita ($FSM = \{ \text{Idle}, \text{Loading}, \text{Error}, \text{Pressed} \}$), testando transições táticas e estados ativados (`surface-inset`).
5. **Sanitização XSS & Eficiência de DOM (`AUDIT-SEC-01`):** Valida que strings maliciosas (`<img src=x onerror=alert(1)>`) sejam escapadas como texto seguro e que o componente não provoque re-renderizações em cascata.

---

## 2. ENTRADAS OBRIGATÓRIAS E PRÉ-REQUISITOS
1. **Componente ou Página Alvo:** Arquivo `.tsx`, `.jsx` ou `.html` a ser auditado (ex.: `SoftCard.tsx`).
2. **Contrato de Tokens (`DESIGN.md` v4.5-soft):** Superfícies tonais e classes esperadas (`.ui-card-soft`, `.ui-btn-tactile`, `.surface-inset`).
3. **Runner de Testes:** `Jest` ou `Vitest` com `@testing-library/react`, `@testing-library/jest-dom` e `jest-axe`.

---

## 3. FLUXO OPERACIONAL DE AUDITORIA PASSO A PASSO

### 📋 PASSO 1: Mapeamento da Máquina de Estados e Contrato Tátil

| Estado da UI | Propriedades / Triggers | Saída Esperada no DOM | Invariante de Acessibilidade & Estilo |
| :--- | :--- | :--- | :--- |
| **Idle / Default** | `data={null}, isLoading={false}` | Renderiza estrutura base em relevo suave | `aria-busy="false"`, classe `.ui-card-soft` |
| **Loading** | `isLoading={true}` | Skeleton / Container `surface-inset` com `role="status"` | `aria-busy="true"`, `aria-live="polite"` |
| **Error** | `error="Falha na conexão com a API"` | Banner de erro semântico (`role="alert"`) | `aria-live="assertive"`, oculta conteúdo inválido |
| **Pressed / Active** | `onClick` / `:active` | Modificação física da superfície para `surface-inset` | Foco retido visivelmente sem brilho neon |

---

### 🧪 PASSO 2: Código da Suíte de Testes (`SoftCard.test.tsx` — Jest + RTL + Axe)

```typescript
import React from 'react';
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import '@testing-library/jest-dom';
import { SoftCard } from './SoftCard';

expect.extend(toHaveNoViolations);

describe('🛡️ Auditoria Técnica de Alta Fidelidade (Soft UI v4.5) — <SoftCard />', () => {

  // =========================================================================
  // 1. AUDITORIA DE ACESSIBILIDADE E ÁRVORE DOM (WCAG 2.1 AA)
  // =========================================================================
  describe('1. Acessibilidade & Semântica DOM', () => {
    test('AUDIT-A11Y-01: Não deve conter violações automáticas de acessibilidade no Axe Engine', async () => {
      const { container } = render(
        <SoftCard title="Métrica de Teste" badgeText="Ativo">
          <p>Conteúdo de Leitura Limpa</p>
        </SoftCard>
      );

      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    test('AUDIT-A11Y-02: Deve suportar navegação por teclado e gerenciamento de foco sem anéis neon', () => {
      render(
        <SoftCard title="Card Interativo">
          <button className="ui-btn-tactile">Ação Tátil</button>
        </SoftCard>
      );

      const cardElement = screen.getByRole('article');
      cardElement.focus();
      expect(cardElement).toHaveFocus();
    });
  });

  // =========================================================================
  // 2. AUDITORIA DE CAMADAS TONAIS E NEUMORFISMO SUAVE (SOFT UI AUDIT)
  // =========================================================================
  describe('2. Camadas Tonais & Minimalist Impact (Zero Glassmorphism / Zero Cobalto)', () => {
    test('AUDIT-VIS-01: Deve utilizar elevação por superfície e NÃO conter glassmorphism/backdrop-filter', () => {
      render(
        <SoftCard title="Card Tactile" data-testid="soft-card">
          <p>Test Content</p>
        </SoftCard>
      );

      const card = screen.getByTestId('soft-card');
      const computedStyle = window.getComputedStyle(card);

      // Valida ausência de glassmorphism genérico (blur de fundo)
      expect(computedStyle.backdropFilter).not.toContain('blur');
      expect((computedStyle as Record<string, unknown>).webkitBackdropFilter).not.toContain('blur');

      // Valida classe de superfície tátil e posição relativa
      expect(card).toHaveClass('ui-card-soft');
      expect(computedStyle.position).toBe('relative');
    });
  });

  // =========================================================================
  // 3. AUDITORIA DE MÁQUINA DE ESTADOS & RESILIÊNCIA
  // =========================================================================
  describe('3. Estados Finitos & Resiliência Assíncrona', () => {
    test('AUDIT-STATE-01: Deve transicionar de Loading para Success de forma determinística', async () => {
      const { rerender } = render(
        <SoftCard title="Status Async" isLoading={true}>
          <p>Dados Carregados</p>
        </SoftCard>
      );

      expect(screen.getByRole('status')).toBeInTheDocument();
      expect(screen.getByRole('status')).toHaveAttribute('aria-busy', 'true');

      rerender(
        <SoftCard title="Status Async" isLoading={false}>
          <p>Dados Carregados</p>
        </SoftCard>
      );

      expect(screen.getByText('Dados Carregados')).toBeInTheDocument();
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });

    test('AUDIT-STATE-02: Deve tratar estado de Erro com anúncio aria-live="assertive"', () => {
      render(
        <SoftCard title="Card com Erro" error="Falha na conexão com a API">
          <p>Conteúdo Oculto</p>
        </SoftCard>
      );

      const errorMessage = screen.getByRole('alert');
      expect(errorMessage).toBeInTheDocument();
      expect(errorMessage).toHaveTextContent('Falha na conexão com a API');
      expect(screen.queryByText('Conteúdo Oculto')).not.toBeInTheDocument();
    });
  });

  // =========================================================================
  // 4. AUDITORIA DE SEGURANÇA E INTEGRIDADE DE PROPS
  // =========================================================================
  describe('4. Sanitização & Segurança de Injeção (XSS)', () => {
    test('AUDIT-SEC-01: Não deve renderizar tags HTML maliciosas injetadas via string de título', () => {
      const maliciousScript = '<img src=x onerror=alert(1)>';
      render(<SoftCard title={maliciousScript}>Conteúdo Seguro</SoftCard>);

      expect(screen.getByText(maliciousScript)).toBeInTheDocument();
      expect(document.querySelector('img[src="x"]')).toBeNull();
    });
  });

});
```

---

## 4. SAÍDAS, ENTREGÁVEIS E RUBRICA DE AVALIAÇÃO TÉCNICA

Ao finalizar a suíte de testes, entregue o arquivo `.test.tsx` executável, a tabela de status (`AUDIT-A11Y-01/02`, `AUDIT-VIS-01`, `AUDIT-STATE-01/02`, `AUDIT-SEC-01`) e calcule o **Score de Qualidade e Prontidão de Produção (0 - 100)** usando a matriz ponderada:

$$\text{Score} = (W_{\text{a11y}} \cdot S_{\text{a11y}}) + (W_{\text{state}} \cdot S_{\text{state}}) + (W_{\text{token}} \cdot S_{\text{token}}) + (W_{\text{sec}} \cdot S_{\text{sec}})$$

Onde os pesos canônicos são:
- **$W_{\text{a11y}} = 0.35$ (35%):** Acessibilidade WCAG 2.1 AA sem violações no Axe Engine (`AUDIT-A11Y-01/02`).
- **$W_{\text{state}} = 0.30$ (30%):** Cobertura de 100% dos caminhos da Máquina de Estados ($FSM$ — `AUDIT-STATE-01/02`).
- **$W_{\text{token}} = 0.20$ (20%):** Conformidade estrita aos Design Tokens `v4.5-soft` (Tonal Layering & Soft UI, zero glassmorphism/cobalto/neon — `AUDIT-VIS-01`).
- **$W_{\text{sec}} = 0.15$ (15%):** Sanitização contra injeção XSS e contratos de props seguros (`AUDIT-SEC-01`).

### Checklist Silencioso de Liberação de Componente (Self-Refine):
- [ ] Todos os testes possuem razões explícitas de auditoria no nome (`AUDIT-A11Y-01`, `AUDIT-VIS-01`, `AUDIT-STATE-01`, `AUDIT-SEC-01`)?
- [ ] O componente foi auditado para garantir ausência de glassmorphism (`backdrop-filter: blur`), azul cobalto e neons brilhantes?
- [ ] O componente foi testado sob modo de navegação por teclado sem mouse?
- [ ] O Score ponderado final foi calculado matematicamente?
