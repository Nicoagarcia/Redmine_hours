@echo off
chcp 65001 >nul

echo.
echo   Desinstalador de Redmine Hours Automation
echo.

choice /C SN /M "¿Está seguro que desea desinstalar la tarea programada? (S/N)"
if errorlevel 2 goto :cancel

echo.
echo Desinstalando tarea programada...
echo.

if exist "redmine_hours.exe" (
    redmine_hours.exe --uninstall
) else if exist "redmine_hours.py" (
    python redmine_hours.py --uninstall
) else (
    echo ERROR: No se encontró redmine_hours.exe ni redmine_hours.py
    pause
    exit /b 1
)

echo.
echo   Desinstalación completada
echo.
echo La tarea programada ha sido eliminada.
echo.
echo NOTA: El archivo .env no se eliminó. Puede eliminarlo
echo       manualmente si lo desea.
echo.
pause
exit /b 0

:cancel
echo.
echo Desinstalación cancelada.
echo.
pause
exit /b 0
