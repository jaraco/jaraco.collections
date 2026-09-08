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


def test_frozen_dict_hash_with_unorderable_keys():
    first = collections.FrozenDict({1: 'integer', 'name': 'string'})
    reverse = collections.FrozenDict({'name': 'string', 1: 'integer'})

    indexed = {first: 'stored'}

    assert indexed[reverse] == 'stored'
    assert len({first, reverse}) == 1


def test_frozen_dict_hash_is_independent_of_partially_ordered_keys():
    pairs = [(frozenset({1}), 'one'), (frozenset({2}), 'two')]
    first = collections.FrozenDict(pairs)
    reverse = collections.FrozenDict(reversed(pairs))

    assert first == reverse
    assert hash(first) == hash(reverse)
