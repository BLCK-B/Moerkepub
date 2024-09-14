import os
import shutil
import nltk
from bs4 import BeautifulSoup
import epub_utils
import time


def process_contents(html_path):
    html_content = epub_utils.read_html(html_path)
    soup = BeautifulSoup(html_content, 'html.parser')
    p_tags = soup.find_all('p')

    group, tag_sentence_count = preprocess(p_tags)
    if len(p_tags) != len(tag_sentence_count):
        raise Exception("Tag numbers dont match")
    translated = translate(group, batch_size=8)
    apply_translated(translated, p_tags, tag_sentence_count)
    return str(soup)


def preprocess(p_tags):
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
    return group, tag_sentence_count


def translate(group, batch_size):
    import translator
    print("translating")
    translated = []
    for i in range(0, len(group), batch_size):
        chunk = group[i:i + batch_size]
        # for sentence in translator.batch_translate(chunk):
        #     translated.append(sentence)
        for sentence in chunk:
            translated.append(sentence)
        print(min(len(group), i + batch_size), " / ", len(group))
    return translated


def apply_translated(translated, p_tags, tag_sentence_count):
    print("postprocessing")
    begin = 0
    for index, tag in enumerate(p_tags):
        sentcount = tag_sentence_count.get(index)
        # print(tag, sentcount)
        # print()
        if sentcount:
            tag.string = ' '.join(translated[begin:begin + sentcount])
            begin += sentcount


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
    epub_path = r"sideTesting/diary.epub"
    output_path = r"sideTesting/output/exportBook.epub"
    temp_path = "sideTesting/extracted_epub"
    if os.path.exists(output_path):
        os.remove(output_path)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    start_time = time.time()
    process_book(epub_path, temp_path, output_path)
    elapsed_time = time.time() - start_time
    print(f'Full processing time: {elapsed_time} seconds')


if __name__ == '__main__':
    main()
