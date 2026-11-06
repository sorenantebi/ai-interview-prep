"""Scoring rules for the fifteen family of games."""

from collections import Counter
from math import comb

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
    by_value = {}
    for card in cards:
        by_value.setdefault(card.value, []).append(card)
    values = sorted(by_value)
    for i, a in enumerate(values):
        for b in values[i:]:
            c = target - a - b
            if c < b or c not in by_value:
                continue
            needed = Counter((a, b, c))
            if all(len(by_value[v]) >= n for v, n in needed.items()):
                picked = []
                for v, n in needed.items():
                    picked.extend(by_value[v][:n])
                return tuple(picked)
    return None


def count_triples_sum(cards, target=TARGET):
    """Count the triples of positions ``i < j < k`` whose values add up to ``target``.

    ``cards`` is any iterable of :class:`Card`. Equal cards at different
    positions give different triples. Must stay fast for hands of 100,000+
    cards.
    """
    counts = Counter(card.value for card in cards)
    values = sorted(counts)
    total = 0
    for i, a in enumerate(values):
        for b in values[i:]:
            c = target - a - b
            if c < b or c not in counts:
                continue
            if a == b == c:
                total += comb(counts[a], 3)
            elif a == b:
                total += comb(counts[a], 2) * counts[c]
            elif b == c:
                total += counts[a] * comb(counts[b], 2)
            else:
                total += counts[a] * counts[b] * counts[c]
    return total
