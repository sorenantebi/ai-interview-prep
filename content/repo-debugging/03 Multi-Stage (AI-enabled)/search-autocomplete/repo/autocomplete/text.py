"""Text helpers shared by the indexing and query paths."""

import re

_WHITESPACE = re.compile(r"\s+")


def normalize(text):
    """Return the canonical form of a phrase or query.

    The result is lower-case, has no leading or trailing whitespace, and every
    run of whitespace (spaces, tabs, newlines) is collapsed to a single space.
    ``None`` is treated as the empty string.
    """
    if not text:
        return ""
    if text == text.strip() and "  " not in text:
        return text
    return _WHITESPACE.sub(" ", text.strip()).lower()
