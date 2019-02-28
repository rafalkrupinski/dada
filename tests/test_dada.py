import toml

import mattes_dada.dada
from mattes_dada import __version__


def test_version():
    expected_version = '0.2.0'
    assert __version__ == expected_version
    assert get_pyproject_version() == expected_version


def get_pyproject_version():
    return toml.load('pyproject.toml')['tool']['poetry']['version']


def test_generate_from_file():
    sentences = mattes_dada.dada.generate_from_file('tests/test_input.txt')
    assert len(sentences) <= 5
