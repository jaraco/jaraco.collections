import pytest

from jaraco.collections import WeightedLookup


@pytest.mark.parametrize(
    'weights',
    [
        {'a': 1, 'zero': 0, 'b': 1},
        {'a': 1, 'b': 1, 'zero': 0},
        {'zero': 0, 'a': 1, 'b': 1},
    ],
)
def test_zero_weight_does_not_replace_choice(weights: dict[str, int]) -> None:
    lookup = WeightedLookup(weights)
    assert [lookup[index] for index in (0, 0.5, 1, 1.5)] == ['a', 'a', 'b', 'b']


def test_random_skips_zero_weight(monkeypatch: pytest.MonkeyPatch) -> None:
    lookup = WeightedLookup(a=1, zero=0, b=1)
    monkeypatch.setattr('jaraco.collections.random.random', lambda: 0.25)
    assert lookup.random() == 'a'
