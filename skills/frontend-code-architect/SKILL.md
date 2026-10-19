---
name: frontend-code-architect
description: >-
  Scaffolding estrutural de diretórios src/ em 5 camadas de Design Atômico e templates base (globals.css e <SoftCard />) sob DESIGN.md v4.5-soft. Use apenas para criar a estrutura de pastas ou componentes novos do zero. Não use para diagnosticar UI existente (use analise-design-tatil-frontend) nem para refatorar telas (use refatoracao-design-tatil-frontend).
version: "4.1.0"
license: MIT
compatibility: "React 18+, TypeScript 5+, Tailwind CSS v3+, CSS Variables, Next.js 14+"
metadata:
  author: "FrontCraftMaster & Melki"
  version: "4.1.0"
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
    role: "Auditoria determinística FSM + Axe-Core + audit_tactile_ui.py dos componentes gerados"
---

# 🎨 Frontend Code Architect Skill (`frontend-code-architect` v4.1.0 — Minimalist Impact & Soft Tactile Architecture)

## 1. OBJETIVO E DIRETRIZES DE ATIVAÇÃO

Esta Skill fornece procedimentos padronizados para estruturar, organizar e implementar aplicações frontend modernas de nível industrial e estética minimalista tátil (*Minimalist Impact*, *Soft UI*, *Tonal Layering 135°*).

### 🚫 PROIBIÇÕES ABSOLUTAS DE DESIGN (Anti-Patterns):
- ❌ **Não utilizar Glassmorphism / Vidro Fosco:** Proibido o uso de caixas semi-transparentes reluzentes com `backdrop-filter: blur()`.
- ❌ **Não utilizar Neons, Múltiplos Acentos ou Azul Cobalto:** Proibida a poluição visual com bordas brilhantes ou azul cobalto elétrico (`#0044FF`, `#0057FF`, `#1D4ED8`, `#233DFF`). Utilize azuis minerais serenos (**Cerulean Sapphire** `#0284C7`, **Ocean Sapphire** `#1E6091` ou **Mineral Ice** `#38BDF8`).
- ❌ **Não utilizar Bordas Duras de 1px, Micro-Texto (`10px`/`11px`) ou Emojis em Controles:** Divisões de cards e painéis devem ser feitas por variação sutil de tom de superfície ou elevação neumórfica suave a 135°. Proibido deixar `<SoftCard />` órfão sem importação nas views reais (`App.tsx`, `Sidebar.tsx`, `*Workspace.tsx`).

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
  - **60% Fundo Base Contínuo (`Layer 0`):** `--surface-canvas` (`#F1F4F8` Off-white macio no Light; `#12151B` / `#0B0E14` Slate Matte escuro no Dark).
  - **30% Camadas e Elevação (`Layers 1–4`):**
    - `Layer 1`: `--surface-inset` (`#E5E9F0`) e `--surface-sunken` (`#DCE3EC` — plano escavado para inputs, busca, Surface Wells e berço deslizante `#sidebar-active-tracker`).
    - `Layer 2`: `--surface-flat` (`#E9EEF5` — placa intermediária sem bordas duras).
    - `Layer 3`: `--surface-raised` (`#F1F4F8` / `#F8FAFC` / `.ui-card-soft` — plano esculpido a 135°).
    - `Layer 4`: `--surface-contrast` (`#1E293B` / `.terrixa-notched` — âncora de inversão tonal monocromática).
  - **10% Accent Focal Único (`--accent-point`):** Tom único mineral (**Cerulean Sapphire** `#0284C7`, **Moss** `#174930`, **Ocean Sapphire** `#1E6091` ou **Mineral Ice** `#38BDF8`).
- **Física Tactile / Soft UI (Sombras Difusas Duplas em 135°):**
  - Combine uma sombra suave inferior/direita com uma iluminação de topo superior/esquerda sobre a mesma cor do fundo (`--shadow-card`, `--shadow-ambient`, `--shadow-float`, `--shadow-inset`).
  - Substitua bordas duras por transições suaves de relevo.

