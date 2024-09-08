import zipfile
import os
import shutil
from bs4 import BeautifulSoup
import time
import re
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

# define sentence endings . ? ! with ' '
# assemble array of position = tag pos and value = sentences
# translate coherent text
# split by those endings and reinsert to tags


# def process_content(content):
#     # primitive text
#     soup = BeautifulSoup(content, 'html.parser')
#     paragraphs = soup.find_all('p')
#     # replace word
#     start = time.time()
#     bufferText = []
#     for index in range(len(paragraphs)):
#         print(index, " / ", len(paragraphs))
#         bufferText.append(paragraphs[index].get_text())
#         paragraphs[index].clear()
#         if sum(len(element) for element in bufferText) >= 800 and bufferText[-1].strip().endswith('.') or index == len(paragraphs) - 1:
#             paragraphs[index].string = translator.translate(' '.join(bufferText))
#             bufferText = []
#     print("time: ", time.time() - start)
#     return str(soup)


def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())


def split_under_length(longLine):
    sentences = split_sentences(longLine)
    temp = []
    clustered = []
    for index, sent in enumerate(sentences):
        if sum(len(text) for text in temp) >= 200 or index == len(sentences) - 1:
            clustered.append(temp)
            temp = []
        else:
            temp.append(sent.replace('\n', ''))
    return clustered


def process_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    paragraphs = soup.find_all('p')
    start = time.time()
    bufferText = []
    bufferPositions = []
    bufferSentences = []
    for index, para in enumerate(paragraphs):
        print(index + 1, " / ", len(paragraphs))
        para_text = para.get_text()
        sentences = split_sentences(para_text)

        bufferText.append(para_text)
        bufferPositions.append((index, len(sentences)))
        bufferSentences.extend(sentences)

        if sum(len(text) for text in bufferText) >= 250 or index == len(paragraphs) - 1:
            if len(bufferText) == 1 and len(bufferText[0]) > 250:
                translated_chunks = []
                for cluster in split_under_length(bufferText[0]):
                    translated_chunks.append(translator.translate(cluster))
                translated_text = ' '.join([item for sublist in translated_chunks for item in(sublist if isinstance(sublist, list) else [sublist])])
            else:
                translated_text = translator.translate(' '.join(bufferSentences).replace('\n', ''))

            translated_sentences = split_sentences(translated_text)
            for pos, (para_index, sentence_count) in enumerate(bufferPositions):
                sentences_in_para = translated_sentences[:sentence_count]
                translated_para_text = ' '.join(sentences_in_para)
                paragraphs[para_index].clear()
                paragraphs[para_index].append(translated_para_text)
                translated_sentences = translated_sentences[sentence_count:]
            bufferText = []
            bufferPositions = []
            bufferSentences = []
    print("Time elapsed: ", time.time() - start)
    return str(soup)


# def process_content(content):
#     # nodes modification
#     soup = BeautifulSoup(content, 'html.parser')
#     # for element in soup.find_all(string=True):
#     #     if element.parent.name in ['span', 'p', 'h1', 'h2', 'h3', 'a']:
#     #         print(element)
#     #         # new_text = element.replace('a', 'A')
#     #         # element.replace_with(new_text)
#
#     # trying to optimize text
#     elements = soup.find_all(string=True)
#     textBody = []
#     for i in range(len(elements)):
#         element = elements[i]
#         # only text-related tags
#         if element.parent.name in ['span', 'p', 'h1', 'h2', 'h3', 'a']:
#             # assemble coherent textBody and keep track of elements
#             if not element.isspace():
#                 textBody.append(element.strip() + " ☻")
#             if sum(len(element) for element in textBody) >= 800 and textBody[-1].strip().endswith('.☻'):
#                 print(' '.join(textBody))
#                 translated = translator.translate(' '.join(textBody))
#                 print(translated)
#                 # print(' '.join(textBody))
#                 # print()
#                 textBody = []
    # return str(soup)


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


epub_path = r"sideTesting/CurbingTraffic.epub"
output_path = r"sideTesting/output/exportBook.epub"
temp_path = "sideTesting/extracted_epub"

if os.path.exists(output_path):
    os.remove(output_path)
if os.path.exists(temp_path):
    shutil.rmtree(temp_path)

process_book()
