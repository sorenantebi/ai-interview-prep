"""In-memory storage and querying of catalog records."""

SORT_KEYS = {
    "id": lambda r: r.id,
    "name": lambda r: r.name.lower(),
    "price": lambda r: r.price_cents,
}


class RecordRepository:
    """Holds records and returns them filtered and sorted."""

    def __init__(self, records=None):
        self._records = list(records or [])

    def add(self, record):
        """Append a record to the repository."""
        self._records.append(record)

    def __len__(self):
        return len(self._records)

    def query(self, category=None, sort_by="id"):
        """Return a new list of records, optionally filtered by category.

        Raises ValueError if ``sort_by`` is not a supported sort key.
        """
        if sort_by not in SORT_KEYS:
            raise ValueError(f"unknown sort key: {sort_by}")
        records = self._records
        if category is not None:
            records = [r for r in records if r.category == category]
        return sorted(records, key=SORT_KEYS[sort_by])
