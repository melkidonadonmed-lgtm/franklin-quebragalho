# Critérios Determinísticos de Auditoria: curadoria-obsidian-vault

Regras falsificáveis com marcadores booleanos determinísticos:

- `[PASS]` **Critério 01 (Preservação de Notas Não-Vazias):** Nenhuma nota com conteúdo gerado pelo usuário é apagada ou truncada.
- `[FAIL]` **Critério 01:** Comando de remoção executado em nota contendo texto ou links legítimos.

- `[PASS]` **Critério 02 (Proteção da Pasta .obsidian):** O diretório `.obsidian/` é categoricamente excluído de qualquer varredura ou mutação de arquivos.
- `[FAIL]` **Critério 02:** Modificação ou remoção de arquivos internos de configuração do Obsidian.

- `[PASS]` **Critério 03 (Falsificabilidade de Anexos Órfãos):** Comprovação determinística de que o anexo não possui nenhuma referência `![[...]]` ou `![](...)` em todo o vault antes de ser movido.
- `[FAIL]` **Critério 03:** Classificação precipitada de anexo em uso como órfão.

- `[PASS]` **Critério 04 (Integridade do Frontmatter YAML):** Validação de sintaxe YAML válida com tags consistentes e data no formato ISO.
- `[FAIL]` **Critério 04:** Injeção de blocos frontmatter com erros de sintaxe ou que quebrem a renderização do Obsidian.
