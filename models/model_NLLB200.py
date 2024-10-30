import ctranslate2
import transformers
import persistence

beam_size = 8


def get_language_codes():
    ref_tokenizer = transformers.AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-1.3B",
                                                               clean_up_tokenization_spaces=True)
    model_codes = dict()
    for token in ref_tokenizer.additional_special_tokens:
        model_codes[token] = token[:3]
    return model_codes


class Model:

    def __init__(self, hw, source_lang, target_lang):
        print("selected: ", source_lang, target_lang)
        self.target_lang = target_lang
        if hw == "cuda" or hw == "cpu":
            self.model = ctranslate2.Translator(str(persistence.get_appdata_path() / 'models' / 'nllb-ctranslate-int8'), hw)
        else:
            raise ValueError("Device must be 'cuda' or 'cpu'")
        self.tokenizer = transformers.AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-1.3B",
                                                                    src_lang=source_lang,
                                                                    clean_up_tokenization_spaces=True)

    def batch_process(self, text):
        input_tokenized = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        source = [self.tokenizer.convert_ids_to_tokens(sent) for sent in input_tokenized["input_ids"]]
        target_prefix = [[self.target_lang]] * len(source)
        results = self.model.translate_batch(source, target_prefix=target_prefix, beam_size=beam_size,
                                             repetition_penalty=1.3, disable_unk=True)
        target_sents_tokenized = [result.hypotheses[0][1:] for result in results]
        target_sents_to_ids = [self.tokenizer.convert_tokens_to_ids(sent) for sent in target_sents_tokenized]
        return self.tokenizer.batch_decode(target_sents_to_ids)
