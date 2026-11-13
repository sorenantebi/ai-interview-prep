# Learn: Add a Ratio Column

## The idea

- The task: add a new column `ctr` equal to `clicks / views`, the share of views that led to a click.
- Rows where `views` is 0 have no defined rate, so they must hold `NaN` instead of `inf`.
- Return a new table and leave the input `df` unchanged.
- Rates like this appear in feature pipelines and evaluation reports (CTR, conversion rate, error rate).
- **Why not `inf`?**
  - Pandas gives `inf` for `5 / 0` and `NaN` for `0 / 0`.
  - An `inf` can wreck averages and break models, so we want a clean missing value.
- **NaN**: "not a number", pandas' marker for missing data.
  - Any arithmetic with NaN gives NaN, so it spreads instead of producing `inf`.
- **DataFrame**: a table. Each column is a **Series** (a labelled 1-D array).
- **Vectorised**: applied to a whole column at once, with no Python loop.
- **Copy**: a separate table. Changing the copy does not change the original.

## Work it by hand

Example 1: `clicks = [3, 0, 5]`, `views = [10, 4, 0]`.

| row | clicks | views | views == 0? | clicks / views | ctr |
|-----|--------|-------|-------------|----------------|-----|
| 0 | 3 | 10 | no | 3 / 10 | 0.3 |
| 1 | 0 | 4 | no | 0 / 4 | 0.0 |
| 2 | 5 | 0 | yes | 5 / 0 would be `inf` | NaN |

1. Make a copy of the table so the input stays safe. Shape stays `(3, 2)`.
2. Look at `views = [10, 4, 0]`. Row 2 is zero, so that denominator must become "missing" before dividing: `[10, 4, NaN]`.
3. Divide row by row: `[3/10, 0/4, 5/NaN] = [0.3, 0.0, NaN]`.
4. Attach the result as a last column named `ctr`. Shape is now `(3, 3)`.
5. Final output (NaN shown as `null`):

```text
clicks: [3, 0, 5]
views:  [10, 4, 0]
ctr:    [0.3, 0.0, null]
```

## Tools you'll need

### df.copy()

- Returns a new DataFrame with its own data.
- Edits to the copy don't touch the original.

```python
import pandas as pd

a = pd.DataFrame({"x": [1, 2]})
b = a.copy()
b["x"] = 99
print(a["x"].tolist())  # [1, 2]
print(b["x"].tolist())  # [99, 99]
```

### Series division (`/`)

- Divides two columns element by element and gives floats.
- Dividing by zero does not raise an error: it gives `inf`, or `NaN` for 0/0.

```python
import pandas as pd

a = pd.Series([6, 0, 4])
b = pd.Series([3, 0, 0])
print((a / b).tolist())  # [2.0, nan, inf]
```

### Series.replace(old, new)

- Returns a new Series with every `old` value swapped for `new`.
- The original Series is unchanged.

```python
import pandas as pd

s = pd.Series([5, 0, 2])
print(s.replace(0, -1).tolist())  # [5, -1, 2]
print(s.tolist())  # [5, 0, 2]
```

### np.nan

- NumPy's NaN value, which you can use as a replacement value.
- Arithmetic with it gives NaN.

```python
import numpy as np

print(7 / np.nan)  # nan
print(np.isnan(np.nan))  # True
```

### df["new"] = values

- Assigning to a column name that doesn't exist yet adds it at the right end.
- Values line up by row index.

```python
import pandas as pd

d = pd.DataFrame({"p": [1, 2]})
d["q"] = d["p"] * 10
print(list(d.columns))  # ['p', 'q']
print(d.shape)  # (2, 2)
```

### Series.mask(cond, other)

- Replaces values where `cond` is True; an alternative if you prefer a condition over `replace`.
- Returns a new Series.

```python
import numpy as np
import pandas as pd

s = pd.Series([4, 0, 9])
print(s.mask(s == 0, np.nan).tolist())  # [4.0, nan, 9.0]
```

## Common mistakes

- **Editing `df` directly.** Writing `df["ctr"] = ...` changes the input. Copy first and add the column to the copy.
- **Leaving `inf` in the column.** `5 / 0` is `inf`, not `NaN`. Neutralise zero denominators before dividing, or fix the result afterwards.
- **Fixing the wrong column.** Only `views` (the denominator) has the zeros that cause trouble. Don't touch `clicks`.
- **Python loops.** Looping over 10^5 rows is slow and unneeded; one column-wise division does it.
- **Breaking column order.** Assigning a new name appends it at the end, which is what you want. Don't rebuild the table in another order.

## Hints

### Hint 1

- Copy the table first.
- Work out the rate for every row at once, making sure rows with zero views end up missing, not infinite.
- Store that result as a new last column on the copy.

### Hint 2

- Copy with `df.copy()`; the result has the same shape as `df`.
- Turn zeros in the `views` column into NaN with `Series.replace`; you get a Series of the same length.
- Divide the `clicks` column by that cleaned Series; the result is again one value per row.
- Assign it to the copy under the name `ctr`.

### Hint 3

- The key step is the denominator: take `views` and swap every 0 for NaN, so `[10, 4, 0]` becomes `[10, 4, NaN]`.
- Divide `clicks` by it element by element: `3/10`, `0/4`, `5/NaN`. The last one is NaN automatically.
- Use the original `df` columns for the division and put the result on the copy.
