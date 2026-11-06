from datetime import date, datetime

from rooms.service import BookingService, ConflictError

DAY = date(2025, 3, 10)


def at(hour, minute=0, day=10):
    return datetime(2025, 3, day, hour, minute)


def test_ids_increment():
    svc = BookingService()
    a = svc.book("Atlas", "ana", at(9), at(10))
    b = svc.book("Atlas", "ben", at(11), at(12))
    assert (a.booking_id, b.booking_id) == (1, 2)


def test_overlapping_booking_rejected():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(11))
    try:
        svc.book("Atlas", "ben", at(10), at(12))
    except ConflictError:
        return
    assert False, "expected ConflictError"


def test_same_time_different_rooms_ok():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(10))
    svc.book("Borealis", "ben", at(9), at(10))
    assert svc.rooms() == ["Atlas", "Borealis"]


def test_back_to_back_bookings_allowed():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(10))
    nxt = svc.book("Atlas", "ben", at(10), at(11))
    assert nxt.start == at(10)
    svc.book("Atlas", "cy", at(8), at(9))
    assert len(svc.schedule("Atlas", DAY)) == 3


def test_booking_ending_at_midnight_allowed():
    svc = BookingService()
    late = svc.book("Atlas", "ana", at(23), at(0, day=11))
    assert late in svc.schedule("Atlas", DAY)


def test_booking_crossing_midnight_rejected():
    svc = BookingService()
    try:
        svc.book("Atlas", "ana", at(22), at(1, day=11))
    except ValueError:
        return
    assert False, "expected ValueError"


def test_cancel_frees_the_slot():
    svc = BookingService()
    first = svc.book("Atlas", "ana", at(9), at(10))
    svc.cancel(first.booking_id)
    svc.book("Atlas", "ben", at(9), at(10))
    assert [b.organizer for b in svc.schedule("Atlas", DAY)] == ["ben"]


def test_schedule_sorted_by_start():
    svc = BookingService()
    svc.book("Atlas", "late", at(15), at(16))
    svc.book("Atlas", "early", at(9), at(10))
    assert [b.organizer for b in svc.schedule("Atlas", DAY)] == ["early", "late"]


def test_free_slots_between_bookings():
    svc = BookingService()
    svc.book("Atlas", "ana", at(9), at(10))
    svc.book("Atlas", "ben", at(13), at(14))
    assert svc.free_slots("Atlas", DAY) == [
        (at(8), at(9)),
        (at(10), at(13)),
        (at(14), at(20)),
    ]


def test_free_slots_with_back_to_back_bookings():
    svc = BookingService()
    svc.book("Atlas", "ana", at(8), at(10))
    svc.book("Atlas", "ben", at(10), at(12))
    assert svc.free_slots("Atlas", DAY) == [(at(12), at(20))]
