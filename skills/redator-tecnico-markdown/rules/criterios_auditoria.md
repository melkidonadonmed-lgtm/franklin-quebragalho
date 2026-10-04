# Critérios Determinísticos de Auditoria: redator-tecnico-markdown

Regras falsificáveis com marcadores booleanos determinísticos:

- `[PASS]` **Critério 01 (Lei da Linha em Branco):** Presença de linhas em branco antes e depois de títulos, tabelas, alertas, listas e blocos de código.
- `[FAIL]` **Critério 01:** Elementos estruturais colados sem linha em branco adjacente, quebrando a renderização CommonMark.

- `[PASS]` **Critério 02 (Frontmatter YAML Válido):** Documento inicia com bloco `---` contendo `title`, `date` e `tags` sem erros de parsing.
- `[FAIL]` **Critério 02:** Ausência de frontmatter ou metadados malformados.

- `[PASS]` **Critério 03 (Escape de Caracteres Especiais):** Símbolos angulares (`\<`, `\>`) e pipes (`\|`) em tabelas devidamente escapados.
- `[FAIL]` **Critério 03:** Uso de caracteres `<` ou `>` soltos em texto corrido que causem confusão em parsers HTML/Markdown.

- `[PASS]` **Critério 04 (Delimitação de Responsabilidade):** A skill foca estritamente na redação do Markdown sem tentar gerar PDFs diretamente.
- `[FAIL]` **Critério 04:** Execução de scripts de conversão de binários dentro da skill de redação pura.
