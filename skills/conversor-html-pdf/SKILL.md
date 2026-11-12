---
name: conversor-html-pdf
description: "Converte documentos Markdown e HTML para arquivos PDF profissionais via Microsoft Edge ou Chrome headless com CSS de impressão. Use para exportar relatórios em PDF; não use para redigir do zero."
version: "1.2.0"
updated_at: "2026-11-12"
compatibility: "Windows 11, pwsh 7+, Microsoft Edge ou Chrome Headless"
allowed-tools: ["read_file", "write_file", "run_command"]
metadata:
  version: "1.2.0"
  updated_at: "2026-11-12"
  author: "DocMaker & Melki"
  category: "Publicação e Conversão de Documentos"
  tags: ["pdf", "headless-browser", "css-print", "conversao"]
---
# Pipeline de Conversão Markdown/HTML para PDF (`conversor-html-pdf`)

## 1. Propósito e Gatilhos de Ativação (Quando Usar)

- Converter relatórios Markdown (`.md`) ou páginas HTML (`.html`) em PDF A4 pronto para compartilhamento ou impressão.
- Etapa final após redação por `redator-tecnico-markdown` ou diagramação por `organizador-fluxo-arvore-arquivos`.

### Quando NÃO Usar

- Para redigir conteúdo técnico do zero (use `redator-tecnico-markdown`).
- Para editoração gráfica com sangria industrial ou notas que permanecerão apenas no Obsidian Vault (`.md`).

---

## 2. Entradas Esperadas e Pré-requisitos

- `input_file_path` (obrigatório): Caminho absoluto do arquivo `.md` ou `.html`.
- `output_pdf_path` (opcional): Caminho do `.pdf` de saída (padrão: mesmo diretório e nome base).
- `page_orientation` (opcional): `portrait` (padrão) ou `landscape` (recomendado para tabelas `> 8` colunas).
- **Pré-requisito**: Microsoft Edge (`msedge.exe`) ou Google Chrome (`chrome.exe`) local no Windows 11.

---

## 3. Fluxo de Execução (Passo a Passo)

1. **Inspeção da Entrada**: Confirmar existência com `Test-Path -LiteralPath $inputFilePath`.
2. **Envelope HTML + Print Shielding**: Se a entrada for `.md`, aplicar a folha [`references/print_theme.css`](references/print_theme.css) (`@page { size: A4; margin: 18mm 20mm 20mm 20mm; }`, `break-inside: avoid` em `table`, `pre`, `blockquote` e `break-after: avoid` em `h1..h6`) ou acionar [`../../scripts/md-to-pdf.ps1`](../../scripts/md-to-pdf.ps1).
3. **Renderização Headless Local**:

   ```powershell
   $edgePath = @("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "C:\Program Files\Microsoft\Edge\Application\msedge.exe") | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
   & $edgePath --headless --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="$outputPdfPath" "$tempHtmlPath"
   ```

4. **Validação Física (`Read-After-Write`)**: Verificar `(Get-Item -LiteralPath $outputPdfPath).Length -gt 0` e remover apenas o HTML temporário, preservando o arquivo fonte original.

---

## 4. Saídas e Entregáveis

1. Status determinístico (`[PASS]` / `[FAIL]`) conforme [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md).
2. Tamanho final em KB e orientação aplicada (`portrait` / `landscape`).
3. Links clicáveis `file:///` para o PDF gerado e o fonte preservado.

---

## 5. Guardrails e Limites

- Proibido enviar documentos locais para APIs externas de conversão PDF ou exigir Pandoc/wkhtmltopdf quando o browser headless local estiver disponível.
- Proibido excluir ou sobrescrever o arquivo `.md`/`.html` de entrada.
