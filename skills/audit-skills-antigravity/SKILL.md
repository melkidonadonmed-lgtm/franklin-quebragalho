---
name: audit-skills-antigravity
description: "Executa audit-skills-antigravity em habilidades Skills privadas em Python, Go e JS via REA, analisando Context Bloat, colisões, Pass@k e FNR. Use para auditar skills; não use para CSS."
version: "2.1.0"
updated_at: "2026-10-28"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "2.1.0"
  updated_at: "2026-10-28"
  author: "SkillCraft & Melki"
  category: "Governança, Engenharia Reversa REA e Auditoria Matemática de Skills"
  tags: ["audit-skills-antigravity", "rea-skill-audit", "context-bloat", "pass-at-k", "fnr", "progressive-disclosure"]
---
# Skill: `audit-skills-antigravity` — Governança e Auditoria de Skills Privadas com REA (`v2.2.0`)

## 1. Propósito e Gatilhos de Ativação (Quando Usar)

Audita pacotes de Agent Skills privadas em Python, Go e JavaScript/TypeScript combinando inspeção estática via **REA (`Reverse Engineer Anything` v6.8+ / `v49`)** e o motor em Go ([`scripts/skill_auditor_rea.go`](scripts/skill_auditor_rea.go) / `skill_auditor_rea_service.go`), avaliando conformidade de frontmatter YAML, inchaço de contexto (*Context Bloat* > 1.200 tokens), saturação de regras (> 10–15 regras ativas), alinhamento de catálogo (`rea doctor --skill --json`) e métricas formais $\text{Pass}@k$ e $\text{FNR}$.

## 2. Entradas, Pré-requisitos e Parâmetros

- `skills_root_dir` (obrigatório): Diretório contendo as pastas de skills (`SKILL.md`, `scripts/`, `references/`).
- `rea_detail` (opcional): `"summary"` (padrão para projeção enxuta em `inspect_analysis_view`).
- `k_samples` (opcional): Parâmetro $k$ para cálculo do estimador não enviesado $\text{Pass}@k$ (padrão $k=3$).

## 3. Fluxo de Processamento em 4 Etapas (Via REA + Motor Go)

```text
[1. COLETA DE EVIDÊNCIAS (REA)] ──► Executa analyze_javascript_application / inspect_go_binary
               │
               ▼
[2. PROJEÇÃO RESUMIDA (VIEW)]   ──► Filtra dados via inspect_analysis_view (detail: summary)
               │
               ▼
[3. CONFRONTO DE REGRAS & EVALS]──► Avalia YAML, Context Bloat, MCP e Relação de Ferramentas
               │
               ▼
[4. RELATÓRIO CLASSIFICADO]     ──► Emite matriz com [FATO OBSERVADO] e 6 Categorias de Ação
```

1. **Extração Passiva de DNA & Identidade (`REA v6.8`):** Valide a identidade da skill e dos provedores via `npx rea-agents@6.8.0 doctor --client antigravity --skill --json` (`skill_version: 49`, 229 MCP tools, 175 CLI commands, 6 MCP prompts) e `binary_session({})`, invocando `analyze_javascript_application` e `inspect_go_binary` seguidos de `inspect_analysis_view(detail="summary")` sem inflar a janela de contexto.
2. **Avaliação de Divulgação Progressiva e Context Bloat (`<= 1.200` tokens):** Reprove `SKILL.md` com mais de `1.200` tokens estimados no corpo (Nível 2) ou excesso de regras listadas (`> 10`–`15` itens) sem desacoplamento em `references/` ou `scripts/`, alinhado ao SSOT de `estante` e `skill_auditor_rea_service.go`.
3. **Métricas Matemáticas ($\text{Pass}@k$ e $\text{FNR}$):** Calcule $\text{Pass}@k = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}$ e $\text{FNR} = \frac{\text{FN}}{\text{TP}+\text{FN}}$ (exigindo $\text{FNR} = 0.0$ em skills de segurança e isolamento de `_meta.provenance.untrusted_content == true`).

## 4. Saídas, Entregáveis e As 6 Categorias de Ação

O relatório consolida uma tabela com `Skill | Linguagem | Regras (<=10) | Tokens Est. | Pass@3 | FNR | Recomendação` classificada nas **6 Categorias Canônicas** detalhadas em [`references/rea_audit_categories.md`](references/rea_audit_categories.md): `[MANTER]`, `[ATUALIZAÇÃO]`, `[AJUSTE]`, `[MELHORIA]`, `[EXCLUSÃO]` e `[FUSÃO]`.

## 5. Limites, Exceções e Guardrails (Quando NÃO Usar)

1. **Não usar para auditoria de contraste visual, DOM ou CSS frontend:** Para auditoria visual de interfaces web, utilize `plan-uiux`, `frontend-testing-auditor` ou `complex-zero`.
2. **Vedação contra Leitura Bruta sem REA:** Em repositórios com dezenas de skills e scripts, execute o agregador determinístico e o `inspect_analysis_view(detail="summary")` antes de abrir arquivos extensos.
3. **Preservação das 5 Seções Canônicas:** Ao desidratar um `SKILL.md` para `references/`, preserve sempre os cabeçalhos obrigatórios do validador determinístico.
4. **Skills de terceiros são somente leitura:** quando o relatório traz `third_party_source` (instaladas por `npx skills`/`~/.agents/.skill-lock.json`, `rea-agents`, `android` CLI, autor externo ou `LICENSE` de fornecedor), nunca edite o frontmatter (`version`, `updated_at`, `allowed-tools`, `license`) nem o corpo, e não crie arquivos em `references/`. Atualize pelo instalador de origem. Em 2026-11-09 essa reescrita removeu `license`, gravou acentos como `?` e deixou links para `references/extended_playbook.md` inexistente em 37 skills.
