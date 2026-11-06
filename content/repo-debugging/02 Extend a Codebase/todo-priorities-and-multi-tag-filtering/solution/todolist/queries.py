"""Pure query helpers over lists of todos."""

from datetime import date
from typing import Iterable, List, Union

from .models import Todo
from .utils import normalize_tag, normalize_tags


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


def sorted_by_priority(todos: Iterable[Todo]) -> List[Todo]:
    """Return todos ordered by priority (high first), then due date.

    Undated todos come last within a priority. The sort is stable, so todos
    that tie on both keys keep their original relative order.
    """
    return sorted(
        todos,
        key=lambda t: (t.priority, t.due is None, t.due or date.max),
    )


def filter_by_tags(
    todos: Iterable[Todo],
    tags: Union[str, Iterable[str]],
    mode: str = "all",
) -> List[Todo]:
    """Return todos matching several tags, keeping the input order.

    ``mode="all"`` requires every tag, ``mode="any"`` at least one. Tags are
    normalised like todo tags; a bare string is a single tag and an empty
    selection matches everything.
    """
    if mode not in ("all", "any"):
        raise ValueError(f"unknown mode: {mode!r}")
    wanted = normalize_tags([tags] if isinstance(tags, str) else tags)
    if not wanted:
        return list(todos)
    if mode == "all":
        return [t for t in todos if wanted <= t.tags]
    return [t for t in todos if wanted & t.tags]
