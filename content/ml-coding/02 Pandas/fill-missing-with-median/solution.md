---
topic: "Pandas"
difficulty: Easy
---
# Fill Missing Values with the Median - Solution

## Intuition

`fillna` accepts a Series of fill values keyed by column name, and `median()` skips `NaN` by default, so one call fills every numeric column at once.

## Approach

1. Copy `df`.
2. Select the numeric columns with `select_dtypes("number")`.
3. Fill them with `fillna(medians)`, where `medians` is their column-wise median.

## Code

```python
import pandas as pd

def fill_with_median(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    numeric = out.select_dtypes("number").columns
    out[numeric] = out[numeric].fillna(out[numeric].median())
    return out
```

## Complexity

- **Time:** `O(n·c)` — a median per column is linear on average.
- **Space:** `O(n·c)` — the copy.
