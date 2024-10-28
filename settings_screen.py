import os

import model_download
import persistence
import torch
from colorama import Fore, Style


def show():
    while True:
        os.system('cls||clear')
        json_settings = persistence.load()
        model_name = json_settings['selected_model']
        print(f'1. Select translation model [ {model_name} ]')
        if json_settings.get('selected_hw') == 'cuda':
            print('2. Select hardware [cuda]')
        else:
            print(f'2. Select hardware [{Fore.RED} CPU - very slow! {Style.RESET_ALL}]')
        print()
        gpu_available = detect_gpu()

        if not gpu_available and json_settings['selected_hw'] == 'cuda':
            persistence.set(json_settings, 'selected_hw', 'cpu')
            json_settings = persistence.load()

        choice = input('\n')
        os.system('cls||clear')

        if choice == '1':
            print(f'Select translation model [ {model_name} ]')
            print()
            models_exist = check_models_downloaded()
            if models_exist['NLLB200']:
                print("1. NLLB200")
            else:
                print(Fore.YELLOW + "1. NLLB200 - available for download - 1.3 GB" + Style.RESET_ALL)
            if models_exist['small100']:
                print("2. small100")
            else:
                print(Fore.YELLOW + "2. small100 - available for download - 600 MB" + Style.RESET_ALL)
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

        elif choice == '2':
            if json_settings.get('selected_hw') == 'cuda':
                print('Select hardware [cuda]')
            else:
                print(f'Select hardware [{Fore.RED} CPU - very slow! {Style.RESET_ALL}]')
            print()
            print("1. cuda GPU") if gpu_available else print(Fore.YELLOW + "-. no cuda GPU detected" + Style.RESET_ALL)
            print("2. CPU")
            print()
            print_gpu()
            choice = input('\n')
            if choice == '1' and gpu_available:
                persistence.set(json_settings, 'selected_hw', 'cuda')
            elif choice == '2':
                persistence.set(json_settings, 'selected_hw', 'cpu')
        else:
            return


def detect_gpu():
    # todo: check without driver
    # todo: specify number
    return torch.cuda.is_available()


def print_gpu():
    if torch.cuda.is_available():
        print("CUDA is available:")
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("No CUDA GPU detected.")


def check_models_downloaded():
    models_exist = dict()
    models_exist['NLLB200'] = os.path.isfile(r'models/downloaded/nllb-ctranslate-int8/model.bin')
    models_exist['small100'] = os.path.isfile(r'models/downloaded/small100-quantized/model.safetensors')
    return models_exist
