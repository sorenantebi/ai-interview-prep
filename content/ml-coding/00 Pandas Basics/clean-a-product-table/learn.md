# Learn: Clean a Product Table

## The idea

- The task is to **tidy a table**: remove one column, remove rows that miss important values, and renumber the rows from 0.
- Nothing is calculated. You only choose what to keep.
- This is the first step of most ML and data pipelines.
  - Models can't train on missing values, so incomplete rows are dropped or fixed before features are built.
  - Only the columns that matter should force a row out. A missing note shouldn't cost you a good row.
- **DataFrame**: a table with labelled columns.
- **Index**: the row labels on the left (0, 1, 2, ... by default).
  - After rows are deleted, the remaining labels keep their old numbers, so gaps appear.
- **NaN**: the "not a number" marker for a missing value (`None` is treated the same way).
- **Subset**: the list of columns you check for missing values, ignoring all others.

## Work it by hand

Example 1: `drop_col = "note"`, `required = ["price"]`.

Start (4 rows, 4 columns):

| index | id | price | stock | note |
|---|---|---|---|---|
| 0 | 1 | 9.5 | 5 | a |
| 1 | 2 | NaN | 2 | b |
| 2 | 3 | 3.0 | NaN | c |
| 3 | 4 | 7.25 | 1 | d |

1. **Remove the column `note`.** Shape goes from (4, 4) to (4, 3). Columns left: `id`, `price`, `stock`.
2. **Remove rows with a missing `price`.** Only `price` is checked.
   - Row 1 has NaN in `price`, so it goes.
   - Row 2 has NaN in `stock`, but `stock` is not required, so it stays.
   - Shape is now (3, 3) and the index is 0, 2, 3 (a gap).

   | index | id | price | stock |
   |---|---|---|---|
   | 0 | 1 | 9.5 | 5 |
   | 2 | 3 | 3.0 | NaN |
   | 3 | 4 | 7.25 | 1 |

3. **Reset the index** to 0, 1, 2 and throw the old labels away.

   | index | id | price | stock |
   |---|---|---|---|
   | 0 | 1 | 9.5 | 5 |
   | 1 | 3 | 3.0 | NaN |
   | 2 | 4 | 7.25 | 1 |

4. **Read off the result:** `id = [1, 3, 4]`, `price = [9.5, 3.0, 7.25]`, `stock = [5.0, NaN, 1.0]`.
   - This matches the expected output.
   - `stock` shows floats (5.0, 1.0) because a column holding NaN is stored as floats.

## Tools you'll need

### df.drop(columns=...)

- Returns a **new** DataFrame without the named column(s).
- Pass one name or a list of names. The original is unchanged.

```python
import pandas as pd

d = pd.DataFrame({"x": [1, 2], "y": [3, 4], "z": [5, 6]})
out = d.drop(columns="y")
print(list(out.columns))  # ['x', 'z']
print(list(d.columns))    # ['x', 'y', 'z']
```

### df.dropna(subset=...)

- Removes rows that contain missing values and returns a new DataFrame.
- Without `subset`, every column is checked.
- With `subset=[...]`, only the listed columns are checked.
- By default (`how="any"`), a row is removed if **any** checked column is missing.

```python
import pandas as pd
import numpy as np

d = pd.DataFrame({"p": [1.0, np.nan, 3.0], "q": [np.nan, 5.0, 6.0]})
print(len(d.dropna()))                        # 1
print(len(d.dropna(subset=["p"])))            # 2
print(d.dropna(subset=["p"]).index.tolist())  # [0, 2]
```

### df.reset_index(drop=True)

- Renumbers the index as 0, 1, 2, ...
- With `drop=True` the old index is discarded.
- Without it, the old index becomes an extra column, which you don't want here.

```python
import pandas as pd

d = pd.DataFrame({"v": [10, 20, 30]}, index=[4, 7, 9])
print(d.reset_index(drop=True).index.tolist())  # [0, 1, 2]
print(list(d.reset_index().columns))            # ['index', 'v']
```

### Method chaining

- Each method returns a DataFrame, so you can call the next method on the result with a dot.

```python
import pandas as pd

d = pd.DataFrame({"a": [3, 1, 2]})
print(d.sort_values("a").head(2).shape)  # (2, 1)
```

## Common mistakes

- **Calling `dropna()` without `subset`.**
  - It removes rows with a missing value in *any* column, including columns that may be missing.
  - In Example 1 that would wrongly delete the row with the missing `stock`.
- **Forgetting `drop=True` in `reset_index`.**
  - The old index becomes an extra column named `index`, and the output no longer matches.
- **Modifying the input.**
  - Don't use `inplace=True` on `df`.
  - The default methods return new DataFrames, so just use their results.
- **Rebuilding the table by hand.**
  - `drop(columns=...)` keeps the remaining column order. Selecting columns yourself risks reordering them.
- **Writing a loop.**
  - Looping over rows is slow and unnecessary. Three method calls are enough.

## Hints

### Hint 1
- Remove the unwanted column.
- Remove the rows that miss a required value.
- Renumber the rows.
- Each step works on the result of the previous one.

### Hint 2
- Step 1: `drop` with its `columns` argument. Columns shrink by one; rows stay the same.
- Step 2: `dropna` with its `subset` argument. Rows shrink; columns stay the same.
- Step 3: `reset_index`. Shape is unchanged, only the index labels change.
- All three can be chained.

### Hint 3
- For step 2, give `dropna` the list `required` as its `subset`.
  - It then checks only those columns and removes a row if at least one of them is missing.
- For step 3, tell `reset_index` to discard the old index instead of saving it as a column.
- Return the final chained result without touching `df` itself.
