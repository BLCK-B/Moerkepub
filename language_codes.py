import json
import keyboard
import os


def __find__(user_input, languages):
    user_input = user_input.lower()
    suggestions = set()

    for lang in languages:
        if (lang['alpha2'] and lang['alpha2'].lower().startswith(user_input)) or \
                (lang['alpha3-b'] and lang['alpha3-b'].lower().startswith(user_input)) or \
                (lang['alpha3-t'] and lang['alpha3-t'].lower().startswith(user_input)) or \
                (lang['English'] and lang['English'].lower().startswith(user_input)):
            code_parts = []

            for field in lang.values():
                if field:
                    code_parts.append(field)

            suggestions.add(" - ".join(code_parts))

    return list(suggestions)


def search():
    with open(r'sideTesting/language_codes.json', 'r') as file:
        languages = json.load(file)

        user_input = ""
        while True:
            print(f"\r{user_input}", end='')
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'backspace':
                    user_input = user_input[:-1]
                elif event.name == 'enter':
                    print("\nYou entered:", user_input)
                    user_input = ""
                elif len(event.name) == 1:
                    user_input += event.name

                if len(user_input) >= 2:
                    os.system('cls||clear')
                    suggestions = __find__(user_input, languages)
                    if suggestions:
                        for suggestion in sorted(suggestions):
                            print(suggestion)
                        print('\n')
                    else:
                        print("\nNo language found.")
