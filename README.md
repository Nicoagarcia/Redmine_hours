# Redmine Hours

Automatización para registrar horas en Redmine. Muestra un popup para ingresar horas y comentarios por tarea, luego hace login y completa los formularios automáticamente.

## Requisitos

- Python 3
- Google Chrome

## Instalación

```bash
cp .env.example .env
make deps
```

## Configuración

Edita `.env` con tus datos:

```
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

## Comandos

| Comando          | Descripción                            |
| ---------------- | -------------------------------------- |
| `make run`       | Ejecutar popup manualmente             |
| `make install`   | Configurar ejecución automática (cron) |
| `make uninstall` | Quitar ejecución automática            |
| `make status`    | Ver cron actual                        |
| `make deps`      | Instalar dependencias Python           |

## Uso

```bash
make run
```

Se abre un popup donde podés:

- Asignar horas a cada tarea (dejá en 0 las que no apliquen)
- Escribir un comentario diferente para cada tarea

Solo se registran las tareas con horas > 0.

## Ejecución automática

```bash
make install
```

Configura un cron que ejecuta el script de lunes a viernes a la hora definida en `CRON_HOUR`.

Para cambiar la hora, edita `CRON_HOUR` en `.env` y ejecuta `make install` de nuevo.
