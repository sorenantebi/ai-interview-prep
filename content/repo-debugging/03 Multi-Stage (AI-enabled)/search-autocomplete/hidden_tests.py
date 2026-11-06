import heapq
import random
import string
import time

from autocomplete.loader import parse_line, parse_lines
from autocomplete.service import AutocompleteService
from autocomplete.text import normalize


# ---------------------------------------------------------------- helpers

def brute_force(counts, prefix, k):
    key = normalize(prefix)
    matches = [(-c, p) for p, c in counts.items() if p.startswith(key)]
    return [(p, -neg) for neg, p in heapq.nsmallest(k, matches)]


def answer(service, prefix, k):
    return [(s.phrase, s.count) for s in service.suggest(prefix, k)]


def names(suggestions):
    return [s.phrase for s in suggestions]


def _vocabulary(rng, size):
    words = []
    seen = set()
    while len(words) < size:
        word = "".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(3, 5)))
        if word not in seen:
            seen.add(word)
            words.append(word)
    return words


_LARGE = {}


def _large():
    if "service" not in _LARGE:
        rng = random.Random(0)
        words = _vocabulary(rng, 330)
        pairs = [a + " " + b for a in words for b in words]
        phrases = rng.sample(pairs, 100000)
        data = [(p, rng.randint(1, 1000)) for p in phrases]
        service = AutocompleteService()
        service.load(data)
        _LARGE["data"] = data
        _LARGE["service"] = service
    return _LARGE["data"], _LARGE["service"]


def _queries(data, n, rng):
    out = []
    for _ in range(n):
        phrase = data[rng.randrange(len(data))][0]
        out.append(phrase[: rng.randint(1, min(8, len(phrase)))])
    return out


# ------------------------------------------------------------ edge cases

def test_normalize_handles_unicode_whitespace_and_case():
    assert normalize("new\u00a0york") == "new york"
    assert normalize("\u00c4PFEL\tStrudel") == "\u00e4pfel strudel"


def test_normalize_output_is_canonical():
    for raw in ["  A  B ", "X\tY", "Already Clean", "", "\n", "mixed \t Case\r\nlines"]:
        out = normalize(raw)
        assert out == out.lower(), repr(raw)
        assert out == " ".join(out.split()), repr(raw)
        assert normalize(out) == out, repr(raw)


def test_phrase_equal_to_prefix_is_a_completion():
    service = AutocompleteService()
    service.load([("pizza", 2), ("pizza hut", 9), ("pizzas", 1)])
    assert names(service.suggest("pizza")) == ["pizza hut", "pizza", "pizzas"]
    assert service.suggest("pizza ") == service.suggest("pizza")


def test_unknown_prefix_gives_empty_list():
    service = AutocompleteService()
    service.load([("tea", 1)])
    assert service.suggest("teas") == []
    assert service.suggest("x") == []


def test_k_larger_than_number_of_matches():
    service = AutocompleteService()
    service.load([("a", 1), ("ab", 2), ("abc", 3)])
    assert names(service.suggest("", k=100)) == ["abc", "ab", "a"]


def test_k_beyond_typical_cache_size_matches_brute_force():
    service = AutocompleteService()
    data = [("item%02d" % i, (i % 7) + 1) for i in range(40)]
    service.load(data)
    counts = dict(data)
    for k in (11, 25, 40, 60):
        assert answer(service, "item", k) == brute_force(counts, "item", k), k


def test_ties_are_alphabetical_whatever_the_insert_order():
    rng = random.Random(0)
    phrases = ["w%02d" % i for i in range(30)]
    rng.shuffle(phrases)
    service = AutocompleteService()
    service.load([(p, 4) for p in phrases])
    assert names(service.suggest("w", k=12)) == sorted(phrases)[:12]
    assert names(service.suggest("w", k=3)) == ["w00", "w01", "w02"]


