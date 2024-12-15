<h2 align="center">Mørkepub</h2>

This is a command-line tool to translate EPUBs using multilingual transformer models.
Processing runs locally and requires a GPU.

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
Because translating an entire book is lengthy, test the model on a sample first.
A test sample is included in `tests/resources/`. 
As you would expect, the quality is better between closely related languages.

## Models

These are the latest supported models. Quantized versions are used to reduce the size and RAM requirements.

| Model  | Parameters | Languages | Size | Technology | Notes |
| -------------|-------------|-------------|-------------|-------------|-------------|
| [NLLB200](https://huggingface.co/facebook/nllb-200-distilled-1.3B)  | 1.3B | 200 | 1.3 GB |  CTranslate2 | |
| [small100](https://huggingface.co/alirezamsh/small100) | 330M | 100 | 0.6 GB | SentencePiece, bitsandbytes | Only Intel CPUs |

AI evolves quickly. You are welcome to suggest a new state-of-the-art multilingual model that could be added.

## Prerequisites
- CUDA graphics card (Nvidia) or ROCm graphics card (AMD)
- [python](https://www.python.org/downloads/)

### AMD GPU

AMD compatibility additionally depends on the operating system.

- [ROCm Windows compatibility matrix](https://rocm.docs.amd.com/en/docs-5.7.0/release/windows_support.html)

- [ROCm Linux compatibility matrix](https://rocm.docs.amd.com/en/docs-5.7.0/release/gpu_os_support.html)

Though it has not been tested, you may need to install the ROCm drivers.

## Setup

**Setup (first time)**
- download the source code from a [release](https://github.com/BLCK-B/Moerkepub/releases), move it to your preferred location
- open terminal in the unzipped folder
- `pip install -r requirements.txt` - downloads dependencies
- `python ui.py` or `python3 ui.py` - starts the program

**Update to the new version**
- delete the (release) folder
- download a new release, move it to your preferred location
- open terminal in the unzipped folder
- optionally: `pip install -r requirements.txt` - updates dependencies

**Uninstall**
- check where the program data is located (About menu in the program)
- delete both the program data and source code folders
- optionally: uninstall pip dependencies in requirements.txt

## Setup issues

***Could not find a version that satisfies the requirement ctranslate2***

Select the version for your system and install it: `pip install ctranslate2-<version>-<python_version>-<platform>.whl`.
You may then remove ctranslate2 from `requirements.txt`.

***No package metadata was found for bitsandbytes***

Reinstall to a compatible version: `pip install --force-reinstall 'https://github.com/bitsandbytes-foundation/bitsandbytes/releases/download/continuous-release_multi-backend-refactor/bitsandbytes-0.44.1.dev0-py3-none-win_amd64.whl'`.

***Any other issues***

If you have compatible system, you should be able to resolve these issues by following the crash log messages and installing the compatible versions of dependencies. Otherwise, let me know.

##

**Feedback**

I appreciate any bug reports: EPUB formatting, translation, installation etc.
Please use the [issue tracker](https://github.com/BLCK-B/Moerkepub/issues) or [discussions](https://github.com/BLCK-B/Moerkepub/discussions).
