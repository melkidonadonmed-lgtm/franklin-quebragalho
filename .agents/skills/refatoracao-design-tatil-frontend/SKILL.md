---
name: refatoracao-design-tatil-frontend
description: >-
  Fase 3 (Code Execution & 3-Wave Subagent Orchestrator) da esteira de Frontend Tátil & Minimalist Impact Melki (DESIGN.md v4.5-soft). Executa na prática a refatoração de código frontend (React/Next.js, Tailwind, HTML5/CSS, Vue), extraindo código monolítico para as 5 camadas de Design Atômico (frontend-code-architect v4.0), aplicando iluminação direcional 135° (.ui-card-soft, surface-inset, zero cobalto/glassmorphism/neon) e orquestrando em 3 ondas os 4 subagentes de UI + frontend-testing-auditor (v2.5.0).
license: MIT
metadata:
  version: "2.1.0"
  author: "FrontCraftMaster & Melki"
  category: "Implementação, Minimalist Impact e Refatoração Frontend"
  updated_at: "2026-10-18"
  tags:
    - "frontend"
    - "minimalist-impact"
    - "soft-ui"
    - "refatoracao-codigo"
    - "anti-cobalto"
    - "subagentes-ui-3+1"
version: 2.1.0
updated_at: 2026-10-18
author: FrontCraftMaster & Melki
category: Implementação, Minimalist Impact e Refatoração Frontend
authorized_sub_skills:
  - name: design-md
    role: "Garantia de que o DESIGN.md v4.5-soft reflita fielmente os tokens e componentes implementados"
  - name: frontend-code-architect
    role: "Padronização modular src/ em 5 camadas de Design Atômico (v4.0.0)"
  - name: frontend-testing-auditor
    role: "Auditoria determinística FSM + Axe-Core (v2.5.0) pós-refatoração"
---

# Fase 3: Refatoração Prática de Código e Orquestração em 3 Ondas (`refatoracao-design-tatil-frontend` v2.1.0 — Minimalist Impact & Soft Tactile) ⚡

Motor de **Execução de Código e Modularização** (**Fase 3**) da esteira Frontend Melki. Consome o diagnóstico da Fase 1 (`analise-design-tatil-frontend`) e o `DESIGN.md v4.5-soft` da Fase 2 (`consultor-design-tatil-frontend`) para **modularizar arquivos soltos em 5 camadas de Design Atômico (`frontend-code-architect` v4.0)**, **aplicar a Arquitetura Tátil Suave 135° (Zero Cobalto / Zero Glassmorphism)** e **validar com o `frontend-testing-auditor` (`v2.5.0`)**.

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Refatorar na prática o código HTML, CSS, JSX/TSX ou Vue de uma aplicação para o padrão **Minimalist Impact & Soft Tactile (`v4.5-soft`)**.
- Desmembrar arquivos monolíticos da pasta raiz em pastas estruturadas (`components/ui/`, `components/bento/`, `components/layout/`, `config/`, `styles/`, `types/`).
- Substituir azul cobalto (`#0044FF`, `#0057FF`, `#1D4ED8`), glassmorphism (`backdrop-filter: blur`) ou bordas duras de `1px` por elevação tonal 135° (`.ui-card-soft`, `surface-inset`) com **Cerulean Sapphire** (`#0284C7`) ou **Ocean Sapphire** (`#1E6091`).

### Quando NÃO Usar
- Para apenas inspecionar e gerar relatório sem tocar no código (use `analise-design-tatil-frontend`).
- Para alterações puras de backend/banco de dados sem impacto em UI.

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `project_root_path` (obrigatório): Caminho absoluto da raiz do projeto frontend.
- `design_md_path` (opcional): Caminho do `DESIGN.md` (`v4.5-soft`) na raiz (se não existir, crie-o antes via `design-md`).
- `preset` (opcional, padrão `slate`): Preset ativo dentre os **4 Presets Soft UI** (`slate` `#0284C7`, `moss` `#174930`, `sapphire` `#1E6091`, `obsidian` `#38BDF8`) ou **22 temas minerais**.

---

## ⚙️ Execução em 3 Ondas (`Topologia 3+1` + `frontend-code-architect` v4.0 + `frontend-testing-auditor` v2.5)

