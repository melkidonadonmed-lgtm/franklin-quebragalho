---
trigger: model_decision
description: "Diretrizes oficiais do Google Antigravity para criar, refatorar ou validar Agent Skills (SKILL.md, Progressive Disclosure L1-L3, references/, evals/ e frontmatter YAML)."
---

# Regras Oficiais para Criação de Agent Skills (Antigravity / AgentSkills.io)

1. **Descoberta e Escopo Canônico:**
   - Workspace: `.agents/skills/<skill-name>/SKILL.md` (ou `_agents/skills/`); prefira skills em vez do formato legado `.agents/workflows/*.md` (depreciado no Antigravity 2.12+).
   - Global/Plugin: `~/.gemini/config/skills/<skill-name>/SKILL.md` ou `plugins/<plugin>/skills/<skill-name>/SKILL.md` (use `skills.json` com `entries`/`inherits` apenas para diretórios fora do padrão).

2. **Frontmatter YAML Estrito (L1 — Descoberta Semântica):**
   - Apenas **`name`** (obrigatório, minúsculas `[a-z0-9-]`, `<= 64` chars, **idêntico ao nome da pasta**) e **`description`** (obrigatório, em 3ª pessoa, declarando **O QUE** faz, **QUANDO** usar e **limite negativo** "Não use para... / Do not use for...").
   - Sempre envolva `description` com aspas (`"..."`) ou bloco dobrado (`>-`) se houver `: ` para evitar quebra de parser PyYAML.
   - Campos opcionais aceitos: `compatibility`, `license` e `metadata:` (`version`, `updated_at`, `author`, `category`, `tags`). **Proibido duplicar** `version`, `updated_at` ou `allowed-tools` no topo quando `metadata:` estiver presente (`validate_skills.py --strict` reprova chaves órfãs no topo).

3. **Progressive Disclosure em 3 Camadas (L1 $\to$ L2 $\to$ L3):**
   - **L2 (`SKILL.md`):** Mantenha o corpo conciso (`<= 1.200` tokens totais no arquivo, idealmente `< 1.000`, `< 500` linhas) e focado em passos executáveis únicos — sem duplicar guias gerais de codificação.
   - **L3 (`references/`, `scripts/`, `examples/`, `resources/`):** Descarregue tabelas densas, diagramas, templates e matrizes para `references/*.md` (links relativos de 1 nível `[arquivo](references/doc.md)` verificáveis em disco) e encapsule verificações determinísticas em `scripts/`.
   - **Estrutura Canônica Franklin (29 Skills Core):** Preserve as 5 seções validadas (`Gatilhos / Quando Usar`, `Entradas / Pré-requisitos`, `Processamento / Fluxo`, `Saídas / Entregáveis`, `Exceções / Limites`).
   - **Skills de Terceiros (`npx skills`, Orca, plugins externos):** Nunca edite frontmatter, corpo ou `references/` localmente; atualize pelo instalador de origem.

4. **Evals e Portões de Validação Antes de Concluir:**
   - Inclua `evals/evals.json` (`{"skill_name": "...", "evals": [...]}`) com casos positivos (`should_trigger: true`) e negativos próximos (`should_trigger: false`).
   - Valide fisicamente antes de declarar pronto: `validate_skills.py --ecosystem` e `go run skills/audit-skills-antigravity/scripts/skill_auditor_rea.go` (`100/100`, 0 `broken_refs`, 0 colisões e sem vazamento CSS/OKLCH em skills não-visuais).
