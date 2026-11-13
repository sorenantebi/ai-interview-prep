# Learn: Filter and Sort Rows

## The idea

- The task has two parts: keep only the rows that pass a score threshold, then put the survivors in a clear order.
  - Highest score comes first.
  - If two scores are equal, the name breaks the tie alphabetically.
- This shows up all the time in data work.
  - Dropping bad or irrelevant rows before training.
  - Building a leaderboard in an evaluation report: rank models by metric, and list them by name when they tie.
- **DataFrame**: a pandas table. Each column has a name and each row has an index label.
- **Boolean mask**: a column of `True`/`False` values, one per row.
  - Using it to select rows keeps only the `True` ones.
- **Index**: the row labels.
  - After filtering and sorting, the old labels stay attached to the rows, so they are no longer `0..n-1`.
  - You need to renumber them.
- **Tie-break**: a second sort key that only matters when the first keys are equal.

## Work it by hand

Start with `min_score = 70`:

| index | name | score |
|---|---|---|
| 0 | ana | 72 |
| 1 | ben | 90 |
| 2 | cy | 65 |
| 3 | dee | 90 |

1. **Build the mask.** Is `score >= 70`?
   - Result: `[True, True, False, True]`
2. **Keep the `True` rows.** `cy` (65) is gone.
   - Three rows remain, with their old labels 0, 1 and 3:

   | index | name | score |
   |---|---|---|
   | 0 | ana | 72 |
   | 1 | ben | 90 |
   | 3 | dee | 90 |

3. **Sort.** Score goes high to low, so the two 90s come before 72.
   - `ben` and `dee` tie on 90, so the name decides: "ben" comes before "dee".

   | index | name | score |
   |---|---|---|
   | 1 | ben | 90 |
   | 3 | dee | 90 |
   | 0 | ana | 72 |

4. **Renumber the index** to `0, 1, 2`:

   | index | name | score |
   |---|---|---|
   | 0 | ben | 90 |
   | 1 | dee | 90 |
   | 2 | ana | 72 |

5. As columns, this is `{"name": ["ben","dee","ana"], "score": [90,90,72]}`, which matches the expected output.
- In Example 2, no score reaches 60, so the mask is all `False`.
  - You get an empty table that still has both columns.

## Tools you'll need

### Boolean mask: `df[condition]`

- Comparing a column to a number gives a column of `True`/`False`.
- Passing it inside `df[...]` keeps only the rows where it is `True`. The original is not changed.

```python
import pandas as pd

t = pd.DataFrame({"city": ["a", "b", "c"], "temp": [5, 20, 12]})
mask = t["temp"] > 10
print(mask.tolist())  # [False, True, True]
print(t[mask])
#   city  temp
# 1    b    20
# 2    c    12
```

### `df.sort_values(by, ascending=...)`

- Sorts rows by one column or a list of columns. With a list, later columns only break ties in earlier ones.
- `ascending` can also be a list, with one `True`/`False` per column.
- It returns a new DataFrame.

```python
import pandas as pd

t = pd.DataFrame({"k": ["x", "y", "z", "w"], "v": [1, 2, 2, 1]})
out = t.sort_values(["v", "k"], ascending=[True, False])
print(out["k"].tolist())  # ['x', 'w', 'z', 'y']
```

- Here `v` goes up, and ties are broken by `k` going down.

### `df.reset_index(drop=True)`

- Replaces the index with `0..n-1`.
- Without `drop=True`, the old index is added as a new column, which breaks the "keep both columns" rule.

```python
import pandas as pd

t = pd.DataFrame({"a": [3, 1, 2]}, index=[7, 8, 9])
print(t.reset_index(drop=True).index.tolist())  # [0, 1, 2]
print(t.reset_index().columns.tolist())  # ['index', 'a']
```

### Empty results

- If the mask is all `False`, you get zero rows and the same columns.
- Later steps like sorting still work on it.

```python
import pandas as pd

t = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
e = t[t["a"] > 100]
print(e.shape)  # (0, 2)
print(e.sort_values("a").shape)  # (0, 2)
```

## Common mistakes

- **Forgetting to renumber.** After filtering and sorting, the index looks like `1, 3, 0`.
  - Finish with `reset_index(drop=True)`.
- **Using `reset_index()` without `drop=True`.** The result gets a third column called `index`.
- **Wrong direction for the tie-break.** Score is descending but name is ascending.
  - Pass a list to `ascending`, one value per sort column, in the same order as the columns.
- **Assuming `sort_values` works in place.** It returns a new DataFrame, so use the returned value.
- **Using `>` instead of `>=`.** "At least `min_score`" means a score equal to the threshold stays.

## Hints

### Hint 1
- Keep only the rows that meet the threshold.
- Sort what is left by score and name, with a different direction for each.
- Renumber the index so it starts at 0 again.

### Hint 2
- Build a boolean mask from the `score` column and use it to select rows. The result is a smaller DataFrame.
- Call `sort_values` with a list of two column names and a list of two booleans. Same rows, new order.
- Finish with `reset_index`. The index becomes `0..n-1`.
- Each step returns a new DataFrame, so `df` stays untouched.

### Hint 3
- The column list for sorting is score first, name second.
- The direction list says "descending" for score and "ascending" for name.
- The first column is the main key. The second only matters when two scores are equal.
- After sorting, call `reset_index` with `drop=True` so the old labels are thrown away instead of becoming a column.
