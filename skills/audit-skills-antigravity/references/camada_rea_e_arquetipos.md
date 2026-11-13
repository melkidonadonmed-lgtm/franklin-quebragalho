# Fluxo em 4 Etapas e Camadas REA / Cognitiva — `audit-skills-antigravity`

Referência estendida consumida por [`../SKILL.md`](../SKILL.md) e complementando [`rea_audit_categories.md`](rea_audit_categories.md).

## Fluxograma de Auditoria em Dupla Camada

```text
[1. SONDAGEM REA & AMBIENTE]      ──► Sintaxe AST/JSON, links/arquivos reais no SO e dependências REA
               │
               ▼
[2. DETECTOR DE COLISÃO & REGRAS] ──► Colisão de rotas/nomes/gatilhos e regras opostas/incompatíveis
               │
               ▼
[3. CRIVO COGNITIVO-ARQUETÍPICO]  ──► 8 Elos, filtro anti-homogeneização, vagueza e ferramentas reais
               │
               ▼
[4. VEREDITO & MÉTRICAS (GO)]     ──► Coerência (0-100), Pass@3, FNR e classificação nas 6 Categorias
```

## Camada 1 & Camada 2 (Detalhamento)

- **Camada 1 — REA, Sintaxe, Ambiente & Colisões:** Auditar AST/JSON via `go run skills/audit-skills-antigravity/scripts/skill_auditor_rea.go` + `inspect_analysis_view(detail="summary")`; verificar existência física de `scripts/...`, `references/...`, `rules/...` no `Windows 11 / pwsh`, detectar colisões de rotas/gatilhos e regras incompatíveis/opostas.
- **Camada 2 — 8 Elos & Arquétipos:** Cadeia `Nome <-> Descrição <-> Gatilhos <-> Objetivo <-> Estrutura <-> Comandos <-> Referências <-> Ferramentas/Uso Real`:
  - **Anti-Homogeneização:** Reprovar boilerplate CSS/OKLCH (`60-30-10`, `--shadow-elevation`) em skills não-visuais.
  - **Arquétipo `PLANNING`:** 6 fatores-chave: *(i)* decomposição atômica, *(ii)* estrutura/hierarquia, *(iii)* precedência lógica DAG/Kahn, *(iv)* gestão de ambiguidade (`[LACUNA]`), *(v)* descrição de processos e *(vi)* guardrails de segurança.
  - **Arquétipo `E2E_UI_AUDIT`:** Uso real de ferramentas (`click`, `a11y`, `snapshot`/DOM, `agent-browser`/`@eX`, `chrome-devtools` ou scripts auditores); reprovar Falsa Capacidade sem execução real.
  - **Métricas:** $\text{Pass}@k = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}$ e $\text{FNR} = \frac{\text{FN}}{\text{TP}+\text{FN}}$, orçamento `SKILL.md <= 1.200` tokens (ou *Progressive Disclosure*).
