import os
import shutil
import nltk
from bs4 import BeautifulSoup
import epub_utils
import time
import copy


def print_progress(name, progress):
    print(f"{progress} %   {os.path.basename(name)}")


def process_contents(html_path, bilingual):
    html_content = epub_utils.read_html(html_path)
    soup = BeautifulSoup(html_content, 'html.parser')
    p_tags = soup.find_all('p')

    group, tag_sentence_count = preprocess(p_tags)
    if len(p_tags) != len(tag_sentence_count):
        raise Exception("Tag numbers dont match")

    # translated = translate(group, batch_size=4, name=html_path)
    translated = group
    new_tags = apply_translated(translated, p_tags, tag_sentence_count)

    if not bilingual:
        for original_tag, new_tag in zip(p_tags, new_tags):
            if new_tag.string is not None:
                original_tag.clear()
                original_tag.append(new_tag.string)
    else:
        for original_tag, new_tag in zip(p_tags, new_tags):
            if new_tag.string is not None:
                original_tag.append(BeautifulSoup(str(new_tag), 'html.parser'))
                original_tag.append(BeautifulSoup('<p><br/></p>', 'html.parser'))
    return str(soup)


def preprocess(p_tags):
    print("preprocessing")
    group = []
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
                group.append(sentence)
        elif len(sentences) == 1:
            group.append(sentences[0])
    return group, tag_sentence_count


def translate(group, batch_size, name):
    import translator
    print("translating")
    translated = []
    for i in range(0, len(group), batch_size):
        chunk = group[i:i + batch_size]

        chunk_translated = translator.batch_translate(chunk)
        # chunk_translated = chunk

        for num in range(min(batch_size, len(chunk_translated))):
            if len(chunk_translated[num]) < 5 * len(chunk[num]):
                translated.append(chunk_translated[num])
            else:
                translated.append(chunk[num])
        progress = round(min(len(group), i + batch_size) / len(group) * 100)
        print_progress(name, progress)
    return translated


def apply_translated(translated, p_tags, tag_sentence_count):
    print("postprocessing")
    new_tags = copy.deepcopy(p_tags)
    begin = 0
    for index, tag in enumerate(new_tags):
        sentcount = tag_sentence_count.get(index)
        if sentcount:
            tag.string = ' '.join(translated[begin:begin + sentcount])
            begin += sentcount
    return new_tags


def split_sentences(text):
    return nltk.sent_tokenize(text)


def process_book(temp_path, output_path, bilingual=False):
    for path in contents.keys():
        print("processing ", path)
        processed = process_contents(path, bilingual)
        epub_utils.write_html(path, processed)

    epub_utils.recreate_epub(temp_path, output_path)


def book_init(epub_path, temp_path, output_path):
    global contents
    if os.path.exists(output_path):
        os.remove(output_path)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    epub_utils.extract_epub(epub_path, temp_path)

    contents = epub_utils.get_html_lengths(temp_path)
    print("\nBook contents (html, characters):")
    for key, value in contents.items():
        print(os.path.basename(key), "\t\t", value)


contents = {}


# ------------------------------------------------------


def main():
    # epub_path = r"tests/resources/wonderland.epub"
    epub_path = r"sideTesting/diary.epub"
    output_path = r"sideTesting/output/exportBook.epub"
    temp_path = "sideTesting/extracted.epub"
    if os.path.exists(output_path):
        os.remove(output_path)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    start_time = time.time()
    book_init(epub_path, temp_path, output_path)
    process_book(temp_path, output_path)
    elapsed_time = time.time() - start_time
    print(f'\nDone! Full processing time: {elapsed_time} seconds')


if __name__ == '__main__':
    main()
