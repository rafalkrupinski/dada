from unittest import TestCase

from mattes_dada.model.dada_text import DadaText


class TestDadaText(TestCase):
    def test_to_dict(self):
        t = DadaText('Alexandra has a cat')
        self.assertEqual({'state_size': 1, 'chain': [(('___BEGIN__',), {'alexandra': 1}), (('alexandra',), {'has': 1}),
                                                     (('has',), {'a': 1}), (('a',), {'cat': 1}),
                                                     (('cat',), {'___END__': 1})],
                          'parsed_sentences': [['alexandra', 'has', 'a', 'cat']]}, t.to_dict())

    def test_to_json(self):
        t = DadaText('Alexandra has a cat')
        json_txt = t.to_json()
        self.assertEqual(t.to_dict(), DadaText.from_json(json_txt).to_dict())

    def test_generate_sentences_fails(self):
        t = DadaText('Alexandra is not.')
        self.assertEqual(t.make_sentences(), [])
