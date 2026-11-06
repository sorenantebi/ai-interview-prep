"""Parsing and validation of query-string parameters."""

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50


class ParamError(ValueError):
    """Raised when a query parameter is missing, malformed or out of range."""


def _to_int(raw, name):
    try:
        return int(raw)
    except (TypeError, ValueError):
        raise ParamError(f"{name} must be an integer")


def parse_pagination(query):
    """Return ``(page, page_size)`` from a dict of query parameters.

    Values may be ints or numeric strings. The page size is capped at
    ``MAX_PAGE_SIZE``.
    """
    page = _to_int(query.get("page", 1), "page")
    page_size = _to_int(query.get("page_size", DEFAULT_PAGE_SIZE), "page_size")
    if page < 1:
        raise ParamError("page must be >= 1")
    if page_size < 1:
        raise ParamError("page_size must be >= 1")
    return page, min(page_size, MAX_PAGE_SIZE)
