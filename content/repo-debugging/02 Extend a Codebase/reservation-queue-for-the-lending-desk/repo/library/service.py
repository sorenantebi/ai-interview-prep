"""Lending service: checkouts, returns and overdue reporting."""
from typing import Dict, List, Optional

from .errors import (
    AlreadyBorrowed,
    LoanLimitReached,
    NoCopiesAvailable,
    NotBorrowed,
    UnknownBook,
    UnknownMember,
)
from .holds import HoldQueue
from .models import Book, Loan, Member
from .utils import LOAN_DAYS, Clock, add_days


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
        """Lend one copy of ``isbn`` to the member."""
        member = self._member(member_id)
        book = self._book(isbn)
        if self.find_loan(member_id, isbn) is not None:
            raise AlreadyBorrowed(f"{member_id} already has {isbn}")
        if len(self.loans_for(member_id)) >= member.max_loans:
            raise LoanLimitReached(member_id)
        if book.available < 1:
            raise NoCopiesAvailable(isbn)
        book.available -= 1
        now = self.clock.now()
        loan = Loan(isbn, member_id, now, add_days(now, LOAN_DAYS))
        self.loans.append(loan)
        return loan

    def return_book(self, member_id: str, isbn: str) -> None:
        """Take a copy back and put it on the shelf."""
        loan = self.find_loan(member_id, isbn)
        if loan is None:
            raise NotBorrowed(f"{member_id} does not have {isbn}")
        self.loans.remove(loan)
        self._book(isbn).available += 1

    def overdue_loans(self) -> List[Loan]:
        now = self.clock.now()
        return [loan for loan in self.loans if loan.is_overdue(now)]
