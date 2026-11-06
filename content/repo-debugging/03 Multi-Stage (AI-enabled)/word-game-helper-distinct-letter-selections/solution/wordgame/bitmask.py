"""Helpers for representing words as bitmasks over the lowercase alphabet.

A word is mapped to an int in which bit ``i`` is set when the word contains
the letter ``chr(ord("a") + i)``.  Two words share no letters exactly when
their masks have no bits in common (``a & b == 0``).
"""

ALPHABET_SIZE = 26

_BITS = {chr(ord("a") + i): 1 << i for i in range(ALPHABET_SIZE)}


def letter_mask(word):
    """Return the letter mask of ``word``.

    Returns ``None`` when a letter occurs more than once, because such a word
    can never be part of a selection with distinct characters.  Raises
    ``ValueError`` for any character outside ``a``-``z``.
    """
    mask = 0
    for ch in word:
        bit = _BITS.get(ch)
        if bit is None:
            raise ValueError(f"unsupported character: {ch!r}")
        if mask & bit:
            return None
        mask |= bit
    return mask


def popcount(mask):
    """Return the number of bits set in ``mask``."""
    return bin(mask).count("1")


def letters_of(mask):
    """Return the letters present in ``mask`` as a string in alphabetical order."""
    return "".join(
        chr(ord("a") + i) for i in range(ALPHABET_SIZE) if (mask >> i) & 1
    )
