from wordgame.bitmask import letter_mask
from wordgame.solver import max_unique_length, usable_masks
from wordgame.words import clean_words


def test_clean_words_normalises():
    assert clean_words([" Cat ", "DOG", "", "b4d", "ok"]) == ["cat", "dog", "ok"]


def test_usable_masks_skips_repeats():
    assert usable_masks(["ab", "aa", "cd"]) == [letter_mask("ab"), letter_mask("cd")]


def test_usable_masks_keeps_input_order_and_duplicates():
    assert usable_masks(["bc", "ab", "bc"]) == [6, 3, 6]


def test_max_unique_length_examples():
    assert max_unique_length(["un", "iq", "ue"]) == 4
    assert max_unique_length(["cha", "r", "act", "ers"]) == 6
    assert max_unique_length(["abcdefghijklmnopqrstuvwxyz"]) == 26


def test_max_unique_length_nothing_usable():
    assert max_unique_length([]) == 0
    assert max_unique_length(["aa", "bb"]) == 0


def test_same_word_twice_cannot_be_reused():
    assert max_unique_length(["ab", "ab"]) == 2
    assert max_unique_length(["abc", "cba", "abc"]) == 3
