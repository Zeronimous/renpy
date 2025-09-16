# Herramienta de Traduccion para Ren'Py

Este conjunto de herramientas te ayuda a extraer textos de un juego de Ren'Py, prepararlos para una traduccion comoda, y reinyectarlos de vuelta en el juego.

## Prerrequisitos

- Python 3
- pip (Instalador de paquetes de Python)

## Flujo de Trabajo de Traduccion (5 Pasos)

### Paso 1: Extraer los textos del juego al archivo JSON
Coloca los scripts `renpy_translator.py` y `translator_helper.py` en la carpeta raiz de tu juego (donde esta el `.exe`).

Primero, asegurate de tener las dependencias necesarias. Puedes instalarlas con pip:
```bash
pip install rpycdec
```
Para evitar problemas con multiples instalaciones de Python (muy comun en Windows), se recomienda usar este comando:
```bash
python -m pip install rpycdec
```
Luego, para prevenir errores de codificacion en la consola de Windows, ejecuta el script de extraccion con el siguiente comando:
```bash
# Para PowerShell
$env:PYTHONUTF8=1; python renpy_translator.py extract

# Para CMD (Simbolo del sistema)
set PYTHONUTF8=1 && python renpy_translator.py extract
```
Este comando creara (o actualizara) un archivo llamado `translations.json`, que contiene todos los textos del juego en un formato estructurado.

### Paso 2: Exportar los textos a un archivo `.txt` para traducir
Ahora, usa el script de ayuda para convertir el complejo archivo `.json` en un simple archivo de texto `.txt` que puedes editar facilmente.

Ejecuta el siguiente comando:
```bash
python translator_helper.py export
```
Esto creara un archivo llamado `translations.txt`.

### Paso 3: Traducir el archivo `.txt`
Abre `translations.txt` con cualquier editor de texto. Veras una lista numerada de todos los dialogos. Simplemente traduce cada linea, manteniendo el numero y el parentesis al principio.

**Ejemplo:**
```
1) Complete the puzzle.
2) Hint
```
**Despues de traducir:**
```
1) Completa el puzle.
2) Pista
```
**Importante:** No borres ni anadas lineas. El numero de lineas debe ser exactamente el mismo antes y despues de traducir.

### Paso 4: Importar las traducciones de vuelta al archivo JSON
Una vez que hayas terminado de traducir el `.txt`, usa el script de ayuda de nuevo para inyectar tus traducciones en el archivo `.json`.

Ejecuta el siguiente comando:
```bash
python translator_helper.py import
```
Este comando leera tu `translations.txt`, tomara las traducciones y actualizara el archivo `translations.json`, rellenando los campos `"translation"`.

### Paso 5: Inyectar las traducciones en el juego
Finalmente, usa el primer script de nuevo para tomar el `translations.json` actualizado e inyectar los textos traducidos directamente en los archivos del juego.

Ejecuta el comando:
```bash
# Para PowerShell
$env:PYTHONUTF8=1; python renpy_translator.py inject translations.json

# Para CMD (Simbolo del sistema)
set PYTHONUTF8=1 && python renpy_translator.py inject translations.json
```
¡Y listo! Ahora puedes iniciar el juego para ver tus traducciones.

## Disclaimer

- Estas herramientas modifican los archivos de script del juego. Se recomienda encarecidamente **crear una copia de seguridad de la carpeta del juego** antes de empezar.
- La extraccion de texto usa expresiones regulares y puede que no capture el 100% del texto en juegos con formatos muy inusuales, pero esta disenada para los casos mas comunes.
- Cualquier error en el proceso de traduccion (como borrar una linea en el `.txt`) podria causar errores al inyectar los textos.
