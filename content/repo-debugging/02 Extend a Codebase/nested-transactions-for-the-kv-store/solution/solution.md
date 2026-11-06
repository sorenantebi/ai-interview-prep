# Nested transactions for the KV store - Solution

## Root causes / approach
This is a feature task, so there are no bugs. The design uses an **undo log per transaction**, kept on a stack, rather than copying the dict.

**`kvstore/store.py`**
- `self._undo_stack` is a list of dicts, one per open transaction (innermost last). Each dict maps `key -> value before the transaction first touched it`. The `MISSING` sentinel from `utils.py` marks "the key did not exist", which is why a stored `None` and an absent key restore correctly.
- `_record(key)` is called from `set` and `delete` before the raw write (`_put`/`_drop`). It only writes into the innermost log if the key isn't already there, so the log keeps the *first* original value even after many writes to the same key. `delete` of a missing key returns early and records nothing.
- `begin()` pushes `{}`. `rollback()` pops the log and replays it with `_put`/`_drop`, which bypass journaling. Replaying into the raw helpers matters: going through `set` would record the restoration into the parent's log. `commit()` pops the log and, if there is a parent, merges with `parent.setdefault(key, old)`. `setdefault` is essential. If the parent already recorded the key, its value is the older original and must win. If it hasn't, the child's original becomes the parent's original, so an outer rollback also undoes the committed inner changes. Committing the outermost transaction just discards its log.
- `depth` is `len(self._undo_stack)`. Both `commit` and `rollback` raise `NoActiveTransaction` when the stack is empty.
- `transaction()` is a `@contextmanager`: `begin`, `yield`, `commit` on success, `rollback` and re-raise on any exception. Because each level uses its own begin/rollback, a failure in an inner `with` only undoes that level, and an exception that propagates further undoes the outer levels as it passes them.
- `Store(initial)` sets up `_undo_stack` before loading the initial values, and since the stack is empty at that point nothing is journaled. The stack is an instance attribute, not a class attribute, so stores don't share transaction state.

**`kvstore/cli.py`**
- Three new handlers in the existing `_handlers` dispatch table, with the same `_expect` argument checks as the other commands. Each replies `OK`, and `NoActiveTransaction` is already converted to `ERROR: no active transaction` by `execute`.

**Complexity:** `begin` is O(1). `set`/`delete` are O(1). `rollback` and `commit` are O(k) in the number of distinct keys touched in that transaction, independent of store size and nesting depth. No recursion is used, so thousands of nested levels are fine. Copying the dict on `begin` would cost O(n) time and memory per level.

## How to find it
- Read `tests/test_store.py` first. `test_rollback_restores_overwritten_deleted_and_new_keys` and `test_inner_commit_then_outer_rollback_undoes_everything` define the semantics. The failures all show `NotImplementedError` from the stubs in `Store`.
- Note how `set`/`delete` already funnel into `_put`/`_drop`, and that `utils.MISSING` exists. Both are hints about where to hook in and how to represent "absent".
- In `cli.py`, look at how the existing commands are registered and how errors are formatted, then follow the same pattern.
- Before finishing, check the tricky cases yourself: a key holding `None`, deleting a key that doesn't exist, the same key written at two nesting levels followed by inner commit and outer rollback, and a nested `with store.transaction()` block that raises.
