"""Plain data objects used by the lending service."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Book:
    """A title in the catalogue.

    ``copies`` is the number the library owns; ``available`` is how many of
    them can be borrowed right now (defaults to all of them).
    """

    isbn: str
    title: str
    copies: int
    available: Optional[int] = None

    def __post_init__(self):
        if self.available is None:
            self.available = self.copies


@dataclass
class Member:
    """A registered library member."""

    member_id: str
    name: str
    max_loans: int = 3


@dataclass
class Loan:
    """A book currently borrowed by a member."""

    isbn: str
    member_id: str
    checked_out: datetime
    due: datetime

    def is_overdue(self, now: datetime) -> bool:
        return now > self.due


@dataclass
class Hold:
    """A member's place in the queue for a book.

    A hold is *waiting* until a copy is set aside for it. From then on it is
    *ready*: ``ready_at`` and ``expires_at`` are filled in.
    """

    isbn: str
    member_id: str
    placed_at: datetime
    ready_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    @property
    def is_ready(self) -> bool:
        return self.ready_at is not None
