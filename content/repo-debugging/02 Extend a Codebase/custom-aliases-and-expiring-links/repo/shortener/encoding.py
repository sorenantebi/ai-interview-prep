"""Base62 encoding of integer ids into short codes."""

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)
_INDEX = {ch: i for i, ch in enumerate(ALPHABET)}


def encode(number):
    """Encode a non-negative integer as a base62 string."""
    if number < 0:
        raise ValueError("number must be non-negative")
    if number == 0:
        return ALPHABET[0]
    digits = []
    while number:
        number, remainder = divmod(number, BASE)
        digits.append(ALPHABET[remainder])
    return "".join(reversed(digits))


def decode(text):
    """Decode a base62 string back into an integer."""
    if not text:
        raise ValueError("cannot decode an empty string")
    value = 0
    for ch in text:
        digit = _INDEX.get(ch)
        if digit is None:
            raise ValueError("invalid character %r in code" % ch)
        value = value * BASE + digit
    return value
