from payments.backoff import compute_delay


def test_first_retry_waits_base_delay():
    assert compute_delay(1, 0.5, 2.0, 30.0) == 0.5


def test_delay_doubles_with_each_retry():
    delays = [compute_delay(n, 0.5, 2.0, 30.0) for n in range(1, 6)]
    assert delays == [0.5, 1.0, 2.0, 4.0, 8.0], delays


def test_delay_is_capped():
    assert compute_delay(10, 1.0, 2.0, 5.0) == 5.0
