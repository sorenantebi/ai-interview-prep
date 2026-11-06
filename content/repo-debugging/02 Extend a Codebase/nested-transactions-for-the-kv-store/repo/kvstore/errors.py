"""Exceptions raised by the kvstore package."""


class KVError(Exception):
    """Base class for all errors raised on purpose by kvstore."""


class KeyNotFound(KVError):
    """Raised when a key is required but not present."""

    def __init__(self, key):
        super().__init__(f"key not found: {key!r}")
        self.key = key


class NoActiveTransaction(KVError):
    """Raised when commit/rollback is requested but no transaction is open."""

    def __init__(self, message="no active transaction"):
        super().__init__(message)


class UnknownCommand(KVError):
    """Raised by the interpreter for a command name it does not know."""

    def __init__(self, name):
        super().__init__(f"unknown command: {name}")
        self.name = name


class UsageError(KVError):
    """Raised by the interpreter when a command gets the wrong arguments."""

    def __init__(self, usage):
        super().__init__(f"usage: {usage}")
        self.usage = usage
