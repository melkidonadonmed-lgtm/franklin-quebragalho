# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA (EVOLUIR SKILLS)

Toda evolução ou criação de skill deve atender aos seguintes critérios determinísticos:

---

### Regra 1: Validação Estrutural e Frontmatter
- **Critério**: O arquivo `SKILL.md` possui frontmatter YAML com `name`, `description` e `version`?
- **Resultado**:
  - Metadados completos e válidos -> `[PASS]`
  - Campos ausentes ou inválidos -> `[FAIL: Metadados YAML incompletos]`

### Regra 2: Espelhamento Paritário em skills/
- **Critério**: O diretório da skill em `.agents/skills/` possui clone idêntico em `skills/`?
- **Resultado**:
  - Diretórios espelhados e sincronizados -> `[PASS]`
  - Falta de espelhamento ou arquivos divergentes -> `[FAIL: Divergência de espelhamento]`
