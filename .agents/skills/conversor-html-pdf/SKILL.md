---
name: conversor-html-pdf
description: >-
  Converte documentos Markdown (.md) e HTML para arquivos PDF profissionais de alta fidelidade visual via Microsoft Edge ou Chrome headless, aplicando CSS de impressao calibrado, quebras de pagina inteligentes e estilizacao executiva.
license: MIT
metadata:
  version: "1.0.0"
  author: "DocMaker & Melki"
  category: "Publicação e Conversão de Documentos"
  updated_at: "2026-10-04"
  tags:
    - "pdf"
    - "headless-browser"
    - "css-print"
    - "conversao"
version: 1.0.0
updated_at: 2026-10-04
author: DocMaker & Melki
category: Publicação e Conversão de Documentos
---

# 1. NOME DA SKILL
`conversor-html-pdf` (Pipeline Determinístico de Conversão Markdown/HTML para PDF via Browser Headless).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "converta este markdown para PDF", "gere um PDF profissional deste relatório", "imprima este documento sem quebras feias", "exporte esta documentação para PDF".
- Após a redação de um documento por `redator-tecnico-markdown` quando for solicitada a versão final para compartilhamento ou impressão.
- Para gerar PDFs com CSS de impressão profissional (`@page`, cabeçalhos limpos, tabelas zebradas e blocos de código protegidos contra quebra de página).
- Quando for necessário transformar arquivos HTML estáticos ou relatórios de auditoria em documentos PDF portáveis.

### Quando NÃO Usar
- Para redigir o conteúdo técnico ou estruturar as seções do documento (utilize `redator-tecnico-markdown`).
- Para diagramação de materiais gráficos complexos de publicidade ou diagramas editoriais com sangria personalizada (InDesign).
- Quando o usuário quiser apenas a nota no Obsidian Vault em formato `.md`.

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `input_file_path` (obrigatório): Caminho absoluto do arquivo fonte Markdown (`.md`) ou HTML (`.html`).
- `output_pdf_path` (opcional): Caminho de destino do arquivo `.pdf` (padrão: mesmo diretório e nome do arquivo de entrada com extensão `.pdf`).
- `theme` (opcional): Estilo visual de impressão (`light_executive`, `dark_mineral`, `polar_sand`). Padrão: `light_executive` (otimizado para impressão com fundo branco e acentos ardósia).
- `page_orientation` (opcional): `portrait` (retrato) ou `landscape` (paisagem). Padrão: `portrait`.
- **Pré-requisito**: Microsoft Edge (`msedge.exe`) ou Google Chrome (`chrome.exe`) instalado no Windows 11.

---

## 4. DIRETRIZES DE ESTILIZAÇÃO E CSS DE IMPRESSÃO (PRINT SHIELDING)

A conversão emprega regras estritas de CSS `@media print` para eliminar problemas comuns de diagramação:

### 4.1. Prevenção de Quebras de Página Inadequadas
- **Blocos Indivisíveis:** Tabelas, blocos de código (`pre code`), cartões e caixas de alerta devem incluir obrigatoriamente:
  ```css
  page-break-inside: avoid;
  break-inside: avoid;
  ```
- **Títulos Órfãos:** Títulos (`h1`, `h2`, `h3`) devem forçar conexão com o elemento seguinte:
  ```css
  page-break-after: avoid;
  break-after: avoid;
  ```

### 4.2. Margens e Dimensões Canônicas da Página
```css
@page {
  size: A4 portrait;
  margin: 18mm 20mm 20mm 20mm;
}
```

### 4.3. Tipografia e Cores de Impressão
- Fonte principal: **Inter**, **Segoe UI** ou **Helvetica Neue** com `line-height: 1.55`.
- Código monoespaçado: **JetBrains Mono**, **Consolas** com fundo cinza suave (`#F3F4F6`) e borda tênue (`#E5E7EB`).
- Ausência de fundos escuros pesados no tema `light_executive` para economizar tinta e manter legibilidade perfeita no papel.

---

## 5. PROCESSO PASSO A PASSO (EXECUÇÃO DE CONVERSÃO)

### Passo 1: Inspeção do Arquivo de Entrada
Verificar a existência e o tipo do arquivo alvo:
```powershell
Test-Path -Path $inputFilePath
```

### Passo 2: Conversão de Markdown para HTML com Template de Impressão
Se a entrada for `.md`, envolver o conteúdo no envelope HTML canônico com os estilos de impressão calibrados contidos em `references/print_theme.css`.

### Passo 3: Disparo do Browser Headless Nativo
Localizar o binário do Microsoft Edge no Windows 11 e executar a conversão:
```powershell
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (!(Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

# Execução nativa headless com espera de renderização
& $edgePath --headless --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="$outputPdfPath" "$tempHtmlPath"
```

### Passo 4: Validação Determinística do PDF Gerado
Conferir se o arquivo PDF de saída existe e possui tamanho superior a 0 bytes:
```powershell
$pdfItem = Get-Item -Path $outputPdfPath
if ($pdfItem.Length -gt 0) {
    Write-Output "[PASS] PDF gerado com sucesso ($([math]::Round($pdfItem.Length / 1KB, 2)) KB)"
} else {
    throw "[FAIL] O arquivo PDF gerado está vazio (0 bytes)."
}
```

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill entrega:
1. **Confirmação de Geração do PDF:**
   - Tamanho final em KB, total estimado de páginas e tema aplicado.
2. **Status Determinístico de Validação:**
   - Marcador `[PASS]` comprovando exit code 0 e integridade do arquivo.
3. **Link Direto Local:**
   - Link clicável com esquema `file:///` para abertura imediata no leitor de PDF do Windows.

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA depender de ferramentas de terceiros pesadas não instaladas (Pandoc, wkhtmltopdf) quando o Edge/Chrome headless do Windows resolve com máxima fidelidade.
- Se o arquivo de entrada contiver tabelas extremamente largas com muitas colunas (> 8 colunas), a skill DEVE sugerir a orientação `landscape` para evitar compressão horizontal.
- Proibido excluir o arquivo `.md` original durante o processo de conversão.
