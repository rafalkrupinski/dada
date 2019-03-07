import abc
import xml.sax


class MyElement(abc.ABC):

    def __init__(self, name=None, attrs=None) -> None:
        super().__init__()
        self.name = name
        self.attrs = attrs if isinstance(attrs, dict) else {key: attrs[key] for key in attrs.keys()}

    def __str__(self):
        return f'{self.name} {self.attrs}'


class ElemStackHandeler(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()
        self.elem_stack = []

    def startElement(self, name, attrs):
        super().startElement(name, attrs)
        self.elem_stack.append(MyElement(name, attrs))

    def endElement(self, name):
        super().endElement(name)
        if self.elem_stack[-1].name != name:
            raise ValueError('Unexpected end element', name)

        self.elem_stack.pop()

    @property
    def current(self) -> MyElement:
        """:returns: The current element in the xml tree"""

        if len(self.elem_stack) > 0:
            return self.elem_stack[-1]
        else:
            raise ValueError
