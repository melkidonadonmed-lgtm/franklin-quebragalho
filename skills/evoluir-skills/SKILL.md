---
name: evoluir-skills
description: >-
  Orquestrador mestre do ciclo de vida e pipeline de engenharia de skills do Franklin Quebra-Galho. Use quando o usuário pedir para criar uma nova skill a partir de uma ideia bruta, evoluir, homologar, testar (evals Baseline vs. Treatment e Trigger Matrix) ou versionar uma habilidade existente, encadeando automaticamente expansao-contexto-adaptativa, aprimoramento-expansibilidade-agentes-skills, skill-creator e skill-auditor-refatorador-skills. Não use para auditoria isolada de catálogo (use skill-auditor-refatorador-skills) nem para desenvolvimento de software sem relação com skills.
license: MIT
metadata:
  version: "2.0.0"
  author: "SkillCraft & Melki"
  category: "Engenharia e Governança de Skills"
  updated_at: "2026-10-14"
  tags:
    - "skills"
    - "evals"
    - "ciclo-de-vida"
    - "governanca"
    - "pipeline-skillcraft"
    - "progressive-disclosure"
version: 2.0.0
updated_at: 2026-10-14
author: SkillCraft & Melki
category: Engenharia e Governança de Skills
authorized_sub_skills:
  - name: expansao-contexto-adaptativa
    role: "Estágio 1 — Estruturação e desambiguação da ideia bruta da skill (CLAREZA/ReAct)"
  - name: aprimoramento-expansibilidade-agentes-skills
    role: "Estágio 2 — Consultoria de arquitetura (3 Tiers, Envelope Pattern, Context Forking, Evals/Pass@k)"
  - name: skill-creator
    role: "Estágio 3 — Scaffolding físico compatível com agentskills.io e _template"
  - name: skill-auditor-refatorador-skills
    role: "Estágio 4 — Auditoria determinística, validação dos 4 Módulos Táteis Melki e desacoplamento"
---

# Evolução e Orquestração do Ciclo de Vida de Skills (`evoluir-skills` v2.0.0) 🚀

Ponto de entrada (*Entrypoint*) e máquina de estados oficial da persona **`SkillCraft`** para conceber, estruturar, construir, avaliar empiricamente e homologar skills no Google Antigravity e no ecossistema Franklin Quebra-Galho.

---

## 🔗 Pipeline Encadeado Automático (`SkillCraft Chain`)

Para eliminar redundâncias entre skills de engenharia e impedir a criação de monólitos ("Parede de Complexidade"), toda execução da `evoluir-skills` segue obrigatoriamente esta esteira de 4 estágios:

