---
name: frontend-code-architect
description: >-
  Arquitetura, scaffolding e implementação frontend (src/ em 5 camadas de Design Atômico, globals.css, tokens e componentes) adaptando tema, espaçamento, contraste, tipografia e camadas ao propósito do projeto. Não use para auditoria somente-leitura (use frontend-testing-auditor).
version: "5.0.0"
license: MIT
compatibility: "React 18+, TypeScript 5+, Tailwind CSS v3/v4, CSS Variables, Next.js 14+"
metadata:
  author: "FrontCraftMaster & Melki"
  version: "5.0.0"
  category: "Frontend Engineering, Design Atômico & Arquitetura Visual por Propósito"
  updated_at: "2026-10-19"
  tags:
    - "frontend-architect"
    - "atomic-design"
    - "estilo-por-proposito"
    - "ex-umbris-ad-lucem"
    - "aether-2027"
updated_at: 2026-10-19
author: FrontCraftMaster & Melki
category: Frontend Engineering, Design Atômico & Arquitetura Visual por Propósito
authorized_sub_skills:
  - name: minimal-impact-ui
    role: "Atlas Ex Umbris + WinUI 3 Gallery (6 arquétipos de página, 28 efeitos e boilerplate HTML/CSS/JS)"
  - name: design-md
    role: "Síntese e atualização do contrato DESIGN.md guiado pelo propósito do projeto"
  - name: frontend-testing-auditor
    role: "Auditoria determinística de contraste, tipografia, camadas, FSM e Axe-Core via scripts/audit_tactile_ui.py"
---

# 🎨 Frontend Code Architect (`frontend-code-architect` v5.0.0 — Design Atômico & Estilo Guiado por Propósito)

## 1. OBJETIVO E DIRETRIZES DE ATIVAÇÃO

Esta Skill fornece procedimentos padronizados para estruturar, implementar e evoluir aplicações frontend modernas em **5 camadas de Design Atômico**, selecionando **tema, atmosfera, arquétipo de página, espaçamento, contraste, tipografia e camadas** de acordo com o **propósito do projeto** (consulte [`../_template/references/preferencias_estilo_e_temas.md`](../_template/references/preferencias_estilo_e_temas.md), [`../minimal-impact-ui/SKILL.md`](../minimal-impact-ui/SKILL.md) e o modelo [`../minimal-impact-ui/references/atlas_ex_umbris_winui.html`](../minimal-impact-ui/references/atlas_ex_umbris_winui.html)).

### 🚫 ANTI-PADRÕES A EVITAR:
- ❌ **Paleta Fixa Repetitiva ou Letras Vermelhas Embaçadas sobre Cinza/Escuro:** Proibido `color: #e13535` puro ou serifa fina embaçada sobre `#57545d`, `#49464f` ou `#070709`. Use `.highlight-surgical` (Semibold + sublinhado `2px` em `--punctual-accent`) em títulos e `.accent-text` (`#FFFFFF` no cinza/escuro ou `#991B1B` no claro + fundo `--punctual-soft` + `border-left: 2.5px solid var(--punctual-accent)`) em badges.
- ❌ **Texto Branco Lavado em Menus Claros/`#8e8999` ou em Botões Azul/Verde:** Em menus `#8e8999`, os rótulos devem usar tinta escura (`--nav-ink: #16151A`); em botões preenchidos Azul (`#35acd8`) ou Verde (`#10B981`), use `--punctual-btn-ink` escuro (`#091318` / `#062016`).
- ❌ **Poluição de CTAs, Números Desalinhados ou Componentes Órfãos:** Respeite o isolamento 98/2 (1 CTA primário sólido vs. `.btn-ghost` secundários), `font-variant-numeric: tabular-nums` em dados numéricos e consumo real de todo componente criado em `src/components/ui/`.

