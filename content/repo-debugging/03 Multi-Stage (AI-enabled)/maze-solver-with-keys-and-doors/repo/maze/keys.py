"""Helpers for the key and door symbols used in maze files."""

KEY_LETTERS = "abcdef"
DOOR_LETTERS = KEY_LETTERS.upper()


def is_key(symbol: str) -> bool:
    """Return True if ``symbol`` is a key (lowercase ``a``-``f``)."""
    return symbol in KEY_LETTERS


def is_door(symbol: str) -> bool:
    """Return True if ``symbol`` is a door (uppercase ``A``-``F``)."""
    return symbol in DOOR_LETTERS


def key_bit(symbol: str) -> int:
    """Return the bit that represents the given key in a key bitmask."""
    return 1 << KEY_LETTERS.index(symbol.lower())


def door_bit(symbol: str) -> int:
    """Return the bit of the key that opens the given door."""
    return 1 << DOOR_LETTERS.index(symbol)
