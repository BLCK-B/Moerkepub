import zipfile
import os
import shutil
from bs4 import BeautifulSoup

import translator


def extract_epub():
    with zipfile.ZipFile(epub_path, 'r') as z:
        z.extractall(temp_path)


def get_html_files():
    html_files = []
    for root, dirs, files in os.walk(temp_path):
        for file in files:
            if file.endswith('.xhtml') or file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files


def read_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_html(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


# def process_content(content):
#     # primitive text
#     soup = BeautifulSoup(content, 'html.parser')
#     paragraphs = soup.find_all('p')
#     # replace word
#     for para in paragraphs:
#         para.string = translator.translate(para.get_text())
#         # para.string = para.get_text().replace('a', 'A')
#     return str(soup)

def process_content(content):
    # nodes modification
    soup = BeautifulSoup(content, 'html.parser')
    # for element in soup.find_all(string=True):
    #     if element.parent.name in ['span', 'p', 'h1', 'h2', 'h3', 'a']:
    #         print(element)
    #         # new_text = element.replace('a', 'A')
    #         # element.replace_with(new_text)

    # trying to optimize text
    elements = soup.find_all(string=True)
    textBody = []
    for i in range(len(elements)):
        element = elements[i]
        # only text-related tags
        if element.parent.name in ['span', 'p', 'h1', 'h2', 'h3', 'a']:
            # assemble coherent textBody and keep track of elements
            if not element.isspace():
                textBody.append(element)
            if sum(len(element) for element in textBody) >= 800 and textBody[-1].strip().endswith('.'):
                print(' '.join(textBody))
                print()
                textBody = []
    return str(soup)


def recreate_epub():
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(temp_path):
            for file in files:
                file_path = os.path.join(root, file)
                z.write(file_path, os.path.relpath(file_path, temp_path))


def process_book():
    extract_epub()
    html_files = get_html_files()
    for file_path in html_files:
        content = read_html(file_path)
        modified_content = process_content(content)
        write_html(file_path, modified_content)
    recreate_epub()


epub_path = r"sideTesting/diary.epub"
output_path = r"sideTesting/output/exportBook.epub"
temp_path = "sideTesting/extracted_epub"

if os.path.exists(output_path):
    os.remove(output_path)
if os.path.exists(temp_path):
    shutil.rmtree(temp_path)

process_book()
