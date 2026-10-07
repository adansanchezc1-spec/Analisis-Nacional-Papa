@echo off
chcp 65001 > nul
echo ==============================================================================
echo INICIANDO ENTORNO DE DESPLIEGUE POWER BI - PAPA COLOMBIA (2019-2025)
echo ==============================================================================
echo.
echo [1/3] Verificando y regenerando tablas del Modelo Estrella en data\POWERBI...
call .\.venv\Scripts\python.exe scripts\export_powerbi.py
echo.
echo [2/3] Abriendo carpeta con los datos y el modelo dimensional...
start explorer.exe "%~dp0..\data\POWERBI"
start explorer.exe "%~dp0..\powerbi"
echo.
echo [3/3] Lanzando Microsoft Power BI Desktop...
start "" "shell:AppsFolder\Microsoft.MicrosoftPowerBIDesktop_8wekyb3d8bbwe!Microsoft.MicrosoftPowerBIDesktop"
echo.
echo ==============================================================================
echo [OK] Power BI Desktop iniciado. Sigue el manual en docs\03-development\manual_usuario_powerbi.md
echo ==============================================================================
pause
