# Critérios Visuais OKLCH, Navegação 3 Camadas & Template de Saída (`auditoria-projetos-sistema`)

Complemento detalhado de [`SKILL.md`](../SKILL.md). Consulte também [`matriz_5_pilares_e_hand_off_2026.md`](matriz_5_pilares_e_hand_off_2026.md), [`rubrica_auditoria_e_agent_browser.md`](rubrica_auditoria_e_agent_browser.md) e [`taxonomia_subagentes_ui_6_camadas.md`](taxonomia_subagentes_ui_6_camadas.md).

## 1. Critérios Detalhados de Módulo 3 (60-30-10 OKLCH, Luz Zenital & Navegação SGA)

- **Proporção 60-30-10 (`OKLCH` + `light-dark()`):**
  - 60% Canvas (`--surface-canvas`, Dark Mode $L = 0.16$, zero `#000000`).
  - 30% Cartões (`--surface-card` $L = 0.22$, `--surface-elevated` $L = 0.27$, 4 variantes + `@container`).
  - 10% Acento cirúrgico (`--brand-primary` em `oklch(from ...)` / `color-mix(in oklab, ...)`), foco e indicadores `6px`/`2px`.
- **Sombras em 3 Níveis:** Primitivas (`--shadow-layer-sm/md/lg`) + Semânticos (`--shadow-elevation-1..3`, `--shadow-inset`), combinando Umbra + Penumbra (`spread` negativo `-1px..-8px`) + Borda Especular (`inset 0 1px 0 0` / `--catch-light`) + *Ambient Brand Glow* no escuro.
- **Navegação & Tipografia:** `<= 3` `<nav>` (*Global* Bottom Bar `env(safe-area-inset-bottom)` <-> Sidebar `240px` `100dvh` em `>= 48em`; *Local*; *Breadcrumbs* `<ol role="list">` + `::before` silencioso + `aria-current="page"` apenas `>= 3` níveis), Ordem DOM = Visual, menus `>= 13px` / `gap >= 8px` / `>= 44px` (`48px` touch), tokens `--space-*`, Raios Concêntricos ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$), `subgrid` + `.card:has(> img)`, `clamp()`, `60ch–65ch`, `tabular-nums`, `antialiased`, `font-synthesis: none`.

## 2. Formato Obrigatório de Saída (`0–100 pts` + `SGA`)

```markdown
# RELATÓRIO UNIFICADO DE AUDITORIA DE PROJETO, CÓDIGO REAL, MVP E NAVEGAÇÃO (v6.0.0)
- **Projeto & Caminho:** [Nome / Caminho] | **Modo:** `[mvp_and_plan | deep_code_and_nav_audit | live_dom_inspection]`
- **Nível de Complexidade Detectado:** `[Nível 1 | Nível 2 | Nível 3 | Modular MCP/Poliglota]`
- **Scores Determinísticos:** **Nota Geral:** `XX/100` | **SGA:** `XX.XX/100` | **TIF:** `[PASS | FAIL]`

## 1. DIAGNÓSTICO EXECUTIVO DE MVP & PARIDADE DOCUMENTAL VS. CÓDIGO REAL (40 pts)
- **Objetivo Principal & Estado Atual:** [Síntese do código real]
- **O Que Falta para o MVP:** 1. **[Bloqueante]:** [Descrição] — **Por quê:** [Impacto real]

| Item / Caminho | Classificação Real (AST/Disco) | Evidência |
| :--- | :--- | :--- |
| `[Arquivo / Módulo]` | `[IMPLEMENTADO_FUNCIONAL | MOCK_SUPERFICIAL | INEXISTENTE_DOCUMENTADO | CÓDIGO_FANTASMA]` | `[Linha / Função]` |

## 2. MATRIZ DOS 5 PILARES TÉCNICOS (60 pts)
| Pilar | Diagnóstico (`[PASS/FAIL]`) | Prioridade | Ação & Impacto |
| :--- | :--- | :--- | :--- |
| **1. Design 60-30-10 OKLCH & Sombras 3 Níveis** | ... | `[PRIORIDADE | MODERADO | EXTRA]` | ... |
| **2. Navegação 3 Camadas, Ilhas & SGA** | ... | ... | ... |
| **3. Qualidade AST & Órfãos** | ... | ... | ... |
| **4. Segurança & Contratos MCP/RPC** | ... | ... | ... |
| **5. Atualização Temporal & Árvore** | ... | ... | ... |

## 3. PLANO DE AÇÃO EXECUTÁVEL (EM 3 FASES)
- [ ] **Fase 1 (Crítico / MVP):** [Ação + arquivo]
- [ ] **Fase 2 (Estrutura, Navegação & AST):** [Ação + arquivo]
- [ ] **Fase 3 (Polimento OKLCH & Extras):** [Ação + arquivo]
```
