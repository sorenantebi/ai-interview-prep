---
topic: "Pandas"
difficulty: Medium
---
# Rolling 7-Day Average - Solution

## Intuition

A time-based rolling window (`"7D"`) looks back a fixed span of time instead of a fixed number of rows, which is exactly "the last 7 calendar days, whichever are present". It needs a sorted datetime column.

## Approach

1. Parse `date` into a datetime column and sort by it.
2. `rolling("7D", on=<datetime column>)["sales"].mean()`: the window `(t − 7 days, t]` covers the date and the 6 days before.
3. Return `date`, `sales`, `avg_7d` with a fresh index.

## Code

```python
import pandas as pd

def rolling_7_day_average(df: pd.DataFrame) -> pd.DataFrame:
    d = df.assign(ts=pd.to_datetime(df["date"])).sort_values("ts")
    d["avg_7d"] = d.rolling("7D", on="ts")["sales"].mean()
    return d[["date", "sales", "avg_7d"]].reset_index(drop=True)
```

## Complexity

- **Time:** `O(n log n)` — the sort; the rolling mean itself is linear.
- **Space:** `O(n)` — the sorted copy.
