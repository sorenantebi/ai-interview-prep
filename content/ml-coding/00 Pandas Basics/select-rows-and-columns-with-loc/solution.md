---
topic: "Pandas Basics"
difficulty: Easy
---
# Select Rows and Columns with .loc - Solution

## Intuition

`.loc` selects by label. Giving it a list of row labels and a list of column labels returns exactly that sub-table, in the order you listed the labels, and because both are lists the result is always a DataFrame.

## Approach

1. Make the `name` column the index with `set_index("name")` (this returns a new frame, `df` is unchanged).
2. Call `.loc[names, columns]` with the row labels first and the column labels second.
3. Return the result.

## Code

```python
import pandas as pd

def select_rows_cols(df: pd.DataFrame, names: list[str], columns: list[str]) -> pd.DataFrame:
    return df.set_index("name").loc[names, columns]
```
