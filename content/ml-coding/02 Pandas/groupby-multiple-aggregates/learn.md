# Learn: Group By with Several Aggregates

## The idea

- The task: turn a table with one row per game into a short summary with one row per team.
- **Grouping** (`groupby` in pandas) splits the rows into buckets by the value of a column, here `team`.
- An **aggregate** is a function that squeezes many values into one, like `sum`, `mean`, `max` or "count the distinct values".
- **Named aggregation** computes several aggregates in one pass and lets you name each output column.
- **Distinct** means repeats count once: a player who appears in 3 rows is still 1 player.
  - So `players` counts distinct players, but `mean` is over rows, so a repeated player counts each time.
- Where it shows up:
  - per-user features in a feature pipeline,
  - per-class metrics in an evaluation report,
  - per-day statistics in monitoring.
- The **index** is the row label of a DataFrame. After a groupby, the group key becomes the index instead of a normal column.

## Work it by hand

Example 1 input:

| row | team | player | points |
|-----|------|--------|--------|
| 0 | red  | al | 10 |
| 1 | blue | bo | 7 |
| 2 | red  | cy | 4 |
| 3 | red  | al | 6 |

1. **Split into groups**, sorted by team name:
   - blue: row 1, players `bo`, points `7`.
   - red: rows 0, 2, 3, players `al, cy, al`, points `10, 4, 6`.
2. **Compute each statistic per group:**

   | team | players (distinct) | total (sum) | mean | best (max) |
   |------|--------------------|-------------|------|------------|
   | blue | 1 (`bo`) | 7 | 7 / 1 = 7.0 | 7 |
   | red | 2 (`al`, `cy`) | 10+4+6 = 20 | 20 / 3 = 6.66667 | 10 |

3. **Move `team` out of the index** into a normal column, and use the index `0, 1`.
4. **Result**, matching the expected output:

```text
team  players  total  mean      best
blue  1        7      7.00000   7
red   2        20     6.66667   10
```

## Tools you'll need

### df.groupby(col)

- Splits the rows into groups by the values in `col`.
- It shows nothing by itself; you call an aggregation on the result.
- Groups come out sorted by key by default, and the key becomes the index.

```python
import pandas as pd

d = pd.DataFrame({"k": ["b", "a", "b"], "v": [1, 2, 3]})
print(d.groupby("k")["v"].sum())
# k
# a    2
# b    4
# Name: v, dtype: int64
```

### .agg() with named aggregation

- `agg(new_name=(column, function))` computes several statistics at once.
- Each keyword becomes an output column, in the order you write them.
- The function can be a string such as `"sum"`, `"mean"`, `"max"`, `"nunique"`.

```python
import pandas as pd

d = pd.DataFrame({"k": ["b", "a", "b"], "v": [1, 2, 3], "w": [5, 5, 6]})
out = d.groupby("k").agg(lo=("v", "min"), kinds=("w", "nunique"))
print(out)
#    lo  kinds
# k
# a   2      1
# b   1      2
```

### "nunique"

- Counts distinct values in a column. Repeats count once.
- It differs from `len` or `"count"`, which count every row.

```python
import pandas as pd

s = pd.Series(["x", "y", "x", "x"])
print(s.nunique())  # 2
print(len(s))       # 4
```

### .reset_index()

- Moves the index back into a regular column and replaces it with `0..n-1`.
- Use it after `groupby` when the group key should be a column again.

```python
import pandas as pd

d = pd.DataFrame({"k": ["b", "a"], "v": [1, 2]}).groupby("k").sum()
print(d.index.tolist())  # ['a', 'b']
r = d.reset_index()
print(r.columns.tolist())  # ['k', 'v']
print(r.index.tolist())    # [0, 1]
```

## Common mistakes

- **Counting rows instead of distinct players.**
  - `"count"` or `"size"` would give 3 for red, not 2.
  - Use `"nunique"`.
- **Leaving `team` in the index.**
  - After `groupby().agg()` the key is the index, not a column.
  - Call `reset_index()` so `team` is the first column and the index is `0..n-1`.
- **Wrong column names or order.**
  - The output names must be exactly `players`, `total`, `mean`, `best`.
  - With named aggregation, the keyword order is the column order.
- **Averaging over players.**
  - `mean` is over rows, so a player who appears twice counts twice.
  - Don't deduplicate before the mean.
- **Special-casing empty input.**
  - With 0 rows, the result should still have the right columns.
  - Named aggregation handles this on its own, so skip manual loops.

## Hints

### Hint 1
- Group the rows by team.
- For each group, compute four statistics: distinct players, sum of points, mean of points, max of points.
- Turn the team key back into a normal column.

### Hint 2
- Group with `groupby("team")`; the result is one group per team, sorted by name.
- Call `.agg(...)` with named aggregation, each keyword as `name=(column, function)`; you get one row per team with `team` as the index.
- Finish with `reset_index()`; `team` is a column again and the index is `0..n-1`.

### Hint 3
- Write four named pairs inside `agg`.
  - The first uses column `player` with the function `"nunique"`.
  - The other three use column `points` with `"sum"`, `"mean"` and `"max"`.
- Name them `players`, `total`, `mean` and `best`, in that order.
- Groups are already sorted by team name, so no extra sort is needed.
