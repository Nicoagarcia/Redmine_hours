@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo   Instalador de Redmine Hours Automation
echo.

if exist ".env" (
    choice /C SN /M "Ya existe un archivo .env. ¿Desea sobrescribirlo? (S/N)"
    if errorlevel 2 goto :skip_config
)


echo.
echo Configurando credenciales de Redmine...
echo.

set /p REDMINE_USER="Usuario de Redmine: "
if "!REDMINE_USER!"=="" (
    echo ERROR: El usuario no puede estar vacío.
    pause
    exit /b 1
)

set /p REDMINE_PASSWORD="Contraseña de Redmine: "
if "!REDMINE_PASSWORD!"=="" (
    echo ERROR: La contraseña no puede estar vacía.
    pause
    exit /b 1
)

set /p CRON_HOUR="Hora del día para el recordatorio (0-23, ejemplo: 15 para las 3pm): "
if "!CRON_HOUR!"=="" set CRON_HOUR=15

set /p HEADLESS="¿Ejecutar Chrome sin ventana visible? (true/false, por defecto false): "
if "!HEADLESS!"=="" set HEADLESS=false

echo.
echo Ahora configure las tareas de Redmine...
echo (Puede agregar hasta 10 tareas. Deje en blanco para terminar)
echo.

set TASK_COUNT=0

:task_loop
set /a TASK_NUM=!TASK_COUNT!+1

echo.
echo --- Tarea #!TASK_NUM! ---
set /p "TASK_NAME=Nombre de la tarea (Enter para terminar): "

if "!TASK_NAME!"=="" goto :end_tasks

set /p "TASK_URL=URL de la tarea: "
if "!TASK_URL!"=="" (
    echo ERROR: La URL no puede estar vacía.
    goto :task_loop
)

set TASK_!TASK_NUM!_NAME=!TASK_NAME!
set TASK_!TASK_NUM!_URL=!TASK_URL!

set /a TASK_COUNT+=1

if !TASK_COUNT! GEQ 10 goto :end_tasks

goto :task_loop

:end_tasks

if !TASK_COUNT! EQU 0 (
    echo.
    echo ERROR: Debe configurar al menos una tarea.
    pause
    exit /b 1
)


echo.
echo Generando archivo .env...

(
    echo # Configuración de Redmine Hours Automation
    echo.
    echo # Credenciales de Redmine
    echo REDMINE_USER=!REDMINE_USER!
    echo REDMINE_PASSWORD=!REDMINE_PASSWORD!
    echo.
    echo # Hora del día en que aparecerá el recordatorio ^(formato 24hs^)
    echo # Ejemplos: 9 = 9:00am, 15 = 3:00pm, 18 = 6:00pm
    echo CRON_HOUR=!CRON_HOUR!
    echo.
    echo # Ejecutar Chrome en modo oculto ^(sin ventana visible^)
    echo HEADLESS=!HEADLESS!
    echo.
    echo # Tareas de Redmine
    echo # Para cada tarea, especifica un nombre y la URL del formulario de carga de horas

    for /L %%i in (1,1,!TASK_COUNT!) do (
        echo.
        echo TASK_%%i_NAME=!TASK_%%i_NAME!
        echo TASK_%%i_URL=!TASK_%%i_URL!
    )
) > .env

echo.
echo ✓ Archivo .env creado correctamente

:skip_config

echo.
echo Configurando tarea programada de Windows...
echo.

if exist "redmine_hours.exe" (
    redmine_hours.exe --install
) else if exist "redmine_hours.py" (
    python redmine_hours.py --install
) else (
    echo ERROR: No se encontró redmine_hours.exe ni redmine_hours.py
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo configurar la tarea programada.
    echo Verifique que tiene permisos de administrador.
    pause
    exit /b 1
)

echo.
echo   ¡Instalación completada exitosamente!
echo.
echo La herramienta se ejecutará automáticamente
echo de lunes a viernes a las !CRON_HOUR!:00
echo.
echo Para ejecutar manualmente: doble clic en redmine_hours.exe
echo Para cambiar configuración: edite el archivo .env
echo Para desinstalar: ejecute DESINSTALAR.bat
echo.
pause
