import pytest
import os
import shutil
import epub_utils as utils

epub_path = r"resources/wonderland.epub"
temp_path = r"resources/extracted"


@pytest.fixture(autouse=True)
def before_each():
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


def test_epub_extracted():
    utils.extract_epub(epub_path, temp_path)

    assert os.path.exists(temp_path)


def test_list_html():
    utils.extract_epub(epub_path, temp_path)

    html_files = utils.list_html_files(temp_path)

    assert len(html_files) > 0


def test_read_html():
    utils.extract_epub(epub_path, temp_path)
    html_files = utils.list_html_files(temp_path)

    contents = utils.read_html(html_files[0])

    assert len(contents) > 0


def test_html_lengths():
    utils.extract_epub(epub_path, temp_path)

    files_and_lengths = list(utils.get_html_lengths(temp_path).items())
    file_name, length = files_and_lengths[0]

    assert len(file_name) > 0 and length > 0
