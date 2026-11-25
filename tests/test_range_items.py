import operator

import pytest

from jaraco.collections import RangeMap, WeightedLookup


@pytest.mark.parametrize(
    ('comparator', 'reverse'),
    [
        (operator.le, False),
        (operator.lt, False),
        (operator.ge, True),
        (operator.gt, True),
    ],
)
def test_positional_items(comparator, reverse):
    mapping = RangeMap(
        {1: 'first', 3: 'last'},
        sort_params=dict(reverse=reverse),
        key_match_comparator=comparator,
    )
    expected = ['first', 'last'][:: -1 if reverse else 1]

    assert mapping[RangeMap.first_item] == expected[0]
    assert mapping[RangeMap.last_item] == expected[-1]


def test_weighted_lookup_positional_items():
    mapping = WeightedLookup(a=1, b=2)

    assert mapping[RangeMap.first_item] == 'a'
    assert mapping[RangeMap.last_item] == 'b'
    assert mapping[0] == 'a'
    assert mapping[1] == 'b'


def test_positional_undefined_value():
    mapping = RangeMap(
        {0: RangeMap.undefined_value, 3: 'value'}, key_match_comparator=operator.lt
    )

    with pytest.raises(KeyError) as error:
        mapping[RangeMap.first_item]
    assert error.value.args == (0,)
    assert mapping.get(RangeMap.first_item, 'missing') == 'missing'
