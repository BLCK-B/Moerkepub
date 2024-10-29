import json
import os
import platform
from pathlib import Path

settings_file = 'settings.json'


def load():
    default_settings = {
        'selected_model': 'none',
        'selected_hw': 'cpu'
    }
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as json_file:
            return json.load(json_file)
    else:
        with open(settings_file, 'w') as json_file:
            json.dump(default_settings, json_file, indent=4)
        return default_settings


def __save__(settings):
    with open(settings_file, 'w') as json_file:
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
