# Redmine Hours

Automatización para registrar horas en Redmine. Muestra un popup para ingresar horas y comentarios por tarea, luego hace login y completa los formularios automáticamente.

**Compatible con Windows y Linux** - Instalación fácil para usuarios no técnicos.

## Requisitos

- Google Chrome instalado
- **Windows**: No se requiere Python (usa el .exe)
- **Linux**: Python 3

---

## Instalación en Windows (para usuarios finales)

### Opción A: Usando el ejecutable (.exe) - **MÁS FÁCIL**

1. Descarga el archivo ZIP con los archivos
2. Descomprime en una carpeta
3. Haz doble clic en `INSTALAR.bat`
4. Responde las preguntas que te hace el instalador
5. ¡Listo!

**Ver [README_WINDOWS.txt](README_WINDOWS.txt) para instrucciones detalladas.**

### Opción B: Usando Python en Windows

```cmd
pip install -r requirements.txt
python redmine_hours.py --install
```

---

## Instalación en Linux

```bash
cp .env.example .env
make deps
make install
```

---

## Configuración

### Configuración automática (Windows)

El script `INSTALAR.bat` te guiará para configurar todo automáticamente.

### Configuración manual

Edita `.env` con tus datos:

```env
REDMINE_USER=tu_usuario
REDMINE_PASSWORD=tu_contraseña
CRON_HOUR=15
HEADLESS=false

TASK_1_NAME=Proyecto A
TASK_1_URL=https://redmine.ejemplo.com/projects/a/time_entries/new

TASK_2_NAME=Soporte #123
TASK_2_URL=https://redmine.ejemplo.com/issues/123/time_entries/new

TASK_3_NAME=Otro proyecto
TASK_3_URL=https://redmine.ejemplo.com/issues/456/time_entries/new
```

### Variables

- `REDMINE_USER`: Tu usuario de Redmine
- `REDMINE_PASSWORD`: Tu contraseña de Redmine
- `CRON_HOUR`: Hora del día en que aparece el popup (formato 24hs). Ejemplos: `9` = 9:00am, `15` = 3:00pm, `18` = 6:00pm
- `HEADLESS`: Ejecutar Chrome sin ventana visible (`true` o `false`) por defecto esta desactivado

### Tareas

Cada tarea tiene dos líneas:

- `TASK_X_NAME`: Nombre que aparece en el popup
- `TASK_X_URL`: URL del formulario de carga de horas

Podés agregar tantas tareas como quieras (TASK_1, TASK_2, TASK_3, etc.).

**Nota:** Si el nombre tiene `#`, usá comillas: `TASK_2_NAME="Soporte #123"`

Ver [.env.example](.env.example) para ejemplos detallados.

---

## Uso

### Windows (con .exe)

**Automático**: El popup aparecerá de lunes a viernes a la hora configurada.

**Manual**: Doble clic en `redmine_hours.exe`

### Linux

| Comando          | Descripción                            |
| ---------------- | -------------------------------------- |
| `make run`       | Ejecutar popup manualmente             |
| `make install`   | Configurar ejecución automática (cron) |
| `make uninstall` | Quitar ejecución automática            |
| `make status`    | Ver cron actual                        |
| `make deps`      | Instalar dependencias Python           |

### Usando Python directamente

```bash
# Ejecutar manualmente
python redmine_hours.py

# Instalar ejecución automática
python redmine_hours.py --install

# Desinstalar
python redmine_hours.py --uninstall
```

---

## Compilar ejecutable para Windows (para desarrolladores)

### Requisitos

- Python 3 instalado
- Dependencias instaladas: `pip install -r requirements.txt`

### Compilar

```cmd
BUILD.bat
```

Esto generará:

- `dist/redmine_hours.exe` - El ejecutable standalone
- `dist/INSTALAR.bat` - Script de instalación
- `dist/DESINSTALAR.bat` - Script de desinstalación
- `dist/.env.example` - Plantilla de configuración

Para distribuir, comprime toda la carpeta `dist/` en un ZIP.

### Compilación manual con PyInstaller

```bash
pyinstaller redmine_hours.spec
```

---

## Cómo funciona

1. Se abre un popup donde podés:
   - Asignar horas a cada tarea (dejá en 0 las que no apliquen)
   - Escribir un comentario diferente para cada tarea

2. La herramienta:
   - Hace login automáticamente en Redmine
   - Registra las horas en cada proyecto
   - Muestra un resumen de lo registrado

Solo se registran las tareas con horas > 0.

---

## Arquitectura

### Compatibilidad multiplataforma

El código detecta automáticamente el sistema operativo:

- **Windows**: Usa Task Scheduler (`schtasks`)
- **Linux/macOS**: Usa crontab

### Estructura del proyecto

```
redmine_hours/
├── redmine_hours.py      # Script principal
├── requirements.txt      # Dependencias Python
├── redmine_hours.spec    # Configuración PyInstaller
├── .env.example          # Plantilla de configuración
├── INSTALAR.bat          # Instalador Windows
├── DESINSTALAR.bat       # Desinstalador Windows
├── BUILD.bat             # Compilador de .exe
├── README_WINDOWS.txt    # Guía para usuarios finales
├── README.md             # Este archivo
└── Makefile              # Comandos para Linux
```

---

## Solución de problemas

### Windows

Ver [README_WINDOWS.txt](README_WINDOWS.txt) para soluciones detalladas.

### Linux

- **El popup no aparece**: Verifica que la variable `DISPLAY=:0` en el cron sea correcta para tu sistema
- **Error de permisos**: Ejecuta `chmod +x redmine_hours.py`
- **ChromeDriver no funciona**: Se descarga automáticamente, pero asegúrate de tener Chrome instalado

---

## Notas

- La herramienta funciona tanto con proyectos como con issues de Redmine
- Las URLs deben terminar en `/time_entries/new`
- En Linux, la ejecución automática requiere que tengas sesión gráfica iniciada
- En Windows, funciona aunque no estés logueado (si la PC está encendida)

---

## Contribuir

Pull requests son bienvenidos. Para cambios grandes, abre un issue primero para discutir qué te gustaría cambiar.

---

## Licencia

MIT
