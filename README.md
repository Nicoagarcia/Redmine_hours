# Redmine Hours

Automatización para registrar horas en Redmine. Muestra un popup para ingresar horas y comentarios por tarea, luego hace login y completa los formularios automáticamente.

**Compatible con Windows y Linux**

## Requisitos

- Python 3
- Google Chrome

## Instalación

### Windows

```cmd
python redmine_hours.py
```

**Las dependencias se instalan automáticamente la primera vez.**

### Linux

```bash
cp .env.example .env
make deps
```

## Configuración

Copia `.env.example` como `.env` y editalo con tus datos:

```env
REDMINE_USER=tu_usuario
REDMINE_PASSWORD=tu_contraseña
CRON_HOUR=15
HEADLESS=false

TASK_1_NAME=Proyecto A
TASK_1_URL=https://redmine.ejemplo.com/projects/a/time_entries/new

TASK_2_NAME=Soporte #123
TASK_2_URL=https://redmine.ejemplo.com/issues/123/time_entries/new
```

### Variables

- `REDMINE_USER`: Tu usuario de Redmine
- `REDMINE_PASSWORD`: Tu contraseña de Redmine
- `CRON_HOUR`: Hora del día (0-23). Ejemplos: `9` = 9am, `15` = 3pm, `18` = 6pm
- `HEADLESS`: Chrome oculto (`true` o `false`)

### Tareas

- `TASK_X_NAME`: Nombre que aparece en el popup
- `TASK_X_URL`: URL del formulario de carga de horas

Agrega tantas como necesites (TASK_1, TASK_2, TASK_3...).

**Nota:** Si el nombre tiene `#`, usá comillas: `TASK_2_NAME="Soporte #123"`

## Uso

### Windows

```cmd
# Ejecutar manualmente
python redmine_hours.py

# Configurar ejecución automática
python redmine_hours.py --install

# Quitar ejecución automática
python redmine_hours.py --uninstall
```

### Linux

```bash
# Ejecutar manualmente
make run

# Configurar ejecución automática
make install

# Quitar ejecución automática
make uninstall
```

Se abre un popup donde asignas horas y comentarios. Solo se registran las tareas con horas > 0.

## Ejecución automática

Ejecuta `--install` para que el script se ejecute automáticamente de lunes a viernes a la hora configurada.

- **Windows**: Usa Task Scheduler
- **Linux**: Usa crontab

Para cambiar la hora, edita `CRON_HOUR` en `.env` y ejecuta `--install` de nuevo.

## Notas

- En Windows, las dependencias se instalan automáticamente
- En Linux, ejecuta `make deps` primero
- El script detecta el sistema operativo automáticamente
