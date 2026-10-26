---
topic: "Pandas"
difficulty: Easy
---
# Add a Ratio Column - Solution

## Intuition

Division by zero in pandas gives `inf` (or `NaN` for 0/0). Replacing zero denominators with `NaN` first makes every undefined rate `NaN`.

## Approach

1. Copy `df` so the input stays untouched.
2. Divide `clicks` by `views` with zeros replaced by `np.nan`.
3. Store the result as the new `ctr` column.

## Code

```python
import numpy as np
import pandas as pd

def add_ctr(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ctr"] = df["clicks"] / df["views"].replace(0, np.nan)
    return out
```

## Complexity

- **Time:** `O(n)` — one vectorised division.
- **Space:** `O(n)` — the copy and the new column.
