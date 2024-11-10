<h2 align="center">Mørkepub</h2>

This is a command-line tool to translate EPUBs using multilingual transformer models.
Processing runs locally and requires a CUDA-compatible GPU.

<img src="https://github.com/user-attachments/assets/dadf0c1e-72cd-48ac-bdc0-cf44ff625080" width="380px"/>

<img src="https://github.com/user-attachments/assets/70fb0e42-238e-457f-9cae-491101213a4e" width="330px"/>

| Features  |
| ------------- |
| 200+ languages  |
| Choose from several models |
| Unrestricted offline translation  |
| Create bilingual ebooks  |
| Retains ebook formatting |

Currently, the output quality is comparable to Google Translate and DeepL.
You should test the model on a sample before translating an entire book.
A test sample is included in `tests/resources/`. 
In general, the quality is better between closely related languages.

##

**Models**

These are the latest supported models. Quantized versions are used to reduce the size and RAM requirements.

| Model  | Parameters | Languages | Size | Technology |
| -------------|-------------|-------------|-------------|-------------|
| [NLLB200](https://huggingface.co/facebook/nllb-200-distilled-1.3B)  | 1.3B | 200 | 1.3 GB |  CTranslate2
| [small100](https://huggingface.co/alirezamsh/small100) | 330M | 100 | 0.6 GB | SentencePiece, bitsandbytes

AI evolves quickly. You are welcome to suggest a new state-of-the-art multilingual model that could be added.

##

**Prerequisites**
- CUDA graphics card (Nvidia)
- [python](https://www.python.org/downloads/)

**Setup (first time)**
- download the source code from a [release](https://github.com/BLCK-B/Moerkepub/releases), move it to your preferred location
- open terminal in the unzipped folder
- `pip install -r requirements.txt` - downloads dependencies
- `python ui.py` or `python3 ui.py` - starts the program

**Update to new version**
- delete the (release) folder
- download a new release, move it to your preferred location
- open terminal in the unzipped folder
- optionally: `pip install -r requirements.txt` - updates dependencies

**Uninstall**
- check where the program data is located (About menu in the program)
- delete both the program data and source code folders
- optionally: uninstall pip dependencies in requirements.txt

##

**Feedback**

I appreciate any bug reports: EPUB formatting, translation, installation etc.
Please use the [issue tracker](https://github.com/BLCK-B/Moerkepub/issues) or [discussions](https://github.com/BLCK-B/Moerkepub/discussions).
