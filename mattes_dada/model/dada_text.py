import typing

import markovify
import nltk
import regex
from nltk.tokenize.treebank import TreebankWordDetokenizer


class DadaText(markovify.Text):
    alpha_re = regex.compile(r'^[[:alpha:],–:]+$')
    detokenizer = TreebankWordDetokenizer()

    def __init__(self, input_text, state_size=1, chain=None, parsed_sentences=None, retain_original=True,
                 lang='english'):

        self.language = lang

        if not parsed_sentences:
            parsed_sentences = self.generate_corpus(input_text)

        super().__init__(input_text, state_size, chain, parsed_sentences, retain_original)

    def filter_word(self, word: str) -> bool:
        return DadaText.alpha_re.match(word)

    def generate_corpus(self, text):
        text = text.lower()
        return [
            [word for word in nltk.word_tokenize(sentence, language=self.language) if self.filter_word(word)]
            for sentence in nltk.sent_tokenize(text, language=self.language)
        ]

    def word_join(self, words: typing.List[str]):
        return DadaText.detokenizer.tokenize(words)

    @classmethod
    def from_tokens(cls, tokens: typing.List[typing.List[str]], state_size=1, chain=None, retain_original: bool = True,
                    lang='english'):
        return cls(None, state_size, chain, tokens, retain_original, lang)

    @classmethod
    def from_text_file(cls, path: str, encoding: str = 'utf-8-sig', lang='english'):
        with open(path, "r", encoding=encoding) as f:
            return cls(f.read(), lang=lang)

    def make_sentences(self, max_overlap_total=markovify.text.DEFAULT_MAX_OVERLAP_TOTAL, max_results=5,
                       max_failures=100) -> typing.List:
        result = []
        failures = 0

        while len(result) < max_results and failures < max_failures:
            sentence = self.make_sentence(tries=1, max_overlap_total=max_overlap_total)
            if sentence is not None:
                result.append(sentence)
            else:
                failures += 1

        return result
