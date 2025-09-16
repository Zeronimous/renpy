import os
import sys
import json
import re
import argparse
from collections import defaultdict

try:
    from rpycdec import decompile, extract_rpa
except ImportError:
    print("Error: rpycdec is not installed. Please install it using 'pip install rpycdec'")
    sys.exit(1)

def find_game_directory():
    """Finds the 'game' directory in the current path."""
    if os.path.isdir("game"):
        return "game"
    if os.path.basename(os.getcwd()) == "game":
        return "."
    files = os.listdir(".")
    for file in files:
        if file.endswith(".exe"):
            if os.path.isdir("game"):
                return "game"
    return None

def extract_rpa_archives(game_dir):
    """Finds and extracts .rpa archives."""
    print("Searching for .rpa archives...")
    for root, _, files in os.walk(game_dir):
        for file in files:
            if file.endswith(".rpa"):
                rpa_path = os.path.join(root, file)
                print(f"Extracting {rpa_path}...")
                try:
                    with open(rpa_path, "rb") as f:
                        extract_rpa(f, root)
                    print(f"Successfully extracted {rpa_path}")
                except Exception as e:
                    print(f"Error extracting {rpa_path}: {e}")

def decompile_rpyc_files(game_dir):
    """Finds and decompiles .rpyc files."""
    print("Searching for .rpyc files to decompile...")
    for root, _, files in os.walk(game_dir):
        for file in files:
            if file.endswith(".rpyc"):
                rpyc_path = os.path.join(root, file)
                rpy_path = rpyc_path[:-1]
                if os.path.exists(rpy_path):
                    print(f"Skipping {rpyc_path} as {os.path.basename(rpy_path)} already exists.")
                    continue
                print(f"Decompiling {rpyc_path}...")
                try:
                    decompile(rpyc_path)
                    print(f"Successfully decompiled {rpyc_path} to {rpy_path}")
                except Exception as e:
                    print(f"Error decompiling {rpyc_path}: {e}")

def extract_text(game_dir):
    """Extracts translatable strings from .rpy files."""
    print("Extracting translatable text...")
    translations = {}
    # This regex now captures the character, the dialogue, and any trailing content.
    dialogue_regex = re.compile(r'^\s*(?:([a-zA-Z0-9_]+)\s)?("[^"]+")(.*)$')
    menu_regex = re.compile(r'^\s*("[^"]+"):$')

    for root, _, files in os.walk(game_dir):
        for file in files:
            if file.endswith(".rpy"):
                rpy_path = os.path.join(root, file)
                try:
                    with open(rpy_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            match = dialogue_regex.match(line.strip())
                            if match:
                                key = f"{rpy_path}:{i+1}"
                                translations[key] = {
                                    "original": match.group(2),
                                    "translation": "",
                                    "character": match.group(1),
                                    "trailing": match.group(3)
                                }
                            else:
                                match = menu_regex.match(line.strip())
                                if match:
                                    key = f"{rpy_path}:{i+1}"
                                    translations[key] = {
                                        "original": match.group(1),
                                        "translation": "",
                                        "character": "menu",
                                        "trailing": ":"
                                    }
                except Exception as e:
                    print(f"Error reading {rpy_path}: {e}")

    output_file = "translations.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(translations, f, indent=4, ensure_ascii=False)

    print(f"Extracted {len(translations)} strings. Translations saved to {output_file}")
    print("Please fill in the 'translation' fields in this file and then run the injection step.")

def inject_text(translated_file):
    """Injects translated strings back into .rpy files."""
    print(f"Injecting translations from {translated_file}...")

    try:
        with open(translated_file, "r", encoding="utf-8") as f:
            translations = json.load(f)
    except FileNotFoundError:
        print(f"Error: Translated file not found at {translated_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {translated_file}")
        return

    grouped_translations = defaultdict(dict)
    for key, value in translations.items():
        if value.get("translation"):
            try:
                path, line_num_str = key.rsplit(":", 1)
                line_num = int(line_num_str)
                grouped_translations[path][line_num] = value
            except ValueError:
                print(f"Warning: Could not parse key '{key}'. Skipping.")
                continue

    for rpy_path, line_translations in grouped_translations.items():
        try:
            with open(rpy_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_num, trans_data in line_translations.items():
                original_line = lines[line_num - 1]
                original_text = trans_data["original"]
                translated_text = trans_data["translation"]

                # Use re.sub for a safe replacement
                new_line, count = re.subn(re.escape(original_text), translated_text, original_line)
                if count == 1:
                    lines[line_num - 1] = new_line
                else:
                    print(f"Warning: Could not find or replaced multiple instances of text in {rpy_path}:{line_num}. Line not changed.")

            with open(rpy_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            print(f"Successfully processed {rpy_path}")

        except FileNotFoundError:
            print(f"Warning: File not found at {rpy_path}. Skipping.")
        except Exception as e:
            print(f"Error processing {rpy_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="A tool to assist in translating Ren'Py games.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser("extract", help="Extracts all translatable text from the game's scripts.")

    inject_parser = subparsers.add_parser("inject", help="Injects translated text back into the game's scripts.")
    inject_parser.add_argument("translated_file", help="The JSON file with the translated text.")

    args = parser.parse_args()

    if args.command == "extract":
        print("--- Extraction Mode ---")
        game_dir = find_game_directory()
        if not game_dir:
            print("Error: 'game' directory not found. Please run this script from the root of your Ren'Py game.")
            sys.exit(1)

        print(f"Found game directory: {game_dir}")
        extract_rpa_archives(game_dir)
        decompile_rpyc_files(game_dir)
        extract_text(game_dir)
        print("\nExtraction complete.")

    elif args.command == "inject":
        print("--- Injection Mode ---")
        inject_text(args.translated_file)
        print("\nInjection complete.")

if __name__ == "__main__":
    main()
