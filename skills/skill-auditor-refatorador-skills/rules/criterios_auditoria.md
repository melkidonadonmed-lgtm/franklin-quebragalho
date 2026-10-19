# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REFATORAÇÃO DE SKILLS (`v2.2.0`)

Para assegurar validações rigorosas e erradicar auditorias fictícias, toda checagem do subagente auditor deve classificar cada critério sob um dos três estados determinísticos:
- `[PASS]`: Requisito plenamente satisfeito com evidência empírica e factual no arquivo inspecionado.
- `[FAIL]`: Requisito violado com causa-raiz técnica, arquivo e linha comprovados.
- `[UNVERIFIED]`: Não verificável por falta de insumos suficientes ou indisponibilidade de arquivo no escopo.

---

### Regra 1: Eixo 1 — Validação de Frontmatter, Schema YAML e Fronteira de Gatilhos (Tier 1)
- **Critério**: O arquivo `SKILL.md` contém frontmatter YAML válido (`name` em `kebab-case <= 64` igual à pasta, `description` em 3ª pessoa com $30 \le \text{chars} \le 1024$ declarando quando usar e quando NÃO usar, `license: MIT`, `version` SemVer, `updated_at`) e `evals/evals.json` com consultas `should_trigger` e `should_not_trigger` (*near-misses*)?
- **Classificação**:
  - Todos os campos presentes, fronteira limpa sem colisão com skills vizinhas e `evals.json` válido -> `[PASS]`
  - Campo obrigatório ausente, descrição vaga ou colisão de gatilho não tratada -> `[FAIL: Metadados YAML ou fronteira de gatilho deficiente]`

---

### Regra 2: Eixo 2 — Orçamento de Contexto em 3 Tiers, *Gotchas* e Zero Redundância (Tier 2 & 3)
- **Critério**: O corpo do `SKILL.md` possui $< 500$ linhas, prioriza instruções enxutas baseadas no *"Porquê"* (*Lean Instructions*), inclui seção de Armadilhas (*Gotchas*) e Orçamento Operacional, e elimina cópias redundantes referenciando `references/` e `scripts/`?
- **Classificação**:
  - Orçamento de 3 Tiers respeitado ($< 500$ linhas), *Gotchas* presentes e zero duplicação textual entre skills -> `[PASS]`
  - Corpo inchado $\ge 500$ linhas, ausência de *Gotchas* ou blocos copiados/colados de outras skills -> `[FAIL: Violação de Orçamento Tier 2 ou redundância entre skills detectada]`

---

### Regra 3: Eixo 3 & 4 — Contrato Determinístico (`Pydantic`), Isolamento Zero-Trust e Portão HITL
- **Critério**: Cálculos e transformações estão desacoplados em `scripts/` (`<= 300` linhas, tipados com Pydantic `extra="forbid"`, sem `input()` interativo, `stdout` vs `stderr` separados), sem credenciais hardcoded, com isolamento `<untrusted_user_input>` e portão HITL para ações destrutivas?
- **Classificação**:
  - Contratos determinísticos, isolamento XML e portões HITL ativos -> `[PASS]`
  - Lógica determinística delegada ao LLM, segredo hardcoded ou ausência de HITL -> `[FAIL: Quebra de determinismo ou segurança Zero-Trust]`

---

### Regra 4: Detecção de Acoplamento Monolítico e `authorized_sub_skills`
- **Critério**: A skill mantém responsabilidade única (SSOT) ou desacopla sub-funções divergentes via cláusula `authorized_sub_skills` / *Envelope Pattern*?
- **Classificação**:
  - Responsabilidade coesa ou encadeamento explícito via `authorized_sub_skills` -> `[PASS]`
  - Acúmulo de múltiplos domínios conflitantes sem modularização -> `[FAIL: Monólito de alto risco de alucinação detectado]`

---

### Regra 5: Conformidade com o Módulo Específico de Domínio (`M1`..`M7`)
- **Critério**: A skill cumpre integralmente os guardrails do seu módulo em `_template/references/guardrails_por_modulo.md` (`M1` Código/ReAct, `M2` Densidade $\le 35$ palavras, `M3` Frontend & Estilo por Propósito `preferencias_estilo_e_temas.md` com contraste WCAG, `tabular-nums`, camadas esculpidas e FSM, `M4` Grounding RAG, `M5` Imagem 8 Pilares em inglês, `M6` Vídeo temporal em inglês, `M7` Clínica 4 passos + 6 pilares + PII/PHI)?
- **Classificação**:
  - Aderência integral ao módulo de domínio aplicável -> `[PASS]`
  - Violação de qualquer guardrail obrigatório do módulo -> `[FAIL: Discrepância com o Módulo de Domínio M1..M7]`

---

### Regra 6: Governança de Mutação, Sincronização Física e Validação no Terminal
- **Critério**: As alterações foram aprovadas com exit code `0` em `scripts/validate_skills.py`, sincronizadas fisicamente por `scripts/sync_gemini_ecosystem.py` e registradas com SemVer e changelog no `MY_SKILLS.md`?
- **Classificação**:
  - Sincronização concluída, changelog atualizado e `validate_skills.py` `0` -> `[PASS]`
  - Sobrescrita sem changelog, divergência física ou erro no validador -> `[FAIL: Violação de governança de mutação de catálogo]`
