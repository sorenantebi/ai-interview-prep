"""A small in-memory LRU cache with tag based invalidation."""

from collections import OrderedDict

from catalog.models import CacheEntry


class LRUCache:
    """Least-recently-used cache holding at most ``capacity`` entries.

    Entries are kept ordered from least to most recently used. When the cache
    is full, the least recently used entry is evicted to make room.
    """

    def __init__(self, capacity=128):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity
        self._entries = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key, default=None):
        """Return the cached value for ``key`` or ``default`` on a miss."""
        entry = self._entries.get(key)
        if entry is None:
            self.misses += 1
            return default
        self.hits += 1
        return entry.value

    def put(self, key, value, tags=None):
        """Store ``value`` under ``key``, evicting the oldest entry if needed."""
        if tags is None:
            entry = CacheEntry(key, value)
        else:
            entry = CacheEntry(key, value, list(tags))
        self._entries[key] = entry
        self._entries.move_to_end(key)
        while len(self._entries) > self._capacity:
            self._entries.popitem(last=False)

    def tag(self, key, tag):
        """Add ``tag`` to an existing entry. Returns False if the key is absent."""
        entry = self._entries.get(key)
        if entry is None:
            return False
        entry.add_tag(tag)
        return True

    def tags_for(self, key):
        """Return a copy of the tags attached to ``key`` (empty if absent)."""
        entry = self._entries.get(key)
        return list(entry.tags) if entry is not None else []

    def invalidate_tag(self, tag):
        """Remove every entry carrying ``tag``. Returns how many were removed."""
        doomed = [k for k, e in self._entries.items() if e.has_tag(tag)]
        for key in doomed:
            del self._entries[key]
        return len(doomed)

    def keys(self):
        """Keys ordered from least to most recently used."""
        return list(self._entries)

    def clear(self):
        self._entries.clear()

    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

    def __contains__(self, key):
        return key in self._entries

    def __len__(self):
        return len(self._entries)
