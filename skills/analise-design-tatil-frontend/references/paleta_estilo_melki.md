# Matriz de Diagnóstico Visual e Sinais de Violação — Fase 1 (`analise-design-tatil-frontend`)

> **SSOT de Presets Tonais**: A especificação completa dos 4 presets (`slate`, `moss`, `sapphire`, `obsidian`) reside canonicamente em [`../../consultor-design-tatil-frontend/references/paleta_estilo_melki.md`](../../consultor-design-tatil-frontend/references/paleta_estilo_melki.md) e no contrato `DESIGN.md v4.5-soft`. Este documento concentra exclusivamente os **heurísticos e padrões de detecção somente-leitura (Fase 1)**.

---

## 1. Sinais Determinísticos de Reprovação (`audit_tactile_ui.py`)

| Código da Falha | Padrão / Regex Detectado na Fase 1 | Impacto Visual / Cognitivo | Recomendação de Correção (Para Fase 3) |
| :--- | :--- | :--- | :--- |
| **`TOKENS-V4.5`** | Ausência de `--surface-canvas`, `--surface-inset`, `--surface-raised`, `--accent-point` ou `--ease-spring` | UI sem contrato tátil unificado | Injetar `:root` canônico via `frontend-code-architect` (`v4.1.0`) |
| **`ORPHAN-SOFTCARD`** | `<SoftCard />` ou `.ui-card-soft` presente em `< 50%` das views não-primitivas | Componente placebo criado apenas para passar em checagem superficial | Substituir `<div>` genéricos das views reais por `<SoftCard />` |
| **`ANTI-COBALT`** | `#0044FF`, `#0057FF`, `#233DFF`, `#1D4ED8`, `#2563EB`, `bg-blue-600`, `text-indigo-500` | Fadiga retiniana e estética de template IA genérico | Migrar `--accent-point` para Cerulean Sapphire (`#0284C7`) ou Mineral Ice (`#38BDF8`) |
| **`ANTI-GLASSMORPHISM`** | `backdrop-filter: blur(...)` ou classes `backdrop-blur-*` | Ruído visual difuso e perda de contraste legível | Substituir por elevação tonal sólida a 135° (`.ui-card-soft`) |
| **`HARD-BORDERS-1PX`** | `> 6` ocorrências de `border-slate-*`, `border-gray-*`, `border-zinc-*` | "Caixa dentro de caixa" rígida sem percepção tátil | Delimitar ilhas por degrau tonal (`surface-raised` vs `surface-inset`) |
| **`MICRO-TYPOGRAPHY`** | Classes `text-[9px]`, `text-[10px]`, `text-[11px]` | Micro-texto ilegível fora da escala harmônica `1.25` | Elevar metadados para `0.75rem` (`12px`) ou `0.8125rem` (`13px`) com `tabular-nums` |
| **`EMOJI-IN-UI`** | Emojis Unicode (`U+1F300..1FAFF`) dentro de `.tsx`/`.vue`/`.html` | Quebra de sobriedade executiva e desalinhamento de baseline | Substituir por ícones vetoriais Lucide (`stroke-width: 1.75`) |
| **`FAKE-SIDEBAR-TRACKER`** | `id={isActive ? 'sidebar-active-tracker' : undefined}` dentro de `.map()` | Indicador salta estaticamente sem física deslizante | Implementar elemento irmão absoluto com `transform: translateY(...)` em `surface-inset` |

---

## 2. Protocolo de Inspeção Somente-Leitura (Zero Mutação na Fase 1)

1. Executar `uv run python skills/frontend-testing-auditor/scripts/audit_tactile_ui.py --target "<project_root>" --json`.
2. Inspecionar a árvore `src/` verificando a existência das 5 camadas do Design Atômico (`components/ui`, `components/bento`, `components/layout`, `config`, `styles`, `types`).
3. Emitir a tabela comparativa `[PASS]` / `[FAIL]` / `[UNVERIFIED]` com caminhos e linhas exatas antes de acionar a Fase 2 (`consultor-design-tatil-frontend`) ou Fase 3 (`refatoracao-design-tatil-frontend`).
