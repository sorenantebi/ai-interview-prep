"""Exceptions raised by the shortener package."""


class ShortenerError(Exception):
    """Base class for all shortener errors."""


class InvalidUrlError(ShortenerError):
    """The URL to shorten is malformed or uses an unsupported scheme."""


class InvalidAliasError(ShortenerError):
    """A custom alias does not satisfy the alias rules."""


class AliasTakenError(ShortenerError):
    """The requested code or alias is already in use."""


class LinkNotFoundError(ShortenerError):
    """No link is stored under the given code."""


class LinkExpiredError(ShortenerError):
    """The link exists but its expiry time has passed."""
