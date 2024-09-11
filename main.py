import os
import shutil
import nltk
from bs4 import BeautifulSoup
import epub_utils
import translator
import time


# def process_contents(html_path):
#     html_content = epub_utils.__read_html(html_path)
#     soup = BeautifulSoup(html_content, 'html.parser')
#     p_tags = soup.find_all('p')
#
#     for tag in p_tags:
#         text = tag.get_text().replace('\n', '').strip()
#         sentences = split_sentences(text)
#         if len(sentences) == 0:
#             continue
#         elif len(sentences) > 1:
#             tag.string = ' '.join(translator.batch_translate(sentences))
#         else:
#             tag.string = translator.translate(sentences)
#
#     return str(soup)


def process_contents(html_path):
    html_content = epub_utils.__read_html(html_path)
    soup = BeautifulSoup(html_content, 'html.parser')
    p_tags = soup.find_all('p')

    print("preprocessing")
    group = []
    tag_sentence_count = {}
    for index, tag in enumerate(p_tags):
        text = tag.get_text().replace('\n', '').strip()
        sentences = split_sentences(text)
        tag_sentence_count[index] = len(sentences)
        if len(sentences) > 1:
            for sentence in sentences:
                group.append(sentence)
        elif len(sentences) == 1:
            group.append(sentences[0])

    if len(p_tags) != len(tag_sentence_count):
        raise Exception("Tag numbers dont match")

    print("translating")
    translated = []
    size = 8
    for i in range(0, len(group), size):
        chunk = group[i:i + size]
        # for sentence in translator.batch_translate(chunk):
        #     translated.append(sentence)
        for sentence in chunk:
            translated.append(sentence)
        print(min(len(group), i + size), " / ", len(group))

    print("postprocessing")
    begin = 0
    for index, tag in enumerate(p_tags):
        sentcount = tag_sentence_count.get(index)
        # print(tag, sentcount)
        # print()
        if sentcount:
            tag.string = ' '.join(translated[begin:begin + sentcount])
            begin += sentcount

    return str(soup)


def split_sentences(text):
    return nltk.sent_tokenize(text)


def process_book(epub_path, temp_path, output_path):
    epub_utils.extract_epub(epub_path, temp_path)

    contents = epub_utils.get_html_lengths(temp_path)
    print("book contents:")
    for key, value in contents.items():
        print(os.path.basename(key), "\t\t", value)

    for path in contents.keys():
        print("processing ", path)
        processed = process_contents(path)
        epub_utils.write_html(path, processed)

    epub_utils.recreate_epub(temp_path, output_path)


def main():
    # epub_path = r"test/resources/wonderland.epub"
    epub_path = r"sideTesting/CurbingTraffic.epub"
    output_path = r"sideTesting/output/exportBook.epub"
    temp_path = "sideTesting/extracted_epub"
    if os.path.exists(output_path):
        os.remove(output_path)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


    start_time = time.time()
    process_book(epub_path, temp_path, output_path)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time} seconds')

main()
