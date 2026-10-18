---
name: evoluir-skills
description: >-
  Orquestrador de construção e evolução funcional de skills (Forward Builder & TDD). Use quando o usuário pedir para criar uma nova skill a partir de uma ideia bruta, adicionar novas funcionalidades/scripts a uma skill existente ou configurar sua suíte de avaliação empírica (evals/evals.json e Trigger Matrix). Não use para auditoria de catálogo, desacoplamento de monólitos ou refatoração estrutural de skills inchadas (use skill-auditor-refatorador-skills) nem para arquitetura de código multiagente ADK/MCP (use aprimoramento-expansibilidade-agentes-skills).
license: MIT
metadata:
  version: "2.1.0"
  author: "SkillCraft & Melki"
  category: "Engenharia e Governança de Skills"
  updated_at: "2026-10-17"
  tags:
    - "skills"
    - "tdd-skills"
    - "forward-builder"
    - "evals"
    - "progressive-disclosure"
version: 2.1.0
updated_at: 2026-10-17
author: SkillCraft & Melki
category: Engenharia e Governança de Skills
authorized_sub_skills:
  - name: expansao-contexto-adaptativa
    role: "Estágio 1 — Desambiguação e estruturação da ideia bruta da skill (CLAREZA/ReAct)"
  - name: skill-creator
    role: "Estágio 2 — Referência de especificação agentskills.io para scaffolding físico"
  - name: skill-auditor-refatorador-skills
    role: "Estágio 3 — Homologação final caso a skill exija desacoplamento ou auditoria dos 4 Módulos Táteis Melki"
---

# Construção e Evolução Funcional de Skills (`evoluir-skills` v2.1.0) 🚀

Motor **Forward Builder & TDD** da esteira `SkillCraft`. Seu papel exclusivo é transformar uma **ideia bruta** ou **novo requisito funcional** em um pacote de skill enxuto, testado deterministicamente pelo harness em Go (`dispatch_skill_deterministic_tests`) e homologado em `skills/<slug>/`.

---

## 🔗 Fronteira de Responsabilidade (Zero Sobreposição)

| Intenção do Pedido | Skill Responsável |
| :--- | :--- |
| **Criar skill do zero** ou **adicionar feature/script** a uma skill existente | **`evoluir-skills`** *(esta skill)* |
| **Enxugar monólito (`> 500` linhas)**, extrair código repetitivo de `transcript.jsonl`, corrigir gatilhos ou auditar catálogo | **`skill-auditor-refatorador-skills`** |
| **Projetar arquitetura de código de agentes** (Google ADK Go/Py/TS, MCP, A2A, Circuit Breaker, Theranostic Pipeline) | **`aprimoramento-expansibilidade-agentes-skills`** |

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Criar uma nova skill a partir de uma ideia, prompt recorrente ou fluxo de trabalho identificado na sessão.
- Evoluir uma skill existente adicionando novos parâmetros, scripts utilitários (`scripts/`) ou casos de avaliação (`evals/evals.json`).
- Configurar e executar pela primeira vez os testes determinísticos A vs B (`Pass@1`, `Pass@3`, `TEI`) de uma skill.

## 🚫 Quando NÃO Usar
- **Não usar** para auditar o catálogo existente ou dividir uma skill monolítica em sub-skills (delegue para `skill-auditor-refatorador-skills`).
- **Não usar** para arquitetar agentes em código Python/Go/TypeScript sem criação de pacote `SKILL.md` (delegue para `aprimoramento-expansibilidade-agentes-skills`).

---

## 🔄 Fluxo de Execução em 3 Passos (Forward Builder)

### Passo 1: Desambiguação e Contrato de Intenção (`expansao-contexto-adaptativa`)
Extraia do pedido bruto:
1. **Slug canônico**: `a-z0-9-` (máx. 64 caracteres), idêntico ao nome do diretório.
2. **Fronteira de Ativação (Tier 1)**:
   - `description` em 3ª pessoa ($\le 1024$ caracteres) declarando explicitamente **quando usar** e **quando NÃO usar** (*near-misses* para evitar colisão de Softmax com skills vizinhas).
3. **Separação Cognitivo vs. Determinístico**:
   - O que exige julgamento contextual fica nas instruções do `SKILL.md` (Tier 2, $< 500$ linhas, escrito com foco causal no *"Porquê"* e sem regras maiúsculas redundantes).
   - O que for tabela estática ou schema extenso vai para `references/` (Tier 3).
   - O que for cálculo, validação mecânica ou comando repetitivo vai para `scripts/` ou tools MCP (`agy_deterministic_calc_suite`).

### Passo 2: Scaffolding Físico Canônico
Gere ou atualize a árvore física em `.agents/skills/<slug>/`:

```text
.agents/skills/<slug>/
├── SKILL.md                   # Tier 1 (YAML) + Tier 2 (Fluxo enxuto < 500 linhas)
├── references/                # Tier 3: Tabelas, schemas JSON/Pydantic (lidos sob demanda)
├── rules/
│   └── criterios_auditoria.md # Regras falsificáveis ([PASS], [FAIL], [UNVERIFIED])
├── scripts/                   # Scripts determinísticos (Python uv / PowerShell pwsh)
└── evals/
    └── evals.json             # Casos funcionais + trigger_eval_queries (should/should_not)
```

> [!IMPORTANT]
> Se a skill gerar interfaces, HTML/CSS ou relatórios visuais, inclua a referência aos **4 Módulos Táteis Melki (`v2.6.0-2026`)** conforme o `_template` e valide com `skill-auditor-refatorador-skills`.

### Passo 3: Despacho Determinístico de Testes (`adk-go-mcp`) e Espelhamento
1. **Despacho para o Harness Determinístico em Go**:
   - Invoque a tool MCP **`dispatch_skill_deterministic_tests`** (servidor `adk-go-mcp`) com:
     - `skill_target`: `"<slug>"`
     - `action`: `"configure_and_run"`
   - O subagente Go `skill_deterministic_test_dispatcher` criará/validará `evals/evals.json` e `rules/criterios_auditoria.md`, auditará o limite de `< 500` linhas e executará o benchmark concorrente A vs B (`Pass@1`, `Pass@3`, `Paired t-Stat`, `TEI`).
   - Se a skill envolver cálculos matemáticos/clínicos/financeiros, valide os casos de referência com **`agy_deterministic_calc_suite`**.
2. **Espelhamento Físico Paritário**:
   - Copie fisicamente `.agents/skills/<slug>/` para `skills/<slug>/` (e para `.gemini/config/plugins/franklin-skills/skills/<slug>/` quando aplicável). Nunca use symlinks/junctions (`d----l`).
3. **Validador do Repositório e Catálogo**:
   - Execute `uv run python scripts/validate_skills.py --targets <slug>` no repositório `franklin-quebragalho` e registre a versão SemVer no [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md).

---

## 📤 Entregáveis Obrigatórios
1. **Arquivos Criados/Atualizados**: Links clicáveis `file:///` para `SKILL.md`, `evals/evals.json`, `rules/criterios_auditoria.md` e `scripts/` ou `references/`.
2. **Telemetria Determinística (`dispatch_skill_deterministic_tests`)**: Resultado `[PASS]` do Eval Harness A vs B (`Pass@1`, `Pass@3`, `TEI`) + `validate_skills.py`.
3. **Sincronia**: Confirmação da cópia física em `skills/<slug>/` e atualização do `MY_SKILLS.md`.
