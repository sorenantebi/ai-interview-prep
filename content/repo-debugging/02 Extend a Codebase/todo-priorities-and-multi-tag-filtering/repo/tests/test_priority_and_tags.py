from datetime import date

from todolist import models, queries
from todolist.models import Todo
from todolist.storage import TodoStore


def ids(todos):
    return [t.id for t in todos]


def test_default_priority_and_add_with_priority():
    assert Todo(id=1, title="a").priority == models.Priority.MEDIUM
    store = TodoStore()
    todo = store.add("urgent thing", priority=models.Priority.HIGH)
    assert todo.priority == models.Priority.HIGH
    assert store.add("normal thing").priority == models.Priority.MEDIUM


def test_priority_survives_store_round_trip():
    store = TodoStore()
    store.add("low one", priority=models.Priority.LOW)
    store.add("high one", priority=models.Priority.HIGH)
    restored = TodoStore.loads(store.dumps())
    assert [t.priority for t in restored.all()] == [
        models.Priority.LOW,
        models.Priority.HIGH,
    ]


def test_from_dict_without_priority_defaults_to_medium():
    legacy = {"id": 4, "title": "old", "due": None, "tags": [], "done": False}
    assert Todo.from_dict(legacy).priority == models.Priority.MEDIUM


def test_sorted_by_priority_then_due():
    P = models.Priority
    todos = [
        Todo(id=1, title="a", priority=P.LOW, due=date(2025, 1, 1)),
        Todo(id=2, title="b", priority=P.HIGH, due=date(2025, 6, 1)),
        Todo(id=3, title="c", priority=P.HIGH, due=date(2025, 2, 1)),
        Todo(id=4, title="d", priority=P.HIGH),
        Todo(id=5, title="e", priority=P.MEDIUM, due=date(2025, 3, 1)),
    ]
    assert ids(queries.sorted_by_priority(todos)) == [3, 2, 4, 5, 1]


def test_sorted_by_priority_is_stable():
    P = models.Priority
    d = date(2025, 3, 1)
    todos = [
        Todo(id=i, title=f"t{i}", priority=P.MEDIUM, due=d if i % 2 else None)
        for i in range(1, 7)
    ]
    assert ids(queries.sorted_by_priority(todos)) == [1, 3, 5, 2, 4, 6]


def test_filter_all_tags():
    todos = [
        Todo(id=1, title="a", tags=["home", "chore"]),
        Todo(id=2, title="b", tags=["home"]),
        Todo(id=3, title="c", tags=["Chore", "HOME", "weekend"]),
    ]
    assert ids(queries.filter_by_tags(todos, ["home", "chore"])) == [1, 3]
    assert ids(queries.filter_by_tags(todos, ["home", "chore"], mode="all")) == [1, 3]


def test_filter_any_tags():
    todos = [
        Todo(id=1, title="a", tags=["home"]),
        Todo(id=2, title="b", tags=["work"]),
        Todo(id=3, title="c", tags=["Chore"]),
        Todo(id=4, title="d"),
    ]
    assert ids(queries.filter_by_tags(todos, ["HOME", "chore"], mode="any")) == [1, 3]
