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


def test_update_transforms_keys():
    d = AlwaysStringKeysDict()
    d.update({3: 'three'})
    assert d[3] == 'three'
    d.update([(4, 'four')], fifth='five')
    assert dict(d) == {'3': 'three', '4': 'four', 'fifth': 'five'}


def test_update_case_insensitive_keys():
    d = collections.FoldedCaseKeyedDict({'Name': 'before'})
    d.update(NAME='after')
    assert len(d) == 1
    assert d['name'] == 'after'


def test_inplace_union_transforms_keys():
    d = AlwaysStringKeysDict()
    original = d
    d |= {3: 'three'}
    assert d is original
    assert d[3] == 'three'
    d |= [(4, 'four')]
    assert dict(d) == {'3': 'three', '4': 'four'}
