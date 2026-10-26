---
topic: "Pandas"
difficulty: Medium
---
# Rank Within Group - Solution

## Intuition

`groupby(...).rank()` ranks inside each group while keeping the original rows aligned. `method="dense"` gives tied values the same rank without leaving gaps.

## Approach

1. Copy `df`.
2. `groupby("dept")["salary"].rank(method="dense", ascending=False)`.
3. Convert the ranks (floats) to `int` and store them in `rank`.

## Code

```python
import pandas as pd

def rank_in_department(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["rank"] = out.groupby("dept")["salary"].rank(method="dense", ascending=False).astype(int)
    return out
```

## Complexity

- **Time:** `O(n log n)` — sorting salaries within each group.
- **Space:** `O(n)` — the copy and the ranks.
