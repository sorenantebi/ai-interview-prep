from kvstore.errors import KeyNotFound, NoActiveTransaction
from kvstore.store import Store


def _raises(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return True
    return False


def test_set_and_get():
    store = Store()
    store.set("a", 1)
    assert store.get("a") == 1
    assert store.get("zzz") is None
    assert store.get("zzz", 7) == 7


def test_none_is_a_real_value():
    store = Store({"a": None})
    assert "a" in store
    assert store.get("a", 5) is None
    assert store.require("a") is None


def test_require_missing_raises():
    store = Store()
    assert _raises(KeyNotFound, store.require, "nope")


def test_delete_returns_flag():
    store = Store({"a": 1})
    assert store.delete("a") is True
    assert store.delete("a") is False
    assert len(store) == 0


def test_keys_sorted():
    store = Store({"b": 1, "a": 2, "c": 3})
    assert store.keys() == ["a", "b", "c"]
    assert store.items() == [("a", 2), ("b", 1), ("c", 3)]


def test_depth_starts_at_zero():
    store = Store()
    assert store.depth == 0
    store.begin()
    assert store.depth == 1
    store.commit()
    assert store.depth == 0


def test_rollback_restores_overwritten_deleted_and_new_keys():
    store = Store({"a": 1, "b": 2})
    store.begin()
    store.set("a", 10)
    store.delete("b")
    store.set("c", 3)
    assert store.get("a") == 10 and "b" not in store and store.get("c") == 3
    store.rollback()
    assert store.items() == [("a", 1), ("b", 2)]


def test_rollback_only_undoes_innermost():
    store = Store()
    store.begin()
    store.set("a", 1)
    store.begin()
    store.set("a", 2)
    store.set("b", 9)
    store.rollback()
    assert store.depth == 1
    assert store.get("a") == 1 and "b" not in store
    store.rollback()
    assert "a" not in store


def test_inner_commit_then_outer_rollback_undoes_everything():
    store = Store({"a": 0})
    store.begin()
    store.set("a", 1)
    store.begin()
    store.set("z", 5)
    store.commit()
    assert store.depth == 1 and store.get("z") == 5
    store.rollback()
    assert store.items() == [("a", 0)]


def test_commit_and_rollback_without_transaction_raise():
    store = Store()
    assert _raises(NoActiveTransaction, store.commit)
    assert _raises(NoActiveTransaction, store.rollback)


def test_context_manager_commits_and_rolls_back():
    store = Store()
    with store.transaction():
        store.set("a", 1)
    assert store.get("a") == 1 and store.depth == 0
    try:
        with store.transaction():
            store.set("a", 2)
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    else:
        assert False, "exception must propagate"
    assert store.get("a") == 1 and store.depth == 0
