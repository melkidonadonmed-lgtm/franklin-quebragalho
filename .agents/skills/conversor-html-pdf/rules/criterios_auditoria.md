# Critérios Determinísticos de Auditoria: conversor-html-pdf

Regras falsificáveis com marcadores booleanos determinísticos:

- `[PASS]` **Critério 01 (Arquivo PDF Não-Vazio):** O arquivo PDF gerado existe fisicamente no caminho indicado e possui tamanho superior a 0 bytes (`Length > 0`).
- `[FAIL]` **Critério 01:** Arquivo PDF não encontrado ou corrompido com tamanho igual a 0 bytes.

- `[PASS]` **Critério 02 (Prevenção de Quebras de Tabela e Código):** O CSS de impressão injetado contém obrigatoriamente `page-break-inside: avoid;` ou `break-inside: avoid;` para tabelas e blocos `pre`.
- `[FAIL]` **Critério 02:** CSS sem blindagem contra quebras de página, permitindo corte de linhas no meio de tabelas.

- `[PASS]` **Critério 03 (Execução Headless Nativa):** Uso de binários oficiais do Windows (`msedge.exe` ou `chrome.exe`) sem requisições a servidores externos de conversão.
- `[FAIL]` **Critério 03:** Tentativa de enviar conteúdo do documento para APIs remotas não autorizadas de conversão.

- `[PASS]` **Critério 04 (Preservação do Fonte Original):** O arquivo Markdown ou HTML de origem permanece inalterado e preservado após a conversão.
- `[FAIL]` **Critério 04:** Remoção inadvertida do arquivo de entrada após a geração do PDF.
