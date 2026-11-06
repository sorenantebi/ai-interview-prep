"""Usage reports built on top of the booking service."""

from datetime import date
from typing import Iterable, List, Tuple

from rooms.models import Booking
from rooms.service import BookingService


def hours_booked(bookings: Iterable[Booking]) -> float:
    """Total booked time of the given bookings, in hours."""
    return sum(b.duration.seconds // 3600 for b in bookings)


def utilization(
    service: BookingService,
    room: str,
    day: date,
    open_hour: int = 8,
    close_hour: int = 20,
) -> float:
    """Fraction of the opening hours that ``room`` is booked on ``day``."""
    if close_hour <= open_hour:
        raise ValueError("close_hour must be after open_hour")
    booked = hours_booked(service.schedule(room, day))
    return round(booked / (close_hour - open_hour), 2)


def summary(service: BookingService, day: date) -> List[Tuple[str, float]]:
    """(room, hours booked) pairs for ``day``, busiest room first."""
    rows = [
        (room, hours_booked(service.schedule(room, day)))
        for room in service.rooms()
    ]
    return sorted(rows, key=lambda row: (-row[1], row[0]))
