---
name: frontend-code-architect
description: >-
  Estrutura e padroniza projetos frontend em React, Next.js, Vue ou HTML/CSS utilizando Design Atômico (5 camadas), Design Tokens (DESIGN.md v4.5-soft), matrizes BENTO Grid, escala tipográfica proporcional e Arquitetura Tátil Minimalista (Minimalist Impact & Soft Neumorphism 135°). Use para organizar diretórios src/, criar estilos modulares (globals.css) e componentes tipados (<SoftCard />) proibindo glassmorphism, neons e azul cobalto.
version: "4.0.0"
license: MIT
compatibility: "React 18+, TypeScript 5+, Tailwind CSS v3+, CSS Variables, Next.js 14+"
metadata:
  author: "FrontCraftMaster & Melki"
  version: "4.0.0"
  category: "Frontend Engineering & Design Systems"
  updated_at: "2026-10-18"
  tags:
    - "frontend-architect"
    - "atomic-design"
    - "minimalist-impact"
    - "soft-ui"
    - "anti-cobalto"
updated_at: 2026-10-18
author: FrontCraftMaster & Melki
category: Frontend Engineering & Design Systems
authorized_sub_skills:
  - name: design-md
    role: "Síntese e atualização do contrato DESIGN.md v4.5-soft"
  - name: frontend-testing-auditor
    role: "Auditoria determinística FSM + Axe-Core dos componentes gerados"
---

# 🎨 Frontend Code Architect Skill (`frontend-code-architect` v4.0.0 — Minimalist Impact & Soft Tactile Architecture)

## 1. OBJETIVO E DIRETRIZES DE ATIVAÇÃO

Esta Skill fornece procedimentos padronizados para estruturar, organizar e implementar aplicações frontend modernas de nível industrial e estética minimalista tátil (*Minimalist Impact*, *Soft UI*, *Tonal Layering 135°*).

### 🚫 PROIBIÇÕES ABSOLUTAS DE DESIGN (Anti-Patterns):
- ❌ **Não utilizar Glassmorphism / Vidro Fosco:** Proibido o uso de caixas semi-transparentes reluzentes com `backdrop-filter: blur()`.
- ❌ **Não utilizar Neons, Múltiplos Acentos ou Azul Cobalto:** Proibida a poluição visual com bordas brilhantes ou azul cobalto elétrico (`#0044FF`, `#0057FF`, `#1D4ED8`, `#233DFF`). Utilize azuis minerais serenos (**Cerulean Sapphire** `#0284C7`, **Ocean Sapphire** `#1E6091` ou **Mineral Ice** `#38BDF8`).
- ❌ **Não utilizar Bordas Duras de 1px em Containers:** Divisões de cards e painéis devem ser feitas por variação sutil de tom de superfície ou elevação neumórfica suave a 135°.

### ✅ Gatilhos Positivos (Quando Usar):
- Pedidos de criação de estrutura de pastas/diretórios (`src/`) para projetos frontend.
- Organização de componentes em **Design Atômico** (Átomos, Moléculas, Organismos, Templates e Pages).
- Criação de sistemas de **Design Tokens (`DESIGN.md` v4.5-soft)** e variáveis globais CSS baseados em **Camadas Tonais**.
- Construção de layouts BENTO, Sidebars com Tracker de Ícone (`surface-inset`) e dashboards limpos com **Neumorfismo Suave (*Soft UI*)**.
- Refatoração de código frontend para desacoplamento, tipagem estrita em TypeScript ($\le 300$ linhas/arquivo) e acessibilidade (WCAG 2.1 AA).

### ❌ Quando NÃO Usar (Limites e Exceções):
- Criação simples de scripts backend isolados sem interface visual.
- Dúvidas puramente conceituais de algoritmos sem relação com UI/UX.

---

## 2. ENTRADAS OBRIGATÓRIAS

1. **Stack Tecnológica:** (ex.: React + TypeScript + CSS Variables / Tailwind CSS, Next.js App Router, ou HTML5 + CSS3 puro).
2. **Estilo Visual Target:** *Minimalist Impact* / *Soft Neumorphism* (Paleta restrita monocromática/duo-tone em OKLCH/HEX com elevação por profundidade tonal e zero cobalto).
3. **Escopo da Aplicação:** (ex.: Dashboard BENTO, Centro de Operações Agênticas, SaaS B2B, App Clínico).

---

## 3. FLUXO OPERACIONAL PASSO A PASSO

