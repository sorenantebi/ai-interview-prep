from ratelimit.window import SlidingWindow


def test_count_within_window():
    w = SlidingWindow(10)
    w.record(0)
    w.record(5)
    assert w.count(9) == 2


def test_hit_expires_exactly_at_edge():
    w = SlidingWindow(10)
    w.record(0)
    assert w.count(10) == 0, "a hit made exactly `size` seconds ago is outside the window"


def test_oldest_none_when_empty():
    w = SlidingWindow(10)
    assert w.oldest() is None
    w.record(3)
    assert w.oldest() == 3
