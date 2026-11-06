"""Scoring rules for the fifteen family of games."""

TARGET = 15
BUST_LIMIT = 21


def hand_total(cards):
    """Return the summed point value of an iterable of cards."""
    return sum(card.value for card in cards)


def is_bust(cards, limit=BUST_LIMIT):
    """Return True if the cards are worth more than ``limit`` points."""
    return hand_total(cards) > limit


def find_triple_sum(cards, target=TARGET):
    """Return three cards from ``cards`` whose values add up to ``target``.

    ``cards`` is any iterable of :class:`Card` (a :class:`Hand` works too).
    The three cards must come from three different positions in the hand, so
    one card can never be used twice, while two equal cards in a multi-deck
    hand count as two cards. Any matching triple is acceptable. Return a tuple
    of three cards, or ``None`` when there is no such triple.
    """
    raise NotImplementedError


def count_triples_sum(cards, target=TARGET):
    """Count the triples of positions ``i < j < k`` whose values add up to ``target``.

    ``cards`` is any iterable of :class:`Card`. Equal cards at different
    positions give different triples. Must stay fast for hands of 100,000+
    cards.
    """
    raise NotImplementedError
