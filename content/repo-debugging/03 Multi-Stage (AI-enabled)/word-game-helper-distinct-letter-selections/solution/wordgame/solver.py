"""Selecting words whose letters never overlap."""

from .bitmask import letter_mask, popcount


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
    # Identical strings and anagrams collapse to the same mask; only distinct
    # masks matter because a mask can never be combined with itself.
    masks = set(usable_masks(set(words)))
    masks.discard(0)

    # Every mask in ``reachable`` is the letter set of a valid selection.  Since
    # the letters are all distinct, the total length equals the popcount.
    reachable = {0}
    for mask in masks:
        for taken in list(reachable):
            if not taken & mask:
                reachable.add(taken | mask)
    return max(popcount(taken) for taken in reachable)
