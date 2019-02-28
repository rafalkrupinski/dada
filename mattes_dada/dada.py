import os

from mattes_dada import model
from .odt import Parser


def load_from_file(path: str, lang='english') -> model.DadaText:
    path_str: str = os.fspath(path)
    if path_str.endswith('odt'):
        text = Parser().extract(path)
        return model.DadaText(text, lang=lang)
    else:
        return model.DadaText.from_text_file(path, lang=lang)
