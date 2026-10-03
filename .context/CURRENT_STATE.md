# Estado Atual do Workspace: Franklin Quebra-Galho

> **Última Atualização**: 2026-10-03  
> **Nível de Persistência**: Nível 2 (Resumo de Contexto)  
> **Status Geral**: 🟢 100% Operacional e Conforme com a Governança 2026 (14/14 PASS)  

---

## 1. Visão Geral e Fase do Projeto
- **Repositório**: `c:\Users\melki\dev\franklin-quebragalho\`
- **Objetivo**: Incubadora central de automações de produtividade, runbooks e skills personalizadas do agente Franklin Quebra-Galho para o Google Antigravity.
- **Integração Global**: O diretório `.agents/skills/` está montado como Junction direta no plugin global do Antigravity (`~/.gemini/config/plugins/franklin-skills/skills`).
- **Fase**: Catálogo consolidado, auditoria determinística universal (14/14 aprovadas), espelhamento paritário estrito e reindexação AST concluída.

---

## 2. Catálogo Consolidado de Skills (15 Ativas - 100% PASS)

| Skill | Versão | Status | Paridade (`.agents` ➔ `skills/`) |
| :--- | :---: | :---: | :---: |
| `organizar-gdrive` | `v1.0.0` | ✅ Validada | ✅ Sincronizado |
| `organizar-local` | `v1.0.0` | ✅ Validada | ✅ Sincronizado |
| `gerar-docs-pdf` | `v1.0.0` | ✅ Validada | ✅ Sincronizado |
| `organizador-fluxo-arvore-arquivos` | `v1.1.0` | ✅ Validada | ✅ Sincronizado |
| `arquiteto-conteudo-solucoes` | `v2.2.0` | ✅ Validada | ✅ Sincronizado |
| `evoluir-skills` | `v1.1.0` | ✅ Validada | ✅ Sincronizado |
| `aprimoramento-expansibilidade-agentes-skills` | `v1.0.0` | ✅ Validada | ✅ Sincronizado |
| `arquitetura-design-implementacao-sistema` | `v1.1.0` | ✅ Validada | ✅ Sincronizado |
| `auditoria-projetos-sistema` | `v2.1.0` | ✅ Validada | ✅ Sincronizado |
| `consultor-design-tatil-frontend` | `v1.1.0` | ✅ Validada | ✅ Sincronizado |
| `context-sentinel` | `v1.0.0` | ✅ Validada | ✅ Sincronizado |
| `design-interface-medica-minimalista` | `v1.0.0` | ✅ Validada | ✅ Sincronizado |
| `skill-auditor-refatorador-skills` | `v1.1.0` | ✅ Validada | ✅ Sincronizado |
| `skill-orquestrador-planos-encadeados` | `v1.1.0` | ✅ Validada | ✅ Sincronizado |
| `_template` | `v1.2.0` | 🚀 Produção | ✅ Sincronizado |

---

## 3. Decisões Arquiteturais Vigentes
- **KISS & Local-First**: Priorização estrita do Google Drive montado nativamente em `G:\Meu Drive` e cmdlets do PowerShell 7, dispensando servidores HTTP mockados e stacks pesadas desnecessárias.
- **Divulgação Progressiva**: `SKILL.md` enxutos com documentação e critérios técnicos desacoplados em `references/`, `rules/` e `evals/`.
- **4 Módulos Canônicos de Design & Preferências Melki**: Implementados em 5 skills chave: (1) Paleta de Cores Canônica (Ardósia/Creme, acentos minerais, banimento anti-cobalto), (2) Design Tátil & Composição (Tactile Matte 4K, cards lighter than canvas, sombras multicamadas, rim light zenital, anti-squish), (3) Opções das Preferências (consulta via `ask_question`, 5 arquétipos canônicos e padrão shadcn/ui copy-paste) e (4) Matriz de Detecção de Discrepâncias com as Preferências (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).
- **Governança Determinística Falsificável**: Toda skill possui obrigatoriamente `rules/criterios_auditoria.md` com status `[PASS]`, `[FAIL]` e testes reais em `evals/evals.json`. Validação contínua via `python scripts/validate_skills.py`.
- **Caminhos Canônicos**: Todos os links internos utilizam esquema `file:///` referenciando `c:/Users/melki/dev/franklin-quebragalho/`.

---

## 4. Próximo Ponto de Entrada
- Catálogo 100% auditado (15/15 PASS), com módulos de design tátil e preferências perenes formalizados em todas as skills relevantes. Pronto para uso rotineiro.
