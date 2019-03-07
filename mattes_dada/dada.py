import os

from mattes_dada import model
from .odt import extract_from_odt_file

_lang = {
    'en': 'english',
    'pl': 'polish'
}


def _odt_lang(lang: str) -> str:
    return _lang[lang]


def load_from_file(path: str, lang) -> model.DadaText:
    path_str: str = os.fspath(path)
    if path_str.endswith('odt'):
        text = extract_from_odt_file(path, _odt_lang(lang))
        return model.DadaText(text, lang=lang)
    else:
        return model.DadaText.from_text_file(path, lang=lang)
