"""A player's hand of cards."""

from .cards import parse_cards


class Hand:
    """An ordered collection of cards held by one player."""

    def __init__(self, cards=()):
        self._cards = list(cards)

    @classmethod
    def from_text(cls, text):
        """Build a hand from notation like ``"KH 5S 10D"``."""
        return cls(parse_cards(text))

    def add(self, card):
        """Add a card to the hand."""
        self._cards.append(card)

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)

    def __str__(self):
        return " ".join(str(card) for card in self._cards)
