# Critérios Determinísticos de Auditoria — `redator-tecnico-markdown` (`v1.2.0`)

Regras falsificáveis com marcadores determinísticos (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) sob o Módulo **M5 (Documentação Técnica Markdown & Layout Shielding)**:

---

- **`[PASS]` Critério 01 (Lei da Linha em Branco — `02-layout-shielding.md`):** Presença obrigatória de linhas em branco antes e depois de títulos, tabelas, alertas GitHub (`> [!NOTE]`), listas e blocos de código.
- **`[FAIL: COLISAO_DE_BLOCO_MARKDOWN]` Critério 01:** Elementos estruturais colados sem linha em branco adjacente, quebrando a renderização CommonMark/GFM.
- **`[UNVERIFIED]` Critério 01:** Documento de destino não gerado ou apenas rascunho verbal.

- **`[PASS]` Critério 02 (Frontmatter YAML Válido e Compatibilidade Obsidian):** Documento inicia com bloco `---` contendo `title` (ou `aliases`), `date` (ISO `YYYY-MM-DD`) e `tags` sem erros de parsing YAML.
- **`[FAIL: FRONTMATTER_INVALIDO]` Critério 02:** Ausência de frontmatter quando aplicável ou metadados YAML malformados.

- **`[PASS]` Critério 03 (Escape de Caracteres Especiais e Mermaid Seguro):** Símbolos angulares (`\<`, `\>`) e pipes (`\|`) em células de tabela devidamente escapados, `$` literal escapado (`\$` ou em backticks) e nós Mermaid com caracteres especiais entre aspas duplas.
- **`[FAIL: QUEBRA_DE_PARSER]` Critério 03:** Uso de `<`, `>`, `|` ou `$` soltos que quebrem tabelas, KaTeX ou blocos Mermaid.

- **`[PASS]` Critério 04 (Delimitação de Responsabilidade — Redação vs. PDF):** A skill foca na redação e estruturação do arquivo `.md` com links clicáveis `file:///`, delegando a conversão binária para `conversor-html-pdf` quando solicitado PDF.
- **`[FAIL: ACOPLAMENTO_BINARIO]` Critério 04:** Tentativa de converter binários fora do pipeline headless homologado.
