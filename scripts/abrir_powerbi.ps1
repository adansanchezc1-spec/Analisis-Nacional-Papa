# Script PowerShell para iniciar y desplegar el dashboard en Power BI Desktop
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "INICIANDO ENTORNO DE DESPLIEGUE POWER BI - PAPA COLOMBIA (2019-2025)" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan

# 1. Regenerar datos si es necesario
Write-Host "`n[1/3] Verificando datos del Modelo Estrella en data/POWERBI..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe scripts/export_powerbi.py

# 2. Abrir carpetas de datos y scripts en Windows Explorer
Write-Host "`n[2/3] Abriendo carpetas de trabajo en el explorador de archivos..." -ForegroundColor Yellow
Start-Process explorer.exe (Resolve-Path "data/POWERBI").Path
Start-Process explorer.exe (Resolve-Path "powerbi").Path

# 3. Lanzar Power BI Desktop
Write-Host "`n[3/3] Lanzando Microsoft Power BI Desktop..." -ForegroundColor Green
Start-Process "shell:AppsFolder\Microsoft.MicrosoftPowerBIDesktop_8wekyb3d8bbwe!Microsoft.MicrosoftPowerBIDesktop"

Write-Host "`n[OK] Power BI Desktop iniciado correctamente." -ForegroundColor Green
Write-Host "Consulta el manual paso a paso en: docs/03-development/manual_usuario_powerbi.md" -ForegroundColor White
