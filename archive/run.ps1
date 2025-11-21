# ====================================================================
# Скрипт запуска конвертера Docling для PowerShell
# ====================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Запуск конвертера Docling            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Переходим в папку скрипта
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Активируем виртуальное окружение
Write-Host "[1/2] Активация виртуального окружения..." -ForegroundColor Yellow

$venvPath = "..\venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "     ✅ Окружение активировано" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ ОШИБКА: Не найден venv" -ForegroundColor Red
    Write-Host "   Путь: $venvPath" -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}

Write-Host ""

# Запускаем конвертер
Write-Host "[2/2] Запуск конвертера..." -ForegroundColor Yellow
python converter.py

Write-Host ""

if ($LASTEXITCODE -eq 0) {
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║   ✅ Конвертер завершил работу         ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
} else {
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║   ❌ Конвертер завершился с ошибкой    ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Red
}

Write-Host ""
Write-Host "Нажмите любую клавишу для выхода..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
