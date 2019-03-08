from unittest import TestCase

import pytest


class TestNltkData(TestCase):
    def test__init_location_fails_on_unknown_os(self):
        import platform
        from unittest.mock import MagicMock
        platform.system = MagicMock(return_value='Plan9')

        with pytest.raises(Exception):
            from mattes_dada.nltk_data import nltk_data
            nltk_data._init_location()
