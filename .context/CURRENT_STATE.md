# Estado Atual do Workspace: Franklin Quebra-Galho

> **Última Atualização**: 2026-10-04  
> **Nível de Persistência**: Nível 2 (Resumo de Contexto)  
> **Status Geral**: 🟢 100% Operacional e Conforme com a Governança 2026 (26/26 PASS)  

---

## 1. Visão Geral e Fase do Projeto
- **Repositório**: `c:\Users\melki\dev\franklin-quebragalho\`
- **Objetivo**: Incubadora central de automações de produtividade, runbooks e skills personalizadas do agente Franklin Quebra-Galho para o Google Antigravity.
- **Integração Global**: O diretório `.agents/skills/` está montado como NTFS Junction direta no plugin global do Antigravity (`~/.gemini/config/plugins/franklin-skills/skills`).
- **Fase**: Fases 1, 2 e 3 de modularização concluídas com sucesso. Catálogo consolidado em 26 skills canônicas com 100% de aprovação no `validate_skills.py`. Desacoplados os monólitos de frontend, Google Drive, sistema local e documentação/conversão PDF. Subagentes especializados plenamente mapeados. Reindexação AST concluída (280 arquivos, Tree Hash `cf8d5fe6923e1fe8`).

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
- **KISS & Local-First**: Operações diretas no SO e browser headless nativo (`msedge.exe`), eliminando dependências pesadas de terceiros (Pandoc, wkhtmltopdf).
- **Desacoplamento Cirúrgico em 3 Fases**:
  * Fase 1: Frontend dividido em Análise (Read-Only) e Refatoração (Write por framework).
  * Fase 2: Storage dividido em Auditoria/Limpeza (pesados e quarentena) vs. Taxonomia (estrutura e datas ISO); e SO local vs. PKM Obsidian Vault.
  * Fase 3: Documentação dividida em Redação Estruturada Markdown vs. Pipeline de Impressão Headless em PDF.
- **Divulgação Progressiva**: `SKILL.md` enxutos com metadados claros, referências em `references/`, regras determinísticas em `rules/` e asserções reais em `evals/`.
- **Governança Determinística Falsificável**: 100% das 26 skills possuem validação por asserções booleanas `[PASS]` e `[FAIL]`.

---

## 4. Próximo Ponto de Entrada
- Fases 1, 2 e 3 100% concluídas e validadas (26/26 PASS).
- Todos os monólitos foram substituídos por pares modulares de alta precisão.
- Repositório pronto para consolidação e commit.