### ✅ Gatilhos Positivos (Quando Usar):
- Criação ou refatoração da estrutura `src/` em **Design Atômico** (Átomos, Moléculas, Organismos, Templates Bento e Pages/Views) e implementação dos **6 Arquétipos de Página** (*Split-Screen Workbench*, *Timeline*, *Kanban*, *Canvas de Nós*, *Wizard Foco Anti-TDAH*, *Catálogo WinUI Gallery*) e **28 Efeitos WinUI 3 + Ex Umbris**.
- Implementação de sistemas de **Design Tokens (`DESIGN.md` + `globals.css`)** adaptados ao propósito do projeto (*Ad Lucem*, *Cinza Monolítico `#57545d` + Menus `#8e8999`*, *Preto Terminal IBM `Ex Umbris` + `IBM Plex`*, ou *AETHER 2027* `oklch()`).

### ❌ Quando NÃO Usar (Limites e Exceções):
- Scripts puramente backend/CLI sem interface visual, diagnóstico read-only (`auditoria-projetos-sistema`) ou execução isolada de testes (`frontend-testing-auditor`).

---

## 📥 Entradas e Pré-requisitos
- `project_root_path`: Caminho raiz da aplicação frontend.
- `project_purpose`: Objetivo do sistema (`conversao_saas`, `editorial_leitura`, `fintech_confianca`, `ia_nativa_aether`, `medtech_clinico`, `devtools_terminal_ibm`).

---

## 2. FLUXO OPERACIONAL PASSO A PASSO

### Passo 1: Enquadramento do Propósito, Arquétipo de Página e Atmosfera
1. Identifique o objetivo central e o **Arquétipo Espacial** (além de formulários e gráficos comuns):
   - **Conversão & SaaS / Editorial**: *Ad Lucem* (`--bg-canvas: #F3F3F5`, `--bg-surface: #FFFFFF`, `--bg-elevated: #E6E6EA`, bloco de contraste `--bg-contrast-card: #18181C`).
   - **Estúdio Analítico / Produtividade Anti-TDAH / FinTech**: *Cinza sobre Cinza Monolítico* (`--bg-canvas: #57545d`, `--bg-surface: #49464f`, `--bg-elevated: #635f6a`, contraste `#232127`, menus em pílula `--nav-bg: #8e8999` com tinta escura `--nav-ink: #16151A`).
   - **DevTools / Observabilidade / Terminal Técnico**: *Preto Terminal IBM (`Ex Umbris`)* (`--bg-canvas: #070709`, `--bg-surface: #101014`, `--bg-elevated: #18181E`) acoplado a **`IBM Plex Sans` + `IBM Plex Mono`**.
2. Defina o **Acento Pontual de Intenção** (`--punctual-accent`: `#e13535`, `#35acd8`, `#10B981` ou `#D97706`) ocupando 2% da tela.

### Passo 2: Mapeamento da Hierarquia Atômica (5 Camadas) e Árvore `src/`
```text
src/
├── assets/           # Mídia estática, SVGs vetoriais (Lucide stroke 1.75), fontes
├── components/       # Componentes desacoplados por camada atômica (<= 300 linhas/arquivo)
│   ├── ui/           # Átomos e Moléculas (SurfaceCard.tsx, ActionButton.tsx, Badge, Input)
│   ├── bento/        # Organismos Bento Grid (12 colunas, spans assimétricos, gap 16px..24px)
│   └── layout/       # Navegação (Pill Nav #8e8999 / Sidebar com tracker ativo), Header, Shell
├── config/           # Configurações de tema, constantes e tokens
│   ├── tokens.ts     # Mapeamento JS/TS dos tokens semânticos por propósito
│   └── DESIGN.md     # Contrato arquitetural do sistema de design
├── hooks/            # Custom Hooks React (useThemeAtmosphere, useFSMState)
├── styles/           # Estilos globais e variáveis CSS
│   ├── globals.css   # Variáveis :root, famílias de tema, sombras 3 camadas + 1px Rim Light
│   └── theme.css     # Presets adaptáveis ao domínio do projeto
├── types/            # Interfaces e types TypeScript estritos (zero any)
│   └── index.ts      # Contratos de UIState ('idle' | 'loading' | 'error' | 'pressed')
└── views/            # Páginas e telas consumindo efetivamente os componentes de ui/ e bento/
```

