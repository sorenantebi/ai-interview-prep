"""Input validation helpers for the shortener."""

import re
from urllib.parse import urlsplit

from .errors import InvalidAliasError, InvalidUrlError

MAX_URL_LENGTH = 2048
ALLOWED_SCHEMES = ("http", "https")

ALIAS_PATTERN = re.compile(r"[A-Za-z0-9_-]{3,32}")
RESERVED_ALIASES = frozenset({"api", "admin", "static", "health"})


def validate_url(raw):
    """Return the normalised URL, or raise ``InvalidUrlError``.

    Surrounding whitespace is stripped. Only absolute http(s) URLs with a
    host part are accepted.
    """
    if not isinstance(raw, str):
        raise InvalidUrlError("url must be a string")
    url = raw.strip()
    if not url:
        raise InvalidUrlError("url must not be empty")
    if len(url) > MAX_URL_LENGTH:
        raise InvalidUrlError("url is too long")
    parts = urlsplit(url)
    if parts.scheme.lower() not in ALLOWED_SCHEMES:
        raise InvalidUrlError("unsupported scheme: %r" % parts.scheme)
    if not parts.netloc:
        raise InvalidUrlError("url has no host")
    return url


def validate_alias(alias):
    """Return ``alias`` unchanged, or raise ``InvalidAliasError``.

    Aliases are 3-32 ASCII letters, digits, ``-`` or ``_``. They are
    case-sensitive, but the reserved names are matched case-insensitively.
    """
    if not isinstance(alias, str):
        raise InvalidAliasError("alias must be a string")
    if ALIAS_PATTERN.fullmatch(alias) is None:
        raise InvalidAliasError(
            "alias must be 3-32 characters of A-Z, a-z, 0-9, '-' or '_'"
        )
    if alias.lower() in RESERVED_ALIASES:
        raise InvalidAliasError("alias %r is reserved" % alias)
    return alias
