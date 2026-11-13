# Learn: Load a CSV Table with an Index Column

## The idea

- The task: turn a block of CSV text into a table, use one named column as the row labels, and throw away incomplete rows.
- **CSV** is plain text: a header line with column names, then one line per row, values separated by commas.
- **DataFrame** is pandas' table type, with named columns and a label for each row.
- **Index** is the row axis, the labels that name each row.
  - By default pandas labels rows 0, 1, 2, ...
  - An item name or sensor id is often a better label.
  - A column used as the index is no longer a normal column.
- **NaN** ("not a number") is pandas' marker for a missing value.
  - An empty CSV field is read as `NaN`.
- **File-like object** is anything that behaves like an open file.
  - `read_csv` expects a path or a file-like object, not raw text.
- Where it shows up: this load-and-clean step opens almost every data pipeline, before computing statistics or training a model.

## Work it by hand

Example 1 text:

```text
item,price,stock
apple,1.5,10
pear,2.0,4
plum,0.8,25
```

1. Read the header: the columns are `item`, `price`, `stock`.
2. Split each line at the commas:

| item | price | stock |
|---|---|---|
| apple | 1.5 | 10 |
| pear | 2.0 | 4 |
| plum | 0.8 | 25 |

3. `index_col = "item"`: move `item` out of the data and use it as the row labels.
   - Now there are 3 rows and 2 columns (`price`, `stock`).
4. Check for missing values.
   - Every cell is filled, so no row is removed.
5. Read the result as `{column: {row label: value}}`:
   - `{"price":{"apple":1.5,"pear":2.0,"plum":0.8},"stock":{"apple":10,"pear":4,"plum":25}}`
   - `price` has decimals, so it is float. `stock` has only whole numbers, so it stays integer.

## Tools you'll need

### io.StringIO(text)

- Wraps a string so it behaves like a file held in memory.
- Pass the wrapper to functions that expect a file.

```python
import io

f = io.StringIO("a,b\n1,2\n")
print(f.read())
# a,b
# 1,2
```

### pd.read_csv(source, index_col=...)

- Parses CSV into a `DataFrame`. The first line is the header by default.
- `index_col` takes a column name and uses that column as the row index.
- Empty fields become `NaN`.

```python
import io
import pandas as pd

df = pd.read_csv(io.StringIO("name,x,y\nu,1,2\nv,3,4\n"), index_col="name")
print(df.shape)  # (2, 2)
print(list(df.columns))  # ['x', 'y']
print(list(df.index))  # ['u', 'v']
```

### DataFrame.dropna()

- Returns a new frame without the rows that contain any `NaN`.
- By default it checks every column. The index is not a column, so it is not checked.
- It keeps the order of the remaining rows.
- It does not change the original unless you pass `inplace=True`.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"a": [1.0, np.nan, 3.0], "b": [4.0, 5.0, np.nan]},
                  index=["r1", "r2", "r3"])
print(df.dropna())
#       a    b
# r1  1.0  4.0
print(df.shape, df.dropna().shape)  # (3, 2) (1, 2)
```

### DataFrame.isna()

- Marks which cells are `NaN`. Handy for checking what `dropna` will remove.
- Chain `.sum()` to count missing values per column.

```python
import io
import pandas as pd

df = pd.read_csv(io.StringIO("p,q\n1,\n2,5\n"))
print(df.isna().sum().to_dict())  # {'p': 0, 'q': 1}
```

## Common mistakes

- **Passing the raw string to `read_csv`.**
  - Pandas treats a string as a file path.
  - Wrap it in `io.StringIO` first.
- **Leaving the key column as a normal column.**
  - Use `index_col` in `read_csv` so it is moved out while reading.
  - Otherwise `dropna` would also check that column.
- **Ignoring the return value of `dropna`.**
  - `df.dropna()` returns a new frame.
  - Calling it without using the result changes nothing.
- **Expecting `dropna` to check the index.**
  - It only looks at the data columns.
- **Being surprised by floats.**
  - A column with a gap is read as float, so `40` becomes `40.0`.
  - The column stays float after the gappy rows are dropped, as Example 2 shows.

## Hints

### Hint 1
- Turn the string into something pandas can read like a file.
- Parse it so the chosen column becomes the row labels.
- Remove the incomplete rows.
- Return the result.

### Hint 2
- `io.StringIO` wraps the text as a file-like object.
- `pd.read_csv` with `index_col` gives a frame whose index is that column and whose other columns are the data.
- `dropna` removes rows with missing values and returns a new frame.

### Hint 3
- `read_csv` already reads empty fields as `NaN`, so no conversion is needed.
- `dropna()` with no arguments drops a row if any of its cells is `NaN`.
- It only checks the data columns, because the index column was already moved out.
- Return the result of `dropna()`, since it makes a new frame.
