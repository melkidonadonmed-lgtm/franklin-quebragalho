# Estado Atual do Workspace: Franklin Quebra-Galho

> **Última Atualização**: 2026-10-04  
> **Nível de Persistência**: Nível 2 (Resumo de Contexto)  
> **Status Geral**: 🟢 100% Operacional e Conforme com a Governança 2026 (26/26 PASS + Template Universal Ativo)  

---

## 1. Visão Geral e Fase do Projeto
- **Repositório**: `c:\Users\melki\dev\franklin-quebragalho\`
- **Objetivo**: Incubadora central de automações de produtividade, runbooks e skills personalizadas do agente Franklin Quebra-Galho para o Google Antigravity.
- **Integração Global**: O diretório `.agents/skills/` está montado como NTFS Junction direta no plugin global do Antigravity (`~/.gemini/config/plugins/franklin-skills/skills`).
- **Fase**: Fases 1, 2 e 3 de modularização concluídas com sucesso (26 skills canônicas). Arquitetura Universal de Projetos Melki 2026 implementada em `templates/universal-app/` com o documento canônico `docs/frontend.design.md` (Design System Tátil, fórmulas multi-sombra CSS e Canvas 2D, paletas minerais e few-shot prompts). Scaffolder automatizado em PowerShell (`scripts/scaffold-universal-app.ps1`) validado empiricamente. Reindexação AST concluída (306 arquivos, Tree Hash `daebbcd930a4abbe`).

---

## 2. Catálogo Consolidado de Skills (26 Ativas - 100% PASS)

| Skill | Versão | Status | Paridade (`.agents` ➔ `skills/`) | Subagente Operador |
| :--- | :---: | :---: | :---: | :--- |
| `redator-tecnico-markdown` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `DocMaker` / `VaultMaster` |
| `conversor-html-pdf` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `DocMaker` |
| `gdrive-auditoria-limpeza` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `DriveMaster` |
| `gdrive-taxonomia-organizacao` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `DriveMaster` |
| `manutencao-disco-windows` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `FileOpsLocal` |
| `curadoria-obsidian-vault` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `VaultMaster` |
| `analise-design-tatil-frontend` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `FrontCraftMaster` |
| `refatoracao-design-tatil-frontend` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `FrontCraftMaster` |
| `high-level-context-planner` | `v2.0.0` | ✅ Validada | ✅ Sincronizado | `LoopPlanner` |
| `skill-orquestrador-planos-encadeados` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `LoopPlanner` |
| `gap-analyzer-auditor` | `v2.0.0` | ✅ Validada | ✅ Sincronizado | `LoopPlanner` |
| `gerar-docs-pdf` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | *(Legado / Transição)* |
| `organizar-gdrive` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | *(Legado / Transição)* |
| `organizar-local` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | *(Legado / Transição)* |
| `consultor-design-tatil-frontend` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | *(Legado / Transição)* |
| `organizador-fluxo-arvore-arquivos` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `DocMaker` |
| `arquiteto-conteudo-solucoes` | `v2.2.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `evoluir-skills` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `SkillCraft` |
| `skill-auditor-refatorador-skills` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `SkillCraft` |
| `aprimoramento-expansibilidade-agentes-skills` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `SkillCraft` |
| `arquitetura-design-implementacao-sistema` | `v1.1.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `auditoria-projetos-sistema` | `v2.1.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `context-sentinel` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `design-interface-medica-minimalista` | `v1.0.0` | ✅ Validada | ✅ Sincronizado | `FrontCraftMaster` |
| `refine-prompt` | `v3.0.0` | ✅ Validada | ✅ Sincronizado | `Franklin-Main` |
| `_template` | `v1.2.0` | 🚀 Produção | ✅ Sincronizado | Base Padrão 2026 |

---

## 3. Decisões Arquiteturais Vigentes
- **KISS & Local-First**: Operações diretas no SO, scripts nativos em PowerShell (`pwsh`) e browser headless nativo (`msedge.exe`).
- **Arquitetura Universal de Projetos**: Template modular residente em `templates/universal-app/` integrando Vite, React, TypeScript no modo estrito e Tailwind CSS com Design System Tátil.
- **Motor Multi-Sombra Canvas 2D**: Pipeline de dupla passagem (`ctx.shadowBlur` 18px e 4px) com rim light zenital de 1px garantindo gráficos táteis nítidos.
- **Divulgação Progressiva**: `SKILL.md` enxutos com referências em `references/`, regras em `rules/` e asserções reais em `evals/`.
- **Governança Determinística Falsificável**: 100% das 26 skills possuem validação por asserções booleanas `[PASS]` e `[FAIL]`.

---

## 4. Próximo Ponto de Entrada
- Base universal e script `scripts/scaffold-universal-app.ps1` homologados.
- Para provisionar um novo projeto: `.\scripts\scaffold-universal-app.ps1 -ProjectName "nome-do-app"`.
- Repositório pronto para commit Git.
