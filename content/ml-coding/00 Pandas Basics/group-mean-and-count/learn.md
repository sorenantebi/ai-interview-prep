# Learn: Group Mean and Count

## The idea

- The task: for each distinct label in `key`, report the average of `value` and the number of rows.
- The result is a small table with one row per label and two columns, `"mean"` and `"count"`.
- This "split, summarise, combine" pattern is everywhere in data work.
  - Feature pipeline: average spend per customer segment.
  - Evaluation report: accuracy per class.
- **groupby** sorts rows into buckets, one bucket per distinct label. You then ask for one summary per bucket.
- **Series**: a single labelled column.
- **DataFrame**: a table of several columns.
- **Index**: the labels on the rows. Here the group labels become the index.

## Work it by hand

Example 1: `team = [a, b, a, b, a]`, `score = [1.0, 2.0, 3.0, 6.0, 5.0]`.

1. Pair each row with its label:

| row | team | score |
|---|---|---|
| 0 | a | 1.0 |
| 1 | b | 2.0 |
| 2 | a | 3.0 |
| 3 | b | 6.0 |
| 4 | a | 5.0 |

2. Split into buckets, ordered by label:
   - `a` gets scores 1.0, 3.0, 5.0.
   - `b` gets scores 2.0, 6.0.
3. Mean per bucket: `a` is (1+3+5)/3 = 3.0 and `b` is (2+6)/2 = 4.0. This is a Series of length 2.
4. Row count per bucket: `a` has 3 rows and `b` has 2. This is also a Series of length 2, with the same index.
5. Put the two Series side by side, with the labels as the index:

| team | mean | count |
|---|---|---|
| a | 3.0 | 3 |
| b | 4.0 | 2 |

6. The final shape is (2, 2). As a dict, it is `{"mean":{"a":3.0,"b":4.0},"count":{"a":3,"b":2}}`, which is the expected output.

## Tools you'll need

### df.groupby(col)

- Splits the rows by the values in `col`.
- It returns a grouped object, not a table. Nothing is computed until you ask for a summary.
- By default the groups are sorted by label, and the label becomes the index of the result.

```python
import pandas as pd

df = pd.DataFrame({"fruit": ["pear", "fig", "pear"], "kg": [1.0, 4.0, 3.0]})
g = df.groupby("fruit")
print(g.ngroups)  # 2
print(list(g.groups))  # ['fig', 'pear']
```

### grouped[column]

- Picking a column from the grouped object limits the summary to that column.
- The result is a Series rather than a table.

```python
import pandas as pd

df = pd.DataFrame({"fruit": ["pear", "fig", "pear"], "kg": [1.0, 4.0, 3.0]})
col = df.groupby("fruit")["kg"]
print(col.max())
# fruit
# fig     4.0
# pear    3.0
# Name: kg, dtype: float64
```

### .mean()

- Averages the numbers in each group.
- The result is a Series indexed by the group label.

```python
import pandas as pd

df = pd.DataFrame({"k": [2, 1, 2, 1], "x": [10.0, 0.0, 20.0, 4.0]})
m = df.groupby("k")["x"].mean()
print(m.tolist())  # [2.0, 15.0]
print(m.index.tolist())  # [1, 2]
```

### .size()

- Counts the rows in each group, whatever the values are.
- It returns a Series of integers with the same sorted index.

```python
import pandas as pd

df = pd.DataFrame({"k": ["u", "v", "u", "u"], "x": [1.0, 2.0, 3.0, 4.0]})
s = df.groupby("k")["x"].size()
print(s.tolist())  # [3, 1]
print(s.shape)  # (2,)
```

### .count() (the look-alike)

- Counts only the non-missing values, so it can differ from `.size()`.
- Here it is not the right tool, but it is easy to confuse with `.size()`.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"k": ["a", "a", "b"], "x": [1.0, np.nan, 2.0]})
g = df.groupby("k")["x"]
print(g.size().tolist())  # [2, 1]
print(g.count().tolist())  # [1, 1]
```

### pd.DataFrame({name: series, ...})

- Builds a table from a dict. Each key becomes a column name and each Series becomes that column.
- Rows are matched by index label.
- Column order follows the dict order.

```python
import pandas as pd

a = pd.Series([1.5, 2.5], index=["p", "q"])
b = pd.Series([7, 8], index=["p", "q"])
t = pd.DataFrame({"first": a, "second": b})
print(t.columns.tolist())  # ['first', 'second']
print(t.shape)  # (2, 2)
```

## Common mistakes

- **Using `.count()` instead of `.size()`.**
  - `.count()` skips missing values, and on a whole grouped table it returns one column per input column.
  - Use `.size()`, as the problem says.
- **Summarising the whole grouped table.**
  - Without picking the `value` column, pandas tries to average the other columns too, which can fail on text or add extra columns.
  - Select the `value` column first.
- **Wrong column names or order.**
  - The output needs exactly `"mean"` then `"count"`.
  - The dict order you pass to `pd.DataFrame` sets the column order.
- **Turning the label into a normal column.**
  - The label must stay as the index.
  - Don't call `reset_index()` or pass `as_index=False`.
- **Looping over rows or groups.**
  - The task forbids it, and it is slow for 10^5 rows.
  - Let `groupby` do the work.

## Hints

### Hint 1

- Split the rows by the `key` column.
- For each group, compute two summaries of the `value` column: the average and the row count.
- Put the two summaries next to each other in one table with the right column names.

### Hint 2

- Group by `key`, then pick the `value` column from the grouped object.
- Call `.mean()` on it: you get a Series with one entry per group.
- Call `.size()` on it: you get another Series with the same length and index.
- Combine the two Series with `pd.DataFrame` and a dict.

### Hint 3

- Build the grouped column once and reuse it for both summaries.
- Both Series share the same sorted group labels as their index, so pandas lines them up automatically.
- Pass a dict whose first key is `"mean"` and second key is `"count"`, each pointing at its Series.
- The index is already named `key` and sorted ascending, so nothing more is needed.