---

## 3. TEMPLATES BASE ADAPTÁVEIS POR PROPÓSITO

### A. Variáveis Globais e Física de Camadas (`src/styles/globals.css`)
```css
:root,
[data-theme="ad-lucem"] {
  --bg-canvas: #F3F3F5;
  --bg-surface: #FFFFFF;
  --bg-elevated: #E6E6EA;
  --bg-contrast-card: #18181C;
  --contrast-card-ink: #FAFAFA;

  --ink-primary: #111113;
  --ink-secondary: #4A4A52;
  --ink-muted: #71717A;
  --ink-subtle: #A1A1AA;

  --nav-bg: rgba(228, 228, 233, 0.88);
  --nav-ink: #18181B;
  --nav-active-bg: #18181C;
  --nav-active-ink: #FFFFFF;

  --punctual-accent: #35acd8;
  --border-hairline: rgba(24, 24, 27, 0.08);
  --rim-light: rgba(255, 255, 255, 0.9);
  --shadow-sculpted:
    0 1px 2px rgba(9, 9, 11, 0.05),
    0 8px 24px -4px rgba(9, 9, 11, 0.06),
    0 20px 40px -12px rgba(9, 9, 11, 0.04),
    inset 0 1px 0 0 var(--rim-light);

  --font-sans: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  --font-display: 'Instrument Serif', Georgia, serif;
  --font-mono: 'IBM Plex Mono', 'JetBrains Mono', monospace;
  --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);
}

[data-theme="monolith-gray"] {
  --bg-canvas: #57545d;
  --bg-surface: #49464f;
  --bg-elevated: #635f6a;
  --bg-contrast-card: #232127;
  --contrast-card-ink: #F4F4F6;
  --ink-primary: #F4F3F6;
  --ink-secondary: #DFDCE5;
  --ink-muted: #BCB7C6;
  --ink-subtle: #9A94A6;
  --nav-bg: #8e8999;
  --nav-ink: #16151A;
  --nav-active-bg: #18181C;
  --nav-active-ink: #FFFFFF;
  --border-hairline: rgba(255, 255, 255, 0.12);
  --rim-light: rgba(255, 255, 255, 0.14);
}

[data-theme="ibm-terminal-dark"] {
  --bg-canvas: #070709;
  --bg-surface: #101014;
  --bg-elevated: #18181E;
  --bg-contrast-card: #F3F3F5;
  --contrast-card-ink: #09090B;
  --ink-primary: #F4F4F6;
  --ink-secondary: #A1A1AA;
  --ink-muted: #71717A;
  --ink-subtle: #52525B;
  --nav-bg: rgba(24, 24, 30, 0.9);
  --nav-ink: #E4E4E7;
  --nav-active-bg: #F4F4F6;
  --nav-active-ink: #09090B;
  --border-hairline: rgba(255, 255, 255, 0.08);
  --rim-light: rgba(255, 255, 255, 0.08);
  --font-sans: 'IBM Plex Sans', system-ui, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
}

.sculpted-card {
  background-color: var(--bg-surface);
  color: var(--ink-primary);
  border: 1px solid var(--border-hairline);
  border-radius: 20px;
  padding: 1.75rem;
  box-shadow: var(--shadow-sculpted);
  transition: transform 0.28s var(--ease-spring), box-shadow 0.28s var(--ease-spring);
}

.sculpted-card[data-variant="contrast"] {
  background-color: var(--bg-contrast-card);
  color: var(--contrast-card-ink);
}

.btn-primary-intent,
.btn-ghost {
  min-height: 44px;
  min-width: 44px;
  padding: 0.65rem 1.25rem;
  border-radius: 12px;
  font-weight: 600;
  flex-shrink: 0;
  white-space: nowrap;
  cursor: pointer;
  transition: transform 0.18s var(--ease-spring), background-color 0.18s ease;
}

.btn-primary-intent {
  background-color: var(--punctual-accent);
  color: #FFFFFF;
  border: none;
}

.btn-ghost {
  background-color: transparent;
  color: var(--ink-primary);
  border: 1px solid var(--border-hairline);
}

.tabular-metric {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### B. Componente de Superfície com Máquina de Estados FSM (`src/components/ui/SurfaceCard.tsx`)
```tsx
import React, { useState } from 'react';

