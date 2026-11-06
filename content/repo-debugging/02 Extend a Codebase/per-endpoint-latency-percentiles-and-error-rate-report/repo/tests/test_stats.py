from logstats import stats


def test_mean():
    assert stats.mean([1, 2, 3, 4]) == 2.5


def test_percentile_nearest_rank():
    values = list(range(1, 101))
    assert stats.percentile(values, 50) == 50
    assert stats.percentile(values, 95) == 95
    assert stats.percentile(values, 99) == 99


def test_percentile_small_sample_and_unsorted_input():
    values = [40, 10, 30, 20]
    assert stats.percentile(values, 50) == 20
    assert stats.percentile(values, 95) == 40
    assert values == [40, 10, 30, 20], "input must not be modified"


def test_percentile_rejects_bad_input():
    for args in (([], 50), ([1, 2], 101), ([1, 2], -1)):
        try:
            stats.percentile(*args)
        except ValueError:
            continue
        assert False, f"expected ValueError for {args!r}"
