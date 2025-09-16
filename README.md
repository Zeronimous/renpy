# Ren'Py Translation Tool

This tool helps you extract text from a Ren'Py game, translate it, and inject it back into the game.

## Prerequisites

- Python 3
- pip (Python package installer)

## How to Use

1.  **Place the script:** Put the `renpy_translator.py` script in the root directory of your Ren'Py game (the same folder that contains the game's `.exe` file).

2.  **Install dependencies:** The script requires the `rpycdec` library. It will attempt to detect if it's not installed, but you can also install it manually:
    ```bash
    pip install rpycdec
    ```

3.  **Extract the text:** Open a terminal or command prompt in the game's root directory and run the following command:
    ```bash
    python renpy_translator.py extract
    ```
    This command will:
    - Decompile the game's script files (`.rpyc` to `.rpy`).
    - Extract all the dialogue and menu options into a file named `translations.json`.

4.  **Translate the text:**
    - Open the `translations.json` file in a text editor.
    - For each entry, you will see an `"original"` field with the text to be translated, and an empty `"translation"` field.
    - **Fill in the `"translation"` field** with your translated text. Make sure the translated text is enclosed in double quotes.

    Example of a translation entry:
    ```json
    {
        "game/script.rpy:123": {
            "original": "\"Hello, world!\"",
            "translation": "",
            "character": "e",
            "trailing": ""
        }
    }
    ```
    After translation to Spanish, it would look like this:
    ```json
    {
        "game/script.rpy:123": {
            "original": "\"Hello, world!\"",
            "translation": "\"¡Hola, mundo!\"",
            "character": "e",
            "trailing": ""
        }
    }
    ```

5.  **Inject the translated text:** Once you have finished translating, run the following command:
    ```bash
    python renpy_translator.py inject translations.json
    ```
    This will take your translated text from the `"translation"` field and update the game's script files.

6.  **Test the game:** Launch the game to see your translations in action.

## Disclaimer

- This tool modifies the game's script files. It is highly recommended to **create a backup of your game folder** before using this tool.
- The text extraction uses regular expressions and may not capture every single piece of text in complex games. It is designed to capture the most common dialogue and menu formats.
- The injection process directly replaces text in the script files. Any errors in the translated JSON file could potentially break the game.
