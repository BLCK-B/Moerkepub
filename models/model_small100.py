import torch
from transformers import M2M100ForConditionalGeneration
from tokenization_small100 import M2M100Tokenizer
import persistence

model_path = str(persistence.get_appdata_path() / 'models' / 'small100-quantized')


def get_language_codes():
    ref_tokenizer = M2M100Tokenizer.from_pretrained(model_path)
    model_codes = dict()
    for token in ref_tokenizer.additional_special_tokens:
        model_codes[token] = token.replace('_', '')
    return model_codes


class Model:

    def __init__(self, hw, source_lang, target_lang):
        print("selected: ", source_lang, target_lang)
        self.model = M2M100ForConditionalGeneration.from_pretrained(model_path)
        if hw == "cuda":
            self.device = torch.device("cuda:0")
        elif hw == "cpu":
            self.device = torch.device("cpu")
        else:
            raise ValueError("Device must be 'cuda' or 'cpu'")
        self.tokenizer = M2M100Tokenizer.from_pretrained(model_path)
        self.tokenizer.tgt_lang = target_lang.replace('_', '')

    def batch_process(self, text):
        encoded_hi = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        generated_tokens = self.model.generate(**encoded_hi)
        result = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return result
