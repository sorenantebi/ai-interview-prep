# Learn: Sessionize Events

## The idea

- **Sessionizing** means cutting each user's click log into bursts of activity, called sessions, separated by quiet periods.
  - If a user is quiet for **more than** `gap_minutes`, their next click starts a new session.
  - Every session then gets a number, counting up across the whole result.
- It shows up in feature pipelines and analytics: "sessions per user", "average session length", or grouping clicks before feeding a recommender.
  - Raw logs rarely come pre-grouped, so you build the groups yourself.
- **groupby**: splits rows into one bucket per value of a column (here, per user), then does something inside each bucket.
- **diff**: for each row, its value minus the previous row's value (inside its bucket).
  - A bucket's first row has no previous row, so its result is missing (`NaN`, or `NaT` for times).
- **cumulative sum (cumsum)**: a running total. `[1, 0, 0, 1]` becomes `[1, 1, 1, 2]`.
- **The key trick**: mark rows that *start* a session with 1 and the others with 0, then take a running total.

## Work it by hand

Example 1, `gap_minutes = 30`.

1. **Sort** by user, then time (ties keep the input order).
   - Order: u1 10:00, u1 10:20, u1 11:00, u2 09:00.
2. **Gap to the same user's previous event:**

   | user | ts | gap |
   |---|---|---|
   | u1 | 10:00 | missing (first of u1) |
   | u1 | 10:20 | 20 min |
   | u1 | 11:00 | 40 min |
   | u2 | 09:00 | missing (first of u2) |

3. **Does the row start a session?** Yes if the gap is missing, or the gap is more than 30 minutes (exactly 30 would stay in the session).

   | ts | starts? |
   |---|---|
   | 10:00 | 1 (first) |
   | 10:20 | 0 (20 ≤ 30) |
   | 11:00 | 1 (40 > 30) |
   | 09:00 | 1 (first of u2) |

4. **Running total** of the starts: `1, 1, 2, 3`.
5. **Result:** `user = [u1, u1, u1, u2]`, `ts` = the original strings in sorted order, `session = [1, 1, 2, 3]`.
   - This matches the expected output.
   - The running total never resets between users, which is why ids count up across the whole result.

## Tools you'll need

### pd.to_datetime(series)

- Converts strings like `"2024-01-01 10:00:00"` into real timestamps.
- You need real datetimes to subtract and compare times.

```python
import pandas as pd

s = pd.Series(["2030-05-01 08:00:00", "2030-05-01 08:45:00"])
t = pd.to_datetime(s)
print(t.dtype)  # datetime64[ns]
print(t[1] - t[0])  # 0 days 00:45:00
```

### df.sort_values(by_list)

- Sorts rows by several columns; earlier columns take priority.
- Ties are not guaranteed to keep input order, so add a tiebreaker column (like the original row position) last.
- Index labels travel with their rows.

```python
import pandas as pd

d = pd.DataFrame({"k": ["b", "a", "b"], "v": [2, 9, 1], "pos": [0, 1, 2]})
print(d.sort_values(["k", "v", "pos"])["v"].tolist())  # [9, 1, 2]
```

### groupby(...)[col].diff()

- Difference to the previous row *within each group*.
- The first row of each group gets `NaN` (`NaT` for datetimes); for times the result is a `Timedelta`.

```python
import pandas as pd

d = pd.DataFrame({"g": ["x", "x", "y"], "n": [5, 8, 20]})
print(d.groupby("g")["n"].diff().tolist())  # [nan, 3.0, nan]
```

### Series.isna() and combining masks

- `isna()` is `True` where a value is missing.
- Combine boolean Series with `|` (or) and `&` (and), not `or`/`and`; wrap each comparison in parentheses.

```python
import pandas as pd

x = pd.Series([None, 4.0, 1.0])
print((x.isna() | (x > 3)).tolist())  # [True, True, False]
```

### pd.Timedelta(minutes=...)

- A duration you can compare against a difference of timestamps.

```python
import pandas as pd

gap = pd.Timedelta(minutes=10)
print(pd.Timedelta(minutes=15) > gap)  # True
print(pd.Timedelta(minutes=10) > gap)  # False
```

### Series.cumsum()

- Running total; booleans count as 0 and 1.
- Cast to `int` afterwards if you want integer output.

```python
import pandas as pd

flags = pd.Series([True, False, False, True])
print(flags.cumsum().tolist())  # [1, 1, 1, 2]
```

### reset_index(drop=True)

- Replaces the index with `0..n-1` and discards the old one.
- Needed because sorting shuffles the index labels.

```python
import pandas as pd

d = pd.DataFrame({"a": [3, 1, 2]}).sort_values("a")
print(d.index.tolist())  # [1, 2, 0]
print(d.reset_index(drop=True).index.tolist())  # [0, 1, 2]
```

## Common mistakes

- **Using `>=` instead of `>`.**
  - A gap of exactly `gap_minutes` stays in the same session; only strictly larger starts a new one.
- **Forgetting each user's first event.**
  - Its diff is `NaT`, and `NaT > something` is `False`, so users would merge into one session.
  - Add `isna()` explicitly.
- **Diffing without `groupby`.**
  - A plain `diff()` compares u1's last event with u2's first, which is meaningless.
- **Losing tie order.**
  - Same user and same time must keep their input order.
  - Record the original position before sorting and use it as the last sort key.
- **Returning the wrong columns or index.**
  - Return `ts` as the original strings, drop helper columns, and reset the index.
  - Make sure an empty DataFrame doesn't crash.

## Hints

### Hint 1
- Put the events in the required order: user, time, original position.
- For each row, find how long it has been since the same user's previous event.
- A row starts a session if it is the user's first row or the wait is longer than the gap.
- Number the sessions by counting starts as you go down the table.

### Hint 2
- Parse `ts` with `pd.to_datetime` into a helper column, and save row positions in another; the table is now the same length with two extra columns.
- Sort on user, time, position with `sort_values`; same rows, new order.
- `groupby("user")[time_col].diff()` gives a Timedelta Series, same length, with `NaT` at each user's first row.
- Build a boolean Series from `isna()` and a comparison with `pd.Timedelta`, then apply `cumsum()` to get one integer per row.

### Hint 3
- For each row, `start = 1` if the gap is missing or the gap is greater than `gap_minutes` minutes; otherwise `start = 0`.
- A row's session id is the sum of `start` over all rows from the top of the sorted table down to and including that row.
- This sum runs over the whole table and is never reset per user.
- Finally, keep only `user`, the original `ts`, and `session` (as integers), and reset the index.
