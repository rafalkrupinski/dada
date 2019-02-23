import os
import typing

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


alpha_re = regex.compile(r'^[\w,–]+$')


def generate_from_str(text: str):
    text = text.lower()
    words = [
        [word for word in nltk.word_tokenize(sentence, 'polish') if alpha_re.match(word)]
        for sentence in nltk.sent_tokenize(text, 'polish')
    ]
    return markovify_generate(words)


def generate_from_file(path: str) -> typing.List:
    text = path_to_str(path)

    return generate_from_str(text)


def markovify_generate(tokens, max_results=5, max_attempts=100) -> typing.List:
    m = markovify.Text(None, state_size=1, parsed_sentences=tokens)
    result = []
    attempts = 0

    while len(result) < max_results and attempts < max_attempts:
        attempts += 1
        sentence = m.make_sentence(max_overlap_total=3)
        if sentence is not None:
            result.append(sentence)

    return result
