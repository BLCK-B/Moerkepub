import copy
import os
import shutil
from progress.bar import IncrementalBar
import time

import nltk
from bs4 import BeautifulSoup

import epub_utils


def split_sentences(text):
    return nltk.sent_tokenize(text)


def apply_translated(translated, p_tags, tag_sentence_count):
    new_tags = copy.deepcopy(p_tags)
    begin = 0
    for index, tag in enumerate(new_tags):
        sentcount = tag_sentence_count.get(index)
        if sentcount:
            tag.string = ' '.join(translated[begin:begin + sentcount])
            begin += sentcount
    return new_tags


def process_contents(html_object, bilingual):
    html_path = html_object.get('html_name')
    html_content = epub_utils.read_html(html_path)
    soup = BeautifulSoup(html_content, 'html.parser')
    p_tags = soup.find_all('p')

    import translator
    translated = translator.translate(html_object.get('sentence_list'), batch_size=4, name=html_path)
    # translated = group
    new_tags = apply_translated(translated, p_tags, html_object.get('tag_sentence_count'))

    for original_tag, new_tag in zip(p_tags, new_tags):
        if new_tag.string is not None:
            if not bilingual:
                original_tag.clear()
                original_tag.append(new_tag.string)
            else:
                original_tag.append(BeautifulSoup(str(new_tag), 'html.parser'))
                original_tag.append(BeautifulSoup('<p><br/></p>', 'html.parser'))
    return str(soup)


def process_book_files(html_objects, temp_path, output_path, bilingual=False):
    total_sentences = sum(len(obj.get('sentence_list', [])) for obj in html_objects)
    start_time = time.time()
    processed_sentences = 0
    for obj in html_objects:
        print(f'\nElapsed: {round((time.time() - start_time) / 60)} min')
        with IncrementalBar('\nTotal:', max=total_sentences, suffix='%(index)d / %(max)d', index=processed_sentences) as bar:
            processed_soup = process_contents(obj, bilingual)
            epub_utils.write_html(obj.get('html_name'), processed_soup)
            processed_sentences += len(obj.get('sentence_list'))
            bar.goto(processed_sentences)
            os.system('cls')

    epub_utils.recreate_epub(temp_path, output_path)


def preprocess_html(p_tags):
    sentence_list = []
    tag_sentence_count = {}
    for index, tag in enumerate(p_tags):
        text = tag.get_text().replace('\n', ' ').strip()
        sentences = split_sentences(text)
        for i, sentence in enumerate(sentences):
            sentences[i] = sentences[i].strip()
            if not (sentence.endswith('.') or sentence.endswith('!') or sentence.endswith('?')):
                sentences[i] += '.'
        tag_sentence_count[index] = len(sentences)
        if len(sentences) > 1:
            for sentence in sentences:
                sentence_list.append(sentence)
        elif len(sentences) == 1:
            sentence_list.append(sentences[0])
    return sentence_list, tag_sentence_count


def preprocess_book(htmls):
    html_objects = []
    for html in htmls:
        html_content = epub_utils.read_html(html)
        soup = BeautifulSoup(html_content, 'html.parser')
        p_tags = soup.find_all('p')

        sentence_list, tag_sentence_count = preprocess_html(p_tags)
        if len(sentence_list) > 0:
            html_objects.append({
                "html_name": html,
                "sentence_list": sentence_list,
                "tag_sentence_count": tag_sentence_count
            })
    return html_objects


def book_init(epub_path, temp_path, output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    epub_utils.extract_epub(epub_path, temp_path)
    htmls = epub_utils.get_html_paths(temp_path)

    html_objects = preprocess_book(htmls)

    print("\nBook contents (file, sentences):")
    for obj in html_objects:
        print(os.path.basename(obj.get('html_name')), "\t\t", len(obj.get('sentence_list')))

    return html_objects
