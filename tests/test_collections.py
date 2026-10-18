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


def test_range_map_lookup_and_cache_invalidation():
    r = collections.RangeMap({3: 'a', 6: 'b'})

    assert (r[1], r[3], r[4], r[6]) == ('a', 'a', 'b', 'b')
    assert r.bounds() == (3, 6)

    r[4] = 'c'
    assert r[4] == 'c'

    del r[4]
    assert r[4] == 'b'


def test_range_map_left_and_weighted_lookup():
    left = collections.RangeMap.left({1: 'a', 4: 'b'})
    assert (left[1], left[3], left[4], left[6]) == ('a', 'a', 'b', 'b')

    weighted = collections.WeightedLookup(a=1, b=2)
    assert (weighted[0], weighted[1], weighted[2]) == ('a', 'b', 'b')
