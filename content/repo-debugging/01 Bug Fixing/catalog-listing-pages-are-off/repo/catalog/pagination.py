"""Generic offset-based pagination helpers."""

from dataclasses import dataclass, field


@dataclass
class Page:
    """One page of results plus the metadata clients need."""

    items: list = field(default_factory=list)
    page: int = 1
    page_size: int = 10
    total: int = 0
    has_next: bool = False


def offset_for(page, page_size):
    """Index of the first item on a 1-based ``page``."""
    return page * page_size


def has_more(offset, page_size, total):
    """True if there are items after the page starting at ``offset``."""
    return offset + page_size <= total


def total_pages(total, page_size):
    """Number of pages needed to show ``total`` items."""
    return -(-total // page_size)


def paginate(items, page, page_size):
    """Slice ``items`` into the requested 1-based page."""
    total = len(items)
    start = offset_for(page, page_size)
    chunk = items[start:start + page_size]
    return Page(
        items=chunk,
        page=page,
        page_size=page_size,
        total=total,
        has_next=has_more(start, page_size, total),
    )
