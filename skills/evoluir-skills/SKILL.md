---
name: evoluir-skills
description: >-
  Orquestrador de construção e evolução funcional de skills (Forward Builder & TDD). Use quando o usuário pedir para criar uma nova skill a partir de uma ideia bruta, adicionar funcionalidades/scripts a uma skill existente ou configurar sua suíte evals/evals.json. Não use para auditoria ou desacoplamento de monólitos (use skill-auditor-refatorador-skills) nem para arquitetura de código ADK/MCP (use aprimoramento-expansibilidade-agentes-skills).
license: MIT
metadata:
  version: "2.2.0"
  author: "SkillCraft & Melki"
  category: "Engenharia e Governança de Skills"
  updated_at: "2026-10-19"
  tags:
    - "skills"
    - "tdd-skills"
    - "forward-builder"
    - "evals"
    - "progressive-disclosure"
version: 2.2.0
updated_at: 2026-10-19
author: SkillCraft & Melki
category: "Engenharia e Governança de Skills"
authorized_sub_skills:
  - name: expansao-contexto-adaptativa
    role: "Passo 1 — Desambiguação e estruturação da ideia bruta da skill por nível (RTF / CARE / CLAREZA)"
  - name: skill-creator
    role: "Passo 2 — Scaffolding físico via especificação agentskills.io e _template v2.0.0"
  - name: skill-auditor-refatorador-skills
    role: "Passo 3 — Homologação determinística contra os 5 Eixos e Módulos M1..M7"
---

# Construção e Evolução Funcional de Skills (`evoluir-skills` v2.2.0) 🚀

Motor **Forward Builder & TDD** da esteira `SkillCraft`. Seu papel exclusivo é transformar uma **ideia bruta** ou **novo requisito funcional** em um pacote de skill enxuto, modular e homologado sem duplicar regras já existentes no `_template`.

---

## 🔗 Fronteira de Responsabilidade (Zero Sobreposição)

| Intenção do Pedido | Skill Canônica Responsável (SSOT) |
| :--- | :--- |
| **Criar skill do zero** ou **adicionar feature/script** a uma skill existente | **`evoluir-skills`** *(esta skill)* |
| **Enxugar monólito (`> 500` linhas)**, extrair código repetitivo de `transcript.jsonl`, corrigir gatilhos ou auditar catálogo | **`skill-auditor-refatorador-skills`** |
| **Projetar arquitetura de código de agentes, tools Pydantic, frameworks e métricas ($\text{Pass}@k$, $\text{TEI}$)** | **`aprimoramento-expansibilidade-agentes-skills`** |
| **Refinar prompts avulsos com auditoria epistêmica Zero-Trust (`[FATO]/[INFERÊNCIA]/[LACUNA]`)** | **`refine-prompt`** |

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Criar uma nova skill a partir de uma ideia, prompt recorrente ou fluxo de trabalho identificado na sessão.
- Evoluir uma skill existente adicionando novos parâmetros, scripts utilitários (`scripts/`) ou casos de avaliação (`evals/evals.json`).
- Configurar e executar pela primeira vez os testes determinísticos A vs B (`Pass@1`, `Pass@3`, `TEI`) de uma skill.

## 🚫 Quando NÃO Usar
- **Não usar** para auditar o catálogo existente ou dividir uma skill monolítica em sub-skills (delegue para `skill-auditor-refatorador-skills`).
- **Não usar** para arquitetar agentes em código Python/Go/TypeScript sem criação de pacote `SKILL.md` (delegue para `aprimoramento-expansibilidade-agentes-skills`).

---

## 📥 Entradas e Pré-requisitos
- `skill_idea_or_slug` (obrigatório): Descrição da ideia bruta ou nome (`slug` em `kebab-case <= 64` chars) da skill a evoluir.
- `domain_module` (opcional): Módulo de domínio (`M1` Código/Automação, `M2` Design, `M3` Frontend/UI, `M4` Pesquisa/RAG, `M5` Imagem, `M6` Vídeo, `M7` Saúde/Clínica).

---

## 🔄 Fluxo de Execução em 3 Passos (Forward Builder)

