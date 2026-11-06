"""Lending service: checkouts, returns and overdue reporting."""
from typing import Dict, List, Optional

from .errors import (
    AlreadyBorrowed,
    HoldError,
    LoanLimitReached,
    NoCopiesAvailable,
    NotBorrowed,
    UnknownBook,
    UnknownMember,
)
from .holds import HoldQueue
from .models import Book, Hold, Loan, Member
from .utils import HOLD_DAYS, LOAN_DAYS, Clock, add_days


class LendingService:
    """In-memory lending desk."""

    def __init__(self, clock: Optional[Clock] = None) -> None:
        self.clock = clock if clock is not None else Clock()
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.loans: List[Loan] = []
        self.holds = HoldQueue()

    # -- registration -------------------------------------------------

    def add_book(self, book: Book) -> None:
        self.books[book.isbn] = book

    def add_member(self, member: Member) -> None:
        self.members[member.member_id] = member

    def _book(self, isbn: str) -> Book:
        try:
            return self.books[isbn]
        except KeyError:
            raise UnknownBook(isbn)

    def _member(self, member_id: str) -> Member:
        try:
            return self.members[member_id]
        except KeyError:
            raise UnknownMember(member_id)

    # -- loans ----------------------------------------------------------

    def find_loan(self, member_id: str, isbn: str) -> Optional[Loan]:
        for loan in self.loans:
            if loan.member_id == member_id and loan.isbn == isbn:
                return loan
        return None

    def loans_for(self, member_id: str) -> List[Loan]:
        return [loan for loan in self.loans if loan.member_id == member_id]

    def checkout(self, member_id: str, isbn: str) -> Loan:
        """Lend one copy of ``isbn`` to the member.

        A member with a ready hold collects the copy that was set aside for
        them; everybody else needs a copy that is available on the shelf.
        """
        self.expire_holds()
        member = self._member(member_id)
        book = self._book(isbn)
        if self.find_loan(member_id, isbn) is not None:
            raise AlreadyBorrowed(f"{member_id} already has {isbn}")
        if len(self.loans_for(member_id)) >= member.max_loans:
            raise LoanLimitReached(member_id)
        hold = self.holds.get(isbn, member_id)
        if hold is not None and hold.is_ready:
            self.holds.remove(isbn, member_id)
        elif book.available < 1:
            raise NoCopiesAvailable(isbn)
        else:
            book.available -= 1
        now = self.clock.now()
        loan = Loan(isbn, member_id, now, add_days(now, LOAN_DAYS))
        self.loans.append(loan)
        return loan

    def return_book(self, member_id: str, isbn: str) -> Optional[Hold]:
        """Take a copy back.

        Returns the hold that received the copy, or ``None`` if it went back
        on the shelf.
        """
        self.expire_holds()
        loan = self.find_loan(member_id, isbn)
        if loan is None:
            raise NotBorrowed(f"{member_id} does not have {isbn}")
        self.loans.remove(loan)
        return self._release_copy(isbn)

    def overdue_loans(self) -> List[Loan]:
        now = self.clock.now()
        return [loan for loan in self.loans if loan.is_overdue(now)]

    # -- holds ----------------------------------------------------------

    def _release_copy(self, isbn: str) -> Optional[Hold]:
        """A copy became free: reserve it for the next waiting hold or shelve it."""
        hold = self.holds.first_waiting(isbn)
        if hold is None:
            self._book(isbn).available += 1
            return None
        now = self.clock.now()
        hold.ready_at = now
        hold.expires_at = add_days(now, HOLD_DAYS)
        return hold

    def place_hold(self, member_id: str, isbn: str) -> Hold:
        """Put the member at the back of the queue for ``isbn``."""
        self.expire_holds()
        self._member(member_id)
        book = self._book(isbn)
        if book.available > 0:
            raise HoldError(f"{isbn} is available, borrow it instead")
        if self.find_loan(member_id, isbn) is not None:
            raise HoldError(f"{member_id} already has {isbn} on loan")
        if self.holds.get(isbn, member_id) is not None:
            raise HoldError(f"{member_id} already has a hold on {isbn}")
        hold = Hold(isbn, member_id, self.clock.now())
        self.holds.add(hold)
        return hold

    def cancel_hold(self, member_id: str, isbn: str) -> None:
        """Remove the member's hold; a ready hold hands its copy on."""
        self.expire_holds()
        hold = self.holds.remove(isbn, member_id)
        if hold.is_ready:
            self._release_copy(isbn)

    def hold_position(self, member_id: str, isbn: str) -> int:
        """1-based position of the member's hold in the queue."""
        self.expire_holds()
        return self.holds.position(isbn, member_id)

    def expire_holds(self) -> List[Hold]:
        """Drop expired ready holds and pass their copies on."""
        expired = self.holds.expired(self.clock.now())
        for hold in expired:
            self.holds.remove(hold.isbn, hold.member_id)
        for hold in expired:
            self._release_copy(hold.isbn)
        return expired
