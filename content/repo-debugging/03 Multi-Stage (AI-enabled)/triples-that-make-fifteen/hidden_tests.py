import random
import time
from collections import Counter
from itertools import combinations
from math import comb

from cardgame.cards import RANKS, SUITS, Card, parse_card, parse_cards, rank_value
from cardgame.deck import Deck
from cardgame.hand import Hand
from cardgame.rules import count_triples_sum, find_triple_sum, hand_total, is_bust

FULL_DECK = [Card(rank, suit) for suit in SUITS for rank in RANKS]
TENS_AND_ACES = [card for card in FULL_DECK if card.value in (10, 1)]


def brute_count(cards, target=15):
    return sum(
        1 for a, b, c in combinations(cards, 3) if a.value + b.value + c.value == target
    )


def reference_count(cards, target=15):
    """Independent check: dynamic programming over groups of equal values."""
    counts = Counter(card.value for card in cards)
    ways_by_state = {(0, 0): 1}
    for value, group_size in counts.items():
        updated = {}
        for (picked, total), ways in ways_by_state.items():
            for take in range(0, 4 - picked):
                new_total = total + take * value
                if new_total > target:
                    break
                key = (picked + take, new_total)
                updated[key] = updated.get(key, 0) + ways * comb(group_size, take)
        ways_by_state = updated
    return ways_by_state.get((3, target), 0)


def check_triple(cards, triple, target=15):
    assert triple is not None, "expected a triple but got None"
    assert len(triple) == 3
    available = Counter(cards)
    for card, needed in Counter(triple).items():
        assert available[card] >= needed, f"{card} used more often than it appears"
    assert sum(card.value for card in triple) == target


def test_every_rank_value():
    expected = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
                "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    assert set(expected) == set(RANKS)
    for rank, value in expected.items():
        assert rank_value(rank) == value, rank


def test_face_cards_ten_in_every_suit():
    for suit in SUITS:
        for rank in "JQK":
            assert parse_card(rank + suit).value == 10, rank + suit


def test_parse_cards_separators():
    assert [str(c) for c in parse_cards("kh, 5s  2d,10h")] == ["KH", "5S", "2D", "10H"]
    assert parse_cards("") == []


def test_hand_total_and_bust_with_jacks():
    hand = Hand.from_text("JH JS AD")
    assert hand_total(hand) == 21
    assert not is_bust(hand)
    assert is_bust(Hand.from_text("JH JS 2D"))


def test_deal_zero_and_exhaust():
    deck = Deck()
    assert deck.deal(0) == []
    assert len(deck) == 52
    assert len(deck.deal(52)) == 52
    assert len(deck) == 0
    try:
        deck.deal(1)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_find_triple_agrees_with_bruteforce():
    rng = random.Random(0)
    for _ in range(300):
        hand = rng.choices(FULL_DECK, k=rng.randint(0, 9))
        triple = find_triple_sum(hand)
        expected = brute_count(hand) > 0
        assert (triple is not None) == expected, [str(c) for c in hand]
        if triple is not None:
            check_triple(hand, triple)


def test_find_triple_custom_target():
    cards = parse_cards("AH 2S 3D")
    check_triple(cards, find_triple_sum(cards, target=6), target=6)
    assert find_triple_sum(cards, target=7) is None


def test_find_triple_accepts_hand_object():
    hand = Hand.from_text("9H 3S 3D KC")
    check_triple(list(hand), find_triple_sum(hand))


def test_find_triple_short_hands():
    assert find_triple_sum([]) is None
    assert find_triple_sum(parse_cards("5H 10S")) is None


def test_find_triple_with_equal_cards():
    five = Card("5", "H")
    check_triple([five] * 3, find_triple_sum([five] * 3))
    assert find_triple_sum([five] * 2) is None


def test_find_triple_unsolvable_larger_hand():
    rng = random.Random(0)
    hand = rng.choices(TENS_AND_ACES, k=120)
    assert find_triple_sum(hand) is None


def test_count_agrees_with_bruteforce():
    rng = random.Random(0)
    for _ in range(200):
        hand = rng.choices(FULL_DECK, k=rng.randint(0, 14))
        assert count_triples_sum(hand) == brute_count(hand), [str(c) for c in hand]


def test_count_empty_and_short_hands():
    assert count_triples_sum([]) == 0
    assert count_triples_sum(parse_cards("5H 5S")) == 0
    assert count_triples_sum([Card("5", "H")] * 4) == 4


def test_count_custom_target():
    assert count_triples_sum(parse_cards("KH QS JD 10C"), target=30) == 4
    assert count_triples_sum(parse_cards("KH QS AD"), target=21) == 1
    assert count_triples_sum(parse_cards("KH QS AD"), target=22) == 0


def test_count_large_random_hand_is_fast():
    rng = random.Random(0)
    hand = rng.choices(FULL_DECK, k=100_000)
    start = time.perf_counter()
    result = count_triples_sum(hand)
    elapsed = time.perf_counter() - start
    assert result == reference_count(hand)
    assert elapsed < 1.0, f"took {elapsed:.2f}s"


def test_count_large_identical_cards_exact():
    hand = [Card("5", "S")] * 100_000
    start = time.perf_counter()
    result = count_triples_sum(hand)
    elapsed = time.perf_counter() - start
    assert result == comb(100_000, 3)
    assert elapsed < 1.0, f"took {elapsed:.2f}s"


def test_count_large_hand_without_any_triple():
    rng = random.Random(1)
    hand = rng.choices(TENS_AND_ACES, k=100_000)
    start = time.perf_counter()
    result = count_triples_sum(hand)
    elapsed = time.perf_counter() - start
    assert result == 0
    assert elapsed < 1.0, f"took {elapsed:.2f}s"
