---
name: plan-uiux
description: "Análise minuciosa e global de frontend UI/UX com REA Reverse Engineer Anything, proporção 60-30-10 OKLCH e propostas de mutação Antes Depois. Use para auditar UI com REA; não use para backend puro."
version: "1.1.0"
updated_at: "2026-10-28"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "1.1.0"
  updated_at: "2026-10-28"
  author: "UI-Architect & Melki"
  category: "Auditoria Estrutural e Planejamento Global UI/UX com REA"
  tags: ["plan-uiux", "rea-uiux", "oklch", "60-30-10", "container-queries", "before-after-diff"]
---
# Skill: `plan-uiux` — Auditoria & Planejamento Global de Frontend UI/UX com REA (`v1.2.0`)

## 1. Propósito e Gatilhos de Ativação (Quando Usar)

Executa auditoria estrutural e visual de aplicações frontend (JavaScript/TypeScript/React e templates Go) orientada a evidências verificáveis do **REA (`Reverse Engineer Anything`)**, confrontando o grafo real do código com a arquitetura CSS moderna (`OKLCH`, proporção `60-30-10`, sombras multi-camadas, `@container` e tipografia fluida `clamp()`) e emitindo planos **CLAREZA** com diffs `Antes vs. Depois`.

## 2. Entradas, Pré-requisitos e Parâmetros

- `target_path` (obrigatório): Diretório raiz do projeto frontend ou serviço Go com UI embarcada.
- `detail_level` (opcional): `"summary"` (padrão para economia de contexto no `inspect_analysis_view`) ou `"full"`.
- `reference_docs` (opcional): Caminhos para `README.md`, `SPEC.md`, `DESIGN.md` e `AGENTS.md`.

## 3. Fluxo de Processamento em 4 Etapas (Via REA)

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

1. **Coleta de Evidências Estáticas & Visuais (`REA v6.8+`):** Execute `analyze_javascript_application` / `inspect_go_binary`, extraia o `parent_evidence_id` e projete rotas e fatos de UI via `inspect_analysis_view(kind="javascript-routes" | "javascript-facts" | "api-surface", detail="summary")`. Em alvos web ativos, complemente com `inspect_web_page`, `capture_web_screenshot` e `compare_web_screenshots` (isolando `_meta.provenance.untrusted_content == true`).
2. **Validação de Cores e Proporção (`OKLCH` & `60-30-10`):** Verifique se as cores usam `oklch(L C H)` distribuídas em **60% Canvas**, **30% Superfícies** e **10% Pontos Focais**.
3. **Elevação Física e Dark Mode Progressivo:** Exija sombras multi-camadas (`0 1px 2px oklch(...), 0 4px 8px oklch(...)`) e clareamento progressivo da luminosidade $L$ no modo escuro (`0.16 -> 0.22`).
4. **Responsividade Autônoma & Tipografia:** Exija `@container` (`container-type: inline-size`), escala fluida `clamp()` e largura de leitura `max-inline-size: 65ch`.

## 4. Saídas, Entregáveis e Formato do Plano CLAREZA

Todo achado deve ser rotulado com classificação epistêmica estrita (`[FATO OBSERVADO]`, `[INFERÊNCIA TÉCNICA]`, `[INCERTEZA / LACUNA]`) e estruturado nas 7 seções **CLAREZA** (**C**ontexto, **L**eitor, **A**ção, **R**eferências, **E**strutura, **Z**onas de Risco, **A**valiação) acompanhado do bloco de mutação `Antes vs. Depois` (veja exemplos completos em [`references/mutation_patterns.md`](references/mutation_patterns.md)).

## 5. Limites, Exceções e Guardrails (Quando NÃO Usar)

1. **Não usar para auditoria de backend puro sem interface gráfica:** Para servidores sem UI, utilize `agent-server-auditor` ou `code-acceptability-auditor`.
2. **Vedação contra Inchaço de Contexto:** Nunca carregue bundles minificados inteiros no prompt; utilize sempre `inspect_analysis_view` com `detail: "summary"`.
3. **Zero Emojis e Alvos Táteis Seguros:** Proibido usar emojis em títulos/botões de UI; garanta área mínima de toque `48x48px` e `:focus-visible`.
