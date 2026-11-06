from datetime import date

from todolist.models import Todo


def test_tags_are_normalised():
    todo = Todo(id=1, title="Write report", tags=[" Work ", "URGENT", "work", ""])
    assert todo.tags == frozenset({"work", "urgent"})


def test_dict_round_trip():
    todo = Todo(id=7, title="Pay rent", due=date(2025, 5, 1), tags=["home"], done=True)
    restored = Todo.from_dict(todo.to_dict())
    assert restored == todo
