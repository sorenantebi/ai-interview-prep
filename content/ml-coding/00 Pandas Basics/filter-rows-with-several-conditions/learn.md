# Learn: Filter Rows with Several Conditions

## The idea

- **DataFrame**: a table of rows and named columns.
- The task: keep only the rows that pass a test, and drop the rest.
- The test has two parts joined by "and".
  - Part 1: `type` must be in an allowed list.
  - Part 2: `level` is above `k`, **or** the row is `featured`.
- **Boolean mask**: a column of `True`/`False` values, one per row. `True` means "keep this row".
- You build small masks, combine them, then use the result to pick rows.
- Where it shows up:
  - Dropping bad samples before training.
  - Selecting a class subset for an evaluation report.
  - Cleaning a feature table.
- **Element-wise**: an operation applied to each row separately, with no loop written by you.
- **Index**: the row label pandas shows on the left (0, 1, 2, ...).
  - Filtering keeps the old labels, so you get gaps like 0, 2.
  - Resetting the index renumbers the rows.

## Work it by hand

Example 1 with `types = ["tool", "gem"]` and `k = 2`.

| row | name | type | level | featured |
|---|---|---|---|---|
| 0 | a | tool | 5 | False |
| 1 | b | gem | 2 | False |
| 2 | c | tool | 1 | True |
| 3 | d | food | 9 | False |

1. Type is in the list? `[True, True, True, False]` (only "food" is not allowed).
2. Level above 2? `[True, False, False, True]` (row 1 has level 2, not above 2).
3. Featured? `[False, False, True, False]`.
4. Level test OR featured, row by row: `[True, False, True, True]`.
5. Step 1 AND step 4, row by row: `[True, False, True, False]`.
6. Keep rows 0 and 2. Their labels are now 0 and 2.
7. Renumber the labels to 0 and 1.

Final result:

```text
name: ["a", "c"]
type: ["tool", "tool"]
level: [5, 1]
featured: [false, true]
```

This matches the expected output.

## Tools you'll need

### Comparison on a column: `df["col"] > value`

- Comparing a column to a number gives a boolean Series, one value per row.

```python
import pandas as pd
df = pd.DataFrame({"score": [3, 8, 5]})
print((df["score"] > 4).tolist())  # [False, True, True]
```

### `Series.isin(values)`

- Gives `True` where the cell equals any value in the list.
- An empty list gives all `False`.

```python
import pandas as pd
s = pd.Series(["red", "blue", "green"])
print(s.isin(["red", "green"]).tolist())  # [True, False, True]
print(s.isin([]).tolist())  # [False, False, False]
```

### `&`, `|` and parentheses

- `&` means and, `|` means or, both element-wise.
- Python's `and`/`or` do **not** work on Series.
- Wrap each comparison in parentheses, because `&` and `|` bind tighter than `>` or `==`.
- A column that is already boolean can go straight into a mask, with no `== True`.

```python
import pandas as pd
df = pd.DataFrame({"a": [1, 6, 9], "b": [True, False, False]})
m = (df["a"] > 5) & (df["a"] < 8)
print(m.tolist())  # [False, True, False]
print((m | df["b"]).tolist())  # [True, True, False]
```

### `df[mask]`

- Indexing with a boolean Series keeps the rows where it is `True`.
- All columns stay, and so do the original labels.

```python
import pandas as pd
df = pd.DataFrame({"x": [10, 20, 30]})
out = df[df["x"] != 20]
print(out.index.tolist())  # [0, 2]
print(out.shape)  # (2, 1)
```

### `reset_index(drop=True)`

- Renumbers the index to 0, 1, 2, ...
- With `drop=True` the old labels are thrown away.
- Without it, the old labels become a new column, which you don't want here.

```python
import pandas as pd
df = pd.DataFrame({"x": [10, 20, 30]}, index=[0, 2, 5])
print(df.reset_index(drop=True).index.tolist())  # [0, 1, 2]
print(df.reset_index().columns.tolist())  # ['index', 'x']
```

## Common mistakes

- **Missing parentheses.** `df["a"] > 1 | df["b"]` is parsed in the wrong order and raises an error.
  - Put each comparison in its own parentheses.
- **Using `and` / `or`.** These raise "truth value of a Series is ambiguous".
  - Use `&` and `|`.
- **Wrong grouping.** The "or" must sit inside its own parentheses.
  - Then "and" joins the type test with the whole "level or featured" part.
- **Forgetting `reset_index(drop=True)`.** The rows look right, but the index has gaps.
  - Without `drop=True` you also get an extra `index` column.
- **Using `>=` instead of `>`.** Row "b" has level 2 with `k = 2` and must be dropped.

## Hints

### Hint 1
- Make one yes/no test for each rule: type, level, featured.
- Join the level and featured tests with "or".
- Join that result with the type test using "and".
- Keep the rows that pass.
- Renumber the index.

### Hint 2
- Type test: `isin` gives a boolean Series with one value per row.
- Level test: a `>` comparison gives another, same length.
- Featured test: use the `featured` column as it is.
- Combine them with `|` and `&` into one mask of the same length.
- Select rows with the mask, then reset the index with `drop=True`.

### Hint 3
- Think of the condition as: type-in-list AND (level-above-k OR featured).
- Write the "level-above-k OR featured" part first, inside its own parentheses.
- Join it to the `isin` result with `&`.
- Empty cases need no extra code: an empty list or no matches gives an all-`False` mask.
  - You then get zero rows with the same columns.
