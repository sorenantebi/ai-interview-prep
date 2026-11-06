from datetime import date, datetime

from rooms.report import hours_booked, summary, utilization
from rooms.service import BookingService

DAY = date(2025, 3, 10)


def at(hour, minute=0):
    return datetime(2025, 3, 10, hour, minute)


def test_hours_booked_whole_hours():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(11))
    assert hours_booked(svc.schedule("Atlas", DAY)) == 2


def test_hours_booked_fractional():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(10, 30))
    assert hours_booked(svc.schedule("Atlas", DAY)) == 1.5


def test_utilization():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(10, 30))
    svc.book("Atlas", "ben", at(13), at(14))
    assert utilization(svc, "Atlas", DAY) == 0.21


def test_summary_busiest_first():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(10, 30))
    svc.book("Borealis", "ben", at(9), at(12))
    assert summary(svc, DAY) == [("Borealis", 3.0), ("Atlas", 1.5)]
