"""Cleaning of raw user input before it reaches the solver."""


def clean_words(raw_words):
    """Normalise raw tokens into solver-ready words.

    Each token is stripped and lower-cased.  Tokens that are empty or contain
    anything other than the ASCII letters ``a``-``z`` are dropped.  The order
    of the remaining words is preserved.
    """
    cleaned = []
    for token in raw_words:
        word = token.strip().lower()
        if word.isascii() and word.isalpha():
            cleaned.append(word)
    return cleaned
