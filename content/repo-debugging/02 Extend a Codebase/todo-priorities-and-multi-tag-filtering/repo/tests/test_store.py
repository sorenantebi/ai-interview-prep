from datetime import date

from todolist.storage import TodoNotFound, TodoStore


def test_add_complete_remove():
    store = TodoStore()
    a = store.add("first")
    b = store.add("second", due=date(2025, 1, 2))
    assert (a.id, b.id) == (1, 2)
    store.complete(1)
    assert store.get(1).done
    store.remove(2)
    assert len(store) == 1
    try:
        store.get(2)
    except TodoNotFound:
        pass
    else:
        assert False, "expected TodoNotFound"


def test_dumps_loads_round_trip():
    store = TodoStore()
    store.add("alpha", tags=["x"])
    store.add("beta", due=date(2025, 2, 3))
    restored = TodoStore.loads(store.dumps())
    assert restored.all() == store.all()
    assert restored.add("gamma").id == 3
