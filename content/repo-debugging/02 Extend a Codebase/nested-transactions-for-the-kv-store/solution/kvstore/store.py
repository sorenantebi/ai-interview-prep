"""The in-memory key-value store."""

from contextlib import contextmanager

from .errors import KeyNotFound, NoActiveTransaction
from .utils import MISSING, validate_key


class Store:
    """A dictionary-backed key-value store with string keys and arbitrary values.

    ``None`` is a perfectly valid value; use ``in`` or ``require`` to tell a stored
    ``None`` from an absent key.
    """

    def __init__(self, initial=None):
        self._data = {}
        self._undo_stack = []
        for key, value in (initial or {}).items():
            self.set(key, value)

    # -- raw writes -------------------------------------------------------
    def _put(self, key, value):
        self._data[key] = value

    def _drop(self, key):
        self._data.pop(key, None)

    def _record(self, key):
        """Remember the pre-transaction state of ``key`` in the innermost undo log."""
        if self._undo_stack:
            log = self._undo_stack[-1]
            if key not in log:
                log[key] = self._data.get(key, MISSING)

    # -- public API -------------------------------------------------------
    def get(self, key, default=None):
        """Return the value for ``key`` or ``default`` if it is absent."""
        return self._data.get(validate_key(key), default)

    def require(self, key):
        """Return the value for ``key`` or raise KeyNotFound."""
        validate_key(key)
        if key not in self._data:
            raise KeyNotFound(key)
        return self._data[key]

    def set(self, key, value):
        """Store ``value`` under ``key``, replacing any previous value."""
        validate_key(key)
        self._record(key)
        self._put(key, value)

    def delete(self, key):
        """Remove ``key``. Return True if it existed, False otherwise."""
        validate_key(key)
        if key not in self._data:
            return False
        self._record(key)
        self._drop(key)
        return True

    def keys(self):
        """Return all keys in sorted order."""
        return sorted(self._data)

    def items(self):
        """Return ``(key, value)`` pairs sorted by key."""
        return [(key, self._data[key]) for key in sorted(self._data)]

    def count_value(self, value):
        """Return how many keys currently hold ``value``."""
        return sum(1 for stored in self._data.values() if stored == value)

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    # -- transactions -----------------------------------------------------
    @property
    def depth(self):
        """Number of currently open transactions."""
        return len(self._undo_stack)

    def begin(self):
        """Open a new transaction, nested inside the current one if there is one."""
        self._undo_stack.append({})

    def rollback(self):
        """Undo all changes made in the innermost transaction and close it."""
        if not self._undo_stack:
            raise NoActiveTransaction()
        log = self._undo_stack.pop()
        for key, old in log.items():
            if old is MISSING:
                self._drop(key)
            else:
                self._put(key, old)

    def commit(self):
        """Close the innermost transaction, keeping its changes."""
        if not self._undo_stack:
            raise NoActiveTransaction()
        log = self._undo_stack.pop()
        if self._undo_stack:
            parent = self._undo_stack[-1]
            for key, old in log.items():
                # The parent must keep the *earliest* original value it has seen.
                parent.setdefault(key, old)

    @contextmanager
    def transaction(self):
        """Context manager: commit on success, roll back if the block raises."""
        self.begin()
        try:
            yield self
        except BaseException:
            self.rollback()
            raise
        else:
            self.commit()
