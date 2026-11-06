"""Data models for the booking service."""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Booking:
    """A reservation of one room for the half-open interval [start, end)."""

    booking_id: int
    room: str
    organizer: str
    start: datetime
    end: datetime

    def __post_init__(self):
        if self.end <= self.start:
            raise ValueError("a booking must end after it starts")

    @property
    def duration(self) -> timedelta:
        """Length of the booking."""
        return self.end - self.start

    def overlaps(self, other: "Booking") -> bool:
        """Return True if both bookings are for the same room and share time."""
        if self.room != other.room:
            return False
        return self.start < other.end and other.start < self.end
