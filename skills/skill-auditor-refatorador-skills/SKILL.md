---
name: skill-auditor-refatorador-skills
description: >-
  Cirurgião estrutural, desacoplador de monólitos e auditor determinístico de catálogo de skills. Use quando o usuário pedir para auditar skills existentes, enxugar uma skill acima de 500 linhas (movendo tabelas para references/ e código repetitivo de transcript.jsonl para scripts/), dividir uma skill monolítica em sub-skills, calibrar gatilhos com falsos positivos/negativos ou auditar os 4 Módulos Táteis Melki (v2.6.0-2026) nas skills de UI. Não use para criar uma skill nova do zero a partir de uma ideia bruta (use evoluir-skills).
license: MIT
metadata:
  version: "2.0.0"
  author: "SkillCraft & Melki"
  category: "Governança, Desacoplamento e Auditoria de Skills"
  updated_at: "2026-10-17"
  tags:
    - "auditoria-skills"
    - "refatoracao-cirurgica"
    - "desacoplamento"
    - "trigger-matrix"
    - "design-tatil-2026"
version: 2.0.0
updated_at: 2026-10-17
author: SkillCraft & Melki
category: Governança, Desacoplamento e Auditoria de Skills
authorized_sub_skills:
  - name: skill-orquestrador-planos-encadeados
    role: "Atualização das rotas de hand-off quando um monólito é dividido em sub-skills"
---

# Cirurgia Estrutural e Auditoria Determinística de Skills (`skill-auditor-refatorador-skills` v2.0.0) 🛡️

Motor de **Diagnóstico, Desacoplamento Cirúrgico e Cura de Catálogo**. Não cria skills do zero (papel da `evoluir-skills`) nem projeta arquiteturas de código ADK/MCP (papel da `aprimoramento-expansibilidade-agentes-skills`): atua exclusivamente na **inspeção determinística, redução de entropia, extração de scripts/referências e eliminação de redundâncias entre skills**.

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Auditar uma skill ou todo o catálogo em busca de violações dos 3 Tiers (`SKILL.md > 500` linhas), ausência de `evals/evals.json` ou conflito de gatilhos (*overlapping descriptions*).
- Refatorar e enxugar uma skill inchada: extrair blocos estáticos para `references/` (Tier 3) e comandos/parsers repetitivos detectados em `transcript.jsonl` para `scripts/`.
- Dividir uma skill monolítica (que mistura múltiplos domínios cognitivos) em skills independentes e ortogonais.
- Auditar conformidade de skills de Frontend/UI com os **4 Módulos Táteis Melki (`v2.6.0-2026`)**.

