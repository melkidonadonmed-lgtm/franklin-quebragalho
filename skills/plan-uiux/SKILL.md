---
name: plan-uiux
description: "Análise minuciosa e global de frontend UI/UX com REA Reverse Engineer Anything, proporção 60-30-10 OKLCH e propostas de mutação Antes Depois. Use para auditar UI com REA; não use para backend puro."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "1.2.0"
  updated_at: "2026-11-13"
  author: "UI-Architect & Melki"
  category: "Auditoria Estrutural e Planejamento Global UI/UX com REA"
  tags: ["plan-uiux", "rea-uiux", "oklch", "60-30-10", "container-queries", "before-after-diff"]
---

# `plan-uiux` — Auditoria e Planejamento UI/UX com REA

## 1. Propósito e Gatilhos (Quando Usar)

Executa auditoria estrutural e visual de aplicações frontend empacotadas, compiladas ou ativas (JS/TS/Electron, binários Go com UI embarcada e web ao vivo) baseada em evidências do **REA (`Reverse Engineer Anything`)**, emitindo planos **CLAREZA** com diffs `Antes vs. Depois`. Para código-fonte aberto sem build empacotado, prefira `frontend-ui-ux-auditor` ou `auditoria-projetos-sistema`.

## 2. Entradas e Parâmetros

- **`target_path` (obrigatório):** Raiz do frontend empacotado ou serviço Go com UI embarcada.
- **`detail_level` (opcional):** `"summary"` (padrão no `inspect_analysis_view`) ou `"full"`.
- **`reference_docs` (opcional):** `README.md`, `SPEC.md`, `DESIGN.md`, `AGENTS.md`.

## 3. Processamento em 4 Etapas via REA

Consulte o fluxo completo e tokens em [`references/etapas_rea_uiux.md`](references/etapas_rea_uiux.md):

1. **Extração REA:** Rodar `analyze_javascript_application` / `inspect_go_binary` e projetar `inspect_analysis_view(kind="javascript-routes" | "javascript-facts" | "api-surface", detail="summary")`; em web viva usar `inspect_web_page`, `capture_web_screenshot` e `compare_web_screenshots` (isolando `_meta.provenance.untrusted_content == true`).
2. **Cores `OKLCH` & `60-30-10`:** Validar 60% Canvas, 30% Superfícies, 10% Pontos Focais.
3. **Elevação 3 Camadas & Dark Mode:** Exigir Umbra + Penumbra negativa + Catch-Light zenital e $L$ progressivo (`0.16 -> 0.22 -> 0.27`).
4. **`@container`, `subgrid` & Navegação:** Exigir `@container` separado de `subgrid`, `--space-*`, raios concêntricos, `clamp()`, `60ch–65ch`, `tabular-nums`, Único DOM (`env(safe-area-inset-bottom)` $\leftrightarrow$ Sidebar Rail `240px`) e alvos `48x48px` (`any-pointer: coarse`).

## 4. Saídas e Entregáveis (CLAREZA)

Achados classificados em `[FATO OBSERVADO]`, `[INFERÊNCIA TÉCNICA]` e `[INCERTEZA / LACUNA]` nas 7 seções **CLAREZA** (**C**ontexto, **L**eitor, **A**ção, **R**eferências, **E**strutura, **Z**onas de Risco, **A**valiação) + mutação `Antes vs. Depois` ([`references/mutation_patterns.md`](references/mutation_patterns.md) e [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)).

## 5. Exceções, Limites e Quando NÃO Usar

- **Backend Puro:** Para servidores sem interface gráfica use `agent-server-auditor` ou `code-acceptability-auditor`.
- **Bloqueios:** Nunca carregar bundles minificados brutos no prompt (use `detail: "summary"`), proibir emojis em UI e garantir toque `>= 48x48px` + `:focus-visible`.
