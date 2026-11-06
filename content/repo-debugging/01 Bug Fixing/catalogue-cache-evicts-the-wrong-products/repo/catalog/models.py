"""Plain data objects used by the catalogue."""

from dataclasses import dataclass


@dataclass
class Product:
    """A product as stored in the catalogue backend."""

    id: int
    name: str
    category: str
    price_cents: int


class CacheEntry:
    """A single value held by the cache together with its invalidation tags."""

    def __init__(self, key, value, tags=[]):
        self.key = key
        self.value = value
        self.tags = tags

    def add_tag(self, tag):
        """Attach ``tag`` to this entry (no-op if it is already present)."""
        if tag not in self.tags:
            self.tags.append(tag)

    def has_tag(self, tag):
        return tag in self.tags