### Passo 1: Desambiguação, Contrato de Intenção e Seleção de Módulo (`expansao-contexto-adaptativa`)
Extraia do pedido bruto:
1. **Slug canônico**: `^[a-z0-9]+(-[a-z0-9]+)*$` (máx. 64 caracteres), idêntico ao nome do diretório.
2. **Fronteira de Ativação (Tier 1)**:
   - `description` em 3ª pessoa ($\le 300$ chars recomendado, máx. 1024) declarando explicitamente **quando usar** e **quando NÃO usar** (*near-misses* para evitar colisão de Softmax com skills vizinhas).
3. **Seleção do Módulo de Domínio (`M1`..`M7` sem Redundância)**:
   - Consulte [`skills/_template/references/guardrails_por_modulo.md`](../_template/references/guardrails_por_modulo.md) e selecione **apenas** o módulo pertinente (`M1` a `M7`).
   - Se for `M3` (Frontend/UI), referencie os 4 Módulos Táteis Melki (`DESIGN.md v4.5-soft`) de `_template/references/paleta_estilo_melki.md` sem copiar tabelas inteiras de cores para o `SKILL.md`.
4. **Separação Cognitivo vs. Determinístico**:
   - Julgamento contextual, fluxo e *Gotchas* ficam no `SKILL.md` (Tier 2, $< 500$ linhas, focado no *"Porquê"*).
   - Tabelas estáticas e schemas extensos vão para `references/` (Tier 3).
   - Cálculos, parsers e validações mecânicas vão para `scripts/` (`<= 300` linhas, tipados com Pydantic `extra="forbid"`, sem `input()` interativo e com `stdout` separado de `stderr`).

### Passo 2: Scaffolding Físico Canônico (`_template` v2.0.0)
Gere ou atualize a árvore física em `skills/<slug>/`:

```text
skills/<slug>/
├── SKILL.md                   # Tier 1 (YAML) + Tier 2 (9 perguntas + Gotchas + Orçamento < 500 linhas)
├── references/                # Tier 3: Tabelas, schemas JSON/Pydantic carregados sob demanda
├── rules/
│   └── criterios_auditoria.md # Regras falsificáveis ([PASS], [FAIL], [UNVERIFIED])
├── scripts/                   # Scripts determinísticos testados (Python uv / PowerShell pwsh)
└── evals/
    └── evals.json             # Casos funcionais + Trigger Matrix (should_trigger / should_not_trigger)
```

### Passo 3: Homologação Determinística, Testes (`adk-go-mcp`) e Sincronização
1. **Despacho para o Harness Determinístico (quando disponível)**:
   - Invoque `dispatch_skill_deterministic_tests` (`skill_target: "<slug>"`, `action: "configure_and_run"`) ou execute a validação local para aferir `Pass@1`, `Pass@3` e `TEI`.
   - Para scripts Python criados em `scripts/`, execute o `code_acceptability_auditor.py` garantindo `Quality Score >= 75/100`.
2. **Validação e Sincronização Física do Ecossistema**:
   - Execute `uv run python scripts/validate_skills.py --targets <slug>` e `uv run python scripts/sync_gemini_ecosystem.py` (cópias físicas sem symlinks/junctions) e atualize o [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md).

---

## 🛡️ Exceções, Limites e Armadilhas (*Gotchas*)
- **Zero Duplicação de Catálogo**: Nunca incorpore o texto integral de outra skill dentro da nova skill; use `authorized_sub_skills` no frontmatter para encadeamento.
- **Prevenção de *Overfitting* na Descrição**: Ao calibrar a `description` com base em falhas de gatilho, preserve a generalização (divisão conceitual 70% treino / 30% validação) em vez de colar palavras literais do prompt de teste.

---

## 📤 Entregáveis Obrigatórios
1. **Arquivos Criados/Atualizados**: Links clicáveis `file:///` para `SKILL.md`, `evals/evals.json`, `rules/criterios_auditoria.md` e `scripts/` ou `references/`.
2. **Comprovação Determinística**: Resultado `[PASS]` de `validate_skills.py` (e `code_acceptability_auditor.py` quando houver scripts Python).
3. **Sincronia**: Confirmação de atualização do `MY_SKILLS.md` e espelhamento via `sync_gemini_ecosystem.py`.
