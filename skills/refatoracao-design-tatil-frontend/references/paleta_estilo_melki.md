# Mapa de Conversão de Classes Legadas para Soft UI 135° — Fase 3 (`refatoracao-design-tatil-frontend`)

> **SSOT de Presets Tonais**: Os códigos hexadecimais completos dos 4 presets (`slate`, `moss`, `sapphire`, `obsidian`) residem canonicamente em [`../../consultor-design-tatil-frontend/references/paleta_estilo_melki.md`](../../consultor-design-tatil-frontend/references/paleta_estilo_melki.md). Este guia define a **tabela cirúrgica de substituição de código (Fase 3)** para refatorar views reais (`.tsx`, `.jsx`, `.vue`, `.html`) até atingir `[PASS]` no `audit_tactile_ui.py`.

---

## 1. De-Para Cirúrgico de Classes (Tailwind / CSS Legado $\rightarrow$ `DESIGN.md v4.5-soft`)

| Padrão Legado (Proibido / Reprovado) | Substituto Canônico Soft Tactile (`v4.5-soft`) | Motivo Técnico |
| :--- | :--- | :--- |
| `<div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">` | `<SoftCard title="..." state={status}>...</SoftCard>` ou `<section className="ui-card-soft p-6">` | Elimina borda dura de `1px` e adota iluminação dupla a 135° com suporte a FSM |
| `<div className="bg-slate-900/60 backdrop-blur-md border border-slate-800">` | `<SoftCard className="ui-card-soft">...</SoftCard>` (`--surface-raised: #181D26`) | Banimento de Glassmorphism (`backdrop-blur`) e garantia de $L_{\text{card}} > L_{\text{canvas}}$ |
| `bg-blue-600 hover:bg-blue-700 text-white` | `ui-btn-tactile bg-[#0284C7] hover:bg-[#0369A1] text-white min-h-[44px] shrink-0 whitespace-nowrap` | Substitui cobalto por Cerulean Sapphire (`#0284C7`) com anti-squish e alvo $\ge 44\text{px}$ |
| `<input className="border border-gray-300 rounded-lg px-3 py-2" />` | `<input className="surface-inset-pill px-4 min-h-[44px]" />` | Substitui caixa com borda dura por cavidade escavada `Layer 1` (`--surface-inset: #E5E9F0`) |
| `text-[10px]` / `text-[11px] uppercase` | `text-xs font-medium tracking-wider tabular-nums` | Elimina micro-tipografia ilegível e alinha dígitos em tabelas/badges |
| `id={isActive ? "sidebar-active-tracker" : undefined}` | `<div id="sidebar-active-tracker" style={{ transform: \`translateY(\${activeIndex * 52}px)\` }} />` | Garante tracker físico deslizante em `surface-inset` na Tactile Companion Sidebar |

---

## 2. Checklist de Preservação Funcional em Views Refatoradas

1. **Preservar 100% dos Handlers e Hooks**: Nunca remover `onClick`, `onSubmit`, `useEffect`, `data-testid` ou props de negócio ao trocar `<div>` por `<SoftCard />`.
2. **Conectar Estados Reais de FSM**: Mapear estados de carregamento/erro existentes (`isLoading`, `error`, `status`) para `aria-busy={isLoading}`, `data-state={status}` e `role="alert"` executáveis (sem comentários artificiais `// empty | loading | success | error`).
3. **Validar Pós-Refatoração**: Executar `uv run python skills/frontend-testing-auditor/scripts/audit_tactile_ui.py --target "<project_root>"` e confirmar `Verdict: PASS` (`Readiness >= 90.0`).
