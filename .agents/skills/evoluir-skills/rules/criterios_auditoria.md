# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA (`evoluir-skills` v2.0.0)

Toda criação, evolução ou homologação de skill conduzida pela `evoluir-skills` deve ser auditada contra as 6 regras booleanas abaixo, emitindo exclusivamente `[PASS]`, `[FAIL]` ou `[UNVERIFIED]`:

---

### Regra 1: Conformidade do Pipeline Encadeado (`SkillCraft Chain`)
- **Critério**: A evolução seguiu os 4 estágios (1. Expansão de contexto; 2. Dimensionamento em 3 Tiers/Expansibilidade; 3. Scaffolding com `rules/` e `evals/`; 4. Auditoria + Espelhamento)?
- **Resultado**:
  - Os 4 estágios executados sem pular validações -> `[PASS]`
  - Geração ad-hoc sem regras ou sem avaliação estruturada -> `[FAIL: Pipeline de engenharia incompleto]`

---

### Regra 2: Frontmatter Canônico e Otimização de Gatilho (Tier 1)
- **Critério**: O arquivo `SKILL.md` possui YAML válido com `name`, `description` (3ª pessoa, $30 \le \text{chars} \le 1024$, contendo gatilhos positivos e limites negativos), `license: MIT` e bloco `metadata` (`version`, `author`, `category`, `updated_at`, `tags`)?
- **Resultado**:
  - Metadados completos, descrição calibrada contra falsos positivos (*near-misses*) -> `[PASS]`
  - Campos ausentes, descrição vaga ou fora do limite de caracteres -> `[FAIL: Metadados YAML ou Trigger Description inválidos]`

---

### Regra 3: Divulgação Progressiva em 3 Tiers e Densidade de Atenção (Tier 2 & Tier 3)
- **Critério**: O corpo do `SKILL.md` mantém-se enxuto ($< 500$ linhas), utilizando *Lean Instructions* baseadas no "Porquê", e segregando tabelas extensas, manuais ou códigos repetitivos para `references/` e `scripts/`?
- **Resultado**:
  - Corpo $< 500$ linhas e materiais densos desacoplados em `references/` ou `scripts/` -> `[PASS]`
  - Arquivo monolítico $\ge 500$ linhas ou instruções redundantes que diluem a atenção -> `[FAIL: Violação de Orçamento de Contexto Tier 2]`

---

### Regra 4: Regras Determinísticas Falsificáveis (`rules/criterios_auditoria.md`)
- **Critério**: A skill possui o arquivo `rules/criterios_auditoria.md` contendo critérios objetivos verificáveis com marcadores explícitos `[PASS]`, `[FAIL]` e `[UNVERIFIED]`, livre de validações genéricas vazias?
- **Resultado**:
  - Regras booleanas e falsificáveis presentes -> `[PASS]`
  - Ausência do arquivo ou uso de instruções subjetivas ("validar se está bom") -> `[FAIL: Critérios de auditoria ausentes ou subjetivos]`

---

### Regra 5: Avaliação Empírica e Matriz de Gatilhos (`evals/evals.json`)
- **Critério**: O arquivo `evals/evals.json` existe, é um JSON válido não-vazio com `eval_id` e `expected_behavior`, cobrindo cenários funcionais (*Baseline vs. Treatment*) e consultas de disparo (`should-trigger` vs `should-not-trigger` / *near-misses*)?
- **Resultado**:
  - Suíte `evals.json` estruturada e validada -> `[PASS]`
  - Ausência de `evals.json` ou JSON malformado -> `[FAIL: Suíte de avaliação empírica ausente ou corrompida]`

---

### Regra 6: Espelhamento Físico Paritário e Registro no Catálogo (`MY_SKILLS.md`)
- **Critério**: O diretório `.agents/skills/<nome>/` está espelhado de forma idêntica em `skills/<nome>/`, foi aprovado por `scripts/validate_skills.py` (exit code `0`) e teve versão SemVer/changelog registrados em `MY_SKILLS.md`?
- **Resultado**:
  - Espelhamento 1:1, validador `0` e `MY_SKILLS.md` atualizado -> `[PASS]`
  - Divergência entre pastas, falha no script validador ou omissão no catálogo -> `[FAIL: Divergência de espelhamento ou governança]`
