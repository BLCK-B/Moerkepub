from huggingface_hub import snapshot_download
import os
from colorama import Fore, Style


def download(model_name):
    os.system('cls||clear')
    print(f'downloading: {model_name}')
    repo = ''
    folder = ''
    if model_name == 'NLLB200':
        repo = 'BLCK-B/nllb-ctranslate-int8'
        folder = r'models/downloaded/nllb-ctranslate-int8'
    elif model_name == 'small100':
        repo = 'BLCK-B/small100-quantized'
        folder = r'models/downloaded/small100-quantized'
    else:
        return

    snapshot_download(repo_id=repo, local_dir=folder, cache_dir=None)
    input(Fore.YELLOW + 'model downloaded: {model_name}\n' + Style.RESET_ALL)
