import random

from cardgame.deck import Deck


def test_full_deck_has_52_unique_cards():
    deck = Deck()
    assert len(deck) == 52
    assert len(set(deck.deal(52))) == 52


def test_deal_removes_cards_from_deck():
    deck = Deck()
    hand = deck.deal(5)
    assert len(hand) == 5
    assert len(deck) == 47


def test_deal_more_than_remaining_raises():
    deck = Deck()
    deck.deal(50)
    try:
        deck.deal(3)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_shuffle_is_reproducible_with_a_seed():
    first = Deck(rng=random.Random(7))
    second = Deck(rng=random.Random(7))
    first.shuffle()
    second.shuffle()
    assert first.deal(52) == second.deal(52)
