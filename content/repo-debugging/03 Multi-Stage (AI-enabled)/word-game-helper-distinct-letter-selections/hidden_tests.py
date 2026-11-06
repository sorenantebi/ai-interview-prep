import random
import time

from wordgame.bitmask import letter_mask, letters_of, popcount
from wordgame.report import format_summary, summarize_text
from wordgame.solver import max_unique_length
from wordgame.words import clean_words


def _reference(words):
    """Brute force over all subsets of the usable words, using plain sets."""
    usable = [w for w in words if len(set(w)) == len(w)]
    best = 0

    def go(start, used, total):
        nonlocal best
        best = max(best, total)
        for j in range(start, len(usable)):
            w = usable[j]
            if used.isdisjoint(w):
                go(j + 1, used | set(w), total + len(w))

    go(0, frozenset(), 0)
    return best


def _raises_value_error(text):
    try:
        letter_mask(text)
    except ValueError:
        return True
    return False


def _scramble(rng, word):
    return "".join(rng.sample(word, len(word)))


def test_letter_mask_all_letters():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    assert letter_mask(alphabet) == (1 << 26) - 1
    assert popcount(letter_mask(alphabet)) == 26


def test_letter_mask_boundaries():
    assert letter_mask("az") == 1 | (1 << 25)
    assert letter_mask("a") == 1
    assert letter_mask("z") == 1 << 25


def test_letter_mask_anagrams_equal():
    assert letter_mask("listen") == letter_mask("silent")


def test_letter_mask_rejects_symbols():
    for bad in ("`", "{", "@", "-", "a`", "z{"):
        assert _raises_value_error(bad), f"no ValueError for {bad!r}"


def test_letters_round_trip():
    for word in ("quiz", "jump", "fox", "zebra"):
        assert letters_of(letter_mask(word)) == "".join(sorted(word))
        assert popcount(letter_mask(word)) == len(word)


def test_clean_words_unicode_and_whitespace():
    raw = ["\tTea\n", "na\u00efve", "x-ray", "\u00c4B", "  "]
    assert clean_words(raw) == ["tea"]


def test_matches_brute_force_small():
    rng = random.Random(0)
    for _ in range(80):
        n = rng.randint(0, 9)
        words = [
            "".join(rng.choices("abcdefgh", k=rng.randint(1, 4))) for _ in range(n)
        ]
        assert max_unique_length(words) == _reference(words), words


def test_input_not_mutated():
    words = ["ab", "cd", "ab"]
    snapshot = list(words)
    assert max_unique_length(words) == 4
    assert words == snapshot


def test_empty_word_is_harmless():
    assert max_unique_length([""]) == 0
    assert max_unique_length(["", "ab"]) == 2


def test_summarize_messy_input():
    summary = summarize_text("  Cha, r\tact\nERS,, hello!! 42 \u00e9 ")
    assert summary == {"words": 4, "usable": 4, "best_length": 6}


def test_summarize_text_with_duplicates():
    summary = summarize_text("ab ab ba")
    assert summary == {"words": 3, "usable": 3, "best_length": 2}


def test_format_summary_zero():
    text = format_summary({"words": 0, "usable": 0, "best_length": 0})
    assert text == "0 of 0 words usable, best total length 0"


def test_large_pool_with_many_duplicates():
    rng = random.Random(0)
    letters = [chr(ord("a") + i) for i in range(20)]
    shuffled = letters[:]
    rng.shuffle(shuffled)
    pool = []
    pos = 0
    for size in (3, 3, 3, 3, 4, 4):
        pool.append("".join(shuffled[pos:pos + size]))
        pos += size
    while len(pool) < 24:
        pool.append("".join(rng.sample(letters, rng.randint(2, 4))))
    words = [_scramble(rng, rng.choice(pool)) for _ in range(100_000)]
    words += ["aab", "tt", "cc"] * 100
    rng.shuffle(words)

    start = time.perf_counter()
    result = max_unique_length(words)
    elapsed = time.perf_counter() - start

    assert result == 20
    assert elapsed < 1.0, f"took {elapsed:.2f}s"


def test_large_repeated_single_word():
    words = ["abc"] * 50_000 + ["aab"] * 50_000

    start = time.perf_counter()
    result = max_unique_length(words)
    elapsed = time.perf_counter() - start

    assert result == 3
    assert elapsed < 1.0, f"took {elapsed:.2f}s"


def test_large_small_alphabet():
    rng = random.Random(0)
    words = [
        "".join(rng.choices("abcdefgh", k=rng.randint(1, 6))) for _ in range(100_000)
    ]

    start = time.perf_counter()
    result = max_unique_length(words)
    elapsed = time.perf_counter() - start

    assert result == 8
    assert elapsed < 1.0, f"took {elapsed:.2f}s"
