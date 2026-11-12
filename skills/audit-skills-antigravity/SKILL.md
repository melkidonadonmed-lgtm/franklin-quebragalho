---
name: audit-skills-antigravity
description: "Executa audit-skills-antigravity em Skills privadas em Python, Go e JS via REA, auditando sintaxe, colisões de rotas/referências, coerência cognitiva por arquétipo, Pass@k e FNR. Use para auditar skills; não use para CSS."
version: "2.3.0"
updated_at: "2026-11-12"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "2.3.0"
  updated_at: "2026-11-12"
  author: "SkillCraft & Melki"
  category: "Governança, Engenharia Reversa REA e Auditoria Cognitivo-Discriminativa de Skills"
  tags: ["audit-skills-antigravity", "rea-skill-audit", "cognitive-audit", "route-collision", "context-bloat", "pass-at-k", "fnr"]
---
# Skill: `audit-skills-antigravity` — Auditoria Estrutural REA & Cognitivo-Discriminativa de Skills (`v2.3.0`)

## 1. Propósito e Gatilhos de Ativação (Quando Usar)

Audita pacotes de Agent Skills em Python, Go e JS/TS em **Dupla Camada** via **REA (`Reverse Engineer Anything` v6.8+)** e motor Go ([`scripts/skill_auditor_rea.go`](scripts/skill_auditor_rea.go)):

1. **Camada 1 — Engenharia Reversa REA, Sintaxe, Ambiente e Topologia:** Audita sintaxe/AST real de scripts e JSONs, integridade de caminhos/referências (`scripts/`, `references/`, `rules/`, links Markdown) compatíveis com o ambiente (`Windows 11 / pwsh`), **colisões entre nomes/rotas/gatilhos**, **regras incompatíveis ou opostas**, *Context Bloat* (`> 1.200` tokens) e métricas $\text{Pass}@k$ e $\text{FNR}$.
2. **Camada 2 — Processamento Cognitivo-Discriminativo e Anti-Homogeneização:** Avalia a cadeia de coerência de **8 Elos** (`Nome` $\leftrightarrow$ `Descrição` $\leftrightarrow$ `Gatilhos` $\leftrightarrow$ `Objetivo` $\leftrightarrow$ `Estrutura` $\leftrightarrow$ `Comandos` $\leftrightarrow$ `Referências` $\leftrightarrow$ `Ferramentas/Uso Real`), bloqueia contaminação entre domínios (ex.: regras de cores/CSS vazando para skills de planejamento ou backend), detecta **skills vagas ou com falhas lógicas** e verifica se a skill **faz realmente o que descreve** segundo seu arquétipo de domínio.

## 2. Entradas, Pré-requisitos e Parâmetros

- `skills_root_dir` (obrigatório): Diretório contendo as pastas de skills (`SKILL.md`, `scripts/`, `references/`, `evals/`).
- `rea_detail` (opcional): `"summary"` (projeção enxuta em `inspect_analysis_view`).
- `k_samples` (opcional): Parâmetro $k$ para cálculo de $\text{Pass}@k$ (padrão $k=3$).

## 3. Fluxo de Processamento em 4 Etapas (Camada REA + Camada Cognitivo-Discriminativa)

```text
[1. SONDAGEM REA & AMBIENTE]     ──► Valida sintaxe AST/JSON, links/arquivos reais no SO e dependências REA
               │
               ▼
[2. DETECTOR DE COLISÃO & REGRAS]──► Audita colisão de rotas/nomes/gatilhos e regras opostas/incompatíveis
               │
               ▼
[3. CRIVO COGNITIVO-ARQUETÍPICO] ──► Avalia os 8 Elos, filtro anti-homogeneização, vagueza e ferramentas reais
               │
               ▼
[4. VEREDITO & MÉTRICAS (GO)]    ──► Calcula Coerência (0-100), Pass@3, FNR e classifica nas 6 Categorias
```

