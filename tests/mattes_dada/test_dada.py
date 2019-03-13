from unittest import TestCase

import toml

import mattes_dada.dada
from mattes_dada import __version__

# noinspection PyUnresolvedReferences
import mattes_dada.nltk_data as _
from tests.mattes_dada import test_odt, test_txt


class TestDada(TestCase):

    def test_version(self):
        expected_version = '0.2.2'
        assert __version__ == expected_version
        assert TestDada.get_pyproject_version() == expected_version

    @staticmethod
    def get_pyproject_version():
        return toml.load('pyproject.toml')['tool']['poetry']['version']

    def test_generate_from_file(self):
        model = mattes_dada.dada.load_from_file(test_txt, 'en')
        sentences = model.make_sentences()
        assert len(sentences) <= 5

    def test_load_from_file_odt(self):
        model = mattes_dada.dada.load_from_file(test_odt, 'en')
        sentences = model.make_sentences()
        assert len(sentences) <= 5
