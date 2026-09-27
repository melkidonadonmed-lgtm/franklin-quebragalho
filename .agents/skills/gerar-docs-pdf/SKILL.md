---
name: gerar-docs-pdf
description: >-
  Use esta skill sempre que o usuário solicitar criação, redação, formatação de notas ou relatórios em Markdown (.md) e conversão para arquivos PDF profissionais.
---

# Geração de Documentos Markdown e Conversão para PDF 📄

Procedimento para redigir documentação estruturada em Markdown e converter automaticamente para PDF profissional no Windows 11.

---

## 🎯 Quando Usar
- Criação de relatórios técnicos, atas, resumos e documentações de projetos.
- Geração de notas no formato compatível com o Obsidian Vault.
- Exportação de arquivos `.md` para arquivos `.pdf` prontos para compartilhamento ou impressão.

---

## 🛠️ Métodos de Conversão para PDF

No ambiente Windows 11 do Melki, a conversão é realizada de forma nativa e rápida utilizando **Microsoft Edge headless** ou **Google Chrome headless**, eliminando a necessidade de ferramentas pesadas externas.

### Fluxo de Conversão:
1. **Markdown ➔ HTML estilizado**: O conteúdo Markdown é envolvido em um template HTML com CSS limpo (tipografia moderna, tabelas formatadas, quebras de página `@media print`).
2. **HTML ➔ PDF**: O navegador converte o HTML em PDF com comandos nativos via PowerShell.

---

## 📋 Passo a Passo de Execução

### 1. Redação do Arquivo Markdown
Estruture o arquivo com títulos semânticos, listas, tabelas e caixas de destaque quando relevante.
Exemplo de cabeçalho YAML para Obsidian:
```markdown
---
titulo: Relatório Técnico
autor: Franklin Quebra-Galho / Melki
data: 2026-09-27
tags: [relatorio, automacao]
---
```

### 2. Conversão Automatizada via Script
Utilize o utilitário incluído no workspace:
```powershell
# Execução pelo script utilitário do workspace
powershell -ExecutionPolicy Bypass -File .\scripts\md-to-pdf.ps1 -InputFile "documento.md" -OutputFile "documento.pdf"
```

### 3. Comando Direto via Microsoft Edge Headless
Caso queira converter um HTML diretamente:
```powershell
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$htmlPath = (Resolve-Path "documento.html").Path
$pdfPath = [System.IO.Path]::ChangeExtension($htmlPath, ".pdf")

& $edgePath --headless --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf=$pdfPath $htmlPath
```

---

## 🎨 Padrão Visual do PDF
- **Fonte**: Segoe UI, Inter ou Arial (legibilidade em tela e papel).
- **Margens**: 20mm (1.5cm a 2cm).
- **Cores**: Tons neutros com azul/grafite para cabeçalhos.
- **Quebras de Página**: `page-break-inside: avoid;` em tabelas e blocos de código.
