from pathlib import Path
from unittest import TestCase

from mattes_dada.odt.content import *


class TestOdtContentHandler(TestCase):
    def test_handle_tab(self):
        h = OdtContentHandler()
        h.startElement('text:tab', {})
        assert h.current.name == 'text:tab'

    def test_line_break(self):
        h = OdtContentHandler()
        h.startElement('text:line-break', {})
        assert h.target[0] == '\n'

    def test_sax(self):
        p = xml.sax.make_parser()
        h = OdtContentHandler()
        p.setContentHandler(h)

        with Path(Path(__file__).parent, 'test_odt.xml').open('rt') as f:
            p.parse(f)

        assert h.target == ['\n', 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.', '\n',
                            '        Aenean commodo ligula eget dolor.', '\n', 'Aenean massa.', '\n',
                            'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus', '\n',
                            '            mus.', '\n',
                            ' ', 'Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem.', '\n']

    def test_passed_list(self):
        target = []
        h = OdtContentHandler(target=target)
        h.startElement('text:tab', {})
        self.assertEqual(target, ['\t'])

    def test_content_without_ending_period(self):
        h = OdtContentHandler()
        h.startElement('text:p', {})
        h.characters('Alexandra has a cat')
        h.endElement('text:p')
        self.assertEqual(h.target[-2], '.')

    def test_file_last_text_on_empty_contents(self):
        h = OdtContentHandler()
        self.assertEqual(h.find_last_text(), None)

    def test_extract(self):
        from tests.mattes_dada import test_odt
        odt_text = extract_from_odt_file(test_odt, 'en')
        self.assertEqual("Default style.\ncustom style.\n", odt_text)

    def test_end_p_no_text(self):
        h = OdtContentHandler()
        h.startElement('text:p', {})
        h.endElement('text:p')
        self.assertEqual('\n', h.target[0])
