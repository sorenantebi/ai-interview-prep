import time
from datetime import datetime, timedelta

from library.errors import (
    HoldError,
    LoanLimitReached,
    NoCopiesAvailable,
    UnknownBook,
    UnknownMember,
)
from library.models import Book, Member
from library.service import LendingService
from library.utils import Clock


def make_service():
    svc = LendingService(Clock(datetime(2024, 3, 1, 10, 0)))
    svc.add_book(Book("111", "Dune", 1))
    svc.add_book(Book("222", "Emma", 2))
    svc.add_book(Book("333", "Ulysses", 1))
    svc.add_book(Book("444", "Hamlet", 1))
    for i in range(1, 6):
        svc.add_member(Member(f"m{i}", f"Member {i}"))
    return svc


def expect_error(exc_type, func, *args):
    try:
        func(*args)
    except exc_type:
        return
    assert False, f"expected {exc_type.__name__}"


def ready_queue():
    """m1 borrowed Dune, m2 and m3 are waiting, m1 returned it: m2 is ready."""
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.place_hold("m3", "111")
    svc.return_book("m1", "111")
    return svc


def test_hold_still_valid_just_before_three_days():
    svc = ready_queue()
    svc.clock.advance(days=2, hours=23)
    assert svc.expire_holds() == []
    assert svc.holds.get("111", "m2") is not None
    assert svc.holds.get("111", "m3") is not None and not svc.holds.get("111", "m3").is_ready


def test_hold_expires_exactly_at_three_days():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.return_book("m1", "111")
    svc.clock.advance(days=3)
    expired = svc.expire_holds()
    assert len(expired) == 1 and expired[0].member_id == "m2"
    assert svc.books["111"].available == 1


def test_expired_holder_cannot_collect_without_explicit_sweep():
    svc = ready_queue()
    svc.clock.advance(days=3)
    expect_error(NoCopiesAvailable, svc.checkout, "m2", "111")
    assert svc.checkout("m3", "111").member_id == "m3"


def test_checkout_sweeps_expired_hold_with_empty_queue():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.return_book("m1", "111")
    svc.clock.advance(days=4)
    assert svc.checkout("m4", "111").member_id == "m4"


def test_duplicate_hold_rejected():
    svc = ready_queue()
    expect_error(HoldError, svc.place_hold, "m3", "111")
    expect_error(HoldError, svc.place_hold, "m2", "111")


def test_current_borrower_cannot_hold_same_book():
    svc = make_service()
    svc.checkout("m1", "111")
    expect_error(HoldError, svc.place_hold, "m1", "111")


def test_place_hold_unknown_ids():
    svc = make_service()
    expect_error(UnknownBook, svc.place_hold, "m1", "999")
    expect_error(UnknownMember, svc.place_hold, "zz", "111")


def test_cancel_waiting_hold_keeps_order_and_copy():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.place_hold("m3", "111")
    svc.place_hold("m4", "111")
    svc.cancel_hold("m3", "111")
    assert svc.hold_position("m4", "111") == 2
    ready = svc.return_book("m1", "111")
    assert ready.member_id == "m2"
    assert svc.books["111"].available == 0


def test_cancel_missing_hold_raises():
    svc = make_service()
    svc.checkout("m1", "111")
    expect_error(HoldError, svc.cancel_hold, "m2", "111")
    expect_error(HoldError, svc.hold_position, "m2", "111")


def test_cancel_ready_hold_with_empty_queue_restores_shelf():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.return_book("m1", "111")
    svc.cancel_hold("m2", "111")
    assert svc.books["111"].available == 1


def test_return_without_queue_goes_to_shelf():
    svc = make_service()
    svc.checkout("m1", "111")
    assert svc.return_book("m1", "111") is None
    assert svc.books["111"].available == 1


def test_positions_count_ready_holds():
    svc = ready_queue()
    assert svc.hold_position("m2", "111") == 1
    assert svc.hold_position("m3", "111") == 2


def test_multiple_copies_give_multiple_ready_holds():
    svc = make_service()
    svc.checkout("m1", "222")
    svc.checkout("m2", "222")
    for member in ("m3", "m4", "m5"):
        svc.place_hold(member, "222")
    assert svc.return_book("m1", "222").member_id == "m3"
    assert svc.return_book("m2", "222").member_id == "m4"
    assert not svc.holds.get("222", "m5").is_ready
    assert svc.hold_position("m5", "222") == 3
    assert svc.books["222"].available == 0


def test_two_expiries_in_one_sweep():
    svc = make_service()
    svc.checkout("m1", "222")
    svc.checkout("m2", "222")
    for member in ("m3", "m4", "m5"):
        svc.place_hold(member, "222")
    svc.return_book("m1", "222")
    svc.return_book("m2", "222")
    svc.clock.advance(days=3)
    expired = svc.expire_holds()
    assert sorted(h.member_id for h in expired) == ["m3", "m4"]
    assert svc.holds.get("222", "m5").is_ready
    assert svc.books["222"].available == 1


def test_window_restarts_for_next_holder():
    svc = ready_queue()
    svc.clock.advance(days=3)
    svc.expire_holds()
    svc.clock.advance(days=2, hours=23)
    assert svc.expire_holds() == []
    svc.clock.advance(hours=1)
    assert [h.member_id for h in svc.expire_holds()] == ["m3"]


def test_collected_hold_gets_normal_due_date():
    svc = ready_queue()
    svc.clock.advance(days=1)
    loan = svc.checkout("m2", "111")
    assert loan.due == loan.checked_out + timedelta(days=14)
    assert loan.checked_out == svc.clock.now()


def test_holder_at_loan_limit_cannot_collect_but_keeps_hold():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.place_hold("m2", "111")
    svc.checkout("m2", "222")
    svc.checkout("m2", "333")
    svc.checkout("m2", "444")
    svc.return_book("m1", "111")
    expect_error(LoanLimitReached, svc.checkout, "m2", "111")
    assert svc.holds.get("111", "m2").is_ready
    assert svc.books["111"].available == 0


def test_long_queue_is_served_in_order():
    svc = make_service()
    for i in range(200):
        svc.add_member(Member(f"x{i}", f"Extra {i}"))
    svc.checkout("m1", "111")
    for i in range(200):
        svc.place_hold(f"x{i}", "111")
    current = "m1"
    start = time.perf_counter()
    for i in range(200):
        ready = svc.return_book(current, "111")
        assert ready.member_id == f"x{i}"
        svc.checkout(ready.member_id, "111")
        current = ready.member_id
    assert time.perf_counter() - start < 2.0
    assert svc.return_book(current, "111") is None
    assert svc.books["111"].available == 1
