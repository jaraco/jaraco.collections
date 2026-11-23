import pytest

from jaraco.collections import FoldedCaseKeyedDict


@pytest.mark.parametrize('key', [42, ('tuple', 1), frozenset({1, 2}), None])
def test_nonstring_keys_remain_distinct_from_their_text(key):
    mapping = FoldedCaseKeyedDict({key: 'object', str(key): 'text', 'Mixed': 'case'})
    assert len(mapping) == 3
    assert mapping[key] == 'object'
    assert mapping[str(key)] == 'text'
    assert mapping['MIXED'] == 'case'
    assert mapping.matching_key_for(key) == key
    assert mapping.get(key) == 'object'
    assert mapping.setdefault(key, 'replacement') == 'object'
    assert mapping.pop(key) == 'object'
    assert key not in mapping
    assert mapping[str(key)] == 'text'
    mapping[key] = 'restored'
    del mapping[key]
    assert key not in mapping
