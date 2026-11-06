"""Pure query helpers over lists of todos."""

from datetime import date
from typing import Iterable, List

from .models import Todo
from .utils import normalize_tag


def pending(todos: Iterable[Todo]) -> List[Todo]:
    """Return the todos that are not done yet."""
    return [t for t in todos if not t.done]


def by_tag(todos: Iterable[Todo], tag: str) -> List[Todo]:
    """Return the todos carrying ``tag`` (case-insensitive)."""
    wanted = normalize_tag(tag)
    return [t for t in todos if wanted in t.tags]


def due_before(todos: Iterable[Todo], cutoff: date) -> List[Todo]:
    """Return todos whose due date is strictly before ``cutoff``."""
    return [t for t in todos if t.due is not None and t.due < cutoff]


def sorted_by_due(todos: Iterable[Todo]) -> List[Todo]:
    """Return todos ordered by due date, undated ones last."""
    return sorted(todos, key=lambda t: (t.due is None, t.due or date.max))
