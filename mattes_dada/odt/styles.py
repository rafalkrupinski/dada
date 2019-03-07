import typing

from .handler import ElemStackHandeler
import xml.sax

FO_LANGUAGE = 'fo:language'

STYLE_PARAGRAPH = 'paragraph'

STYLE_FAMILY = 'style:family'

DEFAULT_STYLE = 'style:default-style'

TEXT_PROPS = 'style:text-properties'


class StyleHandler(ElemStackHandeler):

    def __init__(self):
        super().__init__()
        self.lang = None

    def startElement(self, name: str, attrs: dict):
        super().startElement(name, attrs)

        if name == TEXT_PROPS:
            self.handle_para_props()

    def handle_para_props(self) -> None:
        parent = self.elem_stack[-2]

        if parent.name == DEFAULT_STYLE and STYLE_FAMILY in parent.attrs and \
                parent.attrs[STYLE_FAMILY] == STYLE_PARAGRAPH:
            self.lang = self.current.attrs[FO_LANGUAGE]


def extract_default_language(text: typing.Union[str, bytes]) -> str:
    handler = StyleHandler()
    xml.sax.parseString(text, handler)
    return handler.lang
