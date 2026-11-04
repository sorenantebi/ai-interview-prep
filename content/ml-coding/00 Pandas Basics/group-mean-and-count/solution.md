---
topic: "Pandas Basics"
difficulty: Easy
---
# Group Mean and Count - Solution

## Intuition

`groupby` splits the rows by label. Selecting the `value` column and calling `.mean()` gives the per-group mean, and `.size()` gives the number of rows per group. Both return a Series indexed by the group label (sorted), so they line up when put side by side in a DataFrame.

## Approach

1. Build the grouped column with `df.groupby(key)[value]`.
2. Take `.mean()` and `.size()` of it.
3. Combine the two Series into a DataFrame with columns `"mean"` and `"count"`.

## Code

```python
import pandas as pd

def group_mean_count(df: pd.DataFrame, key: str, value: str) -> pd.DataFrame:
    g = df.groupby(key)[value]
    return pd.DataFrame({"mean": g.mean(), "count": g.size()})
```
