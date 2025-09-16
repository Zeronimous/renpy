import json
import argparse
import sys
import os

TRANSLATIONS_JSON = "translations.json"
TRANSLATIONS_TXT = "translations.txt"

def export_texts():
    """
    Lee el archivo translations.json, extrae los textos originales,
    y los escribe en un archivo numerado translations.txt.
    """
    if not os.path.exists(TRANSLATIONS_JSON):
        print(f"Error: El archivo '{TRANSLATIONS_JSON}' no fue encontrado.")
        print("Por favor, ejecuta primero el script 'renpy_translator.py extract'.")
        sys.exit(1)

    try:
        with open(TRANSLATIONS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: El archivo '{TRANSLATIONS_JSON}' no es un JSON valido o esta corrupto.")
        sys.exit(1)

    print(f"Exportando {len(data)} lineas desde '{TRANSLATIONS_JSON}' a '{TRANSLATIONS_TXT}'...")

    with open(TRANSLATIONS_TXT, 'w', encoding='utf-8') as f:
        for i, key in enumerate(data.keys()):
            original_text = data[key].get("original", "")

            # Quita las comillas del principio y del final para obtener el texto limpio
            if original_text.startswith('"') and original_text.endswith('"'):
                text_to_translate = original_text[1:-1]
            else:
                text_to_translate = original_text

            # Reemplaza saltos de linea literales con un espacio para facilitar la traduccion en una sola linea
            text_to_translate = text_to_translate.replace('\\n', ' ')

            f.write(f"{i+1}) {text_to_translate}\n")

    print("Exportacion completada.")
    print(f"Por favor, edita el archivo '{TRANSLATIONS_TXT}' con tus traducciones.")

def import_texts():
    """
    Lee los textos traducidos desde translations.txt y los inyecta
    en el campo 'translation' de translations.json.
    """
    if not os.path.exists(TRANSLATIONS_JSON):
        print(f"Error: El archivo '{TRANSLATIONS_JSON}' no fue encontrado.")
        sys.exit(1)

    if not os.path.exists(TRANSLATIONS_TXT):
        print(f"Error: El archivo '{TRANSLATIONS_TXT}' no fue encontrado.")
        print("Por favor, ejecuta primero el modo 'export' para crearlo.")
        sys.exit(1)

    with open(TRANSLATIONS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(TRANSLATIONS_TXT, 'r', encoding='utf-8') as f:
        translated_lines = f.readlines()

    json_keys = list(data.keys())

    if len(translated_lines) != len(json_keys):
        print("Error: El numero de lineas en 'translations.txt' no coincide con el numero de entradas en 'translations.json'.")
        print("Asegurate de no haber anadido o eliminado ninguna linea en 'translations.txt'.")
        sys.exit(1)

    print(f"Importando {len(translated_lines)} traducciones desde '{TRANSLATIONS_TXT}' a '{TRANSLATIONS_JSON}'...")

    for i, key in enumerate(json_keys):
        line = translated_lines[i]

        try:
            # Extrae el texto despues de 'X) '
            content_start_index = line.index(' ') + 1
            translated_text = line[content_start_index:].strip()
        except ValueError:
            print(f"Aviso: La linea {i+1} en '{TRANSLATIONS_TXT}' parece estar vacia o mal formada. Se usara un texto vacio.")
            translated_text = ""

        # Formatea el texto de vuelta a "..." para que sea un string literal valido en Ren'Py
        formatted_translation = f'"{translated_text}"'
        data[key]["translation"] = formatted_translation

    with open(TRANSLATIONS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Importacion completada.")
    print(f"El archivo '{TRANSLATIONS_JSON}' ha sido actualizado con las traducciones.")
    print("Ahora puedes usar el script 'renpy_translator.py inject' para aplicar los cambios al juego.")


def main():
    parser = argparse.ArgumentParser(
        description="Una herramienta de ayuda para facilitar la traduccion de los textos extraidos del juego.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comandos disponibles")

    # Comando para exportar
    parser_export = subparsers.add_parser(
        "export",
        help="Extrae los textos del archivo translations.json a un archivo translations.txt, facil de editar."
    )

    # Comando para importar
    parser_import = subparsers.add_parser(
        "import",
        help="Importa los textos traducidos desde translations.txt de vuelta al archivo translations.json."
    )

    args = parser.parse_args()

    if args.command == "export":
        export_texts()
    elif args.command == "import":
        import_texts()

if __name__ == "__main__":
    main()
