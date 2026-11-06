from pkgres.versions import parse_version, satisfies


def test_trailing_zeros_are_ignored():
    assert parse_version("1.0.0") == parse_version("1")
    assert parse_version("2.1") == parse_version("2.1.0")


def test_numeric_ordering():
    assert parse_version("1.10") > parse_version("1.9")
    assert parse_version("2.0") > parse_version("1.99.99")


def test_satisfies_range():
    assert satisfies("1.4", ">=1.2,<2.0")
    assert not satisfies("2.0", ">=1.2,<2.0")
    assert not satisfies("1.1", ">=1.2,<2.0")


def test_satisfies_equality():
    assert satisfies("1.2.0", "==1.2")
    assert not satisfies("1.3", "==1.2")
