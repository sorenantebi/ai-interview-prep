"""Small helpers shared across the kvstore package."""


class _Missing:
    """Type of the MISSING sentinel.

    ``None`` is a legitimate stored value, so "there is no value" needs its own marker.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "MISSING"

    def __bool__(self):
        return False


MISSING = _Missing()


def validate_key(key):
    """Return ``key`` if it is a non-empty string, otherwise raise TypeError."""
    if not isinstance(key, str) or not key:
        raise TypeError("keys must be non-empty strings")
    return key


def tokenize(line, maxsplit=2):
    """Split a command line into at most ``maxsplit + 1`` whitespace separated parts.

    The last part keeps its inner whitespace, so ``SET k hello world`` yields
    ``["SET", "k", "hello world"]``.
    """
    return line.strip().split(None, maxsplit)
