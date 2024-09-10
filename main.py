import epub_utils
import zipfile
import os
import shutil
from bs4 import BeautifulSoup
import time
import re
import nltk
import token_counter


# import translator


def split_sentences(text):
    return nltk.sent_tokenize(text)


# given text nodes
# merge until length with sentence endings AND save sentence counts
# call batch translate with batch size
# print results
# when all, reconstruct by sentence counts
# return new tags

def process_contents(html_paths):
    for key, value in html_paths.items():
        text_tags = epub_utils.get_raw_texts(key)
        # for later reconstruction
        sentences_per_tag = []
        for tag in text_tags:
            sentences_per_tag.append(len(split_sentences(str(tag))))

        to_translate = prepare_translation_texts(text_tags, 90)
        for ttt in to_translate:
            print(ttt)
            print("----------")

    return html_paths


def get_sentence_list_from_tags(text_tags):
    sentences = [split_sentences(tag) for tag in text_tags]
    return [sentence for sublist in sentences for sentence in sublist]


def prepare_translation_texts(text_tags, token_limit):
    sentences = get_sentence_list_from_tags(text_tags)
    prepared_texts = []
    index = 0
    merged = sentences[0]
    tokens = token_counter.count_tokens(sentences[0])
    while index < len(sentences) - 1:
        next_tokens = token_counter.count_tokens(sentences[index + 1])
        if (tokens + next_tokens) < token_limit:
            tokens += next_tokens
            merged += ' ' + sentences[index + 1]
            index += 1
        else:
            prepared_texts.append(merged)
            tokens = 0
            merged = ""
            if next_tokens >= token_limit:
                index += 1
                merged = sentences[index]

    if len(merged) > 0:
        prepared_texts.append(merged)
    prepared_texts = [t.strip() for t in prepared_texts]
    return prepared_texts


# def process_contentOld(content):
#     soup = BeautifulSoup(content, 'html.parser')
#     paragraphs = soup.find_all('p')
#     bufferText = []
#     bufferPositions = []
#     bufferSentences = []
#     for index, para in enumerate(paragraphs):
#         para_text = para.get_text()
#         sentences = split_sentences(para_text)
#
#         bufferText.append(para_text)
#         bufferPositions.append((index, len(sentences)))
#         bufferSentences.extend(sentences)
#
#         if sum(len(text) for text in bufferText) >= 250 or index == len(paragraphs) - 1:
#             if len(bufferText) == 1 and len(bufferText[0]) > 250:
#                 translated_chunks = []
#                 for cluster in split_under_length(bufferText[0]):
#                     translated_chunks.append(translator.translate(cluster))
#                 translated_text = ' '.join([item for sublist in translated_chunks for item in(sublist if isinstance(sublist, list) else [sublist])])
#             else:
#                 translated_text = translator.translate(' '.join(bufferSentences).replace('\n', ''))
#
#             translated_sentences = split_sentences(translated_text)
#             for pos, (para_index, sentence_count) in enumerate(bufferPositions):
#                 sentences_in_para = translated_sentences[:sentence_count]
#                 translated_para_text = ' '.join(sentences_in_para)
#                 paragraphs[para_index].clear()
#                 paragraphs[para_index].append(translated_para_text)
#                 translated_sentences = translated_sentences[sentence_count:]
#             bufferText = []
#             bufferPositions = []
#             bufferSentences = []
#     return str(soup)


def process_book(epub_path, temp_path, output_path):
    epub_utils.extract_epub(epub_path, temp_path)

    contents = epub_utils.get_html_lengths(temp_path)

    print("book contents:")
    for key, value in contents.items():
        print(os.path.basename(key), "\t", value)

    process_contents(contents)

    epub_utils.recreate_epub(temp_path, output_path)


def main():
    # epub_path = r"test/resources/wonderland.epub"
    epub_path = r"sideTesting/comeback.epub"
    output_path = r"sideTesting/output/exportBook.epub"
    temp_path = "sideTesting/extracted_epub"
    if os.path.exists(output_path):
        os.remove(output_path)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    process_book(epub_path, temp_path, output_path)


main()
