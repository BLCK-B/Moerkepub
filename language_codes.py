import json
import logging
import os
from pynput import keyboard

# https://iso639-3.sil.org/code_tables/639/data

def __find_by_code__(search_code, json_all_codes):
    if isinstance(search_code, list):
        search_code = str(search_code[0])

    for lang in json_all_codes:
        if (lang['alpha2'] and lang['alpha2'].lower() == search_code) or \
                (lang['alpha3-b'] and lang['alpha3-b'].lower() == search_code) or \
                (lang['alpha3-t'] and lang['alpha3-t'].lower() == search_code):
            return lang
    return None


def map_languages(model_langs, json_path):
    with open(json_path, 'r') as file:
        json_all_codes = json.load(file)

    mapped_json = {}
    if isinstance(model_langs, dict):
        for model_key, link_code in model_langs.items():
            json_entry = __find_by_code__(link_code, json_all_codes)
            if not json_entry:
                logging.warning(f'Language code missing: {link_code}, originally: {model_key}.')
                continue
            mapped_json[model_key] = json.loads(json.dumps(json_entry))
            mapped_json[model_key]['model-key'] = model_key

    elif isinstance(model_langs, list):
        print("not done yet")

    else:
        raise ValueError('model_langs must be a list or a dict')

    return mapped_json


def __find_suggestions__(user_input, json_mapped, modelKeyOnly=False):
    user_input = user_input.lower()
    suggestions = []
    json_values = json_mapped.values() if isinstance(json_mapped, dict) else json_mapped

    for lang in json_values:
        if (lang['alpha2'] and lang['alpha2'].lower().startswith(user_input)) or \
                (lang['alpha3-b'] and lang['alpha3-b'].lower().startswith(user_input)) or \
                (lang['alpha3-t'] and lang['alpha3-t'].lower().startswith(user_input)) or \
                (lang['English'] and lang['English'].lower().startswith(user_input)) or \
                (lang['model-key'] and lang['model-key'].lower().startswith(user_input)):

            code_parts = []
            if modelKeyOnly:
                return lang.get("model-key")
            for field in lang.values():
                if field:
                    code_parts.append(field)
            suggestions.append(code_parts)

    return list(suggestions)

def search(json_mapped, message):
    user_input = ''
    prev_suggestions = []
    print(message + '\n')
    with keyboard.Events() as events:
        while True:
            event = events.get(1.0)
            if event is not None:
                if isinstance(event, keyboard.Events.Press):
                    if event.key == keyboard.Key.backspace:
                        user_input = user_input[:-1]
                    elif event.key == keyboard.Key.enter:
                        if len(prev_suggestions) == 1:
                            return __find_suggestions__(user_input, json_mapped, True)
                        else:
                            print("\nSpecify a single language.")
                            continue
                    elif event.key == keyboard.Key.space:
                        user_input += ' '
                    elif isinstance(event.key, keyboard.KeyCode) and event.key.char is not None:
                        user_input += event.key.char

                os.system('cls||clear')
                print(message + '\n')
                if len(user_input) >= 2:
                    suggestions = __find_suggestions__(user_input, json_mapped)
                    prev_suggestions = suggestions
                    if suggestions:
                        for suggestion in sorted(suggestions):
                            print(' - '.join(suggestion))
                    else:
                        print("\nNo language found.")
                print(f"\n\r{user_input}", end='')

