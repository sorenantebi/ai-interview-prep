# Learn: Order Totals

## The idea

- The task: take a small table of orders (one row per item) and add a **total** column equal to price times quantity in each row.
- A **DataFrame** is pandas' table type.
  - Think of it as a dict of columns: each key is a column name, each value is a column of equal length.
- A **Series** is a single column of a DataFrame.
- **Element-wise** means row 0 is combined with row 0, row 1 with row 1, and so on.
- A **vectorised** operation works on whole columns at once, with no Python `for` loop.
  - It is shorter and much faster than looping.
- Where it shows up: building features in an ML pipeline (e.g. `price * quantity`) and computing metrics for an evaluation report.
- **NaN** ("not a number") is how pandas stores a missing value.
  - Any arithmetic with `NaN` gives `NaN`, so a missing price gives a missing total.

## Work it by hand

Example 1: `data = {"item": ["pen", "book"], "price": [1.5, 12.0], "quantity": [4, 2]}`

1. Build the table. It has 2 rows and 3 columns, in the key order of the dict:

| | item | price | quantity |
|---|---|---|---|
| 0 | pen | 1.5 | 4 |
| 1 | book | 12.0 | 2 |

2. Take the two columns you need. Each is a Series of length 2:
   - `price` = [1.5, 12.0]
   - `quantity` = [4, 2]
3. Multiply them element-wise:
   - row 0: 1.5 * 4 = 6.0
   - row 1: 12.0 * 2 = 24.0
   - The result is [6.0, 24.0], still length 2.
4. Store that Series under the new column name `total`. A new column goes at the right-hand end:

| | item | price | quantity | total |
|---|---|---|---|---|
| 0 | pen | 1.5 | 4 | 6.0 |
| 1 | book | 12.0 | 2 | 24.0 |

5. This matches the expected output: `item` = ["pen","book"], `price` = [1.5,12.0], `quantity` = [4,2], `total` = [6.0,24.0].

## Tools you'll need

### pd.DataFrame(dict)

- Builds a table from a dict whose values are equal-length lists.
- Keys become column names, and columns keep the order of the dict.

```python
import pandas as pd

df = pd.DataFrame({"city": ["Bonn", "Köln", "Essen"], "temp": [11.5, 13.0, 9.5]})
print(df.shape)  # (3, 2)
print(list(df.columns))  # ['city', 'temp']
```

### df["col"] (column access)

- Square brackets with a column name return that column as a Series.
- It has one value per row and keeps the row labels.

```python
import pandas as pd

df = pd.DataFrame({"w": [2.0, 3.0], "h": [5.0, 4.0]})
print(df["w"].tolist())  # [2.0, 3.0]
print(df["w"].shape)  # (2,)
```

### Element-wise arithmetic on columns

- Operators like `+`, `-`, `*`, `/` between two Series of the same length work row by row.
- `NaN` in either input gives `NaN` in the output.

```python
import pandas as pd
import numpy as np

a = pd.Series([1.0, 2.0, np.nan])
b = pd.Series([10, 20, 30])
print((a + b).tolist())  # [11.0, 22.0, nan]
```

### df["new"] = ... (column assignment)

- Assigning to a name that doesn't exist yet adds a new column at the end.
- Assigning to an existing name replaces that column.

```python
import pandas as pd

df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
df["diff"] = df["y"] - df["x"]
print(list(df.columns))  # ['x', 'y', 'diff']
print(df["diff"].tolist())  # [2, 2]
```

## Common mistakes

- **Looping over rows.** `iterrows()` works but is slow, and the problem forbids loops.
  - Multiply the two columns directly.
- **Wrong column order.** Don't rebuild a DataFrame with `total` first.
  - Assigning a new name appends it last, which is what you want.
- **Treating `NaN` specially.** You don't need `if` checks or `fillna`.
  - `NaN * 5` is already `NaN`, which is the expected result; filling with 0 would be wrong.
- **Misspelled column names.** Names are case-sensitive, so `df["Price"]` is not `df["price"]`.
  - A wrong name raises a `KeyError`.
- **Forgetting to return the DataFrame.** The assignment changes `df`, but the function must still return it.

## Hints

### Hint 1
- Turn the dict into a DataFrame.
- Compute one value per row from the price and quantity columns.
- Store those values as a new column.
- Return the table.

### Hint 2
- Use `pd.DataFrame(data)` for the table: shape n by 3.
- Select a column with square brackets: a Series of length n.
- Multiply two such Series: another Series of length n.
- Assign it to a new column name: the table is now n by 4.

### Hint 3
- The new column is the price column times the quantity column, taken row by row.
- Assign that product to the column name `"total"` on your DataFrame.
- Missing prices stay missing on their own, so no extra handling is needed.
