from autocomplete.text import normalize


def test_lowercases():
    assert normalize("New York") == "new york"


def test_collapses_whitespace_between_words():
    assert normalize("new\tyork") == "new york"
    assert normalize("new  \n york") == "new york"


def test_trims_and_handles_empty():
    assert normalize("  Pizza  ") == "pizza"
    assert normalize("") == ""
    assert normalize(None) == ""
    assert normalize(" \t ") == ""
