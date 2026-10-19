---
name: skill-auditor-refatorador-skills
description: >-
  Cirurgião estrutural, desacoplador de monólitos e auditor determinístico do catálogo de skills. Use quando o usuário pedir para auditar skills existentes contra os 5 Eixos do Checklist Mestre e os 7 Módulos de Domínio (M1..M7), eliminar redundâncias entre skills, enxugar SKILL.md acima de 500 linhas ou calibrar gatilhos. Não use para criar uma skill nova do zero (use evoluir-skills).
license: MIT
metadata:
  version: "2.2.0"
  author: "SkillCraft & Melki"
  category: "Governança, Desacoplamento e Auditoria de Skills"
  updated_at: "2026-10-19"
  tags:
    - "auditoria-skills"
    - "refatoracao-cirurgica"
    - "desacoplamento"
    - "checklist-mestre"
    - "zero-redundancia"
version: 2.2.0
updated_at: 2026-10-19
author: SkillCraft & Melki
category: "Governança, Desacoplamento e Auditoria de Skills"
authorized_sub_skills:
  - name: skill-orquestrador-planos-encadeados
    role: "Atualização das rotas de hand-off quando um monólito é dividido em sub-skills"
---

# Cirurgia Estrutural e Auditoria Determinística de Skills (`skill-auditor-refatorador-skills` v2.2.0) 🛡️

Motor de **Diagnóstico, Desacoplamento Cirúrgico e Eliminação de Redundâncias**. Atua na inspeção determinística das skills existentes contra a Fonte Única de Verdade (SSOT) em [`skills/_template/references/guardrails_por_modulo.md`](../_template/references/guardrails_por_modulo.md).

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Auditar uma skill ou todo o catálogo contra os **5 Eixos do Checklist Mestre Transversal** e os **7 Módulos de Domínio (`M1`..`M7`)**.
- Eliminar redundâncias e sobreposições entre skills vizinhas (*overlapping descriptions*, blocos duplicados de regras ou templates repetidos).
- Refatorar e enxugar uma skill inchada: extrair blocos estáticos para `references/` (Tier 3) e comandos/parsers repetitivos detectados em `transcript.jsonl` para `scripts/`.
- Dividir uma skill monolítica (que mistura múltiplos domínios cognitivos) em skills independentes e ortogonais conforme [`references/matriz_desacoplamento.md`](references/matriz_desacoplamento.md).

