import os
import typing

from mattes_dada import model
from .odt import Parser
import mattes_dada.nltk_data as _


def load_from_file(path: str) -> model.DadaText:
    path_str: str = os.fspath(path)
    if path_str.endswith('odt'):
        text = Parser().extract(path)
        return model.DadaText(text, lang='polish')
    else:
        return model.DadaText.from_text_file(path, lang='polish')


def generate_from_file(path: str) -> typing.List:
    m = load_from_file(path)
    return m.make_sentences()

