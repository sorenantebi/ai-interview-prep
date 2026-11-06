from cardgame.cards import parse_cards
from cardgame.hand import Hand
from cardgame.rules import count_triples_sum, find_triple_sum, hand_total, is_bust


def check_triple(cards, triple, target=15):
    assert triple is not None, "expected a triple but got None"
    assert len(triple) == 3
    remaining = list(cards)
    for card in triple:
        assert card in remaining, f"{card} is not available in the hand"
        remaining.remove(card)
    assert sum(card.value for card in triple) == target


def test_hand_total_with_face_cards():
    assert hand_total(Hand.from_text("JH QS")) == 20
    assert hand_total(Hand.from_text("AS 9D 10C")) == 20


def test_is_bust():
    assert not is_bust(parse_cards("JH 10S AD"))
    assert is_bust(parse_cards("KH QS 2D"))


def test_find_triple_basic():
    cards = parse_cards("5H 4S 6D KC")
    check_triple(cards, find_triple_sum(cards))


def test_find_triple_with_face_card():
    cards = parse_cards("JH 4S AD 9C")
    triple = find_triple_sum(cards)
    check_triple(cards, triple)
    assert {card.rank for card in triple} == {"J", "4", "A"}


def test_find_triple_none():
    assert find_triple_sum(parse_cards("5H 5S 9D")) is None
    assert find_triple_sum(parse_cards("10H JS QD KC AH")) is None


def test_count_triples_small():
    assert count_triples_sum(parse_cards("5H 5S 5D 5C")) == 4


def test_count_triples_mixed():
    assert count_triples_sum(parse_cards("AH 4S 10D KC QH")) == 3
