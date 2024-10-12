from progress.bar import IncrementalBar
import os

from models import model_NLLB200


class translations:

    def __init__(self, model_name):
        self.model = None
        self.model_name = model_name

    def instantiate_model(self, hw, source_lang, target_lang):
        if self.model_name == "NLLB200":
            from models.model_NLLB200 import Model
            self.model = Model(hw, source_lang, target_lang)
        else:
            raise Exception("Model not found")

    def translate(self, group, batch_size, name):
        translated = []
        print(f'\n\n{os.path.basename(name)}\n')
        with IncrementalBar(max=len(group), suffix='%(percent).1f%%') as bar:
            for i in range(0, len(group), batch_size):
                chunk = group[i:i + batch_size]
                chunk_translated = self.model.batch_process(chunk)

                for num in range(min(batch_size, len(chunk_translated))):
                    if len(chunk_translated[num]) < 5 * len(chunk[num]):
                        translated.append(chunk_translated[num])
                    else:
                        translated.append(chunk[num])

                bar.goto(min(len(group), i + batch_size))
        return translated

    def get_language_codes(self):
        if self.model_name == "NLLB200":
            return model_NLLB200.get_language_codes()
