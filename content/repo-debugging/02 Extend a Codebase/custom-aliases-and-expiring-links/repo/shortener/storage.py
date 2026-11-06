"""Storage layer: the link record and an in-memory store."""

from dataclasses import dataclass

from .errors import AliasTakenError


@dataclass
class LinkRecord:
    """A stored short link."""

    code: str
    url: str
    created_at: float
    hits: int = 0


class LinkStore:
    """Keeps link records in a dict keyed by short code."""

    def __init__(self):
        self._records = {}

    def add(self, record):
        """Store a new record; the code must not be in use yet."""
        if record.code in self._records:
            raise AliasTakenError(record.code)
        self._records[record.code] = record

    def get(self, code):
        """Return the record for ``code`` or ``None``."""
        return self._records.get(code)

    def exists(self, code):
        return code in self._records

    def delete(self, code):
        """Remove a record if present."""
        self._records.pop(code, None)

    def records(self):
        """Return a snapshot list of all records."""
        return list(self._records.values())

    def __len__(self):
        return len(self._records)
