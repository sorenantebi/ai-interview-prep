from datetime import datetime, timedelta

from library.errors import HoldError, NoCopiesAvailable
from library.models import Book, Member
from library.service import LendingService
from library.utils import Clock


def make_service():
    svc = LendingService(Clock(datetime(2024, 3, 1, 10, 0)))
    svc.add_book(Book("111", "Dune", 1))
    svc.add_book(Book("222", "Emma", 2))
    for i in range(1, 5):
        svc.add_member(Member(f"m{i}", f"Member {i}"))
    return svc


def expect_error(exc_type, func, *args):
    try:
        func(*args)
    except exc_type:
        return
    assert False, f"expected {exc_type.__name__}"


def test_place_hold_on_unavailable_book():
    svc = make_service()
    svc.checkout("m1", "111")
    hold = svc.place_hold("m2", "111")
    assert hold.member_id == "m2"
    assert not hold.is_ready
    assert svc.hold_position("m2", "111") == 1


def test_hold_rejected_while_copy_is_available():
    svc = make_service()
    expect_error(HoldError, svc.place_hold, "m2", "222")


def test_returned_copy_goes_to_first_in_queue():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.place_hold("m3", "111")
    now = svc.clock.now()
    ready = svc.return_book("m1", "111")
    assert ready.member_id == "m2"
    assert ready.ready_at == now
    assert ready.expires_at == now + timedelta(days=3)
    assert svc.books["111"].available == 0
    assert not svc.holds.get("111", "m3").is_ready


def test_reserved_copy_is_not_lent_to_others():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.return_book("m1", "111")
    expect_error(NoCopiesAvailable, svc.checkout, "m4", "111")


def test_holder_collects_reserved_copy():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.place_hold("m3", "111")
    svc.return_book("m1", "111")
    loan = svc.checkout("m2", "111")
    assert loan.member_id == "m2"
    assert svc.holds.get("111", "m2") is None
    assert svc.books["111"].available == 0
    assert svc.hold_position("m3", "111") == 1


def test_expired_hold_passes_copy_to_next_in_line():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.place_hold("m3", "111")
    svc.return_book("m1", "111")
    svc.clock.advance(days=3)
    expired = svc.expire_holds()
    assert [h.member_id for h in expired] == ["m2"]
    assert svc.holds.get("111", "m2") is None
    nxt = svc.holds.get("111", "m3")
    assert nxt.is_ready
    assert nxt.ready_at == svc.clock.now()
    assert nxt.expires_at == svc.clock.now() + timedelta(days=3)


def test_expired_hold_with_empty_queue_returns_copy_to_shelf():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.return_book("m1", "111")
    svc.clock.advance(days=3)
    svc.expire_holds()
    assert svc.books["111"].available == 1
    assert svc.checkout("m4", "111").member_id == "m4"


def test_cancelling_ready_hold_passes_copy_on():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.place_hold("m3", "111")
    svc.return_book("m1", "111")
    svc.cancel_hold("m2", "111")
    assert svc.holds.get("111", "m2") is None
    assert svc.holds.get("111", "m3").is_ready
