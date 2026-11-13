# Learn: Deduplicate, Keeping the Latest Row

## The idea

- The task: for each `user_id`, keep exactly one row, the one with the latest `updated_at`.
- If two rows of a user share that latest time, the one that appears later in `df` wins.
- Then sort by `user_id`, use a fresh `0..n-1` index, and leave `updated_at` as a string.
- **Deduplication** means collapsing many rows that share a key (here `user_id`) into one.
- It shows up constantly in data work:
  - Event logs and change-data-capture feeds hold many versions of the same entity.
  - Before building features or evaluating a model, you need a clean "current state" with one row per entity.
  - Without it, duplicates leak into training data or get double-counted in reports.
- **DataFrame**: a table with named columns.
- **Index**: the row labels on the left, 0, 1, 2, ... by default.
- **Tie-break**: an extra sort column that decides the order when the first column is equal.
- The timestamps are text like `"YYYY-MM-DD HH:MM:SS"`.
  - This format sorts correctly even as plain text.
  - Converting to real datetimes is the safer habit.
  - The output must still keep `updated_at` as a string.

## Work it by hand

Example 1 has three rows:

| position | user_id | updated_at | email |
|---|---|---|---|
| 0 | 1 | 2024-03-01 10:00:00 | a@new |
| 1 | 2 | 2024-01-05 09:00:00 | b@x |
| 2 | 1 | 2024-02-01 08:00:00 | a@old |

1. **Order the rows.** Sort by `user_id`, then time (oldest first), then original position:

| user_id | updated_at | email |
|---|---|---|
| 1 | 2024-02-01 08:00:00 | a@old |
| 1 | 2024-03-01 10:00:00 | a@new |
| 2 | 2024-01-05 09:00:00 | b@x |

2. **Keep the last row of each user.**
   - User 1's last row is `a@new`, because March beats February.
   - User 2 has one row, so it stays.
3. **Tidy up.**
   - The rows are already in `user_id` order, since it was the first sort key.
   - Reset the index to `0, 1`.

| user_id | updated_at | email |
|---|---|---|
| 1 | 2024-03-01 10:00:00 | a@new |
| 2 | 2024-01-05 09:00:00 | b@x |

4. This matches the expected output.
5. Example 2 shows why the position tie-break matters:
   - Both rows of user 7 have the same time.
   - After sorting by position, `"first"` (0) comes before `"second"` (1).
   - Keeping the last row gives `"second"`.

## Tools you'll need

### df.sort_values(by, ascending=True)

- Sorts rows by one column or a list of columns.
- With a list, later columns only break ties in earlier ones.
- It returns a new DataFrame and keeps the old index labels.

```python
import pandas as pd

d = pd.DataFrame({"k": ["b", "a", "b"], "v": [2, 9, 1]})
print(d.sort_values(["k", "v"]))
#    k  v
# 1  a  9
# 2  b  1
# 0  b  2
```

### df.drop_duplicates(subset, keep)

- Drops rows that repeat a value in the `subset` columns.
- `keep="first"` (default) keeps the first occurrence; `keep="last"` keeps the last.
- Which one is "first" or "last" depends on the current row order.

```python
import pandas as pd

d = pd.DataFrame({"k": ["a", "a", "b"], "v": [1, 2, 3]})
print(d.drop_duplicates("k", keep="last"))
#    k  v
# 1  a  2
# 2  b  3
```

### pd.to_datetime(series)

- Converts text dates into real datetime values that sort and compare by time.

```python
import pandas as pd

s = pd.Series(["2023-05-02 08:00:00", "2023-05-01 23:00:00"])
t = pd.to_datetime(s)
print(t[0] > t[1])  # True
```

### df.assign(name=values)

- Returns a copy with an extra column; the original is not modified.
- Handy for temporary helper columns.

```python
import pandas as pd

d = pd.DataFrame({"x": [10, 20]})
print(d.assign(pos=range(len(d))))
#     x  pos
# 0  10    0
# 1  20    1
print(list(d.columns))  # ['x']
```

### df.drop(columns=[...]) and df.reset_index(drop=True)

- `drop(columns=...)` removes columns.
- `reset_index(drop=True)` replaces the index with `0..n-1` and discards the old labels.
- Without `drop=True`, the old index becomes a new column.

```python
import pandas as pd

d = pd.DataFrame({"a": [1, 2, 3], "tmp": [0, 0, 0]}, index=[5, 3, 4])
out = d.drop(columns=["tmp"]).reset_index(drop=True)
print(out)
#    a
# 0  1
# 1  2
# 2  3
```

## Common mistakes

- **Calling `drop_duplicates` before sorting.**
  - It keeps rows by their current order, so unsorted data gives an arbitrary winner.
  - Sort first.
- **Forgetting the tie-break.**
  - Sorting only by time leaves equal-time rows in an unreliable order.
  - Add the original row position as the last sort key.
- **Leaving helper columns in the output.**
  - The result must have exactly `user_id`, `updated_at`, `email`, with `updated_at` still a string.
  - Drop any helpers you added.
- **Forgetting `reset_index(drop=True)`.**
  - After sorting and dropping rows, the index is scrambled.
  - The expected output has `0..n-1`.
- **Empty input.**
  - `len(df)` can be 0.
  - Check that your steps still work and return the same columns.

## Hints

### Hint 1

- Put each user's rows in order from oldest to newest, with the original row position breaking ties.
- Keep only the last row of each user.
- Remove any helper columns you added.
- Renumber the index.

### Hint 2

- Add a real datetime column and a position column (`assign`, `pd.to_datetime`, `range`); the table now has two extra columns.
- Sort by user, datetime, position with `sort_values` and a list; same rows, new order.
- Call `drop_duplicates` on `user_id` with `keep="last"`; now one row per user.
- Finish with `drop(columns=...)` and `reset_index(drop=True)`.

### Hint 3

- The sort key is the triple (user_id, parsed time, original position), all ascending.
- Within one user, the newest row sits at the bottom of that user's group.
- Among equal times, the row that came latest in the input sits lowest, because of the position column.
- `keep="last"` keeps exactly that bottom row.
- Because `user_id` is the first sort key, the surviving rows are already in `user_id` order, so only the index reset is left.
