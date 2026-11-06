# Todo priorities and multi-tag filtering - Solution

## Root causes / approach
This is a feature extension, so there is no bug. The work is to thread one new field through the existing layers and add two pure helpers that follow the style of `queries.py`.

**`todolist/models.py`**
- Add `class Priority(IntEnum)` with `HIGH = 1`, `MEDIUM = 2`, `LOW = 3`. Using an `IntEnum` with the most urgent member holding the smallest value means the enum itself can be a sort key, and `HIGH < LOW` holds.
- Add `priority: Priority = Priority.MEDIUM` as the last `Todo` field. It goes last and has a default, so existing positional constructions and the dataclass field ordering stay valid.
- `to_dict` writes `self.priority.name`, which keeps the JSON human-readable and independent of the numeric values.
- `from_dict` reads `data.get("priority", "MEDIUM")` and looks it up with `Priority[...]`. The default is what keeps data saved before this change loadable.

**`todolist/storage.py`**
- `TodoStore.add` gets `priority: Priority = Priority.MEDIUM` and passes it to `Todo`. `dumps`/`loads` need no change because they already go through `to_dict`/`from_dict`; this is why the round-trip tests pass once the model is updated.

**`todolist/queries.py`**
- `sorted_by_priority` is a single `sorted` call with the key `(t.priority, t.due is None, t.due or date.max)`. This mirrors `sorted_by_due`, so undated todos go last within each priority. Python's `sorted` is stable, so ties keep input order. Pitfalls: `reverse=True` would also reverse tied items and break stability, and sorting by due and then by priority in two passes only works if the passes run in that order (the second sort must be the primary key).
- `filter_by_tags` normalises the wanted tags with the existing `normalize_tags`, so case and whitespace are handled exactly as in `by_tag`. It uses frozenset operations: `wanted <= t.tags` for all-of, `wanted & t.tags` for any-of. Edge cases handled: validate `mode` first (so an empty tag list still raises for a bad mode), treat a bare `str` as one tag (otherwise it would be split into characters), and return `list(todos)` when nothing is selected, so the result is always a new list.

Complexity: sorting is O(n log n); filtering is O(n * k) for k requested tags.

## How to find it
1. Run the tests. All failures are in `tests/test_priority_and_tags.py`, and they fail with `AttributeError` (`models.Priority`, `queries.filter_by_tags`) or `TypeError` (`add(..., priority=...)`). That list is effectively the to-do list.
2. Read `models.py` first, since everything else depends on the `Todo` shape. Notice that `to_dict`/`from_dict` define persistence, so changing them covers `TodoStore.dumps`/`loads` for free.
3. Read `queries.py` for the conventions to copy: pure functions that return new lists, tag matching through `utils.normalize_tag(s)`, and the `(t.due is None, ...)` idiom for pushing undated items last.
4. Before finishing, check the points the visible tests don't cover: loading JSON that has no `priority` key, an empty tag list, a bare string for `tags`, an invalid `mode`, and that the input list is not mutated.
