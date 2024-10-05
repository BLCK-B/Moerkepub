import logging

import pytest
import language_codes
import json

test_codes_path = r'resources/test_codes.json'
json_all_codes = {}


@pytest.fixture(autouse=True)
def before_each():
    global json_all_codes
    with open(test_codes_path, 'r') as file:
        json_all_codes = json.load(file)


def test_map_language_model_key():
    model_langs = dict()
    model_langs['deu_Latn'] = ['deu']

    mapped = language_codes.map_languages(model_langs, test_codes_path)

    assert 'deu_Latn' in mapped


def test_map_more_languages():
    model_langs = dict()
    model_langs['deu_Latn'] = ['deu']
    model_langs['ice_Latn'] = ['ice']

    mapped = language_codes.map_languages(model_langs, test_codes_path)

    assert len(mapped) == 2


def test_map_language_original_fields():
    model_langs = dict()
    model_langs['deu_Latn'] = ['deu']

    mapped = language_codes.map_languages(model_langs, test_codes_path)['deu_Latn']

    assert mapped['alpha3-b'] == 'ger'
    assert mapped['alpha3-t'] == 'deu'
    assert mapped['alpha2'] == 'de'
    assert mapped['English'] == 'German'


def test_map_language_unknown_code(caplog):
    model_langs = dict()
    model_langs['unk_known'] = ['unk']

    with caplog.at_level(logging.WARNING):
        mapped = language_codes.map_languages(model_langs, test_codes_path)

    assert any(record.levelname == "WARNING" for record in caplog.records)


def test_map_language_wrong_input(caplog):
    with pytest.raises(ValueError):
        mapped = language_codes.map_languages('wrong', test_codes_path)


