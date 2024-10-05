import pytest
from bs4 import BeautifulSoup

import text_processor as processor

text = []
p_tags = []
translated = []


@pytest.fixture(autouse=True)
def renew_data():
    global text, p_tags, translated
    text = [  # lengths: 34, 31, 31 | 23, 15, 37 | 34, 39 | 17
        "Rabbit-hole, dipped suddenly down. So suddenly that Alice had not? She found herself falling down.",
        "She tried to look down. She took a jar! She put it into one of the cupboards.",
        "“Well!” thought Alice, downstairs! How brave they’ll all think me at home.",
        "Down, down, down."
    ]

    p_tags = [
        BeautifulSoup("<p> “Well!” thought Alice, downstairs! How brave they’ll all think me at home. </p>",
                      'html.parser'),
        BeautifulSoup("<p><span> Down, down, down. </span></p>", 'html.parser')
    ]

    translated = [
        "Nun, dachte Alice, nach unten!",
        "Wie mutig werden sie mich alle zu Hause finden.",
        "Runter, runter, runter."
    ]

    return text, p_tags, translated


epub_path = r"resources/wonderland.epub"
temp_path = r"resources/extracted"


def test_split_sentences():
    sentences = processor.split_sentences(text[2])

    assert len(sentences) == 2


def test_preprocess_splits_sentences():
    group, tag_sentence_count = processor.preprocess_html(p_tags)

    assert len(group) == 3


def test_preprocess_counts_sentences_per_tag():
    group, tag_sentence_count = processor.preprocess_html(p_tags)

    assert tag_sentence_count[0] == 2 and tag_sentence_count[1] == 1


def test_preprocess_cleans_whitespaces():
    group, tag_sentence_count = processor.preprocess_html(BeautifulSoup("<p>    Down,\ndown,\ndown.\n    </p>"))

    assert group[0] == "Down, down, down."


def test_preprocess_sentences_end_with_dot():
    p_tags.insert(0, BeautifulSoup("<p> I lost a dot </p>"))

    group, tag_sentence_count = processor.preprocess_html(p_tags)

    assert group[0] == "I lost a dot."


def test_preprocess_sentences_exclamation_unchanged():
    group, tag_sentence_count = processor.preprocess_html(BeautifulSoup("<p> Rabbit\ndown. </p>"))

    assert group[0] == "Rabbit down."


def test_preprocess_sentences_breakline_space():
    group, tag_sentence_count = processor.preprocess_html(p_tags)

    assert group[0].endswith('!')


def test_apply_translated_populates_tags():
    tag_sentence_count = {0: 2, 1: 1}

    processor.apply_translated(translated, p_tags, tag_sentence_count)

    assert len(p_tags) == 2


def test_apply_translated_joins_sentences():
    tag_sentence_count = {0: 2, 1: 1}

    new_tags = processor.apply_translated(translated, p_tags, tag_sentence_count)

    assert new_tags[0].string == 'Nun, dachte Alice, nach unten! Wie mutig werden sie mich alle zu Hause finden.'
    assert new_tags[1].string == 'Runter, runter, runter.'
