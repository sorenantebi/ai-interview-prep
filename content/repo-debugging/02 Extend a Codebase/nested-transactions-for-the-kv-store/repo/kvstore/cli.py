"""A tiny text command interpreter on top of Store."""

from .errors import KVError, UnknownCommand, UsageError
from .store import Store
from .utils import tokenize


class Interpreter:
    """Executes commands such as ``SET key value`` and returns the reply text.

    Replies: ``OK`` for writes, the value (or ``NULL``) for ``GET``, ``1``/``0`` for
    ``DELETE`` and a number for ``COUNT``. Library errors become ``ERROR: <message>``.
    """

    def __init__(self, store=None):
        self.store = store if store is not None else Store()
        self._handlers = {
            "SET": self._set,
            "GET": self._get,
            "DELETE": self._delete,
            "COUNT": self._count,
        }

    def execute(self, line):
        """Run one command line. Returns the reply, or None for a blank line."""
        parts = tokenize(line)
        if not parts:
            return None
        name = parts[0].upper()
        try:
            handler = self._handlers.get(name)
            if handler is None:
                raise UnknownCommand(name)
            return handler(parts[1:])
        except KVError as exc:
            return f"ERROR: {exc}"

    def run(self, script):
        """Run a multi-line script and return the list of non-empty replies."""
        replies = []
        for line in script.splitlines():
            reply = self.execute(line)
            if reply is not None:
                replies.append(reply)
        return replies

    @staticmethod
    def _expect(args, count, usage):
        if len(args) != count:
            raise UsageError(usage)

    def _set(self, args):
        self._expect(args, 2, "SET key value")
        self.store.set(args[0], args[1])
        return "OK"

    def _get(self, args):
        self._expect(args, 1, "GET key")
        value = self.store.get(args[0], "NULL")
        return str(value)

    def _delete(self, args):
        self._expect(args, 1, "DELETE key")
        return "1" if self.store.delete(args[0]) else "0"

    def _count(self, args):
        self._expect(args, 1, "COUNT value")
        return str(self.store.count_value(args[0]))