## 🚫 Quando NÃO Usar
- **Não usar** para criar uma skill nova a partir de uma ideia bruta (use `evoluir-skills`).
- **Não usar** para arquitetar código de agentes em Go, Python ou TypeScript (use `aprimoramento-expansibilidade-agentes-skills`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `skill_target` (obrigatório): Nome/slug da skill ou caminho do diretório a ser auditado/refatorado.
- `audit_mode` (opcional): `diagnostic_only` (somente diagnóstico `[PASS]`/`[FAIL]`) ou `apply_refactoring` (aplica o enxugamento, extrai `references/` e `scripts/`, espelha e atualiza o `MY_SKILLS.md`).
- `transcript_log_path` (opcional): Caminho de `transcript.jsonl` para identificar comandos ou parsers repetitivos que devem migrar para `scripts/`.

---

## ⚙️ Fluxo Cirúrgico em 4 Etapas

### Etapa 1: Diagnóstico Determinístico Zero-LLM (`adk-go-mcp` + `validate_skills.py`)
Nunca faça contagem manual de linhas ou inspeção visual de JSON antes de acionar os motores determinísticos:
1. Invoque a tool MCP **`dispatch_skill_deterministic_tests`** (`action: "run_only"` ou `"configure_and_run"`) para a skill alvo:
   - Obtém em microssegundos: validade do frontmatter YAML, contagem exata de linhas do `SKILL.md` (`tier2_under_500`) e resultado do Eval Harness A vs B (`Pass@1`, `Pass@3`, `Paired t-Stat`, `TEI`).
2. Para auditoria em lote do repositório, execute:
   ```powershell
   uv run python scripts/validate_skills.py
   ```

### Etapa 2: Cirurgia de Desacoplamento e Enxugamento (3 Tiers)
Com base nas falhas apontadas na Etapa 1, aplique as 4 operações cirúrgicas:
1. **Cura de Colisão de Gatilhos (Tier 1)**:
   - Compare a `description` das skills semanticamente próximas.
   - Adicione cláusulas explícitas `"Use quando..."` e `"Não use para X (use skill-Y)"`, calibrando `trigger_eval_queries` (`should_trigger` vs `should_not_trigger` com *near-misses*) em `evals/evals.json`.
2. **Desidratação de Tier 2 (`SKILL.md < 500` linhas)**:
   - Remova listas repetitivas de regras em caixa alta e explicações teóricas duplicadas.
   - Mova tabelas extensas, templates longos e schemas JSON/Pydantic para `references/<arquivo>.md` (Tier 3) com link relativo.
3. **Extração de Trajetórias Repetitivas para `scripts/`**:
   - Se `transcript.jsonl` ou o corpo da skill mostrar que o agente reescreve o mesmo parser/comando em runtime, extraia para um script parametrizado em `scripts/` e substitua no `SKILL.md` por uma única linha de invocação.
4. **Fissão de Monólitos**:
   - Se a skill mistura domínios conflitantes (ex.: *Diagnóstico Read-Only* + *Refatoração Destrutiva*), separe conforme [`references/matriz_desacoplamento.md`](references/matriz_desacoplamento.md).

### Etapa 3: Auditoria dos 4 Módulos Táteis Melki (`v2.6.0-2026` — Apenas Skills de UI/HTML/PDF)
Se e somente se a skill auditada gerar interfaces, componentes frontend ou documentos visuais, verifique e emita a matriz determinística:
- **`[DISC-PALETA]`**: Suporte ao catálogo de 22 temas (`v2.6.0-2026`) e proibição estrita de azul cobalto puro (`#0044FF`, `#233DFF`, `#1D4ED8`) ou neon.
- **`[DISC-TATIL]`**: Anti-glassmorphism (`backdrop-filter: blur` proibido), `L_card > L_canvas` no dark mode, sombras multicamadas, *rim light* zenital, `TYPOGRAPHY_PRESETS`, `GEOMETRY_PRESETS` e anti-squish (`flex-shrink: 0; white-space: nowrap;`).
- **`[DISC-OPCOES]`**: Uso estruturado de `ask_question` para decisões visuais/arquiteturais.
- **`[DISC-SUPPLY]`**: Priorização de `shadcn/ui`, `Radix UI`, `Lucide Icons` e `Tailwind CSS`.

### Etapa 4: Homologação, Espelhamento Físico e Registro
1. Incremente a versão SemVer no frontmatter YAML (`patch` para ajustes de texto/gatilho, `minor` para extração de scripts/referências ou desacoplamento).
2. Copie fisicamente `.agents/skills/<nome>/` para `skills/<nome>/` e `.gemini/config/plugins/franklin-skills/skills/<nome>/`.
3. Reexecute `dispatch_skill_deterministic_tests` e `uv run python scripts/validate_skills.py --targets <nome>` comprovando `[PASS]` total e atualize o [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md).

---

## 📤 Modelo de Saída
1. **Tabela Diagnóstica Antes vs. Depois**: Linhas do `SKILL.md`, Colisões de Gatilho Resolvidas, Arquivos Extraídos (`references/` / `scripts/`) e Veredito do Eval Harness (`[PASS]`/`[FAIL]`).
2. **Matriz Tátil (`[DISC-*]`)**: Presente quando a skill auditada for de UI/Frontend.
3. **Comprovação de Terminal**: Resultado real do `dispatch_skill_deterministic_tests` e `validate_skills.py`.
