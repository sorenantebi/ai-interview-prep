from datetime import datetime, timedelta

from library.errors import (
    AlreadyBorrowed,
    LoanLimitReached,
    NoCopiesAvailable,
    NotBorrowed,
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
    for member_id, name in (("m1", "Ada Example"), ("m2", "Bo Example"), ("m3", "Cy Example")):
        svc.add_member(Member(member_id, name))
    return svc


def expect_error(exc_type, func, *args):
    try:
        func(*args)
    except exc_type:
        return
    assert False, f"expected {exc_type.__name__}"


def test_checkout_sets_due_date():
    svc = make_service()
    loan = svc.checkout("m1", "111")
    assert loan.due == loan.checked_out + timedelta(days=14)
    assert svc.books["111"].available == 0


def test_checkout_without_copies_fails():
    svc = make_service()
    svc.checkout("m1", "111")
    expect_error(NoCopiesAvailable, svc.checkout, "m2", "111")


def test_same_title_twice_is_rejected():
    svc = make_service()
    svc.checkout("m1", "222")
    expect_error(AlreadyBorrowed, svc.checkout, "m1", "222")


def test_loan_limit():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.checkout("m1", "222")
    svc.checkout("m1", "333")
    expect_error(LoanLimitReached, svc.checkout, "m1", "444")


def test_return_makes_copy_available():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.return_book("m1", "111")
    assert svc.books["111"].available == 1
    expect_error(NotBorrowed, svc.return_book, "m1", "111")


def test_overdue_loans():
    svc = make_service()
    svc.checkout("m1", "111")
    svc.clock.advance(days=14)
    assert svc.overdue_loans() == []
    svc.clock.advance(hours=1)
    assert len(svc.overdue_loans()) == 1