export type UIState = 'idle' | 'loading' | 'error' | 'pressed';
export type CardVariant = 'surface' | 'elevated' | 'contrast';

export interface SurfaceCardProps {
  title: string;
  eyebrow?: string;
  colSpan?: 3 | 4 | 5 | 6 | 7 | 8 | 12;
  variant?: CardVariant;
  isLoading?: boolean;
  error?: string | null;
  children: React.ReactNode;
  className?: string;
}

const COL_SPAN_MAP: Record<NonNullable<SurfaceCardProps['colSpan']>, string> = {
  3: 'col-span-3',
  4: 'col-span-4',
  5: 'col-span-5',
  6: 'col-span-6',
  7: 'col-span-7',
  8: 'col-span-8',
  12: 'col-span-12',
};

export const SurfaceCard: React.FC<SurfaceCardProps> = ({
  title,
  eyebrow,
  colSpan = 4,
  variant = 'surface',
  isLoading = false,
  error = null,
  children,
  className = '',
}) => {
  const [isPressed, setIsPressed] = useState(false);
  const currentState: UIState = error ? 'error' : isLoading ? 'loading' : isPressed ? 'pressed' : 'idle';
  const spanClass = COL_SPAN_MAP[colSpan] ?? 'col-span-4';

  return (
    <article
      className={`sculpted-card ${spanClass} ${className}`.trim()}
      data-variant={variant}
      data-state={currentState}
      tabIndex={0}
      aria-label={title}
      aria-busy={isLoading}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseLeave={() => setIsPressed(false)}
    >
      <header className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold tracking-tight">{title}</h3>
        {eyebrow && <span className="text-xs font-mono uppercase tracking-wider">{eyebrow}</span>}
      </header>
      {isLoading ? (
        <div role="status" aria-busy="true" aria-live="polite" className="p-4 rounded-xl">Carregando superfície...</div>
      ) : error ? (
        <div role="alert" aria-live="assertive" className="p-4 rounded-xl font-medium">{error}</div>
      ) : (
        <div className="card-body">{children}</div>
      )}
    </article>
  );
};
```

## 🤖 ATIVAÇÃO DE SUBAGENTES E ORQUESTRAÇÃO (`Topologia 3+1`)
- **Persona Coordenadora:** `FrontCraftMaster`
- **Subagentes Vinculados:** `ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction` e `ui-deterministic-observer`.
- **Disparo Automático:** Utilize `invoke_subagent` ou `franklin_execute_dag(plan_path_or_json="ui", target_dir="<project_root_path>")` para validar a implementação.

## 4. SAÍDAS, ENTREGÁVEIS E CHECKLIST DE ACEITE SELF-REFINE
- [ ] O tema e o acento cromático foram escolhidos com base no **propósito do projeto** (sem paleta fixa engessada)?
- [ ] A hierarquia respeita 4 níveis de tinta, contraste WCAG AA/AAA, tinta escura em menus claros/`#8e8999`, zero texto vermelho ou serifa fina no cinza/escuro (`.highlight-surgical`) e isolamento de 1 CTA primário sólido vs. `.btn-ghost`?
- [ ] Métricas e tabelas usam `tabular-nums` (e `IBM Plex` caso o tema seja Preto Terminal `Ex Umbris`)?
- [ ] O espaçamento preserva $\ge 25\%$ de respiro, raios concêntricos e sombra esculpida em 3 camadas + `1px` Rim Light?
- [ ] O código está particionado em 5 camadas atômicas ($\le 300$ linhas/arquivo) com estados FSM acessíveis (`idle | loading | error | pressed`)?
