# Learn: Rolling 7-Day Average

## The idea

- The task: for each day, average the sales from that day and the 6 days before it.
- **Rolling average** (moving average): an average over a window that slides forward row by row. It smooths out noisy single days.
- "7 days" means 7 *calendar days*, not 7 *rows*.
  - If days are missing, a window of 7 rows would reach back further than a week.
  - So the window must be defined by time.
- Only rows that exist are averaged. A missing day is skipped, not counted as 0.
- Where it shows up:
  - Feature pipelines, e.g. an "average sales over the last week" feature for a forecasting model.
  - Reports that show trends instead of raw spikes.
- **Datetime column**: stores real dates instead of text, so pandas can do date arithmetic on it.
- **Time-based window**: a rolling window whose size is a span of time, like `"7D"` for 7 days.

## Work it by hand

Example 1 input, unsorted:

```text
date        sales
2024-01-03  30.0
2024-01-01  10.0
2024-01-02  20.0
```

1. Sort by date (oldest first):

```text
date        sales
2024-01-01  10.0
2024-01-02  20.0
2024-01-03  30.0
```

2. For each row, collect the sales from the 7 days ending on that date, then average them:

| date | window (7 days ending here) | sales in window | mean |
|---|---|---|---|
| 2024-01-01 | Dec 26 – Jan 1 | 10 | 10 / 1 = 10.0 |
| 2024-01-02 | Dec 27 – Jan 2 | 10, 20 | 30 / 2 = 15.0 |
| 2024-01-03 | Dec 28 – Jan 3 | 10, 20, 30 | 60 / 3 = 20.0 |

3. Days before Jan 1 aren't in the data, so they add nothing.
4. Keep `date`, `sales`, `avg_7d` and reset the index to 0, 1, 2:

```text
date        sales  avg_7d
2024-01-01  10.0   10.0
2024-01-02  20.0   15.0
2024-01-03  30.0   20.0
```

## Tools you'll need

### pd.to_datetime(series)

- Converts a column of date strings into real datetimes.
- ISO strings like `"2024-05-01"` parse with no extra arguments.
- Plain strings can't be used for time-based windows, so convert first.

```python
import pandas as pd

s = pd.Series(["2024-05-02", "2024-05-01"])
t = pd.to_datetime(s)
print(t.dtype)  # datetime64[ns]
print(t.min())  # 2024-05-01 00:00:00
```

### df.assign(name=values)

- Returns a *copy* of the DataFrame with a new column added.
- Your original `df` is untouched.

```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2]})
df2 = df.assign(b=df["a"] * 10)
print(list(df.columns))   # ['a']
print(list(df2.columns))  # ['a', 'b']
```

### df.sort_values(by)

- Sorts rows by a column.
- Row labels travel with the rows, so the index looks shuffled afterwards.

```python
import pandas as pd

df = pd.DataFrame({"k": [3, 1, 2], "v": ["c", "a", "b"]})
out = df.sort_values("k")
print(out.index.tolist())  # [1, 2, 0]
print(out["v"].tolist())   # ['a', 'b', 'c']
```

### df.rolling(window, on=col)

- Creates a rolling window object; call an aggregation such as `.mean()` on a column of it.
- An integer window looks back that many *rows*.
- A string like `"3D"` looks back that much *time*, covering `(t - 3 days, t]`: the current day plus the 2 before.
- For a time window, `on=` names the datetime column, which must be sorted.

```python
import pandas as pd

d = pd.DataFrame({
    "t": pd.to_datetime(["2024-03-01", "2024-03-02", "2024-03-05"]),
    "x": [1.0, 3.0, 8.0],
})
print(d.rolling("3D", on="t")["x"].mean().tolist())  # [1.0, 2.0, 8.0]
print(d.rolling(2, on="t")["x"].mean().tolist())     # [nan, 2.0, 5.5]
```

- The row-based window (`2`) averages the last two *rows*, ignoring the date gap.
- The time-based window (`"3D"`) sees that Mar 5 has no neighbours within 3 days.

### df.reset_index(drop=True)

- Replaces the index with a fresh `0..n-1`.
- `drop=True` throws the old index away instead of keeping it as a column.

```python
import pandas as pd

df = pd.DataFrame({"v": [5, 6]}, index=[7, 3])
print(df.reset_index(drop=True).index.tolist())  # [0, 1]
```

### df[["a", "b"]] (select columns with a list)

- Returns a DataFrame with just those columns, in that order.
- This is how you drop a helper column.

```python
import pandas as pd

df = pd.DataFrame({"a": [1], "b": [2], "tmp": [3]})
print(list(df[["b", "a"]].columns))  # ['b', 'a']
```

## Common mistakes

- **Using an integer window.** `rolling(7)` means 7 *rows*, which is wrong when days are missing. Use a time string like `"7D"`.
- **Rolling on strings or an unsorted column.** A time window needs a sorted datetime column. Convert with `pd.to_datetime` and sort first.
- **Off-by-one on the window size.** "7 days including today" is today plus 6 earlier days, and `"7D"` already means exactly that. Don't use `"6D"` or `"8D"`.
- **Losing the original date strings.** The output needs `date` as the original strings. Keep the datetime in a separate helper column and drop it in the final column selection.
- **Forgetting the index reset.** After sorting, the index is shuffled. Use `reset_index(drop=True)` for a clean `0..n-1` index with no extra `index` column.

## Hints

### Hint 1

- Make a real datetime version of the date strings.
- Sort the rows by it.
- Compute a mean over a window that spans 7 days of time, not a count of rows.
- Pick the three output columns.
- Reset the index.

### Hint 2

- Convert `date` with `pd.to_datetime` into a helper column (via `assign`), then sort by that helper. The frame stays the same shape, in date order.
- Call `rolling` with a time-string window and `on=` set to the helper column, select `sales`, then take the mean. The result is one value per row.
- Store it as the new column `avg_7d`.
- Select `date`, `sales`, `avg_7d` and reset the index.

### Hint 3

- The window string for "the date and the 6 days before it" is `"7D"`.
  - Pandas covers the span (t minus 7 days, t], which includes day t and goes back through t minus 6 days.
- Because `on=` points at the datetime helper, the span uses real dates, and missing days simply have no rows to add.
- The mean comes back aligned row by row, so assign it directly to a new `avg_7d` column on the sorted frame.
- Finish by selecting `date`, `sales`, `avg_7d` and resetting the index with `drop=True`.
