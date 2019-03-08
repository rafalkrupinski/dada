from mattes_dada.odt.handler import MyElement


def test_elem_init():
    e = MyElement('name', {'a': 'b'})
    assert e.name == 'name'
    assert e.attrs == {'a': 'b'}


def test_MyElement_str():
    e = MyElement('name', {'a': 'b'})
    assert str(e) == "name {'a': 'b'}"
