import json
import os

settings_file = 'settings.json'


def load():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as json_file:
            return json.load(json_file)
    else:
        return {}


def __save__(settings):
    with open(settings_file, 'w') as json_file:
        json.dump(settings, json_file, indent=4)


def set(settings, key, value):
    settings[key] = value
    __save__(settings)