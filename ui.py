import language_codes
import settings_screen
import text_processor
import os
import persistence
from translations import translations
from colorama import Fore, Style

output_path = ''
temp_path = r'extracted.epub'
json_codes_path = 'language_codes.json'


def main():
    persistence.ensure_program_files()
    os.system('cls||clear')
    while True:
        json_settings = persistence.load()
        print('--- Ebook translator ---')
        print("1. Settings")
        print("2. Translate")
        print("3. Translate - bilingual")
        print("4. Exit")
        print()
        print('selected model:', json_settings['selected_model'])
        if json_settings.get('selected_hw') == "cuda":
            print('selected hardware: cuda')
        else:
            print(Fore.RED + "selected hardware: CPU - very slow!\n" + Style.RESET_ALL)

        choice = input('\n')
        os.system('cls||clear')

        if choice == 'd':
            print('nothing')

        elif choice == '1':
            settings_screen.show()

        elif choice == '2' or choice == '3':
            if json_settings['selected_model'] == "none":
                input('select a model first')
                continue
            input_file = input("Drag and drop EPUB file.\n\n")
            input_file = input_file.replace('\"', '')
            _, extension = os.path.splitext(input_file)
            extension = extension.lower()
            if extension != '.epub':
                print(f"Wrong input", extension)
                continue

            global output_path
            output_path = f"{os.path.splitext(input_file)[0]}_translated.epub"

            json_settings = persistence.load()
            translator = translations(json_settings.get('selected_model'))
            model_langs = translator.get_language_codes()
            mapped_langs = language_codes.map_languages(model_langs, json_codes_path)

            source_lang = language_codes.search(mapped_langs, 'Select source language (start typing):')
            os.system('cls||clear')
            target_lang = language_codes.search(mapped_langs, f'Source: {source_lang}. Select target language (start '
                                                              f'typing):')
            os.system('cls||clear')

            print("Loading model...")
            translator.instantiate_model(json_settings.get('selected_hw'), source_lang, target_lang)
            os.system('cls||clear')

            match extension:
                case '.epub':
                    process_epub(translator, input_file, bilingual=(choice == '3'))
                case '.txt':
                    print(f"Processing TXT file")

        elif choice == '4':
            print("Ebook translator exited.")
            break


def process_epub(translator, input_file, bilingual):
    html_objects = text_processor.book_init(input_file, temp_path, output_path)

    while True:
        confirm = input("\nConfirm translate y/n: ").strip().lower()
        if confirm.lower() == 'y':
            text_processor.process_book_files(translator, html_objects, temp_path, output_path, bilingual)
            input(Fore.GREEN + f'\nBook translated.' + Style.RESET_ALL)
            os.system('cls||clear')
            return
        elif confirm.lower() == 'n':
            input(Fore.RED + "Translation canceled." + Style.RESET_ALL)
            return


main()
