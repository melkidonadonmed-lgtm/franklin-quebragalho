# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA (DESIGN MÉDICO MINIMALISTA)

---

### Regra 1: Ausência Absoluta de Emojis
- **Critério**: O código de UI contém algum caractere emoji em botões, títulos ou badges?
- **Resultado**:
  - Zero emojis (apenas ícones vetoriais de linha) -> `[PASS]`
  - Presença de emojis na interface -> `[FAIL: Emojis detectados no código de UI]`

### Regra 2: Sobriedade Cromática e Sem Sombras Pesadas
- **Critério**: O CSS utiliza apenas sombras sutis (`shadow-sm` ou 1px) e paleta neutra Slate/Zinc?
- **Resultado**:
  - Estilos em conformidade com o minimalismo executivo -> `[PASS]`
  - Uso de `shadow-lg`, `shadow-2xl` ou cores primárias saturadas -> `[FAIL: Violação de diretriz de sobriedade]`
