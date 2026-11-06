---
difficulty: Medium
kind: extend
---
# Todo priorities and multi-tag filtering

**Kind:** Extend the codebase · **Difficulty:** Medium

## Scenario
`todolist` is a small library behind our team's task board. It has a `Todo` model, an in-memory `TodoStore` with JSON persistence, and a few query helpers. Product wants two things: every todo gets a priority (high, medium or low) so the board can show the most urgent work first, and the board needs to filter by several tags at once instead of one. The existing behaviour works and its tests pass; the new tests in `tests/test_priority_and_tags.py` fail until the features are built.

## Your tasks
1. **Priorities.** Add a `Priority` enum to `todolist/models.py` with members `HIGH`, `MEDIUM` and `LOW`, where `HIGH` compares as the most urgent (it must sort first when sorted by the enum itself). Give `Todo` a `priority` field that defaults to `Priority.MEDIUM`. Make `TodoStore.add` accept an optional `priority` argument, and make sure the priority survives `to_dict`/`from_dict` and `TodoStore.dumps`/`loads`.
2. **Sorting.** Add `sorted_by_priority(todos)` to `todolist/queries.py`. It returns a new list ordered by priority (high first), then by due date (earliest first, todos without a due date last). The sort must be stable: todos that tie on both keys keep their original relative order.
3. **Tag filtering.** Add `filter_by_tags(todos, tags, mode="all")` to `todolist/queries.py`. With `mode="all"` a todo matches only if it has every given tag; with `mode="any"` it matches if it has at least one. Match the way the existing tag helpers do. Keep the input order, and raise `ValueError` for an unknown mode.

## Notes
- Entry points: `todolist/models.py` (`Todo`), `todolist/storage.py` (`TodoStore`), `todolist/queries.py` (pure functions over lists of todos), `todolist/utils.py` (tag normalisation).
- Data saved before this change has no priority. Loading it must still work and give those todos `Priority.MEDIUM`. In dicts and JSON the priority is stored by member name, e.g. `"HIGH"`.
- For `filter_by_tags`: a bare string passed as `tags` counts as a single tag, blank entries are ignored, and an empty set of tags means "no filtering" (return all todos, as a new list, in either mode).
- None of the query helpers should mutate their input.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
