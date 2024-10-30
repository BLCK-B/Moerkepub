import json
import os
import platform
from pathlib import Path


def load():
    path = get_appdata_path() / 'settings.json'
    default_settings = {
        'selected_model': 'none',
        'selected_hw': 'cpu'
    }
    if os.path.exists(path):
        with open(path, 'r') as json_file:
            return json.load(json_file)
    else:
        with open(path, 'w') as json_file:
            json.dump(default_settings, json_file, indent=4)
        return default_settings


def __save__(settings):
    with open(get_appdata_path() / 'settings.json', 'w') as json_file:
        json.dump(settings, json_file, indent=4)


def set(settings, key, value):
    settings[key] = value
    __save__(settings)


def get_appdata_path():
    system = platform.system()
    if system == "Windows":
        return Path(os.path.join(os.environ.get('APPDATA'), 'EbookTranslate'))
    elif system == "Linux":
        return Path.home() / '.config' / 'EbookTranslate'
    elif system == "Darwin":
        return Path.home() / 'Library' / 'Application Support' / 'EbookTranslate'
    else:
        raise ValueError("Unsupported operating system")


def ensure_program_files():
    appdata_path = get_appdata_path()
    appdata_path.mkdir(parents=False, exist_ok=True)
    downloaded = get_appdata_path() / 'models'
    downloaded.mkdir(parents=False, exist_ok=True)
