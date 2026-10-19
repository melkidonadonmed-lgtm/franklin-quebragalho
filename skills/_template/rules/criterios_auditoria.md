# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`_template` v2.0.0)

Toda skill derivada deste template deve ser verificada contra os 5 eixos determinísticos abaixo, emitindo exclusivamente `[PASS]`, `[FAIL]` ou `[UNVERIFIED]`:

---

### Regra 1: Metadados YAML e Fronteira de Gatilho (Eixo 1 — Tier 1)
- **Critério**: O `SKILL.md` possui YAML válido com `name` (`kebab-case <= 64`, igual à pasta), `description` em 3ª pessoa ($30 \le \text{chars} \le 1024$ com gatilhos positivos e exclusões explícitas), `license: MIT` e bloco `metadata`?
- **Resultado**:
  - Todos os campos presentes e descrição calibrada contra *near-misses* -> `[PASS]`
  - Campo ausente, nome divergente ou descrição sem fronteira negativa -> `[FAIL: Metadados YAML ou descrição de gatilho inválidos]`

---

### Regra 2: Governança de Contexto, Seção de *Gotchas* e Zero Redundância (Eixo 2 — Tier 2 & 3)
- **Critério**: O corpo do `SKILL.md` possui `< 500` linhas, inclui seção explícita de Armadilhas (*Gotchas*) e Orçamento Operacional (`max_steps`), e desacopla tabelas/módulos extensos em `references/` e `scripts/` sem copiar blocos redundantes?
- **Resultado**:
  - Corpo `< 500` linhas, *Gotchas* documentados e módulos em `references/` -> `[PASS]`
  - Monólito `>= 500` linhas, ausência de *Gotchas* ou cópia redundante de regras de outras skills -> `[FAIL: Violação de Progressive Disclosure ou redundância detectada]`

---

### Regra 3: Execução Determinística, Tipagem Estrita e Erros Acionáveis (Eixo 3)
- **Critério**: Cálculos e transformações rígidas estão delegados a `scripts/` (`<= 300` linhas, sem `input()` bloqueante, `stdout` separado de `stderr`) com validação tipada (`Pydantic extra="forbid"` / JSON Schema) e erros acionáveis?
- **Resultado**:
  - Scripts determinísticos tipados, testados e com erros acionáveis -> `[PASS]`
  - Cálculos delegados ao LLM, uso de `input()` em terminal ou erros opacos -> `[FAIL: Quebra de contrato determinístico]`

---

### Regra 4: Defesa Zero-Trust, Tags XML e Portão HITL (Eixo 4)
- **Critério**: A skill proíbe credenciais hardcoded, isola entradas externas em `<untrusted_user_input>` e exige `--dry-run` / confirmação humana (HITL) antes de mutações destrutivas?
- **Resultado**:
  - Zero segredos expostos, tags XML ativas e portão HITL configurado -> `[PASS]`
  - Segredo hardcoded, ausência de isolamento ou mutação destrutiva silenciosa -> `[FAIL: Violação de segurança Zero-Trust]`

---

### Regra 5: Conformidade com o Módulo de Domínio (`M1`..`M7`) e `evals/evals.json` (Eixo 5)
- **Critério**: A skill aplica os guardrails específicos do seu módulo (`M1` Código, `M2` Design, `M3` Frontend & Estilo por Propósito `preferencias_estilo_e_temas.md`, `M4` RAG, `M5` Imagem, `M6` Vídeo, `M7` Clínica) e possui `evals/evals.json` válido com casos `should_trigger` e `should_not_trigger` (*near-misses*)?
- **Resultado**:
  - Guardrails do módulo atendidos e `evals/evals.json` validado -> `[PASS]`
  - Violação de guardrail de domínio ou `evals.json` sem *near-misses* -> `[FAIL: Inconformidade de módulo de domínio ou suíte de evals incompleta]`
