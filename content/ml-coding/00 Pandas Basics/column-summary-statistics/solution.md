---
topic: "Pandas Basics"
difficulty: Easy
---
# Column Summary Statistics - Solution

## Intuition

`Series.agg` accepts a list of aggregation names and returns one value per name, as a Series indexed by those names. The result keeps the name of the column it was computed from, and NaN values are skipped by default.

## Approach

1. Select the column with `df[col]`.
2. Call `.agg(["mean", "min", "max", "sum"])` on it. The order of the list is the order of the result's index.

## Code

```python
import pandas as pd

def column_stats(df: pd.DataFrame, col: str) -> pd.Series:
    return df[col].agg(["mean", "min", "max", "sum"])
```

## Complexity

`O(n)` for `n` rows: each statistic is a single pass over the column.
