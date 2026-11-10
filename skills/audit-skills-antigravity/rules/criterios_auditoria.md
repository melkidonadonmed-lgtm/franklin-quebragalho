# Critérios Determinísticos de Auditoria — `audit-skills-antigravity`

- `[PASS]` Frontmatter YAML válido com `name`, `description` (com fronteira negativa) e `allowed-tools` em formato de lista YAML.
- `[PASS]` Corpo Nível 2 (`SKILL.md`) enxuto (`<= 2.500` tokens, `<= 10` regras ativas) com blocos extensos desacoplados em `references/`.
- `[FAIL]` Inchaço de contexto (`> 2.500` tokens no `SKILL.md`), ausência de evidência REA (`[FATO OBSERVADO]`) ou `FNR > 0` em guardrails críticos.
- `[FAIL]` Colisão semântica entre skills sem recomendação de `[FUSÃO]` ou falta das 6 categorias de veredito.