### Passo 1: Definição dos Design Tokens (`DESIGN.md` v4.5-soft)
Compile as variáveis essenciais no padrão W3C/YAML focando em conforto e legibilidade:
- **Regra 60-30-10 Tonal Restrita:**
  - **60% Fundo Base Contínuo (`Layer 0`):** `surface-canvas` (`#F1F4F8` Off-white macio no Light; `#12151B` / `#090B10` Slate Matte escuro no Dark).
  - **30% Camadas e Elevação (`Layers 1–4`):**
    - `Layer 1`: `surface-inset` (`#E5E9F0` — plano escavado para inputs, busca e berço do ícone ativo na sidebar `#sidebar-active-tracker`).
    - `Layer 2`: `surface-flat` (`#E9EEF5` — placa intermediária sem bordas duras).
    - `Layer 3`: `surface-raised` (`.ui-card-soft` / `.bento-card-soft` — plano esculpido a 135°).
    - `Layer 4`: `surface-contrast` (`#1E293B` / `.terrixa-notched` — âncora de inversão tonal monocromática).
  - **10% Accent Focal Único (`--accent-point`):** Tom único mineral (**Cerulean Sapphire** `#0284C7` ou **Ocean Sapphire** `#1E6091`) para CTAs principais e indicadores ativos.
- **Física Tactile / Soft UI (Sombras Difusas Duplas em 135°):**
  - Combine uma sombra suave inferior/direita com uma iluminação de topo superior/esquerda sobre a mesma cor do fundo.
  - Substitua bordas duras por transições suaves de relevo.

### Passo 2: Mapeamento da Hierarquia Atômica (5 Camadas)
Classifique a interface em 5 camadas funcionais:
1. **Átomos:** Botões táteis (`.ui-btn-tactile`), Inputs escavados (`surface-inset`), Badges tonais (`.badge-soft`), Ícones monocromáticos, Typography Labels.
2. **Moléculas:** Barra de busca escavada (`surface-inset-pill`), Linhas de atividade tátil (`.activity-row`), Módulos de estatística tátil.
3. **Organismos:** Tactile Companion Sidebar com `#sidebar-active-tracker`, Headers integrados, Cards BENTO esculpidos (`<SoftCard />`), Modais com sombra difusa.
4. **Templates:** Grids assimétricos BENTO (12 colunas, `col-span-8` + `col-span-4`, respiro amplo e `gap >= 24px`).
5. **Pages / Views:** Páginas completas conectando o Template Bento aos dados de estado e telemetria.

### Passo 3: Organização Modular do Diretório de Código
```text
src/
├── assets/           # Mídia estática, SVGs, fontes
├── components/       # Componentes desacoplados por camada atômica (<= 300 linhas/arquivo)
│   ├── ui/           # Átomos e Moléculas reutilizáveis (SoftCard.tsx, Button, Badge, Input)
│   ├── bento/        # Cards BENTO e organismos visuais
│   └── layout/       # Header, Tactile Companion Sidebar, Container
├── config/           # Configurações de tema, constantes e tokens
│   ├── tokens.ts     # Mapeamento JS/TS dos Design Tokens v4.5-soft (Zero Cobalt)
│   └── DESIGN.md     # Especificação YAML pública do sistema de design (v4.5-soft)
├── hooks/            # Custom Hooks React para lógica de UI (useTheme, useTactileFeedback)
├── styles/           # Estilos globais e variáveis CSS
│   ├── globals.css   # Variáveis :root, resets e física tátil (Soft UI 135°)
│   └── theme.css     # Paletas tonais (Nexus Slate, Moss, Soft Sapphire, Obsidian Dark)
├── types/            # Interfaces e types TypeScript estritos
│   └── index.ts      # Contratos de Props de UI, TonalLayer e ComponentFSMState
└── views/            # Páginas e telas da aplicação
```

### Passo 4: Implementação com Tipagem e Acessibilidade (WCAG 2.1 AA)
- Exija **TypeScript estrito** (`strict: true`) sem `any`.
- Garanta atributos **ARIA** (`aria-label`, `role="status"`, `role="alert"`, `aria-busy`, `aria-live`).
- Assegure contraste tipográfico mínimo de $4.5:1$ para texto normal e $7:1$ para títulos.
- Garanta suporte total a navegação por teclado (`:focus-visible` com anel tracejado tátil sutil `2px dashed var(--accent-point)`).

---

## 4. TEMPLATE DE CÓDIGO PADRÃO (SOFT UI / MINIMALIST IMPACT)

