from unittest import TestCase
import sys
import mattes_dada.cmd as cmd


class CmdTest(TestCase):
    def test_parse_args(self):
        sys.argv = ['mdada', '--lang', 'en', 'input_file.txt']

        parsed = cmd.parse_args()
        print(parsed)
        self.assertEqual('input_file.txt', parsed.input_file)
        self.assertEqual('en', parsed.lang)
