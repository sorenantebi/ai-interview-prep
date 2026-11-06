from wordgame.bitmask import letter_mask, letters_of, popcount


def test_letter_mask_basic():
    assert letter_mask("abc") == 0b111
    assert letter_mask("zb") == (1 << 25) | (1 << 1)


def test_letter_mask_single_letter():
    assert letter_mask("a") == 1
    assert letter_mask("z") == 1 << 25


def test_letter_mask_empty_word():
    assert letter_mask("") == 0


def test_repeated_letter_returns_none():
    assert letter_mask("hello") is None
    assert letter_mask("aa") is None


def test_non_lowercase_letters_raise():
    for bad in ("Abc", "a1", "a b", "\u00e9"):
        try:
            letter_mask(bad)
        except ValueError:
            continue
        assert False, f"expected ValueError for {bad!r}"


def test_popcount_and_letters():
    mask = letter_mask("quiz")
    assert popcount(mask) == 4
    assert letters_of(mask) == "iquz"
    assert popcount(0) == 0
