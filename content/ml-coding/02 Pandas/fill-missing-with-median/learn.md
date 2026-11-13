# Learn: Fill Missing Values with the Median

## The idea

- The task: for every numeric column, replace each hole with that column's median, and leave text columns alone.
- You must return a new table and not change the one you were given.
- This is **imputation**, a standard step in a feature pipeline, because most models can't train on `NaN`.
- **NaN**: how pandas stores a missing value ("not a number").
- **DataFrame**: a table. A **Series** is one column of it.
- **dtype**: the type of data in a column, such as `int64`, `float64` or `object` (text).
- A column is **numeric** if its dtype is a number type.
- **Median**: the middle value after sorting.
  - With an even count, it is the average of the two middle values.
  - It is less affected by outliers than the mean, which is why it is popular for filling holes.
- Each column gets its own median, computed only from the values that are present.

## Work it by hand

Example 1: `age = [30, NaN, 50, 20]`, `city = ["a", NaN, "b", "c"]`.

1. Find the numeric columns.
   - `age` is numeric.
   - `city` is text, so it is skipped.
2. Collect the present values of `age`: 30, 50, 20. The `NaN` is ignored.
3. Sort them: 20, 30, 50.
4. There are three values, so the median is the middle one: **30**.
5. Replace the `NaN` in `age` with 30. Leave `city` untouched.

| row | age before | age after | city before | city after |
|-----|-----------|-----------|-------------|------------|
| 0   | 30        | 30        | a           | a          |
| 1   | NaN       | **30**    | NaN         | NaN        |
| 2   | 50        | 50        | b           | b          |
| 3   | 20        | 20        | c           | c          |

- Result: `age = [30, 30, 50, 20]`, `city = ["a", null, "b", "c"]`.
- This matches the expected output (numbers shown as floats, `30.00000`).
- Example 2 for practice:
  - `x = [1, 2, NaN]` has median 1.5.
  - `y = [NaN, NaN, 4]` has median 4.

## Tools you'll need

### df.copy()

- Returns a new DataFrame with its own data.
- Changes to the copy don't affect the original.

```python
import pandas as pd

a = pd.DataFrame({"v": [1, 2]})
b = a.copy()
b.loc[0, "v"] = 99
print(a["v"].tolist())  # [1, 2]
print(b["v"].tolist())  # [99, 2]
```

### df.select_dtypes(include)

- Returns only the columns of the given dtype.
- `"number"` matches all integer and float columns.
- Add `.columns` to get just the names.

```python
import pandas as pd

d = pd.DataFrame({"h": [1.5, 2.0], "name": ["x", "y"], "n": [3, 4]})
print(list(d.select_dtypes("number").columns))  # ['h', 'n']
print(d.select_dtypes("number").shape)  # (2, 2)
```

### Series.median() and DataFrame.median()

- Computes the median and skips `NaN` by default (`skipna=True`).
- On a DataFrame it returns one median per column, as a Series indexed by column name.
- A column with only `NaN` gives `NaN`.

```python
import numpy as np
import pandas as pd

d = pd.DataFrame({"a": [4.0, np.nan, 1.0, 10.0], "b": [np.nan] * 4})
print(d.median())
# a    4.0
# b    NaN
# dtype: float64
```

### fillna(value)

- Replaces `NaN` with `value`.
- A scalar is used everywhere.
- A dict or Series is matched to **column names**, so each column gets its own fill value.
- Filling with `NaN` changes nothing.

```python
import pandas as pd

d = pd.DataFrame({"a": [1.0, None], "b": [None, 5.0]})
print(d.fillna({"a": 0.0, "b": -1.0}).values.tolist())
# [[1.0, -1.0], [0.0, 5.0]]
```

### Assigning to several columns

- `df[list_of_names] = other_df` writes several columns back at once.
- Other columns and the column order stay as they were.

```python
import pandas as pd

d = pd.DataFrame({"a": [1, 2], "t": ["u", "v"]})
d[["a"]] = d[["a"]] * 10
print(d["a"].tolist(), list(d.columns))  # [10, 20] ['a', 't']
```

## Common mistakes

- **Modifying the input.** Assigning into `df` changes the caller's data. Copy first and work only on the copy.
- **Touching text columns.** A median on text fails or gives nonsense. Pick the numeric columns with `select_dtypes` first.
- **Using the mean.** The task says median. Example 2 gives 1.5 either way, but other data would not match.
- **Pre-cleaning the `NaN`s.** pandas already skips them, so don't drop rows or fill with 0 before taking the median.
- **Special-casing edge cases.** An all-`NaN` column has median `NaN`, so filling leaves it `NaN`. An empty DataFrame should work too.

## Hints

### Hint 1

- Make a copy of the table.
- Find which columns are numeric.
- Compute one median per numeric column.
- Fill the holes in those columns, each with its own median.
- Return the copy.

### Hint 2

- `copy()` gives a safe table to edit.
- `select_dtypes("number")` gives the numeric columns, still a table.
- `.median()` on that part gives a Series of medians, one per column name.
- `fillna(...)` with that Series fills each column with its own median.
- Write the filled columns back into the copy with `out[names] = ...`.

### Hint 3

- Given a Series, `fillna` looks up each column's name in the Series index. It uses the matching value for that column's `NaN`s.
- So one call on the numeric part is enough, passing the medians of that same numeric part.
- Assign the result back to those same column names in the copy. Text columns are then never touched.
- All-`NaN` columns need no special handling.
