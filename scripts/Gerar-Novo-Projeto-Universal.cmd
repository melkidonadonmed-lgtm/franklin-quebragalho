@echo off
setlocal EnableDelayedExpansion
title Scaffolder Universal Melki - Gerador de Projetos 2026
chcp 65001 >nul

echo ==========================================================
echo    SCAFFOLDER UNIVERSAL MELKI 2026 - TACTILE MATTE BASE   
echo ==========================================================
echo.

set "PROJECT_NAME=%~1"

if "%PROJECT_NAME%"=="" (
    set /p "PROJECT_NAME=Digite o nome da pasta do novo projeto (ex: meu-novo-app): "
)

if "%PROJECT_NAME%"=="" (
    echo [ERRO] O nome do projeto não pode ser vazio. Abortando.
    pause
    exit /b 1
)

echo.
echo [+] Iniciando provisionamento do projeto: %PROJECT_NAME%
echo [+] Destino padrao: C:\Users\melki\Projetos\%PROJECT_NAME%
echo.

where pwsh >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "C:\Users\melki\dev\franklin-quebragalho\scripts\scaffold-universal-app.ps1" -ProjectName "%PROJECT_NAME%" -DestinationPath "C:\Users\melki\Projetos"
) else (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\melki\dev\franklin-quebragalho\scripts\scaffold-universal-app.ps1" -ProjectName "%PROJECT_NAME%" -DestinationPath "C:\Users\melki\Projetos"
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha durante o provisionamento.
    pause
    exit /b %ERRORLEVEL%
)

echo.
set /p "OPEN_EXPLORER=Deseja abrir a pasta do projeto no Windows Explorer? (S/N): "
if /i "%OPEN_EXPLORER%"=="S" (
    explorer "C:\Users\melki\Projetos\%PROJECT_NAME%"
)

echo.
echo Pressione qualquer tecla para encerrar...
pause >nul
