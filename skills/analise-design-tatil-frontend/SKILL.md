---
name: analise-design-tatil-frontend
description: >-
  Fase 1 (Diagnóstico Read-Only): escaneia projetos frontend com audit_tactile_ui.py sob DESIGN.md v4.5-soft, detectando SoftCard órfão, bordas 1px, cobalto/blur e pastas faltantes. Não use para refatorar código (use refatoracao-design-tatil-frontend).
license: MIT
metadata:
  version: "2.2.0"
  author: "FrontCraftMaster & Melki"
  category: "Design System Tátil, Minimalist Impact e Frontend"
  updated_at: "2026-10-18"
  tags:
    - "design-tatil"
    - "minimalist-impact"
    - "auditoria-ui"
    - "design-md"
    - "anti-cobalto"
    - "subagentes-ui-3+1"
version: 2.2.0
updated_at: 2026-10-18
author: FrontCraftMaster & Melki
category: Design System Tátil, Minimalist Impact e Frontend
authorized_sub_skills:
  - name: design-md
    role: "Síntese e criação automática do DESIGN.md v4.5-soft na raiz quando ausente"
  - name: frontend-code-architect
    role: "Padronização modular src/ em 5 camadas de Design Atômico (v4.1.0)"
  - name: frontend-testing-auditor
    role: "Execução determinística de scripts/audit_tactile_ui.py + Axe-Core (v2.6.0)"
  - name: consultor-design-tatil-frontend
    role: "Fase 2 — Seleção interativa de tema (4 presets Soft UI + 22 paletas), mockup e scaffolding"
  - name: refatoracao-design-tatil-frontend
    role: "Fase 3 — Implementação prática nos componentes em 3 ondas (Topologia 3+1)"
---

# Fase 1: Inspeção Visual, Varredura da Raiz e Auditoria Frontend (`analise-design-tatil-frontend` v2.2.0) 🔍

Ponto de entrada (**Fase 1 — Diagnóstico Read-Only**) da esteira de UI/UX Tátil & Minimalist Impact Melki (`DESIGN.md v4.5-soft`). Combina a **varredura estrutural da pasta raiz** com o scanner determinístico **`audit_tactile_ui.py`** (`frontend-testing-auditor` v2.6.0) para impedir falsos positivos ("componentes placebo", bordas `1px` do Tailwind, micro-texto `10px`/`11px` e *comment-gaming* de FSM).

---

## 🔗 Esteira Encadeada de Frontend (Zero Sobreposição)

| Fase / Skill | Papel Exato |
| :--- | :--- |
| **Fase 1: `analise-design-tatil-frontend`** *(esta)* | Diagnóstico *read-only*: roda `audit_tactile_ui.py`, mapeia pastas faltantes e aponta onde há "cara de IA genérica". |
| **Fase 2: `consultor-design-tatil-frontend`** | Consulta escolhas via `ask_question` (4 presets `v4.5-soft`: `slate`, `moss`, `sapphire`, `obsidian`), estrutura pastas via `frontend-code-architect` e gera `DESIGN.md` + mockup. |
| **Fase 3: `refatoracao-design-tatil-frontend`** | Refatora na prática as views reais (`App.tsx`, `Sidebar.tsx`, `*Workspace.tsx`) em 3 ondas com os 4 subagentes `ui-*` até passar no `audit_tactile_ui.py`. |

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Diagnosticar por que uma interface parece feita por "IA genérica" ou auditar conformidade com o `DESIGN.md v4.5-soft`.
- Mapear pastas/arquivos ausentes (`DESIGN.md`, `components/ui/`, `components/bento/`, `components/layout/`, `config/`, `styles/`, `types/`) antes de refatorar.

### 🚫 Quando NÃO Usar
- Para aplicar mutações em lote no código das telas (use `refatoracao-design-tatil-frontend`).
- Para auditoria exclusiva de backend sem interface (use `auditoria-projetos-sistema`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `project_root_path` (obrigatório): Caminho da pasta raiz do projeto frontend a ser inspecionado.
- `target_url` (opcional): URL ativa para inspeção ao vivo via `agent-browser`.

---

## ⚙️ Fluxo de Execução em 3 Passos

### Passo 1: Execução Imediata do Scanner Determinístico (`audit_tactile_ui.py`)
Nunca avalie no "olhômetro". Execute imediatamente:
```powershell
python C:\Users\melki\dev\repos\franklin-quebragalho\skills\frontend-testing-auditor\scripts\audit_tactile_ui.py --target "<project_root_path>"
```
Este script mede de forma exata:
- **Adoção Real vs. Placebo (`ORPHAN-SOFTCARD`)**: Quantas views reais importam `<SoftCard />`, `.ui-card-soft`, `.ui-btn-tactile` e `--surface-inset`.
- **Contagem de Clichês de IA Genérica**: Bordas duras `1px` (`border-slate-*`), `backdrop-blur`, gradientes (`bg-gradient-to-*`), micro-texto (`text-[10px]`/`text-[11px]`), azul cobalto e emojis em UI.
- **Integridade de FSM e Tracker**: Detecta *comment-gaming* (`// empty | loading | success | error`) e verifica se `#sidebar-active-tracker` é realmente deslizante.

### Passo 2: Varredura da Pasta Raiz (5 Camadas de Design Atômico)
Verifique a presença de:
1. `DESIGN.md` (`v4.5-soft` na raiz) — se ausente, sinalize para a `design-md`.
2. `src/components/ui/`, `src/components/bento/`, `src/components/layout/`.
3. `src/styles/globals.css` (única fonte de verdade de tokens `--surface-canvas`, `--surface-inset`, `--surface-flat`, `--surface-raised`, `--surface-contrast`, sem briga de `!important` entre múltiplos arquivos CSS).
4. `src/config/tokens.ts` e `src/types/index.ts` (referenciando [`references/tokens_frontcraft.json`](references/tokens_frontcraft.json) `v4.5.0-soft`).

### Passo 3: Emissão da Matriz `[DISC-*]` e Hand-off para a Topologia 3+1
Emita o diagnóstico com base nos números reais do `audit_tactile_ui.py` e encaminhe para a Fase 2 (`consultor-design-tatil-frontend`) ou Fase 3 (`refatoracao-design-tatil-frontend`), ativando os 4 subagentes de UI (`ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer`) via `invoke_subagent` ou `franklin_execute_dag(plan_path_or_json="ui", target_dir="<project_root_path>")`.

---

## 🤖 Ativação de Agentes e Subagentes (`Topologia 3+1`)
- **Persona Coordenadora:** `FrontCraftMaster`
- **Subagentes Vinculados:**
  - `ui-shell-navigator` (Onda 1 — Shell, UI Islands e `#sidebar-active-tracker`)
  - `ui-controls-data` (Onda 2A — Controles 44x44px anti-squish, `tabular-nums` e `aria-live`)
  - `ui-motion-interaction` (Onda 2B — Física 135°, `--ease-spring` e `prefers-reduced-motion`)
  - `ui-deterministic-observer` (Onda 3 Gatekeeper — `audit_tactile_ui.py`, WCAG AA e `9/9 PASS`)
- **Comandos de Disparo:** `invoke_subagent` ou `franklin_execute_dag(plan_path_or_json="ui", target_dir="<project_root_path>")`.

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
1. **Saída Real do `audit_tactile_ui.py`**: Readiness Score (`0–100`), métricas visuais e lista de discrepâncias `[FAIL: ...]`.
2. **Mapa Estrutural da Raiz (`[OK]` vs `[MISSING]`)**.
3. **Plano de Hand-off Cirúrgico** para a Fase 2 ou Fase 3.
