import toml

import mattes_dada.dada
from mattes_dada import __version__

# noinspection PyUnresolvedReferences
import mattes_dada.nltk_data as _


def test_version():
    expected_version = '0.2.1'
    assert __version__ == expected_version
    assert get_pyproject_version() == expected_version


def get_pyproject_version():
    return toml.load('pyproject.toml')['tool']['poetry']['version']


def test_generate_from_file():
    model = mattes_dada.dada.load_from_file('tests/test_input.txt', 'english')
    sentences = model.make_sentences()
    assert len(sentences) <= 5
