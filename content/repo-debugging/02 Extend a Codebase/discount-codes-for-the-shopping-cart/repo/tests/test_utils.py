from cart.utils import normalize_code, split_proportionally


def test_split_proportionally_distributes_remainder():
    assert split_proportionally(100, [1, 1, 1]) == [34, 33, 33]
    assert split_proportionally(10, [0, 0]) == [0, 0]


def test_normalize_code():
    assert normalize_code("  save10 ") == "SAVE10"
