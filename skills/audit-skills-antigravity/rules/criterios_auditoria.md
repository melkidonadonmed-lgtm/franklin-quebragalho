# Critérios Determinísticos de Auditoria — `audit-skills-antigravity`

- `[PASS]` Frontmatter YAML válido (`name <= 64` idêntico à pasta, `description <= 240` chars com fronteira negativa, `compatibility <= 500` chars e `allowed-tools` coerente com o fluxo).
- `[PASS]` Corpo Nível 2 (`SKILL.md`) enxuto (`<= 1.200` tokens, `<= 500` linhas, `<= 10` regras ativas), `CognitiveCoherenceScore >= 80` e `0` referências quebradas.
- `[FAIL]` Inchaço de contexto (`> 1.200` tokens no `SKILL.md` sem *Progressive Disclosure*), links/referências inexistentes, contaminação de domínio UI em skill não-visual, falta de fatores arquetípicos (`PLANNING` / `E2E_UI_AUDIT`) ou `FNR > 0.05`.
- `[FAIL]` Colisão semântica (`>= 80%`) ou de rota entre skills sem recomendação de `[FUSÃO]`.
- `[UNVERIFIED]` Métricas dinâmicas de runtime externo quando binários opcionais (`rea`) não estiverem ativos no host.
