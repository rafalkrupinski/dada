import unittest.mock
from unittest import TestCase

from mattes_dada.odt.styles import StyleHandler
from mattes_dada.odt import styles


class TestStyleHandler(TestCase):
    def test_startElement(self):
        h = StyleHandler()
        h.handle_para_props = unittest.mock.MagicMock()
        h.startElement(styles.TEXT_PROPS, {})
        h.handle_para_props.assert_called()

    def test_handle_para_props(self):
        h = StyleHandler()
        h.startElement(styles.DEFAULT_STYLE, {})
        h.startElement(styles.TEXT_PROPS, {})
        assert h.lang is None
