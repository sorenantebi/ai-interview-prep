---
topic: "Pandas"
difficulty: Hard
---
# Sessionize Events - Solution

## Intuition

After sorting by user and time, a row starts a new session exactly when it is the user's first row (its within-user time difference is missing) or its difference from the previous row is larger than the gap. A cumulative sum of those "starts" flags numbers the sessions.

## Approach

1. Parse `ts`, remember each row's input position, and sort by user, time, position.
2. `groupby("user")[time].diff()` gives the gap to the user's previous event (`NaT` for the first).
3. `starts = gap.isna() | (gap > Timedelta(minutes=gap_minutes))`; `session = starts.cumsum()`.

## Code

```python
import pandas as pd

def sessionize(df: pd.DataFrame, gap_minutes: int) -> pd.DataFrame:
    d = df.assign(_t=pd.to_datetime(df["ts"]), _pos=range(len(df))).sort_values(["user", "_t", "_pos"])
    gap = d.groupby("user")["_t"].diff()
    starts = gap.isna() | (gap > pd.Timedelta(minutes=gap_minutes))
    d["session"] = starts.cumsum().astype(int)
    return d[["user", "ts", "session"]].reset_index(drop=True)
```

## Complexity

- **Time:** `O(n log n)` — the sort.
- **Space:** `O(n)` — the sorted copy and helper columns.