### Passo 2: Mapeamento da Hierarquia Atômica (5 Camadas)
Classifique a interface em 5 camadas funcionais:
1. **Átomos:** Botões táteis (`.ui-btn-tactile`), Inputs escavados (`surface-inset`), Badges tonais (`.badge-soft`), Ícones vetoriais Lucide (`stroke-width: 1.75`, zero emojis), Typography Labels.
2. **Moléculas:** Barra de busca escavada (`.surface-inset-pill`), Linhas de atividade tátil (`.activity-row`), Módulos de estatística tátil (`tabular-nums`).
3. **Organismos:** Tactile Companion Sidebar com `#sidebar-active-tracker` deslizante, Headers integrados, Cards BENTO esculpidos (`<SoftCard />`).
4. **Templates:** Grids assimétricos BENTO (12 colunas, `col-span-8` + `col-span-4`, respiro amplo e `gap >= 24px`).
5. **Pages / Views:** Páginas completas importando efetivamente `<SoftCard />` e `.ui-btn-tactile` (proibido criar `<SoftCard />` como componente órfão).

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
- Garanta suporte total a navegação por teclado (`:focus-visible` com `outline: 2px solid var(--accent-point); outline-offset: 3px;`).

---

## 4. TEMPLATE DE CÓDIGO PADRÃO (SOFT UI / MINIMALIST IMPACT)

### A. Variáveis Globais CSS (`src/styles/globals.css`)
```css
:root {
  --surface-sunken: #DCE3EC;
  --surface-canvas: #F1F4F8;
  --surface-inset: #E5E9F0;
  --surface-flat: #E9EEF5;
  --surface-raised: #F1F4F8;
  --surface-contrast: #1E293B;

  --text-primary: #0F172A;
  --text-secondary: #334155;
  --text-muted: #64748B;

  --accent-point: #0284C7;
  --accent-secondary: #1E6091;
  --accent-soft-bg: #E0F2FE;

  --shadow-card: 10px 10px 24px rgba(148, 163, 184, 0.32), -8px -8px 20px rgba(255, 255, 255, 0.92);
  --shadow-ambient: 0 12px 28px rgba(15, 23, 42, 0.06), 0 4px 10px rgba(15, 23, 42, 0.04);
  --shadow-float: 14px 14px 32px rgba(148, 163, 184, 0.42), -10px -10px 26px rgba(255, 255, 255, 0.98);
  --shadow-inset: inset 3px 3px 7px rgba(148, 163, 184, 0.35), inset -3px -3px 7px rgba(255, 255, 255, 0.85);

  --radius-lg: 24px;
  --radius-md: 14px;
  --radius-sm: 8px;
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
}

.ui-card-soft {
  background-color: var(--surface-raised);
  color: var(--text-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: 1.75rem;
  transition: transform 0.25s var(--ease-spring), box-shadow 0.25s var(--ease-spring);
  position: relative;
}

.ui-card-soft:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-float);
}

.ui-btn-tactile {
  background-color: var(--surface-raised);
  color: var(--text-primary);
  font-weight: 600;
  min-height: 44px;
  min-width: 44px;
  padding: 0.65rem 1.25rem;
  border-radius: var(--radius-md);
  border: none;
  box-shadow: var(--shadow-card);
  flex-shrink: 0;
  white-space: nowrap;
  cursor: pointer;
  transition: transform 0.15s var(--ease-spring), box-shadow 0.15s var(--ease-spring), color 0.15s ease;
}

.ui-btn-tactile:hover {
  color: var(--accent-point);
  transform: translateY(-2px);
}

.ui-btn-tactile:active,
.ui-btn-tactile[aria-pressed="true"] {
  background-color: var(--surface-inset);
  transform: translateY(1px);
  box-shadow: var(--shadow-inset);
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### B. Componente Reutilizável com FSM em React + TS (`src/components/ui/SoftCard.tsx`)
```tsx
import React, { useState } from 'react';

export type UIState = 'idle' | 'loading' | 'error' | 'pressed';
export type SoftCardVariant = 'raised' | 'well' | 'contrast';

export interface SoftCardProps {
  title: string;
  badgeText?: string;
  colSpan?: 3 | 4 | 6 | 8 | 12;
  variant?: SoftCardVariant;
  isLoading?: boolean;
  error?: string | null;
  children: React.ReactNode;
  className?: string;
}

