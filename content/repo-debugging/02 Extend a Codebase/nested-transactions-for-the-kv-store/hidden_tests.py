from kvstore.cli import Interpreter
from kvstore.errors import NoActiveTransaction
from kvstore.store import Store


def _raises(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return True
    return False


def test_rollback_restores_none_value():
    store = Store({"a": None})
    store.begin()
    store.set("a", 5)
    store.rollback()
    assert "a" in store and store.get("a", "x") is None


def test_rollback_restores_absent_not_none():
    store = Store()
    store.begin()
    store.set("a", 1)
    store.rollback()
    assert "a" not in store
    assert len(store) == 0


def test_delete_of_missing_key_leaves_nothing_behind():
    store = Store({"x": 1})
    store.begin()
    assert store.delete("ghost") is False
    store.rollback()
    assert store.items() == [("x", 1)]
    assert "ghost" not in store


def test_many_writes_to_same_key_restore_original():
    store = Store({"a": "orig"})
    store.begin()
    store.set("a", 1)
    store.set("a", 2)
    store.delete("a")
    store.set("a", 3)
    store.delete("a")
    store.rollback()
    assert store.get("a") == "orig"


def test_inner_commit_keeps_outer_original_for_shared_key():
    store = Store({"a": 0})
    store.begin()
    store.set("a", 1)
    store.begin()
    store.set("a", 2)
    store.commit()
    assert store.get("a") == 2
    store.rollback()
    assert store.get("a") == 0


def test_inner_commit_of_key_untouched_by_outer():
    store = Store()
    store.begin()
    store.begin()
    store.set("k", 1)
    store.commit()
    store.rollback()
    assert "k" not in store


def test_inner_rollback_then_outer_commit():
    store = Store()
    store.begin()
    store.set("a", 1)
    store.begin()
    store.set("a", 2)
    store.set("b", 2)
    store.rollback()
    store.commit()
    assert store.items() == [("a", 1)]
    assert store.depth == 0
    assert _raises(NoActiveTransaction, store.rollback)


def test_three_levels_mixed():
    store = Store({"a": 0})
    store.begin()
    store.set("a", 1)
    store.begin()
    store.set("a", 2)
    store.begin()
    store.delete("a")
    store.rollback()
    assert store.get("a") == 2
    store.rollback()
    assert store.get("a") == 1
    store.rollback()
    assert store.get("a") == 0


def test_deep_nesting_rollback_and_commit():
    depth = 3000
    store = Store()
    for i in range(depth):
        store.begin()
        store.set("k", i)
    assert store.depth == depth
    for i in reversed(range(depth)):
        assert store.get("k") == i
        store.rollback()
    assert "k" not in store and store.depth == 0

    for i in range(depth):
        store.begin()
        store.set("k", i)
    for _ in range(depth):
        store.commit()
    assert store.get("k") == depth - 1 and store.depth == 0
    assert _raises(NoActiveTransaction, store.rollback)


def test_initial_data_is_not_transactional():
    store = Store({"a": 1})
    assert store.depth == 0
    assert _raises(NoActiveTransaction, store.rollback)
    assert store.get("a") == 1


def test_stores_do_not_share_transaction_state():
    first, second = Store(), Store()
    first.begin()
    first.set("a", 1)
    assert first.depth == 1 and second.depth == 0
    second.set("b", 2)
    first.rollback()
    assert second.get("b") == 2
    assert _raises(NoActiveTransaction, second.rollback)


def test_context_manager_nested_failure_only_undoes_inner():
    store = Store()
    with store.transaction():
        store.set("a", 1)
        try:
            with store.transaction():
                store.set("a", 2)
                store.set("b", 3)
                raise ValueError("boom")
        except ValueError:
            pass
        assert store.depth == 1
        assert store.get("a") == 1 and "b" not in store
    assert store.depth == 0 and store.get("a") == 1


def test_context_manager_failure_propagates_through_all_levels():
    store = Store({"a": 0})
    try:
        with store.transaction():
            store.set("a", 1)
            with store.transaction():
                store.set("a", 2)
                raise KeyError("x")
    except KeyError:
        pass
    else:
        assert False, "exception must propagate"
    assert store.get("a") == 0 and store.depth == 0


def test_cli_count_follows_rollback():
    cli = Interpreter()
    replies = cli.run("SET a x\nSET b x\nSET c x\nBEGIN\nDELETE a\nCOUNT x\nROLLBACK\nCOUNT x")
    assert replies == ["OK", "OK", "OK", "OK", "1", "2", "OK", "3"]


def test_cli_values_with_spaces_and_errors():
    cli = Interpreter()
    replies = cli.run(
        "SET greeting hello world\nBEGIN\nSET greeting bye now\nROLLBACK\nGET greeting\nCOMMIT\nbegin extra"
    )
    assert replies == [
        "OK", "OK", "OK", "OK", "hello world",
        "ERROR: no active transaction",
        "ERROR: usage: BEGIN",
    ]


def test_cli_commit_makes_changes_permanent():
    cli = Interpreter()
    replies = cli.run("BEGIN\nSET a 1\nBEGIN\nSET a 2\nCOMMIT\nCOMMIT\nROLLBACK\nGET a")
    assert replies == ["OK", "OK", "OK", "OK", "OK", "OK", "ERROR: no active transaction", "2"]