1. **Validação REA de Sintaxe, Referências, Ambiente e Colisões (`Camada 1`):**
   - Inspecione artefatos via `go run skills/audit-skills-antigravity/scripts/skill_auditor_rea.go` e `inspect_analysis_view(detail="summary")`.
   - Verifique se todo arquivo ou criação citada (`scripts/...`, `references/...`, `rules/...`, `[...](...)`) existe no disco e respeita o ambiente (`Windows 11 / pwsh`), sem links fantasmas ou colisão de rotas/gatilhos entre skills.
   - Reprove **regras incompatíveis ou opostas** (ex.: declarar modo *read-only* mas instruir mutação destrutiva sem `HITL`, ou proibir e exigir o mesmo padrão).
2. **Avaliação Cognitivo-Discriminativa por Arquétipo (`Camada 2` — detalhada em [`references/rea_audit_categories.md`](references/rea_audit_categories.md)):**
   - **Anti-Homogeneização:** Reprove skills não-visuais (planejamento, backend, Go, disco, testes) que copiem boilerplate genérico de UI/cores (`OKLCH`, `60-30-10`, `--shadow-elevation`).
   - **Arquétipo `PLANNING` (Planejamento / DAG / Arquitetura):** Exige os **6 fatores-chave de um plano de qualidade**: *(i)* divisão/decomposição atômica, *(ii)* estrutura/hierarquia, *(iii)* coerência lógica e precedência (DAG/Kahn), *(iv)* gestão de ambiguidade (`[LACUNA]`/clarificação), *(v)* descrição dos processos e *(vi)* guardrails de segurança — validando se executa o que promete.
   - **Arquétipo `E2E_UI_AUDIT` (Auditoria E2E / UI / A11y):** Exige uso real de ferramentas de inspeção/interação (`click`, `a11y`/WAI-ARIA, `snapshot`/DOM, `agent-browser`/`@eX`, `chrome-devtools` ou scripts verificadores). Reprove por **Falsa Capacidade** qualquer skill E2E que não acione ferramentas reais de análise.
   - **Detector de Falhas Lógicas e Vagueza:** Reprove skills vagas (sem passos determinísticos, sem entradas/saídas claras ou cujos comandos/ferramentas não sustentem o objetivo declarado).
3. **Orçamento de Contexto (`<= 1.200` tokens) e Métricas ($\text{Pass}@k$ e $\text{FNR}$):**
   - Exija `<= 1.200` tokens no `SKILL.md` (ou *Progressive Disclosure* ativo) e calcule $\text{Pass}@k = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}$ e $\text{FNR} = \frac{\text{FN}}{\text{TP}+\text{FN}}$.

## 4. Saídas, Entregáveis e As 6 Categorias de Ação

Emite tabela com `Skill | Arquétipo | Coerência | Regras (<=10) | Tokens Est. | Pass@3 | FNR | Recomendação` e diagnósticos (`broken_refs`, `collision_issues`, `cognitive_issues`) nas **6 Categorias** de [`references/rea_audit_categories.md`](references/rea_audit_categories.md): `[MANTIDA]`/`[MANTER]`, `[ATUALIZAÇÃO]`, `[AJUSTE]`, `[MELHORIA]`, `[EXCLUSÃO]` e `[FUSÃO]`.

## 5. Limites, Exceções e Guardrails (Quando NÃO Usar)

1. **Não usar para auditoria de contraste visual, DOM ou CSS frontend:** Para interfaces web, use `plan-uiux`, `frontend-testing-auditor` ou `complex-zero`.
2. **Vedação contra Auditoria Puramente Estrutural:** Nunca aprove uma skill apenas porque o YAML é válido; valide referências físicas, ausência de colisão e coerência cognitiva do arquétipo.
3. **Preservação das 5 Seções Canônicas:** Ao desidratar um `SKILL.md` para `references/`, preserve os cabeçalhos obrigatórios do validador determinístico.
4. **Skills de terceiros são somente leitura:** Quando o relatório traz `third_party_source` (`npx skills`, `rea-agents`, plugin externo, Orca ou licença de fornecedor), nunca edite o frontmatter nem o corpo e não crie arquivos em `references/`.

