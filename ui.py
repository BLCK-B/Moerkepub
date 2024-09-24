import os
import time

import text_processor as processor

output_path = r"sideTesting/output/exportBook.epub"
temp_path = r"sideTesting/extracted.epub"


def main():
    os.system('cls')
    while True:
        print("1. Settings")
        print("2. Translate")
        print("3. Translate bilingual")
        print("4. Exit")

        choice = input("Select 1-3: ")
        os.system('cls')
        if choice == '0':
            epub_path = r"sideTesting/diary.epub"

            processor.book_init(epub_path, temp_path, output_path)

            confirm = input("\nConfirm translate y/n: ")
            if confirm.lower() == 'y':
                start_time = time.time()
                processor.process_book_files(temp_path, output_path)
                elapsed_time = time.time() - start_time
                print(f'Full processing time: {round(elapsed_time)} seconds')
            else:
                print("Translation canceled.")

        elif choice == '1':
            print("settings - GPU, models")

        elif choice == '2' or choice == '3':
            input_file = input("Drag and drop EPUB | TXT file.\n\n")
            input_file = input_file.replace('\"', '')
            _, extension = os.path.splitext(input_file)
            extension = extension.lower()
            if extension == '':
                print(f"Wrong input", extension)
                continue

            os.system('cls')
            match extension:
                case '.epub':
                    process_epub(input_file, bilingual=(choice == '3'))
                case '.txt':
                    print(f"Processing TXT file")
                case _:
                    print(f"Unsupported file type: ", extension)
                    continue

        elif choice == '4':
            print("Ebook translator exited.")
            break


def process_epub(input_file, bilingual):
    processor.book_init(input_file, temp_path, output_path)

    confirm = input("\nConfirm translate y/n: ")
    os.system('cls')
    if confirm.lower() == 'y':
        start_time = time.time()
        processor.process_book_files(temp_path, output_path, bilingual)
        elapsed_time = time.time() - start_time
        input(f'\nDone! Full processing time: {round(elapsed_time)} seconds')
        os.system('cls')
    else:
        input("Translation canceled.")


main()
