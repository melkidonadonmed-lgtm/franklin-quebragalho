<#
.SYNOPSIS
    Provisionador Universal de Projetos Melki (Scaffolder 2026).
.DESCRIPTION
    Cria uma nova base de projeto moderna e padronizada utilizando React 18, Vite,
    TypeScript no modo estrito e o Design System Tátil (Luxury Obsidian & Mineral Slate)
    com especificação frontend.design.md completa, Atomic Design e motor Canvas 2D.
.PARAMETER ProjectName
    Nome da pasta e identificador do novo projeto.
.PARAMETER DestinationPath
    Diretório onde o projeto será instanciado. Padrão: C:\Users\melki\Projetos
.PARAMETER InstallDeps
    Se especificado, roda 'npm install' automaticamente após o provisionamento.
.PARAMETER InitGit
    Se especificado, inicializa um repositório git e cria o commit inicial.
.EXAMPLE
    .\scaffold-universal-app.ps1 -ProjectName "meu-novo-app"
.EXAMPLE
    .\scaffold-universal-app.ps1 -ProjectName "painel-clinico" -InstallDeps -InitGit
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $true, Position = 0, HelpMessage = "Nome do novo projeto")]
    [ValidatePattern('^[a-zA-Z0-9_\-]+$')]
    [string]$ProjectName,

    [Parameter(Mandatory = $false, Position = 1)]
    [string]$DestinationPath = "C:\Users\melki\Projetos",

    [Parameter(Mandatory = $false)]
    [switch]$InstallDeps,

    [Parameter(Mandatory = $false)]
    [switch]$InitGit
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Caminhos absolutos
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = Split-Path -Parent $ScriptDir
$TemplateDir = Join-Path $WorkspaceRoot "templates\universal-app"
$TargetDir = Join-Path $DestinationPath $ProjectName

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   SCAFFOLDER UNIVERSAL MELKI 2026 - TACTILE MATTE BASE   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Projeto Alvo: $ProjectName" -ForegroundColor Yellow
Write-Host "Destino     : $TargetDir" -ForegroundColor Yellow
Write-Host "Origem      : $TemplateDir" -ForegroundColor Gray
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

# 1. Validação de pré-requisitos
if (-not (Test-Path $TemplateDir)) {
    throw "Diretório de template não encontrado em '$TemplateDir'. Abortando."
}

if (-not (Test-Path $DestinationPath)) {
    Write-Host "[+] Criando diretório pai '$DestinationPath'..." -ForegroundColor Gray
    New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
}

if (Test-Path $TargetDir) {
    $existingItems = Get-ChildItem -Path $TargetDir -Force
    if ($existingItems.Count -gt 0) {
        throw "O diretório alvo '$TargetDir' já existe e não está vazio. Abortando por segurança."
    }
} else {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

# 2. Cópia dos arquivos do template
Write-Host "[+] Clonando estrutura universal de diretórios e arquivos..." -ForegroundColor Cyan
Copy-Item -Path "$TemplateDir\*" -Destination $TargetDir -Recurse -Force

# Copiar arquivos pontuados (.env.example, .gitignore)
Get-ChildItem -Path $TemplateDir -Filter ".*" -Force | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $TargetDir -Force
}

# 3. Customização dos Metadados do Projeto
Write-Host "[+] Injetando identidade e tokens do projeto '$ProjectName'..." -ForegroundColor Cyan

# 3.1 package.json
$pkgPath = Join-Path $TargetDir "package.json"
if (Test-Path $pkgPath) {
    $pkgContent = Get-Content -Path $pkgPath -Raw -Encoding utf8
    $pkgContent = $pkgContent -replace '"name":\s*"universal-app-template"', "`"name`": `"$ProjectName`""
    Set-Content -Path $pkgPath -Value $pkgContent -Encoding utf8
}

# 3.2 index.html
$indexPath = Join-Path $TargetDir "index.html"
if (Test-Path $indexPath) {
    $indexContent = Get-Content -Path $indexPath -Raw -Encoding utf8
    $indexContent = $indexContent -replace '<title>Universal App</title>', "<title>$ProjectName</title>"
    Set-Content -Path $indexPath -Value $indexContent -Encoding utf8
}

# 3.3 docs/CONTEXT.md
$contextPath = Join-Path $TargetDir "docs\CONTEXT.md"
if (Test-Path $contextPath) {
    $ctxContent = Get-Content -Path $contextPath -Raw -Encoding utf8
    $ctxContent = $ctxContent -replace '\[NOME_DO_PROJETO\]', $ProjectName
    Set-Content -Path $contextPath -Value $ctxContent -Encoding utf8
}

# 3.4 docs/SPEC.md
$specPath = Join-Path $TargetDir "docs\SPEC.md"
if (Test-Path $specPath) {
    $spContent = Get-Content -Path $specPath -Raw -Encoding utf8
    $spContent = $spContent -replace '\[NOME_DO_PROJETO\]', $ProjectName
    Set-Content -Path $specPath -Value $spContent -Encoding utf8
}

# 4. Instalação Opcional de Dependências
if ($InstallDeps) {
    Write-Host "[+] Instalando dependências Node.js via npm install..." -ForegroundColor Magenta
    Push-Location $TargetDir
    try {
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Falha durante o npm install (Exit Code: $LASTEXITCODE)."
        } else {
            Write-Host "[PASS] Dependências instaladas com sucesso." -ForegroundColor Green
        }
    } finally {
        Pop-Location
    }
}

# 5. Inicialização Opcional do Git
if ($InitGit) {
    Write-Host "[+] Inicializando repositório Git local..." -ForegroundColor Magenta
    Push-Location $TargetDir
    try {
        git init -b main
        git add .
        git commit -m "feat: scaffold universal do projeto $ProjectName com Design System Tatil Melki"
        Write-Host "[PASS] Repositório Git inicializado com commit inaugural." -ForegroundColor Green
    } catch {
        Write-Warning "Aviso: Não foi possível inicializar o Git: $_"
    } finally {
        Pop-Location
    }
}

# 6. Resumo Executivo
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " PROVISIONAMENTO CONCLUÍDO COM SUCESSO!                   " -ForegroundColor Green
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "Diretório do Projeto : $TargetDir" -ForegroundColor White
Write-Host "Especificação de UI  : $TargetDir\docs\frontend.design.md" -ForegroundColor White
Write-Host "Bússola Cognitiva    : $TargetDir\docs\CONTEXT.md" -ForegroundColor White
Write-Host "Entrada da Aplicação : $TargetDir\src\App.tsx" -ForegroundColor White
Write-Host ""
Write-Host "Próximos passos sugeridos:" -ForegroundColor Yellow
Write-Host "  1. cd '$TargetDir'" -ForegroundColor Gray
Write-Host "  2. npm install" -ForegroundColor Gray
Write-Host "  3. npm run dev" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan
