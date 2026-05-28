import operator

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


def test_rangemap_empty_lookup_raises_keyerror():
    """
    An empty RangeMap should raise KeyError on any lookup.
    """
    r = collections.RangeMap({})
    with pytest.raises(KeyError):
        r[0]


def test_rangemap_bounds_at_sentinels():
    """
    bounds() should return the minimum and maximum keys, and the
    first_item/last_item sentinels should resolve to the corresponding values.
    """
    r = collections.RangeMap({1: 'a', 5: 'b', 10: 'c'})
    assert r.bounds() == (1, 10)
    assert r[collections.RangeMap.first_item] == 'a'
    assert r[collections.RangeMap.last_item] == 'c'


def test_rangemap_key_match_comparator_override():
    """
    A custom key_match_comparator and sort_params should change range semantics.
    """
    r = collections.RangeMap(
        {1: 'a', 4: 'b'},
        sort_params=dict(reverse=True),
        key_match_comparator=operator.ge,
    )
    assert r[1] == r[2] == r[3] == 'a'
    assert r[4] == r[5] == r[6] == 'b'
