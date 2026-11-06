"""Exceptions raised by the lending service."""


class LibraryError(Exception):
    """Base class for all lending errors."""


class UnknownBook(LibraryError):
    """The ISBN is not in the catalogue."""


class UnknownMember(LibraryError):
    """The member id is not registered."""


class NoCopiesAvailable(LibraryError):
    """Every copy of the book is on loan or set aside for someone else."""


class LoanLimitReached(LibraryError):
    """The member already has the maximum number of loans."""


class AlreadyBorrowed(LibraryError):
    """The member already has this title on loan."""


class NotBorrowed(LibraryError):
    """The member does not have this title on loan."""


class HoldError(LibraryError):
    """A hold cannot be placed, found or cancelled."""
