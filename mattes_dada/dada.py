import os
from typing import List

import markovify
import nltk
import regex

from .odt import Parser


def path_to_str(path: str) -> str:
    path_str: str = os.fspath(path)
    if path_str.endswith('odt'):
        return Parser().extract(path)
    else:
        with open(path, "r", encoding='utf-8-sig') as f:
            return f.read()


def generate_from_file(path: str) -> List:
    raw = path_to_str(path)

    tokens = nltk.word_tokenize(raw)

    return markovify_generate(tokens)


def markovify_generate(tokens, max_results=5) -> List:
    m = markovify.Text(None, state_size=1, parsed_sentences=group_words(tokens))
    result = []

    for _ in range(100):
        sentence = m.make_sentence(max_overlap_total=3)
        if sentence is not None:
            result.append(sentence)
            if len(result) == max_results:
                break

    return result


end_of_sentence_re = regex.compile('[;.?!]')
alpha_re = regex.compile(r'^[\w,–]+$')


def group_words(tokens) -> List:
    result = []
    sentence = []
    for token in tokens:
        token = token.lower()
        if end_of_sentence_re.match(token):
            sentence.append(token)
            result.append(sentence)
            sentence = []
        if not alpha_re.match(token):
            continue
        else:
            sentence.append(token)
    if len(sentence) != 0:
        result.append(sentence)
    return result
