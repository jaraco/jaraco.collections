import pytest

from jaraco import collections


class AlwaysStringKeysDict(collections.KeyTransformingDict):
    """
    An implementation of a KeyTransformingDict subclass that always converts
    the keys to strings.
    """

    @staticmethod
    def transform_key(key):
        return str(key)


def test_always_lower_keys_dict():
    """
    Tests AlwaysLowerKeysDict to ensure KeyTransformingDict works.
    """
    d = AlwaysStringKeysDict()
    d['farther'] = 'closer'
    d['Lasting'] = 'fleeting'
    d[3] = 'three'
    d[{'a': 1}] = 'a is one'
    assert all(isinstance(key, str) for key in d)
    assert "{'a': 1}" in d
    assert 3 in d
    assert d[3] == d['3'] == 'three'


def test_bijective_pop_missing_default():
    mapping = collections.BijectiveMap(a='b')
    default = object()
    assert mapping.pop('missing', default) is default
    assert mapping == {'a': 'b', 'b': 'a'}


def test_bijective_pop_missing_without_default():
    mapping = collections.BijectiveMap(a='b')
    with pytest.raises(KeyError):
        mapping.pop('missing')
    assert mapping == {'a': 'b', 'b': 'a'}


@pytest.mark.parametrize('key', ['a', 'b'])
def test_bijective_pop_existing_with_default(key):
    mapping = collections.BijectiveMap(a='b')
    assert mapping.pop(key, None) == ('b' if key == 'a' else 'a')
    assert mapping == {}


def test_bijective_pop_invalid_arguments_preserve_pair():
    mapping = collections.BijectiveMap(a='b')
    with pytest.raises(TypeError):
        mapping.pop('a', None, None)
    assert mapping == {'a': 'b', 'b': 'a'}


def test_bijective_pop_invalid_keyword_preserves_pair():
    mapping = collections.BijectiveMap(a='b')
    with pytest.raises(TypeError):
        mapping.pop('a', default=None)
    assert mapping == {'a': 'b', 'b': 'a'}
