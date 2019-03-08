import os

from mattes_dada import model
from .odt import extract_from_odt_file

_lang = {
    'en': 'english',
    'pl': 'polish'
}


# pragma: no cover
def _nltk_lang(lang: str) -> str:
    return _lang[lang]


def load_from_file(path: str, lang) -> model.DadaText:
    path_str: str = os.fspath(path)
    if path_str.endswith('odt'):
        text = extract_from_odt_file(path, lang)
        return model.DadaText(text, lang=_nltk_lang(lang))
    else:
        return model.DadaText.from_text_file(path, lang=_nltk_lang(lang))