```text
[Ideia Geral / Pedido Bruto do Usuário]
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ESTÁGIO 1 (Auto): expansao-contexto-adaptativa                              │
│ • Intercepta a ideia bruta, elimina ambiguidades e estrutura o escopo sob   │
│   CLAREZA + ReAct sem alterar a intenção original do desenvolvedor.         │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ESTÁGIO 2 (Consultivo): aprimoramento-expansibilidade-agentes-skills        │
│ • Define o Nível de Maturidade (1 a 4), a divisão em 3 Tiers (Catálogo,     │
│   Corpo <500 linhas, Referências/Scripts), Padrão Envelope (Action Routing),│
│   Context Forking e a arquitetura de métricas (Baseline vs. Treatment).     │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ESTÁGIO 3 (Construção): skill-creator + _template                           │
│ • Gera o scaffolding físico em .agents/skills/<slug>/ com SKILL.md enxuto   │
│   (Lean Instructions baseadas no "Porquê"), references/, rules/, scripts/   │
│   e evals/evals.json (incluindo Trigger Matrix should-trigger/near-misses). │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ESTÁGIO 4 (Auditoria & Release): skill-auditor-refatorador-skills           │
│ • Valida os 4 Módulos Táteis Melki (v2.6.0-2026), executa validate_skills.py│
│   ([PASS] 100%), espelha 1:1 em skills/<slug>/ e registra em MY_SKILLS.md.  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Criação de uma nova skill a partir de uma ideia geral, rascunho ou fluxo repetitivo identificado na sessão.
- Evolução de uma skill existente para incorporar novos recursos, scripts auxiliares ou métricas de avaliação (`evals.json`).
- Execução do ciclo de avaliação empírica (*Eval-Driven Iteration*): comparação *Baseline vs. Treatment* e calibração de gatilhos (`should-trigger` vs `should-not-trigger`).
- Atualização de versão semântica (SemVer), espelhamento paritário e registro de changelog no [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md).

---

## 🚫 Limites, Exceções e Quando NÃO Usar
- **Não usar** para auditoria estática em lote de todo o catálogo ou desacoplamento cirúrgico de monólitos já existentes sem criação de fluxo novo (delegue diretamente para `skill-auditor-refatorador-skills`).
- **Não usar** quando o pedido for exclusivamente arquitetura de código multiagente em Python/TypeScript no Google ADK ou LangGraph sem criação de pacote de skill (use diretamente `aprimoramento-expansibilidade-agentes-skills`).
- **Não usar** para desenvolvimento de software de domínio geral que não constitua uma habilidade reutilizável do agente.

---

## 📥 Entradas Obrigatórias e Pré-requisitos
1. **Intenção ou Ideia Geral**: Descrição bruta do procedimento, automação ou habilidade desejada (mesmo que incompleta — será expandida no Estágio 1).
2. **Slug da Skill (ou sugestão automática)**: Identificador em minúsculas separado por hífens (`a-z0-9-`, máx. 64 caracteres), idêntico ao nome da pasta.
3. **Escopo de Ferramentas e Risco**: Definição se a skill é *Read-Only*, mutação reversível ou requer portão *Human-in-the-Loop (HITL)*.

---

## 🔄 Fluxo Passo a Passo de Execução (Padrão 2026)

### Passo 1: Expansão Adaptativa da Ideia (`expansao-contexto-adaptativa`)
- Aplique o motor de expansão sobre o pedido bruto para extrair:
  - **Propósito central** e fronteiras de atuação (o que faz e o que não faz).
  - **Gatilhos de ativação** explícitos e casos limítrofes (*near-misses*).
  - **Entradas, processamento e contrato de saída**.

### Passo 2: Dimensionamento de Expansibilidade e Qualidade (`aprimoramento-expansibilidade-agentes-skills`)
Consulte os parâmetros arquiteturais da `aprimoramento-expansibilidade-agentes-skills` para estruturar a skill sob 5 pilares:
1. **Divulgação Progressiva em 3 Tiers**:
   - *Tier 1 (Catálogo)*: `name` + `description` em 3ª pessoa (~50–100 tokens, $\le 1024$ chars) com palavras-chave de disparo e exclusão.
   - *Tier 2 (Ativação)*: Corpo do `SKILL.md` estritamente enxuto ($< 500$ linhas / $< 5.000$ tokens), preservando a densidade atencional (Softmax).
   - *Tier 3 (Execução sob demanda)*: Tabelas extensas, schemas JSON/Pydantic e manuais alocados em `references/` e carregados apenas quando necessário.
2. **Instruções Enxutas (*Lean Instructions*) e o "Porquê"**:
   - Substitua regras imperativas cegas e repetitivas ("SEMPRE faça X") por instruções causais enxutas ("Faça X porque Y previne Z"), evitando *over-constraining* do modelo.
3. **Extração de Lógica Repetitiva para `scripts/`**:
   - Se a tarefa exigir parsing determinístico, cálculos, varredura de disco ou validação mecânica que o agente reescreveria a cada turno, empacote como script executável em `scripts/` (Python via `uv` ou PowerShell 7 `pwsh`).
4. **Padrão Envelope (*Action Routing*) e Context Forking**:
   - Se a skill cobrir múltiplas ações correlatas, exponha um contrato Envelope (`action` + `params`) em vez de criar dezenas de micro-skills fragmentadas.
   - Se a execução envolver varredura pesada ou tentativa-e-erro longa, recomende bifurcação em subagente isolado (`context: fork` / `invoke_subagent`) para não poluir a thread principal.
5. **Engenharia de Avaliação (*Eval-Driven Iteration*)**:
   - Desenhe `evals/evals.json` para suportar comparação *Baseline vs. Treatment* (com/sem skill) e matriz de gatilhos (`should-trigger` vs `should-not-trigger`).

### Passo 3: Scaffolding e Redação Canônica (`skill-creator` + `_template`)
Crie a estrutura física em `.agents/skills/<nome-da-skill>/`:
```text
.agents/skills/<nome-da-skill>/
├── SKILL.md                   # Tier 1 (YAML) + Tier 2 (Fluxo decisório enxuto < 500 linhas)
├── references/                # Tier 3: Conhecimento factual imutável, tabelas e schemas
├── rules/
│   └── criterios_auditoria.md # Regras booleanas falsificáveis ([PASS], [FAIL], [UNVERIFIED])
├── scripts/                   # Utilitários determinísticos (Python/PowerShell)
└── evals/
    └── evals.json             # Casos de teste funcionais + Trigger Eval Queries
```
- Se a skill envolver UI/UX, HTML, relatórios visuais ou frontend, injete obrigatoriamente os **4 Módulos Táteis Melki (`v2.6.0-2026`)** conforme o `_template`.

### Passo 4: Auditoria Determinística, Espelhamento e Homologação (`skill-auditor-refatorador-skills`)
1. **Espelhamento Paritário**: Copie fisicamente `.agents/skills/<nome-da-skill>/` para `skills/<nome-da-skill>/` (nunca use junctions/symlinks `d----l` em diretórios globais de skills).
2. **Validação Automatizada**: Execute no terminal:
   ```powershell
   uv run python scripts/validate_skills.py --targets <nome-da-skill>
   ```
3. **Governança do Catálogo**: Atualize [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md) com o status (`💡 Ideia`, `🧪 Em Teste`, `✅ Validada`, `🚀 Produção`), versão SemVer e entrada detalhada no Changelog.

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
Toda execução de `evoluir-skills` deve entregar:
1. **Resumo do Pipeline Encadeado**: Síntese das decisões tomadas nos Estágios 1 (Expansão) e 2 (Arquitetura/Tiers).
2. **Artefatos Físicos Criados/Atualizados**: Links clicáveis `file:///` para `SKILL.md`, `rules/criterios_auditoria.md`, `evals/evals.json` e `references/` ou `scripts/`.
3. **Relatório Determinístico de Validação**: Saída comprovada do `scripts/validate_skills.py` com código de retorno `0` (`[PASS]`) e confirmação do espelhamento em `skills/<nome-da-skill>/`.
4. **Registro de Governança**: Confirmação da atualização de versão e histórico em [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md).
