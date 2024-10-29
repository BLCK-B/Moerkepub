from huggingface_hub import snapshot_download
import os
from colorama import Fore, Style

import persistence


def download(model_name):
    os.system('cls||clear')
    print(f'downloading: {model_name}')
    repo = ''
    folder = ''
    appdata = persistence.get_appdata_path()
    if model_name == 'NLLB200':
        repo = 'BLCK-B/nllb-ctranslate-int8'
        folder = appdata / 'models' / 'nllb-ctranslate-int8'
    elif model_name == 'small100':
        repo = 'BLCK-B/small100-quantized'
        folder = appdata / 'models' / 'small100-quantized'
    else:
        return

    snapshot_download(repo_id=repo, local_dir=folder, cache_dir=None)
    input(Fore.GREEN + 'model downloaded: {model_name}\n' + Style.RESET_ALL)


def check_models_downloaded():
    models_exist = dict()
    appdata = persistence.get_appdata_path()
    models_exist['NLLB200'] = os.path.isfile(appdata / 'models' / 'nllb-ctranslate-int8' / 'model.bin')
    models_exist['small100'] = os.path.isfile(appdata / 'models' / 'small100-quantized' / 'model.safetensors')
    return models_exist
