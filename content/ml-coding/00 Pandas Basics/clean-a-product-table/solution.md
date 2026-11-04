---
topic: "Pandas Basics"
difficulty: Easy
---
# Clean a Product Table - Solution

## Intuition

Each requirement maps to one standard method: `drop(columns=...)` removes a column, `dropna(subset=...)` removes rows with missing values only in the listed columns, and `reset_index(drop=True)` renumbers the rows. All three return new DataFrames, so the input is left untouched.

## Approach

1. Drop `drop_col` with `df.drop(columns=drop_col)`.
2. Drop the rows with a missing value in any column of `required` with `dropna(subset=required)` (the default `how="any"`).
3. Renumber the index with `reset_index(drop=True)`.

## Code

```python
import pandas as pd

def clean_table(df: pd.DataFrame, drop_col: str, required: list[str]) -> pd.DataFrame:
    return df.drop(columns=drop_col).dropna(subset=required).reset_index(drop=True)
```

## Complexity

Linear in the number of cells: each step makes one pass over the data.
