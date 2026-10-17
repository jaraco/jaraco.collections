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


@pytest.mark.parametrize('key', [3, None, {'a': 1}, 'already a string'])
def test_matching_key_for_transforms_key(key):
    d = AlwaysStringKeysDict()
    d[key] = 'value'
    (stored_key,) = d.keys()
    assert key in d
    assert d[key] == 'value'
    assert d.matching_key_for(key) is stored_key


def test_matching_key_for_normalized_string():
    class LowerKeysDict(collections.KeyTransformingDict):
        transform_key = staticmethod(str.lower)

    d = LowerKeysDict({'Mixed': 'value'})
    assert d['MIXED'] == 'value'
    assert d.matching_key_for('MIXED') == 'mixed'


def test_matching_key_for_missing_key():
    d = AlwaysStringKeysDict()
    with pytest.raises(KeyError) as exc_info:
        d.matching_key_for(3)
    assert exc_info.value.args == (3,)
