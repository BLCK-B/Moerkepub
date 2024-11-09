import os

from colorama import Fore, Style

import model_download
import persistence


def show():
    while True:
        os.system('cls||clear')
        json_settings = persistence.load()
        model_name = json_settings['selected_model']
        print(f'1. Select translation model [ {model_name} ]')

        choice = input('\n')
        os.system('cls||clear')

        if choice == '1':
            print(f'Select translation model [ {model_name} ]')
            print()
            models_exist = model_download.check_models_downloaded()
            if models_exist['NLLB200']:
                print("1. NLLB200")
            else:
                print(Fore.YELLOW + "1. NLLB200 - available for download [1.3 GB]" + Style.RESET_ALL)
            if models_exist['small100']:
                print("2. small100")
            else:
                print(Fore.YELLOW + "2. small100 - available for download [0.6 GB]" + Style.RESET_ALL)
            choice = input('\n')
            if choice == '1':
                if models_exist['NLLB200']:
                    persistence.set(json_settings, 'selected_model', 'NLLB200')
                else:
                    if input("download NLLB200? [y]\n") == 'y':
                        model_download.download('NLLB200')
            elif choice == '2':
                if models_exist['small100']:
                    persistence.set(json_settings, 'selected_model', 'small100')
                else:
                    if input("download small100? [y]\n") == 'y':
                        model_download.download('small100')
        else:
            return
