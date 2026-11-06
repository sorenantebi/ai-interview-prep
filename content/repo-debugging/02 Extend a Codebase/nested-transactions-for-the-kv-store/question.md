---
difficulty: Hard
kind: extend
---
# Nested transactions for the KV store

**Kind:** Extend the codebase · **Difficulty:** Hard

## Scenario
`kvstore` is a small in-memory key-value store with a text command interpreter on top of it (think a toy Redis). Teams use it as a test double for a real database and now want transactions that nest. `BEGIN` can be called while a transaction is already open, and `ROLLBACK` must undo only the innermost open transaction. The store and the interpreter currently have no transaction support: the transaction methods are stubs.

## Your tasks
1. Implement nested transactions on `Store`: `begin()`, `rollback()`, `commit()` and a read-only `depth` property (the number of open transactions, `0` when none).
   - `rollback()` undoes every `set`/`delete` made since the matching `begin()` and closes only that transaction.
   - `commit()` closes the innermost transaction and keeps its changes. If it was nested, the changes become part of the enclosing transaction, so rolling the outer one back undoes them too. Committing the outermost transaction makes the changes permanent.
   - `rollback()` and `commit()` with no open transaction raise `NoActiveTransaction`.
2. Implement `Store.transaction()`, a context manager that begins a transaction, commits when the block finishes normally, and rolls back (re-raising the exception) when the block raises.
3. Expose the feature in the text interpreter with `BEGIN`, `ROLLBACK` and `COMMIT` commands, following the existing command conventions.

## Notes
- Entry points: `kvstore/store.py` (`Store`) and `kvstore/cli.py` (`Interpreter`). Shared helpers and the sentinel for "no value" live in `kvstore/utils.py`; exceptions in `kvstore/errors.py`.
- `None` is a valid stored value, and a key that doesn't exist is not the same thing as a key holding `None`. Rolling back must restore either state exactly.
- Values set through `Store(initial)` are not part of any transaction.
- Interpreter replies: `BEGIN`, `ROLLBACK` and `COMMIT` reply `OK` on success. The interpreter already turns `KVError`s into `ERROR: <message>` replies.
- Nesting can get deep (thousands of levels in some test suites), so don't rely on recursion.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
