<#
.SYNOPSIS
    Converte um arquivo Markdown (.md) em PDF profissional usando Microsoft Edge headless no Windows 11.
.EXAMPLE
    .\scripts\md-to-pdf.ps1 -InputFile "relatorio.md" -OutputFile "relatorio.pdf"
#>
param (
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [Parameter(Mandatory=$false)]
    [string]$OutputFile,

    [switch]$KeepHtml
)

if (-not (Test-Path $InputFile)) {
    Write-Error "Arquivo de entrada no encontrado: $InputFile"
    exit 1
}

$fullInputPath = (Resolve-Path $InputFile).Path
if (-not $OutputFile) {
    $OutputFile = [System.IO.Path]::ChangeExtension($fullInputPath, ".pdf")
} else {
    $OutputFile = [System.IO.Path]::GetFullPath($OutputFile)
}

$tempHtmlPath = [System.IO.Path]::ChangeExtension($fullInputPath, ".tmp.html")
$rawContent = Get-Content -Path $fullInputPath -Raw -Encoding UTF8

# Converso simples e elegante de Markdown bsico para HTML (ou preserva se j tiver tags)
# Utiliza formatao moderna com CSS profissional
$htmlBody = $rawContent
# Headers
$htmlBody = [regex]::Replace($htmlBody, '^### (.*?)$', '<h3>$1</h3>', [System.Text.RegularExpressions.RegexOptions]::Multiline)
$htmlBody = [regex]::Replace($htmlBody, '^## (.*?)$', '<h2>$1</h2>', [System.Text.RegularExpressions.RegexOptions]::Multiline)
$htmlBody = [regex]::Replace($htmlBody, '^# (.*?)$', '<h1>$1</h1>', [System.Text.RegularExpressions.RegexOptions]::Multiline)
# Bold / Italic
$htmlBody = [regex]::Replace($htmlBody, '\*\*(.*?)\*\*', '<strong>$1</strong>')
$htmlBody = [regex]::Replace($htmlBody, '\*(.*?)\*', '<em>$1</em>')
# Inline code
$htmlBody = [regex]::Replace($htmlBody, '`([^`]+)`', '<code>$1</code>')
# Paragraphs / Newlines
$htmlBody = $htmlBody -replace "\r\n", "`n"
$paragraphs = $htmlBody -split "\n\n" | ForEach-Object {
    $trimmed = $_.Trim()
    if ($trimmed -match '^<(h[1-6]|table|ul|ol|pre|blockquote)') {
        $trimmed
    } else {
        "<p>$($trimmed -replace "`n", "<br>")</p>"
    }
}
$finalBody = $paragraphs -join "`n"

$htmlDocument = @"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Documento</title>
<style>
    @page {
        size: A4;
        margin: 20mm 18mm 20mm 18mm;
        @bottom-right {
            content: counter(page);
        }
    }
    body {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        color: #24292f;
        line-height: 1.6;
        font-size: 11pt;
        background: #ffffff;
        margin: 0;
        padding: 0;
    }
    h1, h2, h3, h4 {
        color: #0f172a;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        font-weight: 600;
        page-break-after: avoid;
    }
    h1 { font-size: 20pt; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.3em; }
    h2 { font-size: 15pt; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.2em; }
    h3 { font-size: 12pt; }
    p { margin: 0 0 1em 0; }
    code {
        font-family: 'Cascadia Code', Consolas, Monaco, monospace;
        font-size: 9pt;
        background: #f1f5f9;
        padding: 0.2em 0.4em;
        border-radius: 4px;
        color: #0f172a;
    }
    pre {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px;
        overflow-x: auto;
        page-break-inside: avoid;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 1.5em;
        page-break-inside: avoid;
    }
    th, td {
        border: 1px solid #cbd5e1;
        padding: 8px 12px;
        text-align: left;
    }
    th {
        background-color: #f1f5f9;
        font-weight: 600;
    }
    blockquote {
        margin: 1em 0;
        padding: 0.5em 1em;
        color: #475569;
        border-left: 4px solid #3b82f6;
        background: #f8fafc;
        page-break-inside: avoid;
    }
</style>
</head>
<body>
$finalBody
</body>
</html>
"@

Set-Content -Path $tempHtmlPath -Value $htmlDocument -Encoding UTF8

# Caminhos dos executveis Edge / Chrome
$browserPath = ""
if (Test-Path "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") {
    $browserPath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
} elseif (Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe") {
    $browserPath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
}

if (-not $browserPath) {
    Write-Error "Nenhum navegador (Edge ou Chrome) foi encontrado para renderizar o PDF."
    exit 1
}

Write-Host "Convertendo para PDF via $browserPath..."
$uri = "file:///" + ($tempHtmlPath -replace "\\", "/")
$processArgs = @(
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--no-pdf-header-footer",
    "--print-to-pdf=`"$OutputFile`"",
    "`"$uri`""
)

$process = Start-Process -FilePath $browserPath -ArgumentList $processArgs -NoNewWindow -PassThru -Wait

if (-not $KeepHtml -and (Test-Path $tempHtmlPath)) {
    Remove-Item -Path $tempHtmlPath -Force
}

if (Test-Path $OutputFile) {
    Write-Host "PDF gerado com sucesso em: $OutputFile"
} else {
    Write-Error "Falha ao gerar o PDF."
    exit 1
}
