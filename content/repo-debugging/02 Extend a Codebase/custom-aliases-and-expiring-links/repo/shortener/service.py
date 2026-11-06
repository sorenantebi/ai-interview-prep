"""Core shortener service: ties together validation, encoding and storage."""

from .clock import SystemClock
from .encoding import encode
from .errors import LinkNotFoundError
from .storage import LinkRecord, LinkStore
from .validation import validate_url

# The first generated code is "1000", so generated codes are at least 4 long.
FIRST_ID = 62 ** 3


class ShortenerService:
    """Creates short links and resolves them back to their URLs."""

    def __init__(self, store=None, clock=None):
        self._store = store if store is not None else LinkStore()
        self._clock = clock if clock is not None else SystemClock()
        self._next_id = FIRST_ID

    def shorten(self, url):
        """Store ``url`` under a freshly generated code and return the code."""
        url = validate_url(url)
        code = self._generate_code()
        record = LinkRecord(code=code, url=url, created_at=self._clock.now())
        self._store.add(record)
        return code

    def resolve(self, code):
        """Return the URL for ``code`` and count the hit."""
        record = self._store.get(code)
        if record is None:
            raise LinkNotFoundError(code)
        record.hits += 1
        return record.url

    def stats(self, code):
        """Return the stored record for ``code`` without counting a hit."""
        record = self._store.get(code)
        if record is None:
            raise LinkNotFoundError(code)
        return record

    def _generate_code(self):
        code = encode(self._next_id)
        self._next_id += 1
        return code
