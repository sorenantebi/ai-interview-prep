# Learn: Clean a Survey Table

## The idea

- **The task:** fix two kinds of mess in a table, and hand back a cleaned copy.
  - Fill the empty cells, using a default chosen per column.
  - Correct misspelled labels, using a fix list chosen per column.
- **Where it shows up:** this is the first step of almost every feature pipeline, before you count, group, or feed data to a model.
- **DataFrame:** a table with named columns, pandas' main data structure.
- **Missing value:** an empty cell, shown as `NaN` (or `None`) in pandas.
- **Nested dict:** a dict whose values are dicts. Here it looks like `{column: {old: new}}`.
- **Order matters:** fill first, then replace, so a default you just inserted can also be corrected by `fixes`.
- **Copy:** both tools return a new DataFrame, so the input stays untouched.

## Work it by hand

Example 1 starts as this table:

```text
   city     age
0  Berlin   25.0
1  Bon      NaN
2  NaN      31.0
3  Bonn     NaN
```

1. **Read the inputs.**
   - `defaults = {"city": "unknown", "age": 30.0}`
   - `fixes = {"city": {"Bon": "Bonn"}}`
2. **Fill missing values.**
   - `city` gap in row 2 becomes `"unknown"`.
   - `age` gaps in rows 1 and 3 become `30.0`.

```text
   city     age
0  Berlin   25.0
1  Bon      30.0
2  unknown  31.0
3  Bonn     30.0
```

3. **Apply fixes.**
   - Only `city` is named, so only that column is searched.
   - Row 1 changes from `"Bon"` to `"Bonn"`.
   - `age` is not named, so it stays as is.

```text
   city     age
0  Berlin   25.0
1  Bonn     30.0
2  unknown  31.0
3  Bonn     30.0
```

4. **Check.**
   - This matches the expected output.
   - The index (0 to 3) and the columns are unchanged.

## Tools you'll need

### df.fillna(dict)

- Fills missing values. With a dict, each key is a column name and each value is the fill for that column.
- Columns not in the dict keep their `NaN`.
- Returns a new DataFrame.

```python
import pandas as pd

t = pd.DataFrame({"x": [1.0, None], "y": ["a", None], "z": [None, 5.0]})
out = t.fillna({"x": 0.0, "y": "?"})
print(out["x"].tolist())  # [1.0, 0.0]
print(out["y"].tolist())  # ['a', '?']
print(out["z"].tolist())  # [nan, 5.0]
```

### df.replace(nested dict)

- Swaps values for other values.
- With `{column: {old: new}}`, each inner mapping applies only to its own column.
- Other columns are untouched, and a new DataFrame is returned.

```python
import pandas as pd

t = pd.DataFrame({"c": ["red", "rde", "blue"], "n": ["rde", "x", "y"]})
out = t.replace({"c": {"rde": "red"}})
print(out["c"].tolist())  # ['red', 'red', 'blue']
print(out["n"].tolist())  # ['rde', 'x', 'y']
```

- Note that `"rde"` in column `n` stayed, because the mapping names only `c`.

### Method chaining

- Both methods return a DataFrame, so you can call the next method on the result.
- The steps run left to right.

```python
import pandas as pd

t = pd.DataFrame({"v": [1, 2, 3]})
print(t.replace({"v": {1: 10}}).replace({"v": {10: 99}})["v"].tolist())  # [99, 2, 3]
```

## Common mistakes

- **Wrong order.**
  - Replacing before filling means a default like `"unknown"` never gets corrected by `fixes`.
  - Fill first, then replace.
- **Passing a single value to `fillna`.**
  - `fillna(0)` fills every column, including ones that should keep their `NaN`.
  - Pass a dict.
- **Flat dict in `replace`.**
  - `{"Bon": "Bonn"}` applies to every column.
  - Use the nested form so only the named column changes.
- **Modifying the input.**
  - Don't assign into `df` or use `inplace=True`.
  - Both methods already return a copy.
- **Writing a loop.**
  - Looping over rows or columns is slow and unnecessary.
  - The dict forms handle all columns at once.

## Hints

### Hint 1

- Do two passes over the table.
- First deal with the missing values.
- Then correct the misspelled labels.
- Keep that order, and return the result.

### Hint 2

- Use `fillna` with the `defaults` dict for the first step. The result is a DataFrame of the same shape as the input.
- Use `replace` with the `fixes` dict on that result. The shape is still the same.

### Hint 3

- `fillna` takes the dict as it is: each key is a column, each value is what goes into that column's gaps.
- `replace` takes the nested dict as it is: the outer key picks the column, the inner dict lists `old: new` pairs.
- Call the first, call the second on its result, and return that.
- Neither call needs a loop or `inplace`.
