# As 6 Categorias de Veredito e Fórmulas Matemáticas (`audit-skills-antigravity`)

## 1. Fórmulas Matemáticas de Acuidade

- **Estimador Não Enviesado $\text{Pass}@k$ (Chen et al.):**
  $$\text{Pass}@k = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}$$
- **Taxa de Falsos Negativos ($\text{FNR}$):**
  $$\text{FNR} = \frac{\text{FN}}{\text{TP} + \text{FN}}$$

## 2. As 6 Categorias de Ação Obrigatórias

1. **`[RECOMENDAÇÃO: MANTER]`**: Skill enxuta (`<= 2.500` tokens), YAML válido, `<= 10` regras e $\text{Pass}@3 \ge 95\%$.
2. **`[RECOMENDAÇÃO: ATUALIZAÇÃO]`**: Dependências defasadas, ausência de lista `allowed-tools` ou SDK antigo detectado pelo REA.
3. **`[RECOMENDAÇÃO: AJUSTE]`**: Saturação atencional (`> 10` regras no mesmo contexto) ou falta de fronteira negativa na descrição.
4. **`[RECOMENDAÇÃO: MELHORIA]`**: Inchaço de contexto (`> 2.500` tokens no `SKILL.md`) exigindo extração para `references/` (*Progressive Disclosure*).
5. **`[RECOMENDAÇÃO: EXCLUSÃO]`**: Skill obsoleta, quebrada ou sem scripts/referências válidas ($\text{Pass}@k < 50\%$).
6. **`[RECOMENDAÇÃO: FUSÃO]`**: Sobreposição semântica alta com outra skill do catálogo, causando ambiguidade de roteamento.
