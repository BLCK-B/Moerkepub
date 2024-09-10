import pytest
import os
import shutil
import main
from unittest.mock import patch

text = [  # lengths: 34, 31, 31 | 23, 15, 37 | 34, 39 | 17
    "Rabbit-hole, dipped suddenly down. So suddenly that Alice had not? She found herself falling down.",
    "She tried to look down. She took a jar! She put it into one of the cupboards.",
    "“Well!” thought Alice, downstairs! How brave they’ll all think me at home.",
    "Down, down, down."
]

epub_path = r"resources/wonderland.epub"
temp_path = r"resources/extracted"


def test_split_sentences():
    sentences = main.split_sentences(text[2])
    assert len(sentences) == 2


def test_sentence_list_from_tags():
    sentences = main.get_sentence_list_from_tags(text)

    assert len(sentences) == 9


@patch('token_counter.count_tokens')
def test_prepare_translation_texts(mock_count_tokens):
    mock_count_tokens.side_effect = lambda text: len(text)

    result = main.prepare_translation_texts(text, token_limit=100)

    assert len(result) == 3


@patch('token_counter.count_tokens')
def test_prepare_translation_texts_exceed_limit(mock_count_tokens):
    mock_count_tokens.side_effect = lambda text: len(text)

    result = main.prepare_translation_texts(text, token_limit=10)

    assert len(result) == 9


@patch('token_counter.count_tokens')
def test_prepare_translation_texts_unlimited(mock_count_tokens):
    mock_count_tokens.side_effect = lambda text: len(text)

    result = main.prepare_translation_texts(text, token_limit=10000)

    assert len(result) == 1