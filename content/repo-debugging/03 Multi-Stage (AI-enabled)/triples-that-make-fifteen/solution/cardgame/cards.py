"""Card model and parsing of the short text notation (``"KH"``, ``"10s"``, ``"ac"``)."""

from dataclasses import dataclass

SUITS = {"C": "clubs", "D": "diamonds", "H": "hearts", "S": "spades"}
RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")


def rank_value(rank):
    """Return the point value of a rank.

    Aces are worth 1, number cards their face value and J/Q/K ten points.
    """
    try:
        index = RANKS.index(rank)
    except ValueError:
        raise ValueError(f"unknown rank: {rank!r}") from None
    if index >= 10:
        return 10
    return index + 1


@dataclass(frozen=True)
class Card:
    """A single playing card, e.g. ``Card("K", "H")`` for the king of hearts."""

    rank: str
    suit: str

    def __post_init__(self):
        if self.rank not in RANKS:
            raise ValueError(f"unknown rank: {self.rank!r}")
        if self.suit not in SUITS:
            raise ValueError(f"unknown suit: {self.suit!r}")

    @property
    def value(self):
        """Point value of the card (1-10)."""
        return rank_value(self.rank)

    def __str__(self):
        return f"{self.rank}{self.suit}"


def parse_card(text):
    """Parse notation such as ``"KH"`` or ``"10s"`` into a :class:`Card`.

    Surrounding whitespace and letter case are ignored.
    """
    cleaned = text.strip().upper()
    if len(cleaned) < 2:
        raise ValueError(f"cannot parse card: {text!r}")
    return Card(cleaned[:-1], cleaned[-1])


def parse_cards(text):
    """Parse several cards separated by spaces and/or commas."""
    return [parse_card(part) for part in text.replace(",", " ").split()]
