from datetime import date

from todolist.models import Todo
from todolist.queries import by_tag, pending, sorted_by_due


def test_pending_and_by_tag():
    todos = [
        Todo(id=1, title="a", tags=["Home"]),
        Todo(id=2, title="b", tags=["home"], done=True),
        Todo(id=3, title="c", tags=["work"]),
    ]
    assert [t.id for t in pending(todos)] == [1, 3]
    assert [t.id for t in by_tag(todos, "HOME")] == [1, 2]


def test_sorted_by_due_puts_undated_last():
    todos = [
        Todo(id=1, title="a"),
        Todo(id=2, title="b", due=date(2025, 3, 2)),
        Todo(id=3, title="c", due=date(2025, 3, 1)),
    ]
    assert [t.id for t in sorted_by_due(todos)] == [3, 2, 1]
