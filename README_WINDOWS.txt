========================================
  REDMINE HOURS - GUÍA DE USO
========================================

¿Qué hace esta herramienta?
---------------------------
Automatiza el registro de horas en Redmine. Te muestra un popup cada día
a la hora que configures, donde puedes ingresar las horas trabajadas en
cada proyecto, y la herramienta las registra automáticamente por ti.


REQUISITOS
==========

1. Tener Google Chrome instalado
2. Tener acceso a Redmine con usuario y contraseña


INSTALACIÓN (Primera vez)
==========================

1. Haz doble clic en "INSTALAR.bat"

2. El instalador te hará algunas preguntas:
   - Tu usuario de Redmine
   - Tu contraseña de Redmine
   - A qué hora quieres que aparezca el recordatorio cada día
   - Los proyectos/tareas donde registras horas habitualmente

3. ¡Listo! La herramienta está configurada.


CÓMO SE USA
===========

AUTOMÁTICAMENTE:
----------------
Cada día de lunes a viernes, a la hora configurada, aparecerá un popup
preguntándote cuántas horas trabajaste en cada proyecto.

Solo tienes que:
1. Ingresar las horas en cada proyecto (deja en 0 los que no apliquen)
2. Escribir un comentario si quieres
3. Hacer clic en "Registrar"

La herramienta se encargará de:
- Hacer login en Redmine
- Registrar las horas en cada proyecto
- Mostrarte un resumen de lo que se registró


MANUALMENTE:
------------
Si quieres registrar horas en cualquier momento sin esperar al horario
programado, simplemente haz doble clic en "redmine_hours.exe"


CAMBIAR LA CONFIGURACIÓN
=========================

¿Necesitas cambiar tu contraseña? ¿Agregar un nuevo proyecto?
¿Cambiar el horario del recordatorio?

1. Haz clic derecho en el archivo ".env"
2. Selecciona "Abrir con" → "Bloc de notas"
3. Modifica lo que necesites (las instrucciones están en el archivo)
4. Guarda y cierra

Los cambios se aplicarán la próxima vez que se ejecute.


DESINSTALAR
===========

Si quieres desinstalar la herramienta y que deje de ejecutarse
automáticamente:

1. Haz doble clic en "DESINSTALAR.bat"
2. Confirma que quieres desinstalar

Esto eliminará el recordatorio automático, pero no borrará tus archivos
de configuración por si quieres volver a usarla después.


SOLUCIÓN DE PROBLEMAS
======================

"No aparece el popup a la hora configurada"
-------------------------------------------
1. Verifica que tu computadora esté encendida y con sesión iniciada
   a esa hora
2. Revisa que la tarea esté configurada correctamente:
   - Presiona Windows + R
   - Escribe: taskschd.msc
   - Busca "RedmineHoursAutomation" en la lista
   - Haz clic derecho → "Ejecutar" para probarlo


"La herramienta no registra las horas correctamente"
-----------------------------------------------------
1. Verifica que tu usuario y contraseña en .env sean correctos
2. Verifica que las URLs de las tareas sean correctas
   (deben terminar en /time_entries/new)
3. Intenta ejecutar con HEADLESS=false para ver qué está pasando


"Chrome no se abre" o "Error de ChromeDriver"
----------------------------------------------
1. Asegúrate de tener Google Chrome instalado
2. Cierra todas las ventanas de Chrome
3. Vuelve a intentar


¿NECESITAS AYUDA?
=================

Si tienes algún problema o sugerencia, contacta al administrador
del sistema o al desarrollador de la herramienta.


========================================
Versión 2.0 - Soporte Windows
========================================
