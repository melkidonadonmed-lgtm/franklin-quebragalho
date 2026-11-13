---
name: audit-skills-antigravity
description: "Executa audit-skills-antigravity em Skills privadas em Python, Go e JS via REA, auditando sintaxe, colisões de rotas/referências, coerência cognitiva por arquétipo, Pass@k e FNR. Use para auditar skills; não use para CSS."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "2.3.0"
  updated_at: "2026-11-13"
  author: "SkillCraft & Melki"
  category: "Governança, Engenharia Reversa REA e Auditoria Cognitivo-Discriminativa de Skills"
  tags: ["audit-skills-antigravity", "rea-skill-audit", "cognitive-audit", "route-collision", "context-bloat", "pass-at-k", "fnr"]
---

# `audit-skills-antigravity` — Auditoria REA & Cognitiva de Skills

## 1. Propósito e Gatilhos (Quando Usar)

Audita pacotes de Agent Skills em Python, Go e JS/TS via **REA (`Reverse Engineer Anything`)** e motor Go [`scripts/skill_auditor_rea.go`](scripts/skill_auditor_rea.go):

- **Camada 1 (REA, Sintaxe & Colisões):** AST/JSON de scripts, existência física de links (`scripts/`, `references/`, `rules/`), `Windows 11 / pwsh`, colisão de rotas/gatilhos, regras incompatíveis e orçamento `<= 1.200` tokens.
- **Camada 2 (Cognitivo-Discriminativa):** Cadeia dos **8 Elos**, filtro anti-homogeneização, vagueza/falhas lógicas e verificação real por arquétipo.

## 2. Entradas e Parâmetros

- **`skills_root_dir` (obrigatório):** Diretório raiz contendo `SKILL.md`, `scripts/`, `references/`, `evals/`.
- **`rea_detail` (opcional):** `"summary"` para projeção enxuta em `inspect_analysis_view`.
- **`k_samples` (opcional):** $k$ para $\text{Pass}@k$ (padrão: `3`).

## 3. Processamento em 4 Etapas e Arquétipos

Consulte [`references/camada_rea_e_arquetipos.md`](references/camada_rea_e_arquetipos.md) e [`references/rea_audit_categories.md`](references/rea_audit_categories.md):

1. **Sondagem REA & Ambiente:** Rodar `skill_auditor_rea.go` e `inspect_analysis_view(detail="summary")` checando caminhos reais e regras consistentes.
2. **Arquétipos & Anti-Homogeneização:** Bloquear CSS/OKLCH em skills não-visuais; exigir os **6 fatores** em `PLANNING` (decomposição, hierarquia, DAG/Kahn, `[LACUNA]`/ambiguidade, processos, guardrails) e ferramentas reais em `E2E_UI_AUDIT` (`click`, `a11y`, `snapshot`/DOM, `agent-browser`/`@eX`, `chrome-devtools`, scripts).
3. **Orçamento & Métricas:** Validar `<= 1.200` tokens (ou *Progressive Disclosure*) e calcular $\text{Pass}@k$ e $\text{FNR}$.

```powershell
go -C C:\Users\melki\dev\repos\franklin-quebragalho run ./skills/audit-skills-antigravity/scripts/skill_auditor_rea.go
```

## 4. Saídas e As 6 Categorias de Ação

Tabela (`Skill | Arquétipo | Coerência | Regras (<=10) | Tokens Est. | Pass@3 | FNR | Recomendação`) e diagnósticos (`broken_refs`, `collision_issues`, `cognitive_issues`) nas 6 categorias de `rea_audit_categories.md`: `[MANTIDA]`, `[ATUALIZAÇÃO]`, `[AJUSTE]`, `[MELHORIA]`, `[EXCLUSÃO]`, `[FUSÃO]`.

## 5. Exceções, Limites e Quando NÃO Usar

- **CSS / Visual Web / Backend Puro:** Não use para contrastes/DOM web (`plan-uiux`, `frontend-testing-auditor`, `complex-zero`).
- **Guardrails ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)):** Nunca aprovar apenas por YAML válido, preservar as 5 seções canônicas ao desidratar para `references/`, e tratar skills com `third_party_source` (`npx skills`, Orca, plugins externos) como **somente leitura**.
