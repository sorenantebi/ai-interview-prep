---
topic: "Pandas"
difficulty: Medium
---
# Deduplicate, Keeping the Latest Row - Solution

## Intuition

Sort so each user's rows run from oldest to newest, with input position as the final tie-break; then the last row of each user is the answer, which `drop_duplicates(keep="last")` keeps.

## Approach

1. Add a parsed timestamp and the original row position as helper columns.
2. Sort by `user_id`, timestamp, position.
3. `drop_duplicates("user_id", keep="last")`, drop the helpers and reset the index.

## Code

```python
import pandas as pd

def latest_per_user(df: pd.DataFrame) -> pd.DataFrame:
    d = df.assign(_t=pd.to_datetime(df["updated_at"]), _pos=range(len(df)))
    d = d.sort_values(["user_id", "_t", "_pos"]).drop_duplicates("user_id", keep="last")
    return d.drop(columns=["_t", "_pos"]).reset_index(drop=True)
```

## Complexity

- **Time:** `O(n log n)` — the sort.
- **Space:** `O(n)` — the sorted copy.
