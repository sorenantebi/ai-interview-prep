from datetime import date, datetime, timedelta

from rooms.models import Booking
from rooms.report import hours_booked, summary, utilization
from rooms.service import BookingService, ConflictError
from rooms.timeutils import fits_in_day, next_midnight

DAY = date(2025, 3, 10)


def at(hour, minute=0, day=10):
    return datetime(2025, 3, day, hour, minute)


def test_chain_of_back_to_back_bookings():
    svc = BookingService()
    for h in range(8, 12):
        svc.book("Atlas", f"u{h}", at(h), at(h + 1))
    assert len(svc.schedule("Atlas", DAY)) == 4


def test_contained_booking_conflicts():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(12))
    try:
        svc.book("Atlas", "ben", at(10), at(11))
    except ConflictError:
        return
    assert False


def test_one_minute_overlap_conflicts():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(10))
    try:
        svc.book("Atlas", "ben", at(9, 59), at(11))
    except ConflictError:
        return
    assert False


def test_failed_booking_does_not_consume_id():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(10))
    try:
        svc.book("Atlas", "ben", at(9), at(10))
    except ConflictError:
        pass
    assert svc.book("Atlas", "cy", at(10), at(11)).booking_id == 2


def test_end_before_start_rejected():
    svc = BookingService()
    try:
        svc.book("Atlas", "ana", at(10), at(9))
    except ValueError:
        return
    assert False


def test_zero_length_rejected():
    try:
        Booking(1, "Atlas", "ana", at(9), at(9))
    except ValueError:
        return
    assert False


def test_midnight_booking_on_consecutive_days():
    svc = BookingService()
    svc.book("Atlas", "ana", at(23), at(0, day=11))
    svc.book("Atlas", "ben", at(23, day=11), at(0, day=12))
    assert len(svc.schedule("Atlas", date(2025, 3, 11))) == 1


def test_full_day_booking_allowed():
    svc = BookingService()
    b = svc.book("Atlas", "ana", at(0), at(0, day=11))
    assert b.duration == timedelta(hours=24)


def test_one_second_past_midnight_rejected():
    svc = BookingService()
    try:
        svc.book("Atlas", "ana", at(23), datetime(2025, 3, 11, 0, 0, 1))
    except ValueError:
        return
    assert False


def test_fits_in_day_helper():
    assert fits_in_day(at(9), at(10))
    assert fits_in_day(at(23), at(0, day=11))
    assert not fits_in_day(at(23), at(1, day=11))
    assert next_midnight(at(23, 59)) == at(0, day=11)


def test_midnight_booking_blocks_late_slot():
    svc = BookingService()
    svc.book("Atlas", "ana", at(22), at(0, day=11))
    try:
        svc.book("Atlas", "ben", at(23), at(0, day=11))
    except ConflictError:
        return
    assert False


def test_cancel_unknown_raises_keyerror():
    svc = BookingService()
    try:
        svc.cancel(42)
    except KeyError:
        return
    assert False


def test_free_slots_booking_before_opening():
    svc = BookingService()
    svc.book("Atlas", "ana", at(6), at(9))
    assert svc.free_slots("Atlas", DAY) == [(at(9), at(20))]


def test_free_slots_fully_booked():
    svc = BookingService()
    svc.book("Atlas", "ana", at(8), at(14))
    svc.book("Atlas", "ben", at(14), at(20))
    assert svc.free_slots("Atlas", DAY) == []


def test_hours_booked_small_and_empty():
    svc = BookingService()
    assert hours_booked([]) == 0
    b = svc.book("Atlas", "ana", at(9), at(9, 15))
    assert hours_booked([b]) == 0.25


def test_hours_booked_many_fractions():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(9, 45))
    svc.book("Atlas", "ben", at(10), at(10, 45))
    svc.book("Atlas", "cy", at(11), at(11, 30))
    assert hours_booked(svc.schedule("Atlas", DAY)) == 2.0


def test_hours_booked_full_day():
    svc = BookingService()
    b = svc.book("Atlas", "ana", at(0), at(0, day=11))
    assert hours_booked([b]) == 24


def test_utilization_empty_and_invalid():
    svc = BookingService()
    assert utilization(svc, "Atlas", DAY) == 0
    try:
        utilization(svc, "Atlas", DAY, open_hour=10, close_hour=10)
    except ValueError:
        return
    assert False


def test_summary_tie_broken_by_room_name():
    svc = BookingService()
    svc.book("Zed", "ana", at(9), at(10, 30))
    svc.book("Atlas", "ben", at(9), at(10, 30))
    assert summary(svc, DAY) == [("Atlas", 1.5), ("Zed", 1.5)]
