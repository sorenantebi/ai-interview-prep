"""Human-readable summaries of a pasted word list."""

from .solver import max_unique_length, usable_masks
from .words import clean_words


def summarize_text(text):
    """Summarise free-form text containing words separated by whitespace or commas.

    Returns a dict with the number of cleaned words (``words``), how many of
    them are usable (``usable``) and the best total length of a selection with
    distinct letters (``best_length``).
    """
    tokens = text.replace(",", " ").split()
    words = clean_words(tokens)
    return {
        "words": len(words),
        "usable": len(usable_masks(words)),
        "best_length": max_unique_length(words),
    }


def format_summary(summary):
    """Format the dict returned by :func:`summarize_text` as one line."""
    return "{usable} of {words} words usable, best total length {best_length}".format(
        **summary
    )
