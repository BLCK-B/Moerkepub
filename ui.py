import os

import torch
from colorama import Fore, Style

import language_codes
import persistence
import settings_screen
import text_processor
from translations import translations

output_path = ''
temp_path = r'extracted.epub'
json_codes_path = 'language_codes.json'


def main():
    persistence.ensure_program_files()
    text_processor.download_nltk_resources()

    os.system('cls||clear')

    if not detect_gpu():
        print(Fore.YELLOW + 'Warning - no CUDA GPU detected.' + Style.RESET_ALL)

    while True:
        json_settings = persistence.load()
        print('--- Mørkepub ---')
        print("1. Translate")
        print("2. Translate - bilingual")
        print("3. Settings")
        print("4. About")
        print("5. Exit")
        print()
        print('selected model:', json_settings['selected_model'])
        print_gpu()

        choice = input('\n')
        os.system('cls||clear')

        if choice == 'd':
            print('nothing')

        elif choice == '1' or choice == '2':
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
            target_lang = language_codes.search(mapped_langs, f'Source: {source_lang}\nSelect target language (start '
                                                              f'typing):')
            os.system('cls||clear')

            print("Loading model...")
            translator.instantiate_model(source_lang, target_lang)
            os.system('cls||clear')
            process_epub(translator, input_file, bilingual=(choice == '2'))

        elif choice == '3':
            settings_screen.show()

        elif choice == '4':
            print('''
  .        *   .    .        .      *     .       .  *
        .         .        .     .           .     .  
.    .     .   .      .         .        .       .     
        *        .         .    *  .  .     .      .  
  .            .   Mørkepub         .           .        
    .      .                   .       .    .     .    
*       .        .   .     by             .           . 
   .     .        .                 .        *          
             .        .      BLCK    .          .   
  .    .    *  .     .     .       .          .     . 
.      .   .  .                   .     .         *  .
  .               .     .    .              .   .     
 .        .   .           .       *     .          .  
            ''')
            print('Version: 1')
            print('\nRepository: https://github.com/BLCK-B/Moerkepub')
            print('For more information, feedback, updates — see repository.')
            print(f'\nProgram files location: {persistence.get_appdata_path()}')
            print('\nCopyright 2024 BLCK')
            print('Licensed under the Apache License, Version 2.0')
            input('\n')
            os.system('cls||clear')

        elif choice == '5':
            print("Mørkepub exited.")
            break


def process_epub(translator, input_file, bilingual):
    input('source language: ')
    input('target language: ')
    html_objects = text_processor.book_init(input_file, temp_path, output_path)
    while True:
        confirm = input("\nConfirm translate y/n: ").strip().lower()
        if confirm.lower() == 'y':
            os.system('cls||clear')
            text_processor.process_book_files(translator, html_objects, temp_path, output_path, bilingual)
            input(Fore.GREEN + f'\nBook translated.' + Style.RESET_ALL)
            os.system('cls||clear')
            return
        elif confirm.lower() == 'n':
            os.system('cls||clear')
            input(Fore.RED + "Translation canceled." + Style.RESET_ALL)
            return


def detect_gpu():
    return torch.cuda.is_available()


def print_gpu():
    print("CUDA devices:")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")


main()
