import xml.sax
import zipfile

import regex

from .handler import ElemStackHandeler
from .styles import extract_default_language


class OdtContentHandler(ElemStackHandeler):
    def __init__(self, language=None, default_language=None, target=None):
        super().__init__()
        self.styles = {}
        if target is not None:
            self.target = target
        else:
            self.target = []
        self.language = language
        self.default_language = default_language

    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if self.is_text_tag():
            self.handle_text_elem()
        elif name == 'text:tab':
            self.handle_tab()
        elif name == 'text:s':
            self.handle_space()
        elif name == 'style:text-properties':
            self.handle_style()
        elif name == 'text:line-break':
            self.handle_line_break()

    def endElement(self, name):
        super().endElement(name)
        if name == 'text:p' or name == 'text:h':
            last_text = self.find_last_text()
            if last_text is not None:
                if regex.match(r'.*[^.]\s*$', last_text):
                    print('Text "' + last_text + '" is missing ending period.')
                    self.target.append('.')
            if len(self.target) == 0 or self.target[-1] != '\n':
                self.target.append('\n')

    ws = regex.compile(r'^\s+$')

    def characters(self, content):

        if self.is_text_tag() and self.is_text_allowed():
            if len(self.target) is 0:
                self.target.append(content)
            else:
                last_text = self.target[-1]
                if OdtContentHandler.ws.match(last_text) and OdtContentHandler.ws.match(content):
                    pass
                else:
                    self.target.append(content)

    def is_text_allowed(self):
        for elem in reversed(self.elem_stack):
            if 'language' in elem.attrs.keys():
                lang = elem.attrs['language']
                break
        else:
            lang = self.default_language

        return lang == self.language

    def is_text_tag(self):
        return self.current.name in ['text:p', 'text:span', 'text:h']

    def handle_tab(self):
        self.target.append('\t')

    def handle_text_elem(self):
        attrs = self.current.attrs
        if 'text:style-name' in attrs:
            style_name = attrs['text:style-name']
            if style_name in self.styles:
                attrs['language'] = self.styles[style_name]

    def handle_space(self):
        attrs = self.current.attrs
        self.target.append(" " * int(attrs.get('text:c', 1)))

    def handle_style(self):
        text_props = self.current.attrs
        style = self.elem_stack[-2]

        if 'fo:language' in text_props.keys():
            self.styles[style.attrs['style:name']] = text_props['fo:language']

    def find_last_text(self):
        for text in reversed(self.target):
            if not OdtContentHandler.ws.match(text):
                return text
        return None

    def handle_line_break(self):
        self.target.append('\n')


def extract(text: str, language: str = None, default_language=None) -> str:
    target = []
    handler = OdtContentHandler(language, default_language, target)
    xml.sax.parseString(text, handler)
    return ''.join(target)


def extract_from_odt_file(path: str, lang: str) -> str:
    with open(path, 'rb') as stream:
        zip_stream = zipfile.ZipFile(stream)
        default_lang = extract_default_language(zip_stream.read('styles.xml'))
        return extract(zip_stream.read("content.xml"), lang, default_lang)
