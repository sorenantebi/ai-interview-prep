from ratelimit.policy import Policy


def test_override_applies_to_endpoint_only():
    p = Policy(5, 10)
    p.set_override("search", 1)
    assert p.limit_for("search") == 1
    assert p.limit_for("upload") == 5


def test_overrides_are_not_shared_between_policies():
    first = Policy(5, 10)
    first.set_override("export", 1)
    second = Policy(5, 10)
    assert second.limit_for("export") == 5


def test_invalid_values_raise():
    for args in [(0, 10), (5, 0), (-1, 10)]:
        try:
            Policy(*args)
        except ValueError:
            continue
        raise AssertionError(f"Policy{args} should raise ValueError")
