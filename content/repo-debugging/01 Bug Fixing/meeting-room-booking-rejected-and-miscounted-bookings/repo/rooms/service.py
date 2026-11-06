"""Booking service: creates, cancels and queries room bookings."""

from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple

from rooms.models import Booking
from rooms.timeutils import day_start, fits_in_day


class ConflictError(Exception):
    """Raised when a requested booking collides with an existing one."""


class BookingService:
    """In-memory store of bookings with conflict detection."""

    def __init__(self):
        self._bookings: Dict[int, Booking] = {}
        self._next_id = 1

    def book(self, room: str, organizer: str, start: datetime, end: datetime) -> Booking:
        """Create a booking, or raise ValueError / ConflictError."""
        if not fits_in_day(start, end):
            raise ValueError("a booking must not run past midnight")
        candidate = Booking(self._next_id, room, organizer, start, end)
        for existing in self._bookings.values():
            if candidate.overlaps(existing):
                raise ConflictError(
                    f"{room} is already booked by {existing.organizer} "
                    f"({existing.start:%H:%M}-{existing.end:%H:%M})"
                )
        self._bookings[candidate.booking_id] = candidate
        self._next_id += 1
        return candidate

    def cancel(self, booking_id: int) -> None:
        """Remove a booking. Raises KeyError for unknown ids."""
        del self._bookings[booking_id]

    def rooms(self) -> List[str]:
        """Names of all rooms that have at least one booking, sorted."""
        return sorted({b.room for b in self._bookings.values()})

    def schedule(self, room: str, day: date) -> List[Booking]:
        """Bookings of ``room`` starting on ``day``, ordered by start time."""
        found = [
            b for b in self._bookings.values()
            if b.room == room and b.start.date() == day
        ]
        return sorted(found, key=lambda b: b.start)

    def free_slots(
        self, room: str, day: date, open_hour: int = 8, close_hour: int = 20
    ) -> List[Tuple[datetime, datetime]]:
        """Gaps between bookings inside the opening hours of ``day``."""
        opens = day_start(day) + timedelta(hours=open_hour)
        closes = day_start(day) + timedelta(hours=close_hour)
        slots = []
        cursor = opens
        for booking in self.schedule(room, day):
            gap_end = min(booking.start, closes)
            if gap_end > cursor:
                slots.append((cursor, gap_end))
            cursor = max(cursor, booking.end)
        if cursor < closes:
            slots.append((cursor, closes))
        return slots
