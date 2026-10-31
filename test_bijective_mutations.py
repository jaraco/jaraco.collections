import pytest

from jaraco.collections import BijectiveMap


def test_setdefault_adds_reverse_mapping() -> None:
    mapping = BijectiveMap()
    assert mapping.setdefault('a', 'b') == 'b'
    assert mapping['b'] == 'a'
    assert len(mapping) == 1
    assert mapping.setdefault('a', 'c') == 'b'


def test_setdefault_rejects_overlap() -> None:
    mapping = BijectiveMap(a='b')
    with pytest.raises(ValueError, match='overlap'):
        mapping.setdefault('c', 'b')
    assert mapping == {'a': 'b', 'b': 'a'}


def test_popitem_removes_both_directions() -> None:
    mapping = BijectiveMap(a='b', c='d')
    assert mapping.popitem() == ('d', 'c')
    assert mapping == {'a': 'b', 'b': 'a'}
    assert len(mapping) == 1
    mapping.popitem()
    assert mapping == {}
    with pytest.raises(KeyError):
        mapping.popitem()


@pytest.mark.parametrize('other', [{'c': 'd'}, [('c', 'd')]])
def test_inplace_union_preserves_pairs_and_identity(other) -> None:
    mapping = BijectiveMap(a='b')
    original = mapping
    mapping |= other
    assert mapping is original
    assert mapping == {'a': 'b', 'b': 'a', 'c': 'd', 'd': 'c'}
    assert len(mapping) == 2


def test_inplace_union_rejects_overlap() -> None:
    mapping = BijectiveMap(a='b')
    with pytest.raises(ValueError, match='overlap'):
        mapping |= {'c': 'b'}
    assert mapping == {'a': 'b', 'b': 'a'}
