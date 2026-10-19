# Critérios Determinísticos de Auditoria — `conversor-html-pdf` (`v1.2.0`)

Regras falsificáveis com marcadores determinísticos (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) sob o Módulo **M5 (Conversão HTML/Markdown para PDF Executivo)**:

---

- **`[PASS]` Critério 01 (Existência Física e Bytes Não-Zero):** O arquivo `.pdf` gerado existe fisicamente no disco (`Test-Path -LiteralPath`) e possui `Length > 0` bytes comprovado após a execução.
- **`[FAIL: PDF_VAZIO_OU_INEXISTENTE]` Critério 01:** Arquivo PDF não encontrado ou corrompido com tamanho igual a `0` bytes.
- **`[UNVERIFIED]` Critério 01:** Binário do navegador (`msedge.exe` / `chrome.exe`) indisponível no ambiente de execução.

- **`[PASS]` Critério 02 (Blindagem de Quebra de Página `@media print`):** O CSS de impressão injetado contém `page-break-inside: avoid; break-inside: avoid;` para tabelas (`table`, `tr`), blocos de código (`pre`, `code`) e callouts, além de `@page { size: A4; }`.
- **`[FAIL: CORTE_DE_TABELA_NO_PDF]` Critério 02:** CSS sem blindagem contra quebras de página, permitindo corte de linhas no meio de tabelas ou código.

- **`[PASS]` Critério 03 (Execução Local-First Headless Sem Nuvem):** Uso exclusivo dos binários locais do Windows (`msedge.exe --headless --print-to-pdf` ou `chrome.exe`) via script `scripts/md-to-pdf.ps1`, sem enviar documentos para APIs externas.
- **`[FAIL: VAZAMENTO_PARA_API_EXTERNA]` Critério 03:** Tentativa de enviar conteúdo local para serviços web externos de conversão.

- **`[PASS]` Critério 04 (Preservação Integral do Fonte Original):** O arquivo `.md` ou `.html` de origem permanece intacto após a geração do PDF, e ambos são entregues com links clicáveis `file:///`.
- **`[FAIL: FONTE_REMOVIDO]` Critério 04:** Exclusão ou sobrescrita destrutiva do arquivo de entrada após a conversão.
