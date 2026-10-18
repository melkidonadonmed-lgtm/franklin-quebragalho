# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REFATORAÇÃO DE SKILLS (`v1.3.0`)

Para assegurar validações rigorosas e erradicar auditorias fictícias ou simulações vazias, toda checagem do subagente auditor deve classificar cada critério sob um dos três estados determinísticos:
- `[PASS]`: Requisito plenamente satisfeito com evidência empírica e factual no arquivo inspecionado.
- `[FAIL]`: Requisito violado com causa-raiz técnica, arquivo e linha comprovados.
- `[UNVERIFIED]`: Não verificável por falta de insumos suficientes ou indisponibilidade de arquivo no escopo.

---

### Regra 1: Validação de Frontmatter e Schema YAML (Tier 1)
- **Critério**: O arquivo `SKILL.md` contém frontmatter YAML válido delimitado por cercas `---` com bloco `metadata` canônico?
- **Campos Obrigatórios**: `name` (igual à pasta), `description` ($30 \le \text{chars} \le 1024$), `license`, `version` (SemVer `x.y.z`), `updated_at` (`YYYY-MM-DD`).
- **Classificação**:
  - Se todos os campos e formatos estiverem presentes -> `[PASS]`
  - Se faltar qualquer campo obrigatório ou o YAML for inválido -> `[FAIL: Campo obrigatório ausente ou formato YAML corrompido]`

---

### Regra 2: Qualidade da Descrição e Matriz de Gatilhos (*Trigger Optimization*)
- **Critério**: O campo `description` orienta o modelo em 3ª pessoa com gatilhos positivos e limites negativos (*near-misses*), acompanhado de casos `should-trigger` e `should-not-trigger` em `evals/evals.json`?
- **Classificação**:
  - Descrição em 3ª pessoa $\le 1024$ chars com fronteira negativa clara e `evals.json` válido -> `[PASS]`
  - Descrição vaga, acima de 1024 chars ou sem proteção contra *near-misses* -> `[FAIL: Descrição deficiente para progressive discovery]`

---

### Regra 3: Orçamento de Contexto em 3 Tiers e *Lean Instructions*
- **Critério**: O corpo do `SKILL.md` (Tier 2) possui $< 500$ linhas, prioriza instruções enxutas baseadas no "Porquê" (evitando *over-constraining*), e move tabelas extensas para `references/` e lógica repetitiva para `scripts/` (Tier 3)?
- **Classificação**:
  - Orçamento de 3 Tiers respeitado ($< 500$ linhas) e alta densidade atencional -> `[PASS]`
  - Corpo inchado $\ge 500$ linhas, excesso de regras redundantes ou scripts pesados inline -> `[FAIL: Violação de Orçamento Tier 2 ou baixa densidade Softmax]`

---

### Regra 4: Detecção de Acoplamento Monolítico e `authorized_sub_skills`
- **Critério**: A skill mantém responsabilidade coesa ou desacopla sub-funções divergentes via cláusula `authorized_sub_skills` / *Envelope Pattern*?
- **Classificação**:
  - Se a responsabilidade for coesa ou tiver encadeamento explícito -> `[PASS]`
  - Se acumular múltiplos domínios conflitantes sem modularização -> `[FAIL: Monólito de alto risco de alucinação detectado]`

---

### Regra 5: Conformidade com os 4 Módulos Táteis Melki (`DESIGN.md v4.5-soft`)
- **Critério**: Em skills que geram UI, HTML ou relatórios visuais, há conformidade com os 4 Presets Soft UI + 22 temas minerais, banimento de cobalto/glassmorphism/bordas 1px, iluminação 135° (`.ui-card-soft`, `surface-inset`), `L_card > L_canvas`, 4 presets tipográficos e 5 geometrias?
- **Classificação**:
  - Aderência integral aos 4 módulos -> `[PASS]`
  - Violação de paleta, ausência de relevo 135° ou omissão de opções -> `[FAIL: Discrepância com o Design System Tátil DESIGN.md v4.5-soft]`

---

### Regra 6: Governança de Mutação, Espelhamento 1:1 e Validação no Terminal
- **Critério**: As alterações estão sincronizadas entre `.agents/skills/` e `skills/`, registradas com SemVer e diff no `MY_SKILLS.md` e aprovadas com exit code `0` em `scripts/validate_skills.py`?
- **Classificação**:
  - Espelhamento idêntico, changelog atualizado e `validate_skills.py` `0` -> `[PASS]`
  - Sobrescrita sem changelog, divergência em `skills/` ou erro no validador -> `[FAIL: Violação de governança de mutação de catálogo]`
