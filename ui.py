import os
import shutil
import time
import argparse
import text_processor as processor


def main():
    # epub_path = r"tests/resources/wonderland.epub"
    epub_path = r"sideTesting/diary.epub"
    output_path = r"sideTesting/output/exportBook.epub"
    temp_path = r"sideTesting/extracted.epub"

    while True:
        print("1. Translate book")
        print("2. Translate book - bilingual")
        print("3. Exit")

        choice = input("Select 1-3: ")
        if choice == '1':
            processor.book_init(epub_path, temp_path, output_path)

            confirm = input("\nConfirm translate y/n: ")
            if confirm.lower() == 'y':
                start_time = time.time()
                processor.process_book(temp_path, output_path)
                elapsed_time = time.time() - start_time
                print(f'Full processing time: {round(elapsed_time)} seconds')
            else:
                print("Translation canceled.")
        elif choice == '2':
            processor.book_init(epub_path, temp_path, output_path)

            confirm = input("\nConfirm translate y/n: ")
            if confirm.lower() == 'y':
                start_time = time.time()
                processor.process_book(temp_path, output_path, bilingual=True)
                elapsed_time = time.time() - start_time
                print(f'Full processing time: {round(elapsed_time)} seconds')
            else:
                print("Translation canceled.")
        elif choice == '3':
            break


main()
