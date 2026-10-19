---
name: refatoracao-design-tatil-frontend
description: >-
  Fase 3 (Execução de Código & Orquestração 3+1): refatora views reais (.tsx/.vue/.html) aplicando <SoftCard /> 135°, #sidebar-active-tracker deslizante e 8 kits Soft UI até passar no audit_tactile_ui.py. Não use para diagnóstico read-only (Fase 1).
license: MIT
metadata:
  version: "2.2.0"
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
version: 2.2.0
updated_at: 2026-10-18
author: FrontCraftMaster & Melki
category: Implementação, Minimalist Impact e Refatoração Frontend
authorized_sub_skills:
  - name: design-md
    role: "Garantia de que o DESIGN.md v4.5-soft reflita fielmente os tokens e componentes implementados"
  - name: frontend-code-architect
    role: "Padronização modular src/ em 5 camadas de Design Atômico (v4.1.0)"
  - name: frontend-testing-auditor
    role: "Gatekeeper determinístico via scripts/audit_tactile_ui.py + Axe-Core (v2.6.0)"
---

# Fase 3: Refatoração Prática de Código e Orquestração em 3 Ondas (`refatoracao-design-tatil-frontend` v2.2.0) ⚡

Motor de **Execução de Código e Modularização** (**Fase 3**) da esteira Frontend Melki. Consome o diagnóstico da Fase 1 (`analise-design-tatil-frontend`) e o `DESIGN.md v4.5-soft` para **substituir efetivamente o Tailwind de IA genérica nas views reais (`App.tsx`, `Sidebar.tsx`, `*Workspace.tsx`)** pelos 8 Kits Soft UI a 135° e aprovar o projeto no scanner determinístico **`audit_tactile_ui.py`**.

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Refatorar na prática o código `.tsx`, `.jsx`, `.vue` ou `.html`/`.css` para o padrão **Minimalist Impact & Soft Tactile (`v4.5-soft`)**.
- Eliminar "cara de IA genérica": substituir `border-slate-*` (`1px`), `bg-gradient-to-*`, `backdrop-blur`, micro-textos `text-[10px]`/`text-[11px]` e emojis por `<SoftCard />`, `.ui-card-soft`, `.ui-btn-tactile`, `--surface-inset` e ícones vetoriais Lucide.

### 🚫 Quando NÃO Usar
- Para apenas inspecionar e gerar relatório sem tocar no código (use `analise-design-tatil-frontend`).
- Para alterações puras de backend/banco de dados sem impacto em UI.

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `project_root_path` (obrigatório): Caminho absoluto da raiz do projeto frontend.
- `preset` (opcional, padrão `slate`): Preset ativo dentre os **4 Presets Soft UI** (`slate` `#0284C7`, `moss` `#2E6F40`, `sapphire` `#0369A1`, `obsidian` `#38BDF8`) em [`references/tokens_frontcraft.json`](references/tokens_frontcraft.json).

---

## ⚙️ Regras Anti-Placebo e Execução em 3 Ondas (`Topologia 3+1`)

### Passo 0: Saneamento CSS Único e Proibição de Componentes Placebo
1. **Fonte Única de Tokens CSS (`globals.css`)**: Unifique os tokens (`--surface-sunken`, `--surface-canvas`, `--surface-inset`, `--surface-flat`, `--surface-raised`, `--surface-contrast`, `--accent-point`, `--shadow-card`, `--shadow-ambient`, `--shadow-float`, `--shadow-inset`, `--ease-spring`). **Proibido** criar múltiplos arquivos CSS brigando com `!important` sobre `.bg-slate-900`.
2. **Proibição de `<SoftCard />` Órfão**: Não basta criar `src/components/ui/SoftCard.tsx`; você **DEVE importar e usar `<SoftCard />`, `.ui-card-soft` e `.ui-btn-tactile` diretamente nas views reais** (`App.tsx`, `Sidebar.tsx`, `*Workspace.tsx`), removendo as classes `border border-slate-*` e `bg-gradient-to-*` do JSX.
3. **Proibição de Comment-Gaming**: Nunca adicione comentários `// empty | loading | success | error` para simular FSM. Implemente `data-state`, `aria-busy` e `role="alert"` reais no JSX.

### Passo 1: Onda 1 — Casca Estrutural, Bento Grid & Sidebar Tátil (`ui-shell-navigator`)
Acione `invoke_subagent(TypeName="ui-shell-navigator", ...)` na camada `components/layout/` e `components/bento/`:
- **Matriz Bento de 12 Colunas**: `grid-cols-12 gap-6` (`col-span-8` + `col-span-4`), `CLS < 0.1` e zero bordas duras de `1px`.
- **Tactile Companion Sidebar (`#sidebar-active-tracker`)**: Sidebar (`256px`) em `--surface-inset` com um **único elemento companion deslizante** `#sidebar-active-tracker` (`position: absolute; height: 52px; transition: transform 0.35s var(--ease-spring)`) + barra vertical esquerda de `4px` (`var(--accent-point)`). Proibido colocar `id="sidebar-active-tracker"` condicional em item estático de `.map()`.
- **Inversão Tonal Terrixa (`.terrixa-notched`)**: Destaque de cards âncora via `--surface-contrast` e recorte chanfrado `24px`.

### Passo 2: Onda 2 (Paralela) — 8 Kits Soft UI (`ui-controls-data`) + Física Spring (`ui-motion-interaction`)
1. **`ui-controls-data`**: Aplicar nas views os 8 Kits (`<SoftCard />`, `.ui-btn-tactile` $\ge 44\times44\text{px}$ anti-squish, `.badge-soft`, `.swatch-disc`, `.tactile-thumb`, `.tactile-range`, `.surface-inset-pill`, `.activity-row`), escala tipográfica `1.25` (zero `text-[10px]`/`text-[11px]`), `tabular-nums` e zero emojis em botões.
2. **`ui-motion-interaction`**: Hover `translateY(-2px)` com `--shadow-float`, clique `:active` convertendo para `--surface-inset` com `translateY(1px)` e `@media (prefers-reduced-motion: reduce)`.

### Passo 3: Onda 3 (Gatekeeper Obrigatório) — `ui-deterministic-observer` + `audit_tactile_ui.py` + `franklin_execute_dag`
Execute obrigatoriamente no terminal e/ou via MCP (`franklin_execute_dag(plan_source="ui", target_dir="<project_root_path>")`):
```powershell
python C:\Users\melki\dev\repos\franklin-quebragalho\skills\frontend-testing-auditor\scripts\audit_tactile_ui.py --target "<project_root_path>"
```
- Se o `Readiness Score` for `< 90.0` ou houver qualquer `[FAIL: ORPHAN-SOFTCARD]`, `[FAIL: HARD-BORDERS-1PX]`, `[FAIL: MICRO-TYPOGRAPHY]`, `[FAIL: EMOJI-IN-UI]` ou `[FAIL: FSM-COMMENT-GAMING]`, **corrija as views antes de encerrar**.

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
1. **Views Reais Refatoradas**: Links clicáveis `file:///` comprovando o uso de `<SoftCard />` / `.ui-card-soft` nas telas principais.
2. **Saída Real do `audit_tactile_ui.py`**: Comprovação de `Readiness Score >= 90.0` e `[PASS]`.
3. **Verificação de Build/Testes**: Comprovação de compilação (`typecheck` / `Vitest` / `Jest`).
