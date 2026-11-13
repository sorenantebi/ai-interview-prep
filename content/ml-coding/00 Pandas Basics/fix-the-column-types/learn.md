# Learn: Fix the Column Types

## The idea

- The task: each column arrived in the wrong **dtype**, and you convert each one to the type it should have.
- **dtype** (data type): how pandas stores a column, e.g. text (`object`), whole numbers (`int64`), decimals (`float64`), or true/false (`bool`).
- A CSV file has no types at all, so every value can arrive as text.
- Where it shows up: cleaning types is usually the first step of a feature pipeline.
  - You can't average a column of strings.
  - Models expect numbers, not `"yes"` and `"no"`.
- **Series**: one column of a DataFrame.
- **NaN** ("not a number"): pandas' marker for a missing or invalid number.
- Each column needs a different conversion, and the input DataFrame must stay untouched.

## Work it by hand

Example 1 starts like this:

| item | price   | member | count |
|------|---------|--------|-------|
| pen  | "1.50"  | "yes"  | 3     |
| ink  | "2.00"  | "no"   | 0     |
| pad  | "10.25" | "yes"  | 12    |

1. `item`: leave it alone. It stays `"pen"`, `"ink"`, `"pad"`.
2. `price`: parse each string as a decimal number.
   - `"1.50"` becomes `1.5`, `"2.00"` becomes `2.0`, `"10.25"` becomes `10.25`.
   - The column is now `float64`.
3. `member`: look up each label.
   - `"yes"` becomes `True`, `"no"` becomes `False`.
   - Result: `[True, False, True]`, dtype `bool`.
4. `count`: same numbers, stored as decimals. `[3, 0, 12]` becomes `[3.0, 0.0, 12.0]`.
5. The final result keeps the column order and the index `0, 1, 2`:

| item | price | member | count |
|------|-------|--------|-------|
| pen  | 1.50  | True   | 3.0   |
| ink  | 2.00  | False  | 0.0   |
| pad  | 10.25 | True   | 12.0  |

- Example 2: the price `"n/a"` can't be parsed, so that cell becomes `NaN`.
- The rest of that column is still `float64`.

## Tools you'll need

### pd.to_numeric(series, errors=...)

- Converts a Series of strings to numbers.
- The `errors` argument decides what happens to a bad string:
  - `"raise"` (default) stops with an error.
  - `"coerce"` turns the bad value into `NaN`.

```python
import pandas as pd

s = pd.Series(["4.5", "x", "0.25"])
print(pd.to_numeric(s, errors="coerce").tolist())  # [4.5, nan, 0.25]
print(pd.to_numeric(s, errors="coerce").dtype)  # float64
```

### Series.map(dict)

- Replaces each value by looking it up in the dict. The result is a new Series.
- A value that is not a key in the dict becomes `NaN`, so cover every label.

```python
import pandas as pd

s = pd.Series(["red", "green", "red"])
out = s.map({"red": 1, "green": 0})
print(out.tolist())  # [1, 0, 1]
print(out.dtype)  # int64
```

### Series.astype(dtype)

- Returns a new Series converted to another dtype, e.g. `float`, `int`, `str`.
- The original Series is not changed.

```python
import pandas as pd

s = pd.Series([7, 8, 9])
print(s.astype(float).tolist())  # [7.0, 8.0, 9.0]
print(s.astype(str).tolist())  # ['7', '8', '9']
```

### df.assign(name=new_series) and df.copy()

- `assign` returns a **new** DataFrame where the named columns are replaced (or added).
  - Existing columns keep their position.
  - The original is not changed.
- The alternative: `df.copy()`, then `df["col"] = ...` on the copy.

```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [10, 20]})
new = df.assign(a=df["a"] * 100)
print(new["a"].tolist())  # [100, 200]
print(df["a"].tolist())  # [1, 2]
print(list(new.columns))  # ['a', 'b']
```

### df.dtypes

- Shows the dtype of every column. Use it to check your work.

```python
import pandas as pd

df = pd.DataFrame({"x": [1, 2], "y": [0.5, 1.5]})
print(df.dtypes["x"])  # int64
print(df.dtypes["y"])  # float64
```

## Common mistakes

- **Changing the input.** Writing `df["price"] = ...` on the argument modifies the caller's DataFrame.
  - Use `assign`, or call `df.copy()` first.
- **Forgetting `errors="coerce"`.** Without it, `"n/a"` raises a `ValueError` instead of becoming `NaN`.
- **Using `astype(bool)` for `member`.** Every non-empty string, including `"no"`, counts as `True`.
  - Use a dict with `map` instead.
- **Typos in the `map` dict.** A label that isn't a key silently becomes `NaN`.
  - Check the exact spelling of `"yes"` and `"no"`.
- **Changing `item`, the order or the index.** Only touch the three columns that need it.
  - Don't rebuild the DataFrame from scratch.

## Hints

### Hint 1
- Work on one column at a time.
- Convert `price` to numbers.
- Turn `member` into booleans.
- Change `count` to a float type.
- Leave `item` alone.
- Do all of this on a copy, so the input is not modified.

### Hint 2
- `price`: `pd.to_numeric` with an `errors` option gives a Series of floats.
- `member`: `Series.map` with a dict gives a Series of bools.
- `count`: `Series.astype` gives a float Series.
- Put the three new columns into a copy of the DataFrame, e.g. with `df.assign`.

### Hint 3
- For `price`, the `errors` option that turns bad strings into `NaN` is `"coerce"`.
- For `member`, build a dict with two entries and pass it to `map`:
  - the key `"yes"` points to `True`;
  - the key `"no"` points to `False`.
- For `count`, ask `astype` for `float`.
- `assign` takes each column name as a keyword and the new Series as its value.
  - It returns a new DataFrame with the same column order and index.
