"""Core shortener service: ties together validation, encoding and storage."""

from .clock import SystemClock
from .encoding import encode
from .errors import AliasTakenError, LinkExpiredError, LinkNotFoundError
from .storage import LinkRecord, LinkStore
from .validation import validate_alias, validate_url

# The first generated code is "1000", so generated codes are at least 4 long.
FIRST_ID = 62 ** 3


class ShortenerService:
    """Creates short links and resolves them back to their URLs."""

    def __init__(self, store=None, clock=None):
        self._store = store if store is not None else LinkStore()
        self._clock = clock if clock is not None else SystemClock()
        self._next_id = FIRST_ID

    def shorten(self, url, alias=None, ttl=None):
        """Store ``url`` and return its short code.

        With ``alias`` the alias is used as the code; otherwise a code is
        generated. With ``ttl`` (seconds) the link expires ``ttl`` seconds
        after creation. All input is validated before any state changes.
        """
        url = validate_url(url)
        if alias is not None:
            alias = validate_alias(alias)
        if ttl is not None and ttl <= 0:
            raise ValueError("ttl must be a positive number of seconds")

        now = self._clock.now()
        if alias is not None:
            self._claim_alias(alias, now)
            code = alias
        else:
            code = self._generate_code()

        expires_at = None if ttl is None else now + ttl
        record = LinkRecord(
            code=code, url=url, created_at=now, expires_at=expires_at
        )
        self._store.add(record)
        return code

    def resolve(self, code):
        """Return the URL for ``code`` and count the hit."""
        record = self._get_live(code)
        record.hits += 1
        return record.url

    def stats(self, code):
        """Return the stored record for ``code`` without counting a hit."""
        return self._get_live(code)

    def purge_expired(self):
        """Delete every expired link and return how many were removed."""
        now = self._clock.now()
        expired = [r.code for r in self._store.records() if r.is_expired(now)]
        for code in expired:
            self._store.delete(code)
        return len(expired)

    def _get_live(self, code):
        record = self._store.get(code)
        if record is None:
            raise LinkNotFoundError(code)
        if record.is_expired(self._clock.now()):
            raise LinkExpiredError(code)
        return record

    def _claim_alias(self, alias, now):
        existing = self._store.get(alias)
        if existing is None:
            return
        if not existing.is_expired(now):
            raise AliasTakenError(alias)
        self._store.delete(alias)

    def _generate_code(self):
        while True:
            code = encode(self._next_id)
            self._next_id += 1
            if not self._store.exists(code):
                return code