def test_new_records_reorder_results():
    service = AutocompleteService()
    service.load([("alpha", 3), ("alps", 2), ("alpine", 1)])
    assert names(service.suggest("al")) == ["alpha", "alps", "alpine"]
    service.record("alpine", 5)
    assert names(service.suggest("al")) == ["alpine", "alpha", "alps"]
    service.record("alps", 3)
    assert answer(service, "al", 5) == [("alpine", 6), ("alps", 5), ("alpha", 3)]


def test_phrase_from_outside_the_top_results_can_jump_in():
    service = AutocompleteService()
    service.load([("q%02d" % i, 10) for i in range(20)])
    service.record("qzz", 50)
    assert names(service.suggest("q", k=3)) == ["qzz", "q00", "q01"]
    service.record("q19", 100)
    assert answer(service, "q", 3) == [("q19", 110), ("qzz", 50), ("q00", 10)]


def test_empty_prefix_returns_global_top():
    service = AutocompleteService()
    service.load([("b", 2), ("a", 2), ("c", 9)])
    assert names(service.suggest("")) == ["c", "a", "b"]
    assert service.suggest("   ") == service.suggest("")


def test_default_k_is_five():
    service = AutocompleteService()
    service.load([("p%d" % i, i) for i in range(1, 9)])
    assert names(service.suggest("p")) == ["p8", "p7", "p6", "p5", "p4"]


def test_loader_handles_crlf_and_rejects_garbage():
    assert parse_line("a b\t4\r\n") == ("a b", 4)
    assert list(parse_lines(["\r\n", "x\t1\n"])) == [("x", 1)]
    try:
        parse_line("no count here")
    except ValueError:
        pass
    else:
        assert False, "expected ValueError"


def test_random_operations_match_brute_force():
    rng = random.Random(4)
    words = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 3))) for _ in range(40)]
    pool = sorted({" ".join(rng.choice(words) for _ in range(rng.randint(1, 2))) for _ in range(160)})
    service = AutocompleteService()
    counts = {}
    for step in range(600):
        phrase = rng.choice(pool)
        count = rng.randint(1, 4)
        raw = phrase.upper() if rng.random() < 0.3 else phrase
        service.record(raw, count)
        counts[phrase] = counts.get(phrase, 0) + count
        prefix = rng.choice(pool)[: rng.randint(0, 4)]
        k = rng.randint(1, 15)
        assert answer(service, prefix, k) == brute_force(counts, prefix, k), (step, prefix, k)


# ------------------------------------------------------- large inputs

def test_large_index_matches_brute_force():
    data, service = _large()
    counts = dict(data)
    prefixes = _queries(data, 12, random.Random(2)) + ["", "a", "zz", "qx"]
    for prefix in prefixes:
        expected = brute_force(counts, prefix, 10)
        for k in (1, 5, 10):
            assert answer(service, prefix, k) == expected[:k], (prefix, k)


def test_many_queries_on_large_index_are_fast():
    data, service = _large()
    queries = _queries(data, 1500, random.Random(1))
    start = time.perf_counter()
    for prefix in queries:
        service.suggest(prefix, 5)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, "1500 queries took %.2fs" % elapsed


def test_interleaved_updates_and_queries_are_fast_and_correct():
    rng = random.Random(3)
    words = _vocabulary(rng, 150)
    phrases = [a + " " + b for a in words for b in words]
    rng.shuffle(phrases)
    service = AutocompleteService()
    counts = {}
    for phrase in phrases[:20000]:
        count = rng.randint(1, 50)
        service.record(phrase, count)
        counts[phrase] = count
    ops = []
    for _ in range(2000):
        phrase = phrases[rng.randrange(len(phrases))]
        ops.append((phrase, rng.randint(1, 30), phrase[: rng.randint(1, 6)]))

    start = time.perf_counter()
    answers = []
    for phrase, count, prefix in ops:
        service.record(phrase, count)
        answers.append(service.suggest(prefix, 5))
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, "2000 record+suggest rounds took %.2fs" % elapsed

    for i, (phrase, count, prefix) in enumerate(ops):
        counts[phrase] = counts.get(phrase, 0) + count
        if i % 100 == 99:
            got = [(s.phrase, s.count) for s in answers[i]]
            assert got == brute_force(counts, prefix, 5), i
