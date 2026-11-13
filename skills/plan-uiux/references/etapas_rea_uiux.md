# Etapas REA UI/UX e Critérios Detalhados — `plan-uiux`

Referência das 4 etapas REA e padrões ópticos consumida por [`../SKILL.md`](../SKILL.md), complementando [`mutation_patterns.md`](mutation_patterns.md).

## Fluxo REA UI/UX em 4 Etapas

```text
[1. EXTRAÇÃO VIA REA]       ──► Executa analyze_javascript_application / inspect_go_binary
              │
              ▼
[2. VISÃO RESUMIDA (VIEW)]  ──► Filtra grafos via inspect_analysis_view (detail: summary)
              │
              ▼
[3. BENCHMARK & CLAREZA]    ──► Confronta evidências com padrões OKLCH, 60-30-10 e A11y
              │
              ▼
[4. PROPOSTA DE MUTAÇÃO]    ──► Emite o plano estruturado com código Antes vs. Depois
```

## Padrões Técnicos Verificados

1. **Coleta REA:** `analyze_javascript_application` / `inspect_go_binary` -> `parent_evidence_id` -> `inspect_analysis_view(kind="javascript-routes" | "javascript-facts" | "api-surface", detail="summary")`, complementando UI web viva com `inspect_web_page`, `capture_web_screenshot` e `compare_web_screenshots` (isolando `_meta.provenance.untrusted_content == true`).
2. **Cores & 60-30-10 (`OKLCH`):** `oklch(L C H)` em 60% Canvas, 30% Superfícies e 10% Pontos Focais.
3. **Elevação Física em 3 Camadas & Dark Mode:** Umbra + Penumbra com `spread` negativo + Catch-Light zenital (`--shadow-elevation-1..3` / `--shadow-elevation-low/medium/high`) e $L$ progressivo (`0.16 -> 0.22 -> 0.27`).
4. **Responsividade, Cards & Navegação:** `@container` separado de `subgrid`, tokens `--space-*` / `--space-card-padding` / `--space-grid-gap`, raios concêntricos $R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$, `flex-wrap: balance`, `clamp()` ($\max \le 2.5\times \min$), `max-inline-size: 60ch–65ch`, `tabular-nums`, Único DOM (`env(safe-area-inset-bottom)` $\leftrightarrow$ Sidebar Rail `240px`) e alvos `48x48px` em `any-pointer: coarse`.
