import json
import os
import time

import language_codes
from translations import translations
import text_processor

output_path = r"sideTesting/output/exportBook.epub"
temp_path = r"sideTesting/extracted.epub"
json_codes_path = r"sideTesting/language_codes.json"


def main():
    os.system('cls')
    while True:
        print("1. Settings")
        print("2. Translate")
        print("3. Translate bilingual")
        print("4. Exit")

        choice = input("Select 1-3: ")
        os.system('cls')
        if choice == '0':
            epub_path = r"sideTesting/diary.epub"

            text_processor.book_init(epub_path, temp_path, output_path)

            confirm = input("\nConfirm translate y/n: ")
            if confirm.lower() == 'y':
                start_time = time.time()
                print("missing here")
                elapsed_time = time.time() - start_time
                print(f'Full processing time: {round(elapsed_time)} seconds')
            else:
                print("Translation canceled.")

        elif choice == 'd':

            print("Loading model...")
            translator = translations('NLLB200', 'cuda', 'eng')
            model_langs = translator.get_language_codes()
            mapped_langs = language_codes.map_languages(model_langs, json_codes_path)
            os.system('cls')

            source_lang = language_codes.search(mapped_langs, 'Select source language.')
            os.system('cls||clear')
            target_lang = language_codes.search(mapped_langs, f'Source: {source_lang}. Select target language.')
            os.system('cls||clear')
            print(f'{source_lang} -> {target_lang}')
            print(input())

        elif choice == '1':
            while True:
                os.system('cls')
                print("0. Back")
                print("1. NLLB GPU")
                print("2. NLLB CPU")
                print("3. small100 CPU")
                print("4. small100 CPU")
                choice = input("Select: ")
                if choice == '0':
                    os.system('cls')
                    break
                elif choice == '1':
                    print("ok")
                elif choice == '2':
                    print("ok")
                elif choice == '3':
                    print("ok")
                elif choice == '4':
                    print("ok")

        elif choice == '2' or choice == '3':
            input_file = input("Drag and drop EPUB | TXT file.\n\n")
            input_file = input_file.replace('\"', '')
            _, extension = os.path.splitext(input_file)
            extension = extension.lower()
            if extension == '':
                print(f"Wrong input", extension)
                continue
            os.system('cls')

            print("Loading model...")
            translator = translations('NLLB200', 'cuda', 'eng') # todo: set target lang
            os.system('cls')

            model_langs = translator.get_language_codes()
            mapped_langs = language_codes.map_languages(model_langs, json_codes_path)
            os.system('cls')

            source_lang = language_codes.search(mapped_langs, 'Select source language.')
            os.system('cls||clear')
            target_lang = language_codes.search(mapped_langs, f'Source: {source_lang}. Select target language.')
            os.system('cls||clear')
            translator.set_target_lang(target_lang) # todo: get model key
            match extension:
                case '.epub':
                    process_epub(translator, input_file, bilingual=(choice == '3'))
                case '.txt':
                    print(f"Processing TXT file")
                case _:
                    print(f"Unsupported file type: ", extension)
                    continue

        elif choice == '4':
            print("Ebook translator exited.")
            break


def process_epub(translator, input_file, bilingual):
    html_objects = text_processor.book_init(input_file, temp_path, output_path)

    confirm = None
    while confirm not in ['y', 'n']:
        confirm = input("\nConfirm translate y/n: ").strip().lower()
        os.system('cls')

    if confirm.lower() == 'y':
        text_processor.process_book_files(translator, html_objects, temp_path, output_path, bilingual)
        input(f'\nBook translated!')
        os.system('cls')
    else:
        input("Translation canceled.")


main()
