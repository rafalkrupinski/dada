from mattes_dada.odt.handler import *
import pytest


def test_handler_start():
    h = ElemStackHandeler()
    h.startElement('name', {'a': 'b'})
    assert len(h.elem_stack) == 1
    elem = h.elem_stack[0]
    assert elem.name == 'name'
    assert elem.attrs == {'a': 'b'}


def test_handler_end():
    h = ElemStackHandeler()
    h.startElement('name', {'a': 'b'})
    h.endElement('name')
    assert len(h.elem_stack) == 0


def test_handler_end_fails_on_wrong_name():
    h = ElemStackHandeler()
    h.startElement('name', {'a': 'b'})

    with pytest.raises(ValueError):
        h.endElement('wrong_name')


def test_current():
    h = ElemStackHandeler()
    h.startElement('name', {'a': 'b'})
    c = h.current
    assert c.name == 'name'
    assert c.attrs == {'a': 'b'}


def test_current_error():
    h = ElemStackHandeler()
    with pytest.raises(ValueError):
        _ = h.current
