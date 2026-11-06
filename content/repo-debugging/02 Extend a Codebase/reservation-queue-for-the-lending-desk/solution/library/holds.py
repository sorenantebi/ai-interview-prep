"""Reservation queue ("holds") for books that are currently out on loan."""
from datetime import datetime
from typing import Dict, List, Optional

from .errors import HoldError
from .models import Hold


class HoldQueue:
    """Keeps one FIFO queue of :class:`Hold` objects per ISBN.

    Holds are stored in the order they were placed. Ready holds (a copy has
    been set aside for them) always form the front of their queue; the queue
    itself never changes a hold's state, the service does that.
    """

    def __init__(self) -> None:
        self._queues: Dict[str, List[Hold]] = {}

    def add(self, hold: Hold) -> None:
        """Append ``hold`` to the back of the queue for its ISBN."""
        self._queues.setdefault(hold.isbn, []).append(hold)

    def get(self, isbn: str, member_id: str) -> Optional[Hold]:
        """Return the member's hold on ``isbn`` or ``None``."""
        for hold in self._queues.get(isbn, []):
            if hold.member_id == member_id:
                return hold
        return None

    def remove(self, isbn: str, member_id: str) -> Hold:
        """Remove and return the member's hold; raise ``HoldError`` if absent."""
        queue = self._queues.get(isbn, [])
        for index, hold in enumerate(queue):
            if hold.member_id == member_id:
                return queue.pop(index)
        raise HoldError(f"{member_id} has no hold on {isbn}")

    def position(self, isbn: str, member_id: str) -> int:
        """1-based position in the queue (ready holds count); ``HoldError`` if absent."""
        for index, hold in enumerate(self._queues.get(isbn, []), start=1):
            if hold.member_id == member_id:
                return index
        raise HoldError(f"{member_id} has no hold on {isbn}")

    def first_waiting(self, isbn: str) -> Optional[Hold]:
        """Return the first hold of ``isbn`` that is not ready yet, if any."""
        for hold in self._queues.get(isbn, []):
            if not hold.is_ready:
                return hold
        return None

    def expired(self, now: datetime) -> List[Hold]:
        """Return all ready holds, over every ISBN, whose ``expires_at`` is at or before ``now``."""
        return [
            hold
            for queue in self._queues.values()
            for hold in queue
            if hold.expires_at is not None and hold.expires_at <= now
        ]
