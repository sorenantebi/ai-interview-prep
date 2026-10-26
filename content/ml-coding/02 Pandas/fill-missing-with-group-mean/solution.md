---
topic: "Pandas"
difficulty: Medium
---
# Fill Missing Values with the Group Mean - Solution

## Intuition

`groupby(...).transform("mean")` returns a group mean for every row, aligned with the original index, which is exactly the fill value each row needs. A second `fillna` with the overall mean covers groups that had nothing to average.

## Approach

1. Compute the per-row category mean with `transform("mean")`.
2. Fill missing prices with it.
3. Fill whatever is still missing with the overall mean of the original prices.

## Code

```python
import pandas as pd

def fill_with_group_mean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    group_mean = out.groupby("category")["price"].transform("mean")
    out["price"] = out["price"].fillna(group_mean).fillna(df["price"].mean())
    return out
```

## Complexity

- **Time:** `O(n)` — one grouped pass (hash grouping).
- **Space:** `O(n)` — the copy and the per-row means.
