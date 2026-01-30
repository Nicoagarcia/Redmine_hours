@echo off
chcp 65001 >nul


echo.
echo   Compilando Redmine Hours a ejecutable
echo.

python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller no está instalado. Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias.
        pause
        exit /b 1
    )
)


if exist "dist" (
    echo Limpiando compilación anterior...
    rmdir /s /q dist
)
if exist "build" (
    rmdir /s /q build
)


echo.
echo Compilando con PyInstaller...
echo (Esto puede tomar algunos minutos)
echo.

pyinstaller redmine_hours.spec

if errorlevel 1 (
    echo.
    echo ERROR: La compilación falló.
    pause
    exit /b 1
)

echo.
echo Copiando archivos necesarios...

copy INSTALAR.bat dist\ >nul
copy DESINSTALAR.bat dist\ >nul
copy .env.example dist\ >nul

if exist "README_WINDOWS.txt" (
    copy README_WINDOWS.txt dist\ >nul
)

echo.
echo.
echo El ejecutable está en la carpeta: dist\
echo.
echo Archivos generados:
echo   - redmine_hours.exe
echo   - INSTALAR.bat
echo   - DESINSTALAR.bat
echo   - .env.example
echo.
echo Para distribuir: comprime toda la carpeta dist\ en un ZIP
echo.
pause
