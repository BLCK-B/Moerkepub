import pytest
import os
import shutil
import main
from unittest.mock import patch
from bs4 import BeautifulSoup

text = [  # lengths: 34, 31, 31 | 23, 15, 37 | 34, 39 | 17
    "Rabbit-hole, dipped suddenly down. So suddenly that Alice had not? She found herself falling down.",
    "She tried to look down. She took a jar! She put it into one of the cupboards.",
    "“Well!” thought Alice, downstairs! How brave they’ll all think me at home.",
    "Down, down, down."
]

p_tags = [
    BeautifulSoup("<p> “Well!” thought Alice, downstairs! How brave they’ll all think me at home. </p>"),
    BeautifulSoup("<p><span> Down, down, down. </span></p>"),
]

epub_path = r"resources/wonderland.epub"
temp_path = r"resources/extracted"


def test_split_sentences():
    sentences = main.split_sentences(text[2])

    assert len(sentences) == 2


def test_preprocess_splits_sentences():
    group, tag_sentence_count = main.preprocess(p_tags)

    assert len(group) == 3


def test_preprocess_counts_sentences_per_tag():
    group, tag_sentence_count = main.preprocess(p_tags)

    assert tag_sentence_count[0] == 2 and tag_sentence_count[1] == 1


def test_preprocess_cleans_whitespaces():
    group, tag_sentence_count = main.preprocess(BeautifulSoup("<p>    Down,\n down,\n down.\n    </p>"))

    assert group[0] == "Down, down, down."


# @patch('token_counter.count_tokens')
# def test_preprocess_returns_sentences(mock_count_tokens):
#     mock_count_tokens.side_effect = lambda text: len(text)
#
#     result = main.prepare_translation_texts(text, token_limit=100)
#
#     assert len(result) == 3