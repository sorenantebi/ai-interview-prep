import random
from datetime import date, timedelta

from todolist import models, queries
from todolist.models import Todo
from todolist.storage import TodoStore

P = models.Priority


def ids(todos):
    return [t.id for t in todos]


def sample():
    return [
        Todo(id=1, title="a", tags=["home", "chore"]),
        Todo(id=2, title="b", tags=["work"]),
        Todo(id=3, title="c", tags=["home", "work", "chore"]),
        Todo(id=4, title="d"),
    ]


def test_priority_enum_ordering():
    assert P.HIGH < P.MEDIUM < P.LOW
    assert sorted([P.LOW, P.HIGH, P.MEDIUM]) == [P.HIGH, P.MEDIUM, P.LOW]


def test_to_dict_stores_priority_by_name():
    assert Todo(id=1, title="a", priority=P.HIGH).to_dict()["priority"] == "HIGH"
    assert Todo(id=2, title="b").to_dict()["priority"] == "MEDIUM"


def test_legacy_json_loads_with_medium_priority():
    text = (
        '{"next_id": 3, "todos": ['
        '{"id": 1, "title": "x", "due": "2025-01-02", "tags": ["a"], "done": false},'
        '{"id": 2, "title": "y", "due": null, "tags": [], "done": true}]}'
    )
    store = TodoStore.loads(text)
    assert [t.priority for t in store.all()] == [P.MEDIUM, P.MEDIUM]
    assert store.add("z", priority=P.LOW).id == 3


def test_store_dict_round_trip_all_priorities():
    for p in P:
        todo = Todo(id=1, title="a", priority=p, due=date(2025, 4, 4))
        assert Todo.from_dict(todo.to_dict()) == todo


def test_sort_empty_and_single():
    assert queries.sorted_by_priority([]) == []
    t = Todo(id=1, title="a")
    assert queries.sorted_by_priority([t]) == [t]


def test_sort_returns_new_list_without_mutating():
    todos = [
        Todo(id=1, title="a", priority=P.LOW),
        Todo(id=2, title="b", priority=P.HIGH),
    ]
    original = list(todos)
    result = queries.sorted_by_priority(todos)
    assert todos == original
    assert result is not todos
    assert ids(result) == [2, 1]


def test_sort_all_undated_orders_by_priority_only():
    todos = [
        Todo(id=1, title="a", priority=P.LOW),
        Todo(id=2, title="b", priority=P.MEDIUM),
        Todo(id=3, title="c", priority=P.HIGH),
        Todo(id=4, title="d", priority=P.MEDIUM),
    ]
    assert ids(queries.sorted_by_priority(todos)) == [3, 2, 4, 1]


def test_sort_ties_keep_input_order_even_when_reversed():
    d = date(2025, 9, 9)
    todos = [Todo(id=i, title=f"t{i}", due=d, priority=P.HIGH) for i in (5, 4, 3, 2, 1)]
    assert ids(queries.sorted_by_priority(todos)) == [5, 4, 3, 2, 1]


def test_sort_matches_reference_on_random_data():
    rng = random.Random(0)
    base = date(2025, 1, 1)
    todos = []
    for i in range(300):
        due = None if rng.random() < 0.3 else base + timedelta(days=rng.randint(0, 5))
        todos.append(Todo(id=i, title=f"t{i}", due=due, priority=rng.choice(list(P))))
    expected = sorted(
        range(len(todos)),
        key=lambda i: (
            todos[i].priority.value,
            todos[i].due is None,
            todos[i].due or date.max,
            i,
        ),
    )
    assert ids(queries.sorted_by_priority(todos)) == expected


def test_filter_all_requires_every_tag_and_can_be_empty():
    todos = sample()
    assert ids(queries.filter_by_tags(todos, ["home", "work"])) == [3]
    assert queries.filter_by_tags(todos, ["home", "missing"]) == []


def test_filter_any_with_unknown_and_known_tags():
    todos = sample()
    assert ids(queries.filter_by_tags(todos, ["missing", "work"], mode="any")) == [2, 3]
    assert queries.filter_by_tags(todos, ["missing"], mode="any") == []


def test_filter_empty_tags_returns_everything_as_new_list():
    todos = sample()
    for mode in ("all", "any"):
        result = queries.filter_by_tags(todos, [], mode=mode)
        assert ids(result) == [1, 2, 3, 4]
        assert result is not todos
    assert ids(queries.filter_by_tags(todos, [" ", ""], mode="any")) == [1, 2, 3, 4]


def test_filter_bare_string_is_one_tag():
    todos = sample()
    assert ids(queries.filter_by_tags(todos, "Home")) == [1, 3]
    assert ids(queries.filter_by_tags(todos, "work", mode="any")) == [2, 3]


def test_filter_invalid_mode_raises():
    for tags in (["home"], []):
        try:
            queries.filter_by_tags(sample(), tags, mode="some")
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"


def test_filter_accepts_sets_and_generators():
    todos = sample()
    assert ids(queries.filter_by_tags(todos, {"home", "chore"})) == [1, 3]
    assert ids(queries.filter_by_tags(iter(todos), (t for t in ["work"]))) == [2, 3]


def test_filter_does_not_mutate_and_preserves_order():
    todos = list(reversed(sample()))
    snapshot = list(todos)
    result = queries.filter_by_tags(todos, ["work"], mode="any")
    assert todos == snapshot
    assert ids(result) == [3, 2]


def test_store_pipeline_filter_then_sort():
    store = TodoStore()
    store.add("a", tags=["home"], priority=P.LOW, due=date(2025, 1, 1))
    store.add("b", tags=["home", "chore"], priority=P.HIGH, due=date(2025, 5, 1))
    store.add("c", tags=["chore"], priority=P.HIGH, due=date(2025, 2, 1))
    store.add("d", tags=["work"], priority=P.HIGH)
    chosen = queries.filter_by_tags(store.all(), ["home", "chore"], mode="any")
    assert ids(queries.sorted_by_priority(chosen)) == [3, 2, 1]