const COL_SPAN_MAP: Record<NonNullable<SoftCardProps['colSpan']>, string> = {
  3: 'col-span-3',
  4: 'col-span-4',
  6: 'col-span-6',
  8: 'col-span-8',
  12: 'col-span-12',
};

const VARIANT_CLASS_MAP: Record<SoftCardVariant, string> = {
  raised: 'ui-card-soft',
  well: 'surface-inset p-6 rounded-2xl',
  contrast: 'ui-card-soft terrixa-notched',
};

export const SoftCard: React.FC<SoftCardProps> = ({
  title,
  badgeText,
  colSpan = 4,
  variant = 'raised',
  isLoading = false,
  error = null,
  children,
  className = '',
}) => {
  const [isPressed, setIsPressed] = useState(false);
  const currentState: UIState = error ? 'error' : isLoading ? 'loading' : isPressed ? 'pressed' : 'idle';
  const spanClass = COL_SPAN_MAP[colSpan] ?? 'col-span-4';
  const surfaceClass = VARIANT_CLASS_MAP[variant] ?? 'ui-card-soft';

  return (
    <article
      className={`${surfaceClass} ${spanClass} ${className}`.trim()}
      data-state={currentState}
      tabIndex={0}
      aria-label={title}
      aria-busy={isLoading}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseLeave={() => setIsPressed(false)}
    >
      <div className="flex justify-between items-center mb-5">
        <h3 style={{ color: 'var(--text-primary)' }} className="text-lg font-semibold tracking-tight">
          {title}
        </h3>
        {badgeText && <span className="badge-soft">{badgeText}</span>}
      </div>

      {isLoading ? (
        <div role="status" aria-busy="true" aria-live="polite" className="surface-inset p-4 rounded-xl">
          Sincronizando camada tonal...
        </div>
      ) : error ? (
        <div role="alert" aria-live="assertive" className="surface-inset p-4 rounded-xl font-medium">
          {error}
        </div>
      ) : (
        <div className="card-body">{children}</div>
      )}
    </article>
  );
};
```

### C. Arquétipos de Layout por Domínio (Anti-Monotonia Visual)
Combine os 3 arquétipos conforme o domínio da tela em vez de repetir o mesmo grid em todas as páginas:
1. **`Tactile Raised Card` (`variant="raised"`)**: Para KPIs, métricas operacionais e Bento Dashboards em relevo 135° (`--surface-raised: #F8FAFC`).
2. **`Surface Well` (`variant="well"`)**: Para leitura longa, prontuários clínicos, logs e tabelas densas acomodadas em cavidade `--surface-inset`.
3. **`Split-Pane Studio` (`variant="contrast"` + Sidebar `#sidebar-active-tracker`)**: Para IDEs, cockpits agênticos e editores multi-painel.

---

## 🤖 ATIVAÇÃO DE SUBAGENTES E ORQUESTRAÇÃO (`Topologia 3+1`)
- **Persona Coordenadora:** `FrontCraftMaster`
- **Subagentes Vinculados:** `ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction` e `ui-deterministic-observer`.
- **Disparo Automático:** Utilize `invoke_subagent` ou `franklin_execute_dag(plan_path_or_json="ui", target_dir="<project_root_path>")` para validar o scaffolding gerado.

---

## 5. SAÍDAS E ENTREGÁVEIS (CHECKLIST DE ACEITE SELF-REFINE)

Toda entrega desta skill produz a árvore `src/` modularizada, o `DESIGN.md` (`v4.5-soft`) e valida:
- [ ] Foram eliminados glassmorphism (`backdrop-filter: blur`), luzes neon, azul cobalto (`#0044FF`, `#0057FF`, `#1D4ED8`) e bordas duras de 1px?
- [ ] A paleta de cores segue a regra 60-30-10 com Cerulean/Ocean Sapphire (`#0284C7` / `#1E6091`) e elevação tonal a 135°?
- [ ] O arquivo `DESIGN.md` (`v4.5-soft`) foi incluído com os tokens de Neumorfismo Suave?
- [ ] O código é 100% modularizado em Design Atômico (5 camadas) com arquivos $\le 300$ linhas e mapeamento estático `COL_SPAN_MAP`?
- [ ] O componente é acessível (WCAG 2.1 AA), tipado em TypeScript estrito e pronto para o `frontend-testing-auditor`?
