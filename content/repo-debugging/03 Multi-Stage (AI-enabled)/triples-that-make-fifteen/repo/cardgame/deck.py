"""A deck of cards that can be shuffled and dealt from."""

import random

from .cards import RANKS, SUITS, Card


class Deck:
    """A pile of cards. Dealing takes cards from the top of the pile."""

    def __init__(self, cards=None, rng=None):
        if cards is None:
            cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        self._cards = list(cards)
        self._rng = rng if rng is not None else random.Random()

    def __len__(self):
        return len(self._cards)

    def shuffle(self):
        """Shuffle the remaining cards in place using the deck's own RNG."""
        self._rng.shuffle(self._cards)

    def deal(self, count=1):
        """Remove ``count`` cards from the deck and return them as a list."""
        if count < 0 or count > len(self._cards):
            raise ValueError(
                f"cannot deal {count} cards from a deck of {len(self._cards)}"
            )
        start = len(self._cards) - count
        dealt = self._cards[start:]
        del self._cards[start:]
        return dealt
