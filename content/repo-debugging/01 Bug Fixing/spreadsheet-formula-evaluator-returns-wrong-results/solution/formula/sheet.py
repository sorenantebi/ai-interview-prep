"""A small in-memory sheet that stores numbers and formulas."""

from .errors import EvalError
from .evaluator import Evaluator
from .parser import parse


def _key(ref):
    """Canonical storage key for a cell reference."""
    return ref.strip().upper()


class Sheet:
    """Cells hold either a number or a formula string starting with '='."""

    def __init__(self):
        self._cells = {}
        self._stack = []

    def set(self, ref, content):
        """Store a number or a formula (a string starting with '=') in a cell."""
        key = _key(ref)
        if isinstance(content, str) and content.startswith("="):
            self._cells[key] = content
            return
        try:
            self._cells[key] = float(content)
        except (TypeError, ValueError):
            raise EvalError(f"cell {key} must hold a number or a formula") from None

    def value(self, ref):
        """Return the computed value of a cell (empty cells are 0)."""
        return self._compute(_key(ref))

    def evaluate(self, formula):
        """Evaluate an ad-hoc formula; a leading '=' is optional."""
        text = formula.strip()
        if text.startswith("="):
            text = text[1:]
        return self._run(text)

    def _run(self, text):
        return Evaluator(self._lookup).evaluate(parse(text))

    def _lookup(self, name):
        return self._compute(_key(name))

    def _compute(self, key):
        content = self._cells.get(key)
        if content is None:
            return 0.0
        if isinstance(content, str):
            if key in self._stack:
                raise EvalError(f"circular reference at {key}")
            self._stack.append(key)
            try:
                return self._run(content[1:])
            finally:
                self._stack.pop()
        return content
