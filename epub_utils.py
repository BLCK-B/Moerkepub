import zipfile
import os
from bs4 import BeautifulSoup
from collections import OrderedDict

import text_processor


def extract_epub(epub_path, temp_path):
    with zipfile.ZipFile(epub_path, 'r') as z:
        z.extractall(temp_path)


def read_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def __list_html_files(temp_path):
    html_files = []
    for root, dirs, files in os.walk(temp_path):
        for file in files:
            if file.endswith('.xhtml') or file.endswith('.html'):
                html_files.append(os.path.join(root, file).replace("\\", "/"))
    return html_files


def get_raw_texts(html_file_path):
    html = read_html(html_file_path)
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('p')
    texts = [tag.get_text() for tag in tags]
    texts = [text.replace('\n', ' ').strip() for text in texts]
    texts = [text.strip() for text in texts]
    return texts


def get_html_lengths(temp_path):
    html_files = __list_html_files(temp_path)
    html_files.sort()
    html_lengths = OrderedDict()
    for file in html_files:
        raw_texts = get_raw_texts(file)
        length = len(text_processor.split_sentences(''.join(raw_texts)))
        if length != 0:
            html_lengths[file] = length
    return html_lengths


def get_html_paths(temp_path):
    return __list_html_files(temp_path)


def write_html(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def recreate_epub(temp_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(temp_path):
            for file in files:
                file_path = os.path.join(root, file)
                z.write(file_path, os.path.relpath(file_path, temp_path))





