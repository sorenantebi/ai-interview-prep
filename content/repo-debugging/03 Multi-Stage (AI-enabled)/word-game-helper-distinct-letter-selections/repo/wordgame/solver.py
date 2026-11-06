"""Selecting words whose letters never overlap."""

from .bitmask import letter_mask


def usable_masks(words):
    """Return the letter masks of all words that do not repeat a letter.

    The result keeps the input order and keeps duplicates, so it has one entry
    per usable input word.
    """
    masks = []
    for word in words:
        mask = letter_mask(word)
        if mask is not None:
            masks.append(mask)
    return masks


def max_unique_length(words):
    """Return the largest total length of a selection with all-distinct letters.

    A selection is a sub-collection of ``words`` (each list entry used at most
    once) in which no letter occurs more than once across all chosen words.
    Words that repeat a letter themselves are ignored.  Returns ``0`` when no
    word is usable.

    ``words`` must already be cleaned (lowercase ``a``-``z`` only).
    """
    raise NotImplementedError("max_unique_length is not implemented yet")
