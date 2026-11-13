# Learn: Fill Missing Values with the Group Mean

## The idea

- The task: replace each missing price with a sensible guess, the average price of products in the same category.
- **NaN** ("not a number") is pandas' marker for "no value here".
- **Imputation** means filling gaps in data with estimated values.
  - It shows up in feature pipelines, because many models can't accept `NaN` as input.
  - A group average is usually a better guess than one global number.
- **groupby** splits rows into buckets by a column (here `category`), so you can compute something per bucket.
- The **mean** skips `NaN` values: the mean of `[10, NaN, 20]` is 15.
- Two edge cases need a fallback:
  - A category has no known prices at all.
  - A row's category is itself missing.
- In both cases, use the mean of all known prices.
- If no price is known anywhere, the value stays `NaN`.

## Work it by hand

Example 1:

| row | category | price |
|---|---|---|
| 0 | a | 10.0 |
| 1 | a | NaN |
| 2 | b | 4.0 |
| 3 | a | 20.0 |

1. Split by category.
   - Group `a` holds rows 0, 1, 3, with known prices 10 and 20.
   - Group `b` holds row 2, with known price 4.
2. Take the mean of the known prices in each group.
   - `a`: (10 + 20) / 2 = 15.
   - `b`: 4.
3. Give every row its group's mean, in the original row order: `[15, 15, 4, 15]`.
4. Fill only the gaps.
   - Rows 0, 2, 3 keep their own price.
   - Row 1 takes 15.
5. Result: `[10.0, 15.0, 4.0, 20.0]`, which matches the expected output.

- No fallback was needed here.
- In Example 2, category `b` has no known prices, so its group mean is `NaN`. The overall mean 6.0 takes over.

## Tools you'll need

### `df.groupby("col")["other"].transform("mean")`

- **transform** computes a per-group result but returns one value per original row, with the same length and index as the input.
- `.mean()` is different: it returns one row per group.
- `NaN`s are skipped, and a group with only `NaN`s gives `NaN`.

```python
import pandas as pd
df = pd.DataFrame({"team": ["x", "y", "x", "y"], "score": [1.0, 5.0, 3.0, 9.0]})
print(df.groupby("team")["score"].mean().tolist())  # [2.0, 7.0]
print(df.groupby("team")["score"].transform("mean").tolist())  # [2.0, 7.0, 2.0, 7.0]
```

```python
import numpy as np
import pandas as pd
d = pd.DataFrame({"g": ["p", "p", "q"], "v": [2.0, np.nan, np.nan]})
print(d.groupby("g")["v"].transform("mean").tolist())  # [2.0, 2.0, nan]
```

### `Series.fillna(value)`

- Replaces `NaN` and returns a new Series.
- `value` can be one number, or a Series: each gap then takes the value at the same index label.
- Known values are never touched.

```python
import numpy as np
import pandas as pd
s = pd.Series([1.0, np.nan, 3.0])
print(s.fillna(0.0).tolist())  # [1.0, 0.0, 3.0]
print(s.fillna(pd.Series([9.0, 8.0, 7.0])).tolist())  # [1.0, 8.0, 3.0]
```

- Calls can be chained: a second `fillna` only affects what the first left empty.

```python
import numpy as np
import pandas as pd
s = pd.Series([np.nan, np.nan, 5.0])
print(s.fillna(pd.Series([np.nan, 2.0, 1.0])).fillna(-1.0).tolist())  # [-1.0, 2.0, 5.0]
```

### `Series.mean()`

- The average of the known values.
- It skips `NaN` by default, and returns `NaN` if nothing is known.

```python
import numpy as np
import pandas as pd
print(pd.Series([2.0, np.nan, 4.0]).mean())  # 3.0
print(pd.Series([np.nan, np.nan]).mean())  # nan
```

### `df.copy()`

- Makes an independent copy, so edits to it don't change the original.

```python
import pandas as pd
a = pd.DataFrame({"x": [1, 2]})
b = a.copy()
b.loc[0, "x"] = 99
print(a["x"].tolist(), b["x"].tolist())  # [1, 2] [99, 2]
```

## Common mistakes

- **Using `.mean()` instead of `.transform("mean")`.**
  - `.mean()` gives one row per category, so it can't line up with the rows.
  - `transform` keeps the original length and index.
- **Forgetting the fallback.**
  - A category with only `NaN` prices has a `NaN` group mean, so the gap stays.
  - Rows with a missing category also get `NaN`, because groupby skips `NaN` keys by default.
  - A second fill step with the overall mean fixes both.
- **Computing the fallback from the already-filled column.**
  - Take the overall mean from the original known prices.
  - Otherwise the filled-in group means leak into it.
- **Modifying `df` in place.**
  - The task says `df` must stay unchanged, so work on a copy.
- **Reordering or resetting the index.**
  - Don't sort or call `reset_index`.
  - Index-aligned `fillna` only works if the index stays as it was.

## Hints

### Hint 1
- Make a copy of the data.
- Work out a per-row "group average" for the price column.
- Fill the gaps using it.
- Fill whatever is still empty with the overall average of the known prices.

### Hint 2
- Get one group mean per row with `transform("mean")`; the result has the same length and index as `df`.
- Fill the price gaps with that Series, using `fillna`.
- Fill again with a single number from `Series.mean()` on the original prices.
- Assign the result back to the copy's `price` column.

### Hint 3
- After the first fill, a row is still empty only if its group had no known price, or its category was missing.
- The second fill takes a single number: the mean of the original `price` column, which already skips `NaN`.
- If every price was missing, that number is `NaN`, so those values correctly stay missing.
- Assign the final Series to the `price` column of the copy and return the copy.