### A. Variáveis Globais CSS (`src/styles/globals.css`)
```css
:root {
  /* Paleta Tonal Monocromática (Soft Light v4.5 — Cerulean Sapphire, Zero Cobalto) */
  --surface-canvas: #F1F4F8;
  --surface-raised: #F8FAFC;
  --surface-inset: #E2E8F0;
  --surface-contrast: #1E293B;
  
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --text-muted: #94A3B8;
  
  --accent-point: #0284C7;
  --accent-sapphire: #1E6091;
  --accent-soft-bg: #E0F2FE;

  /* Física Tactile / Neumorfismo Suave 135° */
  --soft-shadow-main: 8px 8px 24px rgba(166, 180, 200, 0.40);
  --soft-shadow-light: -8px -8px 24px rgba(255, 255, 255, 0.95);
  --soft-shadow-inset: inset 3px 3px 8px rgba(166, 180, 200, 0.35), inset -3px -3px 8px rgba(255, 255, 255, 0.80);
  
  --radius-lg: 24px;
  --radius-md: 14px;
  --radius-sm: 8px;
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
}

/* Card Bento Tátil sem Bordas Duras */
.ui-card-soft {
  background-color: var(--surface-canvas);
  border-radius: var(--radius-lg);
  box-shadow: var(--soft-shadow-main), var(--soft-shadow-light);
  padding: 1.75rem;
  transition: transform 0.25s var(--ease-spring), box-shadow 0.25s var(--ease-spring);
  position: relative;
}

.ui-card-soft:hover {
  transform: translateY(-2px);
  box-shadow: 12px 12px 32px rgba(166, 180, 200, 0.50), -12px -12px 32px rgba(255, 255, 255, 1);
}

/* Botão Tátil Pressionável */
.ui-btn-tactile {
  background-color: var(--surface-canvas);
  color: var(--text-primary);
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-md);
  border: none;
  box-shadow: 4px 4px 12px rgba(166, 180, 200, 0.35), -4px -4px 12px rgba(255, 255, 255, 0.90);
  cursor: pointer;
  transition: all 0.15s var(--ease-spring);
}

.ui-btn-tactile:hover {
  color: var(--accent-point);
  transform: translateY(-1px);
}

.ui-btn-tactile:active {
  transform: translateY(1px);
  box-shadow: var(--soft-shadow-inset);
}
```

### B. Componente Reutilizável com FSM em React + TS (`src/components/ui/SoftCard.tsx`)
```tsx
import React from 'react';

export interface SoftCardProps {
  title: string;
  badgeText?: string;
  colSpan?: 3 | 4 | 6 | 8 | 12;
  isLoading?: boolean;
  error?: string | null;
  children: React.ReactNode;
  className?: string;
}

export const SoftCard: React.FC<SoftCardProps> = ({
  title,
  badgeText,
  colSpan = 4,
  isLoading = false,
  error = null,
  children,
  className = '',
}) => {
  return (
    <article
      className={`ui-card-soft col-span-${colSpan} ${className}`}
      tabIndex={0}
      aria-label={title}
      aria-busy={isLoading}
    >
      <div className="flex justify-between items-center mb-5">
        <h3 className="text-xl font-semibold text-slate-800 tracking-tight">{title}</h3>
        {badgeText && <span className="badge-soft">{badgeText}</span>}
      </div>

      {isLoading ? (
        <div role="status" aria-busy="true" aria-live="polite" className="surface-inset p-4 rounded-xl">
          Sincronizando camada tonal...
        </div>
      ) : error ? (
        <div role="alert" aria-live="assertive" className="surface-inset p-4 rounded-xl text-red-600 font-medium">
          {error}
        </div>
      ) : (
        <div className="card-body">{children}</div>
      )}
    </article>
  );
};
```

---

## 5. SAÍDAS E ENTREGÁVEIS (CHECKLIST DE ACEITE SELF-REFINE)

Toda entrega desta skill produz a árvore `src/` modularizada, o `DESIGN.md` (`v4.5-soft`) e valida:
- [ ] Foram eliminados glassmorphism (`backdrop-filter: blur`), luzes neon, azul cobalto (`#0044FF`, `#0057FF`, `#1D4ED8`) e bordas duras de 1px?
- [ ] A paleta de cores segue a regra 60-30-10 com Cerulean/Ocean Sapphire (`#0284C7` / `#1E6091`) e elevação tonal a 135°?
- [ ] O arquivo `DESIGN.md` (`v4.5-soft`) foi incluído com os tokens de Neumorfismo Suave?
- [ ] O código é 100% modularizado em Design Atômico (5 camadas) com arquivos $\le 300$ linhas?
- [ ] O componente é acessível (WCAG 2.1 AA), tipado em TypeScript estrito e pronto para o `frontend-testing-auditor`?
