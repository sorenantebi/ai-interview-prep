from autocomplete.index import PhraseIndex


def make_index():
    index = PhraseIndex()
    for phrase, count in [
        ("pizza", 5),
        ("pizza hut", 9),
        ("pasta", 5),
        ("pancake", 2),
        ("burger", 7),
    ]:
        index.add(phrase, count)
    return index


def test_add_accumulates_counts():
    index = PhraseIndex()
    assert index.add("tea") == 1
    assert index.add("tea", 4) == 5
    assert index.count("tea") == 5
    assert index.count("coffee") == 0
    assert "tea" in index
    assert len(index) == 1


def test_top_k_orders_by_count_descending():
    index = make_index()
    assert index.top_k("p", 3) == [("pizza hut", 9), ("pasta", 5), ("pizza", 5)]


def test_ties_are_broken_alphabetically():
    index = PhraseIndex()
    for phrase in ["delta", "alpha", "charlie", "bravo"]:
        index.add(phrase, 2)
    assert [p for p, _ in index.top_k("", 10)] == ["alpha", "bravo", "charlie", "delta"]


def test_top_k_only_returns_matching_prefix():
    index = make_index()
    assert [p for p, _ in index.top_k("pa", 10)] == ["pasta", "pancake"]
    assert index.top_k("zzz", 5) == []


def test_top_k_respects_limit_and_empty_prefix():
    index = make_index()
    assert index.top_k("", 2) == [("pizza hut", 9), ("burger", 7)]
    assert index.top_k("p", 1) == [("pizza hut", 9)]
