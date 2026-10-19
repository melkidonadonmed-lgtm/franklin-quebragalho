# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA (`evoluir-skills` v2.2.0)

Toda criação, evolução ou homologação de skill conduzida pela `evoluir-skills` deve ser auditada contra as 6 regras booleanas abaixo, emitindo exclusivamente `[PASS]`, `[FAIL]` ou `[UNVERIFIED]`:

---

### Regra 1: Conformidade do Fluxo Forward Builder em 3 Passos
- **Critério**: A construção/evolução executou os 3 passos canônicos (Passo 1: Desambiguação e seleção do módulo `M1..M7`; Passo 2: Scaffolding físico com `rules/`, `evals/` e seção de *Gotchas*; Passo 3: Validação determinística + sincronização física)?
- **Resultado**:
  - Os 3 passos executados sem pular validações -> `[PASS]`
  - Geração ad-hoc sem regras, sem *Gotchas* ou sem avaliação estruturada -> `[FAIL: Pipeline de engenharia incompleto]`

---

### Regra 2: Frontmatter Canônico e Otimização de Gatilho (Tier 1)
- **Critério**: O arquivo `SKILL.md` possui YAML válido com `name` (`kebab-case <= 64`, idêntico à pasta), `description` (3ª pessoa, $30 \le \text{chars} \le 1024$, contendo gatilhos positivos e exclusões explícitas), `license: MIT` e bloco `metadata` (`version`, `author`, `category`, `updated_at`, `tags`)?
- **Resultado**:
  - Metadados completos e descrição calibrada contra *near-misses* -> `[PASS]`
  - Campos ausentes, descrição vaga ou fora do limite de caracteres -> `[FAIL: Metadados YAML ou Trigger Description inválidos]`

---

### Regra 3: Divulgação Progressiva em 3 Tiers e Zero Redundância (Tier 2 & Tier 3)
- **Critério**: O corpo do `SKILL.md` mantém-se enxuto ($< 500$ linhas), focado no *"Porquê"* (*Lean Instructions*), inclui seção de Armadilhas (*Gotchas*) e Orçamento Operacional, e segrega tabelas extensas ou scripts repetitivos para `references/` e `scripts/` (`<= 300` linhas/arquivo)?
- **Resultado**:
  - Corpo $< 500$ linhas, sem cópia redundante de outras skills e materiais densos desacoplados -> `[PASS]`
  - Arquivo monolítico $\ge 500$ linhas, ausência de *Gotchas* ou duplicação textual de regras -> `[FAIL: Violação de Orçamento de Contexto Tier 2 ou redundância]`

---

### Regra 4: Regras Determinísticas e Guardrails por Módulo (`rules/criterios_auditoria.md`)
- **Critério**: A skill possui `rules/criterios_auditoria.md` com marcadores `[PASS]`, `[FAIL]` e `[UNVERIFIED]`, incorporando os guardrails específicos do seu módulo de domínio (`M1` a `M7` de `_template/references/guardrails_por_modulo.md`)?
- **Resultado**:
  - Regras booleanas falsificáveis e alinhadas ao módulo de domínio presentes -> `[PASS]`
  - Ausência do arquivo ou uso de instruções subjetivas genéricas -> `[FAIL: Critérios de auditoria ausentes ou subjetivos]`

---

### Regra 5: Avaliação Empírica e Matriz de Gatilhos (`evals/evals.json`)
- **Critério**: O arquivo `evals/evals.json` existe, é um JSON válido não-vazio com `eval_id` e `expected_behavior`, cobrindo cenários funcionais e consultas de disparo (`should_trigger` vs `should_not_trigger` / *near-misses*)?
- **Resultado**:
  - Suíte `evals.json` estruturada e validada -> `[PASS]`
  - Ausência de `evals.json`, JSON malformado ou falta de *near-misses* -> `[FAIL: Suíte de avaliação empírica ausente ou incompleta]`

---

### Regra 6: Sincronização Física e Registro no Catálogo (`MY_SKILLS.md`)
- **Critério**: A skill foi aprovada por `scripts/validate_skills.py` (exit code `0`), sincronizada fisicamente por `scripts/sync_gemini_ecosystem.py` e teve versão SemVer/changelog registrados em `MY_SKILLS.md`?
- **Resultado**:
  - Validador `0`, sincronização física concluída e `MY_SKILLS.md` atualizado -> `[PASS]`
  - Divergência entre pastas, falha no validador ou omissão no catálogo -> `[FAIL: Divergência de sincronização ou governança]`
