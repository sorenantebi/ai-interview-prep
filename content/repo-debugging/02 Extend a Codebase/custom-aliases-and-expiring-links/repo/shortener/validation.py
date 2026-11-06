"""Input validation helpers for the shortener."""

from urllib.parse import urlsplit

from .errors import InvalidUrlError

MAX_URL_LENGTH = 2048
ALLOWED_SCHEMES = ("http", "https")


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
