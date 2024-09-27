from abc import ABC, abstractmethod


class TranslationModelInterface(ABC):
    @abstractmethod
    def initialize(self, hw, source_lang):
        pass

    @abstractmethod
    def get_language_codes(self):
        pass

    @abstractmethod
    def batch_process(self, text):
        pass