### Passo 0: Saneamento da Pasta Raiz e Injeção de Tokens (`DESIGN.md v4.5-soft` $\rightarrow$ CSS)
1. **Design Atômico & Orçamento de Linhas**: Extraia cada responsabilidade para `src/{components/ui,components/bento,components/layout,config,styles,types}` respeitando o limite de `<= 300` linhas por arquivo.
2. **Tokens Soft UI 135° (`:root` / `globals.css`)**:
   ```css
   :root {
     --surface-canvas: #F1F4F8;
     --surface-flat: #E9EEF5;
     --surface-raised: #F1F4F8;
     --surface-inset: #E5E9F0;
     --surface-contrast: #1E293B;
     --text-primary: #1E293B;
     --text-secondary: #64748B;
     --accent-point: #0284C7;      /* Cerulean Sapphire — Zero Cobalto */
     --accent-sapphire: #1E6091;   /* Ocean Sapphire */
     --accent-emerald: #059669;
     --soft-shadow-main: 8px 8px 20px rgba(166, 180, 200, 0.42);
     --soft-shadow-light: -8px -8px 20px rgba(255, 255, 255, 0.95);
     --soft-shadow-inset: inset 4px 4px 10px rgba(166, 180, 200, 0.45),
                          inset -4px -4px 10px rgba(255, 255, 255, 0.85);
     --radius-lg: 24px;
     --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
   }
   ```

### Passo 1: Onda 1 — Casca Estrutural, Bento Grid & Sidebar Tátil (`ui-shell-navigator`)
Acione `invoke_subagent(TypeName="ui-shell-navigator", ...)` na camada `components/layout/` e `components/bento/`:
- **Matriz Bento de 12 Colunas**: `grid-cols-12 gap-7` (`col-span-8` + `col-span-4`), reservas anti-CLS (`CLS < 0.1`) e zero bordas duras de `1px`.
- **Tactile Companion Sidebar (`#sidebar-active-tracker`)**: Sidebar expandida `272px` (colapsável para `92px` modo ícones) com berço escavado `surface-inset` e barra vertical de `4px` (`var(--accent-point)`) acompanhando o ícone ativo via `IntersectionObserver`, mais atalho `Ctrl+K`.
- **Inversão Tonal Terrixa (`.terrixa-notched`)**: Destaque de cards âncora via `surface-contrast` (`#1E293B`) e recorte chanfrado `28px` em vez de neon.

### Passo 2: Onda 2 (Paralela) — 8 Kits Soft UI (`ui-controls-data`) + Física Spring (`ui-motion-interaction`)
1. **`ui-controls-data` (`components/ui/`)**:
   - Implementar `<SoftCard />`, `.ui-btn-tactile`, `.btn-tactile-primary`, `.badge-soft`, `.swatch-disc`, `.tactile-thumb`, `.tactile-range`, `.surface-inset-pill` e `.activity-row`.
   - Alvos $\ge 44\text{px}$, anti-squish (`flex-shrink: 0; white-space: nowrap;`), Regra 1+2 e estados FSM (`Idle`, `Loading` com `role="status" aria-busy="true"`, `Error` com `role="alert" aria-live="assertive"`).
2. **`ui-motion-interaction` (`lib/utils` & `styles/`)**:
   - Elevação no hover (`translateY(-2px)`) e compressão física no clique (`:active` / `.is-pressed` convertendo para `surface-inset` com `translateY(1px)`), transições `--ease-spring: cubic-bezier(0.16, 1, 0.3, 1)` e proteção `@media (prefers-reduced-motion: reduce)`.

### Passo 3: Onda 3 (Gatekeeper) — `ui-deterministic-observer` + `frontend-testing-auditor` (`v2.5.0`)
1. **Auditoria de Código e DOM**:
   - Validar os 9 pontos `[AUDIT-01: SHELL-CLS]` a `[AUDIT-09: LIGHT-SHADOW]` e a suíte do `frontend-testing-auditor` (`AUDIT-A11Y-01/02`, `AUDIT-VIS-01` sem `blur()` e sem cobalto, `AUDIT-STATE-01/02` FSM e `AUDIT-SEC-01` anti-XSS).
   - Calcular o Score de Prontidão ($\text{Score} = 0.35\cdot\text{A11y} + 0.30\cdot\text{FSM} + 0.20\cdot\text{Tokens} + 0.15\cdot\text{Sec}$).

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
1. **Arquivos Modularizados e Refatorados**: Links clicáveis `file:///` para `DESIGN.md`, `styles/`, `components/ui/`, `components/bento/`, `components/layout/`, `config/` e `types/`.
2. **Checklist Gatekeeper `[AUDIT-01..09]` + Score `frontend-testing-auditor` (`0–100`)**.
3. **Verificação de Build/Testes**: Comprovação de compilação (`typecheck` / `Jest` / `Vitest`) e orçamento de linhas (`<= 300` linhas/arquivo).