## 🚫 Quando NÃO Usar
- **Não usar** para criar uma skill nova a partir de uma ideia bruta (use `evoluir-skills`).
- **Não usar** para arquitetar código de agentes em Go, Python ou TypeScript (use `aprimoramento-expansibilidade-agentes-skills`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `skill_target` (obrigatório): Nome/slug da skill, lista de skills ou `"all"` para varredura de catálogo.
- `audit_mode` (opcional): `diagnostic_only` (somente diagnóstico `[PASS]`/`[FAIL]`) ou `apply_refactoring` (elimina redundâncias, extrai `references/` e `scripts/`, sincroniza e atualiza o `MY_SKILLS.md`).
- `transcript_log_path` (opcional): Caminho de `transcript.jsonl` para identificar comandos repetitivos que devem migrar para `scripts/`.

---

## ⚙️ Fluxo Cirúrgico em 4 Etapas

### Etapa 1: Diagnóstico Determinístico Zero-LLM (`validate_skills.py` + `adk-go-mcp`)
Nunca faça contagem manual de linhas ou inspeção visual de JSON antes de acionar os motores determinísticos:
1. Execute o validador estrutural do repositório:
   ```powershell
   uv run python scripts/validate_skills.py --targets <skill_target>
   ```
2. Quando o servidor `adk-go-mcp` estiver ativo para benchmark A vs B, invoque **`dispatch_skill_deterministic_tests`** (`action: "run_only"`).

### Etapa 2: Auditoria nos 5 Eixos Transversais + Cirurgia de Desacoplamento
Confronte a skill com [`skills/_template/references/guardrails_por_modulo.md`](../_template/references/guardrails_por_modulo.md) e aplique as 4 operações cirúrgicas:
1. **Eixo 1 — Cura de Colisão de Gatilhos (Tier 1)**:
   - Compare a `description` das skills semanticamente próximas e elimine sobreposições.
   - Adicione cláusulas explícitas `"Use quando..."` e `"Não use para X (use skill-Y)"`, calibrando `should_trigger` vs `should_not_trigger` (*near-misses*) em `evals/evals.json`.
2. **Eixo 2 — Desidratação de Tier 2 (`SKILL.md < 500` linhas) e Eliminação de Redundâncias**:
   - Remova blocos copiados de outras skills (ex.: tabelas inteiras de paletas em skills que não são de UI ou checklists duplicados), substituindo por links para a SSOT (`_template/references/`).
   - Confirme a presença da seção de **Armadilhas (*Gotchas*)** e do **Orçamento Operacional** (`max_steps`).
3. **Eixo 3 & 4 — Extração para `scripts/` e Defesa Zero-Trust**:
   - Extraia parsers/cálculos repetitivos para `scripts/` (`<= 300` linhas, tipados com Pydantic `extra="forbid"`, sem `input()`, `stdout` vs `stderr`).
   - Verifique isolamento XML (`<untrusted_user_input>`), zero credenciais hardcoded e portões HITL / `--dry-run`.
4. **Fissão de Monólitos**:
   - Se a skill mistura domínios conflitantes (ex.: *Diagnóstico Read-Only* + *Refatoração Destrutiva*), separe conforme [`references/matriz_desacoplamento.md`](references/matriz_desacoplamento.md).

### Etapa 3: Auditoria do Módulo Específico de Domínio (`M1`..`M7`)
Verifique apenas o módulo correspondente à natureza da skill:
- **`M1` (Execução/Código)**: `max_steps`, zero `input()`, `stdout`/`stderr` separados, dependências isoladas (`uv`).
- **`M2` (Design/Layout)**: Arquitetura da informação prévia, teto de $\le 35$ palavras/bloco e 6–10 blocos/tela.
- **`M3` (Frontend/UI `DESIGN.md v4.5-soft`)**: HTML5 semântico, anti-XSS (`AUDIT-SEC-01`), WCAG 2.1 AA (`AUDIT-A11Y-01/02`), FSM 4 estados (`AUDIT-STATE-01/02`) e matriz tátil (`[DISC-PALETA]` zero cobalto/Cerulean `#0284C7`, `[DISC-TATIL]` luz 135°/zero blur/zero 1px, `[DISC-OPCOES]`, `[DISC-SUPPLY]`).
- **`M4` (Pesquisa/RAG)**: Memória separada da fonte de verdade, grounding explícito e sanitização contra *context poisoning*.
- **`M5` / `M6` (Imagem / Vídeo)**: Prompts finais em inglês, 8 Pilares Visuais (Imagem) e 1 ação + 1 câmera com progressão temporal (Vídeo).
- **`M7` (Saúde/Clínica)**: Anonimização PII/PHI, cadeia causal em 4 passos, prescrição em 6 pilares e citação de diretriz (Instituição + Ano).

### Etapa 4: Homologação, Sincronização Física e Registro
1. Incremente a versão SemVer no frontmatter YAML (`patch` para ajustes de texto/gatilho, `minor` para extração de scripts/referências ou eliminação de redundâncias).
2. Execute `uv run python scripts/validate_skills.py` e `uv run python scripts/sync_gemini_ecosystem.py` comprovando `[PASS]` total e atualize o [MY_SKILLS.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/MY_SKILLS.md).

---

## 🛡️ Exceções e Armadilhas (*Gotchas*)
- **Falso Positivo de Concisão**: Enxugar uma skill nunca deve remover cláusulas negativas de fronteira (`Quando NÃO Usar`) nem regras determinísticas falsificáveis (`[PASS]`/`[FAIL]`).
- **Sincronização Tripla**: Sempre rode `scripts/sync_gemini_ecosystem.py` após refatorar em `skills/` para propagar para o plugin global `~/.gemini/config/plugins/franklin-skills/`.

---

## 📤 Modelo de Saída
1. **Tabela Diagnóstica Antes vs. Depois**: Linhas do `SKILL.md`, Redundâncias Eliminadas, Módulos Extraídos (`references/` / `scripts/`) e Veredito (`[PASS]`/`[FAIL]`).
2. **Checklist Transversal (5 Eixos) + Módulo de Domínio (`M1`..`M7`)**: Avaliação objetiva item a item.
3. **Comprovação de Terminal**: Resultado real de `validate_skills.py` e `sync_gemini_ecosystem.py`.
